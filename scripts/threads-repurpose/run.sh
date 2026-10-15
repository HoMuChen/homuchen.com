#!/usr/bin/env bash
# 排程：把已發布的部落格文章拆成多個 idea，一則一則發到 Threads。
#
# 每次執行：
#   1. 同步到最新 main（含補 commit / push 上次沒完成的結果）
#   2. 發布「一則」status: approved 的貼文（檔名排序最前面的）
#   3. 待發的貼文（draft + approved）少於 THREADS_MIN_QUEUE 則，就請 Claude 挑一篇文章拆成新的一批
#
#   THREADS_MODE=review（預設）  新草稿是 draft，要人工改成 approved 才會發
#   THREADS_MODE=auto            新草稿驗證通過就直接標成 approved，依序自動發
#   THREADS_SKIP_GENERATE=1      這次不產生新的
#   THREADS_SKIP_PUBLISH=1       這次不發布
#   THREADS_POST=<slug>          指定要拆的文章（不看佇列，一定產生一批）
#
# 在 hq VM 以 threads 帳號由 systemd timer 執行（見同資料夾 systemd/、README.md）。
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../.." && pwd)
cd "$REPO"
HERE=scripts/threads-repurpose
MODE=${THREADS_MODE:-review}
MIN_QUEUE=${THREADS_MIN_QUEUE:-3}
TODAY=$(TZ=Asia/Taipei date +%F)
STATE=${XDG_STATE_HOME:-$HOME/.local/state}/threads-repurpose
mkdir -p "$STATE"

log() { printf '[%s] %s\n' "$(TZ=Asia/Taipei date '+%F %T')" "$*"; }
field() { python3 $HERE/thread_file.py field "$1" "$2"; }

exec 9>"$STATE/lock"
flock -n 9 || { log "another run is in progress, skip"; exit 0; }

push() {
  for i in 1 2 3; do
    git pull --rebase -q origin main && git push -q origin HEAD:main && return 0
    log "push failed (attempt $i), retrying"
    sleep 10
  done
  log "push failed; the commit stays local and will be pushed next run"
  return 1
}

commit() { # commit <message> <files...>
  local msg=$1
  shift
  git add -- "$@"
  git commit -q -m "$msg" -m "Automated by scripts/threads-repurpose on hq."
  push || true
}

# 新格式（一篇拆多則）的檔案：threads/{date}-{slug}-{nn}.md
batch_files() { find threads -maxdepth 1 -regextype posix-extended -regex '.*/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+-[0-9]{2}\.md' | sort; }

# ── 1. 同步 ────────────────────────────────────────────────
sync_repo() {
  local dirty f ok=1
  dirty=$(git status --porcelain --untracked-files=all)
  if [ -n "$dirty" ]; then
    # 上次發布成功但 commit 前中斷：只允許 threads/ 底下 published / failed 的檔案
    while read -r _ f; do
      case "$f" in
        threads/*.md)
          case "$(field "$f" status)" in
            published | failed) ;;
            *) ok=0 ;;
          esac ;;
        *) ok=0 ;;
      esac
    done <<<"$dirty"
    if [ "$ok" = 1 ]; then
      log "recovering uncommitted results: $(echo "$dirty" | awk '{print $2}' | tr '\n' ' ')"
      git add -- threads/
      git commit -q -m "Record Threads publish results (recovered)" -m "Automated by scripts/threads-repurpose on hq."
    else
      log "working tree has unexpected changes, refusing to run:"
      echo "$dirty"
      exit 1
    fi
  fi
  git pull --rebase -q origin main
  if [ -n "$(git log origin/main..HEAD --oneline)" ]; then
    push || true
  fi
}

# ── 2. 發布一則 ─────────────────────────────────────────────
publish() { # publish <file>
  local f=$1 name json ids url
  name=$(basename "$f" .md)
  json=$(mktemp) ids=$(mktemp)
  python3 $HERE/thread_file.py posts-json "$f" "$json"
  if python3 .agents/skills/post-to-threads/scripts/post_threads.py "$json" --ids-out "$ids"; then
    url=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("permalink") or "")' "$ids")
    python3 $HERE/thread_file.py set-status "$f" published "$url"
    log "published $f → ${url:-(no permalink)}"
    commit "Publish Threads post: $name" "$f"
  else
    # 可能已發出部分貼文：標成 failed 不再重試，留給人工處理
    python3 $HERE/thread_file.py set-status "$f" failed
    log "publish FAILED for $f (marked failed; check Threads for partial posts)"
    commit "Threads publish failed: $name" "$f"
  fi
  rm -f "$json" "$ids"
}

publish_next() {
  local f
  for f in threads/*.md; do
    [ "$(field "$f" status)" = approved ] || continue
    if python3 $HERE/thread_file.py check "$f"; then
      publish "$f"
      return 0
    fi
    log "skip $f: approved but fails validation (fix it or set another status)"
  done
  log "nothing approved to publish"
}

# ── 3. 產生新的一批 ─────────────────────────────────────────
queue_size() {
  local f n=0
  for f in $(batch_files); do
    case "$(field "$f" status)" in draft | approved) n=$((n + 1)) ;; esac
  done
  echo "$n"
}

generate() {
  local prompt out new files f bad=0
  prompt=$(sed "s/{TODAY}/$TODAY/g" $HERE/prompt.md)
  if [ -n "${THREADS_POST:-}" ]; then
    prompt="$prompt

## 這次指定文章

這次已經指定要拆 /posts/${THREADS_POST}/，跳過「挑文章」步驟，直接用這篇。"
  fi
  out="$STATE/claude-$(date +%Y%m%dT%H%M%S).json"
  log "asking Claude to pick a post and split it into ideas"
  timeout 30m claude -p "$prompt" \
    --allowedTools "Read" "Glob" "Grep" "Write" "Skill" \
    "Bash(python3 .agents/skills/gsc/scripts/gsc.py:*)" \
    --max-turns 80 --output-format json >"$out" 2>&1 || log "claude exited non-zero, see $out"
  python3 -c 'import json,sys
try:
  d=json.load(open(sys.argv[1]))
  print("claude:", d.get("subtype"), "turns", d.get("num_turns"), "est. $%.2f" % (d.get("total_cost_usd") or 0))
  print("result:", (d.get("result") or "")[:400])
except Exception as e:
  print("claude output not JSON:", e)' "$out"

  new=$(git status --porcelain --untracked-files=all)
  if [ -z "$new" ]; then
    log "Claude did not create any file"
    return 1
  fi
  if echo "$new" | grep -qv '^?? threads/[^/]*\.md$'; then
    log "unexpected changes from Claude, stashing them:"
    echo "$new"
    git stash push -u -q -m "threads-repurpose rejected $(date +%F_%T)"
    return 1
  fi
  files=$(echo "$new" | awk '{print $2}' | sort)
  for f in $files; do
    python3 $HERE/thread_file.py check "$f" || bad=1
  done
  if [ "$bad" = 1 ]; then
    log "batch failed validation, stashing it"
    git stash push -u -q -m "threads-repurpose invalid batch $(date +%F_%T)"
    return 1
  fi
  if [ "$MODE" = auto ]; then
    for f in $files; do python3 $HERE/thread_file.py set-status "$f" approved; done
  fi
  log "new batch OK ($(echo "$files" | wc -l | tr -d ' ') posts, mode=$MODE)"
  # shellcheck disable=SC2086
  commit "Draft Threads posts: $(basename "$(echo "$files" | head -1)" .md | sed -E 's/^[0-9-]{11}//; s/-[0-9]{2}$//')" $files
}

SELF_HASH=$(sha256sum "$0" | cut -d' ' -f1)
sync_repo
# pull 之後腳本本身更新了 → 用新版重跑一次（bash 已經讀進舊版）
if [ "$(sha256sum "$0" | cut -d' ' -f1)" != "$SELF_HASH" ] && [ -z "${THREADS_REEXEC:-}" ]; then
  log "run.sh was updated by the pull, re-executing the new version"
  exec 9>&-
  THREADS_REEXEC=1 exec "$0" "$@"
fi
[ "${THREADS_SKIP_PUBLISH:-0}" = 1 ] || publish_next

if [ -n "${THREADS_POST:-}" ]; then
  log "THREADS_POST=$THREADS_POST, generating a batch for it"
  generate || true
elif [ "${THREADS_SKIP_GENERATE:-0}" != 1 ]; then
  q=$(queue_size)
  if [ "$q" -lt "$MIN_QUEUE" ]; then
    log "queue has $q pending posts (< $MIN_QUEUE), generating a new batch"
    generate || true
  else
    log "queue has $q pending posts, no new batch needed"
  fi
fi
log "done"

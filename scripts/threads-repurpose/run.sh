#!/usr/bin/env bash
# 排程：從已發布文章挑一篇改寫成 Threads 串文（Claude 寫），驗證後發布（腳本發），commit + push。
#
#   THREADS_MODE=review（預設）  只寫草稿並 commit/push，不發布；另外會發布狀態改成 approved 的草稿
#   THREADS_MODE=auto            寫完驗證通過就直接發布
#   THREADS_SKIP_GENERATE=1      這次不寫新的，只處理 approved / 補 push
#
# 在 hq VM 以 threads 帳號由 systemd timer 執行（見同資料夾 systemd/）。
set -euo pipefail

REPO=$(cd "$(dirname "$0")/../.." && pwd)
cd "$REPO"
HERE=scripts/threads-repurpose
MODE=${THREADS_MODE:-review}
TODAY=$(TZ=Asia/Taipei date +%F)
STATE=${XDG_STATE_HOME:-$HOME/.local/state}/threads-repurpose
mkdir -p "$STATE"

log() { printf '[%s] %s\n' "$(TZ=Asia/Taipei date '+%F %T')" "$*"; }

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

commit() { # commit <file> <message>
  git add -- "$1"
  git commit -q -m "$2" -m "Automated by scripts/threads-repurpose on hq."
  push || true
}

# ── 1. 同步：先處理上次留下的東西，再 pull 到最新 main ─────────────
sync_repo() {
  local dirty
  dirty=$(git status --porcelain --untracked-files=all)
  if [ -n "$dirty" ]; then
    # 上次發布成功但 commit 前中斷：只允許 threads/ 底下狀態是 published/failed 的檔案
    local f ok=1
    while read -r _ f; do
      case "$f" in
        threads/*.md)
          case "$(python3 $HERE/thread_file.py field "$f" status)" in
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

# ── 發布一個檔案 ─────────────────────────────────────────────
publish() { # publish <file>
  local f=$1 slug json ids url
  slug=$(basename "$f" .md | cut -d- -f4-)
  if ! python3 $HERE/thread_file.py check "$f"; then
    log "validation failed, not publishing $f"
    return 1
  fi
  json=$(mktemp) ids=$(mktemp)
  python3 $HERE/thread_file.py posts-json "$f" "$json"
  if python3 .agents/skills/post-to-threads/scripts/post_threads.py "$json" --ids-out "$ids"; then
    url=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("permalink") or "")' "$ids")
    python3 $HERE/thread_file.py set-status "$f" published "$url"
    log "published $f → ${url:-(no permalink)}"
    commit "$f" "Publish Threads thread: $slug"
  else
    # 可能已發出部分貼文：標成 failed 不再重試，留給人工處理
    python3 $HERE/thread_file.py set-status "$f" failed
    log "publish FAILED for $f (marked failed; check Threads for partial posts)"
    commit "$f" "Threads publish failed: $slug"
  fi
  rm -f "$json" "$ids"
}

# ── 2. 用 Claude 寫一篇新草稿 ─────────────────────────────────
generate() {
  local prompt out new
  prompt=$(sed "s/{TODAY}/$TODAY/g" $HERE/prompt.md)
  out="$STATE/claude-$(date +%Y%m%dT%H%M%S).json"
  log "asking Claude to pick a post and write a thread"
  timeout 30m claude -p "$prompt" \
    --allowedTools "Read" "Glob" "Grep" "Write" "Skill" \
    "Bash(python3 .agents/skills/gsc/scripts/gsc.py:*)" \
    --max-turns 60 --output-format json >"$out" 2>&1 || {
    log "claude exited non-zero, see $out"
  }
  python3 -c 'import json,sys
try:
  d=json.load(open(sys.argv[1]))
  print("claude:", d.get("subtype"), "turns", d.get("num_turns"), "cost $%.2f" % (d.get("total_cost_usd") or 0))
  print("result:", (d.get("result") or "")[:300])
except Exception as e:
  print("claude output not JSON:", e)' "$out"

  new=$(git status --porcelain --untracked-files=all)
  local count
  count=$(echo "$new" | grep -c '^?? threads/.*\.md$' || true)
  if [ -z "$new" ]; then
    log "Claude did not create any file"
    return 1
  fi
  if [ "$count" != 1 ] || [ "$(echo "$new" | wc -l)" != 1 ]; then
    log "unexpected changes from Claude, stashing them:"
    echo "$new"
    git stash push -u -q -m "threads-repurpose rejected $(date +%F_%T)"
    return 1
  fi
  NEW_FILE=$(echo "$new" | awk '{print $2}')
  if ! python3 $HERE/thread_file.py check "$NEW_FILE"; then
    log "draft failed validation, stashing it"
    git stash push -u -q -m "threads-repurpose invalid $NEW_FILE"
    return 1
  fi
  log "draft OK: $NEW_FILE"
}

sync_repo

# 先發布人工審過（status: approved）的草稿
for f in threads/*.md; do
  if [ "$(python3 $HERE/thread_file.py field "$f" status)" = approved ]; then
    publish "$f" || true
  fi
done

if [ "${THREADS_SKIP_GENERATE:-0}" != 1 ]; then
  NEW_FILE=
  if generate; then
    if [ "$MODE" = auto ]; then
      publish "$NEW_FILE"
    else
      commit "$NEW_FILE" "Draft Threads thread for review: $(basename "$NEW_FILE" .md | cut -d- -f4-)"
      log "review mode: draft committed. Set 'status: approved' to publish it on the next run."
    fi
  fi
fi
log "done"

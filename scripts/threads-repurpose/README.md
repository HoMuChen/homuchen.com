# threads-repurpose

排程把已發布的部落格文章改寫成 Threads 串文。跑在 hq VM 的 `threads` 帳號（見 homuchen-edge README「使用者帳號」）。

```
systemd timer（週二、四、六 09:00 台北）
 └ run.sh
    1. flock；處理上次沒 commit/push 的結果；git pull --rebase 到最新 main
    2. 發布 status: approved 的草稿
    3. claude -p（prompt.md）：gsc skill 挑文章 → 讀過去的 threads/ → 寫 threads/{date}-{slug}.md
       權限只有 Read/Glob/Grep/Write/Skill + gsc.py，不能跑 git、不能發文
    4. thread_file.py check：frontmatter、3–10 則、每則 ≤500 字、連結只在最後一則且指向原文、不用「掰掰」、沒改寫過
    5. review 模式：commit/push 草稿；auto 模式：post_threads.py 發布 → 回寫 status/threads_url → commit/push
```

- Claude 產生其他檔案或草稿驗證失敗 → `git stash` 收起來（`git stash list` 看得到），這次不發。
- 發布失敗 → 標 `status: failed` 並 commit，不會自動重試（Threads 上可能有部分貼文，要人工看）。
- 審稿：review 模式下把草稿的 `status: draft` 改成 `approved` 並 push，下次排程會發布它。
- log：`journalctl -u threads-repurpose`；Claude 的完整輸出在 `~/.local/state/threads-repurpose/claude-*.json`。

## 安裝（root）

```bash
install -m 644 /home/threads/homuchen.com/scripts/threads-repurpose/systemd/threads-repurpose.{service,timer} /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now threads-repurpose.timer
systemctl list-timers threads-repurpose.timer
```

手動跑一次：`systemctl start threads-repurpose.service`（或以 threads 帳號 `THREADS_SKIP_GENERATE=1 scripts/threads-repurpose/run.sh`）。

改成全自動：`systemctl edit threads-repurpose.service` 加上 `Environment=THREADS_MODE=auto`。

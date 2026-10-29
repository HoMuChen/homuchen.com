# threads-repurpose

排程把已發布的部落格文章拆成多個 idea，一則一則發到 Threads。寫法依 `threads-writing` skill。跑在 hq VM 的 `threads` 帳號（見 homuchen-edge README「使用者帳號」）。

```
systemd timer（每天 17:00–19:00 台北隨機一個時間）
 └ run.sh
    1. flock；處理上次沒 commit/push 的結果；git pull --rebase 到最新 main
    2. 發布「一則」status: approved 的貼文（最久沒發過的文章優先，不同文章交錯發）→ 回寫 status/threads_url/published_at → commit/push
       發文透過 outbox（outbox_publish.py → POST /api/v1/threads/publish，idempotency key = threads-repurpose:{檔名}），這裡不放 Threads token
    3. 待發的（draft + approved）少於 3 則 → claude -p（prompt.md）產生新的一批：
       gsc skill 挑文章 → 讀 threads-writing 寫作指南與最近的 threads/ → 拆成 3–6 個 idea
       → threads/{date}-{slug}-01.md、-02.md…（大多是 single，最多 1 個 thread）
       Claude 的權限只有 Read/Glob/Grep/Write/Skill + gsc.py，不能跑 git、不能發文
    4. thread_file.py check：檔名、frontmatter、則數、≤500 字、主貼文無連結、不用「掰掰」、沒改寫過
       → review 模式 commit 成 draft；auto 模式直接標 approved，之後每次排程發一則
```

- 一篇文章拆成多則、每次排程只發一則，所以一批大約能發一週多。
- Claude 產生 threads/ 以外的檔案或整批驗證失敗 → `git stash` 收起來（`git stash list` 看得到），這次不產生。
- 發布失敗 → 標 `status: failed` 並 commit，不會自動重試（Threads 上可能有部分貼文，要人工看；outbox 那邊用 `ops send:get` 看哪幾則發出了、`ops send:resume` 從失敗那則接著發）。
- outbox 連不上、或 outbox 還在自動重試 → 維持 `approved`，下次排程用同一個 idempotency key 再問一次，不會發兩次。
- 要不要先核准由 outbox 金鑰 `threads-repurpose` 的政策決定。現在是 `threads:homuchen.build.ai` auto（審稿已經在 git 裡把 draft 改成 approved 做過了）；想發之前再到 Telegram 按一次，就把政策改成 approve。
- 審稿：把想發的檔案 `status: draft` 改成 `approved`（可以先改內文）並 push；不要的改成 `rejected`（不要刪檔，刪了那篇文章會被當成沒改寫過）。
- log：`journalctl -u threads-repurpose`；Claude 的完整輸出在 `~/.local/state/threads-repurpose/claude-*.json`。

## 安裝（root）

`/home/threads/.config/threads-repurpose.env`（600，threads 擁有）要有 outbox 的金鑰：

```
OUTBOX_API_KEY=obx_...        # outbox: ops key:create threads-repurpose --rules-json '[{"match":"threads:homuchen.build.ai","mode":"auto"}]'
```

```bash
install -m 644 /home/threads/homuchen.com/scripts/threads-repurpose/systemd/threads-repurpose.{service,timer} /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now threads-repurpose.timer
systemctl list-timers threads-repurpose.timer
```

手動跑一次：`systemctl start threads-repurpose.service`（或以 threads 帳號跑 `scripts/threads-repurpose/run.sh`；`THREADS_SKIP_GENERATE=1` 只發不寫、`THREADS_SKIP_PUBLISH=1` 只寫不發；`THREADS_POST=<slug>` 指定拆某篇）。

改成全自動：`systemctl edit threads-repurpose.service` 加上 `Environment=THREADS_MODE=auto`。

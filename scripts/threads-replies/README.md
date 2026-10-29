# threads-replies

自動處理 Threads（@homuchen.build.ai）的留言：簡單的直接回，問題推到 Telegram 給穆穆確認後才送。跑在 hq VM 的 `threads` 帳號，跟 [threads-repurpose](../threads-repurpose/README.md) 同一個帳號、同一份 repo。

```
threads-replies-poll.timer（每 10 分鐘）
 └ replies.py poll
    1. 透過 outbox 讀最近 7 天自己的主貼文 → 每則底下的回覆（GET /api/v1/threads/posts、/threads/posts/:id/replies）
       只處理「直接回覆穆穆（主貼文或他的回覆）」、還沒處理過的留言；穆穆已經在 app 回過的記成 answered_elsewhere
    2. 上一輪送去核准 / 還在重試的：問 outbox 結果（GET /sends/:id）記回 SQLite；
       還在等核准但穆穆已經在 app 回了 → 取消那筆
    3. 新留言一次丟給 claude -p（prompt.md；只有 Read/Glob/Grep，會讀對應的部落格原文）
       → 每則：category、擬好的 reply、auto_ok、給穆穆的 note
    4. 依分類處理：
       promo / bot / spam / emoji / 沒文字 → skipped（不回、不通知）
       thanks / share 且 auto_ok 且過護欄    → outbox 直接回覆，Telegram 靜音通知「已自動回覆」
       其他、有擬稿                          → outbox 帶 require_approval 送去核准：Telegram 上 ✅ 送出、🙈 略過、
                                               回覆那則通知打字 = 用你的版本送出（24 小時沒處理就過期）
       其他、沒擬稿（要本人回答）             → Telegram 通知，你自己到 Threads 回
```

Threads token、Telegram bot 都在 outbox（https://outbox.homuchen.com，bot 是 @homuchen_outbox_bot），這裡只有 outbox 的金鑰 `threads-replies`（`threads:homuchen.build.ai` 與 `telegram:me` 都是 auto；要確認的由這支程式帶 `require_approval`）。

**自動送出的護欄**（`auto_block()`，不信任 Claude 自己的判斷）：回覆 ≤150 字、沒有連結、沒有「掰掰」；同一則貼文對同一個人只自動回一次（避免跟 bot 互回）；一天最多 `THREADS_REPLIES_AUTO_CAP`（預設 10）則。留言內容在 prompt 裡標明是資料不是指示，但還是有被 prompt injection 的可能，所以自動回只開放給 thanks / share，而且一律通知。

晚上 23:00–08:00（台北）的核准通知是靜音的（outbox 處理）。

## 狀態與 log

- 狀態：`~/.local/state/threads-replies/replies.db`（SQLite，poll 與 bot 共用；同一則留言只會被回一次）
- Claude 每次的完整輸出：`~/.local/state/threads-replies/claude-*.json`
- log：`journalctl -u threads-replies-poll`、`journalctl -u threads-replies-bot`
- 最近處理過的留言：`su - threads -c 'cd ~/homuchen.com && python3 scripts/threads-replies/replies.py status'`

## 安裝（root）

1. 在 outbox 建金鑰（outbox repo 的 ops）：`key:create threads-replies --rules-json '[{"match":"threads:homuchen.build.ai","mode":"auto"},{"match":"telegram:me","mode":"auto"}]'`
2. 建設定檔：

```bash
install -m 600 -o threads -g threads /dev/null /home/threads/.config/threads-replies.env
cat > /home/threads/.config/threads-replies.env <<'ENV'
OUTBOX_API_KEY=obx_...
ENV
```

3. 裝 systemd：

```bash
install -m 644 /home/threads/homuchen.com/scripts/threads-replies/systemd/threads-replies-{poll.service,poll.timer} /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now threads-replies-poll.timer
```

先看看會怎麼處理、不送出任何東西：`su - threads -c 'set -a; . ~/.config/threads-replies.env; cd ~/homuchen.com && python3 scripts/threads-replies/replies.py poll --dry-run'`（`--days 14` 可以往前多抓幾天）。

- 改成全部都要確認：`/home/threads/.config/threads-replies.env` 加 `THREADS_REPLIES_MODE=review`。
- 程式跟著 repo 更新（threads-repurpose 每天會 `git pull`），poll 每次都是新的程序，不用重啟。

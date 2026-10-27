---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/claude-code-stock-agent-monitor-alert/
idea: 盯盤 agent 最重要的設計是「什麼時候不要通知我」：條件全到齊才敲我，接近的只寫 log
topic: 台股
tags: [台股, AI Agent, Telegram]
status: approved
threads_url:
---

盤中我在開會，手機震了一下。

是我那隻台股 bot 傳來的 Telegram：
🔔 2330 台積電【波動率擠壓】
✓ 突破上軌　✓ 量能達標　✓ 5 日動量正向

那個當下我完全沒在看盤。
是它早上自己選好要盯的股票，盤中每 10 分鐘檢查一輪，條件全部到齊才敲我。

做這隻 bot 時，我最在意的反而是：什麼時候「不要」通知我。
接近但還沒到齊的，它只默默寫進 log。

因為通知一吵，你最後一定會把它靜音，那就等於沒做 😂

---

選股、盯盤、Telegram 怎麼串，完整做法在這篇：
👉 https://homuchen.com/posts/claude-code-stock-agent-monitor-alert/

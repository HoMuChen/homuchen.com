---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/claude-code-stock-agent-monitor-alert/
idea: 讓 AI 從「問它才動」變成「時間到自己上工」，差的就是一張 crontab 作息表
topic: AI Agent
tags: [AI Agent, 台股, crontab]
status: draft
threads_url:
---

我那隻台股 agent 沒有什麼高深的排程系統，
就是一張 crontab 作息表，它一天自己醒來四次：

🌅 08:00 掃全市場，選出今天要盯的股票
📈 09:00–13:30 每 10 分鐘盯盤，條件到齊就發 Telegram
🌙 18:00 補當天股價
🌃 22:00 補三大法人、融資融券

補資料 → 選股 → 盯盤，天天自己跑，我不用碰。

讓 AI 從「我問它才動」變成「時間到自己上工」，差的其實就是這張作息表。

你有沒有什麼事，是每天固定要看一輪的？

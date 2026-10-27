---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/claude-code-stock-agent-monitor-alert/
idea: 盯盤程式幾乎不是我寫的：一段把需求講清楚的 prompt，Claude Code 就生出來
topic: claude code
tags: [Claude Code, 台股, AI Agent]
status: draft
threads_url:
---

我那隻會自己盯盤的台股 agent，核心那支程式幾乎不是我寫的。

我只跟 Claude Code 說了這段話：

「幫我寫一個 monitor.py，每 10 分鐘讀 watchlist_conditions.json，抓 FinMind 盤中即時報價，比對每檔的觸發條件，全部滿足就發 Telegram 通知我，接近的只寫 log。」

抓資料、判斷條件、串 Telegram Bot API，它全部生出來。
我要做的是看懂邏輯、測一輪、告訴它哪裡要改。

重點不是你會不會寫 code，是能不能把「要什麼」講到這麼清楚。

---

提醒一下：FinMind 的盤中即時資料要 Sponsor 方案才有，免費版抓不到。完整做法：
👉 https://homuchen.com/posts/claude-code-stock-agent-monitor-alert/

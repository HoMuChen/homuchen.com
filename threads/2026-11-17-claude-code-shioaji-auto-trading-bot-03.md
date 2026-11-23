---
date: 2026-11-17
type: single
source: repurposed
source_post: /posts/claude-code-shioaji-auto-trading-bot/
idea: 下單模式跟緊急煞車都用一個檔案切換：先只講不做的提醒模式，touch 一個檔案就全停
topic: AI Agent
tags: [AI Agent, 自動交易, Claude Code]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DgFGWiTmZoY
published_at: 2026-11-23T17:51:16+08:00
---

我那隻會自己下單的機器人，最重要的開關是兩個空檔案 😂

📄 下單旗標檔：存在才會真的下單
不存在的時候，它只發 Telegram「建議買進 1 口」，要不要下是我決定。

🛑 AUTO_OFF：存在就立刻全停，連提醒都不發

為什麼用檔案？
因為 touch 一個檔案，比改程式、改設定快太多了。在手機上叫 agent 幫我建，幾秒就煞住。

緊急的時候，越簡單的煞車越好用。

給 AI 做事的權限也一樣：先讓它只講不做，跑到你信任它，再打開開關。

---

提醒模式跟下單模式怎麼設計，完整寫在這：
https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/

---
date: 2026-10-15
type: single
source: repurposed
source_post: /posts/claude-code-finmind-stock-tracking/
idea: 前後對照——以前買股要開試算表手動記、常忘記；現在跟 Claude Code 說一句就記進 positions.json，問一句就列出持倉損益
topic: 台股
tags: [台股, Claude Code, 持倉追蹤]
status: draft
threads_url:
---

以前買完股票：
打開試算表 → 找到那一列 → 打代號、價格、日期。
而且常常忘記記 😂

現在買完股票，我在 Claude Code 裡打一句：
「我今天買了 2330，均價 900 元，幫我記下來。」

它就自己寫進本機的 positions.json，我連試算表都不用開。

想看狀況就問：
「現在的持倉狀況怎樣？有沒有哪檔到了出場條件？」
所有持倉的損益、有沒有碰到追蹤停損條件，一次列出來。

這種感覺很不一樣。
不是在操作軟體，是在跟一個助理聊天。

---

小提醒：positions.json 跟放 API token 的 .env.local 記得加進 .gitignore，project 推上 GitHub 也不會把持倉帶上去～

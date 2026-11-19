---
date: 2026-11-19
type: single
source: repurposed
source_post: /posts/claude-code-ai-assistant-one-day/
idea: 40 分鐘會議轉逐字稿，最便宜的是 Whisper 語音轉文字，真正花錢的是 Claude 潤飾
topic: AI Agent
tags: [AI Agent, 語音轉文字, Whisper]
status: draft
threads_url:
---

一場 40 分鐘的會議，從錄音到摘要，我的 AI 助理總共花了不到 0.3 美元。

拆開來看很有趣：
・Whisper 語音轉文字：/bin/zsh（在 Cloudflare 免費額度內）
・Claude 潤飾逐字稿：/bin/zsh.21
・Claude 摘要、抽待辦：/bin/zsh.06

最便宜的反而是語音轉文字，真正花錢的是後面的潤飾😂

Cloudflare Workers AI 的免費額度，換算下來每天大約可以轉 3.5 小時的錄音。開會開到超過這個量，大概也不用轉了吧。

---

完整的系統跟成本拆解在這：
https://homuchen.com/posts/claude-code-ai-assistant-one-day/

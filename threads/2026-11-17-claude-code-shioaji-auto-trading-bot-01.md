---
date: 2026-11-17
type: single
source: repurposed
source_post: /posts/claude-code-shioaji-auto-trading-bot/
idea: 叫 Claude Code 寫會下單的程式，給它的需求幾乎沒在講策略，全部在講「出事的時候怎麼辦」
topic: claude code
tags: [Claude Code, Shioaji, 自動交易]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/Df1tBBak1TQ
published_at: 2026-11-17T18:21:23+08:00
---

我那隻會自己下單的期貨機器人，寫下單版的時候，我給 Claude Code 的需求大概是這樣：

「預設不下單，要有旗標才開；要有 kill switch；每輪先跟券商對帳，對不上就停機；下單前查真實保證金；每輪最多一張單；用限價單，逾時撤單；任何例外都停機並通知我。」

你會發現，這段話幾乎沒在講策略。
全部都在講「萬一出事怎麼辦」。

策略邏輯 AI 一下就寫好了。
用 AI 寫交易程式，真正要花心思的是那些「萬一」😂

---

9 道安全機制每一道在防什麼，整理在這（工程做法分享，不是投資建議）：
https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/

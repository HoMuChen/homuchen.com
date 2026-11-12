---
date: 2026-11-07
type: single
source: repurposed
source_post: /posts/claude-stock-skill-tradermonty-taiwan/
idea: 國外最紅的 Claude 股票 skill（tradermonty，3,663 星、74 個 skill）刻意不報明牌，花很多力氣在下單前擋住自己、交易後檢討
topic: claude code
tags: [Claude Skills, Claude Code, 股票]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/Dfo5Qmmk8tG
published_at: 2026-11-12T18:58:12+08:00
---

最近挖到國外很紅的一套 Claude 股票 skill：tradermonty/claude-trading-skills。

GitHub 3,663 顆星，74 個 skill，MIT 開源。

最讓我意外的不是選股器，而是它花了一堆力氣在「擋住自己」：
・pre-trade-discipline-gate：下單前的紀律檢查
・drawdown-circuit-breaker：虧到一個程度就停
・position-sizer：先算好要買多少
・trader-memory-core：每筆交易都記下來，事後檢討

作者自己講得很白：目標不是把買賣決策外包給 AI，是把流程結構化。

大部分人做 AI 股票工具，都在想怎麼選出會漲的；真正讓人進步的，常常是下單前跟交易後那兩段😂

---

它的資料源全是美股，所以我把其中一個 skill 改成台股版，安裝方式跟實測都寫在這：
https://homuchen.com/posts/claude-stock-skill-tradermonty-taiwan/

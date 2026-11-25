---
date: 2026-11-17
type: single
source: repurposed
source_post: /posts/claude-code-shioaji-auto-trading-bot/
idea: 期貨自動轉倉要「先平再開」，順序一開始寫反了，檢查才抓到
topic: 台股
tags: [期貨, 自動交易, 程式交易]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DgKSc8omb4H
published_at: 2026-11-25T18:13:12+08:00
---

期貨自動轉倉，我一開始把順序寫反了 😱

做期貨有個股票沒有的麻煩：每個月都會到期。
手上還有部位，就要在到期前平掉近月、改開下個月，這叫轉倉。

靠我手動，一定有忘記的一天，所以交給程式。

順序應該是「先平近月，再開次月」。
萬一開次月失敗，最壞的情況是空手；
反過來寫，失敗時就可能同時抱著兩個月的部位。

這個是我後來檢查邏輯才抓到的。

寫一隻會下單的程式不難，難的是讓它不出事。

---

轉倉的完整流程（含先停利再轉）寫在這：
https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/

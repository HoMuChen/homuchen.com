---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/ai-labor-not-tool-500-commits/
idea: agent loop 沒設上限，token 一直燒；max iteration + spend cap 兩個習慣
topic: AI Agent
tags: [AI Agent, LLM, 踩坑]
status: approved
threads_url:
---

AI 變成你的勞力之後，出錯的成本不一樣了。

以前程式寫出 infinite loop，CPU 爆掉、server 重啟，最多服務中斷幾分鐘。

現在 agent loop 沒設上限，它會一直重試 LLM call：
token 一直燒，帳單一直跑。錢是不可逆的。

我自己踩過一次：structured output 的 schema 跟 validation 對不上，agent 不斷 retry，看到帳單才發現 😱

兩個習慣救你：
✅ 每個 agent loop 設 max iteration，超過就停下來回報
✅ LLM 帳戶設每日／每月 spend cap，最後一道防線

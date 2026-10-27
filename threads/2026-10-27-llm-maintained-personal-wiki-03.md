---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/llm-maintained-personal-wiki/
idea: 遠端 inbox 把「捕捉靈感」和「整理」解耦；backlog 指標就是 ls | wc -l
topic: AI Agent
tags: [知識管理, 自動化, LLM]
status: draft
threads_url:
---

靈感都在最不方便的時候出現：捷運上、吃飯時、洗澡時。
但整理需要坐下來、連續的注意力。

所以我在知識庫外面加了一個「遠端 inbox」：
一個收 POST 的小 HTTP 端點，10–20 行程式就夠，東西先丟進 inbox/pending/ 躺著。
手機、網頁、Claude Code session 都能往裡丟。

有空的時候，再叫 LLM 一次整理進 wiki。

我的 backlog 指標就是：
ls inbox/pending/ | wc -l

捕捉不等整理，整理不擋靈感 ✅

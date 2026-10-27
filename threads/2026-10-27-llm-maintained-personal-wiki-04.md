---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/llm-maintained-personal-wiki/
idea: RAG 每次查詢都從零開始；讓 LLM 當維護者，知識才會累積
topic: AI觀察
tags: [LLM, RAG, 知識管理]
status: draft
threads_url:
---

「用 AI 管理知識」，很多人想到的是 RAG：
筆記丟進向量資料庫，再用自然語言查。

但 RAG 有個根本問題：每次查詢都從零開始。
它不會主動去想 A 筆記跟 B 筆記有什麼關係，也不會發現兩篇互相矛盾。

我的做法是讓 LLM 當「維護者」：
每次有新素材，它不只摘要放進去，還會想這條跟哪些舊概念有關、要更新哪些連結、有沒有矛盾要處理。

差別是：知識會累積，越用越強，而不是一堆孤立的筆記。

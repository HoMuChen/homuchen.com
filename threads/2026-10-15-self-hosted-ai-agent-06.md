---
date: 2026-10-15
type: single
source: repurposed
source_post: /posts/self-hosted-ai-agent/
idea: 模型會失憶，所以讓 agent 把一切寫進檔案當記憶，再用索引檔＋漸進式揭露讓它每次只讀需要的部分
topic: AI Agent
tags: [AI Agent, Memory, Context, 漸進式揭露]
status: draft
threads_url:
---

AI 模型本身是會「失憶」的。
對話一結束，它就忘了。

那我的股票 bot 怎麼記得昨天看過什麼？

答案很土：通通寫進檔案 📝

每天的行情、算好的指標、判斷的理由，它都自己寫下來。久了，這些檔案就變成它的資料庫。

但檔案一多，總不能每次全塞進腦袋。
所以我用「索引檔連到細節檔」的方式組織：
它先讀索引，需要哪塊再點進去讀那塊。

這招叫漸進式揭露（progressive disclosure）。

agent 的記憶，不是靠模型記住，
是靠你幫它把檔案擺好。

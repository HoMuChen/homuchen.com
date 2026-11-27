---
date: 2026-11-27
type: single
source: repurposed
source_post: /posts/agent-instruction-claude-md/
idea: 股票 agent 從白目實習生變靠譜同事，沒換模型，只把 instruction 從一句空話改成具體條件
topic: AI Agent
tags: [AI Agent, CLAUDE.md, Agent Instruction]
status: draft
threads_url:
---

我那隻盯台股的 agent，剛開始超白目😂

開會開到一半，傳「某某股票漲了 0.3%」轟炸我；
該提醒的訊號反而沒講清楚；
格式每次都不一樣，中英文還混著來。

我一度以為是模型不夠聰明，後來才發現是我的指令只寫了這樣：

「請幫我分析台股，看到重要的訊號就通知我，講得專業一點。」

「重要」是多重要？agent 只能靠猜。

改成具體條件之後：
・單日漲跌幅超過 5% 才通知
・成交量到 20 日均量 2 倍以上
・不給買賣建議，只偵測與回報
・抓不到資料就說「資料不足」，不要硬掰

同一個模型，馬上變成我信得過的同事。

差別不在模型多強，在那份指令寫得好不好。

---

我把好 vs 壞兩份指令完整對照貼在這篇，連回報格式和範例都有～
👉 完整做法：https://homuchen.com/posts/agent-instruction-claude-md/

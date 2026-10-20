---
date: 2026-10-15
type: thread
source: repurposed
source_post: /posts/self-hosted-ai-agent/
idea: 清單——一隻自架 agent 的四層結構：Context → 能力 → 溝通 → 自動化，用股票 bot 走一遍
topic: AI Agent
tags: [AI Agent, Claude Code, 自動化, crontab]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DetkbM8kys-
published_at: 2026-10-20T18:01:46+08:00
---

一隻會自己開工的 AI agent，拆開來其實只有四層 👇

Context（它知道什麼）
→ 能力（它能做什麼）
→ 溝通（它怎麼跟你來往）
→ 自動化（它什麼時候自己動）

我電腦上那五隻 agent 長得都不一樣，但骨架是同一套。用我的股票 bot 走一遍～

---

1️⃣ Context
一份 instruction 當它的「憲法」：該關心哪些訊號、風險邊界在哪、什麼時候該敲我、什麼時候閉嘴。
再加上檔案當記憶：每天的行情、指標、判斷理由通通寫進檔案。

指令寫得好不好，幾乎決定這隻 agent 靠不靠譜。

2️⃣ 能力
讓它能動手：抓股價、算指標、寫檔案。
我是叫 Claude Code 讀 FinMind 文件、寫支 script 直接抓資料，再包成 skill。

---

3️⃣ 溝通
agent 不該只活在終端機裡。
偵測到訊號，它直接傳 Telegram 到我手機。
兩個方向都要接：你遙控它，它主動通知你。

4️⃣ 自動化
用老牌的 crontab 排程。盤中每 10 分鐘醒來看一次行情，收盤後自己補資料跑分析。
不用我打開、不用我下指令，時間到了它自己上工 ✅

---

四層轉起來長這樣：
到點自動跑 → 用工具完成任務 → 結果寫進檔案 → 有訊號傳到手機。

每一層的完整做法我都寫成一篇了，系列地圖在這：

👉 完整做法：https://homuchen.com/posts/self-hosted-ai-agent/

---
date: 2026-10-15
type: single
source: repurposed
source_post: /posts/claude-code-finmind-stock-tracking/
idea: Google Sheet 用 GOOGLEFINANCE 抓台股常 #N/A、延遲；台股要找專門的資料源（FinMind，資料來自證交所）
topic: Google Sheet
tags: [Google Sheet, GOOGLEFINANCE, 台股, FinMind]
status: approved
threads_url:
---

打開股票試算表，一排股價全是 #N/A 😱

有用 GOOGLEFINANCE 追台股的，應該都遇過。
它對美股還不錯，台股就是二等公民：

・收盤好幾個小時，價格還沒更新
・上櫃股、小型股常常直接找不到 ticker
・Google Finance 一有狀況，整張表跟著掛

我就是某次看股票看到一半、數字全空，才決定換方法。

後來改用 FinMind 抓：資料源自證交所開放資料，收盤後當天更新，我隨機抽幾檔對證交所網站，數字一致。
只追蹤自己的持股，免費方案就夠用。

大家的股票試算表現在還靠 GOOGLEFINANCE 撐著嗎？

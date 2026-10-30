---
date: 2026-10-15
type: single
source: repurposed
source_post: /posts/claude-code-finmind-stock-tracking/
idea: 踩坑更正——FinMind 免費版不能一次抓全市場，要一檔一檔抓；但追蹤自己 20 檔持股一天約 20 次，免費額度綽綽有餘
topic: 台股
tags: [FinMind, 台股, API, 踩坑]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DfHaQanE7P1
published_at: 2026-10-30T18:52:21+08:00
---

我之前寫錯了一件事，來更正一下 🙏

我原本寫：FinMind 免費版一個指令就能抓下全市場 2,500 多支股票的收盤價。

錯。
不帶股票代號、一次抓全市場，要 Backer 以上的付費方案。
我寫的時候自己已經在用付費版，沒注意到這個差別。

免費版的正確用法是一檔一檔抓。
聽起來很弱？其實還好：
免費版每小時 600 次 request，
追蹤自己十幾二十檔持股，每天也才用 20 次左右。

只是要追蹤自己的股票，免費版真的就夠了。
要全市場、還原股價、盤中即時資料，再考慮付費。

---

文章已經更正，免費版和付費版各自怎麼用都寫在裡面～

👉 完整做法：https://homuchen.com/posts/claude-code-finmind-stock-tracking/

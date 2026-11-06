---
date: 2026-11-07
type: single
source: repurposed
source_post: /posts/claude-stock-skill-tradermonty-taiwan/
idea: 台股市場寬度 skill 開源：問一句「台股漲勢健不健康」就跑出 0–100 分（11/6 是 19.1 分 Critical）；FinMind 免費版要改用未還原股價、全上市要跑兩個多小時
topic: 台股
tags: [台股, FinMind, Claude Skills, 開源]
status: approved
threads_url:
---

在 Claude Code 問一句「台股漲勢健不健康？」

它會自己去 FinMind 抓 1,200 多檔上市股票，算出一個 0–100 的市場寬度分數。

11/6 跑出來是 19.1 分，Critical；同一時間美股是 50 分，中性。

這個 skill 我開源了，不過免費版有兩個坑先講：
・還原股價要 Backer 以上，免費版要改用未還原股價，除權息會有假跌破
・免費版每小時 600 次，全上市要跑兩個多小時

我自己用 Sponsor，開 8 條並行，不到 2 分鐘跑完😎

GitHub 連結放留言～

---

GitHub：https://github.com/HoMuChen/tw-market-breadth-skill

設定跟分數怎麼解讀：
https://homuchen.com/posts/claude-stock-skill-tradermonty-taiwan/

這是市場環境的觀察工具，不是買賣訊號～

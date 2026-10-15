---
date: 2026-10-15
type: single
source: repurposed
source_post: /posts/claude-code-finmind-stock-tracking/
idea: 串 API 不用自己讀文件：把文件連結丟給 Claude Code，它自己讀完寫出有增量更新、處理 rate limit 的 script
topic: claude code
tags: [Claude Code, FinMind, API, 台股]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DegsVdGE7pK
published_at: 2026-10-15T18:00:09+08:00
---

FinMind 的 API 文件，我一行都沒讀。

我只跟 Claude Code 講了一句：
「我想用 FinMind API 抓台股日 K，存到本地 CSV，幫我建一個每天可以更新的系統。文件在這裡：（貼連結）」

然後它就自己去讀文件了。

讀完寫出一支 stock_cache.py：
✅ 每支股票一個 CSV
✅ 增量更新，只抓還沒有的日期
✅ 自己處理掉每小時 600 次的 API 限制

我去喝杯咖啡回來，程式就寫好了 ☕

以前自己串 API，光讀文件、處理錯誤重試就要搞半天。
現在比較重要的能力是：講清楚你要什麼，再把文件丟給它。

---

完整的 prompt 跟整套流程（含怎麼用對話記持倉）寫在這篇～

👉 完整做法：https://homuchen.com/posts/claude-code-finmind-stock-tracking/

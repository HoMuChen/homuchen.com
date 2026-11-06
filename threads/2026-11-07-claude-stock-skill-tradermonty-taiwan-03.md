---
date: 2026-11-07
type: single
source: repurposed
source_post: /posts/claude-stock-skill-tradermonty-taiwan/
idea: 把美股寬度 skill 改成台股版，評分程式 0 行修改：skill 把「資料從哪來」跟「怎麼判斷」拆開，換市場只要換一半
topic: claude code
tags: [Claude Skills, Claude Code, Skill 設計]
status: approved
threads_url:
---

把一個美股的 Claude skill 改成台股版，評分程式我一行都沒改。

原因是原作者把它拆成兩半：
1. 資料層：每天算好一份 CSV
2. 評分層：讀這份 CSV，算 6 個分項的分數

所以我只做一件事：用 FinMind 產生一份「格式一模一樣」的台股 CSV，丟給原本的評分程式。

大功告成～台股版就這樣出來了🎉

寫 skill 我現在都照這個拆法：「資料從哪來」跟「怎麼判斷」分開。

換資料源、換市場、換券商，都只要改一半。

---

改寫的過程跟開源的台股版 skill：
https://homuchen.com/posts/claude-stock-skill-tradermonty-taiwan/

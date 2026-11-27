---
date: 2026-11-17
type: single
source: repurposed
source_post: /posts/claude-code-shioaji-auto-trading-bot/
idea: 永豐 Shioaji 開通前要通過模擬環境測試，這一關整個交給 Claude Code 跑
topic: claude code
tags: [Claude Code, Shioaji, 永豐 API]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DgOhyf1Ge-E
published_at: 2026-11-27T09:44:11+08:00
---

永豐 Shioaji API 開通前，要先在模擬環境通過登入和下單測試。

這一關我完全沒自己動手，只跟 Claude Code 說：

「幫我在 Shioaji 模擬環境跑完 API 測試：登入、查帳戶、下一張期貨測試單、確認委託狀態，把每一步的結果印出來給我看。」

它自己寫測試腳本、跑完、整理結果，我只看一眼確認都過了 😎

能這麼順，是因為 Shioaji 是台灣第一個支援 AI coding agent skill 的券商 API，Claude Code 載入之後就知道它怎麼用、有哪些坑。

💡 測試一直不過的話，先檢查時間跟網路：模擬測試有規定的時段，有些時段還要台灣 IP。

---

申請金鑰、簽同意書、模擬測試的完整流程：
https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/

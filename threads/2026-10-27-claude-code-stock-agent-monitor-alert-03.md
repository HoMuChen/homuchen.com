---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/claude-code-stock-agent-monitor-alert/
idea: 選股策略上線前的四條回測鐵則；回測的價值是篩掉沒用的策略，不是那個年化
topic: 台股
tags: [台股, 回測, 量化交易]
status: approved
threads_url:
---

選股策略誰都會喊，問題是準不準。

所以我給自己的台股 agent 定了幾條鐵則，策略要先過這關才能上線：
✅ 全市場約 2,369 檔都回測，不挑漂亮的說嘴
✅ 一定算進手續費 0.1425% 和交易稅 0.3%
✅ 參數從 10 改成 20 結果就天差地別的，直接丟掉
✅ 分成 6 群驗證，避免「剛好在某一檔賺很多」

活下來 14 個。挑 3 個組成投資組合回測：年化約 +34%、最大回撤 9.1%、Sharpe 2.58。

但這是回測，不是對帳單，也不保證未來 🙏
回測對我最大的價值不是那個年化，是逼我篩掉「聽起來很厲害、其實沒用」的策略。

---

四條鐵則的細節、這三個策略各在做什麼，寫在這篇：
👉 https://homuchen.com/posts/claude-code-stock-agent-monitor-alert/

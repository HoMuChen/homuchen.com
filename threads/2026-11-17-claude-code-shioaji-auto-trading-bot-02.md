---
date: 2026-11-17
type: single
source: repurposed
source_post: /posts/claude-code-shioaji-auto-trading-bot/
idea: 下單機器人最重要的一道保險是每輪先跟券商對帳，對不上就停機，寧可什麼都不做
topic: 台股
tags: [自動交易, Shioaji, 程式交易]
status: approved
threads_url:
---

會下單的程式，最可怕的不是策略賠錢，是程式出 bug。

我的期貨機器人每次醒來，第一件事不是看行情，是先問券商：「我現在真的有幾口？」
再跟自己的帳本比。

只要對不上，就發 Telegram 給我，然後停機。

什麼時候會對不上？
・我自己手動下過單
・某張單只成交一部分
・上一輪程式在奇怪的地方掛掉

這時候繼續下單，就是在錯的狀態上疊更多錯。

交易程式的 fail fast 要更極端：
有疑慮的時候，什麼都不做永遠最安全。

---

其他 8 道保險跟對帳的程式碼放這（工程做法，不是投資建議）：
https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/

---
date: 2026-11-03
type: single
source: repurposed
source_post: /posts/ai-stock-picking-taiwan-backtest/
idea: 機器學習選股的預測準確度比任何單一特徵都高，年化超額卻只有簡單規則的三分之一多一點；目標是平均排名，模型學會避開爛股而不是挑大贏家
topic: AI觀察
tags: [AI選股, 機器學習, 台股, 回測]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DfuBOyVGT2y
published_at: 2026-11-14T18:43:59+08:00
---

我用機器學習選台股，預測準確度比任何單一指標都高。

報酬卻輸給一條簡單規則。

2015–2023 樣本外，每年用過去的資料重新訓練，挑同樣數量的股票：
・股價強勢＋營收驚喜（簡單規則）：年化超額 +39.1%
・梯度提升樹：+14.6%
・線性迴歸：+7.9%

問題出在目標。我給模型的目標是「預測每檔股票在全市場的排名」，它為了把平均做好，學會的是避開爛股：低波動、不是彩券型的股票權重最大。

可是只挑前面一小籃的投組，賺的就是那幾個大贏家，模型根本沒對準它。

目標設錯，模型再強都沒用。

---

公平起見補一句：2015–2019 剛好是簡單規則被挑出來的期間，對機器學習比較不利。但差距這麼大，我覺得結論還是成立。

完整數字和回撤在這篇：
https://homuchen.com/posts/ai-stock-picking-taiwan-backtest/

以上是歷史回測，不是投資建議～

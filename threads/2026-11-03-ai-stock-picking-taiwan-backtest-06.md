---
date: 2026-11-03
type: single
source: repurposed
source_post: /posts/ai-stock-picking-taiwan-backtest/
idea: AI 回測出漂亮數字時，叫它自己找漏洞、用打亂股票代號的安慰劑估計假訊號比例；實測篩選標準放行了 19.4% 的假特徵
topic: claude code
tags: [Claude Code, 回測, AI選股]
status: approved
threads_url:
---

用 AI 回測出很漂亮的數字時，我會再丟一句話給它：

「這個結果好得不太正常。幫我檢查有沒有前視、倖存者偏差、成本沒算，再跑一次截斷資料的前視檢查。」

還有一句更狠的：
「把股票代號隨機打亂 20 次當安慰劑，看這個篩選標準會放行多少假訊號。」

我們實際量過：打亂之後，理論上什麼特徵都不該有效，結果篩選標準還是放行了 19.4% 的假特徵 😱

測得越多，就越容易「剛好」找到一個好看的結果。AI 跑回測很快，快到也很容易幫你找到一個假的好結果。

---

這兩句都在我實際下給 AI 的 6 句選股研究指令裡，可以照抄：
https://homuchen.com/posts/ai-stock-picking-taiwan-backtest/

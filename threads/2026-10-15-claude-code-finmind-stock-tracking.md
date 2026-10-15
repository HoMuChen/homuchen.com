---
date: 2026-10-15
type: thread
source: repurposed
source_post: /posts/claude-code-finmind-stock-tracking/
tags: [台股, Claude Code, FinMind, Google Sheet]
status: draft
threads_url:
---

用 Google Sheet 追台股的人，應該都看過這個畫面：

打開試算表，一排股價全是 #N/A 😩

GOOGLEFINANCE 對美股還行，台股就是二等公民：資料延遲、上櫃股和小型股常抓不到、偶爾整張清單一起壞。

我某次看股票看到一半，發現數字全空了，就決定不忍了。

後來換了一套做法：資料改抓 FinMind，程式交給 Claude Code 寫，記持倉只要跟它講一句話 👇

---

先說為什麼選 FinMind。

它是台股金融資料 API，日 K、三大法人買賣超、融資融券都有，資料源自證交所，我自己抽幾檔對過證交所網站，數字一致。

免費方案每小時 600 次 request，要指定股票代號一檔一檔抓。追自己十幾二十檔持股，一天也才用 20 次左右，很夠用。

⚠️ 先講清楚：不帶代號、一次抓全市場，要 Backer 以上的付費方案。我原本文章寫錯了，後來已經更正 🙏

---

整個串接過程，我沒讀過 FinMind 的 API 文件。

我只是開一個 Claude Code project 跟它說：「我想用 FinMind 抓台股日 K，存成本地 CSV，做一個每天可以更新的系統，文件在這裡。」

它自己去讀文件，寫出一支 stock_cache.py：

📁 每支股票一個 CSV
🔁 增量更新，只補還沒有的日期
⏱ 順便處理好每小時 600 次的限制

我一行 Python 都沒寫，喝杯咖啡回來就好了 ☕

---

但真正讓我覺得「AI 原來可以這樣用」的，是記持倉。

以前買股票要自己開試算表，手動記代號、價格、日期，常常忘記記。

現在直接說：
「我今天買了 2330，均價 900 元，幫我記下來。」
它就寫進 positions.json。

想看狀況就問：
「現在持倉怎樣？有沒有哪檔到了出場條件？」
損益、有沒有碰到追蹤停損，一次列給我看。

不像在操作軟體，比較像在跟助理聊天～

---

想自己做一套的話，有三個小地方很關鍵：

✅ 腳本寫完，叫它把用法寫進 CLAUDE.md，下次開新對話就不用重新解釋
✅ 持倉要用什麼格式記，也讓它自己設計、寫進 CLAUDE.md，之後每次才會記得一致
✅ positions.json 跟 .env.local 加進 .gitignore，就算推上 GitHub，持倉和 token 也不會跟著上去

設定好之後，每天收盤後跑一次更新，幾秒鐘就完成。

---

用 GOOGLEFINANCE 抓台股，就像用膠帶黏東西，有時黏得住、有時不行。

這次給我最大的感觸是：Claude Code 的價值不只是幫你寫程式，而是把一個「想法」變成「真的能跑的系統」。我不用會 Python、不用設計資料結構，只要知道自己想要什麼。

資料來源比較表、4 個步驟、可以直接貼給 Claude Code 的 prompt，都整理在文章裡了，連結放留言 👇

---

👉 完整做法：https://homuchen.com/posts/claude-code-finmind-stock-tracking/

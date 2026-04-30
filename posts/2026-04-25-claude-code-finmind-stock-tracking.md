---
title: "用 Claude Code 建台股追蹤系統 — AI 幫你接 API、管持倉，你只要說你買了什麼"
date: 2026-04-25
author: HoMuChen
category: AI
tags: [AI, Claude Code, 股票, FinMind, Google Sheet]
image: https://storage.googleapis.com/homuchen.com/images/claude-code-finmind-stock-tracking-0.jpg
description: "不用寫程式，用 Claude Code 接 FinMind API 自動抓台股資料、每天收盤後更新、還能用對話追蹤你的持倉。工程師的台股追蹤系統，原來可以這麼建。"
---

**快速總結（TL;DR）**：本文示範如何用 Claude Code 串接 FinMind 的免費台股 API，建立每天自動更新收盤價、用對話記錄持倉的個人系統。整個過程不需要自己寫一行 Python，從零到可用大約 30 分鐘。適合**有在用 Google Sheet 追蹤台股、但受夠 GOOGLEFINANCE 不穩定**的個人投資者。

我之前寫過一篇 [**Google Sheet 股票損益表**](/posts/google-sheet-stock-income-statement/)，教大家用 `GOOGLEFINANCE` 函數自動帶入股價。那篇到現在都還有不少人在看，顯然大家都有在用 Google Sheet 管自己的投資組合。

但你有沒有遇過這個狀況：打開試算表，某幾格股價顯示 `#N/A` 或是根本不更新？

台股用 `GOOGLEFINANCE` 就是會這樣。資料來源不穩定、有時候抓不到、有時候延遲，偶爾整個台股清單都壞掉。我自己也是在某次看股票看到一半、發現數字全都是空的，才決定——好，我要換個方法。

然後我叫 Claude Code 去幫我重新做一套。

結果比我預期的好很多，今天來分享整個過程：

* 為什麼改用 FinMind API
* Claude Code 怎麼「自己」去串接 API
* 每天收盤後一行指令自動更新
* 最好玩的部分：用對話的方式追蹤持倉

> **關於作者**：我是工程師阿穆，寫程式十多年，這幾年在做電商系統跟 AI Agent 開發。自己用 Google Sheet 追蹤台股多年，這篇是我從 GOOGLEFINANCE 換到 FinMind 後的第一手實作紀錄。

---

## 為什麼 GOOGLEFINANCE 抓不到台股？

`GOOGLEFINANCE` 對美股支援算不錯，但台股就是二等公民。常見的問題：

- **資料延遲**：有時候收盤好幾個小時了，價格還在更新前
- **`#N/A` 錯誤**：找不到台灣的 ticker，尤其是上櫃股和小型股
- **依賴 Google**：如果 Google Finance 服務有問題，你的試算表就全掛

既然台股資料要找專門的來源，那就找 **FinMind**。

## 台股資料來源比較：FinMind 跟其他選項差在哪？

在決定用 FinMind 之前，我也比較過幾個常見的台股資料來源。整理成一張表給大家參考：

| 來源 | 免費額度 | 資料即時性 | 易用性 | 適合誰 |
|------|---------|-----------|--------|--------|
| GOOGLEFINANCE | 無限 | 不穩、常 #N/A | ★★★★★ | 主要看美股的人 |
| FinMind | 600 req/hr | 收盤後 T+1 | ★★★★ | 個人投資者、寫腳本自動化 |
| 證交所開放資料 | 無限 | T+1 | ★★ | 願意自己 parse CSV 的工程師 |
| 永豐金 Shioaji | 開戶免費 | 即時 | ★★★ | 要做交易（不只是追蹤）的人 |
| 富果 / 玉山 API | 條件式開放 | 即時 | ★★ | 高頻交易者、做交易策略的人 |

我會選 FinMind 的理由很簡單：**只是要追蹤股價跟記持倉，不交易，免費就夠用**，而且資料源來自證交所，正確性有保障。如果你的需求是寫策略下單，那就要看永豐 Shioaji 或富果。

## FinMind 是什麼？

[FinMind](https://finmindtrade.com/analysis/#/data/api) 是一個台股金融資料 API，有免費方案（每小時 600 次 request），資料包括：

- 台股日 K 股價（開高低收、成交量）
- 三大法人買賣超
- 融資融券
- 基本上你想得到的台股資料它都有

免費方案就夠個人使用了。申請帳號後拿到 API token，就可以開始抓資料。

## Claude Code 怎麼幫我串接 FinMind API？

這是整件事裡最有趣的部分。

我沒有自己去讀 FinMind 的 API 文件。我只是開一個 Claude Code 的 project，跟它說：

> 「我想用 FinMind API 抓台股的日 K 資料，存到本地 CSV 檔案，幫我建一個可以每天更新的系統。FinMind 的文件在這裡：https://finmindtrade.com/analysis/#/data/api」

然後 Claude Code 就去讀文件了。

它讀完文件之後，自己寫了一個 `stock_cache.py`，設計了一套 CSV 快取機制：每支股票一個 CSV 檔，支援增量更新（只抓還沒有的日期），還處理好了 API 限制（600 req/hr）的問題。整個過程我沒有寫任何一行 Python。

寫出來的程式是這樣用的：

```bash
# 更新今天全市場股價（只需要 1 個 API call）
python3 stock_cache.py today

# 補抓某段日期
python3 stock_cache.py range 2026-04-01 2026-04-20

# 更新單檔
python3 stock_cache.py one 2330
```

一個指令，全部 2,500 多支股票的今日收盤價全部更新完畢。

如果你有用過 Python 自己爬過 API，你就知道要做到這個功能、還要處理增量更新和錯誤重試，大概要花多久。我跟 Claude Code 說我要什麼，然後喝了一杯咖啡回來，程式就寫好了。

## 台股收盤後怎麼自動更新本地資料？

台股收盤時間是下午 1:30，但收盤資料大概要到 2:30 之後才完整。

我的習慣是，盤後大概 3 點左右，開一個 terminal，跑：

```bash
python3 stock_cache.py today
```

幾秒鐘，本地的股價資料就更新了。

這些 CSV 資料不是直接存在 Google Sheet 裡，是存在本機。但如果你需要，也可以很輕鬆地匯入 Google Sheet——或是直接讓 Claude Code 幫你把資料格式化成你想看的樣子。

## 怎麼用對話的方式追蹤股票持倉？

這個才是讓我覺得「原來 AI 工具可以這樣用」的地方。

之前我買股票，都要自己打開試算表，手動記錄買入的股票代號、價格、日期。很麻煩，而且常常忘記記。

現在我的做法是：在 Claude Code 的 project 裡，直接跟它說：

> 「我今天買了 2330，均價 900 元，幫我記下來。」

它就直接幫我記到 `positions.json` 裡，完全不需要我打開任何試算表或手動輸入。

或是問它：

> 「現在的持倉狀況怎樣？有沒有哪檔到了出場條件？」

它就把目前所有持倉的狀態、損益、是否達到追蹤停損條件，一次列給我看。

這種感覺很不一樣。不是在操作軟體，是在跟一個助理聊天。

## 怎麼自己建一套台股追蹤系統？4 步驟

如果你想建一個類似的系統，大致步驟是：

**Step 1：申請 FinMind 帳號**

到 [FinMind 官網](https://finmindtrade.com/) 申請，拿到 API token。免費方案就夠了。

**Step 2：告訴 Claude Code 你要什麼，讓它去讀文件**

這是整個流程最關鍵的一步，也是我覺得最神奇的地方——你不需要自己去讀 API 文件。

開一個 Claude Code 的新 project，跟它說你想做什麼，然後把 FinMind 的文件連結丟給它：

> 「我想用 FinMind API 抓台股日K資料，每支股票存一個 CSV 到本地，支援每天增量更新（只補沒有的日期）。API token 存在 .env.local。FinMind 文件在這裡：https://finmindtrade.com/analysis/#/data/api」

Claude Code 會自己去讀文件、理解 API 結構，然後把腳本寫好。

重要的是，**寫完腳本之後，請它同時更新 `CLAUDE.md`，把腳本的使用方式記錄下來**。這樣下次開一個新的對話，Claude Code 讀到 CLAUDE.md 就知道這個 project 是在做什麼、每個腳本怎麼用——不需要每次重新解釋。

**Step 3：如果你也想追蹤持倉，讓它定義好格式**

持倉資料要用什麼格式存、存在哪個檔案，這些細節讓 Claude Code 自己決定並記錄在 CLAUDE.md。

你可以跟它說：

> 「我想用對話的方式追蹤我的股票持倉。設計一個持倉記錄的格式，把說明寫進 CLAUDE.md，這樣我說『我買了 XXX 均價 OOO』的時候，你就知道怎麼記錄。」

它會設計好資料格式（通常是一個 JSON 檔），並在 CLAUDE.md 裡把規則寫清楚。之後每次說「我買了什麼」，它就照這個格式幫你記，不會每次都不一樣。

**Step 4：每天收盤後跑一次**

設定好之後，每天台股收盤後，開終端機跑一次更新指令，幾秒鐘就完成。具體指令名稱看 Claude Code 幫你寫的腳本叫什麼，查 CLAUDE.md 就有。

---

## 常見問題 FAQ

### FinMind 免費方案能用多久？

**永久免費**，每小時上限 600 次 API request。日常更新台股大概只用 1-2 次 call 就夠（用 `today` 模式一次抓全市場），所以 600 次的限額對個人使用完全綽綽有餘。

### FinMind 的資料準確性夠嗎？跟證交所對得上嗎？

FinMind 的台股資料源自[**台灣證券交易所**](https://www.twse.com.tw/) 的開放資料，**T+1 更新**（也就是收盤後當天會更新好）。我自己隨機抽了幾檔對證交所網站的數字，結果一致。如果你做的是學術研究或重要決策，建議自己也抽樣驗證一次比較安心。

### 沒寫過 Python 也能做嗎？

可以。重點是讓 Claude Code 讀 FinMind 文件、寫好腳本，使用者只需要會在終端機跑 `python3 stock_cache.py today` 這種指令。整個建置過程，使用者不需要看 Python 程式碼一行——只要會描述「我想做什麼」。

### 持倉資料存哪？會不會被別人看到？

存在**本機的 `positions.json`** 檔案，不上雲端、不上 GitHub。記得在 `.gitignore` 裡加上 `positions.json` 跟 `.env.local`，這樣即使你把這個 project 推到 GitHub，敏感資料也不會跟著上去。

### 跟 GOOGLEFINANCE 最大的差別？

| 比較項 | GOOGLEFINANCE | FinMind + Claude Code |
|--------|---------------|----------------------|
| 台股支援 | 不穩、常 #N/A | 完整 |
| 資料來源 | Google Finance（黑盒） | 證交所開放資料 |
| 控制權 | 沒有 | 完全在自己手上 |
| 客製化 | 很難 | 想加什麼功能就跟 Claude Code 講 |

### Claude Code、Claude Cowork、Claude.ai 是同一個東西嗎？

不是。**Claude.ai** 是聊天介面（網頁版）；**Claude Code** 是給工程師在終端機用的 CLI 工具；**Claude Cowork** 是 Claude Code 包了一層 GUI、給非工程師也能用的桌面應用。本文用的是 Claude Code，因為這個案例需要它在電腦上實際執行 Python 腳本。

### 這套系統可以接 LINE 通知嗎？

可以，再叫 Claude Code 加一個 webhook 腳本就好。例如「股價跌破成本 10% 通知我」「持倉有變動寄 email」這類條件式通知，都是再開一個對話補一支腳本的事，不需要再付 SaaS 訂閱費。

---

## 該不該從 GOOGLEFINANCE 換到 FinMind？

這整件事給我最大的感觸是：**Claude Code 的價值不在於它幫你寫程式碼，而在於它幫你把一個「想法」變成一個「真的可以跑的系統」**。

我不需要會 Python、不需要讀 API 文件、不需要設計資料庫結構——我只要知道我想要什麼。

用 GOOGLEFINANCE 抓台股就像用膠帶黏東西，有時候黏得住、有時候不行。現在改用 FinMind 搭配 Claude Code，感覺是真的把一套工具建好了，而不是湊合著用。

如果你也有在追蹤台股，這套流程真的值得試試看。設定好之後，每天花不到一分鐘，資料就自動準備好了。

延伸閱讀：
* [**Google Sheet 股票損益計算：自動更新最新股價，算出投資損益**](/posts/google-sheet-stock-income-statement/)
* [**Claude Code 接 Google Search Console — 用 AI 幫你做 SEO 分析**](/posts/claude-code-search-console-seo-analysis/)
* [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/)

希望這篇對大家有一丁點兒的幫助～掰掰～👋

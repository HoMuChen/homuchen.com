---
title: "FinMind 是什麼？台股 API 免費額度、方案價格與 Python 教學（2026 實測）"
date: 2026-10-14
author: HoMuChen
category: AI
tags: [FinMind, 台股, API, Python, Claude Code]
image: https://storage.googleapis.com/homuchen.com/images/finmind-taiwan-stock-api-guide-0.jpg
description: "FinMind 是台股開源金融資料 API。免費版每小時 600 次夠不夠？Backer、Sponsor 差在哪？我實測免費版做不到的 4 件事，附 Python 抓股價教學與方案選擇建議。"
---

**快速總結（TL;DR）**：**FinMind** 是一個以台股為主的開源金融資料平台，用 API 或 Python 套件就能抓股價、三大法人、融資融券、財報、期貨等資料。**免費版**未登入每小時 300 次、註冊拿 token 後 600 次，可用 45 種資料集，追蹤幾十檔股票綽綽有餘；但「一次抓全市場」、還原股價、盤中即時、分點這些要付費方案（Backer NT$699/月起）。我自己付費用 Sponsor 年繳，這篇是第一手實測整理（價格以 2026 年 10 月官網為準）。

我第一次用 FinMind，是因為 Google Sheet 的 `GOOGLEFINANCE` 抓台股一直出現 `#N/A`😫

那時候我寫了一篇 [**用 Claude Code 建台股追蹤系統**](/posts/claude-code-finmind-stock-tracking/)，用免費方案抓收盤價、記持倉，覺得「免費就夠了啦」。

結果用著用著，從追蹤幾檔股票，變成[**每天掃全市場選股、盤中盯盤的 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/)，最後還接上了[**自動下單**](/posts/claude-code-shioaji-auto-trading-bot/)。免費版開始不夠用，我就升級成付費的 Sponsor。

如果你 Google 過 FinMind，會發現大家最想知道的就是：「FinMind 是什麼？」「要錢嗎？」「免費版的流量限制是多少？」

所以這篇一次整理：

* FinMind 是什麼？有哪些資料？
* 要錢嗎？免費額度多少？各方案價格比較
* 免費版做不到的 4 件事（我實測的）
* 申請 token + Python 抓股價教學
* 不想寫程式？讓 AI 幫你接 FinMind
* 該選哪個方案？

> **關於作者**：我是工程師阿穆，寫程式十多年，這幾年在做電商系統跟 AI Agent 開發。從 2026 年初開始用 FinMind 接自己的台股工具，現在付費用 Sponsor 年繳，每天讓 agent 拿它的資料選股、盯盤、做回測研究。

> **先說清楚**：這篇不是業配，FinMind 的錢是我自己付的😂 所有價格、限制都是 2026 年 10 月看官網、自己打 API 實測的結果，方案可能會調整，購買前請以[**官網方案頁**](https://finmind.github.io/Pricing/)為準。

## FinMind 是什麼？

**FinMind 是一個以台股為主的開源金融資料平台**，把散落在證交所、櫃買中心、期交所等地方的公開資料整理好，用統一的 API 提供給你。

顧名思義就是 Finance + Mind，你不用再自己寫爬蟲去證交所網站一頁一頁抓，打一個 API 就拿到整理好的 JSON。

它的資料大致分成這幾類：

| 類別 | 例子 |
|------|------|
| 技術面 | 日 K 股價、本益比/股價淨值比、加權指數 |
| 籌碼面 | 三大法人買賣超、融資融券、外資持股 |
| 基本面 | 月營收、綜合損益表、資產負債表、股利政策 |
| 衍生性商品 | 期貨、選擇權每日成交資訊 |
| 國際市場 | 美股股價、美債殖利率、黃金、原油、匯率 |

資料每天更新，可以用三種方式拿：

1. **直接打 API**（任何語言都可以，回傳 JSON）
2. **官方 Python 套件** `FinMind`（`pip install FinMind`）
3. **AI 整合**：MCP Server、Agent Skill、`llms.txt`（後面會講）

整個專案是開源的，原始碼在 [**GitHub**](https://github.com/FinMind/FinMind)，文件在 [**finmind.github.io**](https://finmind.github.io/)。

## FinMind 要錢嗎？免費額度有多少？

**有免費版，而且不用綁卡、沒有期限。** 差別在每小時能打幾次 API、能用哪些資料集。

### 免費版：每小時 300 次，註冊後 600 次

- **不登入**（不帶 token）：每小時 **300 次**
- **註冊並驗證 email**、帶 token：每小時 **600 次**
- 可用資料集：**45 種**
- 只能**非商業使用**，引用資料要標示來源「FinMind」

### 各方案價格比較（2026 年 10 月）

| 方案 | 月繳 | 年繳 | API 上限（每小時） | 資料集 | 商業使用 |
|------|------|------|------|------|------|
| **Free** | 免費 | 免費 | 300 次（註冊 600 次） | 45 種 | ❌ |
| **Backer** | NT$699 | NT$5,499 | 1,600 次 | 81 種 | ❌ |
| **Sponsor** | NT$999 | NT$8,888 | 6,000 次 | 97 種 | ❌ |
| **Sponsor Pro** | NT$3,330 | NT$29,620 | 20,000 次 | 97 種＋整日全商品下載 | ✅ |

資料來源：[**FinMind 方案與價格**](https://finmind.github.io/Pricing/)

幾個官網寫在角落、但很重要的規則：

- **單次付款、不會自動續扣**，到期自動降回 Free。不用擔心忘記取消😎
- **年繳比較划算**：Sponsor 月繳一年是 999 × 12 = 11,988，年繳 8,888，省了 3,100（約 26%）；Backer 月繳一年 8,388、年繳 5,499，省 2,889（約 34%）
- 已經買了 Backer 或 Sponsor，想升級可以**按剩餘天數補差額**（最低 NT$100）
- 可以開統編發票，學校另外有校園方案
- **Free、Backer、Sponsor 都只能非商業使用**。如果要用在公司內部系統、SaaS、對外販售的產品，要 Sponsor Pro。而且不管哪個方案，都**不能轉散布原始資料**，也不能把即時資料直接放在對外的網站或 App 上

## 免費版做不到的 4 件事（我實測的）

官網的方案表列了一長串資料集，看完還是很難想像「免費到底卡在哪」。所以我開一個沒登入的請求，直接打 API 試給大家看：

| 想做的事 | 用到的資料 | 免費版結果 | 最低方案 |
|------|------|------|------|
| 抓單檔股價、三大法人、融資融券、月營收、本益比 | `TaiwanStockPrice` 等 | ✅ 正常 | Free |
| **不指定股票、一次抓某天全市場** | `TaiwanStockPrice`（不帶 `data_id`） | ❌ 400 | Backer |
| **還原股價**（除權息調整後） | `TaiwanStockPriceAdj` | ❌ 400 | Backer |
| **股權分散表**（大戶/散戶持股分級） | `TaiwanStockHoldingSharesPer` | ❌ 400 | Backer |
| **分點買賣**、**盤中即時報價** | `TaiwanStockTradingDailyReport`、`taiwan_stock_tick_snapshot` | ❌ 400 | Sponsor |

被擋的時候，API 會回這個：

```json
{
  "msg": "Your level is free. Please update your user level. Detail information:https://finmindtrade.com/analysis/#/Sponsor/sponsor",
  "status": 400
}
```

其中最多人會撞到的是第一個：**一次抓全市場**。

上市櫃的股票加 ETF，四位數代號的就有 2,300 多檔。免費版只能一檔一檔抓，等於 2,300 多次 request；註冊後每小時 600 次，光是更新一天的收盤價就要分 4 個小時跑完😱 付費版不帶股票代號，一個 request 就拿到整個市場。

> 🙏 **更正**：我在 4 月那篇[**用 Claude Code 建台股追蹤系統**](/posts/claude-code-finmind-stock-tracking/)寫過「免費版用 `today` 模式一次抓全市場」，這是錯的——我那時已經在用付費方案，沒注意到免費版做不到。那篇已經一起改正了，抱歉！

另外還有一個限制：**超過每小時上限**，API 會回 HTTP **402**，訊息是 `Requests reach the upper limit.`，等下一個小時重置就好。

## 免費版夠不夠用？我為什麼升級到 Sponsor

**如果你只是追蹤自己手上的十幾二十檔股票，免費版完全夠用。**

每天收盤後每檔抓一次，20 檔就是 20 次，離 600 次的上限還很遠。看三大法人、融資融券、月營收、財報，免費版也都有。

我會升級，是因為需求長大了：

1. **每天掃全市場選股**：我的[**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/) 每天盤前要掃全部股票找訊號，免費版一檔一檔抓太慢
2. **盤中盯盤**：要拿盤中即時報價比對進場條件，這是 Sponsor 才有的
3. **研究籌碼**：想看分點進出，也是 Sponsor 才有

所以選方案可以這樣想：

| 你的需求 | 建議方案 |
|------|------|
| 追蹤自己的持股、看日 K 和三大法人 | **Free**（先註冊拿 token） |
| 要掃全市場選股、要還原股價做回測 | **Backer** |
| 要盤中即時資料、分點、分 K | **Sponsor** |
| 要用在公司或對外的產品 | **Sponsor Pro** |

我的建議是：**先用免費版做到卡住，再升級**。你很快就會知道自己卡在哪一個資料集，到時候再買對應的方案，不會花冤枉錢。

## 怎麼申請 FinMind token？

1. 到 [**FinMind 官網**](https://finmindtrade.com/)註冊帳號
2. 收信、點驗證連結（**沒驗證 email 就只有 300 次**）
3. 登入後在會員頁複製你的 **API token**

想知道自己目前用了幾次、上限多少，可以打這個：

```bash
curl https://api.web.finmindtrade.com/v2/user_info \
  -H "Authorization: Bearer 你的token"
```

回傳裡的 `user_count` 是已使用次數、`api_request_limit` 是你的每小時上限。

> ⚠️ token 跟密碼一樣，不要寫死在程式碼裡、不要推到 GitHub。放在 `.env` 檔，並把 `.env` 加進 `.gitignore`。

## FinMind API 教學：用 Python 抓台股股價

以下兩種寫法我都在 2026 年 10 月實際跑過。

### 方法一：直接打 API（requests）

```python
import os
import requests

url = "https://api.finmindtrade.com/api/v4/data"
params = {
    "dataset": "TaiwanStockPrice",   # 資料集：台股日 K
    "data_id": "2330",               # 股票代號
    "start_date": "2026-10-01",
    "end_date": "2026-10-08",
}
headers = {"Authorization": f"Bearer {os.environ['FINMIND_TOKEN']}"}

data = requests.get(url, params=params, headers=headers).json()["data"]
for row in data[-3:]:
    print(row["date"], row["open"], row["max"], row["min"], row["close"])
```

跑出來長這樣：

```
2026-10-06 2575.0 2590.0 2565.0 2585.0
2026-10-07 2565.0 2585.0 2560.0 2585.0
2026-10-08 2550.0 2575.0 2550.0 2550.0
```

幾個參數重點：

- `dataset`：要哪一種資料，名字可以在[**官方文件**](https://finmind.github.io/)查
- `data_id`：股票代號（期貨就是商品代號，例如台指期 `TX`）
- `start_date` / `end_date`：日期區間，至少要給一個
- token 放在 header 的 `Authorization: Bearer ...`（舊文件是放在 `token` 參數，也還能用）

### 方法二：官方 Python 套件（DataLoader）

```bash
pip install FinMind
```

```python
from FinMind.data import DataLoader

api = DataLoader()
api.login_by_token(api_token="你的token")  # 不登入也能用，只是上限 300 次

df = api.taiwan_stock_daily(
    stock_id="2330",
    start_date="2026-10-01",
    end_date="2026-10-08",
)
print(df[["date", "open", "max", "min", "close"]].tail(3))
```

套件直接回傳 pandas DataFrame，做分析比較方便。它把常用資料集都包成方法了，例如 `taiwan_stock_institutional_investors`（三大法人）、`taiwan_stock_month_revenue`（月營收）、`taiwan_stock_dividend`（股利），我用的 2.0.11 版有 63 個 `taiwan_stock_*` 方法。

### 常用資料集速查

| 資料集 | 內容 | 方案 |
|------|------|------|
| `TaiwanStockPrice` | 日 K（開高低收、成交量） | Free |
| `TaiwanStockInstitutionalInvestorsBuySell` | 三大法人買賣超 | Free |
| `TaiwanStockMarginPurchaseShortSale` | 融資融券 | Free |
| `TaiwanStockMonthRevenue` | 月營收 | Free |
| `TaiwanStockPER` | 本益比、股價淨值比、殖利率 | Free |
| `TaiwanStockDividend` | 股利政策 | Free |
| `TaiwanStockShareholding` | 外資持股 | Free |
| `TaiwanFuturesDaily` | 期貨日成交 | Free |
| `TaiwanStockPriceAdj` | 還原股價 | Backer |
| `TaiwanStockHoldingSharesPer` | 股權分散表 | Backer |
| `TaiwanStockTradingDailyReport` | 分點買賣 | Sponsor |

上表的 Free 是我不帶 token 實際打過、有拿到資料的；付費的是實際被擋、再對照官網方案表的。

## 不想寫程式？讓 AI 幫你接 FinMind

如果你看到上面的程式碼就頭痛，好消息是：**現在可以讓 AI 幫你寫，甚至直接幫你查**。

FinMind 官方提供了三種 [**AI 整合**](https://finmind.github.io/tutor/ai/Llms/)：

| 方式 | 適合 | 做什麼 |
|------|------|------|
| `llms.txt` | ChatGPT、Claude 網頁版 | 把連結貼給 AI，它讀完就知道有哪些資料集、怎麼寫程式，免安裝 |
| **MCP Server** | 支援 MCP 的工具 | AI 直接幫你抓資料（`uvx finmind-mcp`，用環境變數 `FINMIND_TOKEN` 帶 token） |
| **Agent Skill** | Claude Code 等 CLI 工具 | 用 `/finmind` 指令讓 agent 抓資料 |

我自己用的是另一條路：**叫 Claude Code 讀 FinMind 文件，自己寫一支 Python 腳本，再把「抓哪些資料、怎麼算」包成 skill**。

這樣腳本是我自己的，要快取、要增量更新、要接其他資料源都很好改。整個過程我寫在 [**用 Claude Code 建台股追蹤系統**](/posts/claude-code-finmind-stock-tracking/)，後來長成會自己選股、盯盤的版本在 [**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/)。

想快速試試看，用官方 MCP 或 Skill 最省事；想做成每天自動跑的系統，我比較推薦自己的腳本 + skill。如果你還分不清 MCP 跟 skill 差在哪，可以看這篇：[**MCP、Tools、Skills 差在哪**](/posts/mcp-tools-skills/)。

## FinMind、yfinance、證交所 OpenAPI 怎麼選？

抓台股資料，常見的還有 yfinance 跟證交所 OpenAPI。簡單比較：

| | FinMind | yfinance | 證交所 OpenAPI |
|------|------|------|------|
| 資料範圍 | 台股為主，籌碼、財報、期貨都有 | 全球股價為主 | 證交所自己的資料 |
| 歷史資料 | 長（最早約 1994 年） | 約 2000 年起 | 主要是當日資料，歷史要自己存 |
| 籌碼面（法人、融資券） | ✅ | ❌ | 部分有 |
| 費用 | 免費版＋付費方案 | 免費 | 免費 |
| 適合 | 台股研究、自動化 | 美股、全球市場 | 只要今天的行情 |

（歷史範圍參考 [**FinLab 的台股 API 比較**](https://finlab.finance/blog/python-get-taiwan-stock-data)）

**如果你主要做台股，又想看三大法人、融資融券這些籌碼資料，FinMind 幾乎是最省事的選擇。** 只抓美股的話，yfinance 就夠了。

## 常見問題 FAQ

### FinMind 是什麼？

FinMind 是一個以台股為主的開源金融資料平台，提供股價、籌碼、財報、期貨、國際市場等資料，可以用 API 或 Python 套件取得。官網列出免費版 45 種、最高方案 97 種資料集。

### FinMind 要錢嗎？

有免費版，不用綁卡、沒有期限。付費方案 Backer 每月 NT$699（年繳 NT$5,499）、Sponsor 每月 NT$999（年繳 NT$8,888）、Sponsor Pro 每月 NT$3,330（年繳 NT$29,620），都是單次付款、不會自動續扣。

### FinMind API 每小時可以打幾次？

免費版未登入 300 次、註冊並帶 token 600 次；Backer 1,600 次、Sponsor 6,000 次、Sponsor Pro 20,000 次。超過會回 HTTP 402，下一個小時重置。

### FinMind 免費版可以抓全市場股價嗎？

不行。免費版要指定股票代號（`data_id`）一檔一檔抓；不帶代號、一次抓某天全市場要 Backer 以上。我實測免費版會回 `Your level is free`。

### FinMind 可以商業使用嗎？

只有 Sponsor Pro 可以用在公司內部系統、SaaS 或商業產品。Free、Backer、Sponsor 都限非商業使用。任何方案都不能轉散布原始資料。

### FinMind 好用嗎？有什麼缺點？

我用了大半年，覺得**資料完整、API 簡單**，台股籌碼資料尤其省事。缺點是：免費版要一檔一檔抓、還原股價要付費；每個資料集的欄位格式不太一樣，要合併時得自己處理；額度用完會回 402，自動化腳本要記得處理重試。這些我都是讓 Claude Code 寫腳本時一起處理掉的。

### FinMind 有優惠嗎？

官網公開的省錢方式是年繳（Sponsor 省約 26%、Backer 省約 34%）、已購方案補差額升級，以及學校的校園方案。我沒有推薦碼，也不建議為了找優惠碼去點來路不明的連結。

## 結論

FinMind 是我目前覺得抓台股資料最省事的方式：資料整理好、API 簡單、有免費版可以先試。

**只追蹤自己的持股，免費版就夠了；要掃全市場、看盤中即時或分點，再升級到 Backer 或 Sponsor。** 先用免費版做到卡住，你自然會知道自己需要哪個方案。

如果你想再往前走一步——讓 AI 用這些資料幫你做策略研究、回測，一路做到會自己下單的系統——我正在把整套做法整理成一門課《用 AI 打造自動化交易系統》。**想搶先知道開課消息，[加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) 跟我說一聲「交易課」就好～**（課程教的是怎麼把工具做出來、做得安全，不報明牌、也不保證賺錢😂）

延伸閱讀：
* [**用 Claude Code 建台股追蹤系統 — AI 幫你接 API、管持倉**](/posts/claude-code-finmind-stock-tracking/)
* [**用 Claude Code 打造台股 AI Agent：盤前選股、盤中盯盤、訊號發 Telegram**](/posts/claude-code-stock-agent-monitor-alert/)
* [**網格交易回測：用台積電 6 年資料實測**](/posts/grid-trading-backtest-tsmc/)（資料就是用 FinMind 抓的）
* [**用 Claude Code + Shioaji 打造自動下單機器人**](/posts/claude-code-shioaji-auto-trading-bot/)
* [**Google Sheet 股票損益計算：自動更新最新股價**](/posts/google-sheet-stock-income-statement/)（還在用 GOOGLEFINANCE 的話）

希望這篇對大家有一丁點兒的幫助～

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 想上交易課、或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

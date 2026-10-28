---
title: "GOOGLEFINANCE 台股教學：Google Sheet 抓即時股價、ETF、歷史股價（2026 實測，附上櫃股解法）"
date: 2026-10-28
author: HoMuChen
category: 生活
tags: [Google Sheet, 台股, GOOGLEFINANCE, 股票]
image: https://storage.googleapis.com/homuchen.com/images/googlefinance-taiwan-stock-0.jpg
description: "GOOGLEFINANCE 抓台股要加 TPE: 前綴，上市股、ETF 都抓得到，上櫃股會 #N/A。我 2026 年實測 20 多條公式：即時股價、漲跌幅、本益比、歷史收盤價、走勢圖，附持股損益表範本與上櫃股解法。"
---

**快速總結（TL;DR）**：在 Google Sheet 用 `GOOGLEFINANCE` 抓台股，代號要寫成 **`TPE:2330`** 這種格式，公式是 `=GOOGLEFINANCE("TPE:2330","price")`。我在 2026 年 10 月 28 日實測：**上市股票和上市 ETF（0050、006208、00878）都抓得到**，價格跟證交所收盤價一致；**上櫃股票（例如 6488 環球晶）不管寫 `TPE:`、`TPEX:` 還是 `TWO:` 都是 `#N/A`**，要改用 `IMPORTXML` 或 API。另外有一個大坑：**代號沒加 `TPE:`，`"2330"` 會抓到一檔港股**。

不知道大家有沒有這樣的經驗？打開記錄股票的 Google Sheet，想看看今天賺了還賠了，結果整排都是 `#N/A`😱

我 2021 年寫過一篇 [**Google Sheet 股票損益表**](/posts/google-sheet-stock-income-statement/)，用的就是 `GOOGLEFINANCE`。那篇文章底下最常被問的問題，就是「為什麼我的台股抓不到？」後來我自己改用 FinMind API 寫程式抓資料，但我知道大部分人只想要一張打開就會自己更新的試算表，不想寫程式。

所以這次我開了一張新的 Google Sheet，把 `GOOGLEFINANCE` 對台股的用法**從頭實測一遍**，再拿 FinMind 的證交所資料逐筆比對。這篇整理：

* GOOGLEFINANCE 台股代號怎麼寫（上市、ETF、上櫃哪些抓得到）
* 抓即時股價：常用的 12 個屬性，附台積電實測值
* 抓歷史股價：收盤價、開高低收、週線
* 實戰：一張會自己更新的持股損益表
* 上櫃股抓不到怎麼辦
* 常見錯誤：`#N/A`、抓到港股、漲跌幅格式

> **關於作者**：我是工程師阿穆，寫程式十多年，用 Google Sheet 記帳、追蹤台股很多年，也寫過 [**FinMind 台股 API 教學**](/posts/finmind-taiwan-stock-api-guide/)。本文所有公式都在 2026/10/28 實際跑過，數字是當天的實測結果。

---

## GOOGLEFINANCE 台股代號怎麼寫？

先看函數長怎樣，[**Google 官方說明**](https://support.google.com/docs/answer/3093281?hl=zh-Hant)的語法是：

```
=GOOGLEFINANCE(代號, [屬性], [開始日期], [結束日期或天數], [間隔])
```

除了代號，後面都可以省略。只填代號的話，預設就是抓現價。

台股的代號格式是 **`交易所:股票代號`**，上市股票的交易所代碼是 **`TPE`**：

```
=GOOGLEFINANCE("TPE:2330","price")
```

這樣就能抓到台積電的現價。我實測了幾種常見的寫法，結果整理如下：

| 寫法 | 標的 | 結果 |
|------|------|------|
| `TPE:2330` | 台積電（上市） | ✅ 2425 |
| `TPE:0050` | 元大台灣50（上市 ETF） | ✅ 108.65 |
| `TPE:006208` | 富邦台50（上市 ETF） | ✅ 249.05 |
| `TPE:00878` | 國泰永續高股息（上市 ETF） | ✅ 35.65 |
| `TPE:6488` | 環球晶（上櫃） | ❌ `#N/A` |
| `TPEX:6488` | 環球晶（上櫃） | ❌ `#N/A` |
| `TWO:6488` | 環球晶（上櫃） | ❌ `#N/A` |
| `TPEX:8069` | 元太（上櫃） | ❌ `#N/A` |
| `TPE:00679B` | 元大美債20年（上櫃債券 ETF） | ❌ `#N/A` |
| `2330`（沒加前綴） | — | ⚠️ 抓到港股 |

上面的價格都是 10/28 收盤價，我拿 FinMind 的證交所資料比對過，**每一檔都一模一樣**。

結論很簡單：

* **上市股票、上市 ETF**：加 `TPE:` 就抓得到
* **上櫃股票**：網路上有文章說用 `TPEX:` 就可以，但我 2026 年實測**三種前綴全部 `#N/A`**。錯誤訊息是「系統計算 GOOGLEFINANCE 期間，查詢「6488」符號未傳回任何資料」
* **債券 ETF**：很多債券 ETF（像 00679B）其實是在櫃買中心掛牌，所以也一起抓不到

不確定一檔股票是上市還是上櫃？去 [**證交所**](https://www.twse.com.tw/) 或 Yahoo 股市查一下就知道，Yahoo 網址結尾是 `.TW` 的是上市，`.TWO` 的是上櫃。

### 最大的坑：沒加 TPE: 會抓到港股

這個真的很容易中😂 如果你只寫 `"2330"`：

```
=GOOGLEFINANCE("2330","name")
```

回傳的是 **China Uptown Group Co Ltd**，幣別是 **HKD**，現價 0.2。是一檔香港股票！

而且它不會報錯，你只會看到一個很小的數字，以為台積電崩盤了🤣 所以**一定要加 `TPE:`**，或是用下面的 `currency` 屬性檢查一下，台股應該回傳 `TWD`。

![GOOGLEFINANCE 台股代號實測：上櫃股 #N/A、沒加前綴抓到港股、IMPORTXML 抓上櫃股](https://storage.googleapis.com/homuchen.com/images/googlefinance-taiwan-stock-2.jpg)

---

## 抓即時股價：常用屬性一覽

第二個參數是「屬性」，決定你要抓什麼。下面是我用台積電實測的結果（2026/10/28 下午）：

| 屬性 | 意思 | 台積電實測值 |
|------|------|-------------|
| `price` | 現價（預設） | 2425 |
| `closeyest` | 昨收 | 2400 |
| `changepct` | 今日漲跌幅（%） | 1.04 |
| `volume` | 今日成交量（股） | 20806835（約 2.08 萬張） |
| `high52` | 52 週最高 | 2705 |
| `pe` | 本益比 | 24.68 |
| `eps` | 每股盈餘 | 98.25 |
| `marketcap` | 市值（台幣） | 62885973000000（約 62.9 兆） |
| `currency` | 幣別 | TWD |
| `name` | 公司名稱 | Taiwan Semiconductor Manufacturng Co Ltd |
| `tradetime` | 最後成交時間 | 2026/10/28 下午 |
| `datadelay` | 資料延遲（分鐘） | 0 |

幾個實測時發現的小細節：

* **`changepct` 回傳的已經是百分比數字**：1.04 代表漲 1.04%。如果你直接把儲存格格式改成「百分比」，會變成 104%😱 要嘛不改格式，要嘛先除以 100。
* **`volume` 的單位是「股」不是「張」**：20,806,835 股，換算成張要除以 1000。我比對過，跟證交所的成交股數一致。
* **`name` 只有英文名稱**，還是 Google 自己打錯字的 “Manufacturng”😂 想顯示中文名稱，自己多開一欄打就好。
* **報價可能延遲**：官方說明寫「最長可能延遲 20 分鐘」，盤中看到的不一定是即時價，收盤後就沒差了。

另外 `GOOGLEFINANCE` 也能抓匯率，例如美元兌台幣：

```
=GOOGLEFINANCE("CURRENCY:USDTWD")
```

我實測回傳 32.43，有買美股或外幣資產的話，換算台幣很方便。

---

## 抓歷史股價：收盤價、開高低收、週線

只要加上日期參數，`GOOGLEFINANCE` 就會變成抓歷史資料，而且會**自動展開成一整個表格**（含標題列），所以公式下面要留空間。

### 抓一段期間的每日收盤價

```
=GOOGLEFINANCE("TPE:2330","close",DATE(2026,10,13),DATE(2026,10,24))
```

這會回傳 Date 和 Close 兩欄。我拿這 8 筆跟 FinMind 比對，**日期和收盤價全部一致**：

| 日期 | GOOGLEFINANCE | 證交所（FinMind） |
|------|--------------|------------------|
| 10/13 | 2490 | 2490 |
| 10/14 | 2490 | 2490 |
| 10/15 | 2440 | 2440 |
| 10/16 | 2420 | 2420 |
| 10/19 | 2420 | 2420 |
| 10/20 | 2405 | 2405 |
| 10/21 | 2420 | 2420 |
| 10/22 | 2385 | 2385 |

幾個要注意的地方：

* **只會回傳有開盤的日子**：週末和休市日不會出現，像這段期間的 10/23 台股沒有交易，就沒有那一天。
* **日期會帶時間**：顯示成「2026/10/13 下午 1:30」，也就是台股收盤時間。只想看日期的話，把那欄的格式改成「日期」就好。
* **官方說明有提到日期可能位移一天**（Google 把日期當成 UTC 中午處理），但我比對台股的結果沒有位移，可以放心用。

### 一次抓開高低收：all

屬性改成 `all`，會一次回傳 Date、Open、High、Low、Close、Volume 六欄：

```
=GOOGLEFINANCE("TPE:0050","all",DATE(2026,10,20),DATE(2026,10,28))
```

我比對 0050 的結果，**開盤、最高、最低、收盤都跟證交所一致，但歷史成交量對不上**（例如 10/20 是 105,412,059，證交所是 123,086,544）。所以歷史成交量參考就好，要精準的話還是用證交所或 FinMind 的資料。

第四個參數也可以填「天數」而不是結束日期，但我實測回傳的筆數不太直覺，**建議直接寫結束日期**，比較不會搞混。

### 抓週線：WEEKLY

最後一個參數填 `"WEEKLY"`（或數字 `7`），就會變成每週一筆：

```
=GOOGLEFINANCE("TPE:2330","close",DATE(2026,9,1),DATE(2026,10,24),"WEEKLY")
```

每一筆是**該週最後一個交易日**的收盤價。間隔只有 `"DAILY"` 和 `"WEEKLY"` 兩種，沒有月線。

### 小提醒：Apps Script 讀不到歷史資料

如果你想用 Apps Script 或 Sheets API 把歷史股價讀出來做自動化，會拿到 `#N/A`。這是官方明寫的限制：歷史資料只能在試算表裡看，不能下載或用程式讀取。要做自動化，還是得找 API。

---

## 實戰：一張會自己更新的持股損益表

把上面的東西組起來，就是一張打開就會自己更新的持股損益表：

![GOOGLEFINANCE 台股持股損益表範例：現價、漲跌幅、市值、未實現損益、近 90 天走勢](https://storage.googleapis.com/homuchen.com/images/googlefinance-taiwan-stock-1.jpg)

（股數和成本價是我隨便填的範例數字，不是我的持股～）

每一欄的公式：

| 欄位 | 公式（第 2 列） |
|------|----------------|
| A 代號 | 自己打，例如 `TPE:2330` |
| B 股數 | 自己打（1 張 = 1000 股） |
| C 成本價 | 自己打 |
| D 現價 | `=GOOGLEFINANCE(A2,"price")` |
| E 今日漲跌% | `=GOOGLEFINANCE(A2,"changepct")` |
| F 市值 | `=B2*D2` |
| G 未實現損益 | `=(D2-C2)*B2` |
| H 近 90 天走勢 | `=SPARKLINE(GOOGLEFINANCE(A2,"close",TODAY()-90,TODAY()))` |

寫好第 2 列之後，往下拉就能套用到每一檔股票。

H 欄的 `SPARKLINE` 會在儲存格裡畫一條迷你走勢圖，用法可以參考我之前寫的 [**Sparkline，在儲存格裡插入迷你圖表**](/posts/google-sheet-sparkline/)。

想要更完整的版本（加上已實現損益、股利），可以參考 [**我如何製作股票損益表**](/posts/google-sheet-stock-income-statement/)；如果你本來就用 Google Sheet 記帳，也可以把這張表接到 [**Google Sheet 記帳教學**](/posts/google-sheet-how-to-do-bookkeeping/)的資產總覽裡。

---

## 上櫃股抓不到怎麼辦？

這是最多人卡住的地方。我的建議依難易度排：

### 方法一：IMPORTXML 抓 Yahoo 股市（不用寫程式）

Google Sheet 有一個 `IMPORTXML` 函數，可以抓網頁上的資料。Yahoo 股市的上櫃股網址是 `https://tw.stock.yahoo.com/quote/6488.TWO`，用下面這條公式就能抓到現價：

```
=IMPORTXML("https://tw.stock.yahoo.com/quote/6488.TWO","//span[contains(@class,'Fz(32px)')]")
```

我實測抓到 849，跟櫃買中心的 10/28 收盤價一樣。換股票只要改網址裡的代號。

但這招有幾個缺點，要先知道：

* **第一次用要按「允許存取」**：試算表上方會跳出黃色警告，說「某些公式正試圖傳送資料到外部或接收外部的資料」，要按「允許存取」才會開始抓，沒按的話會顯示 `#REF!`。
* **Yahoo 改版就會壞**：公式裡的 `Fz(32px)` 是 Yahoo 網頁的樣式名稱，Yahoo 一改版，公式就會抓不到，要重新找。
* **不適合大量使用**：每一格都是去抓一次網頁，抓太多檔可能會變慢或被擋。

所以它適合「我只有一兩檔上櫃股」的情況。

### 方法二：改用 API（FinMind）

如果上櫃股很多，或是你想要穩定的資料，就要改用 API 了。我自己是用 [**FinMind**](/posts/finmind-taiwan-stock-api-guide/)，上市、上櫃、ETF 都有，免費版註冊後每小時 600 次，追蹤幾十檔股票綽綽有餘。

不會寫程式也沒關係，我在 [**用 Claude Code 建台股追蹤系統**](/posts/claude-code-finmind-stock-tracking/) 裡示範過，整個過程是用對話叫 AI 寫的。

---

## GOOGLEFINANCE 常見錯誤

### 出現 #N/A

照我實測，最常見的原因有三個：

1. **沒加 `TPE:` 前綴**，或是打錯（例如打成 `TW:2330`）
2. **是上櫃股票**：`GOOGLEFINANCE` 目前抓不到，改用上面的方法
3. **屬性打錯**：屬性要用英文、要加雙引號，例如 `"price"` 不能寫成 `price`

### 數字小得很奇怪

先檢查是不是忘了加 `TPE:`，抓到別的市場的股票了。用 `=GOOGLEFINANCE(A2,"currency")` 看一下，台股應該是 `TWD`。

### 漲跌幅變成 104%

`changepct` 回傳的 1.04 已經是「1.04%」的意思，不要再套百分比格式，或者先除以 100 再套。

### Excel 可以用 GOOGLEFINANCE 嗎？

不行，`GOOGLEFINANCE` 是 Google Sheet 專屬的函數，Excel 裡沒有。想在 Excel 自動抓股價，要用 Excel 自己的「股票」資料類型，或是把 Google Sheet 的資料匯出過去。

### 價格好像沒更新

盤中報價可能延遲最多 20 分鐘，Google Sheet 也不是每秒更新。重新整理頁面通常就會抓到新的。如果你需要真正即時的報價，`GOOGLEFINANCE` 就不適合了。

---

## GOOGLEFINANCE 夠用嗎？什麼時候該換方法

最後整理一下我自己的判斷：

| 你的情況 | 建議 |
|---------|------|
| 只買上市股票和 ETF，想看每天損益 | **GOOGLEFINANCE 就夠用** |
| 有一兩檔上櫃股 | GOOGLEFINANCE + IMPORTXML |
| 上櫃股很多、要籌碼或財報資料 | 改用 FinMind 等 API |
| 想要自動化（每天記錄、通知） | API + 程式，可以叫 AI 幫你寫 |

我自己後來的做法是叫 AI 寫一個 [**淨資產儀表板**](/posts/claude-code-net-worth-dashboard/)，股票、現金、房貸一起看。但如果你只是想知道「今天我的股票漲還跌」，**一張 Google Sheet 加 `GOOGLEFINANCE` 真的就很夠了**，五分鐘就能做好～

## 結論

今天簡單地跟大家分享了 `GOOGLEFINANCE` 抓台股的用法，重點就三個：

* **上市股、上市 ETF：代號寫 `TPE:2330`，抓得到，而且數字準**
* **上櫃股：目前抓不到，用 IMPORTXML 或 API**
* **一定要加 `TPE:`，不然會抓到港股**

這些坑都是我自己實測踩出來的，希望你不用再踩一次，對你整理自己的股票有一丁點兒的幫助～

（本文只是試算表工具教學，數字都是 2026/10/28 的實測結果，不構成任何投資建議。）

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

---
title: "Claude 股票分析 Skill 推薦：國外最紅的 tradermonty，我把它改成台股版（附開源 Skill）"
date: 2026-11-07
author: HoMuChen
category: AI
tags: [Claude Skills, Claude Code, 台股, 市場寬度, FinMind, AI 股票分析]
image: https://storage.googleapis.com/homuchen.com/images/claude-stock-skill-tradermonty-taiwan-0.jpg
description: "Claude 股票 skill 推薦哪個？國外最常被推薦的是 tradermonty/claude-trading-skills：74 個交易 skill、MIT 開源、不報明牌只管流程。我實際裝起來跑，再用 FinMind 把市場寬度 skill 改成台股版，開源附安裝教學。"
---

10 月 6 日，加權指數衝到 49,823 點，離 5 萬點只差一步。

那天如果你問我台股強不強，我大概會說：「很強啊，都要 5 萬點了！」

但我最近跑了一個數字，才發現那天其實有點怪：**上市股票裡，只有 55% 站在自己的 200 日均線上面。** 指數在歷史高點，卻有快一半的股票是往下走的。

一個月後，11 月 6 日，指數跌到 39,702 點，從高點掉了兩成；站上 200 日線的股票，只剩 **23.5%**。

這種「指數很強、大部分股票沒跟上」的狀況，有個專有名詞叫**市場寬度（Market Breadth）不足**。

會注意到這件事，是因為我在玩一個國外很紅的 Claude skill。它本來只能看美股，我請 Claude Code 把它改成台股版，跑出來的就是上面這些數字。

> **TL;DR**：想找 Claude 股票分析 skill，我推薦從 [**tradermonty/claude-trading-skills**](https://github.com/tradermonty/claude-trading-skills) 開始。它是我找到的個人投資者 skill 裡，GitHub 上最多人用的一套（3,663 顆星、MIT 開源），有 74 個 skill，涵蓋市場環境、選股器、部位大小、交易日誌和檢討，**而且它刻意不報明牌，只幫你把決策流程結構化**。缺點是資料源全是美股，所以我用 FinMind 把其中的「市場寬度」skill 改成台股版：**只換資料層，評分邏輯一行都不改**，台股版已經[**開源在 GitHub**](https://github.com/HoMuChen/tw-market-breadth-skill)。

這篇會聊這些：

* Claude 股票分析 skill 是什麼？
* 國外最紅的 tradermonty 有哪些 skill、跟其他選擇比起來如何
* 怎麼安裝，不付錢能用哪些
* 實測：市場寬度 skill 在算什麼
* 改成台股版：只換資料，不換腦袋
* 台股跑出來的結果，跟它的限制

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與自動化系統，自己的[**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/) 每天都在跑 skill。本文的安裝、試跑、改寫都是我用 Claude Code 實際做的，台股資料來自 [**FinMind**](/posts/finmind-taiwan-stock-api-guide/)。

> 免責：本文是工具介紹與市場觀察，不是投資建議。

## Claude 股票分析 Skill 是什麼？

**Claude 股票分析 skill，就是一份教 Claude「怎麼分析股票」的 SOP，加上幫它抓資料、算指標的小程式。** 你裝好之後只要用平常的話問「現在市場健不健康？」，Claude 就會自己找到對應的 skill，照裡面的步驟跑程式、讀結果、跟你解釋。

一個 skill 長這樣：

```
market-breadth-analyzer/
├── SKILL.md          # 給 Claude 看的說明書：什麼時候用、怎麼跑、怎麼解讀
├── scripts/          # 真正抓資料、算分數的 Python
└── references/       # 方法論文件，需要時 Claude 才會去讀
```

如果你還不太清楚 skill 是什麼，可以先看我之前寫的[**Skill 是什麼？讓 AI Agent 從通才變專家**](/posts/what-is-ai-agent-skill/)；想知道它跟 MCP 差在哪，可以看[**MCP / Tools / Skills：AI Agent 的三種能力擴充**](/posts/mcp-tools-skills/)。

簡單講，**沒有 skill 的 Claude 像一個很聰明但第一天上班的新人**，你問它股市怎麼樣，它只能憑印象回答；**有了 skill，它手上就多了一本前輩寫好的作業手冊**，還附計算機 😎

## Claude 股票 Skill 推薦哪個？國外最紅的 tradermonty

**如果你是一般投資人，我推薦 [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)。** 我上網找了一圈「Claude stock skill」，它是最常被推薦、也最活躍的一套，而且是寫給個人投資者、不是寫給投行的：

| 項目 | 數字（2026-11-06） |
|------|------|
| GitHub 星數 | 3,663 |
| Fork 數 | 797 |
| Skill 數量 | 74 個 |
| 現成工作流程 | 13 個（例如每日 15 分鐘市場檢查、每週持股檢討） |
| 授權 | MIT（可以自由修改、衍生） |
| 開始時間 | 2025 年 10 月，到 11 月初都還在更新 |

作者在 README 裡講得很清楚：這是他為了改善自己交易流程做的工具，**目標不是把買賣決策外包給 AI，而是把市場檢查、風險控管、交易計畫、日誌和檢討這些流程結構化**。它不是訊號服務，也不保證獲利。

我很喜歡這個定位，因為跟我在[**AI 選股實測**](/posts/ai-stock-picking-taiwan-backtest/)那篇的結論一樣：**AI 最有用的角色是研究助理，不是投顧。**

### 74 個 skill，大概分成這幾類

| 類別 | 代表 skill | 在做什麼 |
|------|-----------|---------|
| 市場環境 | `market-breadth-analyzer`、`market-top-detector`、`macro-regime-detector` | 判斷現在是多頭、空頭還是盤整 |
| 選股器 | `canslim-screener`、`vcp-screener`、`pead-screener`、`value-dividend-screener` | 把知名的選股方法論各做成一個 skill |
| 風險與部位 | `position-sizer`、`drawdown-circuit-breaker`、`pre-trade-discipline-gate` | 下單前先算好要買多少、虧多少要停 |
| 日誌與檢討 | `trader-memory-core`、`signal-postmortem`、`weekly-performance-digest` | 記錄每筆交易、事後檢討 |
| 研究與回測 | `backtest-expert`、`edge-strategy-designer` | 設計和驗證策略 |
| 個股分析 | `us-stock-analysis`、`technical-analyst` | 基本面、技術面、比較報告 |

最讓我驚訝的是第三、第四類。大部分人做股票 AI 工具，都在想怎麼「選出會漲的股票」；它卻花了很多力氣在**「下單前先擋住自己」**跟**「交易完要檢討」**，像 `pre-trade-discipline-gate` 就是一道下單前的紀律檢查。

這很像健身教練不只教你動作，還幫你記每次練了什麼、哪裡退步了。真正讓人進步的，常常是後面這段 😂

### 跟其他股票 skill 比起來呢？

| Repo | 星數 | 適合誰 |
|------|-----:|--------|
| [**anthropics/financial-services**](https://github.com/anthropics/financial-services) | 41,070 | Anthropic 官方，給投行、研究員：DCF、可比公司、財報分析、晨報，多半要搭 Excel 和付費資料源 |
| [**tradermonty/claude-trading-skills**](https://github.com/tradermonty/claude-trading-skills) | 3,663 | 個人投資者、波段交易者：市場環境、選股器、風控、日誌 |
| [**quant-sentiment-ai/claude-equity-research**](https://github.com/quant-sentiment-ai/claude-equity-research) | 752 | 想要一份華爾街格式的個股研究報告 |
| [**yennanliu/InvestSkill**](https://github.com/yennanliu/InvestSkill) | 276 | 美股個股估值、財報預覽 |

（星數為 2026-11-06 GitHub API 查詢）

官方那套星數最多，但它是給專業金融從業人員的，很多 skill 是在做 Excel 估值模型、投資簡報，也常要搭配付費的金融資料源。**如果你是一般投資人，tradermonty 比較接地氣。**

可惜的是，上面這些**全部都是美股**。我找了一圈，沒看到任何一個支援台股的 Claude skill。

## 怎麼安裝？不付錢能用哪些

### Claude Code

把想要的 skill 資料夾複製到 `~/.claude/skills/` 就好：

```bash
git clone --depth 1 https://github.com/tradermonty/claude-trading-skills.git
cp -r claude-trading-skills/skills/market-breadth-analyzer ~/.claude/skills/
```

之後在 Claude Code 裡問「美股市場寬度現在怎麼樣？」，它就會自己用這個 skill。

### Claude 網頁版

到 repo 的 Releases 下載 `.skill` 檔，在 Claude 的 **Customize > Skills** 上傳就好。要先在 Settings 打開 Code execution。

### 免費入門的 5 個 skill

很多 skill 要接付費資料（FMP、FINVIZ Elite、Alpaca 券商 API），但作者有整理一條**不用付費 API** 的入門路徑：

1. `market-breadth-analyzer`：市場寬度評分，用作者公開的 CSV
2. `uptrend-analyzer`：上升趨勢參與度
3. `position-sizer`：部位大小計算，純計算
4. `trader-memory-core`：本機 YAML 交易日誌
5. `signal-postmortem`：交易檢討框架

> ⚠️ 這是第三方程式碼。我裝之前請 Claude Code 先把 `market-breadth-analyzer` 的 script 掃過一遍：對外只有用 `requests` 去抓作者 GitHub Pages 上的公開 CSV，寫檔只寫到輸出資料夾，沒有執行任何外部指令。建議你裝任何 skill 之前也這樣做一次。

## 實測：市場寬度 skill 在算什麼？

我挑 `market-breadth-analyzer` 來實測，因為它不用 API key，而且「市場寬度」這個概念，台股投資人其實很需要。

### 市場寬度是什麼？

**市場寬度，就是「有多少比例的股票跟著大盤一起走」。** 這個 skill 用的定義是：**每天有幾成的股票，收盤價站在自己的 200 日均線上面。**

用班上考試來比喻：

* **加權指數**像全班平均分數。班上有一個人考 100 分，平均就會被拉高
* **市場寬度**像及格人數。它不管那個 100 分的人，只問「有幾個人及格」

台股的加權指數是市值加權，台積電一檔就占了很大的比重。所以很常發生「台積電大漲、指數創新高，但你手上的股票都在跌」的狀況。**指數告訴你班平均，寬度告訴你多數人過得好不好。**

### 6 個分項，算出 0–100 分

它把寬度資料拆成 6 個面向打分數，再加權成一個總分：

| 分項 | 權重 | 在看什麼 |
|------|-----:|---------|
| 寬度水準與趨勢 | 25% | 現在有幾成股票站上 200 日線，長期趨勢往上還往下 |
| 8 日 vs 200 日均線交叉 | 20% | 短期寬度在長期平均之上還之下 |
| 高低點循環位置 | 20% | 離上一個寬度高點、低點多久了 |
| 空頭訊號 | 15% | 長期趨勢往下，而且短期跌破長期（作者叫它 Pink Zone） |
| 歷史百分位 | 10% | 現在的寬度在過去十年排第幾 |
| 指數與寬度背離 | 10% | 指數在漲、寬度在跌，是最危險的組合 |

### 美股跑出來：50 分，中性

我在 11 月 6 日跑了一次，資料到 11 月 5 日：

```
[1/6] Current Breadth Level & Trend... Score: 62
[2/6] 8MA vs 200MA Crossover... Score: 50
[3/6] Peak/Trough Cycle Position... Score: 45
[4/6] Bearish Signal Status... Score: 50
[5/6] Historical Percentile... Score: 30
[6/6] S&P 500 vs Breadth Divergence... Score: 50.0

Composite Score: 50.0/100
Health Zone: Neutral
```

S&P 500 成分股的 8 日寬度是 0.633，也就是大約六成三的股票站在 200 日線上，算是中性偏健康。

## 改成台股版：只換資料，不換腦袋

接下來是重點。我想知道台股的寬度長怎樣，但這個 skill 只吃美股資料。

翻了一下它的程式，發現它的架構切得很乾淨：

1. **資料層**：作者另一個 repo [**market-breadth-analysis**](https://github.com/tradermonty/market-breadth-analysis) 每天算好 S&P 500 的寬度，輸出成一份 CSV
2. **評分層**：skill 讀這份 CSV，算 6 個分項

**所以只要我能產生一份格式一模一樣的台股 CSV，評分層完全不用動。** 這也是寫 skill 很值得學的一點：**把「資料從哪來」跟「怎麼判斷」拆開，換市場的時候只要換一半。**

### Step 1：用 FinMind 算台股的寬度

我照上游 repo 的算法寫了一支 `build_tw_breadth.py`，核心只有十幾行：

```python
# closes：每檔股票的還原收盤價，欄是股票代號、列是日期
ma = closes.rolling(200).mean()
eligible = ma.notna() & closes.notna()             # 有價、而且算得出 200 日均線的才算
above = (closes > ma).astype(float).where(eligible)

raw = above.mean(axis=1)                            # 每天站上 200 日線的比例
ma200 = raw.ewm(span=200, adjust=False).mean()      # 長期趨勢
ma8 = raw.ewm(span=8, adjust=False).mean()          # 短期動能

peaks, _ = find_peaks(ma200, distance=50, prominence=0.015)     # 寬度高點
troughs, _ = find_peaks(-ma200, distance=50, prominence=0.015)  # 寬度低點
bearish = (trend == -1) & (ma8 < ma200)                         # 空頭訊號
```

股票池用 FinMind 的 `TaiwanStockInfo` 抓上市普通股（4 碼、排除 ETF），一共 1,230 檔；股價用還原股價 `TaiwanStockPriceAdj`，避免除權息被當成跌破均線。原本 CSV 裡放 S&P 500 價格的欄位，我放加權指數。

### Step 2：把 CSV 餵給原版評分程式

原版程式只吃網址，所以我在本機開一個小小的 HTTP server 把 CSV 丟給它：

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory data/ &

python3 ~/.claude/skills/market-breadth-analyzer/scripts/market_breadth_analyzer.py \
  --detail-url http://127.0.0.1:8765/market_breadth_data.csv \
  --summary-url http://127.0.0.1:8765/market_breadth_summary.csv
```

### Step 3：包成 skill

最後把這兩步驟包成一個新的 skill `tw-market-breadth`，之後我只要問 Claude「台股漲勢健不健康？」它就會自己跑。我把它開源在 GitHub，安裝方式放在文末。

### 要打多少次 API？

全上市 1,230 檔，每檔一次請求，加上加權指數，大約 1,231 次：

* **免費版**：註冊後每小時 600 次，要分兩個多小時；而且免費版**不能用還原股價**，要改用未還原的 `TaiwanStockPrice`
* **付費版**：我用的是 Sponsor（每小時 6,000 次），開 8 條並行，從抓資料到出報告不到 2 分鐘

FinMind 各方案的差別，可以看我之前寫的[**FinMind 是什麼？台股 API 免費額度、方案價格與 Python 教學**](/posts/finmind-taiwan-stock-api-guide/)。

## 台股跑出來：19.1 分，Critical

資料到 11 月 6 日，1,164 檔有價格的上市普通股，其中 1,071 檔算得出 200 日均線：

```
[1/6] Current Breadth Level & Trend... Score: 35
[2/6] 8MA vs 200MA Crossover... Score: 5
[3/6] Peak/Trough Cycle Position... Score: 50 (excluded)
[4/6] Bearish Signal Status... Score: 10 [PINK ZONE]
[5/6] Historical Percentile... Score: 10
[6/6] S&P 500 vs Breadth Divergence... Score: 30.0

Composite Score: 19.1/100
Health Zone: Critical
```

把美股跟台股放在一起看：

| | 美股（S&P 500） | 台股（上市普通股） |
|---|---|---|
| 資料截至 | 2026-11-05 | 2026-11-06 |
| 站上 200 日線（8 日平均） | 0.633 | **0.367** |
| 綜合分數 | 50.0 | **19.1** |
| 健康區間 | Neutral 中性 | **Critical** |
| 最弱分項 | 歷史百分位 30 | **8 日 vs 200 日交叉 5** |

台股最弱的是「8 日 vs 200 日交叉」：短期寬度 0.367，已經比長期平均 0.511 低了 0.143。再加上長期趨勢也往下，剛好落在作者說的 Pink Zone。歷史百分位只有 15%，也就是過去十年，有 85% 的時間寬度比現在好。

另外，「高低點循環」這一項因為最近 120 天沒有出現寬度高低點，被程式自動排除，權重分給其他 5 項，所以報告會標「Data Quality: Partial (5/6)」。

### 指數創高那天，股票早就沒跟上

把時間拉長來看更有意思：

| 時間 | 加權指數 | 站上 200 日線的股票比例 |
|------|---------:|---------:|
| 2020-03-19 疫情崩盤 | 8,681 | 3.8% |
| 2022-10-21 空頭底部 | 12,819 | 15.9% |
| 2025-04-09 關稅崩跌 | 17,392 | 3.5% |
| 2026-07-06 這一波寬度最高 | 46,556 | 65.7% |
| 2026-10-06 指數最高 | **49,823** | **55.4%** |
| 2026-11-06 | 39,702 | **23.5%** |

加權指數從 2025 年 11 月初的 28,335 點，一路漲到 2026 年 10 月的 49,823 點。但**寬度的高點出現在 7 月**，那時候有 65.7% 的股票站上 200 日線；之後指數繼續創新高，寬度卻開始往下。到了指數最高的那天，只剩 55.4%。

![加權指數與上市普通股站上 200 日均線比例，2025-06 至 2026-11：寬度 7/6 見高點 65.7%，指數 10/6 見高點 49,823 時寬度只剩 55.4%，11/6 跌到 23.5%](https://storage.googleapis.com/homuchen.com/images/claude-stock-skill-tradermonty-taiwan-1.jpg)

畫成圖更明顯：2025 下半年指數從兩萬一漲到兩萬八，站上 200 日線的股票卻一直在兩成多到四成多之間；今年 7 月寬度到頂，指數則是三個月後才見頂。

用班上的比喻來說，就是**班平均一直創新高，及格人數卻在變少。** 那段時間如果你覺得「大盤漲這麼多，我怎麼沒賺到」，其實很正常，因為越來越多股票根本沒在漲。

這正好是 6 個分項裡「指數與寬度背離」想抓的狀況。

> 再提醒一次：這是回頭看的市場觀察，只有一次，不能證明寬度「預測得到」下跌，也不是叫你賣股票。寬度弱可以弱很久，指數也可能繼續被權值股撐著。

## 台股版的限制，我老實說

* **門檻是美股的經驗值**：0.4、0.6、0.7 這些分界點是作者用 S&P 500 調出來的。台股過去十年寬度高點的平均是 0.669，比美股的 0.722 低一點，所以分數只能當參考
* **持股比例建議別照抄**：報告裡會寫「Equity Exposure 25-40%」，那是原作者對美股的經驗區間，不是我的建議，更不是你的持股比例
* **倖存者偏差**：`TaiwanStockInfo` 只有目前掛牌的股票，已下市的不在裡面。我用自己另外整理、含下市股的資料交叉比對過，兩份每天的寬度相關係數 0.9997，平均只差 0.2 個百分點，影響不大
* **它不會告訴你買什麼**：它回答的是「現在的市場環境適不適合積極」，不是「該買哪一檔」

## 台股版 skill 開源：安裝方式

我把台股版放在 GitHub：[**HoMuChen/tw-market-breadth-skill**](https://github.com/HoMuChen/tw-market-breadth-skill)，MIT 授權，算法跟評分都有標明出處是 tradermonty。

```bash
# 1. 原版評分 skill（tradermonty）
git clone --depth 1 https://github.com/tradermonty/claude-trading-skills.git /tmp/claude-trading-skills
cp -r /tmp/claude-trading-skills/skills/market-breadth-analyzer ~/.claude/skills/

# 2. 台股版 skill
git clone https://github.com/HoMuChen/tw-market-breadth-skill.git ~/.claude/skills/tw-market-breadth

# 3. 套件
pip install -r ~/.claude/skills/tw-market-breadth/requirements.txt
```

再設好兩個環境變數：

| 變數 | 說明 |
|------|------|
| `FINMIND_API_TOKEN` | 你的 FinMind token |
| `TRADERMONTY_SKILL` | 原版 skill 的位置，例如 `~/.claude/skills/market-breadth-analyzer` |

**免費版**記得再加一個 `FINMIND_PRICE_DATASET=TaiwanStockPrice`，因為還原股價要 Backer 以上才有；付費版可以加 `FINMIND_WORKERS=8` 讓它並行抓。

裝好之後，在 Claude Code 問一句「台股市場寬度現在怎麼樣？」就好，大功告成～～🎉

SKILL.md 裡的核心是這段「讀報告」的指示，它決定 Claude 跑完之後怎麼跟你解釋：

```markdown
## Step 2：讀報告

讀 reports/.../market_breadth_*.md，用繁體中文向使用者說明：

1. 綜合分數與健康區間（Health Zone）
2. 最強、最弱的分項，各用一句話解釋原因
3. 目前站上 200 日線的股票比例（Breadth_Index_Raw）與 8MA、200MA
4. 有沒有在 Pink Zone（200MA 下彎且 8MA < 200MA）
5. 指數與寬度是否背離（指數漲、寬度跌最需要注意）
```

如果你想讓 Claude 換個方式解釋，例如「每次都跟上一次的分數比較，告訴我變好還變差」，或「落在 Pink Zone 時，提醒我用 `position-sizer` 重新檢查部位」，改這一段就好。**這就是 skill 好玩的地方：改 SOP 不用改程式。**

## 常見問題

### Claude 股票分析 skill 要錢嗎？

skill 本身免費。tradermonty 是 MIT 開源，複製資料夾就能用；Claude 的部分依你的方案而定，Claude Code 需要付費方案。要花錢的是**資料**：tradermonty 有些 skill 要接 FMP、FINVIZ Elite 這類付費 API，但有 5 個入門 skill 不用付費資料。台股版用 FinMind，免費版就能跑，只是比較慢、而且只能用未還原股價。

### 有支援台股的 Claude 股票 skill 嗎？

我找了一圈，目前公開的股票 skill 幾乎都是美股，中文的則多半是 A 股、港股。台股要自己接資料，最常用的是 FinMind。這篇的台股版就是一個例子：用 FinMind 產生資料，沿用國外 skill 的分析邏輯。

### 股票 skill 跟 MCP 差在哪？

MCP 是讓 AI 接上外部工具的「插座」，skill 是教 AI「怎麼把一件事做對」的說明書。股票分析兩種都可以用；我自己的台股 agent 是用 **script + skill** 接 FinMind，沒有用 MCP，這篇的台股版也是同樣做法。詳細比較在[**MCP / Tools / Skills**](/posts/mcp-tools-skills/)這篇。

### 可以自己寫一個股票 skill 嗎？

可以，而且不難。一個 skill 就是一個資料夾：`SKILL.md` 寫清楚「什麼時候用、怎麼跑、怎麼解讀」，`scripts/` 放抓資料、算指標的程式。我的建議是照 tradermonty 的拆法，**把「資料從哪來」跟「怎麼判斷」分開**，換資料源或換市場時只要改一半。程式不會寫也沒關係，這篇的台股版就是我叫 Claude Code 寫的。

### 市場寬度低，是不是代表要賣股票？

不是。寬度低代表「大部分股票表現不好」，但寬度可以低很久，指數也可能繼續漲。它比較適合用來調整心態跟風險，例如這時候追高要更小心、部位不要太滿，而不是直接當賣出訊號。

## 結語

這次玩下來，我最大的收穫不是那個 19.1 分，而是 tradermonty 的設計方式：**一個 skill 只做一件事、資料跟判斷拆開、刻意不報明牌。** 正因為拆得乾淨，我才能只換資料，就把一個美股工具搬到台股。

如果你也想做自己的股票 skill，我建議不要從「讓 AI 選股」開始，而是從「讓 AI 幫我檢查市場環境、記錄交易、事後檢討」開始。這些事很無聊，但正好是 AI 最擅長、人最容易偷懶的部分 😂

希望對你有一丁點兒的幫助～

如果你想學怎麼用 AI 從「研究、回測」一路做到「自動下單、安全上線」，我正在把整套做法整理成一門課，**想搶先知道開課消息的話，[加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) 跟我說一聲「交易課」就好～**

延伸閱讀：

* [**AI 選股實測：我讓 AI 回測 140 個台股策略，只有 2 種活下來**](/posts/ai-stock-picking-taiwan-backtest/)
* [**用 Claude Code 打造台股 AI Agent：盤前自動選股、盤中盯盤、訊號到就發 Telegram**](/posts/claude-code-stock-agent-monitor-alert/)
* [**用 Claude Code 建台股追蹤系統 — AI 幫你接 API、管持倉，你只要說你買了什麼**](/posts/claude-code-finmind-stock-tracking/)
* [**Skill 是什麼？讓 AI Agent 從通才變專家**](/posts/what-is-ai-agent-skill/)
* [**Hermes Agent 是什麼：會自己長記憶、長技能的 AI Agent**](/posts/hermes-ai-agent/)（tradermonty 也有出 Hermes 版的工作流程包）

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 想上交易課、或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

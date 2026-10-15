# 跨平台企劃：《養一隻台股 AI Agent》YouTube 系列

> 設計文件 — 建立於 2026-06-23
> 主軸：把網站最強 SEO cluster「Claude Code + 股票」延伸為 4 集 YouTube 教學系列

---

## 1. 主題概要

- **系列名稱**：《養一隻台股 AI Agent》（暫定，4 集階梯系列）
- **核心主張**：你已經會用 Claude Code，這系列教你怎麼把它用到位——從「接 API 抓股價」一路長成一隻**會自己選股、盯盤、發 Telegram 通知你**的台股 AI Agent。一集長一層，看完任何一集都有一個能跑的東西。
- **目標受眾**：**沒有要自己寫程式、但已經摸過 Claude Code 跟 terminal、有心自學這類工具的人**。不一定有技術背景，但願意跟著做、會開 terminal、會貼指令、會跑一個 Claude Code session。
  - 卡點不在「terminal 怎麼用」，而在「**怎麼把需求講清楚、讓 Claude 幫我做出能跑的東西**」「為什麼要它寫 CLAUDE.md」「怎麼判斷它寫得對不對」。
  - 賣點語氣：從「入門除魅」上移到「**把工具用到位**」。招牌敘事＝出一張嘴的產品經理。
- **這系列怎麼來的**：源自兩篇站內已驗證的高排名文章——
  - [用 Claude Code 建台股追蹤系統（FinMind）](/posts/claude-code-finmind-stock-tracking/)（站內 SEO 引擎，搜尋流量主力）
  - [用 Claude Code 打造台股 AI Agent：盤前選股、盤中盯盤、發 Telegram](/posts/claude-code-stock-agent-monitor-alert/)（進階升級版）

### 連貫 vs 獨立（系列設計核心）

| 機制 | 做法 |
|------|------|
| **連貫** | 同一個 project 資料夾、同一隻 agent，一集長一層，對齊 HoMuChen 自己的**四層框架（Context → 能力 → 溝通 → 自動化）**。片頭固定放一條「四層進度條」圖，標示這集點亮哪一層。 |
| **獨立** | 每集開頭 60 秒 recap +「沒看過前集？前 2 分鐘幫你補齊，或下載 starter」；每集結尾有明確交付物「看完你手上會有 X」。 |

### 製作規格（全系列共用）

- **Demo 工具**：Claude Code (terminal) 為主，包裝成「你只是貼指令／出一張嘴」。
- **每集長度**：15–25 分鐘，跟著做得出來的完整 tutorial。
- **拍攝順序建議**：EP1 先拍（漏斗頂端、最大搜尋入口、最可能單集爆量）。

---

## 2. 產出規劃

### 影片清單（YouTube，4 集）

| 集 | 主題 | 點亮的層 | 獨立交付物 |
|----|------|---------|-----------|
| **EP1** | 接 FinMind 抓台股 | 能力(工具) + 記憶 | 每天一行指令更新全市場股價的本地系統 |
| **EP2** | 對話式持倉 + 分析 | Context(記憶) | 跟 Claude 說「我買了什麼」就記帳、問一句列損益、叫它做分析 |
| **EP3** | 盤前自動選股 | 能力(主動) | scan 腳本掃全市場、產出今日觀察清單 |
| **EP4** | 盯盤 + Telegram + crontab | 溝通 + 自動化 | 會自己上工、訊號到就敲你的完整 agent |

### 衍生產出（跨平台）

- **Threads**：每集切 1–2 則 repurposed 貼文（`source: repurposed`），導流回對應影片／部落格。
- **部落格**：兩篇來源文章已存在；影片發布後，於文章內嵌入對應影片（反向導流）。
- **投影片**：選配，若要做研討會／直播講解可由 EP4 的四層框架延伸。

---

## 3. 跨平台發布狀態表

| 產出 | 類型 | 狀態 | 檔案路徑 | 發布連結 |
|------|------|------|---------|---------|
| EP1 接 FinMind 抓台股 | YouTube | 規劃中 | `youtube/{date}-claude-stock-ep1-finmind/` | — |
| EP2 對話式持倉 + 分析 | YouTube | 規劃中 | `youtube/{date}-claude-stock-ep2-positions/` | — |
| EP3 盤前自動選股 | YouTube | 規劃中 | `youtube/{date}-claude-stock-ep3-scan/` | — |
| EP4 盯盤 + Telegram + crontab | YouTube | 規劃中 | `youtube/{date}-claude-stock-ep4-agent/` | — |
| EP1 導流 Threads | Threads | 未開始 | `threads/{date}-claude-stock-ep1.md` | — |
| EP2 導流 Threads | Threads | 未開始 | `threads/{date}-claude-stock-ep2.md` | — |
| EP3 導流 Threads | Threads | 未開始 | `threads/{date}-claude-stock-ep3.md` | — |
| EP4 導流 Threads | Threads | 未開始 | `threads/{date}-claude-stock-ep4.md` | — |
| finmind 文章嵌入 EP1 影片 | 部落格 | 已發布(待更新) | `posts/2026-04-25-claude-code-finmind-stock-tracking.md` | /posts/claude-code-finmind-stock-tracking/ |
| agent 文章嵌入 EP4 影片 | 部落格 | 已發布(待更新) | `posts/2026-06-04-claude-code-stock-agent-monitor-alert.md` | /posts/claude-code-stock-agent-monitor-alert/ |

> **狀態更新規則**：撰寫腳本完成 → 改「已撰寫」+ 填路徑；發布 → 改「已發布」+ 填 YouTube/Threads URL。新 session 處理本系列前，先讀本表了解進度。

---

## 4. 各集規劃

### EP1 — 接 FinMind 抓台股（漏斗頂端）

- **Hook**：打開試算表，台股價格全變 `#N/A`（最大共鳴 + 最大搜尋）。
- **核心內容**：
  1. 痛點：`GOOGLEFINANCE` 抓台股不穩（延遲、`#N/A`、依賴 Google）
  2. 為什麼選 FinMind（帶來源比較表）
  3. 申請 FinMind token（螢幕錄逐步）
  4. **核心橋段：你不讀 API 文件，把文件連結丟給 Claude，它自己讀、自己寫 `stock_cache.py`**
  5. 跑 `python3 stock_cache.py today` 一行更新全市場 ~2,500 檔
  6. 叫 Claude 把用法寫進 `CLAUDE.md`（為什麼要這步：下次新對話它就懂這個 project）
- **獨立交付物**：每天一行指令更新全市場股價的本地系統。
- **連貫鉤子（片尾）**：「現在它會抓資料了，下一集讓它記得你買了什麼。」
- **自學者關卡備註**：不用除魅 terminal；重點放「怎麼把需求講清楚讓 Claude 去讀文件」。
- **對應部落格**：/posts/claude-code-finmind-stock-tracking/

### EP2 — 對話式持倉 + 分析（第二大流量）

- **Hook**：手動記持倉很煩、常忘記。
- **核心內容**：
  1. 讓 Claude 自己設計持倉格式（`positions.json`）並寫進 `CLAUDE.md`
  2.「我今天買了 2330，均價 900」→ 對話式記錄
  3.「現在持倉狀況怎樣？」→ 一次列出損益、是否達出場條件
  4. **進階：結合本地股價，叫它做技術面／基本面分析**（吃 `claude 股票分析` 大流量）
  5. 隱私：`positions.json`、`.env.local` 加進 `.gitignore`
- **獨立交付物**：對話式持倉系統 + 用自然語言問分析。
- **連貫鉤子（片頭 recap）**：「上集建好股價系統，這集讓它記得你買了什麼。」
- **連貫鉤子（片尾）**：「它記得你的持倉了，但還是你問它才動——下一集讓它主動幫你找機會。」
- **對應部落格**：/posts/claude-code-finmind-stock-tracking/（持倉段）

### EP3 — 盤前自動選股（意圖升級）

- **Hook**：盤前不知道看哪檔、自己掃太花時間。
- **核心內容**：
  1. 用白話講三個策略：波動率擠壓（彈簧壓緊準備變盤）、超跌反彈、AD 背離
  2. 跟 Claude 說「幫我寫一個盤前掃全市場、挑出今天值得盯的腳本」
  3. 跑出今日觀察清單（`morning_watchlist`），順帶算好每檔盤中觸發條件
  4. **誠實鉤子：策略不能亂喊，怎麼知道準不準？→ 預告 EP4 的回測**
- **獨立交付物**：盤前選股腳本 + 今日觀察清單。
- **連貫鉤子（片頭 recap）**：「前兩集它會抓資料也記得你的持倉，這集讓它主動幫你找機會。」
- **連貫鉤子（片尾）**：「它幫你選好了，但你還得自己盯盤——最後一集讓它自己盯、到點敲你。」
- **誠實揭露**：選股 ≠ 保證賺，這是研究工具。
- **對應部落格**：/posts/claude-code-stock-agent-monitor-alert/（選股段）

### EP4 — 盯盤 + Telegram + crontab（agent 成形，CTA 最重）

- **Hook**：開會沒看盤，手機震一下 → 那則 Telegram 通知（沿用 agent 文開頭那段）。
- **核心內容**：
  1. 四層框架總回顧（收束全系列：Context／能力／溝通／自動化）
  2. 申請 Telegram bot（逐步螢幕錄）
  3. 叫 Claude 寫 `monitor.py`：每 10 分鐘比對條件，全部滿足才發通知，接近的只寫 log
  4. crontab 作息表：盤前選股 / 盤中盯盤 / 收盤補資料
  5. **回測那段放這裡**：全市場驗證、算進成本、參數穩健性、群組驗證；三策略組合回測 ≈ 年化 +34%、最大回撤 9.1%、Sharpe 2.58
  6. **誠實收尾**：不下單、不保證賺錢、回測 ≠ 對帳單
  7. CTA：諮詢／代建服務、訂閱、系列總論
- **獨立交付物**：會自己上工、訊號到就發 Telegram 的完整 agent。
- **連貫鉤子（片頭 recap）**：「前三集它會抓資料、記持倉、會選股，最後一集讓它自己動起來。」
- **自學者關卡備註（本系列最難一集）**：crontab 需要「一台 24 小時開的電腦」這個門檻**照實講**，給替代方案（電腦不關機／雲端）。定位成「想做全自動的人這樣做」。
- **對應部落格**：/posts/claude-code-stock-agent-monitor-alert/

---

## 5. 跨平台交叉引用地圖

```
部落格(finmind) ──嵌入──> EP1, EP2 影片
部落格(agent)   ──嵌入──> EP3, EP4 影片
EP1 ──描述欄連回──> 部落格(finmind)
EP2 ──描述欄連回──> 部落格(finmind)
EP3 ──描述欄連回──> 部落格(agent)
EP4 ──描述欄連回──> 部落格(agent) + 自架 AI Agent 系列
EP1→EP2→EP3→EP4 ──片頭/片尾──> 互相導引（同一隻 agent 長大）
每集 ──切──> 1–2 則 Threads(repurposed) ──導流──> 影片 / 部落格
```

- 影片 `related_post` 指向對應部落格；Threads `source_post` / 影片連結回填。
- 部落格兩篇文章在影片發布後，於文中嵌入對應 YouTube 影片並更新狀態表。

---

## 6. 關鍵字研究

### 資料來源：Google Search Console（sc-domain:homuchen.com，2026-03-23 ~ 2026-06-23）

兩篇來源文章的實際搜尋表現，需求自然分成三層，正好對應系列階梯：

| 需求層 | 代表 query（clicks / 平均排名） | 對應集數 |
|--------|------------------------------|---------|
| **入門 / 抓資料**（量最大、最廣，漏斗頂端） | `claude 股票`(64, #4.6)、`claude 台股`(25, #1.8)、`claude股票`(16)、`finmind`(13)、`台股api`(8+5)、`finmind api 限制`(5)、`googlefinance 日股抓不到`(1, #5.0) | **EP1** |
| **分析 / 持倉**（第二大、意圖明確） | `claude 股票 分析`(37)、`claude 股票分析`(24+9)、`claude code 股票`(26)、`claude 投資`(4)、`claude 投資分析`(3)、`codex 股票分析`(15) | **EP2** |
| **選股 / 自動 agent**（量小、意圖最強、最值錢） | `claude 選股`(7)、`claude code 股票分析`(9)、`ai 股票分析指令`(1)、`claude code 自動交易機器人`、`ai盯盤`、`claude code 投資 自動化`(1) | **EP3 / EP4** |

### 觀察

- **EP1 是最大入口**：`claude 股票` 系列（含各種空格／簡寫變體）累積 clicks 遠高於其他，且排名已在第一頁前段，影片化最可能直接吃到既有需求。
- **第二篇（agent）目前幾乎沒有搜尋流量**（13 個 query、個位數曝光）——太新、太進階，搜尋的人還沒爬到那一級。印證「不能只拍最進階那一級」的判斷：需求是從抓資料一路往上長的。
- **`codex 股票分析`(15 clicks) / `codex 股票`(4)** 出現，顯示有人用 Codex 找同類內容——影片標題仍主打 Claude，但描述／字幕可帶到「同樣思路 Codex 也能做」以擴大觸及。
- **`finmind` 相關 query 群**（`finmind`、`finmind api`、`finmind api 限制`、`finmind 教學`、`finmind 費用`）足以讓 EP1 同時吃下「FinMind 教學」這個獨立搜尋意圖。

### 各集 YouTube 標題關鍵字策略（草案）

| 集 | 標題須含的主關鍵字 |
|----|------------------|
| EP1 | `Claude Code`、`台股 / 股票`、`FinMind`、`抓股價 / 追蹤` |
| EP2 | `Claude`、`股票分析 / 持倉`、`投資` |
| EP3 | `Claude`、`選股`、`盤前` |
| EP4 | `Claude Code`、`台股 AI Agent`、`盯盤 / Telegram / 自動` |

### 待辦（進入腳本撰寫時）

- 每集正式寫腳本前，依 CLAUDE.md 工作流跑一次 `keyword-research` skill，補上 YouTube 平台自身的搜尋量與既有影片表現（GSC 只反映 Google 網頁搜尋，YouTube 搜尋需另查）。
- 發布前對影片說明文字（description）跑 SEO review（標題吃對應 query、描述含主關鍵字、連回部落格）。

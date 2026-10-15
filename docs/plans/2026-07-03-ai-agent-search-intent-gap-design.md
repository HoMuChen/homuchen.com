# AI Agent 系列：搜尋意圖補洞計劃

> 建立日期：2026-07-03
> 資料來源：Google Search Console（sc-domain:homuchen.com，2026-06-02 ～ 2026-07-02，對照期 2026-05-08 ～ 2026-06-04）
> 背景：self-hosted AI agent 系列（2026-06-02 起共 9 篇）發布約一個月後，用 GSC 盤點新出現的搜尋字，找出「有搜尋、但現有文章沒接住或意圖錯位」的缺口，規劃下一批文章。

## 主題概要

- **主題名稱**：AI Agent 系列搜尋意圖補洞（第二波）
- **核心主張**：第一波系列建立了「自架 AI agent」的骨架，第二波針對 GSC 實際觀察到的搜尋意圖補實作細節與進階主題
- **目標受眾**：想自己架 AI agent 的非工程師／半技術背景讀者；已在搜「claude code 股票／自動交易／LINE bot」的人
- **SEO 槓桿**：全站最強 cluster 是「AI/Claude + 股票」（finmind 文為 top 1 頁面），本計劃 6 篇中有 3 篇落在此 cluster

## GSC 關鍵發現（2026-07-03 盤點）

### 系列發布後新出現的搜尋群

1. **Hermes agent + LINE**（合計約 40 曝光，排名 5–7，落在 `/posts/ai-agent-channels-telegram-line/`）
   - `hermes agent 串接 line`（18 曝光）、`hermes agent 連接 line`（11）、`hermes agent line bot`、`hermes line bot`、`openclaw hermes telegram`
   - 意圖：把某個 AI agent 產品接上 LINE 的「實作教學」，現有 channels 文偏概念
2. **自架／個人 AI agent**（落在 `/posts/self-hosted-ai-agent/`，排名 7–10）
   - `自架ai`（6）、`替寫個人ai agent`（5）、`ai agent 電腦`（10 曝光，排名 8.5）、`自建agent`、`自建ai`
   - `ai agent 電腦` 意圖 = 跑 agent 需要什麼電腦／規格，現有文沒直接回答
3. **股票 agent 的進階意圖**
   - `claude code 自動交易機器人`：20 曝光、排名 1.9、CTR 僅 5% → **意圖錯位**（搜尋者要自動下單，文章是監控+通知）
   - `問ai盤後下單 但沒收到通知`：53 曝光、排名 5.7、0 點擊 → 通知失敗 debug 的具體痛點
   - `claude 選股`：+6 點擊、排名 3.6（落在 stock-agent-monitor-alert 文）
   - 其他：`claude 自動交易`（6 曝光）、`claude code 量化交易`、`claude code 炒股`
4. **Codex 比較**（`/posts/claude-code-vs-codex/` 接住，排名 2–9）
   - `claude code codex 比較`、`codex和claude code有什么区别`（簡中）、`codex 費用`、`codex automode`、`codex 全自動`、`codex cowork 比較`
   - 衍生意圖：費用方案、全自動模式
5. **其他新芽**
   - `notion llm`（15 曝光，排名 5.7，wiki 文）、`notion llm wiki`（+3 點擊，排名 3.8）
   - `finmind mcp`（5 曝光）、`台股 mcp`、`mcp skills`
   - `ai agent 工作流 自动化`（簡中，7 曝光，排名 14.7）

### 表現弱的既有系列文（待觀察或後續 refresh）

幾乎零曝光：`crontab-ai-agent-schedule`、`agent-instruction-claude-md`、`ai-agent-memory-file-system`、`openclaw-ai-agent`；`mcp-tools-skills` 僅 1 次曝光。原因可能是太新＋標題關鍵字未對準搜尋用語。**下次盤點（建議 2026-08 初）若仍無起色，考慮改 title/description。**

### 順帶的 CTR 低垂果實（非本系列，另行處理）

- `markdown 語法`：2,173 曝光、排名 4.3、CTR 1.4% → 改 title/description 估 +79 點擊/月，全站最大單一機會

## 關鍵字研究：AI Agent 串接 LINE（2026-07-14）

### 市場觀察與 SERP

以繁體中文搜尋結果觀察，`AI agent 串接 LINE`、`LINE Bot AI Agent 教學`、`LINE Messaging API webhook 教學` 目前的結果主要分成三群：

1. **OpenClaw × LINE 教學**：已有數篇新文章切入，主打把 OpenClaw 接進 LINE，內容包含 LINE Official Account、Messaging API、Webhook 與部署。
2. **n8n / 無程式碼 AI 客服**：搜尋結果不少，但偏向企業客服、視覺化 workflow，與「自架 agent／個人工作流」意圖不同。
3. **傳統 LINE Bot Webhook 教學**：有 Python、Node.js 與 ngrok 教學，能解決 API 基礎問題，但通常沒有接到 Claude Code、Hermes 或自架 AI agent。

競爭程度判斷：

- `LINE Bot 教學`：中～高，結果多且已有完整教學。
- `LINE Messaging API webhook`：中，有官方文件與多篇技術教學。
- `AI agent 串接 LINE`：中，OpenClaw 文章增加中，但「不綁定單一 agent 的自架 LINE adapter」仍有切角。
- `hermes agent 串接 line`：低，主要結果是 Hermes 官方文件，繁體中文實作內容幾乎沒有。

### 競品與權威來源

- [LINE Developers — Build a bot](https://developers.line.biz/en/docs/messaging-api/building-bot/) — 官方建立 Bot、Channel access token 與 Webhook 設定。
- [LINE Developers — Receive messages (webhook)](https://developers.line.biz/en/docs/messaging-api/receiving-messages/) — 官方 Webhook event、簽章驗證與非同步處理說明。
- [LINE Developers — Send messages](https://developers.line.biz/en/docs/messaging-api/sending-messages/) — 官方 reply / push message 差異。
- [OXXO — 建立並串接 Webhook（Python）](https://steam.oxxostudio.tw/category/python/example/line-webhook.html) — 繁中 Python 基礎 Webhook 教學。
- [Hermes Agent — LINE](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/line) — 官方 Hermes LINE adapter、allowlist、Webhook path 與 reply token 行為。
- [OpenClaw LINE 串接教學](https://ohya.co/blog/openclaw-line-integration-guide) — OpenClaw 導向的繁中實作文章。
- [n8n LINE 整合教學](https://kevinmind.com/blog/n8n-line) — 無程式碼／workflow 導向的教學。

### 關鍵字映射

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | `ai agent line`、`AI agent 串接 LINE` |
| 次要關鍵字 | `line bot ai agent`、`LINE Messaging API`、`LINE webhook` |
| 長尾關鍵字 | `hermes agent 串接 line`、`hermes agent line bot`、`openclaw hermes telegram`、`LINE Bot webhook 教學` |
| 搜尋意圖 | Informational + Implementation |
| 買家階段 | Awareness → Implementation |
| 競爭程度 | 主要詞中；Hermes 長尾低 |
| SEO 差異化 | 不假裝第一手 LINE 經驗；用 Telegram 經驗解釋 channel 差異，聚焦原理與架構，並以 Hermes 官方 LINE adapter 作為完整例子。 |

### 寫作與技術注意事項

- 不要把 LINE Notify 當成新方案；LINE Notify 已於 2025-03-31 終止服務，本文統一使用 Messaging API。
- Webhook 必須使用公開 HTTPS；本機測試可用 Cloudflare Tunnel 或 ngrok。
- 必須驗證 `x-line-signature`，不能只依賴 webhook URL 隱藏安全性。
- Webhook 收到事件後要快速回 `200`，慢速 LLM 回覆需考慮 reply token 約 60 秒的一次性限制，必要時改用 Push API。
- Hermes 官方目前已有 LINE bundled adapter，包含 `/line/webhook`、allowlist 與慢回覆處理；文章應以官方文件為準，不自行推測 CLI 行為。

## 產出規劃：6 篇文章（依優先級）

| # | 暫定 slug | 主題 | 承接搜尋意圖 | Cluster | 狀態 | 檔案路徑 | 發布連結 |
|---|-----------|------|--------------|---------|------|----------|----------|
| 1 | `ai-agent-line-bot-tutorial` | AI agent 串接 LINE 手把手教學（Messaging API + webhook） | hermes agent 串接 line 全群 | agent 通路 | 草稿 | `drafts/2026-07-14-ai-agent-line-bot-tutorial.md` | |
| 2 | `claude-code-auto-trading` | Claude Code 能自動下單嗎？從盯盤到交易機器人的距離 | claude code 自動交易機器人、量化交易 | AI+股票 | 未開始 | | |
| 3 | `self-hosted-ai-agent-hardware` | 跑自架 AI agent 要什麼電腦？（舊筆電/Mac mini/VPS/樹莓派＋費用） | ai agent 電腦、自架ai | 自架 agent | 未開始 | | |
| 4 | `ai-agent-notification-debug` | AI agent 通知沒收到怎麼辦？排程與通知 debug 指南 | 問ai盤後下單但沒收到通知 | 自架 agent | 未開始 | | |
| 5 | `claude-code-stock-screening` | 用 Claude Code 選股：條件篩選 agent 實作 | claude 選股 | AI+股票 | 未開始 | | |
| 6 | `finmind-mcp-vs-skill` | FinMind 接 Claude：MCP 還是 script + skill？ | finmind mcp、台股 mcp | AI+股票 | 未開始 | | |

**狀態值**：未開始 / 研究中 / 草稿 / 已撰寫 / 已發布。每完成一步要回來更新此表。

## 各篇規劃

### 1. AI agent 串接 LINE 手把手教學

- **為什麼優先**：唯一一篇「已有排名 5–7 的既有流量在等」的題目，寫完最快見效
- **核心內容**：LINE Developers 申請、Messaging API、webhook 設定、接到自架 agent 的完整流程；troubleshooting 段落
- **關鍵字**：主要 `ai agent line`、`line bot ai agent`；長尾涵蓋 hermes 系（可在文中自然提及「不管你用 OpenClaw、Hermes 還是 Claude Code」）
- **交叉引用**：`/posts/ai-agent-channels-telegram-line/`（概念篇 → 實作篇互連）、`/posts/self-hosted-ai-agent/`
- **個人經驗**：目前未實際串接 LINE；以官方文件、可重現 demo 與 Telegram 實作經驗做對照，避免假裝有第一手踩坑經驗

### 2. Claude Code 能自動下單嗎？從盯盤到交易機器人的距離

- **為什麼優先**：已排名 1.9 但 CTR 只有 5%，意圖錯位最該修；在最強 cluster
- **核心內容**：直接回答「能不能自動下單」；券商 API（如永豐 Shioaji）現況、風險與責任、為什麼我停在「監控＋通知」；BLUF 答案前置
- **關鍵字**：`claude code 自動交易`、`ai 自動下單`、`claude code 量化交易`
- **交叉引用**：`/posts/claude-code-stock-agent-monitor-alert/`、`/posts/claude-code-finmind-stock-tracking/`
- **注意**：股票 agent 用 script+skill 接 FinMind，**沒用 MCP**，別寫錯

### 3. 跑自架 AI agent 要什麼電腦？

- **核心內容**：舊筆電 vs Mac mini vs VPS vs 樹莓派；規格需求（其實很低，因為 LLM 在雲端）、電費/月費比較、24 小時開機注意事項
- **關鍵字**：`ai agent 電腦`、`自架 ai agent 硬體`、`ai agent 主機`
- **交叉引用**：`/posts/self-hosted-ai-agent/`（系列總覽）
- **個人經驗**：詢問穆穆實際用什麼機器跑

### 4. AI agent 通知沒收到怎麼辦？排程與通知 debug 指南

- **核心內容**：crontab 沒觸發、時區問題、agent 跑了但訊息沒送出、API rate limit、log 怎麼看；用「盤後下單通知沒收到」當開場故事
- **關鍵字**：長尾為主（`ai 通知 沒收到`、`crontab 沒執行`）
- **交叉引用**：`/posts/crontab-ai-agent-schedule/`（反向連結救活這篇零曝光文）、`/posts/ai-agent-channels-telegram-line/`

### 5. 用 Claude Code 選股：條件篩選 agent 實作

- **核心內容**：從「盯已持有的股」到「篩還沒買的股」；FinMind 撈全市場資料、篩選條件寫成 skill、定期跑＋通知
- **關鍵字**：`claude 選股`（已排 3.6）、`ai 選股`、`claude code 選股`
- **交叉引用**：`/posts/claude-code-stock-agent-monitor-alert/`、`/posts/claude-code-finmind-stock-tracking/`

### 6. FinMind 接 Claude：MCP 還是 script + skill？

- **核心內容**：兩種接法的差異、為什麼我選 script+skill、什麼情況該用 MCP；順便當作「台股 mcp」搜尋的入口
- **關鍵字**：`finmind mcp`、`台股 mcp`、`claude mcp 股票`
- **交叉引用**：`/posts/mcp-tools-skills/`（救活它）、`/posts/claude-code-finmind-stock-tracking/`、第 2、5 篇

## 發布前 SEO Review（2026-07-14）

### seo-eeat-authority review

- **Experience**：誠實揭露目前只有 Telegram 第一手經驗，LINE 範例尚未在作者 Channel 完成端到端實測；避免虛構踩坑故事。
- **Expertise**：補上 Webhook、簽章驗證、reply token、Push API、allowlist 與 agent 權限控管，並連結 LINE Developers 與 Hermes 官方文件。
- **Authority**：以官方文件作為主要引用來源；目前沒有外部專家引用、原創測試數據或截圖，這是文章的明確缺口。
- **Trust**：補上作者經驗範圍、驗證日期、資料來源與「文件可行 ≠ 已實測」的限制說明；不宣稱 Hermes 或自寫程式碼已由作者上線驗證。
- **決定**：保留文章作為「可重現的技術整理」先行發布前草稿；若要提高 E-E-A-T，後續應實際建立測試 Channel，加入成功回覆與失敗排錯紀錄。

### seo-ai-overviews-advanced review

- **BLUF**：開頭新增「先講結論」，直接回答 AI Agent 串 LINE 的架構與三個主要坑。
- **Query fan-out 覆蓋**：涵蓋建立 Channel、Webhook、HTTPS、signature、Hermes、reply / Push API、Telegram 比較與常見錯誤。
- **Entity proximity**：在同一篇中明確共提 LINE Messaging API、LINE Developers、Hermes Agent、Telegram、Webhook 與自架 AI Agent。
- **Chunk 可引用性**：使用問句 H2、架構圖、步驟清單、FAQ 與資料來源區塊；每個 FAQ 直接回答一個長尾問題。
- **Platform 差異**：官方來源適合 Google / Perplexity 的技術查詢；限制與驗證範圍有助於 Claude 等重視 attribution 的平台。
- **缺口與決定**：尚未加入 HowTo / FAQPage schema（由 Ghost theme / 發布流程決定），也沒有原創測試數據；先不虛構，後續實測後補上截圖、錯誤 log 與測試結果。

## 跨平台聯動

- 每篇發布後評估改寫一則 Threads（`source: repurposed`）導流；Threads 不用「掰掰～👋」結尾、連結放回覆
- 第 1 篇（LINE 教學）和第 3 篇（電腦選擇）適合延伸 YouTube 教學影片，可掛進既有的 youtube 企劃評估

## 工作流程備忘（每篇動工時）

1. 先跑 `keyword-research` skill（SERP 分析＋關鍵字映射）
2. 寫作用 `homuchen-writing-style` skill
3. 發布前跑 `seo-eeat-authority` ＋ `seo-ai-overviews-advanced` 兩個 review
4. 發布後回本文件更新狀態表
5. 下次 GSC 盤點：2026-08 初，順便檢查零曝光系列文是否需要改 title

# AI 助理平台（headquarter.homuchen.com）文章企劃

## 主題概要

- **主題**：AI 顧問用 Claude Code 一天做出自己的 AI 助理平台——LINE、Gmail、會議錄音全部收進資料庫，自動轉全文、抽出待辦／期限／金額，外部 agent 直接讀資料庫
- **核心主張**：一天做出「能用的」，之後兩週把它磨成「好用的」；人負責做決定（MVP 範圍、要不要做、選哪個供應商），程式交給 Claude Code
- **目標受眾**：想用 AI 整理工作訊息的接案者、顧問、小團隊；對 Claude Code 能做多大專案好奇的人
- **來源專案**：`../headquarter.homuchen.com`（私有 repo，沒有開源）

## 內容邊界（使用者 2026-10-22 決定）

- 可以寫「我是 AI 顧問，系統收的是工作和客戶的 LINE、Gmail、會議」，**不出現任何客戶名稱、訊息或檔案內容**
- 截圖只能用 seed／假資料；不露出 `hq.homuchen.com` 網址（避免被試登入）
- 使用數字來自正式機唯讀統計（只取總數），2026-10-22 查
- 動機（使用者選）：期限待辦常漏掉、想讓 agent 讀得到、會議記錄太花時間、多通路的收整（訊息跟檔案）

## 產出規劃

| # | 類型 | 標題（暫定） | 主要關鍵字 | 狀態 | 檔案 | 連結 |
|---|---|---|---|---|---|---|
| 1 | 部落格 | 我用 Claude Code 一天做出自己的 AI 助理：LINE、Gmail、會議錄音全收進來，自動抓出待辦和期限 | AI 助理、Claude Code | 已發布（2026-10-22） | `posts/2026-10-22-claude-code-ai-assistant-one-day.md` | https://homuchen.com/posts/claude-code-ai-assistant-one-day/ |
| 2 | 部落格 | Whisper 中文語音轉文字：用 Cloudflare 免費額度把會議錄音轉成逐字稿 | whisper 中文、逐字稿 ai | 規劃中 | | |
| 3 | Threads | 由 hq 上的 threads-repurpose 排程自動拆（兩篇發布後） | | 未開始 | | |

## 各產出規劃

### #1 一天做出 AI 助理（故事＋設計）

- 開頭：多通路（LINE、信件、附件、會議）散落 → 期限待辦漏掉、會議記錄花時間、想讓 agent 讀得到
- 這個 AI 助理做什麼（BLUF 表格）
- 一天時間軸（git commit 時間＋Claude Code session 紀錄，台灣時間）
- 我做了什麼：做決定（MVP 定位、不做 agent 讀取層、選 Cloudflare Whisper、兩個 session 平行）
- 語音轉文字一節：Cloudflare Whisper 免費額度＋真實會議成本 → 連到 #2
- 上線後的真實數字、值得偷學的設計、上線後兩週的打磨、FAQ

### #2 Whisper 中文（SEO 主力）

- STT 方案比較（Cloudflare Whisper / Groq / OpenAI / Deepgram / 雅婷）——價格發布前逐一對官方頁
- Cloudflare Workers AI 免費額度換算、REST API 呼叫範例（`vad_filter`、`condition_on_previous_text`、`initial_prompt`）
- ffmpeg 切段、OpenCC 簡轉台灣繁體、全形標點、Claude 潤飾保留時間碼
- 限制：不分辨說話者、台語弱
- 真實 40 分鐘會議的成本拆解

## 跨平台交叉引用

- #1 → #2（Whisper 一節，#2 發布後補連結）、自架 AI Agent 系列（記憶、MCP/Skills、LINE 頻道）、淨資產儀表板、Vibe Coding
- #2 → #1（完整系統）、MCP/Skills
- Threads → #1、#2

## 真實數據（2026-10-22，正式機唯讀統計）

- 開發：10/3 13:16 開工（session 紀錄）→ 23:15 記錄第一次正式部署；當天 62 個 commit，約 16,500 行 TypeScript（不含測試）＋ 32 個測試檔約 4,300 行；兩個 session 平行；使用者當天約 74 則訊息
- 到 10/15 共 165 個 commit（全部 Co-Authored-By Claude Opus 5.5）；現在約 27,500 行
- 收集：Email 1,021 封（3 個 Gmail 信箱）、LINE 22 則（1 個官方帳號）、檔案 115 個、會議 1 場
- 信件分類：促銷 439、通知 297、電子報 201、社群 2（共 939，92% 只收不加工）；交易 67、個人 15
- 分析：198 份文件／訊息 → 待辦 67 項、日期 171 個、金額 256 筆
- Job：29,178 成功、1 失敗
- AI 花費：2026-10 共 US$5.20（每月預算 US$20）；analyze $4.37、OCR $0.41、polish $0.22、triage $0.13、Whisper $0.02（牌價，實際在免費額度內）
- 會議：40.6 分鐘 → 5 段 → Whisper 約 1.5 分鐘轉完；Whisper $0.02（牌價）＋ Claude 潤飾 $0.21 ＋ 分析 $0.06 ≈ $0.29；逐字稿 11,096 字
- VM：Linode g6-standard-2（2 vCPU／4GB，東京），US$24／月
- Cloudflare Workers AI（官方 pricing 頁，2026-10-22）：免費方案每天 10,000 neurons、00:00 UTC 重置、超過直接報錯；whisper-large-v3-turbo 每分鐘 46.63 neurons（$0.0005／分鐘）→ 每天約 214 分鐘免費
- Opus vs Sonnet analyze eval（2026-10-10，30 筆）：Opus 期限待辦沒有明顯較好、摘要略好，花費 2.2 倍、每筆慢約 5 秒 → 用 Sonnet

## 關鍵字研究（Ahrefs，台灣，2026-10-22）

| 關鍵字 | 月搜尋量 | KD | 用在 |
|---|---|---|---|
| 語音轉文字 | 19,000 | 3 | #2（工具清單意圖為主，次要） |
| 逐字稿 | 7,200 | 12 | #2 |
| 會議記錄 | 6,100 | 3 | — |
| 會議記錄 ai | 1,900 | 3 | #2 次要 |
| 逐字稿 ai | 1,300 | 0 | #2 次要 |
| whisper 中文 | 800 | 1 | #2 主要 |
| 錄音轉逐字稿 | 500 | 0 | #2 長尾 |
| ai 會議記錄 | 500 | 2 | #2 |
| whisper 語音轉文字 | 400 | — | #2 主要 |
| ai 助理 | 300 | 0 | #1 主要 |
| cloudflare workers ai | 150 | — | #2 |
| line 訊息 備份 | 60 | — | #1 |
| ai 秘書 | 30 | — | #1 |
| claude code 專案 | 10 | — | #1 |

**SERP 觀察**

- `會議記錄 ai`：AI Overview ＋ 工具推薦清單（manus、104 職場力、Plaud、經理人、Notion、數位時代）；沒有人教自己串 Whisper，也沒人寫 Cloudflare 免費額度
- `whisper 中文`：意圖混雜（劍橋詞典「whisper 的中文翻譯」佔前排），技術文是黑暗執行緒（DR 44，#6）、iThome、HackMD；PAA 有「OpenAI Whisper 有中文版嗎」「Whisper 的費用是多少」→ #2 用 FAQ 正面回答

**策略**：#1 的故事關鍵字幾乎沒搜尋量，價值在品牌、E-E-A-T 和 Threads 導流；SEO 流量交給 #2。

## #1 發布前 SEO review（2026-10-22）

**seo-eeat-authority**
- Experience ✅：真實時間軸（git commit＋Claude Code session 紀錄）、自己的原話引用、正式機統計數字、單場會議成本拆解、上線後踩到的問題
- Expertise ✅：「收 → 加工 → agent 讀」分工、讀取順序（摘要 → 結構化 → 全文 → 原檔）、eval 決定模型
- Trust ✅：開頭聲明不出現客戶資料、數字只取總數；Whisper 缺點與上線後的錯誤照實寫；隱私 FAQ（R2、Claude API 不訓練、憑證加密）
- 補強：補上 LINE Messaging API、Anthropic 商業條款、Cloudflare 模型頁三個權威連結
- 刻意不做：**沒有介面截圖**——系統裡是客戶資料，要截圖得另建假資料環境；先不放，之後需要再用 seed 資料補

**seo-ai-overviews-advanced**
- BLUF：「這個 AI 助理在做什麼？」第一句就是答案；「為什麼選 Cloudflare Whisper？」改成第一句先給答案（每天約 3.5 小時免費）
- 問句 H2／H3、表格（時間軸、來源、信件分類、會議成本）利於 chunk 擷取；5 題 FAQ
- Fan-out：AI 助理怎麼做、LINE 個人帳號能不能收、要花多少錢、安全嗎、為什麼不用現成會議記錄工具——都有段落正面回答
- 統計＋引述密度高（ChatGPT 偏好）；entity：Claude Code、Cloudflare Workers AI、Whisper、LINE Messaging API、Gmail、PostgreSQL
- 不做：FAQPage schema（Ghost 沒有逐篇 schema 機制，維持現狀）

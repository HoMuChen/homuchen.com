# 自架 AI Agent 實戰系列 — 設計文件

> 建立日期：2026-06-02
> 結構方案：A+C 混合（觀念主幹線性排列 + 系列總論當 pillar hub）

## 系列概要

- **系列名稱**：自架 AI Agent 實戰
- **核心主張**：你不需要等別人做好的產品 —— 在自己的電腦或工作站上，就能養一隻能自主完成任務、會記憶、能被遙控、會自己定時開工的 AI Agent。
- **目標讀者**：半技術的 builder / power user（會用終端機、敢碰 CLI、想自己組裝 agent 的工程師、技術創業者、進階自學者）。**刻意與既有「Claude Cowork 系列」（非技術 GUI 讀者）區隔。**
- **顧問服務定位（軟導流）**：HoMuChen 提供「**幫你看怎麼設計你的 agent ＋ 直接幫你做（代建）**」的諮詢服務。文章以教學/觀念價值為主，文末自然帶到服務，不硬推、不每篇都塞 CTA 區塊。建立信任優先。
  - **軟 CTA 落點（全系列統一）**：文末「諮詢顧問與代建服務」連到既有服務頁 [`/ai-automation-workflow/`](https://homuchen.com/ai-automation-workflow/)（標題「AI 自動化工作流」），LINE `@673duklg` 保留當「直接敲我」的聯絡點。每篇都套這個慣例。
- **涵蓋的 agent 類型**：跑在個人電腦／工作站、能自主完成多步驟任務的 agent（非雲端 SaaS、非純 chatbot）。

### 與既有內容的關係

| 既有內容 | 關係 |
|---------|------|
| Claude Cowork 打造 AI Agent 系列（12 篇，非技術 GUI） | 平行系列。本系列偏 builder/CLI，互相鏈結但不重疊。Skill 觀念可交叉引用 Cowork #4 而非重寫 |
| `posts/2026-05-05-claude-code-remote-control-conversational-bookkeeping.md` | 本系列 #5（Channels）的招牌案例打底 |
| `posts/2026-05-27-llm-maintained-personal-wiki.md` | 本系列 #3（Memory/檔案）的案例打底 |
| `posts/2026-04-25-claude-code-finmind-stock-tracking.md` | 案例篇落點 |
| `posts/2026-04-15-claude-code-shopify-admin-api-ecommerce-assistant.md` | 案例篇落點 |
| `posts/2026-03-25-claude-code-search-console-seo-analysis.md` | 案例篇落點 |
| `posts/2026-05-13-ai-labor-not-tool-500-commits.md` | 系列總論可引用其「AI 是勞動力不是工具」的觀點 |

---

## 產出規劃

**結構**：觀念篇（pillar + 5）→ 工具篇（依設計理念 3 篇）→ 案例篇（未來補，軟導流落點）。

### 跨平台發布狀態表

| # | 類型 | 暫定標題 | 狀態 | 檔案 / 連結 |
|---|------|---------|------|------------|
| 1 | 部落格(pillar) | 自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工 | 已發布 | [/posts/self-hosted-ai-agent/](https://homuchen.com/posts/self-hosted-ai-agent/) |
| 2 | 部落格 | Agent Instruction：怎麼寫 AI Agent 的「憲法」 | 未撰寫 | — |
| 3 | 部落格 | AI Agent 的記憶與檔案系統：memory、檔案記錄、漸進式揭露 | 未撰寫 | — |
| 4 | 部落格 | MCP / Tools / Skills：AI Agent 的三種能力擴充 | 未撰寫 | — |
| 5 | 部落格 | 用 LINE / Telegram 遙控你的 AI Agent、收任務通知 | 未撰寫 | — |
| 6 | 部落格 | 用 Crontab 讓 AI Agent 自己定時開工 | 未撰寫 | — |
| 7 | 部落格 | Claude Code vs Codex：監督式 vs 全自動的 CLI 泛用 Agent | 未撰寫 | — |
| 8 | 部落格 | OpenClaw：always-on、會 heartbeat、住在通訊軟體裡的 Agent | 未撰寫 | — |
| 9 | 部落格 | Hermes：會自我改進的 Agent — 記憶與自動長技能的設計理念 | 未撰寫 | — |
| 10+ | 部落格 | 案例篇（遠端記帳 / 股票追蹤 / SEO / 電商 / 個人 wiki） | 規劃中 | 引用既有文章 |

> 狀態更新規則：撰寫完 → 改「已撰寫」填路徑；發布 → 改「已發布」填 Ghost URL。新 session 先讀本表了解進度。

---

## 各篇規劃

### 觀念篇

#### #1 系列總論 — 自架 AI Agent 實戰（Pillar / Hub）

- **角色**：topic cluster 中樞，連結全系列每一篇，後續所有文章都 reference 回這篇。
- **核心內容**：
  - 什麼是「跑在你自己電腦上、能自主幹活」的 agent？跟 chatbot、跟雲端 SaaS、跟 Cowork（GUI）差在哪
  - 為什麼是現在（2026 Agent 元年、工具成熟、開源 agent 崛起）
  - 一隻自主 agent 的解剖：**Context（instruction + memory + 檔案）→ 能力（MCP/tools/skills）→ 溝通（channels）→ 自動化（cron）** 四層地圖
  - 全系列導覽（每個觀念連到 spoke 文章）
- **交叉引用**：→ #2~#9 全系列；← `ai-labor-not-tool-500-commits`（AI 是勞動力）；← Cowork 系列總論（GUI 路線對照）
- **需要個人經驗**：你為什麼開始自己跑 agent、你現在電腦上有幾隻在跑
- **軟導流**：文末第一次帶出顧問服務 —— 「想要但不知道從哪開始 / 沒空自己組」

#### #2 Agent Instruction — agent 的「憲法」

- **核心內容**：
  - Instruction 是什麼：agent 的人格、守則、邊界、工作流程
  - 好的 instruction vs 壞的 instruction（具體對比範例）
  - 結構化寫法：角色、能力、限制、輸出格式、範例
  - 實務檔案：`CLAUDE.md` / `AGENTS.md` 之類的專案級指令檔
  - 常見錯誤：指令太模糊、塞太多、沒有範例
- **交叉引用**：→ #3（instruction 與 memory 的分工）、#4（skill 也是一種 instruction）；← #1
- **需要個人經驗**：你寫過最有效 / 踩坑的 instruction
- **差異化**：繁中多談理論，本篇走「我實際在跑的 agent 的指令長怎樣」

#### #3 AI Agent 的記憶與檔案系統 — memory、檔案記錄、漸進式揭露

- **核心內容**：
  - 為什麼 agent 會「失憶」：context window 不是記憶
  - Memory 的層次：工作記憶 vs 長期記憶；什麼該記、什麼不該記
  - 用**檔案系統當記憶**：把知識寫成檔案、agent 自己讀寫
  - **漸進式揭露（progressive disclosure）**：用「索引檔 → 連到細節檔」的 link 結構，避免一次塞爆 context（這是本篇的招牌觀念）
  - 實例：個人 wiki / memory 資料夾的設計
- **交叉引用**：→ #4（skill 也用漸進式揭露）、#9（Hermes 把記憶自動化）；← #1、#2；← `llm-maintained-personal-wiki`
- **需要個人經驗**：你的 memory / 檔案結構怎麼設計的
- **差異化**：避開 context engineering 理論紅海，主打「在個人電腦用資料夾＋連結做記憶」的實作

#### #4 MCP / Tools / Skills — agent 的三種能力擴充

- **核心內容**：
  - 一句話分清楚：**Tools = 單一動作**、**MCP = 連到外部世界的標準管道（協定）**、**Skills = 教 agent「怎麼用」的工作流文件（方法論）**
  - 大廚比喻：MCP 是食材庫與設備、Skill 是食譜與手藝
  - 三者怎麼搭配（MCP 是管道、Skill 是流過管道的水）
  - 何時用哪個：要不要寫 MCP、什麼時候一個 skill 就夠
- **交叉引用**：→ #7~#9（各工具的 MCP/skill 實作）；← #2、#3；← Cowork 系列 #4「Skill 是什麼」（不重寫，導讀者過去看入門）
- **差異化**：繁中已有「MCP vs Skill」討論，本篇加值在「三者在自架 agent 的實際分工 + 取捨判斷」

#### #5 用 LINE / Telegram 遙控你的 AI Agent、收任務通知（Channels）

- **核心內容**：
  - Channel 是什麼：agent 不該只活在終端機，要能在你日常用的軟體裡跟你對話
  - 台灣常用 **LINE**、國際常用 **Telegram**；以及 **Claude Code remote control**（手機遙控自己電腦上的 agent）
  - 兩種模式：你下指令遙控 agent ｜ agent 主動回報通知
  - 實作思路：bot token、webhook、把訊息轉成 agent 指令、把結果推回
  - 案例：遠端對話記帳
- **交叉引用**：→ #6（channel + cron = 主動通知）、#8（OpenClaw 把多 channel 做到極致）；← #1；← `claude-code-remote-control-conversational-bookkeeping`
- **需要個人經驗**：你怎麼遙控自己的 agent、收哪些通知
- **差異化**：🟢 **大缺口** —— 繁中此主題全是 n8n/Make/客服自動回覆，沒人講「遙控自己跑的自主 agent」

#### #6 用 Crontab 讓 AI Agent 自己定時開工

- **核心內容**：
  - Crontab 30 秒入門（5 欄位時間格式、`crontab -e`）
  - 從「定時跑指令」到「**定時觸發一隻 agent 完成任務**」的躍遷
  - 設計模式：排程 → agent 自主執行 → 透過 channel（#5）回報結果
  - 實例：每天早上整理收件匣 / 每週產報表 / 定時抓資料
  - 進階預告：OpenClaw 的 heartbeat 就是這個概念的產品化（接 #8）
  - macOS 注意：`launchd` / 權限；Python 的 APScheduler 替代方案
- **交叉引用**：→ #8（heartbeat）；← #5（回報靠 channel）、#1
- **需要個人經驗**：你排了哪些 agent 定時任務
- **差異化**：🟢 **大缺口** —— 繁中 crontab 教學全是傳統 Linux 排程，沒接 agent

### 工具篇（依設計理念拆，每個工具把某個觀念推到極致）

#### #7 Claude Code vs Codex — 監督式 vs 全自動的 CLI 泛用 Agent

- **為什麼合講**：兩者都是 terminal-native 的泛用 coding/任務 agent，設計哲學成對比。
- **核心內容**：
  - Claude Code：**監督式自主**（plan mode 先審再做、hooks 生命週期攔截）、程式品質強
  - Codex：**非監督式自主**（full-auto 無審核、硬體級 sandbox、雲端執行、token 省）
  - 兩者怎麼實現 #2~#4 的觀念（instruction 檔、MCP、skills/sub-agent）
  - 選型建議：架構/前端/複雜任務用 Claude Code；自動化/DevOps/成本敏感用 Codex；很多人兩個都用
  - GUI 對照：Claude Cowork Desktop（鏈到既有 Cowork 系列，給不想碰 CLI 的人）
- **交叉引用**：→ #8、#9；← #2、#4；← Cowork 系列
- **差異化**：🟢 繁中幾乎無此比較（現有多為日文），先行者優勢

#### #8 OpenClaw — always-on、會 heartbeat、住在通訊軟體裡的 Agent

- **角色**：把 #5（channels）+ #6（cron）推到極致的開源代表。
- **核心內容**：
  - OpenClaw 是什麼：local-first、單人用、always-on 的個人助理 agent（TypeScript/Node）
  - 招牌設計：**多 channel**（WhatsApp/Telegram/Slack/Discord/Signal/iMessage 14+）、語音、Live Canvas
  - **heartbeat = crontab + 檔案的延伸**：agent 定時醒來、看狀態、決定要不要行動（比死板 cron 更聰明）
  - Docker sandbox 隔離、webhook、CLI onboarding
  - 可接 Ollama 本地模型（完全免費 / 資料不出門）
  - 適合誰：想要一隻住在手機通訊軟體裡、隨時待命的個人 agent
- **交叉引用**：← #5、#6；→ #9（與 Hermes 的設計理念對比）
- **差異化**：繁中已有 OpenClaw+Ollama 單篇，本篇加值在「用觀念框架解讀它的設計」

#### #9 Hermes — 會自我改進的 Agent：記憶與自動長技能的設計理念

- **角色**：把 #3（memory）+ #4（skills）推到極致的開源代表。
- **核心內容**：
  - Hermes 是什麼：Nous Research 2026/2 開源、local、自主 agent
  - 招牌設計：**persistent memory**（跨 session 記憶）、**完成複雜任務後自動把流程寫成 skill 文件**下次重用（自我改進）
  - 為什麼這是「memory + skill」觀念的終極形態：agent 自己長記憶、自己長能力
  - 70+ 內建 skill、可接 Ollama / OpenRouter / Claude / Gemini 等多模型
  - 與 OpenClaw 的設計理念對比（always-on 助理 vs 自我改進 worker）
  - 適合誰：想要一隻越用越強、能累積專屬知識的 agent
- **交叉引用**：← #3、#4、#8；→ #1（回扣解剖圖）
- **差異化**：繁中幾乎無 Hermes 深入介紹，搭「自我改進」概念有記憶點

### 案例篇（未來補，軟導流落點）

把上述觀念與工具落到真實案例，並作為顧問服務最自然的導流落點。優先引用既有文章、視情況新增：

- 遠端對話記帳（`claude-code-remote-control-conversational-bookkeeping`）→ 對應 #5
- FinMind 股票追蹤（`claude-code-finmind-stock-tracking`）→ 對應 #6 排程
- Search Console SEO 分析（`claude-code-search-console-seo-analysis`）→ 對應 tools/MCP
- Shopify 電商助理（`claude-code-shopify-admin-api-ecommerce-assistant`）→ 對應 tools
- LLM 維護個人 wiki（`llm-maintained-personal-wiki`）→ 對應 #3 memory

> 案例篇細節待 HoMuChen 補充實際做過的專案。

---

## 跨平台交叉引用地圖

```
#1 (pillar) ←→ 全系列每一篇（hub）
#2 instruction → #3, #4, #7
#3 memory/檔案 → #4, #9 ；← llm-maintained-personal-wiki
#4 MCP/tools/skills → #7, #8, #9 ；←→ Cowork 系列 #4
#5 channels → #6, #8 ；← remote-control-bookkeeping
#6 crontab → #8 ；← #5
#7 Claude/Codex → #8, #9 ；←→ Cowork 系列（GUI 對照）
#8 OpenClaw（channels+cron 極致）→ #9
#9 Hermes（memory+skill 極致）→ 回扣 #1
案例篇 → 對應觀念篇 + 既有文章
```

### 跨平台延伸潛力（選做）

- **Threads**：#5（LINE 遙控 agent）、#9（會自我改進的 agent）話題性高，適合 repurposed 串文導流
- **YouTube / 投影片**：#7 工具比較、#1 總論適合做成口語講解或研討會投影片
- **課程**：本系列可與 `courses/2026-03-22-claude-cowork` 形成「GUI 入門 → CLI 自架進階」的課程梯度

---

## 關鍵字研究

### 研究日期：2026-06-02

### 市場觀察（繁體中文）

**內容缺口地圖：**

| 主題 | 繁中現況 | 機會 |
|------|---------|------|
| Channels：把 LINE/Telegram 接到自己跑的自主 agent 當遙控/通知 | 幾乎都是 n8n/Make/客服自動回覆，沒人講遙控自己電腦上的 agent | 🟢 大缺口 |
| Crontab 觸發 agent 自動跑 | crontab 教學多但全是傳統 Linux 排程，沒接 agent | 🟢 大缺口 |
| Claude Code vs Codex CLI 比較 | 繁中幾乎沒有，現有多為日文 | 🟢 缺口（先行者） |
| 本地/自架自主 agent 系列 | 有單篇（鏈新聞 Ollama、shareuhack、OpenClaw+Ollama），無觀念貫穿的系列 | 🟡 中，系列化勝出 |
| MCP / tools / skills 差異 | ExplainThis、Medium、shareuhack 已有 | 🟡 中（交叉引用 Cowork #4，加值在自架取捨） |
| Context engineering / memory 理論 | 繁中已多優質內容（DataSci Ocean、ihower、李宏毅課程） | 🔴 偏飽和，走實作角度避開 |

**搜尋趨勢：** 2026 被稱「Agent 元年」；開源自主 agent 崛起（Ollama v0.21 整合 Hermes、OpenClaw 多 channel）；本地 LLM + 自主 agent 成為「資料不出門」的訴求點。

**競品分析：**
- [鏈新聞 ABMedia](https://abmedia.io/ollama-complete-guide-2026-local-ai-models-tutorial) — Ollama 本地 AI（單篇）
- [shareuhack](https://www.shareuhack.com/zh-TW/posts/ai-agent-beginner-guide-2026) — AI Agent 入門、MCP vs Skill vs CLI（單篇，偏入門）
- [ohya.co](https://ohya.co/blog/openclaw-ollama-local-llm-guide) — OpenClaw + Ollama 本地（單篇）
- [恆遠數位行銷](https://foreverwebs.com/blog/ai-agent-tutorial-from-chatbot-to-autonomous-2026) — AI Agent 教學（單篇）
- [DataSci Ocean](https://datasciocean.com/ai-concept/context-engineering/)、[小企鵝 Penchan](https://penchan.co/ai/agent/ai-agent-memory-guide/)、[ihower](https://ihower.tw/blog/12817-context-engineering) — context engineering/memory（理論導向，繁中已飽和）
- [ExplainThis](https://www.explainthis.io/zh-hant/ai/agent-skills) — Agent Skills（單篇）
- Claude Code vs Codex 比較 — 現有以日文為主（zenn、qiita、homula），繁中空白

**差異化定位：** 繁中唯一「以核心觀念（context→能力→溝通→自動化）貫穿、面向 builder、含開源工具（OpenClaw/Hermes）設計解讀」的自架 agent 系列；channels 與 crontab 接 agent 是全繁中最明顯的空白。

### 各篇關鍵字策略

> 三角色：**Focus**（要排名的核心）／**Secondary**（相關詞）／**Topical**（撐起主題權威的長尾）

#### #1 系列總論（pillar）
| 類型 | 關鍵字 |
|------|--------|
| Focus | 自架 AI Agent |
| Secondary | 本地 AI Agent, 自主 AI Agent |
| Topical | 在自己電腦跑 AI agent, AI agent 自己完成任務, 個人 AI agent 是什麼 |
| 搜尋意圖 | Informational |
| 買家階段 | Awareness |
| 競爭程度 | 低（系列化無競品） |
| SEO 筆記 | pillar，內鏈全系列；標題打「自架/本地/自主」三組意圖 |

#### #2 Agent Instruction
| 類型 | 關鍵字 |
|------|--------|
| Focus | Agent Instruction |
| Secondary | AI Agent 指令, CLAUDE.md 怎麼寫 |
| Topical | 怎麼寫 AI agent 指令, AGENTS.md, system prompt 寫法 |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Consideration |
| 競爭程度 | 低 |
| SEO 筆記 | CLAUDE.md/AGENTS.md 是新興查詢，提早佔位 |

#### #3 Memory 與檔案系統
| 類型 | 關鍵字 |
|------|--------|
| Focus | AI Agent 記憶 |
| Secondary | AI Agent memory, progressive disclosure |
| Topical | AI agent 漸進式揭露, 用檔案當 AI 記憶, agent 長期記憶實作 |
| 搜尋意圖 | Informational |
| 買家階段 | Consideration |
| 競爭程度 | 中（理論飽和，實作角度差異化） |
| SEO 筆記 | 主打「用資料夾＋連結做記憶」實作，避開 context engineering 理論紅海 |

#### #4 MCP / Tools / Skills
| 類型 | 關鍵字 |
|------|--------|
| Focus | MCP Tools Skills 差別 |
| Secondary | MCP 是什麼, Agent Skills 是什麼 |
| Topical | MCP 跟 skill 差在哪, agent 能力擴充, MCP vs skill |
| 搜尋意圖 | Informational |
| 買家階段 | Consideration |
| 競爭程度 | 中（已有競品，加值在自架取捨） |
| SEO 筆記 | 三者一次講清楚 + 自架 agent 的分工判斷；交叉引用 Cowork #4 分散重複 |

#### #5 Channels（LINE / Telegram 遙控）
| 類型 | 關鍵字 |
|------|--------|
| Focus | LINE 控制 AI Agent |
| Secondary | Telegram bot AI agent, 遠端遙控 AI |
| Topical | 用 LINE 操作 AI, AI agent 通知, 手機遙控電腦 AI agent |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Implementation |
| 競爭程度 | 極低（繁中此角度空白） |
| SEO 筆記 | 🟢 最大缺口之一；強調「遙控自己跑的自主 agent」區別於 n8n/客服機器人 |

#### #6 Crontab 排程
| 類型 | 關鍵字 |
|------|--------|
| Focus | crontab AI agent |
| Secondary | 定時執行 AI agent, AI agent 自動排程 |
| Topical | crontab 觸發 agent, 排程跑 AI 任務, 每天自動跑 AI |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Implementation |
| 競爭程度 | 極低（繁中 crontab 全是傳統排程） |
| SEO 筆記 | 🟢 缺口；切入點是「從定時跑指令 → 定時觸發 agent」 |

#### #7 Claude Code vs Codex
| 類型 | 關鍵字 |
|------|--------|
| Focus | Claude Code vs Codex |
| Secondary | Codex CLI 比較, AI coding agent 比較 |
| Topical | Claude Code Codex 差別, 終端機 AI agent 推薦, Claude Code 是什麼 |
| 搜尋意圖 | Commercial |
| 買家階段 | Consideration |
| 競爭程度 | 低（繁中空白，現有為日文） |
| SEO 筆記 | 🟢 先行者；補 GUI 對照（Cowork）吃不想碰 CLI 的搜尋 |

#### #8 OpenClaw
| 類型 | 關鍵字 |
|------|--------|
| Focus | OpenClaw 是什麼 |
| Secondary | OpenClaw 教學, 開源 AI agent |
| Topical | OpenClaw heartbeat, always-on AI agent, 住在 Telegram 的 AI |
| 搜尋意圖 | Informational |
| 買家階段 | Consideration |
| 競爭程度 | 低（繁中少） |
| SEO 筆記 | 用觀念框架解讀設計（heartbeat=cron+檔案延伸），差異於單純工具介紹 |

#### #9 Hermes
| 類型 | 關鍵字 |
|------|--------|
| Focus | Hermes Agent |
| Secondary | Nous Research Hermes, 自我改進 AI agent |
| Topical | Hermes agent 是什麼, 會記憶的 AI agent, 自動生成 skill |
| 搜尋意圖 | Informational |
| 買家階段 | Consideration |
| 競爭程度 | 極低（繁中幾乎無） |
| SEO 筆記 | 「自我改進/越用越強」記憶點；搭 Ollama 整合時效性 |

### SEO 優先級排序

| 優先級 | # | 理由 |
|--------|---|------|
| 最高 | #5 | LINE/Telegram 遙控自架 agent — 繁中最大缺口、實用、轉換意圖強 |
| 最高 | #6 | crontab 觸發 agent — 繁中缺口、Implementation 階段、易導流 |
| 高 | #1 | pillar，承載 topical authority + 全系列入口 |
| 高 | #7 | Claude Code vs Codex — 繁中空白（現有日文），先行者 |
| 高 | #9 | Hermes — 極低競爭 + 強記憶點 |
| 中 | #2 | Agent Instruction / CLAUDE.md 新興查詢 |
| 中 | #3 | memory 實作角度（避理論紅海） |
| 中 | #8 | OpenClaw 設計解讀 |
| 一般 | #4 | MCP/skills 已有競品，靠交叉引用與取捨加值 |

---

## 撰寫前必做（依 CLAUDE.md）

每篇開寫前：本研究已覆蓋系列層級；單篇可再補該篇 SERP 細節。
撰寫時：用 `homuchen-writing-style` skill。
發布前：跑 `seo-eeat-authority` + `seo-ai-overviews-advanced` 兩個 review，盤點結果寫入 commit message。

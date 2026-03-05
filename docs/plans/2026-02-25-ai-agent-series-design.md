# Claude Cowork 打造 AI Agent 系列 — 設計文件

## 系列概要

- **系列名稱**：Claude Cowork 打造 AI Agent 系列
- **總篇數**：12 篇（含已發布的第 1 篇）
- **結構**：觀念篇 (4篇) → 應用篇 (5篇) → 進階篇 (3篇)
- **目標讀者**：非技術背景但對 AI 有興趣的人（PM、設計師、創業者）
- **工具**：Claude Desktop 的 Cowork 功能（GUI 介面、本地檔案系統操作、Skill 系統）
- **核心主張**：你不需要會寫程式，也能用 Claude Cowork 打造屬於自己的 AI Agent，讓 AI 從「聊天工具」變成「工作夥伴」。

## 發布狀態

| 篇數 | 狀態 | 檔案 |
|------|------|------|
| #1 | 已發布 | `posts/2026-02-25-claude-cowork-ai-from-chat-to-work.md` |
| #2 | 已發布 | `posts/2026-03-01-what-is-ai-agent-vs-chatbot.md` |
| #3 | 已發布 | `posts/2026-03-03-ai-agent-how-it-thinks.md` |
| #4 | 已發布 | `posts/2026-03-05-what-is-ai-agent-skill.md` |
| #5 | 未撰寫 | — |
| #6 | 未撰寫 | — |
| #7 | 未撰寫 | — |
| #8 | 未撰寫 | — |
| #9 | 未撰寫 | — |
| #10 | 未撰寫 | — |
| #11 | 未撰寫 | — |
| #12 | 未撰寫 | — |

## 系列結構

採用「由淺入深」結構（方案 A），觀念篇和實作/進階篇之間雙向交叉引用。

文章類型分兩種：
- **(A) 截圖步驟教學**：純示範，讓非工程師也能跟著做
- **(C) 觀念 + 實作**：前半段概念講解，後半段完整實作

---

## 觀念篇 (4 篇)

讓完全不懂技術的人理解 AI Agent 是什麼、為什麼重要、怎麼運作。

### #1 Claude Cowork — 當 AI 從聊天變成工作（已發布）

- **狀態**：已發布
- **檔案**：`posts/2026-02-25-claude-cowork-ai-from-chat-to-work.md`
- **涵蓋內容**：Cowork 是什麼、跟一般聊天的差別、Skills 概念、基本使用情境
- **角色**：系列入口，後續所有文章都會 reference 回這篇

### #2 AI Agent 到底是什麼？跟 ChatBot 差在哪？

- **類型**：純觀念，無實作
- **核心內容**：
  - 用生活比喻解釋：ChatBot 像問路人（你問一句他答一句）、AI Agent 像助理（你交代任務他自己完成）
  - Agent 的三大特性：自主性、工具使用、目標導向
  - 為什麼 2025-2026 是 AI Agent 爆發的時間點
- **交叉引用**：連回 #1 的 Cowork 介紹作為具體例子

### #3 AI Agent 怎麼「思考」？拆解背後的運作原理

- **類型**：觀念 + 簡單示範截圖
- **核心內容**：
  - 用「你交代助理一件事，他會怎麼做？」來類比 Agent 的工作流程
  - 拆解：理解指令 → 規劃步驟 → 使用工具 → 檢查結果 → 回報
  - 用 Cowork 的實際操作截圖展示這個流程
- **交叉引用**：#2 的 Agent 定義、#1 的 Cowork 功能

### #4 Skill 是什麼？讓 AI Agent 從通才變專家

- **類型**：觀念 + 截圖示範
- **核心內容**：
  - Skill 的概念：像是幫助理準備一份 SOP 手冊
  - 沒有 Skill vs 有 Skill 的對比展示（同一個任務的不同結果）
  - Skill 能做什麼：寫作風格、工作流程、專業知識
  - 預告：後面會教你怎麼自己寫 Skill
- **交叉引用**：#1 提到的 Skills 功能、連結到應用篇的各種 Skill 實例

---

## 應用篇 (5 篇)

每篇圍繞一個具體應用場景，截圖步驟教學為主，讓讀者看完就能跟著做。

### #5 用 AI Agent 自動整理你的檔案

- **類型**：截圖步驟教學 (A)
- **場景**：個人生產力
- **核心內容**：
  - 示範讓 Cowork 整理一個混亂的資料夾（依類型/日期分類、重新命名）
  - 一步步截圖展示：怎麼下指令、Agent 怎麼規劃、執行過程、最終結果
  - 延伸：定期整理的思路
- **交叉引用**：#2 的自主性概念、#3 的運作流程
- **需要個人經驗**：檔案管理的痛點

### #6 用 AI Agent 幫你做研究、整理成報告

- **類型**：截圖步驟教學 (A)
- **場景**：資料分析/研究
- **核心內容**：
  - 示範完整流程：給定主題 → Agent 搜集資料 → 整理重點 → 產出結構化報告
  - 展示 Agent 如何使用搜尋工具、讀取網頁、歸納摘要
  - 跟自己手動 Google 研究的效率對比
- **交叉引用**：#2 的工具使用概念、#3 的規劃步驟
- **需要個人經驗**：實際用 Cowork 做過的研究案例

### #7 用 AI Agent 寫部落格文章（從規劃到成品）

- **類型**：觀念 + 實作 (C)
- **場景**：內容創作
- **核心內容**：
  - 前半段：AI 輔助寫作的觀念 — 不是取代你，是加速你
  - 後半段：實際示範用 Cowork + 寫作風格 Skill 產出一篇文章的完整流程
  - 展示：SEO 研究 → 大綱規劃 → 初稿 → 修改 → 成品
  - 誠實分享：哪些部分 AI 做得好、哪些需要人工調整
- **交叉引用**：#4 的 Skill 概念、既有寫作相關文章
- **需要個人經驗**：用 Cowork 寫文章的真實感受和工作流

### #8 用 AI Agent 打造你的工作流自動化

- **類型**：觀念 + 實作 (C)
- **場景**：工作流自動化
- **核心內容**：
  - 前半段：什麼樣的工作適合自動化？判斷標準（重複性、規則明確、耗時）
  - 後半段：示範一個多步驟工作流，例如批次處理檔案、格式轉換
  - 展示 Agent 如何串接多個步驟自動完成
- **交叉引用**：#3 的「規劃步驟」、#5 的檔案操作
- **需要個人經驗**：日常有哪些重複性工作

### #9 用 AI Agent 管理你的待辦事項和專案筆記

- **類型**：截圖步驟教學 (A)
- **場景**：個人生產力
- **核心內容**：
  - 示範用 Cowork 管理本地的 Markdown 筆記系統
  - 每日/每週回顧、整理筆記、產出摘要
  - 跟傳統的 Notion/Obsidian 工作流比較
- **交叉引用**：#5 的檔案操作、讀書筆記系列、生活系列的時間管理文章
- **需要個人經驗**：筆記/待辦管理方式

---

## 進階篇 (3 篇)

帶讀者從「使用者」進階到「打造者」，學會自己建立 Skill，並提供系列展望。

### #10 手把手教你寫第一個 Skill

- **類型**：觀念 + 完整實作 (C)
- **場景**：自訂 Skill 開發
- **核心內容**：
  - 前半段：Skill 檔案的結構拆解 — 用「寫一份給助理的 SOP」來類比
  - 後半段：從零開始寫一個簡單的 Skill（例如每日晨間整理 Skill）
    - 建立檔案 → 寫內容 → 測試 → 修改 → 完成
    - 每個步驟都有截圖
  - 常見錯誤與除錯方式
- **交叉引用**：#4 的 Skill 觀念、#7 寫文章用到的寫作 Skill 作為參考範例

### #11 進階 Skill 設計 — 讓你的 Agent 更聰明

- **類型**：觀念 + 實作 (C)
- **場景**：自訂 Skill 開發（進階）
- **核心內容**：
  - Skill 設計的原則：什麼是好的 Skill？怎麼寫清楚的指令？
  - 進階技巧：多步驟流程、條件判斷、引用外部工具
  - 實作一個比較複雜的 Skill（例如內容策略規劃 Skill、SEO 審核 Skill）
  - 展示好 Skill vs 普通 Skill 的差異
- **交叉引用**：#10 的基礎、應用篇中各種 Skill 的使用場景
- **需要個人經驗**：開發 Skill 過程中踩過的坑

### #12 AI Agent 的未來，以及你現在就能做的事

- **類型**：純觀念
- **核心內容**：
  - 回顧整個系列：從不懂 Agent 到自己打造 Skill 的旅程
  - AI Agent 的發展趨勢：Multi-Agent、更多工具整合、個人化 Agent
  - 給讀者的行動建議：現在就能開始做的 3 件事
  - 對這個領域的個人想法和期待
- **交叉引用**：串聯全系列所有文章、連回 #1 形成首尾呼應
- **需要個人經驗**：對 AI Agent 未來的個人看法

---

## 交叉引用地圖

```
#1 ←→ #2, #3, #4（觀念篇互相串聯）
#2 → #5, #6, #8（Agent 特性 → 實際應用）
#3 → #5, #6, #8（運作原理 → 看到流程實例）
#4 → #7, #10, #11（Skill 觀念 → Skill 實作）
#5 ←→ #8, #9（檔案操作相關場景互引）
#7 → 既有寫作/SEO 相關文章
#9 → 既有時間管理、讀書筆記系列
#12 → 全系列回顧 + 回扣 #1
```

## 需要個人經驗的文章

撰寫以下文章時需先詢問作者的個人經驗：

| 篇數 | 需要的經驗 |
|------|-----------|
| #5 | 檔案管理痛點 |
| #6 | 用 Cowork 做研究的案例 |
| #7 | 用 Cowork 寫文章的真實感受 |
| #8 | 日常重複性工作 |
| #9 | 筆記/待辦管理方式 |
| #11 | 開發 Skill 踩過的坑 |
| #12 | 對 AI Agent 未來的看法 |

---

## 關鍵字研究

### 研究日期：2026-02-25

### 市場觀察

**繁體中文內容缺口：**
- 繁體中文的 AI Agent 教學內容稀少，多數集中在 Medium 且偏技術導向（GCP ADK、AutoGPT）
- 面向非技術人員的 AI Agent 系列教學幾乎不存在 — 這是明確的內容缺口
- Claude Cowork 教學目前只有少數幾篇（RAR 設計攻略、DarrellTW），且都是單篇介紹，無系列化深入教學
- 中文市場的 AI Agent 文章多為簡體中文，繁體中文的優質內容有先行者優勢

**搜尋趨勢：**
- 2025-2026 被稱為「Agent 元年」，搜尋熱度持續攀升
- Gartner 預測 2026 年底 40% 企業應用將嵌入 AI Agent（2025 年不到 5%）
- Agentic AI 支出 2026 年成長 141% 達 2,019 億美元
- Multi-Agent 採用預計 2027 年前成長 67%
- 全球 AI Agent 市場 2024 年 54 億美元，預計 2030 年達 503 億美元（CAGR 45.8%）

**競品分析：**
- [Aiworks](https://aiworks.tw/blog-ai-agent-2025-trends/) — AI Agent 企業趨勢介紹（單篇）
- [ExplainThis](https://www.explainthis.io/zh-hant/ai/agent-skills) — Agent Skills 觀念介紹（單篇）
- [RAR 設計攻略](https://rar.design/posts/claude-cowork) — Claude Cowork 完整教學（單篇）
- [DarrellTW](https://www.darrelltw.com/claude-cowork-intro/) — Claude Cowork 入門介紹（單篇）
- [電腦王阿達](https://www.koc.com.tw/archives/627037) — Claude Cowork 新聞報導（單篇）
- Medium 上 Simon Liu 的 AI Agent 系列、Kellen 的 GCP ADK 系列 — 偏技術導向

**差異化定位：** 繁體中文市場唯一一個面向非技術人員、以 Claude Cowork 為核心的系列化 AI Agent 教學。

---

### 各篇關鍵字策略

#### #1 Claude Cowork — 當 AI 從聊天變成工作（已發布）

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | Claude Cowork |
| 次要關鍵字 | Claude Cowork 教學, Claude Cowork 是什麼 |
| 長尾關鍵字 | Claude Desktop Cowork 功能介紹, Claude AI 工作夥伴 |
| 搜尋意圖 | Informational（想了解 Cowork 是什麼）|
| 買家階段 | Awareness |
| 競爭程度 | 低（繁中內容少）|

#### #2 AI Agent 到底是什麼？跟 ChatBot 差在哪？

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI Agent 是什麼 |
| 次要關鍵字 | AI Agent vs ChatBot, AI Agent ChatBot 差別 |
| 長尾關鍵字 | AI Agent 跟聊天機器人差在哪, AI 代理人是什麼意思, Agentic AI 是什麼 |
| 搜尋意圖 | Informational（基礎認知）|
| 買家階段 | Awareness |
| 競爭程度 | 中（有英文內容但繁中少）|
| SEO 筆記 | Salesforce、Microsoft、Google Cloud 都有英文版對比文章，繁中幾乎空白。標題含「是什麼」和「差在哪」可同時打兩組搜尋意圖 |

#### #3 AI Agent 怎麼「思考」？拆解背後的運作原理

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI Agent 運作原理 |
| 次要關鍵字 | AI Agent 怎麼運作, AI Agent 工作流程 |
| 長尾關鍵字 | AI Agent 背後原理解釋, AI 代理人如何思考, AI Agent 步驟拆解 |
| 搜尋意圖 | Informational（想深入理解機制）|
| 買家階段 | Awareness → Consideration |
| 競爭程度 | 低（通俗解釋幾乎沒有）|
| SEO 筆記 | 多數現有文章偏技術（LLM、ReAct、Tool Use），用生活化比喻解釋是差異化機會 |

#### #4 Skill 是什麼？讓 AI Agent 從通才變專家

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI Agent Skill |
| 次要關鍵字 | Claude Cowork Skill, AI Agent 客製化 |
| 長尾關鍵字 | AI Agent Skill 是什麼, Claude Skill 教學, AI 助理 SOP, 不用寫程式客製 AI |
| 搜尋意圖 | Informational + Commercial（了解 Skill 並考慮使用）|
| 買家階段 | Consideration |
| 競爭程度 | 低（ExplainThis 有一篇，其餘英文為主）|
| SEO 筆記 | Anthropic 2025 年底開源 Skill 規範，2026 年成為跨平台標準。「Skill」是新興關鍵字，提早佔位 |

#### #5 用 AI Agent 自動整理你的檔案

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI 自動整理檔案 |
| 次要關鍵字 | Claude Cowork 檔案整理, AI 整理資料夾 |
| 長尾關鍵字 | 用 AI 自動分類檔案教學, Claude 整理下載資料夾, AI 檔案管理工具 |
| 搜尋意圖 | Informational + Transactional（想馬上跟著做）|
| 買家階段 | Implementation |
| 競爭程度 | 低（XDA 有一篇英文，繁中無）|
| SEO 筆記 | XDA 的「I let an AI agent organize my entire PC」表現佳，證明此主題有讀者興趣 |

#### #6 用 AI Agent 幫你做研究、整理成報告

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI 研究助手 |
| 次要關鍵字 | AI 整理報告, AI 資料搜集工具 |
| 長尾關鍵字 | 用 AI 做研究教學, Claude Cowork 研究報告, AI 自動搜集資料整理 |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Implementation |
| 競爭程度 | 中（有 Perplexity、NotebookLM 相關文章，但 Cowork 角度獨特）|

#### #7 用 AI Agent 寫部落格文章（從規劃到成品）

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI 寫文章 |
| 次要關鍵字 | AI 寫作工具, AI 寫部落格 |
| 長尾關鍵字 | 用 AI 寫部落格文章教學, AI 輔助寫作流程, Claude AI 寫文章 |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Consideration → Implementation |
| 競爭程度 | 高（AI 寫作工具文章很多，但多為工具推薦列表）|
| SEO 筆記 | 差異化在於展示完整工作流而非工具比較，加上個人真實使用心得 |

#### #8 用 AI Agent 打造你的工作流自動化

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI 工作流自動化 |
| 次要關鍵字 | AI 自動化工具, 不用寫程式 AI 自動化 |
| 長尾關鍵字 | 用 AI Agent 自動化工作流程, no code AI 自動化教學, Claude Cowork 自動化 |
| 搜尋意圖 | Informational + Commercial |
| 買家階段 | Consideration → Implementation |
| 競爭程度 | 中（Zapier、Make 相關文章多，但 Cowork 本地自動化是新角度）|
| SEO 筆記 | 強調「不用寫程式」和「本地端」兩個差異點，區別於 Zapier/Make 的雲端自動化 |

#### #9 用 AI Agent 管理你的待辦事項和專案筆記

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI 筆記管理 |
| 次要關鍵字 | AI 待辦事項, AI 生產力工具 |
| 長尾關鍵字 | 用 AI 管理筆記教學, AI 取代 Notion, Claude Cowork 筆記, AI Markdown 筆記 |
| 搜尋意圖 | Informational + Commercial |
| 買家階段 | Consideration |
| 競爭程度 | 中（Notion AI、Obsidian AI 文章多，但本地 Markdown + Agent 管理是獨特角度）|

#### #10 手把手教你寫第一個 Skill

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | Claude Skill 教學 |
| 次要關鍵字 | 寫 AI Skill, 自訂 AI Agent |
| 長尾關鍵字 | Claude Cowork Skill 怎麼寫, 自己做 AI Agent 教學, AI Skill 入門, prompt engineering 教學 |
| 搜尋意圖 | Transactional（想動手做）|
| 買家階段 | Implementation |
| 競爭程度 | 極低（繁中幾乎無相關教學）|
| SEO 筆記 | 這是整個系列 SEO 價值最高的文章之一，因為搜尋需求在成長但繁中內容接近零 |

#### #11 進階 Skill 設計 — 讓你的 Agent 更聰明

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI Skill 設計 |
| 次要關鍵字 | Context Engineering, AI Agent 進階教學 |
| 長尾關鍵字 | AI Skill 設計原則, 怎麼寫好的 prompt, Claude Skill 進階技巧, context engineering 是什麼 |
| 搜尋意圖 | Informational + Transactional |
| 買家階段 | Implementation（進階）|
| 競爭程度 | 極低 |
| SEO 筆記 | Context Engineering 取代 Prompt Engineering 成為 2026 熱門話題，提早佔位有利 |

#### #12 AI Agent 的未來，以及你現在就能做的事

| 類型 | 關鍵字 |
|------|--------|
| 主要關鍵字 | AI Agent 未來趨勢 |
| 次要關鍵字 | AI Agent 2026, Multi-Agent 趨勢 |
| 長尾關鍵字 | AI Agent 未來發展預測, Agentic AI 趨勢 2026, AI Agent 入門建議 |
| 搜尋意圖 | Informational |
| 買家階段 | Awareness（吸引新讀者）+ Decision（系列讀者的行動呼籲）|
| 競爭程度 | 中（英文趨勢文章多，繁中少）|
| SEO 筆記 | 引用 Gartner、IDC、Salesforce 等權威數據增加可信度，時效性關鍵字需定期更新 |

---

### SEO 優先級排序

依據搜尋潛力、競爭程度、內容獨特性綜合評估：

| 優先級 | 篇數 | 理由 |
|--------|------|------|
| 最高 | #2 | 「AI Agent 是什麼」搜尋量大，繁中內容缺口明顯 |
| 最高 | #10 | 「Claude Skill 教學」幾乎零競爭，需求成長中 |
| 高 | #4 | 「AI Agent Skill」新興關鍵字，先行者優勢 |
| 高 | #5 | 「AI 自動整理檔案」實用性強，繁中無競品 |
| 高 | #11 | 「Context Engineering」2026 熱門話題，提早佔位 |
| 中 | #3 | 通俗解釋運作原理的文章稀缺 |
| 中 | #8 | 「不用寫程式 AI 自動化」長尾流量潛力大 |
| 中 | #12 | 趨勢文章時效性強，可帶入新讀者 |
| 中 | #6 | 有 Perplexity/NotebookLM 競品但角度不同 |
| 一般 | #7 | 「AI 寫文章」競爭激烈，需靠個人故事差異化 |
| 一般 | #9 | Notion AI 相關文章多，需強調本地端優勢 |

# AI 內容 → Threads 發布規劃 — 設計文件

> 建立日期：2026-06-11
> 範圍：把既有 18 篇 AI 分類文章 repurpose 成 Threads，建立可持續的發文節奏與導流機制
> 相關設計文件：[Claude Cowork 系列](2026-02-25-ai-agent-series-design.md)、[自架 AI Agent 實戰系列](2026-06-02-self-hosted-ai-agent-series-design.md)

---

## 主題概要

- **核心主張**：Threads 不是把部落格濃縮貼上，而是用「**結果**」和「**觀點**」當鉤子，把人勾進部落格看完整做法。
- **目標受眾**：對 AI 有興趣的台灣讀者 —— 從「想用 AI 但不知怎麼開始」的一般人，到「想自己組裝 agent」的 builder。
- **HoMuChen 的優勢**：手上有大量「AI 真的替我幹活」的真實成果（盯盤 bot、500 commits、5 隻常駐 agent），這類「秀成果 + 真實數字」的內容在 Threads 互動最高。
- **導流目標**：把 Threads 流量導進全站最強 cluster（股票 + AI，finmind 文為 top 1 頁面）與兩條 AI 系列。

### 發文節奏

- **頻率**：一週 3–4 則（solo 可持續的量）。
- **配比**：每週 **2 則 repurposed（導流）+ 1–2 則 standalone（測風向 / 純互動）**。
- **批次製作**：建議週末一次寫好一週份，平日留時間做即時互動與回覆。

---

## 內容支柱（4 根）

| 支柱 | 佔比 | 取材 | 為什麼有效 |
|------|------|------|-----------|
| **① AI 替我幹活的成果** | 35% | 股票 bot、500 commits、5 隻 agent | 數字 + 真實成果，Threads 最高互動 |
| **② 工程師視角 hot take** | 25% | 取代工程師、Notion 爛掉、AI 是勞動力不是工具 | 觀點/痛點共鳴，逼人留言 |
| **③ 跟著做就有** | 25% | 對話記帳、選股盯盤、部落格自動化 | 實用，導流到教學文 |
| **④ AI Agent 觀念科普** | 15% | vs chatbot、怎麼思考、skill、instruction | 串文格式，建立 topical authority |

---

## 跨平台發布狀態表

> 狀態：規劃中 → 已撰寫（填 `threads/` 路徑）→ 已發布（填 Threads URL）。
> 每發一則就回來更新本表。新 session 先讀本表了解進度。

### 第一批（ROI 最高，優先寫）

| 順位 | 支柱 | 取材文章 | 鉤子（首句草稿） | 格式 | 來源 | 狀態 | 檔案 / URL |
|------|------|---------|-----------------|------|------|------|-----------|
| 1 | ① | `claude-code-stock-agent-monitor-alert` | 我寫了一隻 AI 幫我盯台股，盤中偵測到訊號就自動發 Telegram 叫我 | thread | repurposed | 規劃中 | — |
| 2 | ① | `ai-labor-not-tool-500-commits` | 五月才過七天，我的 commit 數快 500。不是我變快，是 AI 在替我幹活 | single | repurposed | 規劃中 | — |
| 3 | ② | `llm-maintained-personal-wiki` | 你的 Notion 第幾次爛掉了？我這次用 LLM 當管理員，終於活下來 | single | repurposed | 規劃中 | — |
| 4 | ③ | `claude-code-remote-control-conversational-bookkeeping` | 我把用了 5 年的 Google Sheet 記帳收掉了，也沒換 App | thread | repurposed | 規劃中 | — |
| 5 | ② | `software-engineer-in-ai-era` | AI 會不會取代工程師？身為每天用 AI 寫 code 的人，講點實話 | single | standalone | 規劃中 | — |
| 6 | ① | `self-hosted-ai-agent` | 我電腦上固定跑著 5 隻 AI agent：記帳、盯盤、SEO、電商、wiki | thread | repurposed | 規劃中 | — |

### 第二批（觀念科普串文 + 導流）

| 順位 | 支柱 | 取材文章 | 鉤子（首句草稿） | 格式 | 來源 | 狀態 | 檔案 / URL |
|------|------|---------|-----------------|------|------|------|-----------|
| 7 | ③ | `claude-code-finmind-stock-tracking` | 不用寫程式，我用 Claude Code 接 FinMind 建了一套會自己更新的台股追蹤系統 | thread | repurposed | 規劃中 | — |
| 8 | ④ | `what-is-ai-agent-vs-chatbot` | ChatBot 像問路人，AI Agent 像個人助理 —— 差別到底在哪 | thread | repurposed | 規劃中 | — |
| 9 | ④ | `what-is-ai-agent-skill` | 想讓 AI 用你的方式做事？給它一份 SOP（Skill）就好，不用寫程式 | thread | repurposed | 規劃中 | — |
| 10 | ③ | `ai-agent-channels-telegram-line` | AI Agent 不該只活在終端機 —— 我用 Telegram / LINE 遙控它、收通知 | thread | repurposed | 規劃中 | — |
| 11 | ③ | `claude-code-not-just-for-coding-for-blog-writing` | Claude Code 不只能寫 code，這篇 SEO 文就是它自己寫的 | single | repurposed | 規劃中 | — |
| 12 | ④ | `crontab-ai-agent-schedule` | 讓 AI Agent 自己定時開工：從「定時跑指令」到「定時觸發 agent 完成任務」 | thread | repurposed | 規劃中 | — |

### 第三批（補完 + 系列科普）

| 順位 | 支柱 | 取材文章 | 鉤子（首句草稿） | 格式 | 來源 | 狀態 | 檔案 / URL |
|------|------|---------|-----------------|------|------|------|-----------|
| 13 | ④ | `ai-agent-how-it-thinks` | AI Agent 怎麼「思考」？想 → 做 → 看結果，循環到完成 | thread | repurposed | 規劃中 | — |
| 14 | ④ | `agent-instruction-claude-md` | AI Agent 靠不靠譜，九成看你給它的 instruction 寫得好不好 | thread | repurposed | 規劃中 | — |
| 15 | ① | `claude-code-shopify-admin-api-ecommerce-assistant` | 純靠對話，我用 Claude Code 一次搬 50 筆商品上架 Shopify | single | repurposed | 規劃中 | — |
| 16 | ③ | `claude-code-search-console-seo-analysis` | 我把 Google Search Console 接給 Claude Code，叫 AI 幫我做 SEO 分析 | thread | repurposed | 規劃中 | — |
| 17 | ③ | `vibe-coding-build-portfolio-website` | 給 AI 一個資料夾，5 步驟做出可部署的作品集網站 | thread | repurposed | 規劃中 | — |
| 18 | ④ | `claude-cowork-ai-from-chat-to-work` | 大多數人用 AI 還停在聊天問答，Claude Cowork 讓它開始「幫你做事」 | single | repurposed | 規劃中 | — |

---

## 發文格式慣例（寫作時遵循）

### 通則
- **首句定生死**：用 hook 公式 —— 數字（500 commits）、反直覺（不是我變快是 AI 幹活）、痛點（Notion 又爛了）、hot take（AI 取代工程師？）。
- **寫作風格**：用 `homuchen-writing-style` skill —— 口語、`～`、適量 emoji、像朋友聊天。
- **發布工具**：用 `post-to-threads` skill。
- **frontmatter** 照 CLAUDE.md `threads/` 規範：`date`、`type`（single / thread）、`source`（standalone / repurposed）、`source_post`、`tags`、`status: draft`，發布後補 `threads_url`。

### single（單則）
- 用在「成果文 / hot take」。一則打到底（500 字內）。
- **部落格連結放結尾，或第一則回覆**，保護觸及。

### thread（串文）
- 用在「步驟 / 清單 / 觀念拆解」。3–6 則，每則一個重點，用 `---` 分隔。
- 第 1 則只放鉤子 + 預告（不放連結）。
- 最後一則放「完整做法 → 部落格連結」+ 軟 CTA。

### 導流與 CTA
- 慣例導流句：「完整做法寫在部落格（連結）」「想看我怎麼做的，文章連結放留言」。
- 連結放結尾或留言，避免首則就外連影響觸及。
- 自架 agent 系列的成果文可帶軟導流到顧問服務頁 `/ai-automation-workflow/`（不硬推，建立信任優先，沿用系列慣例）。

---

## 為什麼這樣排（決策依據）

1. **股票排第一**：GSC 顯示 `claude 選股`、`claude code 投資自動化`、`codex 股票分析` 都有未被滿足的需求，finmind 文已是全站 top 1。Threads 導流能直接灌進最強 cluster。
2. **500 commits / Notion 爛掉 / 取代工程師**：天生的 Threads 鉤子（數字、痛點、hot take），互動潛力最高，適合早期衝聲量。
3. **觀念科普擺第二、三批**：教育型內容轉換慢但建立權威，當串文長期供稿。
4. **repurposed 為主、standalone 點綴**：先用既有文章打底（省力、可導流），standalone 用來測新主題水溫。

---

## 跨平台交叉引用

- **Threads → 部落格**：每則 repurposed 都連回 `source_post`，導流到對應文章。
- **部落格 → Threads**：高互動的 Threads 主題（如「取代工程師」hot take）若引發討論，可回頭擴寫 / refresh 對應部落格文。
- **與兩條系列接軌**：自架 Agent 系列設計文件已標注 #5（channels）、#9（Hermes）話題性高適合 Threads；本規劃的順位 10、12 即對應。

---

## 撰寫前須知（依 CLAUDE.md）

- 撰寫每則前：可參考既有兩份系列設計文件的關鍵字研究，Threads 主題可再看 Threads / Reddit 既有熱門討論脈絡。
- 撰寫時：一律用 `homuchen-writing-style`。
- 發布時：用 `post-to-threads`，發布後回本表更新狀態與 `threads_url`。

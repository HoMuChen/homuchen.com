---
title: "Claude Code 不只 Code！ Agentic AI 自動撰寫 SEO 文章完整指南"
date: 2025-12-04
author: HoMuChen
category: AI
tags: [Vibe Coding]
image: https://homuchen.com/content/images/2025/12/1000007671.jpg
description: "Claude Code 不只能寫程式！這篇帶你用 Agentic AI、Subagent 與 Slash Command 打造自動化工作流程，從關鍵字研究、風格分析到撰寫，全自動產出高品質 SEO 文章。"
---

你是不是以為 Claude Code 只能用來寫程式？覺得 AI 工具離自己很遠，好像只有工程師才能玩得起？如果你曾經對著一堆 AI 工具發愁，不知道該怎麼開始，或者想要用 AI 幫忙寫文章卻不知從何下手，今天這篇文章將會讓你耳目一新。

這篇文章本身，就是用 Claude Code 撰寫的——從關鍵字研究、風格分析到實際撰寫，全部自動化。讓我們一起來看看，Claude Code 不只是程式開發工具，它的 Agentic 特性和 Slash Command 功能，可以讓你打造各種自動化工作流程，甚至寫出高品質的 SEO 文章！

## Claude Code 是什麼？為什麼它不只是程式開發工具

**Claude Code** 是 Anthropic 推出的 AI 命令列工具 (CLI tool)，它不同於你熟悉的 ChatGPT 或網頁版 Claude——它是一個能夠「主動做事」的 AI 助理。

### 與一般 AI 聊天工具的差異

如果你用過 ChatGPT 或 Claude 網頁版，你會發現它們的運作模式都是「問答式」的：你問一個問題，它回答一個答案。但是 **Claude Code** 不一樣，它可以：

* 直接讀取和修改你電腦上的檔案
* 執行複雜的多步驟任務
* 整合外部工具和服務（透過 MCP）
* 自主判斷下一步該做什麼

換句話說，Claude Code 是一個 **Agentic AI**——它不只是回答問題，而是會「幫你做事」。

### 什麼是 Agentic AI？

**Agentic AI（代理式 AI）** 是 2024-2025 年 AI 領域最熱門的概念之一。簡單來說，Agentic AI 是指：

> 能夠自主規劃、執行多步驟任務，並根據結果調整策略的 AI 系統。

傳統的 AI 是這樣的：

1. 你：「幫我分析這份資料」
2. AI：「好的，分析結果是...」
3. 結束

而 Agentic AI 是這樣的：

1. 你：「幫我分析這份資料並產出報告」
2. AI：「我會先讀取檔案... 發現資料不完整，我再抓取補充資料... 分析完成，現在產生圖表... 報告已經寫好並存檔了」
3. AI 自己完成了所有步驟

這就是為什麼 Claude Code 可以做到「撰寫 SEO 文章」這種複雜任務——因為它會自己規劃每一步該做什麼。我之前在 [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/) 這篇，有更完整地聊過這種「從聊天到做事」的轉變。

## Claude Code 的核心特性：Subagent 系統

Claude Code 最強大的功能之一，就是它的 **Subagent（子代理）** 系統。你可以把它想像成「組織一個專業團隊」，每個成員都有自己的專長。

### 什麼是 Subagent？

Subagent 是 Claude Code 內建的「分工機制」。比如說，在我這個 SEO 文章撰寫系統中，我設計了五個 Subagent：

| Subagent | 職責 | 工具 |
|----------|------|------|
| **content-strategist** | 規劃系列文章策略 | WebSearch |
| **seo-researcher** | 關鍵字研究與分析 | WebSearch |
| **style-analyzer** | 分析寫作風格 | Read, Glob |
| **content-writer** | 撰寫文章內容 | WebSearch |
| **editor** | 校對與 SEO 優化 | Read, Edit |

當我下達指令「撰寫一篇關於 Claude Code 的文章」時，Claude Code 會自動：

1. **seo-researcher** 先進行關鍵字研究
2. **style-analyzer** 讀取過往文章，分析我的寫作風格
3. **content-writer** 根據關鍵字和風格指南撰寫草稿
4. **editor** 最後校對並優化 SEO

這整個流程，我只需要下一個指令就完成了！

![subagent](https://homuchen.com/content/images/2025/12/subagent.jpeg)

### 如何建立自己的 Subagent？

在 Claude Code 中，你只需要在專案資料夾中建立 `.claude/agents/` 目錄，然後定義每個 Agent 的職責即可。比如說，一個簡單的 SEO 研究員 Agent 可能長這樣：

```markdown
# seo-researcher

你是專業的 SEO 關鍵字研究員。

## 職責
- 分析目標關鍵字的搜尋量和競爭程度
- 研究競爭對手的內容策略
- 提供長尾關鍵字建議

## 工具
- WebSearch：搜尋相關資料
- Read：讀取既有的關鍵字資料
```

就這麼簡單！Claude Code 會自動理解這個 Agent 的角色，並在需要時呼叫它。

## Slash Command：打造專屬 AI 助理

除了 Subagent，Claude Code 另一個超好用的功能是 **Slash Command（斜線命令）**。這就像是你的「快捷鍵」，可以把複雜的工作流程濃縮成一個指令。

### 什麼是 Slash Command？

在 Claude Code 中，你可以自訂以 `/` 開頭的指令，比如：

```
/write-blog [主題]          # 撰寫單篇文章
/analyze-style              # 分析寫作風格
/plan-series [主題]         # 規劃系列文章
```

這些指令背後，可能包含了數十個步驟，但你只需要輸入一行指令就能啟動。

![slash command](https://homuchen.com/content/images/2025/12/slash-command.jpeg)

### 實際範例：我的 SEO 文章撰寫系統

在我的專案中，`/write-blog` 這個指令會自動執行以下流程：

1. 檢查是否已經有 `style-guide.md`（風格指南）
2. 如果沒有，先執行風格分析
3. 進行關鍵字研究
4. 根據風格指南和關鍵字撰寫文章
5. 自動校對和 SEO 優化
6. 輸出到 `output/draft.md`

整個過程完全自動化，我只需要給它一個主題，剩下的全部交給 Claude Code 處理。

### 如何建立自己的 Slash Command？

只要在 `.claude/commands/` 資料夾中建立一個 Markdown 檔案，定義指令的行為即可：

```markdown
# write-blog

## 描述
撰寫一篇 SEO 優化的部落格文章

## 步驟
1. 讀取 style-guide.md
2. 呼叫 seo-researcher 進行關鍵字研究
3. 呼叫 content-writer 撰寫草稿
4. 呼叫 editor 校對和優化
5. 輸出到 output/draft.md
```

這樣一來，只要輸入 `/write-blog 我的主題`，Claude Code 就會自動完成所有步驟！

## 實戰案例：SEO 文章撰寫系統完整流程

讓我用這篇文章本身作為案例，展示 Claude Code 如何從零到一完成 SEO 文章撰寫。

### 第一步：風格分析

首先，我把自己過去滿意的 5 篇文章放入 `references/` 資料夾，然後執行：

```
/analyze-style
```

Claude Code 會自動：

* 讀取所有參考文章
* 分析我的寫作風格（語氣、句型、結構）
* 產生一份詳細的 `style-guide.md`

這份風格指南包含了：

* 標題層次規範（H1、H2、H3 的使用方式）
* 常用的開頭和結尾模式
* 語氣定位（口語化程度、專業程度）
* 技術術語處理方式（中英混用規則）
* 段落和句子長度建議

### 第二步：關鍵字研究

接著，seo-researcher 這個 Subagent 會進行關鍵字研究：

* 分析「Claude Code 教學」的搜尋趨勢
* 找出次要關鍵字（Claude Code agentic、Slash Command、Subagent）
* 研究競爭對手的文章標題和內容
* 提供長尾關鍵字建議

最後產生一份 `keywords.md`，裡面包含了主要和次要關鍵字的分佈策略。

> 💡 如果你想更進一步，讓 Claude Code 直接接上你的 Google Search Console 來做數據化的 SEO 分析，我寫過一篇實作：[**Claude Code 接 Google Search Console — 用 AI 幫你做 SEO 分析**](/posts/claude-code-search-console-seo-analysis/)。

### 第三步：撰寫草稿

content-writer 根據風格指南和關鍵字策略，開始撰寫文章：

* 標題包含主要關鍵字「Claude Code 教學」
* 前 100 字自然融入「Claude Code」、「Agentic」、「Slash Command」
* H2 標題包含次要關鍵字
* 保持風格指南中的語氣和結構

### 第四步：校對與優化

editor 負責最後的潤飾：

* 檢查關鍵字密度（控制在 1-2%）
* 確認文章結構符合 SEO 最佳實踐
* 校對錯字和語句流暢度
* 確認有溫暖的結尾語（這是我的風格特徵）

### 整個流程的時間成本

如果手動執行這些步驟，可能需要：

* 風格分析：2-3 小時
* 關鍵字研究：1-2 小時
* 撰寫草稿：3-4 小時
* 校對優化：1 小時

**總計：7-10 小時**

但使用 Claude Code，只需要輸入一個指令，**10-15 分鐘** 就完成了！

## Claude Code 的其他創意應用（不只是 coding）

除了撰寫 SEO 文章，Claude Code 還可以應用在許多非程式開發的場景：

### 1. 文件整理與分析

如果你有一大堆散亂的筆記或文件，Claude Code 可以幫你：

* 自動分類和整理
* 提取關鍵資訊
* 產生摘要和索引

### 2. 資料處理自動化

比如說你有一份 Excel 檔需要清理和分析，Claude Code 可以：

* 讀取資料
* 清理格式
* 進行簡單的統計分析
* 產生視覺化圖表

### 3. 學習筆記生成

如果你在學習新技術或知識，Claude Code 可以：

* 讀取你的筆記和參考資料
* 自動產生結構化的學習筆記
* 製作重點整理和複習卡片

### 4. 專案管理

你可以讓 Claude Code 幫你：

* 追蹤專案進度
* 產生工作報告
* 整理會議紀錄

這些都不是空談，我自己就用 Claude Code 做了好幾個非寫程式的小工具，比如 [**用 Claude Code 建台股追蹤系統**](/posts/claude-code-finmind-stock-tracking/)（AI 幫你接 API、管持倉），還有 [**Claude Code 對話式記帳工作流**](/posts/claude-code-remote-control-conversational-bookkeeping/)（用講的就能記帳）。有興趣的話都可以拿去參考。

關鍵在於，你要善用 **Subagent** 和 **Slash Command** 來打造適合你的工作流程。

## 如何開始使用 Claude Code？

如果你已經躍躍欲試，讓我快速帶你入門。

### 基本安裝步驟

Claude Code 支援 Mac、Windows、Linux，安裝非常簡單：

1. **前往官網**：<https://code.claude.com/>
2. **下載安裝**：選擇你的作業系統版本
3. **登入帳號**：使用你的 Anthropic 帳號登入
4. **開始使用**：在終端機輸入 `claude` 即可啟動

### 費用說明

Claude Code 提供兩種方案：

* **免費版**：每月有一定的使用額度，適合輕度使用
* **Pro 版**：每月 $20 美元，提供更高的使用額度和優先權

如果你只是想試試看撰寫文章或處理簡單任務，免費版就很夠用了。

### 新手入門建議

1. **從小專案開始**：不要一開始就想做複雜的系統，先試著用 Claude Code 處理一些簡單的檔案整理任務
2. **建立 CLAUDE.md**：在你的專案資料夾中建立這個檔案，告訴 Claude Code 你的專案是做什麼的（怎麼把這份「Agent 使用說明書」寫好，可以看 [**Agent Instruction：怎麼寫 AI Agent 的「憲法」**](/posts/agent-instruction-claude-md/)）
3. **逐步加入 Subagent**：不用一次定義很多 Agent，先建立一兩個，慢慢擴充
4. **善用官方文件**：<https://code.claude.com/docs/> 有很詳細的教學

### 實用技巧

* 使用 `CLAUDE.md` 來定義專案規則和工作流程
* 把常用的指令寫成 Slash Command
* 利用 MCP (Model Context Protocol) 整合外部工具，比如 Brave Search 或 Google Sheets

## 總結

今天我們從另一個角度認識了 Claude Code：

* **Agentic AI** 不只是回答問題，而是能自主完成複雜任務
* **Subagent 系統** 讓你可以組織專業的 AI 團隊，分工合作
* **Slash Command** 把複雜的工作流程濃縮成一個指令
* Claude Code 不只能寫程式，還能撰寫 SEO 文章、整理資料、管理專案

最重要的是，這篇文章本身就是最好的證明——從關鍵字研究、風格分析到實際撰寫，全部都是 Claude Code 自動完成的。

如果你一直覺得 AI 工具離自己很遠，或者不知道怎麼開始使用，不妨從今天開始試試看 Claude Code。你會發現，AI 不只是工程師的玩具，它可以成為每個人的得力助手。

希望今天的分享對你有一丁點兒的幫助，讓你看見 AI 自動化的新可能性。如果你有任何想法或問題，都歡迎留言討論唷～掰掰 👋

-----

## 參考資料

* [Claude Code 官方文件](https://code.claude.com/docs/en/overview)
* [Anthropic 官網](https://www.anthropic.com/)
* [Model Context Protocol](https://modelcontextprotocol.io/)

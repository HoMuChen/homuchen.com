# HoMuChen.com — 個人品牌部落格

這是 HoMuChen 的個人品牌部落格專案，用於發布技術教學、讀書筆記、生活分享等文章。

## 專案結構

```
posts/               # 已發布的文章
drafts/              # 草稿與文章規劃（尚未發布）
docs/                # 部署與設定文件
  ghost-deployment.md  # Ghost 部署指南
  routes.yaml          # Ghost URL 路由設定
  redirects.yaml       # Ghost 301 redirect 設定
  plans/               # 系列文章設計文件
```

## Ghost 部署

部署相關的設定與注意事項（routes、redirects、API 發布）詳見 [docs/ghost-deployment.md](docs/ghost-deployment.md)。

## 文章檔案規範

### 命名格式

```
{YYYY-MM-DD}-{slug}.md
```

範例：`2024-07-04-how-much-free-time-to-be-happy.md`

- 日期使用 ISO 格式
- slug 使用英文小寫、以 `-` 分隔
- slug 應簡潔描述文章主題

### Frontmatter 格式

```yaml
---
title: "文章標題（繁體中文）"
date: YYYY-MM-DD
author: HoMuChen
category: 生活 / 讀書筆記 / Web Development / AI
tags: [tag1, tag2]
image: https://storage.googleapis.com/homuchen.com/images/{slug}-0.jpg
description: "選填。文章摘要描述，用於 SEO meta description。"
---
```

- `author` 固定為 `HoMuChen`
- `category` 常見值：`生活`、`讀書筆記`、`Web Development`、`AI`
- `image` 固定格式為 `https://storage.googleapis.com/homuchen.com/images/{slug}-0.jpg`，其中 `{slug}` 替換為文章的 slug（檔名去掉日期前綴）
- `description` 為選填，但建議填寫以利 SEO
- 使用通用 Markdown 格式，不使用 Jekyll 特有語法（如 `{:target="_blank"}`、`{{site.cdn_url}}`、`layout` 等）
- 內部連結格式：`/posts/{slug}/`，**不含日期**。slug 對應檔名去掉日期前綴的部分，例如檔案 `2026-02-25-claude-cowork-ai-from-chat-to-work.md` 的連結是 `/posts/claude-cowork-ai-from-chat-to-work/`

## 寫文章的工作流程

### 1. 關鍵字研究（必要步驟）

**撰寫任何文章或規劃內容之前，必須先使用 `keyword-research` skill 做關鍵字研究。** 這個 skill 定義了完整的研究流程：市場觀察 → 競品分析 → SERP 分析 → 關鍵字映射 → 優先級排序。

- 單篇文章：研究該文章的主要/次要/長尾關鍵字、搜尋意圖、競爭程度
- 系列文章：為每篇文章建立關鍵字表，並做整體優先級排序
- 研究結果存放位置：系列 → `docs/plans/`，單篇 → 草稿規劃筆記

### 2. 使用 homuchen-writing-style skill

**所有文章撰寫必須使用 `homuchen-writing-style` skill。** 這個 skill 定義了 HoMuChen 的寫作風格、語調、文章結構、格式規範與禁止事項。

### 3. 寫作前研究

撰寫任何文章前，必須先做研究：
- 使用 WebSearch 搜尋主題相關資料、最新趨勢、數據
- 詢問使用者是否有相關的個人經驗或故事可以融入文章
- 查看 `posts/` 資料夾中是否有相關文章可以交叉引用
- 技術文章需確認資訊的正確性與時效性

### 4. SEO 最佳化

撰寫文章時應考慮 SEO，根據步驟 1 的關鍵字研究結果來最佳化文章。可使用以下 skills：
- `marketing-skills:seo-audit` — 審核文章的 SEO 品質
- `marketing-skills:ai-seo` — 針對 AI 搜尋引擎（GEO/AEO/LLMO）最佳化
- `marketing-skills:schema-markup` — 結構化資料標記
- `marketing-skills:content-strategy` — 內容策略規劃

SEO 注意事項：
- `title` 包含主要關鍵字（來自關鍵字研究）
- `description` 撰寫吸引人的摘要（150-160 字元），包含主要關鍵字
- 文章內自然使用主要/次要/長尾關鍵字，不要堆疊
- H1/H2 標題包含相關關鍵字
- 內部連結：串聯相關的舊文章（HoMuChen 的招牌習慣）
- 外部連結：引用權威來源

### 5. 文章規劃（系列文章 / 內容日曆）

可以進行整體內容規劃，將規劃好的文章放在 `drafts/` 資料夾下：
- **規劃前先使用 `keyword-research` skill 做關鍵字研究**
- 使用 `marketing-skills:content-strategy` skill 規劃內容策略
- 使用 `marketing-skills:marketing-ideas` skill 發想主題
- 草稿檔案同樣遵循 `{YYYY-MM-DD}-{slug}.md` 命名格式
- 草稿的 frontmatter 中 date 可先填預計發布日期

### 6. 系列文章設計文件（`docs/plans/`）

系列文章的規劃存放在 `docs/plans/` 下，命名格式：`YYYY-MM-DD-<topic>-design.md`。

**設計文件包含：**
- 系列概要（名稱、篇數、結構、目標讀者、核心主張）
- **發布狀態表**（每篇的狀態和檔案路徑）
- 各篇文章規劃（類型、核心內容、交叉引用、需要的個人經驗）
- 交叉引用地圖
- 關鍵字研究（市場觀察、競品分析、各篇關鍵字策略、SEO 優先級）

**狀態更新規則（每次都要做）：**
- 撰寫完一篇文章 → 更新該篇狀態為「已撰寫」，填入檔案路徑
- 發布一篇文章 → 更新該篇狀態為「已發布」
- 開始新 session 處理系列文章時，先讀設計文件了解進度

## 文章分類（Ghost Primary Tags）

Ghost 沒有 category，以 **primary tag**（第一個 tag）作為分類。所有文章歸屬於以下 4 大分類，撰寫新文章時必須從中選擇一個作為 primary tag：

| 分類 | 文章數 | 說明 |
|------|--------|------|
| **Web Development** | 42 | 技術文章：RESTful API、HTTP、Node.js、密碼學、網路概論、系統設計等 |
| **生活** | 35 | 生活分享：遠端工作、房間改造、Google Sheet 工具、心理學、時間管理等 |
| **讀書筆記** | 15 | 讀書心得：原子習慣、為什麼要睡覺、金錢心理學、一週工作四小時等 |
| **AI** | 7 | AI 相關：Vibe Coding、AI Agent、Claude Cowork、Agentic AI 等 |

### 各分類下的主題系列

**Web Development（42 篇）**
- RESTful API / HTTP 系列：從 HTTP 基礎到 API 設計（10+ 篇）
- 密碼學系列：為什麼需要密碼學、Hash Function、Node.js 實作
- 網路概論系列：ISP、分層架構、應用層
- Ghost / 部落格架設系列

**生活（35 篇）**
- 遠端工作系列：優點、缺點、老闆角度、如何談、住宿、簽證、職缺趨勢
- 房間改造系列：地板、牆壁、門、家具、工作區、總覽
- Google Sheet 工具系列：記帳、股票、RSS、Sparkline、下拉選單
- 心理學 / 生活：時間管理法則、峰終定律、柴嘉尼效應、動機

**讀書筆記（15 篇）**
- 原子習慣、為什麼要睡覺、金錢心理學、一週工作四小時等

**AI（7 篇）**
- Claude Cowork 打造 AI Agent 系列
- Vibe Coding 系列：基礎教學、擺脫 AI 味

## 寫作風格重點提醒

- 繁體中文為主，技術名詞保留英文
- 口語化、溫暖、像朋友聊天
- 先講故事再帶概念
- 大量交叉引用自己的文章
- **每篇文章結尾必須有「掰掰～👋」**

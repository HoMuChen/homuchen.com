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
category: 生活 / 讀書筆記 / Web Development
tags: [tag1, tag2]
image: image-name.jpg
description: "選填。文章摘要描述，用於 SEO meta description。"
---
```

- `author` 固定為 `HoMuChen`
- `category` 常見值：`生活`、`讀書筆記`、`Web Development`
- `image` 和 `description` 為選填，但建議填寫以利 SEO
- 使用通用 Markdown 格式，不使用 Jekyll 特有語法（如 `{:target="_blank"}`、`{{site.cdn_url}}`、`layout` 等）

## 寫文章的工作流程

### 1. 使用 homuchen-writing-style skill

**所有文章撰寫必須使用 `homuchen-writing-style` skill。** 這個 skill 定義了 HoMuChen 的寫作風格、語調、文章結構、格式規範與禁止事項。

### 2. 寫作前研究

撰寫任何文章前，必須先做研究：
- 使用 WebSearch 搜尋主題相關資料、最新趨勢、數據
- 詢問使用者是否有相關的個人經驗或故事可以融入文章
- 查看 `posts/` 資料夾中是否有相關文章可以交叉引用
- 技術文章需確認資訊的正確性與時效性

### 3. SEO 最佳化

撰寫文章時應考慮 SEO，可使用以下 skills：
- `marketing-skills:seo-audit` — 審核文章的 SEO 品質
- `marketing-skills:ai-seo` — 針對 AI 搜尋引擎（GEO/AEO/LLMO）最佳化
- `marketing-skills:schema-markup` — 結構化資料標記
- `marketing-skills:content-strategy` — 內容策略規劃

SEO 注意事項：
- `title` 包含主要關鍵字
- `description` 撰寫吸引人的摘要（150-160 字元）
- 文章內自然使用關鍵字，不要堆疊
- H1/H2 標題包含相關關鍵字
- 內部連結：串聯相關的舊文章（HoMuChen 的招牌習慣）
- 外部連結：引用權威來源

### 4. 文章規劃（系列文章 / 內容日曆）

可以進行整體內容規劃，將規劃好的文章放在 `drafts/` 資料夾下：
- 使用 `marketing-skills:content-strategy` skill 規劃內容策略
- 使用 `marketing-skills:marketing-ideas` skill 發想主題
- 草稿檔案同樣遵循 `{YYYY-MM-DD}-{slug}.md` 命名格式
- 草稿的 frontmatter 中 date 可先填預計發布日期

## 既有文章主題分類

以下是目前部落格涵蓋的主題系列，撰寫新文章時應考慮與這些系列的關聯：

- **RESTful API / HTTP 系列**：從 HTTP 基礎到 API 設計（10+ 篇）
- **遠端工作系列**：優點、缺點、老闆角度、如何談、住宿、簽證、職缺趨勢
- **讀書筆記系列**：原子習慣、為什麼要睡覺、金錢心理學、一週工作四小時等
- **房間改造系列**：地板、牆壁、門、家具、工作區、總覽
- **密碼學系列**：為什麼需要密碼學、Hash Function、Node.js 實作
- **Google Sheet 工具系列**：記帳、股票、RSS、Sparkline、下拉選單
- **網路概論系列**：ISP、分層架構、應用層
- **生活/心理學**：時間管理法則、峰終定律、柴嘉尼效應、動機

## 寫作風格重點提醒

- 繁體中文為主，技術名詞保留英文
- 口語化、溫暖、像朋友聊天
- 先講故事再帶概念
- 大量交叉引用自己的文章
- **每篇文章結尾必須有「掰掰～👋」**

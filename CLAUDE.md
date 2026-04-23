# HoMuChen.com — 個人品牌內容工作室

這是 HoMuChen 的個人品牌內容中心，涵蓋以下產出：
1. **部落格文章**（發布到 homuchen.com，Ghost CMS）
2. **Threads 貼文**（獨立主題或從文章 repurpose）
3. **YouTube 腳本**
4. **投影片**（HTML / PPTX / Keynote）
5. **課程**（線上課程規劃與素材）

跨平台內容可在 `docs/plans/` 做聯動企劃（一個主題 → 多平台產出）。

## 專案結構

```
# 內容類型（頂層資料夾）
posts/               # Ghost 已發布文章
drafts/              # Ghost 草稿（尚未發布）
threads/             # Threads 貼文（獨立或 repurposed）
youtube/             # YouTube 腳本（每支影片一資料夾）
slides/              # 投影片（每份投影片一資料夾）
courses/             # 課程企劃與素材（每門課一資料夾）

# 文件與共用
docs/
  ghost-deployment.md    # Ghost 部署指南
  routes.yaml            # Ghost URL 路由設定
  redirects.yaml         # Ghost 301 redirect 設定
  plans/                 # 跨平台系列/主題規劃
_resources/          # 共用素材、參考資料、研究文件
scripts/             # 自動化腳本（發文、發 Threads 等）
```

## Ghost 部署

部落格部署相關的設定與注意事項（routes、redirects、API 發布）詳見 [docs/ghost-deployment.md](docs/ghost-deployment.md)。

## 內容類型規範

### 1. 部落格文章（`posts/`、`drafts/`）

#### 命名格式

```
{YYYY-MM-DD}-{slug}.md
```

範例：`2024-07-04-how-much-free-time-to-be-happy.md`

- 日期使用 ISO 格式
- slug 使用英文小寫、以 `-` 分隔
- slug 應簡潔描述文章主題

#### Frontmatter 格式

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

### 2. Threads 貼文（`threads/`）

Threads 分兩種來源：
- **Standalone**：為 Threads 平台原創的獨立主題
- **Repurposed**：從 `posts/` 既有文章改寫，適合作為文章導流

#### 命名格式

`threads/{YYYY-MM-DD}-{slug}.md`

#### Frontmatter 格式

```yaml
---
date: YYYY-MM-DD
type: single                    # single = 單則貼文；thread = 串文
source: standalone              # standalone = 原創；repurposed = 改寫自部落格
source_post: /posts/{slug}/     # 當 source 為 repurposed 時填寫
tags: [tag1, tag2]
status: draft                   # draft / published
threads_url:                    # 發布後填入
---
```

#### 內容規則

- 單則貼文（`type: single`）：frontmatter 下直接寫貼文內容（500 字以內）
- 串文（`type: thread`）：每則貼文以 `---` 分隔，順序即發布順序
- 發布使用 `post-to-threads` skill

### 3. YouTube 腳本（`youtube/`）

每支影片一個資料夾：

```
youtube/
  {YYYY-MM-DD}-{slug}/
    script.md          # 完整腳本（旁白 + 畫面提示）
    outline.md         # 大綱（選填）
    README.md          # 影片 meta
    assets/            # 素材（選填）
```

#### README.md Frontmatter

```yaml
---
title: "影片標題"
date: YYYY-MM-DD
duration: "10:00"               # 預估長度
status: draft                   # draft / recording / editing / published
youtube_url:                    # 發布後填入
related_post: /posts/{slug}/    # 若與部落格文章相關（選填）
tags: [tag1, tag2]
---
```

### 4. 投影片（`slides/`）

每份投影片一個資料夾：

```
slides/
  {YYYY-MM-DD}-{slug}/
    slides.html        # 主要投影片檔（或 .pptx / .key）
    outline.md         # 大綱 + speaker notes
    README.md          # 投影片 meta
```

HTML 投影片可用 `hyperframes` skill 或 HyperFrames CLI 製作。

#### README.md Frontmatter

```yaml
---
title: "投影片標題"
date: YYYY-MM-DD
format: html                    # html / pptx / keynote
occasion: "場合（研討會、課程、YouTube 講解）"
status: draft                   # draft / published
related_post: /posts/{slug}/    # 選填
related_video: /youtube/{slug}/ # 選填
tags: [tag1, tag2]
---
```

### 5. 課程（`courses/`）

每門課程一個資料夾：

```
courses/
  {YYYY-MM-DD}-{slug}/
    outline.md         # 課程大綱（章節、每章實作 demo）
    plan.md            # 課程規劃（應用場景、定價、文案）
    README.md          # 課程 meta
    assets/            # 素材（投影片、影片檔案、資料）
```

#### README.md Frontmatter

```yaml
---
title: "課程標題"
date: YYYY-MM-DD
duration: "8-10 小時"           # 課程總時數
chapters: "8 章 + Bonus"
status: planning                # planning / recording / published
course_url:                     # 課程上架後填入
tags: [課程, ...]
---
```

## 內容產出工作流程

以下步驟 1–4 適用於所有文字內容（部落格、Threads、YouTube 腳本），步驟 5–6 涵蓋跨平台企劃。

### 1. 關鍵字 / 主題研究（必要步驟）

**開始任何內容產出之前，必須先使用 `keyword-research` skill 做研究。** 流程：市場觀察 → 競品分析 → SERP 分析 → 關鍵字映射 → 優先級排序。

- 單篇文章：研究主要/次要/長尾關鍵字、搜尋意圖、競爭程度
- Threads 貼文：研究主題熱度、目標受眾的討論脈絡（可參考 Reddit、Threads 既有熱門話題）
- YouTube 腳本：研究該主題在 YouTube 的搜尋量與既有影片表現
- 結果存放：跨平台企劃 → `docs/plans/`，單篇 → 草稿內規劃筆記

### 2. 使用 homuchen-writing-style skill

**所有中文文字產出（部落格、Threads、YouTube 旁白）都必須使用 `homuchen-writing-style` skill。** 這個 skill 定義了 HoMuChen 的寫作風格、語調、結構、格式規範與禁止事項。

### 3. 寫作前研究

- 使用 WebSearch 搜尋主題相關資料、最新趨勢、數據
- 詢問使用者是否有相關的個人經驗或故事可以融入
- 查看 `posts/` 是否有相關文章可以交叉引用（部落格招牌）
- 技術內容需確認資訊的正確性與時效性

### 4. SEO 最佳化（部落格文章）

根據步驟 1 的關鍵字研究結果最佳化文章。可使用以下 skills：

**基礎（通用）：**
- `seo-audit` — 審核文章的 SEO 品質（技術 SEO、on-page）
- `ai-seo` — AI 搜尋引擎（GEO/AEO/LLMO）基礎最佳化
- `schema-markup` — 結構化資料標記
- `content-strategy` — 內容策略規劃

**進階（Ahrefs 方法論，專案內建）：**
- `seo-content-lifecycle` — 內容衰退偵測、refresh/prune 決策、topical map 建構、search intent shift、Deep Content for AI era、單篇文章的 focus/secondary/topical 三角色關鍵字架構
- `seo-eeat-authority` — 50+ E-E-A-T markers 檢核、Brand SEO 7 步驟、Entity SEO、Semantic SEO、Share of Search 公式、品牌提及 audit
- `seo-ai-overviews-advanced` — Query fan-out、AI visibility audit、Brand gap analysis、10 招 LLMO、各平台（AI Overviews/ChatGPT/Perplexity/Gemini）差異化最佳化、AI 流量追蹤

SEO 注意事項：
- `title` 包含主要關鍵字（來自關鍵字研究）
- `description` 撰寫吸引人的摘要（150-160 字元），包含主要關鍵字
- 文章內自然使用主要/次要/長尾關鍵字，不要堆疊
- H1/H2 標題包含相關關鍵字
- 內部連結：串聯相關的舊文章（HoMuChen 的招牌習慣）
- 外部連結：引用權威來源

### 5. 內容規劃（系列 / 內容日曆）

可對任何內容類型做整體規劃：
- **規劃前先使用 `keyword-research` skill 做研究**
- 使用 `content-strategy` skill 規劃內容策略
- 使用 `marketing-ideas` skill 發想主題
- 部落格草稿放 `drafts/`，其他平台在各自資料夾用 `status: draft` 標記
- 草稿的 frontmatter 中 date 可先填預計發布日期

### 6. 跨平台系列/主題設計文件（`docs/plans/`）

跨平台系列或主題企劃存放在 `docs/plans/` 下，命名格式：`YYYY-MM-DD-<topic>-design.md`。

一個主題可同時規劃多平台產出（例：1 個部落格系列 + N 則 Threads + 1 支 YouTube + 1 份投影片）。

**設計文件應包含：**
- 主題概要（主題名稱、核心主張、目標受眾）
- 產出規劃（文章清單、Threads 清單、影片清單、投影片清單）
- **跨平台發布狀態表**（每個產出的類型、狀態、檔案路徑、發布連結）
- 各產出規劃（核心內容、交叉引用、需要的個人經驗）
- 跨平台交叉引用地圖（部落格 ↔ Threads ↔ YouTube ↔ 投影片）
- 關鍵字研究（市場觀察、競品分析、各產出的關鍵字策略、SEO 優先級）

**狀態更新規則（每次都要做）：**
- 撰寫完一個產出 → 更新狀態為「已撰寫」，填入檔案路徑
- 發布一個產出 → 更新狀態為「已發布」，填入發布連結（Ghost URL / Threads URL / YouTube URL）
- 開始新 session 處理系列時，先讀設計文件了解進度

### 7. 跨平台內容聯動

撰寫任何內容時，都應思考可否延伸到其他平台：

| 從 | 延伸到 | 常見做法 |
|----|-------|---------|
| 部落格文章 | Threads | 重點精華改寫為 Threads 串文（`source: repurposed`），導流回部落格 |
| 部落格文章 | YouTube | 將文章拆為口語腳本，做成教學影片 |
| Threads 熱門話題 | 部落格文章 | 互動好的 Threads 主題擴寫為深度文章 |
| YouTube 腳本 | 部落格文章 | 影片發布後整理成文字版，方便 SEO |
| 任何內容 | 投影片 | 教學/研討會場合可製作對應投影片 |

跨平台產出的檔案應在 frontmatter 中互相引用（`related_post`、`source_post`、`related_video`）。

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

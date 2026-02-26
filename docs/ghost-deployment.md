# Ghost 部署與設定

## 平台資訊

- Ghost 自架於 GCP
- 網址：https://hammerhub.co
- Ghost Admin：https://hammerhub.co/ghost/

## URL 結構

文章路徑為 `/posts/{slug}/`，透過 `routes.yaml` 設定：

```yaml
collections:
  /:
    permalink: /posts/{slug}/
    template: index
```

- 首頁列表在 `/`，文章在 `/posts/{slug}/`
- Tag/author 頁面不受影響

## Redirects 設定

從舊站（或 Ghost 預設的 `/{slug}/`）遷移過來的文章，需要在 `redirects.yaml` 設定 301 redirect。

### 注意事項

- Ghost 的 redirect 路徑會被當作 **regex** 處理，不是 exact match
- **必須用 `^` 和 `$` 錨定路徑**，否則會造成 redirect loop（例如 `/slug/` 會 substring match 到 `/posts/slug/`，導致無限迴圈 `/posts/posts/posts/...`）
- 301 redirect 會被瀏覽器快取，除錯時要用無痕模式測試

### 正確格式

```yaml
301:
  ^/old-slug/$: /posts/old-slug/
```

### 錯誤格式（會造成 redirect loop）

```yaml
301:
  /old-slug/: /posts/old-slug/
```

## 上傳方式

routes.yaml 和 redirects.yaml 透過 Ghost Admin UI 上傳：

1. 前往 https://hammerhub.co/ghost/#/settings
2. 找到 **Labs**
3. Upload routes YAML
4. Upload redirects YAML

**順序：先上傳 routes.yaml，再上傳 redirects.yaml。**

## 新增文章到 Ghost 後的 Redirect

每次有新文章發布到 Ghost，如果該文章在舊站也有對應的 `/{slug}/` URL，需要：

1. 在 `redirects.yaml` 新增一條 `^/slug/$: /posts/slug/`
2. 重新上傳 `redirects.yaml` 到 Ghost Admin

## 發布文章到 Ghost

使用 `ghost-api` skill 透過 Admin API 發布。詳見 `.claude/skills/ghost-api/SKILL.md`。

### 關鍵注意事項（Ghost v6.0）

- **`source: "html"` 已失效** — Ghost v6.0 不支援，會產生空文章
- **必須使用 Lexical 格式** — 將 HTML 轉換成 Lexical JSON，透過 `lexical` 欄位傳送
- 轉換流程：Markdown → 預處理 → HTML → Lexical JSON → Ghost API

### Markdown → Lexical 轉換流程

1. **預處理 Markdown**：在 list 項目前補空行（Python `markdown` 模組需要）
2. **Markdown → HTML**：使用 Python `markdown` 模組（extensions: `tables`, `fenced_code`）
3. **HTML → Lexical JSON**：逐一將 HTML 元素轉換成 Lexical 節點
   - `<p>` → `paragraph`
   - `<h1>`–`<h6>` → `extended-heading`
   - `<ul>/<ol>` → `list` + `listitem`
   - `<blockquote>` → `extended-quote`
   - `<img>` → `image`（從 `<p>` 中提升為頂層節點）
   - `<table>` → `html` card（原始 HTML 直接傳入）
   - `<strong>` → format `1`（bold）, `<em>` → format `2`（italic）, `<code>` → format `16`
   - 外部連結自動加 `target="_blank" rel="noopener noreferrer"`
   - 內部連結（`/posts/...`）不加

### 已完成的 Jekyll 清理

以下 Jekyll 語法已從 `posts/` 中全部移除：
- `{:target="_blank"}` 及所有變體（`{:target="..." name="..."}`、`{:loading="lazy"}`）
- `layout: post` frontmatter
- `{{site.cdn_url}}` → 已替換為 `https://storage.googleapis.com/homuchen.com/images`

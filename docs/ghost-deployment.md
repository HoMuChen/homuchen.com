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

使用 `ghost-api` skill 透過 Admin API 發布。關鍵注意事項：

- 傳 `html` 內容時必須加 `"source": "html"`，否則內容會是空的
- 詳見 `.claude/skills/ghost-api/skill.md`

## Markdown → HTML 轉換規則

Markdown 檔案使用標準 Markdown 語法，不含 Jekyll 特有語法。在轉換成 HTML 發布到 Ghost 時，需要做以下處理：

### 外部連結自動加 `target="_blank"`

- **外部連結**（`http://` 或 `https://` 開頭）→ 加上 `target="_blank" rel="noopener noreferrer"`
- **內部連結**（`/posts/...` 開頭）→ 不加，在同一視窗開啟

範例：
```
Markdown: [Google](https://google.com)
HTML:     <a href="https://google.com" target="_blank" rel="noopener noreferrer">Google</a>

Markdown: [上一篇](/posts/my-post/)
HTML:     <a href="/posts/my-post/">上一篇</a>
```

### 清理 Jekyll 殘留語法

舊文章可能還有 Jekyll 語法，轉換時需清除：
- `{:target="_blank"}` → 移除（由上述外部連結規則自動處理）
- `{{site.cdn_url}}` → 替換為實際的 CDN URL
- `layout: post` → 從 frontmatter 移除

---
name: gsc
description: Query Google Search Console data for homuchen.com (read-only, via service account) — per-post clicks, which search queries bring traffic to a post, trends over time, period-over-period changes, sitemaps. Use when picking posts to repurpose (e.g. for Threads), checking how a post performs in search, finding keyword angles for a post, or whenever Search Console data is needed and the google-search-console MCP is unavailable (e.g. on the hq VM / headless runs).
---

# Google Search Console（homuchen.com）

唯讀查詢 `sc-domain:homuchen.com` 的 Search Console 資料。腳本：`.agents/skills/gsc/scripts/gsc.py`（從 repo 根目錄執行）。

## 前置

- service account 金鑰：`~/.config/gsc-service-account.json`（或用 `GSC_SERVICE_ACCOUNT_FILE` 指定）
  - 帳號 `threads-gsc@homuchen.iam.gserviceaccount.com`，GCP 專案 `homuchen`，在 Search Console 是**受限**使用者（只能讀）
  - 目前只放在 hq VM 的 `threads` 帳號。Mac 上通常改用 `google-search-console` MCP。
- Python 套件：`requests`、`PyJWT`、`cryptography`（repo 其他腳本本來就用到）
- 資料約延遲 2–3 天，預設區間結束日為「今天 −3 天」

## 子命令

| 用途 | 指令 |
|------|------|
| 每篇文章的點擊排行（合併 `?ref=` 等 URL 變體） | `gsc.py top-posts [--not-repurposed] [--limit 10]` |
| 某篇文章是哪些搜尋字帶來流量 | `gsc.py query --dimensions query --filter "page contains /posts/<slug>/"` |
| 某主題的趨勢 | `gsc.py query --dimensions date --days 90 --filter "query includingRegex claude"` |
| 跟前一期比，哪些字成長/衰退 | `gsc.py query --dimensions query --compare --sort clicks` |
| 排名 5–15 名的機會字 | `gsc.py query --dimensions query,page --min-impressions 50 --sort impressions`（再看 position） |
| 裝置 / 國家分布 | `gsc.py query --dimensions device` / `--dimensions country` |
| sitemap 狀態 | `gsc.py sitemaps` |

共用參數：`--days N`（預設 28）或 `--start/--end YYYY-MM-DD`、`--limit`、`--format table|json|csv`、`--type web|image|discover|...`。

`--filter` 格式為 `'<dimension> <operator> <expression>'`，可重複（多個條件為 AND）：
- dimension：`query`、`page`、`date`、`country`、`device`、`searchAppearance`
- operator：`equals`、`notEquals`、`contains`、`notContains`、`includingRegex`、`excludingRegex`（RE2 語法）
- country 用 ISO 3166-1 alpha-3 小寫（如 `twn`），device 用 `DESKTOP` / `MOBILE` / `TABLET`

## 用法提示

- `top-posts` 的 `repurposed` 欄位來自 `threads/*.md` 的 `source_post`，所以要在 repo 最新狀態下跑（先 `git pull`）。
- 點擊高 ≠ 適合 Threads：挑 repurpose 題目時，先看 `top-posts`，再用 `query --filter "page contains ..."` 看讀者是用什麼字找到的，判斷受眾是否和 Threads（AI、Claude Code、理財工具）重疊。
- 權限是受限使用者：提交 sitemap、移除網址等寫入操作不行（刻意如此）。
- 403 代表 service account 沒被加進 Search Console；找不到金鑰會直接提示路徑。

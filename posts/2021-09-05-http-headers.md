---
title: "HTTP Headers 完全指南：常用 headers + Security / CORS / Cookie / Cache（2026 更新版）"
date: 2021-09-05 22:30:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api, security, cors]
description: "HTTP Headers 完整指南：從基礎的 Content-Type、Cache-Control，到現代 Web 必備的 Security headers（CSP、HSTS）、CORS headers、Cookie 屬性（SameSite、HttpOnly）。2026 大幅更新，補上 5 個新手常踩的坑。"
---

> **2026-05 更新**：原本這篇只列了 General / Content / Cache / Connection 四類 headers，但寫 API 跟做網站這幾年遇到的 9 成問題其實都在 **Security、CORS、Cookie** 這三塊（沒設 CSP 被 XSS、Cookie 沒設 SameSite 被 CSRF、跨域請求一直 fail）。這次把這些補齊，最後加上 5 個常見地雷。

在 HTTP 協議中，headers 對於每個 request、response 提供額外的資訊，本質就是一對 `key: value`，由冒號隔開。

這篇會看：

* HTTP message 結構，header 在哪裡
* 8 大類常用 headers：General / Content / Cache / Connection / **Security** / **CORS** / **Cookie & Auth** / **Compression**
* 一張**「該設什麼 header」決策表**
* **5 個新手常踩的地雷**

如果對 HTTP message 格式還不熟，建議先看：[**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)

---

## 一句話結論：你該設什麼 header？

| 你在做的事 | 必須設的 headers |
|----------|----------------|
| 回 JSON API | `Content-Type: application/json` |
| 做靜態網站 | `Cache-Control` + `ETag` |
| 開 HTTPS 網站 | `Strict-Transport-Security`（HSTS） |
| 防 XSS | `Content-Security-Policy`（CSP）+ `X-Content-Type-Options: nosniff` |
| 防 CSRF | Cookie 加 `SameSite=Lax` 或 `Strict` |
| 跨域 API | `Access-Control-Allow-Origin` + `Access-Control-Allow-Methods` |
| 登入 cookie | `Set-Cookie: ...; Secure; HttpOnly; SameSite=Lax` |
| 開壓縮 | `Content-Encoding: gzip / br / zstd` |

---

## HTTP messages 結構

HTTP 是 text-based 的傳輸協議。**Request message** 長這樣：

```
<method> <URL> <version>
<header>
<header>
...

<body>
```

**Response message**：

```
<version> <status code> <status message>
<header>
<header>
...

<body>
```

中間整段就是 headers。每行一對 `Key: Value`，慣例是每個單字首字母大寫、用 `-` 隔開：

```
Connection: Keep-Alive
Content-Length: 10000
Content-Type: text/html
Date: Thu, 02 Sep 2021 02:52:46 GMT
```

> 補充：HTTP/2 之後 headers 改成小寫，且支援 binary 傳輸（HPACK 壓縮）。但你寫程式設 header 時通常還是用大寫慣例，library 會自動處理。

---

## 1. General Headers

幾乎每個 request / response 都會出現的基礎 header。

* **Date** — 訊息建立時間。Server 一定會帶，client 通常不需要設。
* **Host** — Request 要送到哪台 server。為什麼需要？因為一台 server 可能託管多個網站（virtual hosting），同一個 IP 後面可能有 100 個 domain，server 要靠 Host header 知道你要哪個。HTTP/2 之後改成 `:authority` pseudo-header，但邏輯一樣。
* **User-Agent** — 發出 request 的 client 是誰（Chrome、Firefox、curl、Googlebot、ChatGPT-User…）。**注意：絕對不要相信這個 header 做安全判斷**，誰都能偽造。

---

## 2. Content Negotiation（內容協商）

Client 告訴 server「我能接受什麼格式」，server 從中挑一個回。

* **Accept** — 想要的 media type。例：`Accept: application/json, text/html;q=0.9`（`q` 是優先順序）。
* **Accept-Language** — 想要的語言。例：`Accept-Language: zh-TW,zh;q=0.9,en;q=0.8`。
* **Accept-Encoding** — 能解碼的壓縮格式。**現代瀏覽器幾乎都會送** `Accept-Encoding: gzip, deflate, br, zstd`，server 看到就應該回壓縮版本。

---

## 3. Payload Content

跟 body 內容相關的 metadata。

* **Content-Type** — body 是什麼格式。沒設的話，收到端會用猜的（很容易猜錯）。
  * HTML：`text/html`
  * CSV：`text/csv`
  * JSON：`application/json`
  * 圖片：`image/jpeg`、`image/png`、`image/webp`、`image/avif`
  * Form data：`application/x-www-form-urlencoded` 或 `multipart/form-data`
  * 完整列表：[MIME types](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
* **Content-Length** — body 有幾個 bytes。Streaming 時會被 `Transfer-Encoding: chunked` 取代。
* **Content-Encoding** — body 用什麼壓縮。常見：`gzip`、`br`（Brotli）、`zstd`（Zstandard，2024 起 Chrome/Firefox 支援，壓縮率最好）。
* **Content-Disposition** — 提示瀏覽器要 inline 顯示還是下載。例：`Content-Disposition: attachment; filename="report.pdf"` 會觸發下載。

---

## 4. Caching Headers

Browser 跟 CDN 靠這些 headers 決定要不要重新下載資源。**做網站效能時，這幾個是 80% 的關鍵**。

### Cache-Control（最重要的快取 header）

統一控制快取行為，覆蓋舊的 `Expires` / `Pragma`：

```
Cache-Control: public, max-age=31536000, immutable
```

常見指令：

| 指令 | 用法 |
|------|------|
| `public` | 任何 cache（CDN、browser）都可存 |
| `private` | 只給 end-user browser cache，不給 CDN（用於登入後個人化內容） |
| `no-store` | 完全不要 cache（敏感資料） |
| `no-cache` | 可以存，但每次用前要先跟 server 驗證 |
| `max-age=N` | 緩存 N 秒 |
| `immutable` | 告訴 browser 內容絕對不會變，省下 revalidate 的 request |
| `stale-while-revalidate=N` | 過期後 N 秒內仍可用舊內容，背景去更新 |

**典型用法**：
* 帶 hash 的靜態資源（`app.a3f8b2.js`）→ `Cache-Control: public, max-age=31536000, immutable`
* HTML → `Cache-Control: no-cache`（讓 browser 每次驗證）
* API JSON → `Cache-Control: private, max-age=60`

### ETag / If-None-Match（內容指紋驗證）

* **ETag** — Server 對 response body 算的指紋（hash），放在 response。
* **If-None-Match** — Client 下次 request 把上次拿到的 ETag 帶回去，server 比對如果一樣，回 `304 Not Modified`（沒 body，省頻寬）。

```
# 第一次
GET /api/users → 200 OK
ETag: "abc123"
{ ... }

# 第二次
GET /api/users
If-None-Match: "abc123"
→ 304 Not Modified（body 為空）
```

### If-Match（避免 lost update）

PUT 操作的 race condition 防護。比如多人同時編輯一份 wiki：

```
PUT /wiki/page-1
If-Match: "abc123"

→ 如果現在的 ETag 還是 abc123 → 200 OK 更新成功
→ 如果已經被別人改過 → 412 Precondition Failed
```

### Last-Modified / If-Modified-Since

ETag 的時間版本（精度較低）。Server 回 `Last-Modified: Sun, 05 Sep 2021 01:40:14 GMT`，client 下次帶 `If-Modified-Since: 同一時間`，沒改就 304。

> 同時有 ETag 跟 Last-Modified 時，**ETag 優先**。

---

## 5. Connection Management

* **Connection** — 控制連線行為。HTTP/1.1 預設就是 `keep-alive`，可以重用 TCP 連線跑多個 request，省下 handshake 的 RTT。要關就送 `Connection: close`。HTTP/2 之後這個 header 被廢掉了（所有 stream 都共用一個連線）。
* **Keep-Alive** — 配合上面用，可以指定 `timeout`、`max` 等參數。

---

## 6. Security Headers（現代必備）

**幾乎所有正式網站都該設這些**。沒設的話，瀏覽器會用最寬鬆的預設值，等於把門打開。

### Strict-Transport-Security（HSTS）

強制 browser 之後一律走 HTTPS，連 HTTP 都不要試。

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

* `max-age` — 強制 HTTPS 的秒數（建議至少 1 年 = 31536000）
* `includeSubDomains` — 包含子網域
* `preload` — 申請進入 [HSTS preload list](https://hstspreload.org/)，連第一次都直接走 HTTPS

### Content-Security-Policy（CSP）

防 XSS 的最後一道防線。控制哪些來源的 script、style、image 可以被載入：

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline'
```

寫 CSP 是個專業工程（容易把自己鎖在門外），建議從 `Content-Security-Policy-Report-Only` 開始 → 收 violation report → 確認沒誤殺再切到正式 CSP。

### X-Content-Type-Options

```
X-Content-Type-Options: nosniff
```

阻止 browser 用「猜」的方式解讀 content type。沒設的話，攻擊者可能上傳偽裝成圖片的 JS 檔讓 browser 執行。**這個沒理由不設，永遠加上就對了。**

### X-Frame-Options / Content-Security-Policy: frame-ancestors

防 Clickjacking（你的頁面被嵌進別人的 iframe 騙人點擊）：

```
X-Frame-Options: DENY            # 完全不能被 iframe
X-Frame-Options: SAMEORIGIN      # 只有同網域可以
```

新版用 CSP 的 `frame-ancestors` directive 取代，但目前兩個都設沒壞處。

### Referrer-Policy

控制使用者點連結離開時，要不要把當前 URL 寫進 Referer header（注意：原版拼錯成 `Referer`，將錯就錯）。

```
Referrer-Policy: strict-origin-when-cross-origin   # 推薦預設
```

### Permissions-Policy

控制網站能用哪些 browser API（鏡頭、麥克風、地理位置等）：

```
Permissions-Policy: camera=(), microphone=(), geolocation=(self)
```

`()` 是禁用，`(self)` 是只允許自己網域，`(self "https://embed.com")` 是允許特定 origin。

---

## 7. CORS Headers（跨域請求）

當你的 frontend（`a.com`）要打 backend API（`b.com`）時，browser 會擋下來，除非 server 明確說「我允許你」。

### Server 要回的 CORS headers

* **Access-Control-Allow-Origin** — 允許的來源 origin。`*` 是允許所有（**但有 cookie 時不能用 `*`**）。
* **Access-Control-Allow-Methods** — 允許的 HTTP methods。例：`GET, POST, PUT, DELETE`。
* **Access-Control-Allow-Headers** — 允許 client 帶的 custom headers。
* **Access-Control-Allow-Credentials: true** — 允許帶 cookie。
* **Access-Control-Max-Age** — Preflight 結果可以 cache 多少秒。

### Preflight（OPTIONS request）

對 non-simple request（帶 custom header、用 PUT/DELETE 等），browser 會先發一個 `OPTIONS` 詢問，server 回 CORS headers 確認允許後，才會送真正的 request。

> CORS 是 **browser 強制執行**的安全機制。curl、Postman 不會檢查。所以「為什麼我用 Postman 可以，瀏覽器就不行」的標準答案就是 CORS。

### Sec-Fetch-* 系列

新一代的請求 metadata，比 Origin/Referer 更精確，**browser 自動加，不能偽造**：

* `Sec-Fetch-Site: same-origin / cross-site / none`
* `Sec-Fetch-Mode: cors / navigate / no-cors`
* `Sec-Fetch-Dest: document / script / image / style`
* `Sec-Fetch-User: ?1` — 是否使用者主動觸發

server 端拿來做更細的存取控制（例：拒絕跨站的 `Sec-Fetch-Site: cross-site` POST 來防 CSRF）。

---

## 8. Cookie & Auth Headers

### Set-Cookie（server 設給 client）

```
Set-Cookie: session=abc123; Max-Age=86400; Path=/; Secure; HttpOnly; SameSite=Lax
```

關鍵屬性：

| 屬性 | 用途 |
|------|------|
| `Secure` | 只透過 HTTPS 傳，HTTP 不傳 |
| `HttpOnly` | JavaScript 讀不到（防 XSS 偷 cookie） |
| `SameSite=Strict` | 完全只有同站 request 會帶 |
| `SameSite=Lax` | 同站 + top-level navigation（推薦預設） |
| `SameSite=None` | 跨站也帶（必須同時設 `Secure`） |

**登入 cookie 的標配**：`Secure; HttpOnly; SameSite=Lax`。少一個都是漏洞。

### Cookie（client 帶給 server）

Browser 自動把對應網域的 cookie 串起來：

```
Cookie: session=abc123; theme=dark; lang=zh-TW
```

### Authorization

API 認證最常用的 header：

```
Authorization: Bearer eyJhbGc...      # JWT / OAuth2 token
Authorization: Basic dXNlcjpwYXNz      # username:password (Base64) — 只有 HTTPS 下才能用
```

### WWW-Authenticate

當 client 沒帶 token 或 token 失效，server 回 401 + 這個 header 告訴 client 該怎麼做：

```
WWW-Authenticate: Bearer realm="api", error="invalid_token"
```

---

## 5 個新手常踩的地雷

### 地雷 1：API 回 JSON 但沒設 Content-Type

```
HTTP/1.1 200 OK
（沒 Content-Type）

{"name": "homuchen"}
```

Browser / fetch 會猜，可能猜成 `text/plain`，你 `response.json()` 就會炸。**永遠記得設 `Content-Type: application/json`**。

### 地雷 2：Cookie 沒設 SameSite（或設成 None 但忘了 Secure）

新版 Chrome 預設沒設 SameSite 的 cookie 會被當 `Lax` 處理，老程式碼可能突然壞掉。設 `SameSite=None` 時又**必須**同時設 `Secure`，不然 browser 會直接拒絕這個 cookie。

✅ 預設用 `Secure; HttpOnly; SameSite=Lax`，需要跨站再個別調整。

### 地雷 3：CORS `Allow-Origin: *` + cookie

帶 cookie 的請求**不能**用 `*`，必須回**具體 origin**：

```
Access-Control-Allow-Origin: https://app.example.com  ← 要明確
Access-Control-Allow-Credentials: true
```

這時 server 通常要動態 echo 回 client 送來的 `Origin`（搭配白名單檢查）。

### 地雷 4：Cache-Control 跟 ETag 沒搭好

`Cache-Control: max-age=3600` + `ETag` 同時用時：
* 1 小時內 → 直接用 cache（不會碰 server）
* 1 小時後 → 帶 `If-None-Match` 去 revalidate → 304 就繼續用

**常見錯誤**：靜態資源設 `Cache-Control: no-cache`（每次都 revalidate），效能爛但很多人誤以為這樣比較「安全」。

### 地雷 5：信任 X-Forwarded-For 做 IP 判斷

如果你的 server 直接讀 `X-Forwarded-For` 當 client IP，攻擊者只要自己加這個 header 就能偽造任何 IP（繞過 rate limit、IP 白名單）。

✅ 只信任**最外層 proxy（Cloudflare / Nginx）**寫進去的那個 IP，內層的 X-Forwarded-For 都當不可信。

---

## 小結

這次更新從「介紹幾個常用 header」擴展到「現代 Web 開發要知道的 header 全景」：

* **基礎 4 類**：General / Content / Cache / Connection — 收 / 送任何 HTTP 都會碰到
* **現代必備 3 類**：Security / CORS / Cookie & Auth — 沒設好就是漏洞
* **Compression**：開了之後免費省 60-80% 頻寬

如果你只記得 5 件事：

1. API 永遠設 `Content-Type`
2. 登入 cookie 永遠 `Secure; HttpOnly; SameSite=Lax`
3. 網站永遠加 HSTS、CSP、`X-Content-Type-Options: nosniff`
4. 帶 cookie 的 CORS **不能**用 `Allow-Origin: *`
5. 靜態資源用 `Cache-Control: public, max-age=31536000, immutable`

這是 RESTful API 一系列文章中的一篇，想了解更多關於 RESTful API 及 HTTP 的，可以看：[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)。

延伸閱讀：

* [**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)
* [**HTTP Methods 與 RESTful 設計實踐**](/posts/http-methods-which-to-use-and-how-to-use-them-correctly/)
* [**HTTP Status Codes 怎麼用**](/posts/http-response-status-codes-how-to-use/)
* [**Linux HTTP Client 工具 curl 用法**](/posts/linux-http-client-tool-curl-usage/)

## 參考資料

* [HTTP headers - MDN](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers)
* [MIME types - MDN](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
* [RFC 9110 HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)（取代舊的 RFC 7230-7235）
* [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

希望對你有幫助～HTTP header 這東西真的就是「不知道有 → 不會痛 → 知道後再也回不去」，但只要踩過一次坑，這些 header 大概就會記一輩子了。掰掰～👋

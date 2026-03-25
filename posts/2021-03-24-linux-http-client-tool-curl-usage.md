---
title:  "curl 是什麼？Linux HTTP 指令完整教學與常用範例"
date:   2021-03-24 20:00:00 +0800
author: HoMuChen
tags: [http, linux, curl]
category: Web Development
image:
  path: https://storage.googleapis.com/homuchen.com/images/curl-1.jpg
description: "curl 是什麼？完整介紹 curl 指令的用法，涵蓋 GET/POST 請求、Header 設定、檔案上傳下載、Cookie、SSL 憑證等常用範例，讓你快速上手 API 測試與除錯。"
---

**curl 是一個在 Linux、macOS、Windows 上都能使用的命令列工具，用來透過 HTTP（或其他協定）傳送和接收資料。** 簡單來說，它就是你在 terminal 裡的 HTTP client。

想要快速測試一個 API？用 curl 一行指令搞定。想在 shell script 裡抓資料？curl 幫你處理。甚至想寫個簡單的爬蟲？curl 搭配 jq 就很夠用了！

比起打開 [Postman](https://www.postman.com/) 或寫一個 Python script，curl 的好處是**快**——打開 terminal，一行指令，立刻看到結果。

今天來完整介紹 curl 的各種用法：

* HTTP Request 的組成（先搞懂原理）
* curl 常用參數完整介紹
* 如何 debug，確認自己寫的 curl 對不對
* 實用的搭配技巧

## curl 常用參數速查表

先放一張速查表，方便之後隨時回來查：

| 參數 | 用途 | 範例 |
|------|------|------|
| `-X` | 設定 HTTP method | `curl -X POST url` |
| `-H` | 加 Header | `curl -H 'Content-Type: application/json' url` |
| `-d` | 帶 Body（POST data） | `curl -d '{"key":"value"}' url` |
| `-i` | 顯示 Response Header | `curl -i url` |
| `-v` | Verbose 模式（debug 用） | `curl -v url` |
| `-s` | Silent 模式（關閉進度條） | `curl -s url` |
| `-o` | 輸出到檔案 | `curl -o file.html url` |
| `-O` | 用遠端檔名儲存 | `curl -O url/file.zip` |
| `-L` | 自動跟隨 Redirect | `curl -L url` |
| `-k` | 忽略 SSL 憑證驗證 | `curl -k https://url` |
| `-u` | Basic Auth 帳密 | `curl -u user:pass url` |
| `-b` | 帶 Cookie | `curl -b "token=abc" url` |
| `-c` | 儲存 Cookie 到檔案 | `curl -c cookies.txt url` |
| `-F` | 上傳檔案（multipart） | `curl -F "file=@photo.jpg" url` |

## HTTP Request message

在用 curl 之前，先快速了解一下 HTTP Request 的組成，這樣你才知道 curl 的每個參數在做什麼。

### Request line

HTTP message 的第一行，由 method、URL、version 組成：
```
GET /index.html HTTP/1.1
```

### Header lines

第二行開始，每一行是一個 header，field 和 value 用冒號隔開：
```
Host: www.google.com
Connection: Close
Accept-Language: en
```

### Body

Header 結束空一行之後就是 body。GET 通常沒有 body，POST 的表單資料或 JSON 就放在這裡：
```
name=HoMu&phone=0912345678&email=homu@email.com
```

更多關於 HTTP message 的說明，可以看我之前寫過的文章：

[**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)

## curl 基本用法

### 最基本：GET 請求

URL 是必須的，什麼參數都不加，就是一個 GET 請求：
```bash
curl www.google.com
```

### -X：設定 HTTP Method

想要 POST、PUT、DELETE？用 `-X` 指定：
```bash
curl -X POST api.host.com/v1/users
curl -X PUT api.host.com/v1/users/1
curl -X DELETE api.host.com/v1/users/1
```

### -H：加上 Header

用冒號隔開 field 和 value，多個 header 就多打幾次 `-H`：

```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer your-token-here' \
     api.host.com/v1/users
```

### -d：帶上 Body

比如你想 POST 一個 JSON 給 API：
```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"name": "HoMu", "age": 30}' \
     localhost:3000/api
```

如果 data 很多，可以從檔案讀取，路徑前加上 `@`：
```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d @./data.json \
     localhost:3000/api
```

### -i：顯示 Response Header

預設 curl 只會顯示 response 的 body。加上 `-i` 就能看到 status code 和 header：
```bash
curl -i api.host.com/v1/users
```

輸出會像這樣：
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 123

{"users": [...]}
```

## Debug 與進階參數

### -v：Verbose 模式（Debug 必備！）

`-v` 會把完整的 request 和 response 都印出來，包括 TLS 握手、header 交換過程。Debug API 問題的時候超好用：
```bash
curl -v https://api.host.com/v1/users
```

輸出中 `>` 開頭的是你送出去的，`<` 開頭的是收回來的：
```
> GET /v1/users HTTP/2
> Host: api.host.com
> User-Agent: curl/8.1.2
>
< HTTP/2 200
< content-type: application/json
```

### -s：Silent 模式

curl 預設會顯示下載進度條，搭配 `jq` 或在 script 裡用的時候很煩。加 `-s` 關掉它：
```bash
curl -s api.host.com/users | jq
```

### -o / -O：輸出到檔案

`-o` 指定檔名，`-O` 用遠端檔名：
```bash
# 指定檔名
curl -o google.html www.google.com

# 用原始檔名（會存成 report.pdf）
curl -O https://example.com/report.pdf
```

### -L：自動跟隨 Redirect

有些 URL 會回 301/302 redirect，預設 curl 不會自動跟過去。加 `-L` 讓它自動跟隨：
```bash
# 沒有 -L，可能只拿到 301 回應
curl http://google.com

# 加上 -L，自動跟到最終的頁面
curl -L http://google.com
```

### -k：忽略 SSL 憑證驗證

開發環境用自簽憑證？`-k` 跳過 SSL 驗證：
```bash
curl -k https://localhost:8443/api
```

> **注意**：只在開發環境用，production 千萬不要加 `-k`，不然等於沒有 SSL 保護。

### -u：Basic Authentication

需要帳號密碼的 API：
```bash
curl -u username:password https://api.host.com/admin
```

curl 會自動把帳密轉成 `Authorization: Basic <base64>` header。

### -b / -c：Cookie 操作

`-b` 帶 cookie 發送，`-c` 把 response 的 cookie 存到檔案：
```bash
# 帶 cookie
curl -b "session=abc123; lang=zh-TW" https://example.com

# 從檔案讀 cookie
curl -b cookies.txt https://example.com

# 把 server 回的 cookie 存起來
curl -c cookies.txt https://example.com/login

# 登入後帶著 cookie 繼續操作
curl -b cookies.txt https://example.com/dashboard
```

### -F：上傳檔案

上傳檔案用 `-F`，會自動用 `multipart/form-data` 格式：
```bash
curl -X POST \
     -F "avatar=@./photo.jpg" \
     -F "name=HoMu" \
     api.host.com/v1/users/avatar
```

## 利用 nc 指令看看自己到底傳了什麼

你可能寫了一串 curl 指令，不太確定用法對不對，想看看 curl 組出來的 HTTP message 到底長什麼樣子。這時可以用 `nc` 指令在本機開一個 TCP server，然後 curl 打過去看看：

在一個 terminal 開 nc 監聽：
```bash
nc -l 3000
```

在另一個 terminal 打 curl：
```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"name": "HoMu"}' \
     localhost:3000
```

nc 那邊就會印出完整的 HTTP message，你就能確認格式對不對了！

## 實用搭配技巧

### curl + jq：漂亮印出 JSON

API 回傳的 JSON 全部擠在一行，根本看不懂。搭配 `jq` 自動排版：
```bash
curl -s api.host.com/users | jq

# 只取特定欄位
curl -s api.host.com/users | jq '.[0].name'
```

### curl + grep：快速找資料

```bash
curl -s https://example.com | grep '<title>'
```

### 常見的完整範例

一個實際的 API 呼叫通常會長這樣，把上面學的參數組合起來：
```bash
curl -s -X POST \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer eyJhbGci...' \
     -d '{"title": "Hello", "content": "World"}' \
     https://api.host.com/v1/posts | jq
```

## Summary

今天完整介紹了 curl 的各種用法，從最基本的 GET 請求，到 debug 用的 `-v`、處理 SSL 的 `-k`、Cookie 操作的 `-b`/`-c`，應該涵蓋了日常開發中最常碰到的情境。

curl 是每個開發者都該熟悉的工具，不管是測試 API、debug HTTP 問題、還是在 script 裡自動化操作，它都能派上用場。

這是 RESTful API 一系列文章中的一篇，想了解更多關於 RESTful API 及 HTTP 的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

延伸閱讀：
* [**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)
* [**HTTP Headers 完整介紹**](/posts/http-headers/)

感謝您的閱讀～希望對大家有一丁點兒的幫助，掰掰～👋

-----------------------

參考資料

* [curl man page](https://curl.se/docs/manpage.html)
* [MDN - HTTP Messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)
* [jq](https://stedolan.github.io/jq/)

---
title: "[Golang] 4 種發起 HTTP 請求的方式（2026 更新版：含 context、timeout、JSON 處理）"
date: 2022-03-18 11:00:00 +0800
author: HoMuChen
category: Web Development
tags: [golang, http]
description: "用 Go 發 HTTP request 的完整指南：http.Get / Post / PostForm / NewRequest 四種方法、什麼時候用哪個、現代寫法（context、timeout、JSON 編碼）、以及 5 個常見地雷。2026 補上 net/http 最新 best practices。"
---

> **2026-05 更新**：原本這篇只示範 4 種發送方法，但這幾年下來，被讀者問最多的不是「怎麼發」，而是「怎麼發得對」 — context 怎麼帶、timeout 怎麼設、為什麼 connection 沒有被回收。這次更新把這些坑補齊，順便加上一個決策表，告訴你什麼情境用哪種寫法。

這篇文章將介紹如何使用 Go 的 `net/http` 作為 HTTP client 來發起 request，內容會包含：

* 4 種基礎發送方式：`http.Get`、`http.Post`、`http.PostForm`、`http.NewRequest`
* **什麼時候用哪個**（決策表）
* **現代寫法**：`NewRequestWithContext` + 自訂 `http.Client` + JSON 處理
* **5 個常見地雷**（漏 Close、沒 timeout、DefaultClient 的問題等）

如果對 HTTP message 還不熟悉，可以先看：[**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)。

---

## 一句話結論先講

| 你的情境 | 用這個 |
|---------|-------|
| 簡單 GET，沒有自訂 header / timeout | `http.Get` |
| 簡單 POST JSON / 純文字 body | `http.Post` |
| 送 form data（`application/x-www-form-urlencoded`） | `http.PostForm` |
| **要自訂 header / context / timeout / retry**（多數正式環境的情況） | `http.NewRequestWithContext` + 自訂 `http.Client` |

**正式專案幾乎都該用最後一種**。前面三種是給快速腳本、原型用的。

---

## http.Get

```go
func Get(url string) (resp *Response, err error)
```

最簡單的發送方式，沒有 header、沒有 body、沒有 context、沒有 timeout（會吃 `http.DefaultClient` 的設定，預設**沒有 timeout**，這是地雷之一，後面會講）。

```go
resp, err := http.Get("https://api.example.com/users")
if err != nil {
    log.Fatal(err)
}
defer resp.Body.Close() // ← 這行不能少！

body, _ := io.ReadAll(resp.Body)
fmt.Println(string(body))
```

**注意**：`io.ReadAll` 是 Go 1.16+ 的寫法。舊文章你會看到 `ioutil.ReadAll`，那個 package 已經被 deprecated 了，新專案直接用 `io.ReadAll`。

---

## http.Post

```go
func Post(url, contentType string, body io.Reader) (resp *Response, err error)
```

參數為 url、contentType 及 body。除了 `Content-Type` 之外的 header 沒辦法自訂，body 要傳 `io.Reader`。

以下是 `Content-Type` 為 `application/json` 的例子：

```go
jsonBody := []byte(`{"email": "test@homuchen.com", "name": "homuchen"}`)
resp, err := http.Post(
    "http://localhost:5000/api/users",
    "application/json",
    bytes.NewReader(jsonBody),
)
if err != nil {
    log.Fatal(err)
}
defer resp.Body.Close()
```

伺服器端會收到：

```text
POST /api/users HTTP/1.1
Host: localhost:5000
User-Agent: Go-http-client/1.1
Content-Length: 51
Content-Type: application/json
Accept-Encoding: gzip

{"email": "test@homuchen.com", "name": "homuchen"}
```

---

## http.PostForm

```go
func PostForm(url string, data url.Values) (resp *Response, err error)
```

`Content-Type` 會自動設成 `application/x-www-form-urlencoded`，body 用 `url.Values` 傳遞。

```go
// 用 url.ParseQuery
qs, _ := url.ParseQuery("email=test@homuchen.com&name=homuchen")
resp, err := http.PostForm("http://localhost:5000/api/users", qs)
defer resp.Body.Close()
```

```go
// 用 map 組
data := url.Values{
    "email": {"test@homuchen.com"},
    "name":  {"homuchen"},
}
resp, err := http.PostForm("http://localhost:5000/api/users", data)
defer resp.Body.Close()
```

兩種寫法產生一樣的 HTTP message：

```text
POST /api/users HTTP/1.1
Host: localhost:5000
User-Agent: Go-http-client/1.1
Content-Length: 39
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip

email=test%40homuchen.com&name=homuchen
```

---

## http.NewRequest（與 NewRequestWithContext）

要自訂 header、要帶 context、要做 timeout 控制 — 這個就是你正式環境會用的方法：

```go
func NewRequest(method, url string, body io.Reader) (*Request, error)
func NewRequestWithContext(ctx context.Context, method, url string, body io.Reader) (*Request, error)
```

**現代寫法請一律用 `NewRequestWithContext`**。理由：

1. 上游若 cancel（HTTP server handler 收到 client disconnect），你發出的 outbound request 也會跟著 cancel，不會浪費資源
2. 可以用 `context.WithTimeout` 做 per-request timeout
3. trace、log 這些 middleware 都靠 context 傳遞

完整範例：

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

jsonBody := []byte(`{"email": "test@homuchen.com", "name": "homuchen"}`)
req, err := http.NewRequestWithContext(
    ctx,
    "POST",
    "http://localhost:5000/api/users",
    bytes.NewReader(jsonBody),
)
if err != nil {
    log.Fatal(err)
}

req.Header.Set("Content-Type", "application/json")
req.Header.Set("Accept-Language", "en-us")
req.Header.Set("X-Some-Custom-Header", "foo bar")

resp, err := http.DefaultClient.Do(req)
if err != nil {
    log.Fatal(err)
}
defer resp.Body.Close()
```

> 順便提一下 `req.Header.Set` vs `req.Header.Add` — `Set` 會覆蓋同名 header，`Add` 會 append。除非你在做 `Set-Cookie` 這種需要重複的 header，否則用 `Set`。

---

## 推薦的現代寫法：自訂 http.Client

直接用 `http.DefaultClient` 在 production 是地雷（看下一節地雷 #1）。建議自己起一個有 timeout 的 client：

```go
client := &http.Client{
    Timeout: 10 * time.Second, // 整個 request 的 timeout（包含 connect + body read）
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
        DisableCompression:  false,
    },
}

req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
resp, err := client.Do(req)
if err != nil {
    return err
}
defer resp.Body.Close()
```

**重點**：`http.Client` 是 thread-safe，且**內建 connection pool**。所以**整個 application 共用一個 client 實例就好**，不要每次 request 都 `&http.Client{}`，會浪費 connection。

---

## 處理 JSON Response（最常見的需求）

寫 client 95% 的場景就是「打一個 API、parse JSON 回來」。pattern 如下：

```go
type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func GetUser(ctx context.Context, id int) (*User, error) {
    url := fmt.Sprintf("https://api.example.com/users/%d", id)

    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    resp, err := httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }

    var user User
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return nil, fmt.Errorf("decode response: %w", err)
    }

    return &user, nil
}
```

POST JSON 的話，用 `json.NewEncoder` 寫到 buffer 裡：

```go
func CreateUser(ctx context.Context, u User) error {
    var buf bytes.Buffer
    if err := json.NewEncoder(&buf).Encode(u); err != nil {
        return err
    }

    req, err := http.NewRequestWithContext(ctx, "POST", "https://api.example.com/users", &buf)
    if err != nil {
        return err
    }
    req.Header.Set("Content-Type", "application/json")

    resp, err := httpClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode >= 400 {
        return fmt.Errorf("API error: %d", resp.StatusCode)
    }

    return nil
}
```

> 用 `json.NewDecoder/Encoder` 比 `json.Unmarshal/Marshal` 在 streaming 場景更省記憶體（特別是大 response），所以變成現在的慣用法。

---

## 5 個常見地雷

寫 Go HTTP client 三年來，這幾個錯誤我看過最多次：

### 地雷 1：`http.DefaultClient` 沒有 timeout

`http.DefaultClient` 的 `Timeout` 預設是 **0（無限等待）**。你的服務若打 third-party API，對方掛了你的 goroutine 就一起卡死，最後 OOM。

✅ **解法**：永遠自己起一個 client + 設 `Timeout`，或用 `context.WithTimeout` 包 request。

### 地雷 2：忘記 `defer resp.Body.Close()`

`net/http` 用 connection pool 回收 connection。**body 沒被讀完 + close**，連線就不會回到 pool，下次 request 又開新連線，最終 file descriptor 爆炸。

✅ **解法**：拿到 `resp` 立刻 `defer resp.Body.Close()`，**在錯誤檢查之後（因為 err != nil 時 resp 是 nil）**：

```go
resp, err := client.Do(req)
if err != nil {
    return err  // ← 還沒 defer，因為 resp 是 nil
}
defer resp.Body.Close() // ← err == nil 才 defer
```

### 地雷 3：body 沒讀完就 Close

只讀 header 沒讀 body、或讀一半就 break — connection 一樣不會回到 pool。

✅ **解法**：用 `io.Copy(io.Discard, resp.Body)` 把剩下的 body 讀掉再 close：

```go
defer func() {
    io.Copy(io.Discard, resp.Body)
    resp.Body.Close()
}()
```

### 地雷 4：每次都 `&http.Client{}`

```go
// ❌ 不要這樣
func fetchUser() {
    client := &http.Client{Timeout: 10 * time.Second}
    client.Get(...)
}
```

每次 new client 等於每次新的 connection pool，無法重用 keep-alive 連線。

✅ **解法**：把 client 提成 package-level 變數或傳入 dependency：

```go
var httpClient = &http.Client{
    Timeout: 10 * time.Second,
}
```

### 地雷 5：StatusCode 沒檢查

```go
// ❌ 危險寫法
resp, _ := client.Do(req)
defer resp.Body.Close()
body, _ := io.ReadAll(resp.Body) // 500 / 404 也會走到這
```

`err == nil` **只代表 HTTP transport 成功**（連得到、讀得到 response），不代表 server 回 200。一定要檢查 `resp.StatusCode`。

✅ **解法**：

```go
if resp.StatusCode < 200 || resp.StatusCode >= 300 {
    return fmt.Errorf("unexpected status %d", resp.StatusCode)
}
```

---

## 小結

回顧一下這次更新的重點：

* **快速腳本** → `http.Get` / `Post` / `PostForm` 三種就夠
* **正式服務** → 一律 `http.NewRequestWithContext` + 自訂 `http.Client`（共用實例）+ `defer Body.Close()` + 檢查 `StatusCode`
* **JSON 處理** → `json.NewDecoder/Encoder` 比 `Unmarshal/Marshal` 更現代
* **5 個地雷** → DefaultClient 無 timeout、漏 Close、body 沒讀完、每次 new client、沒檢查 status code

如果你只記得一件事：**永遠 `defer resp.Body.Close()` + 永遠用有 timeout 的 client**。光這兩個就能避開 80% 的 production 故障。

延伸閱讀：

* [**HTTP 簡介，以及使用 telnet、nc、curl 等指令來探索**](/posts/http-introduction-telnet-nc-curl/)
* [**HTTP Headers 詳解**](/posts/http-headers/)
* [**HTTP Methods 與 RESTful 設計實踐**](/posts/http-methods-which-to-use-and-how-to-use-them-correctly/)
* [**Linux HTTP Client 工具 curl 用法**](/posts/linux-http-client-tool-curl-usage/)

希望對大家寫 Go HTTP client 有幫助～這些坑都是我自己踩過的，希望你不用再踩一次。掰掰～👋

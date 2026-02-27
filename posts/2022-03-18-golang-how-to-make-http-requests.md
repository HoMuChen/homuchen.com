---
title:  "[Golang] 4種發起HTTP請求的方式"
date: 2022-03-18 11:00:00 +0800
author: HoMuChen
category: Web Development
tags: [golang, http]
---

這篇文章將介紹如何使用golang作為http client，來發起http request，將介紹以下4種做法:
* http.Get
* http.Post
* http.PostForm
* http.NewRequest

一個HTTP Request message不外乎就是**method**、**url**、**headers**跟**body**，如果對於HTTP message還不熟悉的，
可以看我之前寫過的文章: 

[**HTTP 簡介，以及使用telnet、nc、curl等指令來探索**](/posts/http-introduction-telnet-nc-curl)

## http.Get
`func Get(url string) (resp *Response, err error)`

參數為一個url，沒有headers，也沒有body，就是這麼簡單，如果想要客制化自己的header，就必須使用後面的`http.NewRequest`。

## http.Post
`func Post(url, contentType string, body io.Reader) (resp *Response, err error)`

參數為url, contentType及body，headers的部分，除了Content-Type之外的，也無法自己自訂，而body是一個io.Reader，
以下是一個`Content-Type`為`appplication/json`的例子:

```go
jsonString := `{"email": "test@homuchen.com", "name": "homuchen"}`
http.Post("http://localhost:5000/api/users", "application/json", bytes.NewReader([]byte(jsonString)))
```

伺服器端將會收到以下的HTTP message:
```text
POST /api/users HTTP/1.1
Host: localhost:5000
User-Agent: Go-http-client/1.1
Content-Length: 27
Content-Type: application/json
Accept-Encoding: gzip

{"email": "test@gmail.com"}
```

## http.PostForm
`func PostForm(url string, data url.Values) (resp *Response, err error)`

Header `Content-Type`會被自動設為`application/x-www-form-urlencoded`，body是使用`url.Values`來傳遞，
以下為一個範例:

```go
//直接使用字串
qs, _ := url.ParseQuery("email=test@homuchen.com&name=homuchen")
http.PostForm("http://localhost:5000/api/users", qs)
```

```go
//使用map
v := make(map[string][]string)
v["email"] = []string{"test@homuchen.com"}
v["name"] = []string{"homuchen"}

qs := url.Values(v)
http.PostForm("http://localhost:5000/api/users", qs)
```

以上兩個Reqeust，都會產上下列一樣的HTTP message:
```text
POST /api/users HTTP/1.1
Host: localhost:5000
User-Agent: Go-http-client/1.1
Content-Length: 39
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip

email=test%40homuchen.com&name=homuchen
```

## http.NewRequest
`func NewRequest(method, url string, body io.Reader) (*Request, error)`

如果想要客制自己的headers就必須使用`NewRequest`拉，方法如下:

```go
req, err := http.NewRequest("GET", "http://localhost:5000", nil)
req.Header.Add("Content-Type", "application/json")
req.Header.Add("Accept-Language", "en-us")
req.Header.Add("X-Some-Custom-Header", "foo bar")
```

最後要發起HTTP請求，則要使用`http.Client`的`Do`method，以下使用`http.DefaultClient`作為`http.Client`，
至於要如何使用自己的http.Client就不在此多說拉～
```go
jsonString := `{"email": "test@homuchen.com", "name": "homuchen"}`
req, err := http.NewRequest("GET", "http://localhost:5000/api/users", bytes.NewReader([]byte(jsonString)))
req.Header.Add("Content-Type", "application/json")

res, err := http.DefaultClient.Do(req)
```

如此一來就會發送出一個跟前面例子一樣的HTTP Request

## Summary
今天介紹了四種發起HTTP Request的方法，前面三種的彈性比較低但比較方便，有固定的method及content-type，無法隨意更改及加減。

而其實`http.Get`就是`http.Client`的`Get`method，`http.Post`為`http.Client`的`Post`method，
`http.PostForm`是`http.Client`的`PostForm`method。

最後如果想要加上自己更多的header，就要使用`http.NewRequest`，這邊簡單地記錄下使用golang作為http client最基礎的用法，
希望有幫助到任何人，掰掰～👋

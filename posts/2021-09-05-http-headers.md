---
title:  "HTTP headers 簡介: 一些常用的headers"
#date: 2021-09-05 22:30:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api]
---

在HTTP協議中，headers對於每個request，response提供了一些額外的資訊，基本上他們就是只是一對key value pair，由冒號(:)隔開，
今天會看看HTTP協議的格式，header在其中的位置，以及介紹一些常用的header們。

## HTTP messages

HTTP是一個text based的傳輸協議，general的HTTP request message如下：
```
<method> <URL> <version>
<header>
...
...
<header>

<body> 
```

而HTTP response message如下：
```
<version> <status code> <status message>
<header>
...
...
<header>

<body> 
```

可以看到中間部分是由許多行的header所組成，而每一行header是一對key value pair，由冒號(:)隔開，
每個key或value通常第一個字會大寫，然後用`-`隔開，比如說:
```
Connection: Keep-Alive
Content-Length: 10000
Content-Type: text/html
Date: Thu, 02 Sep 2021 02:52:46 GMT
```

如果對於HTTP message format還不熟或想要有更多了解的，可以看我之前寫的文章: [**HTTP 簡介，以及使用telnet、nc、curl等指令來探索**](/posts/http-introduction-telnet-nc-curl/)

## 常用的Headers

Headers對於每個request，response提供了一些額外的資訊，他們就只是一對key value pair，由冒號(:)隔開，你可以放任何你想放的header上去，
不過就是除了你自己的之外沒人看的懂而已，今天我們只討論一般大家約定俗成的header們，以下將他們大致分成幾類: 

category            |header             |description
--------------------|-------------------|--------------
General             | Date              | The time the message was created
                    | Host              | The hostname and port to which the request is being sent
                    | User-Agent        | The name of the application making the request
Payload Content     | Content-Type      | The type of object that this body is
                    | Content-Length    | The length of the body
                    | Content-Encoding  | The encoding of the body
                    | Location          | Where the entity is really locatied at
Conditional Request | ETag              | The entity tag associated with this entity
                    | If-Match          | Get the entity if it matches the tag
                    | If-None-Match     | Get the entity if it does not match the tag
                    | Last-Modified     | The last date and time when this entity changed
                    | If-Modified-Since | Get the entity if it has been modified since the specified date
Connection          | Connection        | To specify options about the request/response connection


## General Headers

* **Date**: 說明這則HTTP訊息被創建出來的時間。

* **Host**: Request要被送去的server目標，你可能會納悶為何會需要這資訊?不是已經透由TCP/IP跟server建立了連線了嗎？
  這是因為

* **User-Agent**: 說明發出request的client是什麼，可能是各種瀏覽器，或者是curl。

## Payload Content
不管是request還是response，body可能會帶有一些資料，關於這些資料的訊息在此一分類討論如下:

* **Content-Type**: 用來說明body裡的資料是什麼格式，常見的像是html檔案的`text/html`、csv檔案的`application/csv`、圖片可能是`image/jpg`
  、你的API可能用的是`application/json`等等，如果沒有Content-Type，收到資料的一方將不知道該要如何處理這些資料，
   至於要用哪種type可以在這查詢[MIME 類別](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
* **Content-Length**: body裡的資料總共有幾個bytes。
* **Content-Encoding**: body裡的資料是什麼ecoding。

## Conditional Requests
Client可能在之前已經取得過相關的資源，並且保有一份備份，如果此資源沒有更新時，可以不需要透過網路在傳輸一次，以節省時間及頻寬。

相關的RFC: [RFC 7232 "HTTP: Conditional Requests](https://tools.ietf.org/html/rfc7232)。

* **ETag**: Response中，對於回傳的資料加的一個tag，有點像是以資料為輸入的hash值，讓client後續使用，會在`If-Match`及`If-None-Match`，以下說明。
* **If-Match**: Server只有在match時，才會動作，通常在PUT操作時用於避免**lost update**的問題，比如說你想編輯一頁Wiki的內容，
  你先要求了本來的頁面，server回傳了`Etag: A`，當你編輯完送出時，帶上`If-Match: A`的header，只有當內容還是A版本時才會更新成功，
  如果在你編輯的時候有人已經先更新了頁面內容，則會回傳412 Precondition Failed，如此一來，避免你的更新會蓋掉別人的更新。
* **If-None-Match**: Server只會在沒有match時，才會回傳資料，因為如果match就代表client擁有的資料的copy還是最新的，就回傳304 Not Modified。
* **Last-Modified**: Response中使用，用來說明回傳的資料最近修改的時間，好讓client可以cache起來並搭配`If-Modified_Since`來更新，詳情見下面。
* **If-Modified-Since**: Request使用此header來決定cache有沒有過期了，比如說上次拿取資源時
  server response了`Last-Modified: Sun, 05 Sep 2021 01:40:14 GMT`，
  這次在request相同資源時，就可以帶上`If-Modified-Since: Sun, 05 Sep 2021 01:40:14 GMT`，
  如果在2021-09-05這時間之後，資料並沒有更新，則server可以回傳304，client就能直接使用cache，
  而不需要再透過網路下載資料，反之，資料有更改的話，就回傳新的資料並帶上新的`Last-Modified`。

## Connection Management

* **Connection**: 每個HTTP request都需要仰賴TCP先建立一個連線，而每建立一次TCP連線都需要三向交握，至少需要花費一個RTT(Round trip time)
  的時間，所以當你有多個request的時候，你會希望TCP建立一次連線就好，之後可以重複使用，所以可以加上`Connection: Keep-Ailve`，
  告訴server，你希望在HTTP response回傳完之後，不要斷掉TCP連線，不過server可能會不鳥你，就會回你`Coonection: Close`。

## Summary

今天簡單看了許多header的用途，還有其他好多好多的header～等遇到了再去了解吧！

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

## 參考資料

* [HTTP headers](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers)
* [MIME 類別](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
* [RFC 7232 "HTTP: Conditional Requests](https://tools.ietf.org/html/rfc7232)

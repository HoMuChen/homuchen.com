---
title:  "HTTP 簡介，以及使用telnet、nc、curl等指令來探索"
date:   2021-03-24 20:00:00 +0800
author: HoMuChen
tags: [http, linux, curl]
category: Networking
last_modified_at: 2021-11-01 18:00:00 +0800
image:
  path: https://storage.googleapis.com/homuchen.com/images/http-intro-1.jpg
---

在網路的世界裡，HTTP扮演著一個重要角色，當你打開Instagram看著無以計數的照片、打開Youtube看看影片、在google上搜尋著你想要知道的答案、瀏覽著別人的網站文章，這些都是HTTP負責把上述的這些照片、影片、文字、等檔案資源從別處的伺服器搬到你的裝置裡，可能是你的手機、平板或是電腦．

HTTP在OSI模型中，是屬於應用層(Application layer)裡的一個通訊協定，透過傳輸層(Transport layer)的TCP來傳輸資料．

關於application layer在整個分層架構中扮演什麼樣的角色，可以參考我之前寫的文章: [**[Networking]Application Layer Overview，什麼是Socket?**](/posts/networking-application-layer-overview-what-is-socket)

# Client server protocol
HTTP是這樣的，想要發起通訊請求的一方作為client(例如你的瀏覽器)，而server則隨時等候，回應client的請求，client首先會建立一個TCP socket，至於TCP連線是怎麼建立，以及資料如何透過TCP connection在client及server之間傳送，則是另外一回事，並不是HTTP需要考慮的事．

Client送出一個請求，例如我要看youtube! 而youtube的server收到這個請求，則回應給他youtube的介面，以及一些影片的清單．

HTTP既然作為client及server之間的語言，他必須有個規範大家才聽得懂，不然有人講中文，有人說英文這樣是無法溝通的．以下就來看看HTTP所傳送的資料到底是長怎樣．

# HTTP message
HTTP message分成兩種，請求(request)及回應(response)，他基本上就是人類可以讀懂的文字．

## Request message
以下一個範例，當你在網址上輸入www.google.com時，你的瀏覽送出去的HTTP message可能會是這樣:
```
GET / HTTP/1.1
Host: www.google.com
Connection: Close
User-agent: Mozilla/5.0
Accept-language: en
```

第一行為request line，由三個部分組成，method、URL、version，分別以空格隔開．

常見的method有GET 、POST 、PUT 、DELETE 、HEAD等等，GET非常地常見，通常代表著你想要取得的某些資源，而你想取的資源則用URL表示，最後HTTP/1.1就是版本．[**點我看更多關於method的介紹．**](/posts/http-methods-which-to-use-and-how-to-use-them-correctly/)

第二行開始為header lines，field跟value以冒號(:)隔開，上面例子中有Host、Connection、User-agent、Accept-language四個header，還有許許多多的header各自有各自的意義，Host代表server，Connection: Close是叫server回傳完資料後就把TCP connection close掉，關於persistent connections的部分，之後會再寫一篇文章來詳細探討．

## Request body
如果client需要傳送額外的資料給server，就要把資料放在body的部分，是在header lines之後空一行，比如說我要通過一個API新增一個user
```
POST /users HTTP/1.1
HOST: api.domain.com
Content-Type: application/json
Connection: Keep-alive

{"name": "HoMuChen", "age": 30, "gender": "male"}
```

## Response message
以下為一個範例:
```
HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Wed, 17 Mar 2021 14:34:29 GMT
Content-Type: text/html
Content-Length: 614
Last-Modified: Wed, 17 Mar 2021 10:27:32 GMT

<!doctype html><html lang="en">........
```

## Status Line
第一行為status line，由三個部分組成，version、status code、phrase，分別以空格隔開．
Status code 跟 phrase拜表著回應的結果，常見的有：

* 200 OK：成功
* 301 Moved Permanently: 資源不在此URL，通常搭配著Location的response header，告訴我們要去哪裡取得資源．
* 400 Bad Request: Request有錯，我server看不懂拉．
* 404 Not Found: 資源不存在．
* 500 Internal Server Error: Server出事了…

詳細的status code的介紹，可以看我另一篇文章:

[**Introduction to HTTP Response Status Codes: How to use them correctly?**](/posts/http-response-status-codes-how-to-use/)

## Header Lines
第二行開始一樣是header lines，我覺得比較重要的是Content-Type，此header就是說明了放在最後body裡的資料是什麼格式，讓client可以去處理．常見的像是text/html、application/json、image/jpeg、application/pdf等等．

## Body
結束header lines之後，空一行，後面就是response body的部分，放著的就是request想要的資料，上面例子中就是html document，也可能是一張圖片的binary data，或是一個Restful API的json資料．

# Get your hands dirty
## text
最後就來使用一些linux command line tool來驗證上面講的對不對吧！
```sh
telnet www.google.com 80
```

使用telnet指令，如此一來就跟google建立了一個TCP連線，接下來輸入並且按下Enter
```text
GET / HTTP/1.1
Host: www.google.com
```

![telnet request response](https://storage.googleapis.com/homuchen.com/images/http-intro-1.jpg)

就可以看到google把網頁吐回來拉～～

## nc、curl

除了telnet之後，也可以用nc作為建立tcp連線的指令，這裡我們用nc來建立一個server，-l 監聽在本機的port 3000上
```sh
nc -l 3000
```

之後在另一個shell，利用curl作為HTTP client，發送HTTP到port 3000
```sh
curl localhost:3000
```

![curl response](https://storage.googleapis.com/homuchen.com/images/http-intro-2.jpg)

nc的terminal上就會出現這些資訊拉～～也就是curl傳送過來的資料，再來試試看上面開創一個新的user的API call吧

```sh
curl -XPOST \
     -H 'Content-Type: application' \
     -H 'Connection: Keep-alive' \
     api.domain.com/users \
     -d '{"name": "HoMuChen", "age": 30, "gender": "male"}'
```

nc server就會收到下面的資料拉！

![curl request](https://storage.googleapis.com/homuchen.com/images/http-intro-3.jpg)

# Summary
HTTP作為網路中最常用的client server 通訊協定，簡單地介紹了HTTP message的格式，他是human readable的text format，熟悉他到底傳來傳去到底在傳什麼，可以幫助我們開發網頁應用時更有底氣。

也可以學習使用一些linux指令，快速的explore別人的API，或是看看自己送出去的request到底有沒有對。

有時也會用curl來寫些簡易的網路爬蟲，可以看看我其他的文章:

[**104人力網站爬蟲: 如何只用shell script來抓取資料**](/posts/crawler-104-jobs-data-using-shell-scripts-curl-and-jq/)

----------

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

感謝您的閱讀~期待下次見！

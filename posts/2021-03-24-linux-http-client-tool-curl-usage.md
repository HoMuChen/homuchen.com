---
layout: post
title:  "A Linux HTTP client tool — curl的介紹及用法"
date:   2021-03-24 20:00:00 +0800
author: HoMuChen
tags: [http, linux, curl]
category: Networking
---

做為一個HTTP client，想要對server發出請求，有許多做法，可能是寫一個python script 或使用其他任何語言，也可以是使用[postman](https://www.postman.com/)這樣的工具，或者是直接在command line上或shell script中使用curl指令．當你想要快速地測試一下某個API，或是explore別人的HTTP service時，直接使用curl是還蠻方便的！甚至直接用shell script來寫爬蟲了！

# Outline

* HTTP Request message
* Curl 的許多參數及用法
* 如何知道自己curl有沒有寫對
* 其他常見搭配的用法及使用情境

![curl]({{site.cdn_url}}/curl-1.jpg)

# HTTP Request message

作為一個HTTP client，要送出一個request，我們先必須知道送出去的message到底會有哪些東西組成．

## Request line
HTTP message的第一行，由method、URL、version所組成，例如：
```
GET /index.html HTTP/1.1
```

## Header lines
第二行開始，每一行是為一個header，field及value由冒號隔開，例如
```
Host: www.google.com
Connection: Close
Accept-Language: en
```

## body
Header結束空一行之後是為body，method是GET的就沒有body，例如你的表單POST的一些資料就會放在body，可能長這樣：
```
name=HoMu&phone=0912345678&email=homu@email.com
```

更多關於HTTP message的說明，可以看我之前寫過的文章：

[**[Networking] HTTP 簡介，以及使用telnet、nc、curl等指令來探索**](/posts/http-introduction-telnet-nc-curl/){:target="\blank"}

# Curl
所以我們要如何使用curl指令來產生HTTP message呢？！

## 基本
URL是必須的，什麼參數都沒有，就產生一個GET message
```
curl www.google.com
```

## -X
設定你想要的method，例如你想要POST，如：
```
curl -X POST api.host.com/v1/users
```

## -H
加上headers，用冒號隔開field及value，如果想要多個header就多打幾次-H，如：

```
curl -X POST \
     -H 'Content-Type: application/json' \
     -H 'X-Whatever-Field: value' \
     api.host.com/v1/users
```

## -d
加上body，比如你想POST JSON string的data給你的API：
```
curl -X POST -H 'Content-Type: application/json' localhost:3000/api -d '{"name": "HoMu", "age": 30}'
```

如果你data很多，想在一個檔案裡頭，也可以使用指定檔案路徑的方式，可以為絕對路徑，也可以是相對的，路徑前必須加上@，例如：-d @./data.json
```
curl -X POST -H 'Content-Type: application/json' localhost:3000/api -d @FILEPATH
```

## -i
按下Enter後，你得到會是server傳回來的body，如果你想要看response的header的話，要加上-i

## -F
上傳檔案

# 利用nc指令看看自己到了傳了什麼
你可能寫了curl指令，不太確定用法，想知道到底curl形成出來的message是不是自己想要的格式，這時可以使用nc指令，在本機端起一個tcp server，在curl這個server，就可以看到HTTP的message囉．

## nc監聽在port 3000
```
nc -l 3000
```

## curl port 3000
```
curl localhost:3000
```

# 其他常見使用情況
## redirect
當curl回來的資料是html時，直接在terminal上噴出一堆字也是很難看，這時長搭配redirect io，把回傳回來的html string寫到檔案裡，就可以用瀏覽器打開來了．
```
curl www.google.com > gg.html
```

## jq
如果content-type是json的話，可以使用jq command幫你parse，不然一堆json string噴在螢幕上，也是眼花．
```
curl api.host.com/users | jq
```

# Summary
今天簡單看了一下HTTP message的格式，以及如何用curl來做出自己想要的HTTP Request，並且知道自己到底有沒有寫對．

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

感謝您的閱讀~期待下次見！

-----------------------

參考資料

* [https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)
* jq - [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/)

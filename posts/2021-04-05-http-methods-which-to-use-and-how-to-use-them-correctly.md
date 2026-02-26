---
layout: post
title:  "What are HTTP Methods？Which to use and How to use them correctly?"
date:   2021-04-04 20:00:00 +0800
author: HoMuChen
tags: [restful api, api, http]
category: Web Development
---

這篇文章主要討論幾個常見的HTTP methods，說明他們分別是否具有哪些特性(Safe、Idempotent)，以及他們應該要怎麼使用，比較會是符合大家的期待．

當然寫server的人可以不照著慣例走，不過如此一來，使用這個API的user可能會很不高興，而這個user可以是公司的客戶，可能是公司內部的其他團隊，也可能是未來的自己！

# Outline
* HTTP Request message格式
* 常見的methods，以及其特性
* 分別介紹各個method的用法

# HTTP Request message
一個general的HTTP request message如下：
```
<method> <URL> <version>
<header>
...
...
<header>

<body> 
```
第一個字就是method，接著為URL跟version，換行後為許多個header，每個header以換行隔開，最後再隔一行之後是body．

對於HTTP message還不熟的，可以看我之前寫的文章：[**[Networking] HTTP 簡介，以及使用telnet、nc、curl等指令來探索**](/posts/http-introduction-telnet-nc-curl/)

URL代表著資源，而method是你想要對資源進行的操作，常見的method如下表：

![http headers]({{site.cdn_url}}/header-1.jpg)

# Don’t surprise your user
並不是所有的server都會實作所有的method，而且每個method要做什麼事，也都是由server所決定的，但是一個好的API通常不會做怪怪的事，而是要符合使用者的期待，使其體驗良好，這裡先來解釋一下safe及Idempotent這兩個特性是什麼吧．
## Safe
如果一個request是safe的，指的是他不會導致server去做一些額外的動作，沒有side effect，例如說改變state、刷你信用卡，這樣的request基本上就是read-only的．
這樣的特性，使得API的user可以大膽放心地去呼叫，實驗你的API，而不必擔心會引發什麼無法挽回的後果，GET、HEAD、OPTIONS都是具有safe特性的method．
## Idempotent
一個Idempotent的操作，指的是這樣的操作執行一次跟執行很多次的結果是一樣的．例如數學上的乘以1，乘以0，一個是數字乘以1或乘以0不管多少次，結果都是原本的數字或者是0．

那有Idempotent的特性，可以帶來什麼好處呢？就是user可以放心的retry，當user不確定剛剛的operation、request有沒有成功時(可能送出後網路突然斷掉、server做完之後再回應之前掛掉、等等…)，就再做一次！

而HTTP method中，除了POST，其他method都預期應該是Idempotent的，Update好幾次，Delete好幾次，應該都跟只做一次的結果一致．

# HTTP Methods
看完了共同的特性之後，接著來看看給個method預期是怎麼使用，以及server如何回應各種情況．

## GET
最常見的method之一，顧名思義就是用來向server索取一些資源．
* 有資源，server就回應200以及資源
* 沒有資源，404

## HEAD
跟GET都一樣，但server並不回傳資源本身，而是只回應headers．
```
<Response>
HTTP/1.1 200 OK
Content-Type: plain/html
Content-Length: 614
```

## OPTIONS
用來詢問server對特定的資源，有支援哪些操作．
* 將結果置於header Allow裡，如下：
  ```
  <Response>
  HTTP/1.1 200 OK
  Allow: GET, POST, PUT, OPTIONS
  Content-Length: 0
  ```

## PUT
Replace the entire resource，對應到CRUD裡的update，就是叫server將我request body裡的資料存起來，如果資源本來不存在就create，在的話就replace．
* 200 OK，成功
* 204 No Content，成功但畫面不需要更新，也就是沒有新的資料產生，client不必取的新的資料，例如說client在更新表單按下save時．
* 201 Created，如果是create的話，並且在header Location放上資源的URI
  ```
  <Response>
  HTTP/1.1 201 Created
  Location: https://api.example.com/users/123 
  ```

## PATCH
Update parts of the resource，跟PUT一樣是update，不過是partial update或者說是merge．
比如說原本有個homuchen的user是長這樣：
```
{
    "name": "HoMuChen",
    "age": 30
}
```
當你PATCH時，想要將age更新為31
```
<Request>
PATCH /users/homuchen HTTP/1.1
Content-Type: application/json
Content-Length: 11

{"age": 31}
```
結果為
```
{
    "name": "HoMuChen",
    "age": 31
}
```
如果是用PUT，則會整個replace掉，name就不見了
```
{
    "age": 31
}
```

## POST
一般來說是指把資料傳給server去做處理，當使用其他的method，語意無法符合時，就會使用POST，常見的有用於Create resources、Search query、Asynchronous tasks．
* 200 OK
* 201 Created
* 202 Accepted，server已接受請求，但還需要時間去完成任務．
* Search Query: Ex. [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)

## DELETE
顧名思義，用來刪除資源．
* 200 OK．
* 207，bulk delete．
* 404 Not Found，要刪除的資源不存在．
* 410 Gone，資源已被刪除．

# Summary
HTTP做為網路世界中眾多通訊協定中的一個，只有當我們更加了解他，service provider才能提供更好用、另client user的學習曲線低，用起來很開心的服務．

今天簡單地討論了各個HTTP Method的用法，每個method有他的語意，只有當server照著大家的預期去做時，才不會造成大家的困擾．

除了Method之外，還有Response code、Header等其他HTTP的組成需要去了解，最後整個API符合RESTful的style是這一系列文章的目標．

--------

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

感謝您的閱讀~期待下次見！

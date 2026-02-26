---
title:  "RESTful API簡介: 什麼是RESTful? 以及為何需要它?"
date: 2021-09-27 20:00:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api]
---

在web開發裡，API是幾乎無所不在，而其中最常見的應該就是基於HTTP協議的RESTful API，
這篇簡介跟討論到底什麼是RESTful，為何有它的出現? 

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

# Introduction
首先，什麼是RESTful，可以說它是一種慣例，一個關於HTTP API如何設計的style，
慣例就是並沒有任何的強制性，但當大家都遵守的慣例時，特立獨行的邊緣人可能就會被排擠，
至少是難以融入大家的，有了慣例，可以不需要在每次要做事前都要溝通，
大家就照著以前一般是怎麼做的做就好。

所以你會希望你要使用的API的夠RESTful的，這樣你用起來才方便、好用，你也會希望你開發的API是RESTful的，
這樣客戶用起來才會開心。當然你也可以不要，如此一來，客戶要用你的API時，會需要更多地去查看你的文件，
他們可能就會覺得麻煩、不開心，你就少了一些賺錢的機會了。

所以接下來看看RESTful API到底是長怎樣吧!

# Resource based
首先他是**resource based**的，也就是每個URL對應到的是一個或多個resource、entity，是**名詞**，
而不會是動詞，比如說下列這樣就是RESTful:
```text
/posts                  -> 代表全部的posts
/posts/1                -> 代表某一篇post
/posts/1/comments       -> 代表某一篇post的所以留言
```
那怎樣不是RESTful呢:
```text
/getPosts               -> 代表全部的posts
/getpostComments/1      -> 代表某一篇post的所以留言
```
# Actions
有了名詞，那**動詞**呢？如果想要對資源做一些操作怎麼辦呢？比如說新增、修改、刪除。
此時就是使用HTTP的method，**GET**、**POST**、**PUT**、**DELETE**，分別對應到**讀取**、**新增**、**修改**、**刪除**。

看幾個例子吧!
```text
GET     /posts/1        -> 取得某一篇文章
POST    /posts          -> 新增一篇文章
PUT     /posts/2        -> 修改某一篇文章
DELETE  /posts/2        -> 刪除某一篇文章
```

# 為什麼RESTful是長這樣呢？
基本上RESTful就是verbs x nouns、操作對上資源，因為HTTP有URL代表資源，還有methods，
這也是為何基於HTTP的RESTful API自然而然就會長成這樣的原因。

![http versus restful api]({{site.cdn_url}}/restful-api-1.jpg)

但HTTP methods有限，所以通常只會有幾種操作，也就是**CRUD**，
這也是為何常常RESTful API就是對資源進行CRUD的操作，大部分簡單的應用也許這樣就夠了，
如果你的應用，無法以簡單的CRUD表示，比如說需要同時對多個資源進行操作才能完成某項任務，
那可以需要重新思考如何設計URL，model你的resourse，之後會在後續的文章裡再來討論。

若對於HTTP協議還不熟悉的，可以看這系列文章中，前面關於HTTP的部分。

# Summary
大概知道了RESTful API應該是什麼樣子，還有許多細節的部分，會在後面的文章中慢慢討論，
比如說URL的設計、如何model resource、documentation、versioning等等...

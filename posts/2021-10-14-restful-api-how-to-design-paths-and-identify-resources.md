---
title:  "RESTful API: How to design paths and identify resources"
date: 2021-10-14 13:20:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api]
---

繼上篇文章[**RESTful API簡介: 什麼是RESTful? 以及為何需要它?**](/posts/restful-api-introduction/)後，
我們知道了RESTful API是**resource based**的，今天講著重討論該如何設計resource，也就是HTTP URL中path的部分。

# Resource based
每個URL都應該對應到一個或多個資源，使用那些使用者與你的服務互動時會需要用到的資源(名詞)，
並使用HTTP Method來表明你想要對資源的操作(動詞)，比如說你是一個網誌服務，
使用者可以看、新增、修改、刪除自己的文章，也能瀏覽別的作者的文章，

```text
GET     /articles               -> 看全部的文章
GET     /articles/d8e209        -> 看某篇文章
POST    /articles               -> 新增文章
PUT     /articles/4f8662        -> 修改某篇文章
DELETE  /articles/4f8662        -> 刪除某篇文章

GET     /authors/homuchen               -> 看作者homuchen的資訊
GET     /authors/homuchen/articles      -> 看作者homuchen的所有文章
```

# 將操作轉成名詞
如果你想要進行的操作比較複雜，可能是需要同時對多個資源進行操作，又或者是無法以CRUD之一來表示，
可以考慮自己創造一個新的Resource。

## 無法以CRUD表示
比如說你想要lock及unlock某篇文章，此時只有一個人可以讀取或修改它，
HTTP Method裡沒有可以表示lock及unlock的操作，所以就自己創造一個資源叫article-locks，
並使用PUT、DELETE來操作。

```text
PUT     /article-locks/{article_id}     -> Lock住某篇文章
DELETE  /article-locks/{article_id}     -> Unlock某篇文章
```

## 牽涉多個資源
當你的一個任務需要同時對多個資源進行操作時，有兩種做法，一個是讓client發出多個api請求，
另一個則是定義一個新的endpoint，來幫使用者做完所有的事。

比如說API的使用者想要發起一筆交易，需要從A帳戶扣一筆錢，在B帳戶新增一筆錢，
如果讓client自己送出兩個api請求也可以，但是他就要處理其他許多狀況，比如說其中一個api成功，另一個失敗怎麼辦。

```text
#還要確保兩個api request同時成功或同時失敗

PUT     /accouts/A/withdrawal   -> 從A帳戶扣一筆錢
PUT     /accouts/B/deposit      -> 在B帳戶新增一筆錢
```

或者可以創造一個新的資源叫transaction，使用PUT來發起一筆交易，而api server則幫client處理了所有該注意的事，
使這個交易atomic、檢查A帳戶裡的餘額夠不夠等等...
```text
PUT     /transactions   -> 發起一筆交易
```

# Identify sub-resources via path segments
有些資源他本身可能沒有意義，也不會被直接使用，必須仰賴在某些資源下，才知道他所要代表的事物，
比如說文章底下的留言，如果不知道它們是在哪篇文章底下，留言本身就無法被看懂，
此時可以使用多段的path來表示parent-child的階層關係。

```text
/articles                                       -> 所有文章
/articles/{article-id}                          -> 某篇文章
/articles/{article-id}/comments                 -> 某篇文章的所有評論
/articles/{article-id}/comments/{comment-id}    -> 每篇文章的某則評論
```

# Summary
今天看了要如何設計我們API的URL，重點就是URL是資源、是名詞，搭配method，表示要對資源進行的操作，
當操作無法以CRUD表示、或需要同時對多個資源進行操作時，可以考慮創造新的domain entity。
另外當資料有階層性的關係時，可以使用多段的path還表示。

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

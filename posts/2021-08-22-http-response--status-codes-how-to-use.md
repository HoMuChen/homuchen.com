---
layout: post
title:  "Introduction to HTTP Response Status Codes: How to use them correctly?"
date: 2021-08-22 22:00:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api]
---

這篇文章會介紹在HTTP協議中，Response status code的作用，有哪些codes以及該如何去使用他們？

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:
[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

# Client Server Model

HTTP是一個Client-Server的架構，客戶端發送一個request，而伺服器端接收到這個request，可能做了些事後，
必須給個回應，不然客戶端會不知所措，到底你有沒有收到我的請求呢？我的請求是合理的嗎？那最後的結果是成功還是失敗，
不管怎樣，總要給個回應吧。

所以在HTTP Response的格式中，第一個就是Status Code，用來簡短地表示請求處理的情況，在大部分常見的簡單請求中，
可能可以只看這個Status code，就知道server處理的情況是如何。

如果還對HTTP response message的格式還不了解的，可以參考先前的文章: [**HTTP簡介**](/posts/http-introduction-telnet-nc-curl/)

# Status Codes

大致可以將code分為四類，分別以2、3、4及5開頭。

* 2開頭: 代表請求成功。
* 3開頭: 需要client在做其他動作，比如說去GET別的URL，或只是content沒變，從cache裡拿就好。
* 4開頭: client request有問題，syntax有問題或是server看不懂，少了某些參數之類的。
* 5開頭: server這邊出了一些問題拉～

Status codes  | Description
--------------|:------
2xx           | Good!
3xx           | Redirection
4xx           | Client你的錯
5xx           | Server我出錯惹

接下來我們就來看看一些常見的status code吧！

## 2xx

* **200 OK**: OK就是OK! 如果你不知道用什麼，但你要表達請求成功了，那就用200吧～😂

* **201 Created**: 當request是**PUT**，要求創建資源時，顧名思義，可以使用201代表資源成功被創建，
  可以在response body裡return整個資源，可以在header Location上，加上新創建的資源的位置。

* **202 Accepted**: 代表你成功接受了請求，然後會asynchronously地處理。

* **204 No content**: 沒有response body，會用到情境像是使用**POST**或**PATCH**做update時，
  成功的話，server沒有額外的資訊需要return給client知道。

## 3xx

* **301 Moved Permanently**: 要求的資源已經搬家了～資源新的位置一般放在Location header中。

* **302 Redirect**: 跟301一樣，會在Location中放上新的URL，跟301不同的是，301是永久性的，就是說舊的URL他之後都不會用了，
  希望用新網頁來取代舊的，而302是暫時的，可能這次有個活動，暫時將頁面導到另個地方，之後有別的活動，又換到新的地方，
  但他還是client繼續使用原本的URL。

## 4xx

* **400 Bad request**: 請求的內容有誤，或是server看不懂。

* **401 Unauthorized**: Authenticate失敗，例如帳號密碼打錯呀，Token不對呀。

* **403 Forbidden**: User有驗證成功，但他沒有足夠的權限來做這個請求。

* **404 Not found**: 請求的資源不存在！

* **405 Method Not Allowed**: 對於請求的資源，不支援所要求的method。

## 5xx

* **500 Internal Server Error**: Server掛掉拉～

# Summary

要使用適當的status code，避免溝通上的誤會，因為可能有懶惰的client看到status code就下了某些判斷，
所以別特立獨行，給你的API的使用者驚喜🎉🙀

---
layout: post
title:  "如何開始開發你的API: API first principle and OpenAPI"
date:   2022-04-09 12:50:00 +0800
author: HoMuChen
description: 開發API應該要使用怎樣的流程，先定義好介面有哪些好處，以及可以使用哪些工具呢？(OpenAPI 3.0)
category: Web Development
tags: [api, http, restful api, openapi]
---

# API first
在一頭熱開始寫code實作你的API service之前，應該首先要關注API中的**I**字，也就是**interface**，
interface是作為服務提供者及服務使用者溝通的介面，為什麼要首先定義好interface呢？有幾下幾個好處:

## 更早得到回饋
為什麼要寫API，總是因為有人要用嘛～有人希望我們提供某些服務，而API就是使用這些服務的入口及介面，
如果我們可以在開工之前，就先把介面設計定義好，並交給客戶，如此一來，
客戶們就可以先看看我們所提供的介面好不好用，有沒有任何的問題，想要的功能有沒有齊全，
如果有需要修改或增減的地方，就能儘早地得到回饋！在真正投入心血開發之前，導正方向～

## 更穩定
由於上述的原因，我們的介面就會更穩定，更少需要變動，整個系統以更容易去維護。
介面的變動往往牽涉到多方人員，越多人依賴這個介面，一旦要改動就麻煩了，所牽涉的層面就越廣。

但也並不是說介面就一定不會變，在整個產品的生命週期中，一定會經歷持續改善的過程，可能要加新功能，
，或是發現有更好用的介面，只是在我們應該盡最大的努力來維持介面的穩定。

## 併行開發
最後，一旦**介面**定義好了之後，服務提供者及使用者就可以同時針對這個介面來進行工作了，
當兩邊都完成各自的工作後，就可以接起來看看有沒有成功，
如此一來就可以避免掉使用者苦苦等著提供者完成的窘境。

那在完成實作之前，該要先如何描述這個介面呢？這個描述的方法或語言應該要是一個標準，
如此一來，各方單位才能看得懂，而這個標準就是**OpenAPI**。

# OpenAPI
OpenAPI是一個描述RESTful API的標準，藉由寫下OpenAPI的spec檔案，
可以讓不管是電腦或是人類的使用者知道，你的API可以做到哪些事，提供了什麼功能及怎麼使用，
而不需要再去看source code，或者是真的打打看你的API service來得知！

這裡就不詳細說明OpenAPI該怎麼使用了，想了解的去官網查詢～

* [**OpenAPI Specification**](https://swagger.io/specification/)

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:

* [**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

---
layout: post
title:  "URL簡介: URL是什麼，由哪些部分組成?"
date: 2021-09-13 22:00:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api, url]
---

這篇文章將會介紹什麼是URL，為何會需要它，以及它是由哪些部分組成的。

# 什麼是URL 
想像你在一座大城市裡，你搭上一部計程車，想要去你朋友家、你小孩的幼兒園、或是去某某旅館，
你必須告訴司機地址; 如果你想聯絡到某人的話，會使用電話號碼; 在政府眼裡每個人有身分證字號。

就像如此，每個東西都有它獨特的識別方法，而且是被大家所公認的，也就是你一說，大家就知道你在說什麼，
知道你所指的是哪個東西，而在網路上，這種識別方法就是**URL**(Uniform Resource Locator)，
也就是我們在瀏覽器上面常常會輸入的**網址**，告訴瀏覽器說你想要前往哪個網站，瀏覽哪些資源。

# URL的組成
以這篇文章的網址`https://homuchen.com/categories`為例，
他代表的就是一篇部落格文章的資源，如何跟server溝通，server在哪裡，以及我想要的特定資源:

![url format]({{site.cdn_url}}/http-url-1.jpg)

* `https`為**傳輸協議**，其他還有許多種，比如說ftp、rtsp、ipfs等等...
* `homuchen.com`就是**host**，用來說明存放資源的伺服器在哪裏，透過DNS可以得到機器的IP位置。
* `/categories`是**path**，用來跟server說你要哪個資源。

## General URL Syntax
一般的URL組成如下:

`<scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<frag>`

component  |description
-----------|:--------------------------------------
scheme     | 用來跟server溝通的通信協議
user       | 需要登入驗證過的user才能存取資源
password   | 需要登入驗證過的user才能存取資源
host       | 一個網域名稱或是IP位置，存放資源的server
port       | server監聽的port，HTTP預設為80，HTTPS則為443
path       | server藉由path來判斷client想要的是什麼資源，什麼資源要用什麼樣的path，<br>由server自己決定，不過RESTful API會有一個關於path設計的慣例，<br>好讓client不需要記很多或一直看文件，關於後續的文章中會再來討論。
query      | 以`?`開始的多對key value pair，每對以`&`隔開，<br>用來傳送更多的資訊給server，比如說搜尋的過濾條件、影片的開始秒數等等...<br>比如說: ?q=TSMC&sort=time

# Summary
一個URL，是網路上一個或多個資源的身分證，今天簡單地看了URL的組成，
對於ㄧ個RESTful API的URL要如何設計，後面再會有詳細的介紹。

這是RESTful API一系列文章中的一篇，想了解更多關於RESTful API及HTTP的，可以看這篇目錄:
[**RESTful API Design — A practical guide**](/posts/http-restful-api-design-practical-guide/)

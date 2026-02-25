---
layout: post
title:  "什麼是message queue? 優點及使用場景"
date:   2019-12-13 20:00:00 +0800
last_modified_at: 2021-10-16 23:00:00 +0800
author: HoMuChen
tags: [message queue]
category: Web Development
---

在大型網頁應用程式系統中，當我們的服務越來越多，服務之間就需要溝通，透過http restful api，想必大家都一定遇過，或許或多或少也聽過使用message queue，那到底它是什麼？為什麼要用它？以及跟restful api有何不同的使用場景呢？

# 什麼是message queue?

![message queue]({{site.cdn_url}}/mq-1.jpg)

顧名思義，就是有個queue，訊息先入先出( FIFO )，基本上就是提供一個讓不同process間通訊的方式( asynchronous messaging )，會有產生訊息的producer，及消耗處理訊息的consumer．

# 為何使用？

為什麼要使用message queue呢？ 他能帶給我們哪些好處？

## Fault tolerance
一但訊息被成功送進queue裡，在他被成功消耗掉之前，都會保存著，有時可能因為莫名原因，consumer都掛了，在consumer恢復之前，需要做的任務還留著，能夠等到恢復之後再繼續處理．

## Decoupling
![decoupling]({{site.cdn_url}}/mq-2.jpg)
訊息的發送方和接受方都不需要知道彼此，consumer和produce可以隨便你用不同語言實作，只要message的格式事先有溝通好，知道就好．

## Scaling
![scaling]({{site.cdn_url}}/mq-3.jpg)
系統可能有時會突然面臨大的流量，此時queue就提供了一個buffer的功能，能夠緩衝尖峰流量，在資源固定的情況下，能夠處理更多的任務，以時間換取資源！
但有時訊息可能真的太多，產生的速度快於消耗的速度，或是你無法接受太長的latency，此時consumer process就可以隨時增加多個，不會有衝突的風險．

# Compare to RESTful API

同樣都是透過network，processes之間的通訊，他們之間最大的不同就是一個是asynchronous message passing，而HTTP request是synchronous(同步)的，也就是client發出了request，會等待在那邊，期待著response回來，所以latency就是一個重要的指標，也主要影響use cases的因素(見下段)．

# Use Cases

## Latency不重要的時候
Sending emails這類工作，使用者可以接受信晚個幾秒，幾十秒甚至幾分鐘到時．
或是比如Build一個你的產品的search index，資料不是由使用者寫入，他也不會知道何時資料應該要出現，就不會怪你的系統怎麼這麼慢拉．

## Computing heavy jobs
比如說image resizing或是video encoding這類CPU intensive的工作，一來是使用者上傳完圖片影片，可能不需要等到這類都做完了你才跟他說ok，二來是你也不會想讓這類工作block住或拖垮你的web server的效能．

## 無法控制的工作
當你的工作需要協調許多資源才能完成時，往往可能一個資源overloaded，就會造成整個工作變得很慢，尤其是當資源又是外部的你無法控制時．

# Tools
主要的Message broker分成兩類，memory based及log based，各類比較知名的分別像是RabbitMQ及Kafka，
對於他們的用法及使用場及不同有興趣的，可以看我的另一篇文章:

[**Difference bwtween rabbitmq and kafka**](/posts/difference-bwtween-rabbitmq-and-kafka/){:target="_blank"}

# Tutorial
之前有寫過的使用[**Redis來當作message broker的示範**](/posts/asynchronous-task-queue-using-redis-and-kue-js/){:target="_blank"}:

如果你連Redis都不想架！可以使用GCP的服務Pub/Sub，上GCP的網站點一點，開箱就用！


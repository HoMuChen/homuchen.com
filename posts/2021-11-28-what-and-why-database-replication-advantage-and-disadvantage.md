---
layout: post
title:  "[System Design] 淺談Database Replication，有何優缺點、做法及何處可見?"
date: 2021-11-28 17:00:00 +0800
author: HoMuChen
category: Web Development
tags: [system design, database]
last_modified_at: 2022-06-30 22:37:00 +0800
image:
  path: https://storage.googleapis.com/homuchen.com/images/database-replication-1.jpg
description: |
  database replication是什麼?有什麼好處及缺點，方法又有哪些呢? 可以在許多系統中看到replication的應用，
  像是各種NoSQL、自己系統的(讀寫分離、cache、search engine)、CDN、DNS等等...
---

# 什麼是database replication?
顧名思義就是將一份資料，複製成多份，並把它放到不同的機器上，
好像也沒什麼好說的🤪，接著會看看為什麼要做複製，它會帶來什麼好處及壞處，
再看看要如何做到replication，最後看看在RDBMS、NoSQL或是你自己的系統，是怎麼應用這些概念的。

# 為何要replication
## 資料備份
把一份資料變成多份放到不同的地方，最明顯的好處就是**備份**，當你的機器壞掉，如果硬碟沒壞，
其實重啟之後資料還是在那邊，但就怕你的機器整組壞光光，或是就是硬碟爆了無法再使用，
此時如果資料有複製道別台機器上，就不用怕會有資料的丟失。

## 讀取效能
資料都在同一台機器時，所有的讀取查詢都必須經由這台機器來完成，一台機器總有他的瓶頸，
一台不行，那你有試過兩台嗎？三台四台五台嗎～

對於讀取效能的增進，主要有兩個方向，分別是吞吐量(throughput)及延遲時間(latency)。

* **read throughput:**
  複製了N份，我就有N台機器可以供我查詢拉，平均分散所有的查詢請求到N台機器上，
  預期最多就可以有N倍的throughput。

* **read latency:**
  另外也可以把一些機器放到離user近一點的地方，減少網路封包來回的時間，降低latency，

# Replication帶來的缺點
## 儲存空間
想當然爾，複製了幾份的資料就需要多幾份的磁碟的空間，不過現在硬碟越來越便宜的時代，
應該不是個大問題。

## 資料的不一致
不一致的主要來源就是兩種: **replication**和**concurrent write**，
試想一下資料如果只有單一來源，那要跟誰不一致呢？反之，因為有了replica，
每份複製要如何保持同步及一致就會是個問題? 會造成什麼consistency的問題，
後面會在陸續討論。

# How
接下來，我們來看看要如何複製。假設你今天有一份檔案，不會再修改，
那就直接將檔案複製一份放到另一台機器上供使用者去讀取，那不就做完了嗎～

沒錯！就是這個簡單，所以問題是什麼呢？ 問題就在於我們會不斷地修改檔案，
資料庫會不斷地接收使用者的insert、update，這時要如何保持多處資料的同步一致呢?

# Master Slave
首先，我們先定義幾個名詞，master為可以接受資料寫入修改的節點，
而slave就是存放複製的檔案的地方，只負責被讀取，並不會從slave中寫入資料。

![master slave repilcation]({{ site.cdn_url }}/database-replication-1.jpg){:target="_blank"}

資料要從master被複製到slave，最簡單的可能就像是直接`cp`，`scp`，
或是你寫備份script，每天固定時間將DB裡的資料寫到另一台DB。

另外現在許多資料庫都有提供**change data capture**的功能: 每當一有資料寫入時，
就會通知你，這有點像是是在application level的trigger，
像是MangoDB的Change Streams或是AWS Dynamo的Streams。

而RDBMS也有類似的功能，像是postgreSQL的WAL、MySQL的Binlog，
如果是cluster的，內部可能也是利用上述的機制來做複製及備份。

# Replication lag
資料要從發生寫入的地方，複製到另一個地方，這中間的時間差就是**replication lag**，
可能是每天將整個資料庫的檔案做一次備份到別台機器，那lag最長就是一天;
如果是在每筆資料寫入的時候，就立即透過網路寫入同一筆資料到另一備份中(透過剛剛說的change data capture)，
那lag可能就是幾毫秒。

## Lag造成不一致
如上所述，資料寫入後、在replication lag這段時間內，多份的複製間並還沒有同步，
也就是說他們是不一樣的！不一樣就是不一致！就會有些問題。
這裡舉兩個例子inconsistency的例子，
就是會無法達成**read your write consistency**及**monotonic read consistency**，

* **read your write**: 寫入一筆資料後在讀取，卻讀不到你剛剛些入的資料，而是取得舊的資料。
  ![not read your write consistency]({{ site.cdn_url }}/database-replication-2.jpg){:target="_blank"}
  如上圖，當你寫入一筆c=3的資料後，資料尚未從master複製到slave，但你馬上從slave讀取，就讀取不到。

* **monotonic read**: 連續的讀取，讀到最新的資料後，接著又讀到舊的資料，經歷了時間上的倒退。
  ![not monotinic read consistency]({{ site.cdn_url }}/database-replication-3.jpg){:target="_blank"}
  如上圖，當你讀取c的值時，首先讀到3的值，接著再讀一次反而不見了。

因為你不知道你是從master還是slave中讀取資料，如果master剛剛接受的新的更新寫入還沒複製到slave，
則slave上的資料就是舊的，從slave讀取就會導致讀不到你剛剛寫入的資料。

## 解決方法
1. 只從master讀取: 但這好像就失去了複製到slave的好處了，read throughput沒有增加，只剩下備份的好處。
2. 當讀自己寫的資料時，從master讀取: 如此一來可以保證有read your write consistency，
   但你要額外判斷query是不是要取得自己的資料。

# 為何要知道這些呢?
## 知道NoSQL的用法
比如說MongoDB的write有各種設定[[1]](#1)，w option可以設為`0`、`1`或`majority`，
你知道他們的區別及取捨嗎?其核心的概念就是今天所討論的replication所造成的
consistency及durability的問題，之後有機會再單獨寫一篇講MongoDB的write concern(TODO)。

## 自己的系統也會有replication
隨著系統越來越複雜，你可能也會使用到多個資料產品，比如說你有個主要的資料庫，
使用者流量越來越大已不堪負荷，可能需要做讀寫分離，
另外還有像是用elasticsearch等搜尋引擎，用redis作為cache，
這些都是一份資料可能同時需要存在許多地方，廣義上來說，也都是replicaton，
以下我們看看cache及讀寫分離這兩個例子。

### Cache
常見的做法可能會是加一台cache database，像是redis，
這也是一種replication，因為你把資料從主要的資料庫裡複製了一份到redis上。

這時候你就有很多事要決定了，要用cache還是本來的資料庫作為master，
也就是說一開始寫入的地方要發生在哪裡: cache還是main database?

還有要多久將兩份資料同步，也就是replication lag會是多久，
可能會有lag也可以沒有，
這一切的決定就會衍伸出有**cache aside**、**read through**、**write through**、**write back**
等等等的架構設計，延伸閱讀:

[淺談各種資料庫cache策略: cache aside、read through、write through、write back](/posts/databse-chache-strategies/){:target="_blank"}

### 讀寫分離
當你的RDBMS資料庫無法再負荷的了大量的寫入或查詢時，或許你有聽過讀寫分離，
就是所有寫入的操作只能在某一台資料庫發生，也就是今天所說的master，
而其他的查詢都透過slave，其實我也沒有實際做過，但核心的概念就是今天所講的replication。

## 其他
### CDN、DNS
廣義上CDN及DNS都有replication的概念，將檔案或DNS record複製到鄰近user的機器上，
DNS甚至複製到了user的本地機器裡，可以看到他們為了支持更好的read performance，
不管是latency還是throughput，而採用了這樣的架構設計，換來的是inconsistency的問題，
就像是DNS record的更新，通常要花上幾分鐘甚至是幾天才有辦法同步。

# Summary
今天看了replication是什麼，會帶來哪些好處(resilient、read performace)，
以及會面對怎樣的問題(inconsistency)，並且知道了一些會用到這些概念的地方，
不管是他內部就幫你做好的(NoSQL)，還是你自己的系統架構，或者是一些已經存在的別的系統(CDN、DNS)。

透過更了解replication的概念，對於我們如何使用別人的產品或是自己系統設計上的取捨都有更清楚深刻的見解，
感謝你的閱讀，有任何問題或是想法都歡迎留言唷～ 掰掰👋

# 參考資料

1. [**MongoDB Write Concern**](https://docs.mongodb.com/manual/reference/write-concern/){:target="_blank" id="1"}

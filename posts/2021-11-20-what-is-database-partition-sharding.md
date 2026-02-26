---
title:  "[System Design] 淺談Database Partition. Centralized and Distributed."
date: 2021-11-21 18:19:00 +0800
author: HoMuChen
category: Web Development
tags: [system design, database]
image:
  path: https://storage.googleapis.com/homuchen.com/images/hash-function-5.jpg
---

什麼是partition，vertical跟horizontal partition有何不同? 阿sharding又是什麼?
這些跟NoSQL有關嗎? 在傳統的RDBMS，像是MySQL或PostgreSQL中，這些概念也有用嗎?
這篇文章將討論上述的問題，看看partition在RDBMS及NoSQL中的實踐應用，以及各種優缺點。

# 什麼是Partition
Partition原意就是**分拆**的意思，在資料的世界裡，就是把一份資料，分成許多小份，
比如說log file的rotation也是，把今年的日記寫在同一本，去年的日記是另一本也是partition。

分拆出來的多份資料，並沒有一定要分散到多台機器中，他們可以被分散到多處，
也能被放在同一台RDBMS裡的不同table，
也就是說partition並不是分散式資料庫(Distributed Database)的專利。

Partion的方式有兩種，分別為vertical及horizontal partition，
我們看資料的方式通常是使用表格的，也就是說有欄有列，
vertical partition就是根據欄來做分拆，而horizontal partition是對列進行分拆。

![vertical partition and horizontal partition](https://storage.googleapis.com/homuchen.com/images/partition-0.jpg)

## Vertical Partition
如下圖，vertical partition是根據欄位來進行拆分，會拆分出schema不同的表格，
主要是為了效能優化，易於管理等目的，再後面的章節中，再來討論應用場景及優缺點。

![vertical partition](https://storage.googleapis.com/homuchen.com/images/partition-1.jpg)

## Horizontal Partition
horizontal partition，是根據列來進行拆分，
每個拆分出來的資料集都跟原本的資料集長一樣，只不過是一個子集合。

![horizontal partition](https://storage.googleapis.com/homuchen.com/images/partition-2.jpg)

# 該如何做Horizontal Partition
要根據列來進行拆分的話，就必須有個方法，來決定每一列是屬於哪一份partition，
作法就是選擇一個資料欄位，用這個欄位經過一些運算或判斷來決定這筆資料屬於哪一個partition，
而這個欄位就稱為**partitioning key**。

![partition key](https://storage.googleapis.com/homuchen.com/images/partition-3.jpg)

在上面的例子中，我們選擇了id做為我們的partition key，將資料拆分為兩份，一份為id是奇數，另一份id是偶數，
除了上述使用ID奇偶數的方法外，哪些欄位可以適合作為partition key呢? 又有哪些方法來利用每筆資料的partition key，
使其分配到特定的partition?

## Range based
就是指shard key依照某個range來指派partition。舉個例子，假設我們選用birthday做為我們的shard key，
然後指派出生年在1960年前的為partition 1，1960-1990的為partition 2，1990之後的為partition 3。

![range partition](https://storage.googleapis.com/homuchen.com/images/partition-4.jpg)

這樣做的缺點是，如果你的資料有一堆1990年後出生的年輕人，那麼partition 3就會有一大堆資料，分散的並不平均。

而優點是做range query時，可以就近就拿到幾乎所有的資料，比如說我想要查詢所有1995-1996出生的人，
此時只要去到partition 3，就可以拿到所有的資料了。

## Hash based
另一個作法，就是先將partition key的值先hash過，如此一來就可以避免使用range partition的缺點，也就是造成hot load，
但是如此一來，將會損失某些資料既有的連續性及相關性。

# Centralized or Distributed?
看完了partition的相關概念之後，接著就來看看是要將partition放在同一台機器裡(**Centralized**)，
或是要分散到多台機器中(**Distributed**)，來討論有何作法及應用場景，
相對應的好壞處、以及相關市面上已經有哪些solution。

![vertical vs. horizontal partition and centralized vs. distributed](https://storage.googleapis.com/homuchen.com/images/partition-5.jpg)

按照上圖的編號的順序一個一個來討論～

## Multiple tables [1]
* **應用場景1**: 將不常用的欄位拆分出來，比如說你有多頁面都會下這樣的查詢:
  ```sql
  SELECT name FROM users WHERE id = '123';
  ```
  只有用到name欄位，但你的`users` table中可能還有description、或是biography等落落長的文字資料，
  平常很少用到，如果放在同一個table的話，每次都還需要將不需要的資料讀取進來。
* **應用場景2**: 除了依照使用頻率來拆分之外，也可以依照資料的性質，比如一些不會改變，
  會用來做聚合計算(COUNT, AVG)的欄位資料，可以拆分到獨自的table。
  ```sql
  SELECT AVG(price) FROM orders;
  ```
  比如說我只關心訂單的平均價格，但如果`orders`table裡包含了所有資訊，類似的query就還是需要將全部的資料都讀取進memory。
* **優點**: 減少不必要讀取，避免佔用server的memory，造成太頻繁的swap。
* **缺點**: 增加了應用程式的複雜度，有些場景需要額外做JOIN來取得資料，而上述的應用場景2，
  現在多會搭配一些適合OLAP的dataware house一起使用，對此不太了解但有興趣的朋友，
  可以用關鍵字**OLAP**、**data warehouse**、**columnar database**、**column oriented database**去搜尋。

## Table partition [2]
* **應用場景**: 最常見的就是選擇**時間**相關的欄位來作為partition key，以下以postgresql為例，
  使用`measurement` table中的`logdate`作為partition key:
  ```sql
  CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
  ) PARTITION BY RANGE (logdate);
  ```
  ```sql
  CREATE TABLE measurement_y2021m09 PARTITION OF measurement
      FOR VALUES FROM ('2021-09-01') TO ('2021-10-01');

  CREATE TABLE measurement_y2021m10 PARTITION OF measurement
      FOR VALUES FROM ('2021-10-01') TO ('2021-11-01');

  CREATE TABLE measurement_y2021m11 PARTITION OF measurement
      FOR VALUES FROM ('2021-11-01') TO ('2021-12-01');
  ```
  並按照每個月的range創建partition。
* **優點**: 常見的access patern可能會是讀取最近的資料，對於比較久以前的資料很少去讀取，所以不需要每次讀取都在一個大的table裡尋找，
  藉由partition創造出多的小的table，改善效能。
  另外像是如果你有保留政策(retention policy)的話，也變得相當容易去管理，比如說你只保證保留近一個月的資料，
  所以超過一個月的partition就直接DROP掉就好了！
* **缺點**: 跟以下的[3]一起說明～

## Multiple RDBMS servers [3]
終於要進到分散式系統的領域了～ 把一份大的檔案分拆成許多小份，當然也有許多益處，
讀取效能的優化、更易於管理等等，但隨著資料的長大，資料增加的速度越來越快，
總有一天一台機器還是會遇到瓶頸，此時就有了將資料放在多台機器的想法。

原理都是一樣的，選定一個欄位作為shard key，你的application server將決定這筆資料的要放到哪台DB上，

![RDBMS sharding](https://storage.googleapis.com/homuchen.com/images/partition-6.jpg)

* **優點**: 增加了throughput，不管是卡在Disk或是CPU，一台機器不夠寫不夠讀，那你有試過兩台三台十台嗎～
* **缺點**: application code的複雜度變大了是一定的，除此之外，每個partiton現在已經各自獨立，
  跨partition沒有unique constraint、reference constraint，更不可能JOIN
  secondary indexes也必須各自去建立，幾乎許多RDBMS提供的好用的功能，在跨partition時都不能用了，
  只能在自己的application code上去實現。

  比如說你想做JOIN，但被referenced的table已經被我們做partition了，application code就必須去到每一台機器裡去找，
  然後在程式裡面把資料做結合。

  舉個例子
  ```sql
  CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    name        VARCHAR(20)
  );

  CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER REFERENCES users (id)
  );
  ```
  我們有`users`及`orders` table，orders的user_id是個foreign key指到users的id，
  如果我們今天將users及orders用它們的id做partition了，
  則同一個user的orders可能會被分散到不同的機器之中，所以就沒法JOIN拉～

  ![after sharding, not able to join](https://storage.googleapis.com/homuchen.com/images/partition-7.jpg)
  
  其實這裡的解決方法就是選用user_id作為shard key就好了，但不可能所有的資料集都有辦法使用同樣意義的欄位來做partition。

## Sharding in NoSQL [4]
在大數據時代，為了處理大量資料而冒出的許多NoSQL都有的內建功能，
就跟上面講的原理一樣，只不過這次資料庫本身就幫我們把sharding這件事都處理好拉～
不需要我們寫任何一行的code，只需要在configuration file或UI上設置一下就好。

而面對的問題還是一樣的，所以大部分的NoSQL提供的API都比較簡單，
不像RDBMS有各種constraint，可以JOIN，transaction可以用。

關於NoSQL怎麼實作sharding的，每種產品也都不同，大家要自己去看他們是如何實作的，shard key怎麼選的，可以自己選嗎?
是range還是hash partition，如何動態增加或減少shard的數量(這部分這篇文章裡沒有討論到)。

比如說MongoDB可以自己選擇shard key，也可以選擇shard strategy，
大家可以根據自己的use case來調整，詳見[MongoDB sharding](https://docs.mongodb.com/manual/sharding/)

## Multiple services? [5]
其實好像沒看到DB做vertical partition，然後把不同的partition分散到不同的機器上的，就算是column oriented的DB，
應該也是用horizontal partition的方式來分散它的資料(不太確定)，如果有人想要補充，歡迎留言～開開孤陋寡聞的我的見識。

所以這邊我的Multiple services的意思是指，比如說今天你的`users` table有個大頭貼的欄位，或是任何大的document或Blob，
雖然DB也可以存，不過也可以將它拆出來，使用其他的服務像是AWS S3、或是GCP的GCS，好拉，
其實加這個就只是要讓我的表格不會空一格😂

# 總結
今天知道了什麼是partition，有分為vertical及horizontal的，以及該如何做horizontal partition，選定shard key，
以及決定你的shard strategy，不管你是自己做，還是資料庫幫你做好好的，根本的核心概念及會面臨的問題都是一樣的，
有了這些概念，對於不管是自己家系統的架構，或是別的資料庫產品，都有更好地了解，
並更清楚地可以根據適合自己問題場景，選擇適當的作法。

感謝你的閱讀，有很多地方我可能還是不懂或搞錯的，或是有任何想法，更棒的idea想討論的，都歡迎可以留言唷～ 掰掰👋

# 參考資料
* [PostgreSQL: Documentation](https://www.postgresql.org/docs/10/ddl-partitioning.html)
* [Understanding Database Sharding](https://www.digitalocean.com/community/tutorials/understanding-database-sharding)
* [MongoDB sharding](https://docs.mongodb.com/manual/sharding/)

---
title:  "淺談各種資料庫cache策略: cache aside、read through、write through、write back"
date: 2022-06-25 23:54:00 +0800
author: HoMuChen
category: Web Development
tags: [system design, database]
image:
  path: https://storage.googleapis.com/homuchen.com/images/database-cache-0.jpg
---

資料庫的快取策略那麼多種: **cache aside**、**read through**、**write through**、**write back**，
常常哪個是哪個也分不清楚、記不起來，今天將分享這些策略背後的內功心法，
讓大家不用在為了記不起這些招式的名稱而傷腦筋。

# 什麼是資料庫快取(database cache)?
快取是一種策略，用來增進你的應用程式及資料庫的效能，
作法是將常使用的資料放在具有更快存取速度的的記憶體中(in memory)，
而達成這樣的目的的策略又有好多種:

* cache aside
* read through
* write through
* write back

有沒有系統性的方法可以歸納這些策略，各自的優缺點即適用的情況又是為何？
讓我們接著看下去！

# Replication
其中最核心的關鍵就是: **cahce就是一種replication**，因為資料一部分放在資料庫中，
而另一個放在快取，這樣就是一種replication，在分散式系統中，要做replication就只要問兩個問題:

1. 誰是Master？誰是Slave？
2. 複製的過程是同步的還是非同步的？

之前有寫過一篇關於replication的文章: 
[**[System Design] 淺談Database Replication，有何優缺點、做法及何處可見?**](/posts/what-and-why-database-replication-advantage-and-disadvantage/)，有興趣的朋友可以再去看看～

## Master or Slave
首先，我們先定義幾個名詞，master就是接受資料寫入修改的最一開始的節點，
而slave就是將master的改變複製一份過來存放的地方。

換句話説，資料要寫入，就是寫到master，然後會在複製一份到slave。

![master slave repilcation]({{ site.cdn_url }}/database-replication-1.jpg)

## Synchronous or Asynchronous replication
從master複製到slave間的過程，會有一個時間差，
同步及非同步的複製差別在於有沒有等到資料確定被複製到了slave才會回傳寫入成功。

* synchronous: 當資料寫入到master時，唯有等到他確定被複製到了slave，才會ack成功。
* asynchronous: 資料一寫入到master，不等它被複製到了slave，就ack成功。

![Synchronous or Asynchronous replication]({{ site.cdn_url }}/database-cache-1.jpg)

# 各種cache策略
知道了Replication之後，要怎麼將這些觀念應用在cache上呢？就是將以下兩種情況排列組合！就會得到四種快取策略拉～

1. 資料庫作為master vs. 快取作為master
2. asynchronous vs. asynchronous replication

![Cache strategies]({{ site.cdn_url }}/database-cache-0.jpg)

基本上，使用資料庫作為master，可以**保證資料不會丟失**；
若使用快取作為master，則是**適合write heavy並且可以容許資料丟失**的應用。
而**同步跟不同步則決定了資料是否會有不一致**的現象。
接著就讓我們分別更加仔細地看他們個別的作法及優缺點吧。

## cache aside
* 寫入: 資料寫入時就是寫到主要的資料庫中。

* 讀取: 應用程式讀取資料時，會先檢查是否有在快取中了，有的話就回傳，沒有的話就去資料庫中讀取，並存放一份在快取中，
  因為這個複製的動作是當這筆有被讀取到時才會進行，所以為非同步的複製。

* 優點: 資料直接寫入到資料庫中，就保證不會丟失，最容易實現，因為寫入時的動作跟沒有快取時是一模一樣的。

* 缺點: 第一次讀取時一定會cache miss，而非同步的複製就可能造成資料間的不一致。

## read through
* 寫入: 資料寫入時就是寫到主要的資料庫中。

* 讀取: 跟cache aside非常相似，唯一差別在於應用程式只直接從緩存去拿資料，不需要同時知道緩存及資料庫的存在，
  而由快取本身決定要去哪裡拿資料。

* 優點: 應用程式的程式碼會更加簡潔。

* 缺點: 同cache aside。

## write through
* 寫入: 寫入時直接寫入緩存及資料庫，必須等到兩者都寫入成功才成功。

* 讀取: 直接讀取緩存，通常搭配read through，如此一來，應用程式都將只需面對緩存就好。

* 優點: 不會有cache miss。

* 缺點: 寫入資料要等到快取及資料庫都寫入成功後才算成功，所以會增加寫入延遲。

## write back、write behind
* 寫入: 寫入時直接寫入緩存，在以非同步的方式寫入到資料庫，這麼做可能有幾個原因，
  你的應用有大量write而資料庫負荷不了，可能在緩存那邊做一個batch insert。

* 讀取: 直接讀取緩存。

* 優點: 不會有cache miss、適用於write heavy的應用、減少對資料庫的負荷。

* 缺點: 資料有可能會丟失，當資料還未被成功從緩存複製到資料庫時，如果緩存這時掛掉，那些資料就不見了。

# 結論
今天從另一個角度來看看各種緩存策略，寫入到資料庫的，不會有資料丟失的問題，
同步及異步的複製則決定了資料的一致性，write heavy的應用可以考慮第一時間寫入緩存。

策略沒有絕對的對錯，根據你的使用場景(write to read ratio、persistency、consistency)，選擇最適合的方案。
希望今天的分享對你有一丁點兒的幫助，祝大家事業成功、生活美滿！掰掰～👋

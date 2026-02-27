---
title:  "[System Design] Data model: Relational V.S. Document"
date:   2020-12-28 20:00:00 +0800
author: HoMuChen
category: Web Development
tags: [data model, system design, database]
image:
  path: https://storage.googleapis.com/homuchen.com/images/data-model-1.jpg
---

開發應用程式時，時常使用到資料庫，儲存資料並在之後需要時將其取出，如今有許多的資料庫產品可供選擇，提供各種不同的data model及function，在各種使用情境下有不同的表現，開發者根據你的應用程式的需求、資料之間的關係、access pattern、scalability、ACID transaction、fault-tolerance、會有各種不同的適合的選擇．

接下來只單純討論資料庫提供給我們application programmer們的data model，看看是否在哪些情況比較適合用哪一種，主要是探討relational 及 document這兩種data model.

## One-to-many relationship
讓我們先從一個簡單的例子Todo list開始，假設我們應用程式有使用者，每個使用者有多個Todo，就這麼簡單的一個one-to-many relationship．

### Relational DBMS

![database relationship](https://storage.googleapis.com/homuchen.com/images/data-model-1.jpg)

如上圖， 一般使用SQL database的做法，會開兩個table，分別是users及todos，並且在todos table有個欄位user_id為foreign key指到user table

### Document database

![document in NoSQL](https://storage.googleapis.com/homuchen.com/images/data-model-2.jpg)

而在document database中，我們可以將整個資訊存成一個JSON document如上圖，當我們的UI需要呈現某使用者的todo的時候，資料庫只需要一個disk seek就可以拿到全部的資料，對比於relational database，必須在todos table裡找到相對應的rows，再將其與users的row合併．

可以看到document database用來model one-to-many relationship的資料可說是天生的適合．

## Many-to-one and Many-to-many relationship

現在假設我們要加入新的功能，使用者可以新增標籤，並把自己的Todo加上一個標籤．

![Many-to-many relationship](https://storage.googleapis.com/homuchen.com/images/data-model-3.jpg)

Relational database按照normalization的做法，就是再多一個tags table，user_id指向Users，而Todos再多一個foreign key指向Tags，如上圖沒什麼問題．

而Document database則會向下圖這樣:

![document in NoSQL](https://storage.googleapis.com/homuchen.com/images/data-model-4.jpg)

資訊重複出現了好幾個地方，容易造成不一致，比如說我想把Coding改成Programming，除了在tags這個array裡面要修改之外，兩個todo裡的tag也要同時修改才行．

### Document database就不能做normalization嗎？
當然是可以的！分別儲存三種類型的document: User、Tag、Todo，當某個user要取得他的資料時，就必須分別從三類document找出相對的document，在合併起來．

那這跟relational database的join有什麼不一樣嗎？

其實本質上是一樣的！只不過使用relational database時是database幫你做，而使用document database則是要在application code上面自己做，除了會有更多的network round trip time之外，relational database通常也會幫你優化．

## Schema flexibility
另外他們倆之間常被討論到的不同，就是schema的有無，雖然說document database可以讓你隨意的放入任何的JSON document，但我們通常不會這樣做，一般來說都會把相同類型，有ㄧ樣資料格式的document放在一起，只不過資料庫本身並不會強迫每個document的schema要一模一樣．

這樣的彈性，讓schema evolution也算方便，資料庫裡可以同時保有舊有的資料和新的資料 ，比如說todo想要新增一個欄位created_at，或是todo原本只能有一個tag，用一個string來表示，現在想要改成可以有多個tag，新新增的資料不在是一個string而是一個array．

但如此一來application programmer在使用document database時，就不能保證拿到的資料的格式，會出現類似這樣的code:
```javascript
if (todo && todo.created_at) {
  //...
}
if (todo && Array.isArray(todo.tags)) {
  //...
}
```

時間久了，資料可能會越來越亂，一不注意就跑出個error:

```Cannot read property ‘some_field’ of undefined!```

該如何管理schema evolution，不讓你的應用程式crash，隨著新功能及新資料的加入能夠compatible，繼續穩定的運行就是另一門學問，有機會可以再來探討．

## What’s the situation preferring to schema-less approach?
其實能有schema最好就有，他是你的資料的一個documentation，一個contract，讓programmer寫起程式來更有信心，不用擔心東擔心西，擔心會不會少了個欄位就讓我的process crash掉，那有什麼樣的情況會更適合使用document database嗎？

* 資料來自外部，格式不是妳能控制的
* 有非常多種類的object，分別將每個object放到個別的table可能不太適合

比如說event sourcing的架構，每種event type都有各自的資料格式，放在relation database的一個table，會有很多欄位是空的，schema定義起來也會非常麻煩．

再來你的資料來源可能來自爬蟲、外部的API，格式可能改變，所以可以在拿到資料的時候就先存起來，之後讀的時候做處理，不然可能就會丟失部分的資料了．

## Summary
如果你的資料之間的關係不複雜，基本上是one-to-many的，一個self-contained的JSON document能夠包含所有需要的資料，那麼document based的DBMS就相當適合，會有更好的performance，因為資料都在一起．

Relational database更適合當你的資料之間的關係複雜，有許多many-to-one、many-to-many relationship時，幫你處理join的動作，雖說使用document database也是可以如此，但join的動作必須在application code上執行．

另外document database也提供更彈性的schema，當你的應用需要面對許多不同且不確定、不是自己能控制的資料格式時，document database也許會有更好的support．

## Reference

1. [Designing Data-Intensive Applications Chapter 2](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321)
2. [https://martinfowler.com/articles/schemaless/](https://martinfowler.com/articles/schemaless/)

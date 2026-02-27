---
title:  "[Networking] 網路的架構，Layered Architecture"
date:   2020-04-04 20:00:00 +0800
author: HoMuChen
category: Networking
tags: [layered architecture]
image:
  path: https://storage.googleapis.com/homuchen.com/images/layered-arc-1.jpg
---

網路是個如此巨大的工程，要如何架構，才能讓全世界的人通力合作，一起打造這豐富的世界呢？答案就是Layered Artichecture ．

----------

## Layered Architecture
網路的最終目的，就是讓兩個執行在不同機器的程式可以互相溝通、交換資料，例如你的瀏覽器chrome跟網頁伺服器溝通，你手機的Skype跟另一個人的Skype溝通，而這中間，資料經過了重重難關、無數的機器及路由器，這麼多的機器到底是如何一起合作的呢？

答案就是分層的架構，Layered Architecture，生活中很多地方都可以看到類似的架構，我們以公司內部的信件為例好了，假設現在有一間公司有ABC三間分公司，在A公司的Alice想要寄封信給B公司的Bob，Alice首先寫了信的內容，將之放入信封內，並寫上收件人: B公司的bob，之後將信封交給A公司裡的一個叫做信件部門的部門，信件部門將信封寫上B公司的地址，再將信封交給附近的郵局，而郵局則使用卡車、飛機等運輸工具將信封運到B公司附近的郵局，此郵局再送到B公司，最後B公司的信件部門收到信，將他交給Bob．

![Layered Architecture](https://storage.googleapis.com/homuchen.com/images/layered-arc-1.jpg)

分層架構將一項任務分成了許多層，每一層只專心做自己的事，並且使用下一層所提供的服務．

例如上圖中，人這一層，只專心將內容寫入信中，放進信封袋裡，然後交給下一層的信件部門就好，人這一層使用了信件部門這一層提供的服務，完全無需去擔心這封信最後是如何抵達另一個人那邊去，而信件部門層則使用郵局提供的服務，郵局服務提供了公司的工司的寄送，而信件部門就只專心將信件交給公司裡的某某人．

## Layers in the Internet
網路世界的分層如下圖，根據OSI Model應該是有七層，但就目前常用，只介紹此五層，Application layer、Transmission layer、Network layer、Link layer、Physical layer．

![Layered Architecture](https://storage.googleapis.com/homuchen.com/images/layered-arc-2.jpg)

### Application layer
這裡就是我們的應用程式所在地方，根據你的程式所要達成的目的，各自執行著自己的協議．例如網頁瀏覽器跟伺服器，一個說給我看某某網頁首頁，伺服器就說，好！給你！這之間資料交換的格式及方法，就是由HTTP協議所規範，只要瀏覽器跟伺服器都遵守HTTP的規範就能互相溝通．電子信箱服務使用的則是SMTP，查詢網域ip位置的是DNS，傳輸檔案的FTP等等．

而所有的application都必須依賴使用下層transmission layer的服務，transmission laye會負責applications之間的通訊，application只需要相信transmission layer會將信息傳遞給另一個application，專心做自己的事就好！

### Transmission layer
Transmission layer protocol負責傳遞信息於application之間，一台機器上可能有多個application，而transmission layer protocol則是用port number來分辨到底目標是哪個process．

目前網路世界中有兩種Transmission layer protocol，分別是TCP及UDP，TCP提供的服務保證資料一定會完整無誤地抵達目的地，並且還有flow control及congestion control．而UDP則沒做這麼多事，資料可能會丟失．

### Network layer
每台連上網路的機器都會有個地址，有就是IP位址，Network layer中的唯一一個protocol就是IP protocol，負責將資料從一個IP送到另一個IP，也就是從一台host到另一台host！這之間會經過許多的router，每個執行IP protacol的router會決定要將封包傳遞給哪下一個router來抵達目的地，但並不保證封包一定會抵達．

### Link layer
以上兩層當web dev以來，也從來沒碰過，哈！不熟，如果有興趣的人在自己去找資料囉～

### Physical layer
這邊就是訊息從0101的bits轉換成真正物理世界裡存在的傳播媒介的地方了，可能是電磁波四處亂射，也可以是光走在光纖裡，或是電走在電線裡．

## Summary
為了讓兩個在不同host上的process能夠通訊，首先你要指出你想要的通訊的process在什麼地方，透過ip:port這個pair，network layer會負責將信息送到擁有這個ip的機器，但卻不保證資料不會丟失，而network layer則透過port知道要將資料傳給哪個process，並且如果是TCP的話，會保證資料完好無缺地抵達另一個process那邊 (TCP可靠的傳輸建立在不可靠的IP上，酷吧！)，最後application根據自己的邏輯，來決定資料的格式，如何及何時發送和接收．



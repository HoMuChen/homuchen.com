---
title:  "[Networking]Application Layer Overview，什麼是Socket?"
date:   2020-05-05 20:00:00 +0800
author: HoMuChen
tags: [linux, socket, tcp, udp]
category: Networking
---

![application layer](https://storage.googleapis.com/homuchen.com/images/app-layer-1.jpg)

# Process communication
上次講過了網路的分層架構之後，接下來要來關注application layer，這一層就是我們應用程式所在的地方，應用程式可能是網頁瀏覽器、電子信箱、Skype等等，每種不同的應用程式會有他們自己的通訊協定，規定應用程式之間該如何交換資料，以及資料的格式，常見的協定例如是HTTP、FTP、DNS等等．

那application layer的process們之間要怎麼互相通訊呢？就是要利用transport layer所提供的服務．

# What is socket?
Application layer的process必須使用transport layer所提供的服務來進行通訊，而這之間的介面就是socket，process只要把資料寫入socket，另一個process從socket讀出資料就好，就是這麼簡單～至於資料是如何在這之間傳遞的，底下的每一層 (transport、network、link、physical layer) 都幫你處理的好好的了，applications就只需要專心做自己的事就好！

不過在通信之前，必須要知道對方在哪裡，資料才有辦法送到，一個socket就是一組ip:port pair，ip用來分別process所在的機器，而一台機器上會有許多的process，port number則用來分別是想要跟哪個程序溝通，有些服務基本上監聽在一些固定的port上，方便client來連，例如HTTP使用80、FTP用21、SSH使用22等等．

另外當client要向server通訊時，作業系統會隨機指定一個port給他，如此一來server才會知道訊息要回傳到哪裡．

![application layer](https://storage.googleapis.com/homuchen.com/images/app-layer-2.jpg)

# Transport layer service
Application programer可以根據自己想打造的應用程式的需求，在兩種transport layer所提供的服務中選擇，一個是TCP，另一個是UDP，以下分別介紹．

## TCP
TCP提供的是一個可靠的服務，確保資料一定會完整無缺的抵達另一端，使用TCP的application programmer不用擔心資料會到不了另一端，專心於application protocal就好．

TCP有congestion control的機制，當網路變得壅塞的時候，會放慢sender的速度，這是為整個網路著想的設計，但對於application並沒有直接的幫助，可能還會使得速度變慢．

## UDP
UDP的服務並不可靠，也就是並不保證資料一定會送達，對於一些應用來說或許是可以接受的，比如即時的通話或視訊，上一秒的聲音或畫面不見就不見了．是ok的．

另外UDP也沒有flow control跟congestion control，sender想送多快就多快，所以如果有application覺得TCP做太多事了，開發起來綁手綁腳，想要看短的latency，就可以考慮使用TCP，例如google的QUIC就是基於UDP上，再重新自己實現了可靠的傳輸．

# Socket programming
之後會寫一篇使用Node.js的net module來實際地使用一下TCP的服務，並在這之上打造自己的application protocol，待續…

# Application layer protocols
接著也會陸續會介紹一些常用的application layer的protocol: HTTP、SMTP、DNS，待續…

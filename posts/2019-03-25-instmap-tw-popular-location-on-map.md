---
title:  "InstMap TW — 從地圖上找尋附近的台灣Instagram熱門景點"
date:   2019-03-25 20:00:00 +0800
author: HoMuChen
tags: [instagram, react, node.js, express, gcp]
category: Web Development
image:
  path: https://storage.googleapis.com/homuchen.com/images/instmap-1.jpg
description: "InstMap TW 是我做的小工具，在地圖上找出附近台灣 Instagram 熱門地點並瀏覽貼文，也分享背後用到的 React、Express、GCP 與 DynamoDB 等技術。"
---

到了一個地方，想知道附近有什麼好玩的景點嗎？想看看IG，Instagram上大家都去哪裡嗎？可以使用我最近做的一個玩具服務[InstMap TW](https://instmap.tw)，找尋台灣最多人標記的地標，或是附近最近的相對熱門的地標．

![instmap](https://storage.googleapis.com/homuchen.com/images/instmap-1.jpg)

點選地圖旁的小人圖案，可以使用您現在的位置做搜尋，不想開定位的話，也可以手動拉動地圖改變中心點．

每個地點點進去可以看到該地點的貼文，可切換成瀏覽圖片或是日期、文字、按讚數、留言數等相關資訊．

![instmap](https://storage.googleapis.com/homuchen.com/images/instmap-2.jpg)

使用到的技術、工具、服務大概是

1. Front-end
   * react
   * redux
   * create-react-app（開發時怎麼串接後端 API，可以看 [**如何用 create-react-app 開發，整合一個或多個 API backend server**](/posts/create-react-app-integrate-multiple-api-backend-servers/)）
2. Back-end web server
   * Nginx
   * ExpressJS
3. Cloud service
   * AWS DynamoDB
   * Cloud Firestore
   * Cloud functions
   * Cloud Pub/Sub
   * Cloud Schedule
   * Compute Engine

---
title:  "如何用create-react-app開發，整合一個或多個API backend server"
date:   2020-08-22 20:00:00 +0800
author: HoMuChen
category: Web Development
tags: [react, create-react-app]
---

在開發single page application時，會需要透過api來取得及操作資料，本篇文章將示範如何在使用create-react-app開發時，整合一個甚至是多個backend api server！

![create-react-app with multiple backend servers](https://storage.googleapis.com/homuchen.com/images/cra-1.jpg)

# Create-react-app
使用create-react-app時，簡單一個指令npm start 就可以開始開發，此時CRA會起一個webpack dev server來serve static files，通常我們會想要做類似這樣的動作: fetch(‘/todos’) 、fetch(‘/api/todos’) 來跟我們的API server通訊，此時該如何讓CRA的dev server將request proxy到我們想要的API server呢？

# 透過package.json
最簡單的方法就是在package.json中加一個proxy欄位，"proxy": "http://localhost:5000" ，如此一來，所有的request便會被proxy到http://localhost:5000．

## 想解決的問題
這樣的做法很簡單但卻不太彈性，通常我們會希望外部的資源可以透過環境變數去控制，而不是寫死在檔案裡面，同一份codebase，透過設置不同的環境變數擁有不同的部署，可能是開發環境、測試環境、或staging、production環境 (https://12factor.net/codebase) ．

另外將proxy寫在package.json中，只能將所有的ajax導到同一個server，假如您是service oriented architecture或microservices這種架構，可能會有許多的服務，例如data api、search api、authentication api、payment api等等．那該如何將不同的path，例如/api、/search、/auth，route到各自的服務呢？

# 透過setupProxy.js
首先需要安裝dependency

```sh
npm i -D http-proxy-middleware
```

接著在src資料夾裡新增一個檔案setupProxy.js，範例如下:

```javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

const API_HOST = process.env['API_HOST'];
const SEARCH_HOST = process.env['SEARCH_HOST'];
const AUTH_HOST = process.env['AUTH_HOST'];

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: API_HOST,
    })
  );
  
  app.use(
    '/search',
    createProxyMiddleware({
      target: SEARCH_HOST,
    })
  );
  
  app.use(
    '/auth',
    createProxyMiddleware({
      target: AUTH_HOST,
      changeOrigin: false,
    })
  );
};
```

如此一來，就能透過環境變數API_HOST、SEARCH_HOST、AUTH_HOST來指向你的服務，變且成功整合多個服務囉！

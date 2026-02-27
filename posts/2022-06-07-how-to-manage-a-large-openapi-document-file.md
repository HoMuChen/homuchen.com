---
title:  "HTTP API: 該如何管理一份很大的OpenAPI document？"
date: 2022-06-07 00:07:00 +0800
author: HoMuChen
category: Web Development
tags: [http, restful api, api, openapi]
---

OpenAPI的document文件可以變得非常大一份，特別是當你有好幾百個routes的時候，
這時候單一份的yaml檔管理起來可能會非常頭大，這篇文章將分享在這種情況下，
我是如何將一份大的檔案拆分成許多小的檔案，易於管理。

## OpenAPI Specification
OpenAPI也被稱為Swagger，是一個用來描述你的API的標準，可以根據這個標準來撰寫你的文件，
我想你應該很熟悉了，如果還不熟的，
可以先看看官方的說明: [OpenAPI specification](https://swagger.io/specification/)。

## 我如何拆分檔案
### 使用JSON格式
官網上的範例文件都是使用yaml，而我偏好使用JSON，基於以下幾個理由：

* 許多語言都內建支援JSON格式，尤其是javascript，JSON的J就是這樣來的。
* 可以直接由程式控制，將需要共用的(**response**、**schema**、**parameter**)寫在不同檔案，要用的時候在import進來就好。
* 除了以上常常會需要共用的，造成spec檔案會變的很大的一個因素就是有太多的**path**，也能將path依照你想要方式做拆分。

寫起來就會像是下面這樣:

#### index.js
```javascript
const schemas = require('./components/schemas')
const securitySchemes = require('./components/securitySchemes')
const parameters = require('./components/parameters')
const responses = require('./components/responses')
const paths = require('./paths')

module.exports = {
  openapi: '3.0.0',
  info: {
    title: 'Example API Overview',
    version: '1.0.0',
    contact: {
      name: 'API Support',
      email: 'b98901052@ntu.edu.tw'
    }
  },
  servers: [{
    url: '/api/v1'
  }],
  components: {
    schemas: schemas,
    parameters: parameters,
    responses: responses,
    securitySchemes: securitySchemes
  },
  paths: paths
}
```

#### paths.js
可能就會長得像下面這樣:
```javascript
const pets = require('./pets')
const users = require('./users')
const stores = require('./stores')

module.exports = {
  ...pets,
  ...users,
  ...stores,
}
```
可以將所有`/pets`開頭的路由放到`pets.js`，以此類推，如此一來就便於管理，
不會有一份檔案裡頭有好幾百個path，
可以更快地知道要修改一個endpoints要去到哪一支相對應的檔案。

### 輸出
當你要輸出JSON檔時，只需要把上述`Object`做一個`JSON.stringify`就行，或是依賴其他套件轉成`YAML`的格式。

### 限制
但前提是你使用的動態語言，像是`javascript`、`python`等等，才有這樣方便的好處。

### 就是想用YAML
其實不用JSON也是可以，上述的方法一樣可以套用到YAML檔，
也就是將一些可以重複使用的schema、response，以及拆分出來的path們放到不同的檔案，
只是可能需要依賴一些額外的library來幫你做合併的動作。

像是[swagger-cli](https://github.com/APIDevTools/swagger-cli)，
就可以讓你把`$ref`的目標，放到不同的檔案。

## 總結
想要拆分一份大的OpenAPI spec檔以便於管理，核心的關鍵就跟寫程式是一樣的，DRY(Don't repeat yourself)，
將會重複使用的部分拆出來，在原先的OpenAPI spec也能做到，就是使用`$ref`，
但今天更近一步跟大家分享將其寫在不同的檔案的方法: 使用`JSON`格式、利用其他套件`swagger-cli`。

希望以上的內容對你有一丁點的幫助！掰掰～👋

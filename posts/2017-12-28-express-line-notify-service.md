---
title: 使用Node.js + Express整合Line Notify通知服務
date:   2017-12-28 20:00:00 +0800
author: HoMuChen
category: Web Development
tags: [express, node.js, line notify, middleware]
image:
  path: https://storage.googleapis.com/homuchen.com/images/line-notify.jpg
---

快速簡單地使用一個express的middleware完成line notify的oauth2流程，取得access\_token來做後續的消息推送

使用line notify可以簡單地讓網站開發者推送訊息到使用者的line裡，雖不像line bot可以跟使用者做更多的互動，但如果只是要單方面的的發送訊息，使用line notify就足矣，而且還不像line bot的push api要收費，這個不用錢～

---------------------------------

# 登入流程

Line notify的流程大致來說是這樣的:

![Line Notify Login Flow](https://storage.googleapis.com/homuchen.com/images/line-notify.jpg)

1. GET https://notify-bot.line.me/oauth/authorize
* 帶著你的client id及redirect_uri，GET上面的url，使用者就會被導到line的登入頁面
* 登入成功之後，line那邊會倒回上述的redirect_uri並且query string帶著code
2.POST https://notify-bot.line.me/oauth/token
* 將第一步得到的code，post到上述url，就可以拿到一個token
3. POST https://notify-bot.line.me/api/notify
* 帶著上面步驟所取得的token及訊息，post上面的url，使用者就可以收到消息拉～

# 套件使用

接下來要實作以上流程覺得好麻煩喔～小的已將上述前兩個步驟寫成一個express的middleware供大家使用，說明如下：
1. npm install express-line-notify
2. 傳入config物件，需要clientId及clientSecret
3. 選個endpoint來走以上oauth2流程，記得endpoint要加在callbackurl裡
```javascript
const express = require('express');
const lineNotify = require('express-line-notify');
const config = {
  clientId: 'your-client-id',
  clientSecret: 'your-client-secret',
}
const app = express();
app.use(
  '/endpoint_u_want_to_use',
  lineNotify(config),
  otherMiddleware
);
app.listen(3000);
```
4.如上實作之後，便可以在otherMiddleware裡的req[‘line-notify-access-token’]拿到token拉～就可開發者要怎麼使用了

---------------------------------

最後附上git hub repository，有較為詳盡的使用說明．

[HoMuChen/express-line-notify](https://github.com/HoMuChen/express-line-notify)

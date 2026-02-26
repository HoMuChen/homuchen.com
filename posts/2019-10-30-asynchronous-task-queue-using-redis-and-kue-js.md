---
title:  "快速擁有一個Asynchronous Task Queue，使用Redis and Kue.js"
date:   2019-10-30 20:00:00 +0800
tags: [message queue, node.js, redis]
author: HoMuChen
category: Web Development
last_modified_at: 2021-10-28 16:49:00 +0800
---

這是篇教你如何在node.js環境下，快速擁有一個Task queue的tutorial，如果想了解什麼是message queue，以及為什麼跟什麼時候要使用它，可以參考我的另外一篇文章[**什麼是message queue? 優點及使用場景**](/posts/message-queue-advantages-use-cases)!

# Outline
1. 部署Redis，使用Docker，在本地起一台Redis
2. 介紹Kue.js

# 部署Redis

先準備一個shell script run_redis.sh ，記錄下docker指令，以便之後繼續使用，內容指令如下：

```bash
#!/bin/sh
docker run                        \
  -d                              \
  -p 6379:6379                    \
  -v $PWD/redis_data:/data        \
  --name my-redis                 \
  redis
```

解釋一下這個docker指令各個參數的意義:

1. -d 在背景執行
2. -p 6379:6379將容器內的port:6379映射到本機的port:6379
3. -v 將容器內的檔案掛載到本機，此處將容器內存放redis 資料的資料夾 /data 掛載到$PWD/reids_data，也就是當前目錄的redis_data資料夾
4. redis為image的名稱，可以用例如redis:latest, redis:5.0，後面加上版本號，沒加就是latest，可用的版本及latest是哪一版可以從此連結查詢https://hub.docker.com/_/redis/

執行完之後執行 docker ps 就可以看到container的資訊如下

![docker ps]({{site.cdn_url}}/kue-1.jpg)

# 介紹Kue.js

## 安裝

```$ npm install kue```

## Connection

```javascript
var kue = require('kue')
var queue = kue.createQueue();
```

預設會連接到127.0.01:6379的redis，如果想要改變，可以

```javascript
var queue = kue.createQueue({
  redis: {
    port: 1234,
    host: '10.0.50.20',
    auth: 'password',
    db: 3, // if provided select a non-default redis db
    options: {
      // see https://github.com/mranney/node_redis#rediscreateclient
    }
  }
});
```

## Produce message

連接到message broker後，就可以開始送message過去拉～

```javascript
queue.create('email', {
    title: 'welcome email for tj',
    to: 'tj@learnboost.com',
    template: 'welcome-email',
}).save( function(err){
   if( !err ) console.log( job.id );
});
```

這裡我們發送了一個message到名為email的queue裡，內容就是個JSON object.

## Consume message

接著我們就可以在別的地方，接收發出去的訊息及處理拉

```javascript
queue.process('email', function(job, done){
  doSomethingWithData(job.data)
  
  done();//acknowledge this message
});
```

queue.process接收兩個參數，第一個是queue的名字，這裡是以’email’為例，第二個參數是一個callback function，他有兩個參數，分別是job跟done，job.data就是我們剛剛發送出去的message，而done是一個function，當你確定這個message已經處理完的時候可以執行done()


## Concurrency controll

上面例子中，一次只會接收一個message直到你ack這個message，如果你的工作是IO密集的話，你可能會想一次同時處理多個message，此時可以在process function中，加入第二參數:

```javascript
queue.process('email', 10, function(job, done){
  doSomethingWithData(job.data)
  
  done();//acknowledge this message
});
```

這樣一來，這個worker process同時就可以接收處理10個message!

------------------

以上是簡單地介紹如何連接到message broker，以及產生和消耗信息，完整的說明文件及更多功能用法，可以到github上看看:

[Automattic/kue](https://github.com/Automattic/kue)

# 延伸閱讀
* [**什麼是message queue? 優點及使用場景**](/posts/message-queue-advantages-use-cases)

* [**RabbitMQ和Kafka有何不同？何時該選用哪種產品？**](/posts/difference-bwtween-rabbitmq-and-kafka/)

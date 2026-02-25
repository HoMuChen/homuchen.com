---
layout: post
title:  "利用Docker建立PostgreSQL開發環境"
date:   2018-07-25 12:19:15 +0800
author: "HoMuChen"
category: Web Development 
tags: [docker, postgres]
---

首先先將需要的configuration variable放到環境變數裏，在這裡就是我們的PostgreSQL database server要起在哪一個port，user，password，db等等，準備好你的 dev.env檔案如下，然後執行 . ./dev.env

```
export PG_PORT=5432
export PG_USER=admin
export PG_PWD=secretpwd
```

再來是一個shell script run_postgres.sh ，記錄下docker指令，以便之後繼續使用

```bash
#!/bin/sh
docker run                                  \
  -d                                        \
  -p $PG_PORT:5432                          \
  -e POSTGRES_USER="$PG_USER"               \
  -e POSTGRES_PASSWORD="$PG_PASSWORD"       \
  -v "$PWD/pgdata":/var/lib/postgresql/data \
  postgres
```

解釋一下這個docker指令各個參數的意義:

1. -d 在背景執行
2. -p $PG\_PORT:5432 將容器內的5432port映射到本機的$PG\_PORT
3. -e 注入環境變數到容器裏，有哪些環境變數可用，可以參考官方連結[https://hub.docker.com/\_/postgres/](https://hub.docker.com/\_/postgres/){:target="_blank"}
4. -v 將容器內的檔案掛載到本機，此處將容器內存放postgres 資料的資料夾 /var/lib/postgresql/data 掛載到$PWD/pgdata，也就是當前目錄的pgdata資料夾
5. postgres為image的名稱，可以用例如postgres:latest, postgres:9.6，後面加上版本號，沒加就是latest，可用的版本及latest是哪一版可以從此連結查詢https://hub.docker.com/\_/postgres/

執行完之後執行 docker ps 就可以看到container的資訊如下

接下來要進去容器裡面create table，下下sql指令的話，就是執行

```docker exec -it {container id} psql -U $PG_USER```

PG_USER是我們的環境變數，預設的DB(此處為admin)的名字就跟PG_USER一樣，進去容器之後看到如下，就可以開始使用拉～

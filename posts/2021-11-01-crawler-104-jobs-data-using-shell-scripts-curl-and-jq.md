---
title:  "104人力網站爬蟲: 如何只用shell script來抓取資料"
date: 2021-11-01 20:00:00 +0800
author: HoMuChen
category: Web Development
tags: [crawler, http, curl, linux]
---

想要抓取網路上的資料，大家可能都會想到python爬蟲，但有時並不需要那麼麻煩，
linux command line tool就有許多好用的工具，
今天以104人力網站的為例，示範如何只使用shell script，就可以開始抓取資料!

# 前言
這邊假設大家已經有網路爬蟲的基本概念了，一般大家寫爬蟲最多人用的就是python，
流程就是到目標網站上操作，並且一邊觀察chrome dev tool，將http requests用python的requests套件重現，
之後將response回來的資料做parse，最後存起來，可能是存到檔案或是資料庫裡。

![爬蟲流程: 用command line tool來實現]({{site.cdn_url}}/104-1.jpg)

前面三個步驟是觀察，後面要進行動作，共有三個主要的動作，
分別為: 發起HTTP請求、處理HTTP回應的資料，將處理好的資料存起來。

而這三個動作，分別都有好用的command line tool可以直接使用，分別為:
* Make HTTP requests: **curl**
* Parse JSON response data: **jq**
* Save data: **redirect >>**

# curl
curl是個HTTP client，相當於python的requests套件，想要在104上搜尋**軟體工程師****第1頁**的結果，
可以使用下列的指令，有兩個querystring的參數: keyword及page。

其他還有許多篩選條件像是地區，年資，有興趣的去104網站自己按按就知道該使用哪些參數囉，這裡就不再多做描述。

```sh
curl -H 'Referer: https://www.104.com.tw/jobs/search' https://www.104.com.tw/jobs/search/list?keyword=軟體工程師&page=1
```

對HTTP message或curl的使用還不熟的，可以參考我之前寫過的文章:
* [**HTTP 簡介，以及使用telnet、nc、curl等指令來探索**](/posts/http-introduction-telnet-nc-curl/)
* [**A Linux HTTP client tool — curl的介紹及用法**](/posts/linux-http-client-tool-curl-usage/)

# jq [**[1]**](#1)
成功取得回應後，可以看到terminal上噴出一堆密密麻麻的資訊，難以去閱讀，今天為例的104 API，
回傳的是application/json的資料格式，可以將這坨資料pipe到jq[**[1]**](#1)指令上，他可以幫我們parse JSON格式的資料，
也可以做其他的動作，包括選擇我們要的欄位、map、filter、transform等等，詳細的使用方法可以到官網看他們的文件。

104的api回傳JSON格式的資料很方便，但很多網站沒有或是找不到這種API可以使用，就必須處理html的解析，
我有找到一個工具**pup**[**[2]**](#2)，看起來也蠻好用的，如果你知道其他更好用的方法，也歡迎留言跟大家分享唷～

# redirect
處理好回應後，最後將資料導到file裡存起來就好囉~ 如果寫到同一份檔案當中，記得使用**>>**，
才不會把先前的資料給蓋掉唷。

# 完整程式碼
```sh
#!/bin/sh

if [ -z $1 ] || [ -z $2 ]; then
    echo ""
    echo "  Usage:"
    echo "      sh ./`basename $0` \$keyword \$page"
    echo ""
    echo "  Example:"
    echo "      sh ./`basename $0` 軟體工程師 1"
    echo "      sh ./`basename $0` 專案管理 2"
    echo ""
    exit
fi

keyword=$1
page=$2

curl \
  -H 'Referer: https://www.104.com.tw/jobs/search' \
  https://www.104.com.tw/jobs/search/list\?\&keyword\=$keyword\&page\=$page \
  | jq
```

前面為防呆的檢查，確保使用者有輸入關鍵字及頁數，用起來就像這樣:
```sh
sh ./104.sh 軟體工程師 1
```

得到的結果如下:
![data]({{site.cdn_url}}/104-2.jpg)

如果只想要資料的list，可以再pipe到jq做進一步的處理:
```sh
sh ./104.sh 軟體工程師 1 | jq .data.list
```

得到的結果如下:
![data]({{site.cdn_url}}/104-3.jpg)

# 結語
有時只想要簡易的爬蟲，不想要大張旗鼓地寫個python時，就可以寫個shell script，加上crontab就能去抓取資料。

比如我只是想記錄某個keyword資料量的每天趨勢變化，就可以
```sh
sh ./104.sh 軟體工程師 1 | jq .data.totalCount >> data.csv
```
一天跑個一次，一份csv檔案，就可以達到我們想要目的。

感謝你閱讀到這邊～希望以上的內容對你有一丁點的幫助，掰掰～ 👋

# 附錄
1. jq - [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/)
2. pup - [https://github.com/ericchiang/pup](https://github.com/ericchiang/pup)

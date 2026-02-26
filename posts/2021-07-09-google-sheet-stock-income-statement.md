---
title:  "[Google sheet]我如何製作股票損益表，自動抓取最新股價"
date:   2021-07-09 16:30:00 +0800
author: HoMuChen
category: Google Sheet
tags: [google sheet, finance]
---

此篇文章將分享我是如何製作我持有股票的未實現損益表，看起來的成果如下:

![google sheet: stock income statement](https://storage.googleapis.com/homuchen.com/images/income-statement-1.jpg)

# 主要功能

* **自動更新股價**
* **根據最新股價，計算損益，並以顏色區分損或益**
* **近一年的股價折線圖**

# Step by Step

## 製作表格

首先填入表頭欄位，在這裡我們會有:

**股票代號**、**名稱**、**近一年股價**、**現價**、**漲跌**、
**成交量**、**持有張數**、**市值**、**持有成本**、**損益**、**損益百分比**

![google sheet: blank data table](https://storage.googleapis.com/homuchen.com/images/income-statement-2.jpg)

每新增一檔股票，需要我們自己填入的有**股票代號**、**名稱**，**持有張數**、**持有成本**

* **股票代號**: 爲後續**GOOGLEFINANCE**函式的參數，這裡以台北股市台積電為例爲TPE:2330
* **名稱**: 就你自己開心如何稱這黨股票就好～
* **持有張數**: 就是你的持有張數...
* **持有成本**: 每次買股票時，就將成本加上去吧

## 取得最新股價資訊(現價、成交量)，計算市值

* **現價**:

  使用**GOOGLEFINANCE**函式來取得股價資訊！

  在D2儲存格中輸入公式: **=GOOGLEFINANCE(A2, "price")**，之後下來套用至整個D欄
  ![google sheet: GOOGLEFINANCE price](https://storage.googleapis.com/homuchen.com/images/income-statement-3.jpg)

* **成交量**:

  **=GOOGLEFINANCE(A2, "volume")**

* **市值**:

  將**持有張數**及**現價**相乘即可～ **=D2*G2**

## 計算當日漲跌損益

* **漲跌**:

  有了現價，可以跟昨日收盤價做比較計算出今日漲跌: **=D2 - GOOGLEFINANCE(A2, "closeyest")**
  ![google sheet: GOOGLEFINANCE closeyest](https://storage.googleapis.com/homuchen.com/images/income-statement-4.jpg)

* **損益**:

  即為**持有成本**及**市值**相減: **=H2-I2**

* **損益百分比**:

  即為**損益**除以**持有成本**: **=IF(ISBLANK(I2), 0, J2/I2)**
  ![google sheet: GOOGLEFINANCE](https://storage.googleapis.com/homuchen.com/images/income-statement-5.jpg)
  **IF**及**ISBLANK**的用途爲如果你尚未實有該檔股票，持有成本爲0或空白，卻又寫列入表中觀察，
  則**損益百分比**顯示為0，否則將出現錯誤．

## 股價折線圖

公式為: **=sparkline(GOOGLEFINANCE(A2, "price",today()-365,today(),1))**
![google sheet: GOOGLEFINANCE sparkline](https://storage.googleapis.com/homuchen.com/images/income-statement-6.jpg)

* GOOGLEFINACE:
  總共四個參數，第一為股票代號、再來是起始日期跟結束日期，此範例使用一年前today()-365到今天today()、最後爲資料的interval，
1代表每天，也可以是7代表每週
* sparkline:
  可以再一個儲存格裡畫圖的函式，詳細的用法可以看我先前寫的文章:[[Google Sheet]Sparkline，在儲存格裡插入迷你圖表](/posts/google-sheet-sparkline/)

## 替漲跌及損益百分比上色

最後！股市就是要紅紅綠綠才比較好看，將賺錢的部分標上紅色，虧錢的弄上綠色吧！

首先點選漲跌那一欄(E)，接著點選工具欄**格式** -> **條件格式設定**
![google sheet: format](https://storage.googleapis.com/homuchen.com/images/income-statement-7.jpg)

將格式規則設為大於0，格式設定樣式改為字體紅色，綠色及損益率的部分也是一樣！
![google sheet: format](https://storage.googleapis.com/homuchen.com/images/income-statement-8.jpg)

如此一來就大功告成囉🎉

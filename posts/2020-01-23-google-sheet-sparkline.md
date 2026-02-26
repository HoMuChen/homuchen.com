---
title:  "[Google Sheet]Sparkline，在儲存格裡插入迷你圖表"
date:   2020-01-23 20:00:00 +0800
author: HoMuChen
category: Google Sheet
tags: [google sheet, sparkline]
---

# Sparkline用起來長怎樣

我在[**[Google Sheet]我如何製作進度表**](/posts/google-sheet-track-progress/)這篇裡

![google sheet: track progress](https://storage.googleapis.com/homuchen.com/images/spark-line-1.jpg)

以及[**[Google sheet]我如何製作股票損益表，自動抓取最新股價**](/posts/google-sheet-stock-income-statement/)

![google sheet: stock](https://storage.googleapis.com/homuchen.com/images/spark-line-2.jpg)

大家可以看到一些儲存格裡都有迷你圖表，像是柱狀圖、線圖，這就是sparkline這個函式的功用，讓我們不需要額外插入一些圖表，就能直接在格子中畫圖．

# Sparkline用法

## sparkline(range, [options])

range就是你的資料，是一個範圍，比如A1:A10、C3:L3

options則是一些其他設置，可有可無，例如圖表的類型是line、bar，圖表的顏色，線條粗細等等．寫法為在一個大括號內{}，一連串的屬性及相對應的值，以分號(;)分開，例如：{"charttype","bar"; "color","blue"; "max",1}

## 圖表類型

圖表的類型可以在options裡透過**charttype**屬性設置

有幾種選擇line, bar, column, winloss (預設為line)

## charttype, line: 折線圖
* color: 線的顏色
* linewidth: 線的粗細

## charttype, bar: 堆疊長條圖

* max: 設定橫軸的上限值
* color1: 兩個堆疊交錯的長條圖，第一種的顏色
* color2: 兩個堆疊交錯的長條圖，第二種的顏色

## charttype, column: 直條圖

* color: 直條圖的顏色
* lowcolor: 最低值的顏色
* highcolor: 最高值的顏色
* firstcolor: 第一欄的顏色
* lastcolor: 最後一欄的顏色
* ymin: 欄高的下限值
* ymax: 欄高的上限值

# 範例

## 黑色折線圖

sparkline(E1:E10)

![google sheet: sparkline line chart](https://storage.googleapis.com/homuchen.com/images/spark-line-3.jpg)

## 藍色且較粗的折線圖

sparkline(E1:E10, {"color","blue"; "linewidth", 2})

![google sheet: sparkline line chart](https://storage.googleapis.com/homuchen.com/images/spark-line-4.jpg)

## 堆疊長條圖

sparkline(H1:H10, {"charttype","bar"; "max", 50})

![google sheet: sparkline stack bar chart](https://storage.googleapis.com/homuchen.com/images/spark-line-5.jpg)

Bar為堆疊長條圖，交替兩個顏色一個疊著一個，max50為上限值，也就是當值疊加到50時會填滿那一欄．

## 長條圖

sparkline(H1, {"charttype","bar"; "max", 5})

![google sheet: sparkline bar chart](https://storage.googleapis.com/homuchen.com/images/spark-line-6.jpg)

這裏我們資料只有一個值，也就是H1的1，當值等於max的5時就會填滿整格，常可以用來代表進度，例如值為百分比而max為1

## 直條圖

sparkline(H1:H10, {"charttype","column"})

![google sheet: sparkline column chart](https://storage.googleapis.com/homuchen.com/images/spark-line-7.jpg)

---
title:  "[Google Sheet]我如何製作進度表"
date:   2019-08-14 20:00:00 +0800
author: HoMuChen
tags: [google sheet, sparkline]
category: Google Sheet
---

追蹤每項任務到目前為止的進度，或每段時間(每天、每個禮拜、或每個月)的努力情況

![google sheet chart]({{site.cdn_url}}/track-progress-1.jpg)

首先先把任務跟時間輸入進去，如下圖:

![google sheet chart]({{site.cdn_url}}/track-progress-2.jpg)

1. 時間只要輸入兩格就可以了，點住右下角的小藍點往右拉，就會補上一樣間距的時間，也就是說那兩格如果是差一天，之後每一格都會差一天，一個禮拜、一個月亦然．

2. 代表每項任務需要完成的單位，簡單用數字量化表示，比如一堂課有10週的課程，就輸入10．

   ![google sheet chart]({{site.cdn_url}}/track-progress-3.jpg)

3. 每個時段，完成某個任務多少單位，就填在這個地方．

4. C4那格裡的公式是=sum(D4:Z4)/B4，就是簡單地將同個任務右邊的每個時段完成的單位(D4:Z4)加起來，再除以Total Unit(B4)，做完後往下拉，每個任務的progress就都有了．

   ![google sheet chart]({{site.cdn_url}}/track-progress-4.jpg)

5. C4=SPARKLINE(SUM(D4:Z4)/B4,{“charttype”,”bar”;”max”,1}) ，這裡使用了SPARKLINE這個函式，將(4)所計算出來的值丟進去第一個參數，第二個參數{“charttype”,”bar”;”max”,1}代表著我們要的是柱狀圖，且最大值為1，因為進度是一個0–1的數字．

   ![google sheet chart]({{site.cdn_url}}/track-progress-5.jpg)

6. 增加一列Total，將每個任務的Total unit，progress及每周的進度都加總起來，以此為例B11 = SUM(B4:B10)，然後再往右拉，應用到每一格上．

7. 製作每時間區間進度條，只是將上述第6步驟的值視覺化:

   1. 先將日期上面的格子全部合併成一格，將D1:N1選起來，從格式 → 合併儲存格 → 全部合併

      ![google sheet chart]({{site.cdn_url}}/track-progress-6.jpg)

   2. 這一格 =SPARKLINE(D11:N11, {“charttype”,”column”})，ㄧ樣使用SPARKLINE函式，如果想要一條線就=SPARKLINE(D11:N11)就好，看起來就像這樣

      ![google sheet chart]({{site.cdn_url}}/track-progress-7.jpg)

大功告成～～🎉🎉🎉

# Referece

* [**[Google Sheet]Sparkline，在儲存格裡插入迷你圖表**](/posts/google-sheet-sparkline/)

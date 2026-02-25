---
layout: post
title:  "如何使用Notion打造Kanban based的待辦清單"
date: 2022-06-04 00:02:00 +0800
author: HoMuChen
category: 生活
tags: [notion, productivity, kanban]
image:
  path: https://storage.googleapis.com/homuchen.com/images/notion-kanban-0.jpg
description: |
  待辦清單系統應該具有哪些原則，什麼是Kanban，
  以及我如何使用Notion，來打造自己的Kanban based的待辦清單系統
---

待辦清單的首要任務是幫助我們整理心智，在眾多的選擇中，優先認出當下最該先執行的事項，
而不會被一堆的事項搞到非常憂慮，什麼都想做卻什麼都做不好，甚至是都沒有開始做。

這篇文章將簡單分享我認為**待辦清單系統應該具有哪些原則**，什麼是**Kanban**，
以及我如何使用**Notion**，來打造自己的Kanban based的待辦清單系統，Let's go！

![notion kanban todo list system]({{site.cdn_url}}/notion-kanban-0.jpg){:loading="lazy"}

# 三大待辦清單原則
市面上的待辦事項系統玲瑯滿目，有沒有一些基本的原則是我們可以把握的呢？以下為大家簡單總結出三項原則：

* **要有截止日期:**
  沒有截止日期，沒有急迫性，大家就是會拖，懶就是人的天性，我想不用多說什麼，大家應該多少都能感同身受吧😂

* **清單不能太長:**
  選項太多也會導致不知道要選哪一項任務來進行，也就是**決策癱瘓**，就算費力地做了選擇，也會導致**決策疲勞**，
  耗費了許多能量在決策上。

* **與目標連結:**
  要知道**為什麼**要做每項任務，它必須可以幫助你達成某項目標，否則做了很多事，很可能只是在瞎忙。

![todo list system principles]({{site.cdn_url}}/book-note-to-do-3.jpg){:loading="lazy"}

關於待辦清單的原則，想看更詳盡的解釋，可以參考我之前寫過的一篇文章: 

[**掌握這3個原則，打造出最適合自己的代辦清單系統**](/posts/book-note-todo-list-formula/){:target="_blank"}

# Kanban是什麼
Kanban緣起於Toyota的生產管理系統，看起來就像是下圖這樣:

![看板系統]({{site.cdn_url}}/book-note-to-do-5.jpg){:loading="lazy"}

主要組成有**欄(column)**、**列**、**卡片(card)**、**WIP limit**，每張卡片即是一項任務，
可以將相關的任務放在同一欄，也可以使用顏色分類，並在每一列區分出**未開始**、**進行中**及**完成**，
而進行中的任務數量會有一個上限，也就是WIP limit(Work in Progress Limit)。

## 組成
* **Cards**: 每一張卡片即代表一個任務事項。
* **Columns**: Kanban最明顯的特徵就是有著不同狀態的直欄: **未開始**、**進行中**及**完成**，
  藉著將卡片移動來移動去以及視覺化，能夠對當前的進度及狀態一目瞭然。
* **WIP limit**: 而對於進行中的那一欄，有一個卡片的數量上限限制，可以避免我們任務越積越多，
  並且首先專注於最重要的幾件事上。

## 好處
* **視覺化**: 對於所以進行中及未開始的能夠一目瞭然，如果是一個團隊，
  成員間也能迅速地同步所有任務事項的狀態。
* **決定優先事項**: 每個當下只需專注於進行中的事項，把他們做完之前，不需要擔心其他的事，
  可以減少心智負擔，也不用擔心是否會忘掉其他任務，因為你有把它們寫在未開始的那欄。

# 使用Notion來實作
最後也是最重要的，將利用Notion這套軟體，來打造自己的Kanban，
並且可以符合上述說的三個原則: **有截止日期**、**不能太長**、**與目標連結**。

原本的Kanban系統因為有WIP limit的關係，有符合清單不能太長的原則，
但缺少了截止日期及與特定目標連結，
接下來我將一步一步地示範如何利用[**Notion**](https://www.notion.so/){:target="_blank"}，
來完善我們Kanban待辦清單系統！

## 建立表格
首先第一步，新增一個頁面，並且選擇**Table**。
![notion: create a table]({{site.cdn_url}}/notion-kanban-1.jpg){:loading="lazy"}

接著系統會要你選擇資料來源，這邊就選**New database**。
![notion: create a table]({{site.cdn_url}}/notion-kanban-2.jpg){:loading="lazy"}

## 新增欄位
現在需要來定義我們的資料庫裡需要的欄位了，這邊我們是會需要名稱、任務狀態、截至日期、目標或專案。
![notion: create columns]({{site.cdn_url}}/notion-kanban-3.jpg){:loading="lazy"}

1. 狀態(Status): 為一個單選欄，主要的狀態就分為未開始、進行中、已完成，可以取用自己喜歡的名字，
   也可以有更多的狀態，這邊最主要的目的就是區分出進行中的任務。

2. 目標或專案(Project): 每個任務會有附屬於一個目標或是專案之下，記錄下來，可以知道為什麼要做這個任務，
   當事項太多時，也可以利用這個欄位來做篩選。

3. 截止日期或時間區間(Deadline): 加上截止日期，為自己增加急迫性，否則就很容易一拖再拖，
   後續也會利用這個欄位來建立timeline的視覺畫圖表，有利於我們使用截止日期來決定哪些任務應該趕快開始進行。

## 新增Board view
建立好資料後，就可以使用board view的功能，按照下圖的步驟，來使得系統像一個看板拉！
![notion: add board view]({{site.cdn_url}}/notion-kanban-4.jpg){:loading="lazy"}

完成後，就可以在板上將任務拖拉移動來更改狀態，可以依照個人習慣的不同，每天或每個禮拜，
決定好要先專注於哪些任務。

## 新增Timeline view
再新增一個timeline view，步驟如下圖:
![notion: add timeline view]({{site.cdn_url}}/notion-kanban-5.jpg){:loading="lazy"}

可以看到紅線的位置就是當天，有了這張圖表，就可以一目瞭然的看出，
哪些任務已經快可以開始或是截止日期已經逼近了，可以據此來調整你的優先事項唷！

# 總結
今天簡單地分享了好的待辦清單系統應該要具有的原則: 截止日期、不能太長、與目標連結，
也認識了一個常見於敏捷開發團隊的系統: 看板(Kanban)，最後使用了Notion來實作。

祝大家生產力高高，每天都可以順利地往自己的目標邁進！ 掰掰～👋

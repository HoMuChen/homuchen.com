---
title:  "[Google sheet]如何建立下拉選單，以及從既有資料中自動建立選項"
date:   2021-06-26 20:00:00 +0800
author: HoMuChen
category: Google Sheet
tags: [google sheet]
---

# 為什麼要用下拉式選單

* 新增資料更為快速，無需重複填寫
* 避免誤植，或統一資料的格式及規則
* 對既有資料鐘進行選擇及後續操作

# 如何建立下拉式選單

## 自行輸入清單選項

1. 首先選擇一個或多個你想要建立選單的儲存格
2. 點選 **資料** -> **資料驗證**
   ![data validation: tool bar](https://storage.googleapis.com/homuchen.com/images/drop-down-1.jpg)
3. 在**條件**選項中，選取**項目清單**
   ![data validation: List of items](https://storage.googleapis.com/homuchen.com/images/drop-down-2.jpg)
4. 輸入你想要的選項，選項間以逗號隔開
   ![data validation: List of items](https://storage.googleapis.com/homuchen.com/images/drop-down-3.jpg)
5. 就大功告成拉
   ![drop down menu](https://storage.googleapis.com/homuchen.com/images/drop-down-4.jpg)

## 從既有資料來建立選項

有時你想要建立一個選單，其中的選項是來自某一大筆資料中的某一個欄位，
你不想一筆一筆手動Key，而且你也不想每次資料有變動時，就要重新去更新一次資料驗證，
此時就可以這麼做，以以下的資料為例:

![example data sheet](https://storage.googleapis.com/homuchen.com/images/drop-down-5.jpg)

1. 重複自行輸入清單選項中的第一及第二部
2. 在**條件**選項中，選取**範圍內的清單**
   ![data validation: List from a range](https://storage.googleapis.com/homuchen.com/images/drop-down-6.jpg)
3. 輸入或選取一個範圍，以這裡的例子為例，我們建立一個國家的下拉選項，填入**F2:F**，代表country那一欄，不包含標頭country本身
4. 大功告成~
   ![drop down menu from a range](https://storage.googleapis.com/homuchen.com/images/drop-down-7.jpg)

# Summary

建立一個下拉選單，選項可以自行輸入，也可以從既有資料的範圍中建立，如此一來當資料有變動時，下拉選單的選項就可以自動更新，而不需要自己再重新輸入新的選項!

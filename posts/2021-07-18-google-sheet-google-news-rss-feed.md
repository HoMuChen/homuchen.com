---
layout: post
title:  "[Google sheet]如何在試算表裡匯入新聞、rss feed"
date:   2021-07-18 12:00:00 +0800
author: HoMuChen
category: Google Sheet
tags: [google sheet, finance]
---

此篇文章將分享我是如何在試算表裡查看新聞，看起來像是下面這樣:

於左上角輸入公司名稱(此處是下拉選單)，即可跑出公司的相關新聞

![google sheet: import google news]({{site.cdn_url}}/google-sheet-news-1.jpg)

在這一篇[**[Google sheet]我如何製作股票損益表，自動抓取最新股價**](/posts/google-sheet-stock-income-statement/){:target="_blank"}裡，
我們已經建立了持有股票清單，我就想說如果同時可以同時看到每一間公司的相關新聞應該不錯，所以才會有了這篇．

# 公式

**=IMPORTFEED(CONCATENATE("https://news.google.com/atom/search?q=", A1, "&hl=zh-TW&gl=TW&ceid=TW:zh-Hant&sort=rated"), "items", false, 150)**

以上公式會使用**A1**儲存格的字去google news查詢，列出150項結果，以下將分別說明各個函式的用法.

# IMPORTFEED

IMPORTFEED爲要匯入新聞RSS Feed的函式，有四個參數，用法為: **IMPORTFEED(網址, [查詢], [標題], [項數])**

* 網址

  此處我們使用的網址為

  https://news.google.com/atom/search?q=**台積電**&hl=zh-TW&gl=TW&ceid=TW:zh-Hant&sort=rated

  改變q=後面的字，就是想要查詢的關鍵字

* 查詢

  第二個參數，可以為下列這些:
  * feed: 只傳回單一列資料
  * feed \<type\>: 可以指定傳回的特定屬性，可能是title、url、author、summary

    舉例: IMPORTFEED(A1, "feed url")
  * items: 此為預設，傳回整個表格，
  * items \<type\>: 一樣可以指定特定屬性，

    舉例: IMPORTFEED(A1, "items title", FALSE, 100)

* 標題

  是否要納入標題欄，預設為FALSE

  舉例: IMPORTFEED(A1, "items", TRUE)

* 項數

  當查詢(第二個參數)爲項目(items)時，代表要傳回的項目數

  舉例: IMPORTFEED(A1, "items", TRUE, 200)

# CONCATENATE

就是把所有的參數串起來，例如=CONCATENATE("123", "456")，就會相當於"123456"．

也能使用儲存格當作參數，這裡的例子就是:

=CONCATENATE("https://news.google.com/atom/search?q=", A1, "&hl=zh-TW&gl=TW&ceid=TW:zh-Hant&sort=rated")，

當A1為台積電時，

就會相當於"https://news.google.com/atom/search?q=台積電&hl=zh-TW&gl=TW&ceid=TW:zh-Hant&sort=rated"

# Summary

利用以上兩個公式，可能成功在試算表上看新聞囉～ 🎉，掰掰～👋

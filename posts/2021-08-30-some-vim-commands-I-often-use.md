---
layout: post
title:  "幾個我常用的vim的功能"
date: 2021-08-30 22:00:00 +0800
author: HoMuChen
category: Web Development
tags: [vim, linux]
---

作為一個軟體工程師，我們花在文字編輯器上的時間一定佔了一定的比例，
更精通熟悉我們使用的編輯器的話，開發的效率可以提升很多，今天就來分享一些我蠻常會用到的vim的功能～

# Introduction

Vim是一個modal editor，可以切換在各個模式之間，一開始時是在**normal mode**，今天要介紹的功能，
都是在normal mode下操作的，按`i`或`a`可以進入**insert mode**，按`esc`即可以退回normal mode。

我通常比較常使用`a`，因為當把指標移到最後時，用`a`可以直接在最後面開始輸入。

# Navigation

## 上下左右
最基本的就是`k`、`j`、`h`、`l`分別對應到上下左右

## 翻頁
覺得上下按著這樣太慢，可以用`Ctrl-U`、`Ctrl-D`來上下翻頁

## 行首、行末
`0`指標會跳掉當行的最前面，`$`則是最後面。

## 字的跳躍
`w`可以跳到下一個字的開頭，`e`則是跳到下一個字的結尾，`b`則是往前跳到前一個字的開頭。

## () [] {} 跳躍
指標找到了一對括號的其中一個，想要到另一個的話可以用`%`。

## 搜尋跳躍
將指標放在字上，按`#`，就會自動幫你搜尋，並跳到相同的字上，效果相當於用`/`搜尋再按`n`。

![vim: #]({{site.cdn_url}}/vim-5.jpg)

# Deletion

## 刪除一個字母
`x`，可以刪除指標上的那個字。

## 刪除一行
`dd`，刪除指標所在的那一行。

## 刪掉指標後的所有字
`D`，常用狀況像是複製了一行method，然後刪掉method name跟paramters再打新的。如下圖反白部分:
![dw]({{site.cdn_url}}/vim-6.jpg)

## d + {navigation key}
搭配上面提到的各種navigation的方法，比如說:

* `dw` : 刪掉一個字，從指標到字的尾端，像是下圖反白的部分。
  ![dw]({{site.cdn_url}}/vim-1.jpg)
* `d%` : 刪掉整個(...)、[...]或{...}

## di

* `diw`：跟`dw`也是刪掉一個字，但是可以刪掉整個字，效果就相當於先按`b`讓指標回到字首再`dw`。
  ![diw]({{site.cdn_url}}/vim-2.jpg)
* `di"` or `di(` or `di[` or `di{`：刪掉""內、()、[]及{}的所有字。

  `di(` or `di)`即可刪掉()中function的paramter
  ![di(]({{site.cdn_url}}/vim-3.jpg)

  `di"`則是刪掉雙引號中間的所有字，留下雙引號
  ![di"]({{site.cdn_url}}/vim-4.jpg)

## da
`da`的話跟上述`di`都ㄧ樣，只不過會將引號或括號都一併刪除。

## d 換成 c
將上面的`d`都換成`c`，可以有一樣的功能，差別就是會直接進入**insert mode**，所以可以省去一個按`i`的時間。
如`cw`、`ciw`、`ci"`、`ca(`。

# Copy and Paste

## 複製一行
`yy`複製一行，`p`貼上

## y + {navigation key}
`y`一樣可以搭配上面提到的navigation key來複製

* `yw`，`yiw`: 複製一個字
* `yi"`: 複製雙引號內的字
* `y%`: 複製成對括號內的字


稍微簡單地紀錄一下及分享，希望能有幫助～～ 掰掰～👋

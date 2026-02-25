---
layout: post
title:  "如何在Mac OS中使用command line來將文字複製到剪貼簿"
date: 2022-03-28 20:40:00 +0800
author: HoMuChen
category: Web Development
tags: [command line]
---

在Mac OS裡，該如何使用command line的指令來將你想要的資料複製到剪貼簿呢？
那就是可以透過**pbcopy**及**pbpaste**指令，也下為一些例子。

# 複製
* 複製`123`
  ```sh
  echo 123 | pbcopy
  ```

* 將`words.txt`檔案中的文字，複製到剪貼簿
  ```sh
  cat words.txt | pbcopy
  ```

  或是

  ```sh
  pbcopy < words.txt
  ```

# 貼上
* 輸出至stdout
```sh
pbpaste
```

* 輸出到檔案裡
```sh
pbpaste > some.txt
```

雖然也可以用滑鼠把想複製的字選起來再按command + C，但有時候就是不想碰到滑鼠！我想這就是工程師的浪漫吧😎

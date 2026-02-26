---
title:  "[Golang] Common verbs of formatting string"
date: 2021-09-20 15:30:00 +0800
author: HoMuChen
category: Web Development
tags: [golang, formatting]
---

在fmt package裡Printf, Fprintf, Fscanf, Scanf，或像是log package裡的Printf, Fatalf，
只要是function名字後面有f的，就能format你的input，以fmt.Printf為例:
```go
fmt.Printf("My name is %s. I am %d years old", "HoMuChen", 30)

//My name is HoMuChen. I am 30 years old
```
第一個參數將會是最後輸出的字串，不過中間我們可以看到`%s`、`%d`的東西，稱之為**verb**，
verb會被後面的參數取代掉，並且是依照你指定的格式，這篇文章將會分享一寫常用的verb。

# Overview
以下為一個常用的verbs表格，依照要format的值的型態做分類，後面再詳細說明:

category | syntax  | description
:--------| :-------| :------- 
general            | %v      | value in default format
                   | %T      | type
                   | %%      | literal % sign
boolean            | %t      | true or false
interger           | %b      | binary
                   | %o      | base 8
                   | %d      | base 10
                   | %x      | base 16
                   | %X      | base 16 with upper-case letters
floating           | %e      | scientific notation
                   | %f      | decimal point but no exponent
                   | %g      | for large exponents
string             | %s      | string
                   | %q      | double quoted string
padding            | %10s    | width 10 string
                   | %-10s   | width 10 string left padding
                   | %10d    | width 10 digit
                   | %010d   | width 10 digit filled with 0
floating precision | %8f     | width 8 floating number
                   | %8.2f   | width 8 with 2 digit presicion floating number
                   | %.2f    | 2 digit presicion floating number

# General

* `%v`: 根據不同的值的型態，預設的格式

  type     | format
  -------  | :-------
  boolean  | %t
  string   | %s
  int      | %d
  float32,float64  | %g

* `%T`: 值的型態
  ```go
  fmt.Printf("The type of this value is %T", "I am a string")
  //The type of this value is string

  fmt.Printf("The type of this value is %T", true)
  //The type of this value is bool
  ```

* `%%`: 真的想要%的時候
  ```go
  fmt.Printf("%v %%", 100)
  //100 %
  ```

# Boolean
* `%t`:
  ```go
  fmt.Printf("This is %t", true)
  ```

# Integer
* `%b` `%d` `%x`: base 2, 10, 16
  ```go
  fmt.Printf("base 2: %b, base 10: %d, base 16: %x", 255, 255, 255)
  //base 2: 11111111, base 10: 255, base 16: ff
  ``` 

# Floating point number
* `%e`: 科學記號表示

* `%f`: 十進位表示，預設顯示到小數點後六位。
  ```go
  fmt.Printf("%f", 123.123456789)
  //123.123457
  ``` 

* `%g`: 小數點後很多位的話，用`%g`全部顯示出來。
  ```go
  fmt.Printf("%g", 123.123456789)
  //123.123456789
  ``` 

# String
* `%s`: 就是字串～

* `%q`: 以雙引號括起來的字串，就不需要再額外寫類似`\"`escape掉。
  ```go
  fmt.Printf("%q", "I am a string")
  //"I am a string"
  ``` 

# Padding
有時我們想要輸出的字串是一樣長度的，可以在前面加上一個數字，代表你想要長度，以下例子:

* `%10s`: 寬度為10的字串
  ```go
  users := []string{"David", "Mu", "HoMuChen", "Noname"}
  for _, user := range users {
          fmt.Printf("User: %10s does something\n", user)
  }
  ```
  ```text
  User:      David does something
  User:         Mu does something
  User:   HoMuChen does something
  User:     Noname does something
  ```

* `%-10s`: 寬度為10的字串，左邊對齊
  ```go
  users := []string{"David", "Mu", "HoMuChen", "Noname"}
  for _, user := range users {
          fmt.Printf("User: %-10s does something\n", user)
  }
  ```
  ```text
  User: David      does something
  User: Mu         does something
  User: HoMuChen   does something
  User: Noname     does something
  ```

* `%-7d`: 寬度為7的整數，左邊對齊
  ```go
  contentLengths := []int{70, 240, 614, 12345}
  for _, contentLength := range contentLengths {
          fmt.Printf("content length: %-7d bytes\n", contentLength)
  }
  ```
  ```text
  content length: 70      bytes
  content length: 240     bytes
  content length: 614     bytes
  content length: 12345   bytes
  ```

# Floating point number precision
也可以指定浮點數的總長度及小數點後要到第幾位。

* `%10f`: 總長度為10的浮點數，小數點後預設為6位，如果需要超過長度10才能表示，還是會超過。
  ```go
  fmt.Printf("response time: %10f ms\n", 25.35)
  fmt.Printf("response time: %10f ms\n", 125.35)
  fmt.Printf("response time: %10f ms\n", 2125.11)
  ```
  ```text
  response time:  25.350000 ms
  response time: 125.350000 ms
  response time: 2125.110000 ms //長度超過9了
  ```
* `%.2f`: 指定小數點後到第2位。
  ```go
  fmt.Printf("response time: %.2f ms\n", 25.35123)
  // response time: 25.35 ms
  ```
* `%10.2f`: 總長度為10，且只小數點後兩位
  ```go
  fmt.Printf("response time: %10.2f ms\n", 25.35)
  fmt.Printf("response time: %10.2f ms\n", 125.35)
  fmt.Printf("response time: %10.2f ms\n", 2125.11)
  ```
  ```text
  response time:      25.35 ms
  response time:     125.35 ms
  response time:    2125.11 ms
  ```

# Summary
在這篇文章記錄了常用的verbs，除了自己忘記可以回來看，也希望能幫助到有需要的人，掰掰～👋

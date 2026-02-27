---
title:  "[Golang] 如何逐行讀取檔案，或使用shell pipe到go process"
date: 2021-11-05 13:00:00 +0800
author: HoMuChen
category: Web Development
tags: [golang, linux]
---

這篇將示範如何用go的bufio，開啟檔案並且一行一行地讀取資料，
最後示範直接用unix pipe將資料pipe給我們的go程式，做到像下面這樣的事:
```sh
cat words.txt | go run ./wc.go
```

## bufio.Scanner
我們將使用`bufio.Scanner`來一行一行地讀取檔案內容，先看看會用到的function們的signature:
* func NewScanner(r io.Reader) *Scanner
* func (s *Scanner) Scan() bool
* func (s \*Scanner) Text() string

bufio之所以叫做bufio，就是因為他在io的基礎上，加上了buffer，
這邊我們使用的`bufio.Scanner`，一樣是從`io.Reader`裡Read資料出來，但會先將資料存在他的buffer裡面，
呼叫`Text()`可以拿到資料，呼叫`Scan()`則是叫他繼續讀取下一筆資料。

預設上，每一次Scan就是讀取一行，如果回傳值為`false`就代表已經沒有資料了，
除了一次讀取一行之外，還有其他的方式，但今天這裡就不介紹了～

## 範例程式
以下示範讀取一個檔案(words.txt)，算出每一行的字出現幾次，並將結果打印至螢幕上:

`words.txt: `
```txt
apple
banana
orange
apple
apple
orange
```
`wc.go:`
```go
package main

import (
        "bufio"
        "fmt"
        "io"
        "log"
        "os"
)

func main() {
        file, err := os.Open("./words.txt")
        if err != nil {
                log.Fatalf("error when reading file with message: %v", err)
        }

        wc(file)
}

func wc(input io.Reader) {
        scanner := bufio.NewScanner(input)

        count := make(map[string]int)
        for scanner.Scan() {
                word := scanner.Text()

                if _, ok := count[word]; ok {
                        count[word] += 1
                } else {
                        count[word] = 1
                }
        }

        for word, n := range count {
                fmt.Printf("%s: %d\n", word, n)
        }
}
```

## Shell Pipe
既然我們已經可以從檔案中一行一行讀取資料了，那要不要試試看這樣！
利用shell pipe從上一個程式的stdout中讀取資料。

```sh
cat words.txt | go run ./wc.go
```

想要達成上面的用法，相當簡單，只要把我們wc function的參數，從使用***os.File**改成**os.Stdin**就行了～
因為他們都有implement `io.Reader`，也就是main function變成如下:
```go
func main() {
        wc(os.Stdin)
}
```

## Separate IO from Logic
前面我們將wc算完的結果，直接`fmt.Printf`到stdout上，但有時如果我們想寫到檔案裡，
或是寫到network socket時，就不太方便。

`wc`應該只專注在word count一件事上就好，
不需要管input是從哪裡來的，就像前面我們使用`*os.File`後面用`os.Stdin`一樣，
也不用管output要寫到哪裡去，所以我們再將程式改寫如下:
```go
import (
        "os"
        "fmt"
        "io"
        "bufio"
)

func main() {
        wc(os.Stdin, os.Stdout)
}

func wc(input io.Reader, output io.Writer) {
        scanner := bufio.NewScanner(input)

        count := make(map[string]int)
        for scanner.Scan() {
                word := scanner.Text()

                if _, ok := count[word]; ok {
                        count[word] += 1
                } else {
                        count[word] = 1
                }
        }

        for word, n := range count {
                fmt.Fprintf(output, "%s: %d\n", word, n)
        }
}
```
`wc`就只管將結果寫到一個可以寫的地方，至於它是什麼地方，就由呼叫他的人來決定！

By the way, `wc`這名字取的不好，因為我們實現的是`uniq -c`這個command，而不是`wc`😄

## Summary
感謝你的閱讀～ 今天學到了如何使用bufio.Scanner來一行一行地讀取檔案，另外也體會到了interface的強大，
io.Reader及io.Writer是個很好的例子，並且利用`os.Stdin`就可以使用shell pipe ( | )，
跟其他linux command一起搭配完成任務！

最後，我也有寫一篇一樣功能的Node.js版本，有興趣的可以看一看:

[**Nodejs: 如何逐行讀取檔案，或使用Unix pipe與其他process互動**](/posts/nodejs-how-to-read-from-file-line-by-line-and-use-shell-pipe-with-nodejs-process/)

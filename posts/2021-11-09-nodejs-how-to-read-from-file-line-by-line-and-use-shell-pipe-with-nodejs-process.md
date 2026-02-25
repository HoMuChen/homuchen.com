---
layout: post
title:  "Nodejs: 如何逐行讀取檔案，或使用Unix pipe與其他process互動"
date: 2021-11-09 10:00:00 +0800
author: HoMuChen
category: Web Development
tags: [node.js, linux]
---

這篇文章將介紹如何使用Nodejs的`readline` module來一行一行地讀取檔案，
接著既然都可以從檔案中逐行讀取了，那也可以從standard input中逐行讀取吧，
如此一來，就可以跟其他linux command一樣，一起使用pipe！像下面這樣: 

```sh
cat words.txt | node wc.js
```

# readline
* **createInterface:**  
  首先使用`readline.createInterface()`，需要一個input參數，他需要是一個`stream.Readable`，
  這裡我們使用`fs.createReadStream()`打開我們的檔案，並作為input，傳給createInterface。

  ```javascript
  const readline = require('readline');
  const fs = require('fs');

  const rl = readline.createInterface({
    input: fs.createReadStream('./words.txt'),
  });
  ```
* **Event: "line"**  
  接著就可以監聽`line` event，每當從input讀取到換行(`\r`、`\n` or `\r\n`)，line event就會被發送。
  callback function有一個參數，它是個字串。
  ```javascript
  rl.on('line', (row) => console.log(row));
  ```
* **Event: "close"**  
  當input stream結束的時候，`close` event就會被發送。
  ```javascript
  rl.on('close', doSomething);
  ```

## 完整程式碼
最後我們就利用上面的資訊，寫一隻`wc.js`，來計算檔案中每個字出現的次數，將結果以JSON的格式輸出至stdout上。

```javascript
const readline = require('readline');
const fs = require('fs');

const input = fs.createReadStream('./words.txt');

const rl = readline.createInterface({ input });
const count = {}

rl.on('line', row => {
  count[row] = (count[row] || 0) + 1
})
rl.on('close', () => console.log(JSON.stringify(count)))
```

# unix pipe
這邊示範如何從stdin中讀取資料流，就可以使用shell pipe ( | )，讀取來自前一個程式的output了。

只需將**`readline.createInterface`**的input參數，從**`fs.createReadStream('./words.txt')`**改成
**`process.stdin`**就行了！因為他們都是`stream.Readable`的implementation。

```javascript
const readline = require('readline');

//只改了這行
const input = process.stdin;

const rl = readline.createInterface({ input });
const count = {}

rl.on('line', row => {
  count[row] = (count[row] || 0) + 1
})
rl.on('close', () => console.log(JSON.stringify(count)))
```

# summary
感謝你的閱讀～ 這篇文章示範了如何使用`readline`模組來逐行讀取檔案，
並且看到了兩個`stream.Readable`的實例，體會到了stream的好用之處。

另外我還有寫過另一篇一樣功能，只不過是用golang寫的，`stream.Readable`可以類比為golang中的`io.Reader`
，有興趣的可以看看:

[**[Golang] 如何逐行讀取檔案，或使用shell pipe到go process**](/posts/golang-how-to-read-from-file-line-by-line-and-use-shell-pipe-with-go-process/){:target="_blank"}

其他stream的實例:

[**How to stream data from Blob Storage at your HTTP server using Azure and express.js**](/posts/how-to-stream-data-from-blob-storage-at-http-server-using-azure-and-express/){:target="_blank"}

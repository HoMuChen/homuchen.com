---
layout: post
title:  "How to stream data from Blob Storage at your HTTP server using Azure and express.js"
date: 2021-08-13 23:30:00 +0800
author: HoMuChen
category: Web Development
tags: [express, node.js, http, api]
last_modified_at: 2021-11-09 15:03:00 +0800
---

這篇文章將會示範如何使用Node.js來下載Azure Blob Storage上的檔案，並且使用Stream的方式，
將檔案儲存到本地端，或是作為一個Server(此篇使用express.js)，回傳給你的client，並且根據檔案名稱來設置正確的Content-Type．

# Download file from Azure
## 取得file的Readable Stream
```js
const { ShareServiceClient, StorageSharedKeyCredential } = require("@azure/storage-file-share");

const ACCOUNT = 'your storage account';
const ACCOUNT_KEY = 'your account secret';

const credential = new StorageSharedKeyCredential(ACCOUNT, ACCOUNT_KEY);
const serviceClient = new ShareServiceClient(
  `https://${ACCOUNT}.file.core.windows.net`,
  credential
);

//下載data share裡的d4ba71bf-3d38-4e69-9ba2-be4c04179e43.csv
const fileClient = serviceClient
  .getShareClient("data")
  .rootDirectoryClient.getFileClient("d4ba71bf-3d38-4e69-9ba2-be4c04179e43.csv");
const downloadFileResponse = await fileClient.download();

//downloadFileResponse.readableStreamBody  ---->> Readable Stream在這裡拉
```
這邊使用套件`@azure/storage-file-share`的幫助，連接上的你的Azure帳戶及share檔案，
可以拿到該檔案的readable stream。

# Write to local file or socket
## 把檔案寫入到本地的檔案
使用fs.createWriteStream(path)建立一個file的Writable stream，再將Readable Stream pipe到那裡．

```js
const fs = require('fs')

const filename = "local.csv"

downloadFileResponse.readableStreamBody.pipe(fs.creatWriteStream(filname))
```

## 把檔案傳到HTTP Response (express.js)
express的handler裡的第二個參數response物件，也是一個writble stream，可以直接將資料pipe過去．

```fs
app.get('/path', (req, res) => {
  downloadFileResponse.readableStreamBody.pipe(res)
})
```

# Content-Type
使用套件mime-types，可以從想要下載的資料的檔案名中取得MIME type，從而設置到HTTP Response的Content-Type header裡．

```js
const mimeTypes = require('mime-types');

const filename = "test.csv";
const mimetype = mimeTypes.lookup(filename);

console.log(mimetype)  //text/csv
```

# Summary
最後將以上結合起來，完整的代碼如下:

<script src="https://gist.github.com/HoMuChen/4b5d8ddd98d1cd9547d2315e0f51d3e1.js"></script>

跑起來之後，就能透過GET http://localhost:3000/share/filename.csv這樣之類的網址來下載檔案囉～～

# 延伸閱讀
這篇文章中可以看到到許多Node.js Stream的實例，像是express.js的`request`、`response` object，
其他還有像是`process.stdin`，`process.stdout`，想看更多使用stream的例子，可以看我寫過的其他文章:

* [**Nodejs: 如何逐行讀取檔案，或使用Unix pipe與其他process互動**](/posts/nodejs-how-to-read-from-file-line-by-line-and-use-shell-pipe-with-nodejs-process/)

# 參考資料

* [Node.js documentation: Stream](https://nodejs.org/api/stream.html)
* [@azure/storage-file-share](https://www.npmjs.com/package/@azure/storage-file-share)

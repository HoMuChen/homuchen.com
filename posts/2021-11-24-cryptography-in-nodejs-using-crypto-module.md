---
title:  "Node.js: 7 cryptography concepts using ctypto module"
date: 2021-11-24 22:11:00 +0800
author: HoMuChen
category: Web Development
tags: [crypto, node.js]
image:
  path: https://storage.googleapis.com/homuchen.com/images/nodejs-crytpo-0.jpg
---

這篇要介紹nodejs中的crypto module的用法，如何使用這個module來實現密碼學中常見的概念，
包含**hash**、**salt**、**password hashing**、
**MAC(message authentication code)**、
**Symmetric Encryption**及**Asymmetric Encryption**
及**Digital Signature**。

![cryptography in node.js cryto module]({{ site.cdn_url }}/nodejs-crytpo-1.jpg)

# Hash
可以使用指令`openssl list -digest-algorithms`來查詢可用的algorithms，以下使用`sha256`為例，
並輸出`base64`的字串。

```javascript
const { createHash } = require('crypto');

function hash(input) {
    return createHash('sha256').update(input).digest('base64');
}
```

# Salt
randomBytes可以幫我們隨機產生你所想要長度的隨機亂數，用來作為salt，
它的回傳值是一個Buffer。

```javascript
const { randomBytes } = require('crypto');

function salt(len) {
    return randomBytes(len).toString('hex')
}

```

# Password hashing
利用`scrypt`及`scryptSync`這個KDF(一個為非同步，一個為同步的API)，
function的前三個參數分別為:
1. 欲hash的明文資料，此處為密碼
2. salt
3. output的長度

```javascript
const { scryptSync, randomBytes } = require('crypto');

function passwordHash(password) {
    const salt = randomBytes(16).toString('hex');
    const hashedPassword = scryptSync(password, salt, 32).toString('hex');

    return `${salt}:${hashedPassword}`
}
```
以上例子使用`randomBytes`來產生salt，接著將密碼與salt一起hash成32 bytes的hash value，最後跟salt一起回傳。

# MAC
跟hash一樣可以使用指令`openssl list -digest-algorithms`來查詢可用的演算法。
```javascript
const { createHmac } = require('crypto');

const key = 'my-secret!';
const message = 'foo bar👻';

const hmac = createHmac('sha256', key).update(message).digest('hex');
```

# Symmetric Encryption
支援的對稱式加密的演算法一樣可以透過這個指令來取得`openssl list -cipher-algorithms`，此處使用`aes256`。
```javascript
const { randomBytes, createCipheriv, createDecipheriv } = require('crypto');

const message = 'This is the message I wanna deliver';
const key = 'key shared between two parties';
const iv = randomBytes(16);

//Encrypt
const cipher = createCipheriv('aes256', key, iv);
const encryptedMessage = cipher.update(message, 'utf8', 'hex') + cipher.final('hex');

//Decrypt
const decipher = createDecipheriv('aes256', key, iv);
const decryptedMessage = decipher.update(encryptedMessage, 'hex', 'utf-8') + decipher.final('utf8');
```

# Asymmetric Encryption
首先使用`generateKeyPair`或`generateKeyPairSync`來產生公鑰及私鑰。

```javascript
const { generateKeyPairSync } = require('crypto');

const { publicKey, privateKey } = generateKeyPairSync('rsa', {
    modulusLength: 4096,
    publicKeyEncoding: {
        type: 'spki',
        format: 'pem'
    },
    privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
        cipher: 'aes-256-cbc',
        passphrase: 'top secret'
    }
})
```

接者使用`publicEncrypt`及`privateDecrypt`來encrypt、decrypt message。
```javascript
const {  publicEncrypt, privateDecrypt } = require('crypto');

const message = "I am the message to be encypted🥳"

//加密 Encrypt
const encryptedData = publicEncrypt(publicKey, Buffer.from(message));

//解密 Decrypt
const decryptedData = privateDecrypt(privateKey, encryptedData);
```

# Digital Signature
數位簽章牽扯到hash及非對稱加密，使用crypto module中的`createSign`及`createVerify`，
回傳的`Sign`及`Verify` Object都幫我們做好好囉～

```javascript
const { createSign, createVerify } = require('crypto');

//取得你的公私鑰匙
const publicKey = require('./ssl/key.pem')
const privateKey = require('./ssl/cert.pem');

const message = 'this data must be signed';

//使用私鑰sign
const signer = createSign('rsa-sha256');
signer.update(message);
const signature = signer.sign(privateKey, 'hex');


// 使用公鑰verify
const verifier = createVerify('rsa-sha256');
verifier.update(message);
const isVerified = verifier.verify(publicKey, signature, 'hex');
```

# Summay
其實就是從官方document裡，把比較常用的整理到這裡，這篇就只有紀錄在Nodejs裡如何實作，
並沒有討論為何需要上述的每一個東西，以及有何用途，有機會再陸續補上～ 掰掰👋

# 參考資料
* [**Crypto \| Node.js Documentation**](https://nodejs.org/api/crypto.html)

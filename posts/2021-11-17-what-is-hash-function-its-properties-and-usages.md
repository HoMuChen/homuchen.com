---
title:  "什麼是Hash Function? 有什麼特性及用途?"
date: 2021-11-17 17:52:00 +0800
author: HoMuChen
category: Web Development
tags: [crypto]
image:
  path: https://storage.googleapis.com/homuchen.com/images/hash-function-0.jpg
description: |
  除了了解hash function是什麼及其特性之外，用更生活化的方式來展現這些特性，以及以有趣的應用來更加地熟悉hash function。
---

在之前一篇文章: [**密碼學是什麼? 有何用途以及要解決什麼樣的問題?**](/posts/what-problems-cryptography-to-solve)
中討論過密碼學的出現是為了解決什麼問題，這篇文章要討論密碼學裡一個重要的概念，
**Hash Function**，其與對稱式加密跟非對稱式加密三者共同構成密碼學裡的核心。

# 賭博遊戲
再開始正式的內容之前，先來想個有趣的問題: **賭博中如何防止莊家出老千?**
比如說我們現在玩骰子遊戲，賭大小，1-3是小，4-6是大，
賭博最怕莊家出老千，莊家看你賭小就作弊讓骰子骰出大，看你賭大就骰小，該如何解決這個問題呢~

這篇文章講Hash那提出的解法當然跟Hash有關囉，文末再來揭曉，首先先來認識Hash function。

# 什麼是Hash Function
Function就是有一組輸入然後會產生一組輸出，同樣的輸入會產生出同樣的輸出，
而hash function的輸出是**固定長度**的，不同的hash funtion，所產出長度都不同，
比如說md5為128個bits，sha256顧名思義為256個bits。

輸出的結果跟輸入的資料相比起來，通常是小很多的，
所以輸出的結果會被稱為**message digest**，或是直接稱為**hash value**。

![hash function]({{site.cdn_url}}/hash-function-0.jpg)

# Hash function的特性
接下來我們來看看好的hash function還具有其他哪些特性，可以使得他在密碼學裡佔有一席之地。

## Irreversibility
不可逆的，單向的，就是說當我們得到一個hash funcition的output時，我們無法反推出其input，

![hash function: irreversibility]({{site.cdn_url}}/hash-function-1.jpg)

## Collision Resistance
什麼是碰撞? 就是說當有兩個不同的輸入，經過hash function的計算後，得到了一樣的結果時，就是碰撞。

比如說我們的hash function是將輸入除以5的餘數，這樣當我們的input是1、6、11、16等等等的時候，
所得到的ouput都是1，就碰撞了。

所以如果一個好的hash function是collision resistance的話，當我們看到兩個不相同的hash value時，
我們就知道他們倆的input也是不相同，反之亦然，當看到兩個相同的hash value時，
我們就知道它是由兩個一樣的input所以計算出來的，因為他不會碰撞，不會有多個input對應到同一個output。

# 用途
Hash Function就是做出**承諾**、**指紋**、**識別**的方法，怎麼說呢？
接下來我們來看看在哪些地方有用到hash function吧!

## 承諾
比如現在要做出愛妻承諾，我們將10條的愛妻守則經過hash function計算的到一個hash value，
這個value就是一個承諾。承諾就是不會改變的東西，如果我們偷偷地更改了愛妻守則裡的其中一個字，
因為改變太微小了，老婆可能不會發現，但只要再經過hash function計算過後，就會發現hash value完全不一樣了～

![hash function: commitment]({{site.cdn_url}}/hash-function-2.jpg)

如此一般，hash value的一致可以用來保障我們原始資料是沒有改變的，可以被用在下列這幾個地方:
* 檔案校正碼
* 下載安裝檔

用來確定我們收到的檔案是沒有損毀的，以及我下載下來要安裝的東西，不是被惡意的第三方給改過的！

## 隱密的承諾
除了是承諾之外，它還可以是隱密的承諾，也就是說我知道你做了一個承諾，
但我不知道你承諾的內容是什麼，因為hash function具有不可逆的特性，
但你可能會說這有什麼用嗎~讓我們來看看吧！

### 密碼儲存
當我們使用密碼登入別人的服務時，伺服器要知道使用者的密碼輸入的對不對，那它就要記錄下大家的密碼，
日後使用者登入的時候才可以比對。不過要是伺服器被駭客侵入，
或透過其他的方式取得這份使用者密碼清單，那代誌就大條了😱

所以通常伺服器資料庫都不會直接把密碼紀錄下來，而是將密碼hash過後，再將hash value存起來，
如此一來就算駭客得到這些hash values，也無法得知原本的密碼是什麼，而每次使用者登入的使用，
只要再將他輸入的密碼hash過一次，然後跟資料庫裡的比對，一樣的話就代表使用者輸入了正確的密碼了，
在這裡這個承諾就是密碼本身。

## 識別
因為hash value是固定長度的，可以將它當作一份資料的識別，比如說身分證字號就是使用一位英文加上九位數字，
來代表著某一位台灣人。

### Git
`commit d9a1e4f5f1fe19b05bafb4176b2c9a6b89c14bc9 (HEAD -> master)`

相信會使用git的大家對這樣的文字不陌生，
其中的`d9a1e4f5f1fe19b05bafb4176b2c9a6b89c14bc9`就是將這個commit版本中的所有檔案作為input，使用SHA1 hash出來的，
長度為160個bits，也就是40個hexadecimal的字母，他就作為這個commit的識別。

### UUID v3、UUID v5
這兩個版本分別使用MD5及SHA1，由於v5使用SHA1會生成160bits的hash value，會將其截斷為128bits。

# 賭博遊戲的解法
現在要來解決文章開頭的問題了～利用的就是hash function的隱密的承諾的特性，提出的解法如下:

玩家可以先將他要下的賭注hash過，得到一串看不懂的東西，然後公開這串hash value，
由於不可逆的特性的關係，莊家看不懂玩家到底是賭大還是賭小，等開出結果之後，
玩家再公布他的賭注，並將此再hash一遍，如果得出的hash value一樣，
玩家就可以宣稱他看到骰子開獎之後才公布的賭注跟原先的賭注是一樣的，酷吧😎

# 總結
感謝你的閱讀～ 這篇文章簡單地介紹了什麼是hash function，以及它具有哪些特性，
還有其用途，包括檔案校正、密碼儲存、git commit、uuid等等...

在密碼學中，還會搭配對稱式及非對稱式加密來達成一些其他的任務，
比如說訊息驗證碼(message authentication code)、數位簽章(digital signature)等等...
後續會再慢慢介紹以上的東西，掰掰～ 👋

---
title: "Hash 是什麼？Hash Function 完整指南：原理、特性、應用 + 2026 該用哪個演算法"
date: 2021-11-17 17:52:00 +0800
author: HoMuChen
category: Web Development
tags: [crypto, hash, security]
image: https://storage.googleapis.com/homuchen.com/images/hash-function-0.jpg
description: "Hash 是什麼？一篇看懂 Hash Function 的 5 個核心特性（不可逆、抗碰撞、確定性、雪崩效應、固定長度）、6 大實際應用（密碼儲存、Git、區塊鏈、IPFS、JWT、檔案校正），以及 2026 該選哪個演算法（SHA-256 / SHA-3 / BLAKE3 / Argon2 完整對照）。"
---

> **2026-05 更新**：原本這篇用「賭博遊戲」介紹 hash 概念，但這幾年讀者最多問的其實是「**那我密碼到底要用 SHA-256 還是 bcrypt？**」、「**MD5 還能用嗎？**」、「**SHA-1 為什麼被棄用？**」這次大改版補上：(1) 2026 hash 演算法選擇指南、(2) 密碼專用 hash（Argon2 / bcrypt）跟一般 hash 的差別 — 這個分不清楚會直接造成資安漏洞、(3) 區塊鏈、IPFS、JWT 等現代應用、(4) 5 個 FAQ。

**Hash function** 是密碼學裡一個重要的概念，跟對稱式加密、非對稱式加密三者構成密碼學核心。這篇會講：

* 用「**賭博遊戲**」直觀理解 hash 概念
* Hash function 的 **5 個核心特性**
* **6 大實際應用**（不只密碼跟 Git）
* 2026 **該用哪個 hash 演算法**（含密碼專用 hash）
* 5 個 **FAQ**

如果還沒看過密碼學的整體介紹，建議先看：[**密碼學是什麼？有何用途以及要解決什麼樣的問題？**](/posts/what-problems-cryptography-to-solve/)

---

## 一句話結論：2026 該用哪個 hash？

| 你的需求 | 選這個 |
|---------|-------|
| 一般檔案校正、commit ID、UUID | **SHA-256**（業界默認） |
| 高效能（大檔案、串流） | **BLAKE3**（比 SHA-256 快 4-10 倍） |
| 學術 / 政府合規 | **SHA-3** |
| **密碼儲存** | **Argon2id**（OWASP 2026 首選）⚠️ 不要用 SHA-256！ |
| 區塊鏈 / Bitcoin | SHA-256（雙雜湊） |
| ❌ **絕對不要用** | MD5、SHA-1（已被破解）|

> ⚠️ **最常見的錯誤**：用 SHA-256 存密碼。SHA-256 是給「資料校驗」設計的，太快了 — 攻擊者可以一秒猜幾十億次。**密碼必須用 Argon2 / bcrypt / scrypt 這種「故意慢」的演算法**。後面會詳解。

---

## 賭博遊戲（暖身概念）

正式開始之前，先想個有趣的問題：**賭博中如何防止莊家出老千？**

我們玩骰子賭大小，1-3 是小，4-6 是大。最怕莊家看你賭小就作弊讓骰子骰大、看你賭大就骰小。怎麼解決？

這篇講 hash，所以解法當然跟 hash 有關。文末再揭曉 — 先來認識 hash function。

---

## 什麼是 Hash Function？

Function = 一組輸入產生一組輸出，**同樣的輸入永遠產生同樣的輸出**（這個特性叫 **Deterministic / 確定性**）。

Hash function 特別的地方：**輸出是固定長度的**，不論你輸入是 1 byte 還是 1 GB：

* MD5 → 128 bits
* SHA-1 → 160 bits
* SHA-256 → 256 bits（顧名思義）
* SHA-3-256 → 256 bits
* BLAKE3 → 預設 256 bits（可變）

輸出通常比輸入小很多，所以叫 **message digest**（訊息摘要），或直接叫 **hash value**。

![hash function](https://storage.googleapis.com/homuchen.com/images/hash-function-0.jpg)

---

## Hash Function 的 5 個核心特性

### 1. Deterministic（確定性）

同樣輸入永遠得到同樣輸出。聽起來廢話，但這是所有應用的基礎 — 沒這個就沒辦法做檔案校驗。

### 2. Fixed Length（固定長度）

無論輸入多大，輸出長度固定。這讓 hash 可以拿來當 ID（UUID、Git commit）。

### 3. Irreversibility（不可逆 / 單向函數）

得到 hash value 後，**無法反推出 input**。

![hash function: irreversibility](https://storage.googleapis.com/homuchen.com/images/hash-function-1.jpg)

### 4. Collision Resistance（抗碰撞）

「碰撞」= 兩個不同輸入得到一樣的 hash。

舉個簡化例子：「除以 5 取餘數」這個爛 hash function，輸入 1、6、11、16 都會得到 1，超容易碰撞。

好的 hash function：**找到兩個碰撞的 input 在計算上幾乎不可能**。所以實務上你可以放心地把 hash value 當作「資料的指紋」 — 兩個 hash 一樣，原始資料就一樣。

> ⚠️ 這也是為什麼 **MD5 跟 SHA-1 已經不能用** — 它們的抗碰撞已經被攻破。2017 年 SHAttered 攻擊在 SHA-1 上做出實際碰撞，2020 年的「SHA-mbles」更展示了 chosen-prefix collision，連 PGP 簽章都能偽造。

### 5. Avalanche Effect（雪崩效應）

輸入只要改 1 個 bit，輸出**完全不一樣**（大約一半的 bits 會翻轉）。例：

```
SHA-256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
SHA-256("Hello") = 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
```

只是把第一個字母大小寫換掉，整個 hash 完全不同。這個特性讓 hash 對篡改極度敏感 — 改一個 byte 就會曝光。

---

## Hash Function 的 6 大應用

Hash 本質就是做出**承諾**、**指紋**、**識別**。看看實務上怎麼用：

### 應用 1：檔案校正 / 安全下載

下載軟體時常看到 SHA-256 checksum：

```
linux-distro.iso        SHA256: 3d8a9e3f...
```

下載完自己算一次，比對 checksum 一樣 → 確定檔案沒被竄改、沒在傳輸中損毀。

### 應用 2：密碼儲存（但不能直接用 SHA-256！）

伺服器要驗證密碼，不能存明文（被駭就完蛋），所以存 hash。使用者登入時把輸入 hash 一遍跟資料庫比對。

**但這裡有個關鍵的坑**：

❌ **不要用** SHA-256 / SHA-3 / BLAKE3 直接 hash 密碼！這些一般 hash 是為了「**快**」而設計，現代 GPU 可以**每秒猜幾百億次** SHA-256，rainbow table + 字典攻擊一下就破。

✅ **要用「故意很慢」的密碼專用 hash**：

| 演算法 | 推薦度 | 適用 |
|--------|-------|------|
| **Argon2id** | ⭐⭐⭐⭐⭐ | OWASP 2026 首選，新專案直接用這個 |
| **scrypt** | ⭐⭐⭐⭐ | Argon2 不可用時 |
| **bcrypt** | ⭐⭐⭐ | 老系統相容 |
| **PBKDF2** | ⭐⭐ | FIPS-140 合規場景 |
| ❌ MD5 / SHA-1 | 0 | 已破解 |
| ❌ SHA-256（直用） | 0 | 太快、抗 GPU 弱 |

OWASP 2026 推薦設定：**Argon2id 19 MiB 記憶體 + 2 iterations + 1 parallelism**（高安全則 128 MiB + 3-5 iterations）。

> 一般 hash vs 密碼 hash 的差別：一般 hash「越快越好」（檔案校驗要快），密碼 hash「故意很慢」（讓暴力破解不可行）。**這兩個用途完全不能混用**。

### 應用 3：Git Commit ID

```
commit d9a1e4f5f1fe19b05bafb4176b2c9a6b89c14bc9
```

那串 40 個 hex 字元就是這個 commit 全部檔案的 **SHA-1 hash**（160 bits）。Git 拿它當 commit 的識別。

> 注意：Git 在 2018 年開始遷移到 SHA-256（因為 SHA-1 不安全），但因為相容性問題，主流 repo 多數還在用 SHA-1。Git 內部的「弱碰撞」沒被利用過，但戰略上 SHA-256 才是未來。

### 應用 4：UUID v3 / v5

* **UUID v3**：基於 MD5（128 bits → 直接用）
* **UUID v5**：基於 SHA-1（截斷成 128 bits）
* **UUID v8**（2024 RFC 9562）：自訂 hash，建議用 SHA-256

### 應用 5：區塊鏈（Bitcoin / Ethereum）

* **Bitcoin**：`SHA-256(SHA-256(block))` 雙雜湊。挖礦本質就是「找一個 nonce 讓 hash 開頭有 N 個 0」。
* **Ethereum**：`Keccak-256`（SHA-3 的近親）。
* **2026 趨勢**：新一代 PoS 鏈（Sui、Aptos 等）開始用 BLAKE3，因為快 4-10 倍能省驗證成本。

### 應用 6：Content-Addressable Storage（IPFS、Git LFS）

把檔案 hash 當作位址：你不再「按檔名找檔案」，而是「按內容指紋找檔案」。

* IPFS 的 CID（Content Identifier）= SHA-256 hash
* Docker image layer 也用 hash 識別
* 同樣內容只存一份，自動去重

---

## 2026 演算法對照表

| 演算法 | 輸出長度 | 速度 | 安全性 | 推薦場景 |
|-------|---------|------|-------|---------|
| MD5 | 128 bits | 極快 | ❌ 已破解 | 只能用於 non-security checksum |
| SHA-1 | 160 bits | 快 | ❌ 已破解（2017 SHAttered）| 不要再用 |
| **SHA-256** | 256 bits | 中 | ✅ 安全 | 業界默認、Bitcoin、SSL 憑證 |
| SHA-512 | 512 bits | 中 | ✅ 安全 | 64-bit 系統上比 SHA-256 還快 |
| **SHA-3 / Keccak** | 224-512 bits | 中慢 | ✅ 安全 | NIST 2015 標準、Ethereum |
| **BLAKE3** | 256 bits（可變）| **超快**（4-10x SHA-256）| ✅ 安全 | 大檔案、串流、新一代區塊鏈 |
| **Argon2id** | 可變 | 故意很慢 | ✅ 安全 | **密碼儲存** |
| bcrypt | 192 bits | 故意很慢 | ✅ 安全 | 密碼儲存（老系統）|
| scrypt | 可變 | 故意很慢 | ✅ 安全 | 密碼儲存（Argon2 替代）|

---

## 賭博遊戲的解法

回到開頭那題：**怎麼讓莊家不能作弊？**

利用 hash 的「**隱密承諾**」特性：

1. 玩家先把賭注（「大」或「小」）+ 一個隨機數 hash 一遍，把 hash 公開
2. 莊家看到 hash 不知道你賭什麼（不可逆）
3. 骰子開出結果
4. 玩家公布原始賭注 + 隨機數，重新 hash 一次
5. 跟一開始公布的 hash 比對 → 一致 = 證明開獎前後賭注沒變

這就是 **commit-reveal scheme**，目前廣泛用在區塊鏈鏈上拍賣、隨機數生成、預測市場。酷吧😎

---

## FAQ

### Q1：MD5 還能用嗎？

**安全用途絕對不行**（密碼、簽章、憑證）。但用來算「下載完整性 checksum」、「資料庫查重」這種非安全場景，速度快還能用。Git LFS 一些早期版本還在用 MD5 算 chunk hash。

### Q2：SHA-256 跟 SHA-3 哪個比較好？

**安全性都一樣強**（沒被攻破過）。差別：
- SHA-256 比較快、硬體加速普及（CPU 有 SHA-NI 指令集）
- SHA-3 用完全不同的 sponge construction（萬一 SHA-2 被破，SHA-3 是備胎）
- **預設用 SHA-256 就好**。除非有合規要求或想「演算法多樣性」才用 SHA-3。

### Q3：BLAKE3 安全嗎？為什麼不大家都用？

BLAKE3 安全性沒被攻破過，速度比 SHA-256 快 4-10 倍。**問題在生態系** — 多數 library、CDN、區塊鏈、SSL 憑證都還是 SHA-256 為主。新專案、自己內部用沒問題，要跟外部互通就要看對方支不支援。

### Q4：為什麼存密碼不能用 SHA-256？

因為**太快**。GPU 每秒可以算幾十億次 SHA-256，加上 rainbow table（預先算好常用密碼的 hash 對照表），破解 8 位數密碼只要幾秒。

Argon2 / bcrypt / scrypt 故意設計成「每次驗證要 100ms-1s」，攻擊速度被砍 10⁹ 倍，加上**抗 GPU**設計（記憶體密集，GPU 沒優勢），實務上不可破。

### Q5：兩個檔案 hash 一樣，內容一定一樣嗎？

**理論上**：不一定（會碰撞），但機率小到可忽略（SHA-256 碰撞機率約 1/2²⁵⁶，比宇宙原子數還少）。

**實務上**：可以當作一定一樣，除非用了被破解的演算法（MD5、SHA-1）。

---

## 小結

回顧一下這次更新的重點：

1. **Hash 5 個特性**：Deterministic、Fixed Length、Irreversibility、Collision Resistance、Avalanche Effect
2. **6 大應用**：檔案校驗、密碼儲存、Git、UUID、區塊鏈、Content-Addressable Storage
3. **2026 選擇**：一般用 SHA-256、要快用 BLAKE3、**密碼用 Argon2id**
4. **絕對不要用**：MD5、SHA-1（已被破解）
5. **最常見的坑**：用一般 hash 存密碼

如果你只記得一件事：**密碼儲存用 Argon2id，其他用 SHA-256，不要用 MD5 / SHA-1**。

延伸閱讀：

* [**密碼學是什麼？有何用途以及要解決什麼樣的問題？**](/posts/what-problems-cryptography-to-solve/)
* [**Node.js 用 crypto module 做 Hash、加密、簽章**](/posts/cryptography-in-nodejs-using-crypto-module/)

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

希望這篇對你理解 hash function 有幫助～密碼學的內容後續會慢慢補，包括 message authentication code、digital signature 等。掰掰～👋

---
title: "Claude Code + Shopify Admin API：讓 AI 當我的電商營運小幫手，一次搬 50 筆商品上架"
date: 2026-04-15
author: HoMuChen
category: AI
tags: [AI, Claude Code, Shopify, API, 電商, 自動化]
image: https://storage.googleapis.com/homuchen.com/images/claude-code-shopify-admin-api-ecommerce-assistant-0.jpg
description: "分享我用 Claude Code 直接透過 curl 打 Shopify Admin API，一次搬 50 筆舊網站商品上架的實戰過程。不靠 MCP、不寫外掛，純靠對話就能完成電商營運日常。"
---

前陣子我把一個舊的電商網站搬到 Shopify，商品總共 50 筆。聽起來好像還好對吧？但每一筆都要填標題、描述、SKU、價格、庫存、分類、照片、變體（尺寸/顏色）……這樣一筆一筆手動點，我估計至少要花我一整個週末🫠

就在我要認命打開 Shopify 後台準備開工的時候，我腦中突然浮現一個問題：**這件事 Claude Code 能幫我做嗎？**

結果不只能，還做得很好。整個過程我幾乎沒碰 Shopify 後台，就是打開 Claude Code，丟一份商品清單進去，剩下的事情它自己搞定。

這篇文章想跟大家聊兩件事：

* **觀念面**：為什麼電商老闆/個人賣家該認真看待 Claude Code 這種 AI Agent
* **案例面**：我實際怎麼用 Claude Code 直接 curl 打 Shopify Admin API 批次上架 50 筆商品

## 為什麼不是請工讀生，也不是用外掛？

在 Claude Code 出現以前，一個人要做這種批次操作，選擇大概是這三條：

1. **手動點 Shopify 後台**：免錢但花時間，50 筆大概 8 小時跑不掉
2. **請工讀生**：每小時 200，做一整天 1600 元，但還要訓練、檢查
3. **裝 Shopify App（外掛）**：每個月訂閱費，而且你要花時間學介面、確認它真的照你的意思做

我本來想走第三條路，但一查發現光是「商品批次上架」的外掛就一堆，每個介面邏輯不一樣、每個月都要付錢、而且對於老網站搬家這種「一次性任務」來說，付月費真的很不划算。

所以我選了第四條路：**直接讓 Claude Code 幫我打 Shopify Admin API**。

## 為什麼不走 MCP，而是直接 curl？

講到 Claude Code 對接外部服務，現在最流行的做法是裝 MCP server。Shopify 官方也有推 AI Toolkit，市場上也有人做好 `shopify-mcp` 之類的套件，照理說我應該用這些才對。

但我後來選擇**不走 MCP，直接讓 Claude Code 用 curl 去打 Admin API**。原因有三個：

**第一，透明。**每一個請求我都看得到 curl 指令本身，要改、要 debug、要重放都很直觀。MCP 在中間包一層，有時候出錯我不知道是 prompt 問題還是 MCP 工具本身的 bug。

**第二，簡單。**我只要有一個 Shopify Admin API 的 access token、一個 store URL，就能動了。不用裝套件、不用設定 MCP server、不用管它跟 Claude Code 的連線。

**第三，可控。**我可以很清楚地告訴 Claude Code：「每次打完一支 API 停下來給我看結果再繼續」。curl 指令是指令，每一筆都在我眼前。

簡單講，就是我想讓 AI 幫我做事，但我想留著方向盤。如果你對 curl 的用法還不熟，可以看我之前寫的 [**Linux HTTP Client 工具 curl 使用**](/posts/linux-http-client-tool-curl-usage/) 這篇。

## 實戰流程：50 筆商品怎麼搬

整個流程大概是這樣：

1. 把舊網站的商品資料整理成一份 CSV（或直接貼成表格）
2. 打開 Claude Code，丟給它商品清單
3. 請它幫我產生 Shopify Admin API 的 curl 指令
4. 先用 1 筆測試 → 確認格式沒問題 → 授權它批次跑完 50 筆
5. 檢查後台、核對結果

### Step 1：準備 Admin API Access Token

這是唯一一個要自己動手的步驟。到 Shopify 後台 → Settings → Apps and sales channels → Develop apps → Create an app，把 Admin API access scopes 裡的 `write_products`、`read_products`、`write_inventory` 這些打勾，安裝後就拿到一個 `shpat_xxx` 開頭的 token。

把這個 token 跟你的 store URL（例如 `your-store.myshopify.com`）一起放在一個檔案裡（記得 `.gitignore`），之後讓 Claude Code 讀就好。

### Step 2：丟商品清單 + 說明目標

我對 Claude Code 下的第一個 prompt 大概長這樣：

> 我要把這個 CSV 裡的商品上架到我的 Shopify。先看一下資料結構，然後幫我寫一個 curl 指令，使用 Shopify Admin API（2025-01 版本）建立第一筆商品。先跑一筆給我確認格式，OK 再批次跑剩下的。

它會做的事：
* 讀 CSV、理解欄位
* 幫我對照 Shopify 的 Product REST API 欄位（`title`、`body_html`、`vendor`、`product_type`、`tags`、`variants`、`images` 等）
* 產出一個 curl 指令
* 跑完一筆後停下來等我確認

這個「停下來等確認」的行為，其實就是 Claude Code 最厲害的地方之一——它不是無腦執行，它會幫你規劃步驟，這部分我在 [**AI Agent 怎麼思考**](/posts/ai-agent-how-it-thinks/) 這篇有更完整的解釋。

### Step 3：測試第一筆

第一筆我會特別緊張地盯著看。因為我最怕的不是它跑不起來，而是它跑起來但資料欄位對錯、圖片連結壞掉、價格少一個零之類的🫠

結果第一筆跑出來，Claude Code 主動做了幾件我沒想到的事：

* 自動把 `$1,290` 這種字串清成純數字 `1290`
* 發現我 CSV 裡有兩筆商品名稱重複，停下來問我要不要合併
* 我商品描述裡有一些 HTML tag 是舊網站的殘留，它幫我清掉並重新排版

這些事如果我自己寫 script 要額外處理，但 Claude Code 會「看懂」資料，做出合理判斷。這也是它跟傳統外掛最大的差別——外掛只會照它設定好的欄位對應規則跑，而 AI Agent 會幫你想。

### Step 4：授權批次執行

確認格式 OK 後，我的 prompt 很簡單：

> 很好，剩下 49 筆照同樣邏輯跑完。每跑 10 筆跟我回報一次進度，遇到失敗的停下來問我。

然後我就去泡咖啡。回來的時候，後台已經躺著 50 筆商品，連變體（尺寸、顏色）跟圖片都掛好了(可以的話，也先請Claude檢查圖片大小，壓縮至適當的大小有利效能)。

中間 Claude Code 主動在一筆遇到 Shopify API rate limit 的時候停下來，告訴我：「這個 store 每秒 cost budget 有上限，我加了 0.5 秒 delay 繼續跑，OK 嗎？」

這種**主動偵測邊界條件、主動請示**的行為，讓我放心很多。

### Step 5：對帳

我最後請 Claude Code 幫我做一件事：把它剛上架的 50 筆商品 ID 列出來，再用 `GET /products.json` 抓一次，跟原始 CSV 對帳，確認每一筆的標題、價格、變體數量都對。

一個自己開、自己幫自己做 QA 的小幫手，完美🎉

## 所以我們能做什麼呢？

講完案例，來講觀念。

如果你是電商老闆、個人賣家、或幫客戶管理店面的人，我真心覺得你應該花一個下午認真玩一次 Claude Code。理由是：

**你的日常營運，80% 是 API 能做的事。**上架商品、改價、調庫存、查訂單、標記出貨、分析銷售——這些在 Shopify 跟 WooCommerce 都有完整開放的 API 可以用（WooCommerce 的 REST API 所有人免費就能開）。蝦皮的 [Shopee Open Platform](https://open.shopee.com/) 跟 91APP 的 Open API 雖然也存在，但前者要申請成為合作夥伴才拿得到 access，後者通常是企業方案才開放，一般個人賣家不一定有權限——這點要先看清楚再選平台。

但重點是：過去卡住你的不是 API 不存在，而是「我不是工程師，我不會寫 code」。

現在 Claude Code 就是幫你跨過那道牆的橋。你不需要會寫 Python、會寫 Node.js，你只需要會**描述你要做的事**。

我在 [**AI 時代的軟體工程師**](/posts/software-engineer-in-ai-era/) 這篇有寫過，AI 不會取代會用 API 的人，但會取代那些「明明可以自動化、卻還在手動做」的工作方式。

而且 Claude Code 的好處是：

* **一次性任務**特別划算（像這次搬家）
* **重複性任務**可以存成 [**Skill**](/posts/what-is-ai-agent-skill/)，下次一句話叫出來就跑
* **沒有月費**，你付的是 Claude 的訂閱費，一個月幾百塊，而且這個能力不只是用在 Shopify，整個電腦都能用

## 幾個實戰小提醒

給想要跟著做的朋友幾個血淚建議：

1. **Token 權限要最小**：不要一次給 full access，先從 `write_products` 這種單一權限開始
2. **先在測試商店跑一次**：Shopify 有 Development Store 免費，可以開一個來玩壞
3. **請 Claude Code 存 log**：每一筆上架成功/失敗的結果寫到一個 `.log` 檔，出事可以回放
4. **Rate limit 要尊重**：Shopify Admin API 每秒 cost budget 有上限，批次跑記得加 delay
5. **備份原始資料**：CSV 先留一份，Claude Code 清資料的過程中萬一有誤判還能回頭對

## 結語

電商營運小幫手不需要是昂貴的 SaaS，也不需要你變成工程師。它可以就是**一個能聽懂你在說什麼、能幫你打 API、能在出錯時停下來問你的 AI**。

這次 50 筆商品，我前後大概花了 40 分鐘：20 分鐘整理 CSV、10 分鐘跟 Claude Code 對話、10 分鐘對帳。比我原本預估的一整個週末少了快 16 小時🎉

下次如果要改價、下季要調庫存、或是要把所有商品的描述加上某段文字——我都不用再打開 Shopify 後台了，我只需要打開 Claude Code，講一句話。

這才是 AI 時代的電商營運該有的樣子。

延伸閱讀：

* [**什麼是 AI Agent？跟 Chatbot 有什麼不一樣**](/posts/what-is-ai-agent-vs-chatbot/)
* [**AI Agent 怎麼思考的？**](/posts/ai-agent-how-it-thinks/)
* [**什麼是 AI Agent 的 Skill？**](/posts/what-is-ai-agent-skill/)
* [**我用 Claude Code 接 Google Search Console 做 SEO 分析**](/posts/claude-code-search-console-seo-analysis/)
* [**Linux HTTP Client 工具 curl 使用**](/posts/linux-http-client-tool-curl-usage/)

感謝您的閱讀～希望對大家有一丁點兒的幫助，掰掰～👋

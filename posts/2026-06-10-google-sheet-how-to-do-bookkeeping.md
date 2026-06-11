---
title: "Google Sheet 記帳教學：4 種方法 + 自動統計公式（2026 更新）"
date: 2026-06-10
author: HoMuChen
category: 生活
tags: [Google Sheet, finance, google form, 記帳]
image: https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-1.jpg
description: "想用 Google Sheet 記帳卻不知從何開始？這篇教你 4 種記帳方式怎麼選，附上自動分類統計的公式範本，還有 2026 年用 AI 對話記帳的新玩法。"
---

不知道大家有沒有試過下載一堆記帳 App，結果用了三天就放棄的經驗？😂

我也是。介面太複雜、要先註冊登入、想看自己的資料還要付費解鎖……最後乾脆不記了。後來我發現，其實用你早就有的 **Google Sheet**，花十分鐘就能做一個完全屬於自己、想怎麼分析都行的記帳系統，而且資料永遠在你自己手上。

這篇就來完整分享一下，用 Google Sheet 記帳的幾種做法。內容會包含：

* **4 種記帳方式怎麼選**——表單、直接打試算表、記帳 App、還是用 AI 對話記帳？
* **用 Google 表單記帳**：把連結放桌面，像 App 一樣按一下就記好
* **直接用試算表記帳**：附上自動分類統計的公式，不用再手動加總
* **2026 新玩法**：用 Claude 對話記帳，連打字分類都省了
* 最後聊聊**為什麼「記帳」這件事本身就會讓你少花錢**

## 先別急著做，你適合哪一種？

在動手之前，先想清楚你是哪種人，免得又做了一個用三天就放棄的系統。我把常見的 4 種記帳方式整理成一張表：

| 方式 | 適合的人 | 優點 | 缺點 |
|------|---------|------|------|
| **Google 表單** | 想在手機上「快速按一下就記完」 | 介面乾淨、可放桌面、不怕手殘改錯資料 | 要看統計得切回試算表 |
| **直接打試算表** | 想自己排版、做進階公式分析 | 最自由、可即時看到統計 | 手機上打字格子有點麻煩 |
| **記帳 App** | 完全不想自己設定 | 開箱即用、有 OCR 掃發票 | 資料被綁在別人平台、想客製化很難 |
| **AI 對話記帳** | 懶到連分類都不想點 | 用講的就好，AI 幫你分類加總 | 要設定一次，2026 才比較成熟 |

我自己的組合是這樣：**手機上用「表單」快速記**，**電腦上用「試算表 + 公式」做月度分析**。兩個搭在一起，記的時候無痛，看的時候清楚。下面就從最簡單的表單法開始。

## 方法一：用 Google 表單記帳（最無痛）

利用 Google 表單來記帳，最大的好處是：表單連結可以放到手機桌面，就像一般 App 一樣，按一下就跳出記帳畫面，填完送出就好，完全不用面對一堆密密麻麻的格子。每次的紀錄會自動存進試算表，之後想做任何統計分析都行。

![google sheet bookkeeping](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-1.jpg)

### 建立表單

先開一個新的試算表，點選 **工具** → **建立表單**，就會在新分頁跑出一張空白表單，接著編輯它的內容。

> 💡 從試算表建立表單的好處是：表單送出的資料會「自動」流進這張試算表，省去自己串接的步驟。

### 編輯表單

幫表單命名，這裡就打個「記帳」。接下來每一題可以是簡答、單選或多選，建議放這三題：

**第一題「項目」**——你花了什麼錢，題型選**簡答**：

![google form question 1: item](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-2.jpg)

**第二題「金額」**——一樣選簡答，填的時候記得只打數字（後面公式才算得動）。

**第三題「分類」**——選**單選題**，選項就你開心怎麼分。我的例子是食、衣、住、行、娛樂、其他：

![google form question 3: types](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-3.jpg)

> 分類這題建議用**單選下拉**而不是簡答，這樣每筆資料的分類文字才會一致，統計時不會「早餐」「早餐 」（多一個空格）被算成兩類。如果你想在試算表那邊也做下拉選單，可以參考我之前寫的 [**Google Sheet 製作下拉式選單**](/posts/google-sheet-create-a-drop-down-list-from-existed-data/)。

後面想加日期、備註、付款方式（現金／信用卡）都可以，越貼近你想分析的維度越好。

### 把表單加到手機主畫面

完成表單後，點右上角的**傳送**，拿手機瀏覽器打開這個網址：

![google form send](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-4.jpg)

點瀏覽器選單裡的**加到主畫面**，桌面就會出現一個小圖示，之後就像開 App 一樣，點一下直接記帳：

![google form add to desktop](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-5.jpg)

### 檢視成果

每次表單送出的資料，都會乖乖收進 Google Sheet：

![google sheet data](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-6.jpg)

接著就能拿這些資料做各種統計圖表，比如每天花多少、各分類佔比多少：

![google sheet charts](https://storage.googleapis.com/homuchen.com/images/google-sheet-bookkeeping-7.jpg)

## 方法二：直接用試算表記帳 + 自動統計公式

如果你不想多管理一張表單，其實直接在 Google Sheet 裡打也完全 OK，而且彈性最大。重點是——**別只是把數字打進去，要讓公式自動幫你算**，不然每個月底還要手動加總就太累了。

假設你的資料長這樣（A 欄日期、B 欄項目、C 欄分類、D 欄金額）：

| 日期 | 項目 | 分類 | 金額 |
|------|------|------|------|
| 6/1 | 早餐 | 食 | 65 |
| 6/1 | 捷運 | 行 | 30 |
| 6/2 | 電影票 | 娛樂 | 320 |

接下來這幾個公式，是我覺得最實用的：

**① 某個分類總共花多少**——用 `SUMIF`：

```
=SUMIF(C:C, "食", D:D)
```

**② 這個月總共花多少**——用 `SUM`：

```
=SUM(D:D)
```

**③ 一次算出「各分類的小計」**——這招最方便，用 `QUERY` 一行搞定，不用每個分類各打一條 `SUMIF`：

```
=QUERY(A:D, "select C, sum(D) where C is not null group by C label sum(D) '總額'")
```

這條公式會自動列出「食 / 衣 / 住 / 行 / 娛樂 / 其他」各自花了多少，新增一筆資料它就自動更新，等於一個會自己長大的小 dashboard 😎。

**④ 想看每日花費趨勢**——可以搭配迷你折線圖 `SPARKLINE`，在格子裡直接畫出趨勢線。這個我之前有寫一篇專門的教學：[**Google Sheet 用 SPARKLINE 做迷你圖表**](/posts/google-sheet-sparkline/)，記帳的趨勢視覺化超好用。

如果你還想更進一步，把記帳資料做成像損益表那樣的月度報表，我寫過一篇 [**用 Google Sheet 製作股票損益表**](/posts/google-sheet-stock-income-statement/)，裡面用到的表格與公式邏輯，搬來做「支出損益表」也完全通用。

> 💡 想更系統地學 Google Sheet 這套自動化工具，我有開一門 [**Claude Code 實戰課**](/courses/)，從 0 帶你用 AI 做出這類自己的小工具。

## 方法三、四：記帳 App 與 2026 的新選擇——AI 對話記帳

前面兩種都是自己動手做。如果你真的懶，市面上的記帳 App 當然也能用，只是資料會被綁在別人的平台上，想客製化分析就比較難。

不過 2026 年有一個我覺得最有趣的新玩法：**用 AI 對話記帳**。你不用打開表單、不用選分類，直接跟 AI 講「今天午餐花了 120」，它就幫你判斷分類、寫進你的 Google Sheet。連「這是食還是娛樂」都讓 AI 去想。

我自己用 Claude Code 串了一個這樣的記帳助手，可以用 LINE 之類的聊天介面隨時記帳，完整做法寫在這篇：[**用 Claude Code 打造對話式記帳助手**](/posts/claude-code-remote-control-conversational-bookkeeping/)。如果你已經習慣前面的 Google Sheet 記帳，這篇等於是幫你把「最後一哩的手動分類」也自動化掉。

簡單對比一下這條演進路線：

* **表單記帳**：按一下、選分類、送出（手動 3 步）
* **試算表記帳**：自己打字、公式自動統計（手動輸入）
* **AI 對話記帳**：一句話，分類與寫入都自動（幾乎零手動）

不用一步到位，先從表單開始記，習慣養成後再考慮要不要升級到 AI 自動化，這樣最不容易半途而廢。對了，記帳這種「持續性的小習慣」要怎麼養成不放棄，我之前在 [**Google Sheet 追蹤進度的小工具**](/posts/google-sheet-track-progress/) 那篇也分享過一些做法。

## 為什麼「記帳」這件事本身就會讓你少花錢？

最後想聊一個比工具更重要的事。

在 [**《金錢心理學》**](/posts/book-note-money-psychology/) 這本書裡有提到：我們人類天生會**避免痛苦**，而付錢其實就是一種痛苦。所以商人發明了各種方法來讓我們「忘記痛苦」——預付、後付、信用卡、一鍵購物……讓花錢變得越方便、越無痛，我們就花得越多。

所以我們能做什麼呢？**記帳這個動作，剛好把那份「痛」還給你。** 每次花錢都要拿出手機記一筆，你會清楚感受到錢正在噴出去。它不只是個追蹤消費的工具，更可能因為「懶得記」，哪天就乾脆不亂花了呢～😂

這本書的下集我也寫了筆記，想更了解我們是怎麼被「無痛花錢」設計的，可以看 [**《金錢心理學》(下)**](/posts/book-note-dollars-and-sense/)。

## 結論

記帳工具沒有最好的，只有最適合你的：

* 想無痛快速記 → **Google 表單**放桌面
* 想自由分析 → **直接打試算表 + QUERY 公式**自動統計
* 想完全自動 → **用 AI 對話記帳**

工具只是手段，重點是你真的開始記、而且記得下去。先挑一個最簡單的開始，記滿一個月，你大概就會對自己的錢都花去哪嚇一跳了。希望這篇對想開始記帳的你有一丁點兒的幫助！

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

---
title: "不用 Google Sheet 也不用 App — 我的 Claude Code 對話式記帳工作流"
date: 2026-05-05
author: HoMuChen
category: AI
tags: [AI, Claude Code, 記帳, Google Sheet, Remote Control]
image: https://storage.googleapis.com/homuchen.com/images/claude-code-remote-control-conversational-bookkeeping-0.jpg
description: "我把用了 5 年的 Google Sheet 記帳收掉了，也沒換成記帳 App。現在用 Claude Code Remote Control，手機隨時對話記帳、AI 自動分類、想看圖隨時生。完整工作流分享。"
---

5 年前，我寫過一篇 [**用 Google 表單記帳**](/posts/google-sheet-how-to-do-bookkeeping/) 的文章，到現在都還有不少人在看。當時的做法是：手機開 Google 表單填一筆，後面 Google Sheet 自動幫你算總和、分類、月結。

那時候覺得這真的好棒，一切都自動化、一切都看得到圖表。

然後我升級過幾次。試過記帳 App、試過 ChatGPT 接 Telegram Bot、甚至試過用 iOS 捷徑串 OpenAI API。

**結果現在我都不用了。** 我也沒換成 Moze、CWMoney、AndroMoney 那些主流記帳 App。

我現在的記帳工具是 **Claude Code**，加上手機上的一個對話 App。完全沒有 Google Sheet、沒有記帳 App、沒有第三方自動化平台。一筆帳就是一句話，「中午便當 120」，AI 自動分類好寫進檔案。月底想看圖，「幫我做這個月的支出分類圖」，幾秒鐘做好。

這套流程我用了幾個月，**整個記帳行為從「打開 App、選分類、填數字、按儲存」這一連串動作，變成只剩一句話。** 分類正確率約 9 成，分錯的下次糾正就學會。每天記帳時間從 1-2 分鐘降到 10 秒以內。

> 利益揭露：本文沒有業配、沒有任何聯盟連結。提到的所有工具都是自己掏錢試過的，包含放棄掉的那幾款。

今天來分享這個工作流，以及為什麼我覺得這是 2026 年比較合理的做法：

* 為什麼我把 Google Sheet 收掉了
* 為什麼我也沒換成記帳 App
* 我現在的對話式記帳工作流
* UI 從 dashboard 朝「想看才生」位移的核心概念
* 你也可以怎麼做

## 為什麼我把 Google Sheet 收掉了

**Google Sheet 在 2026 年從「必要工具」變成「可選工具」，因為它最值錢的能力（視覺化）已經被 AI 取代了。**

Google Sheet 對個人記帳來說，主要提供兩個價值：

1. **結構化儲存**：每一筆帳都有日期、金額、類別、備註
2. **內建視覺化**：圖表、Pivot Table、條件格式

5 年前這兩個能力捆綁在一起非常珍貴，因為**第二項（視覺化）需要結構化的試算表才能做**。

但 2026 年的世界變了。

現在我有 Claude Code，**它可以讀任何結構的資料、隨時做出我想看的圖**。我不需要先把資料放進試算表才能視覺化。一個 markdown 檔、一個 CSV、甚至幾段我亂寫的 log，AI 都能處理。

Sheet 的「視覺化」優勢被拆掉了。

剩下的「結構化儲存」價值還在，但這件事不一定要用 Google Sheet 做。一個本地的 CSV 或 markdown 檔，能力上完全等價，而且不需要連網路、不需要登入、不需要等 Google 載入。

> 當視覺化變成 on-demand，**dashboard 工具的角色就從「主要呈現方式」退到「給人熟悉感的入場票」**。

我把這個現象稱為 **「On-Demand Visualization」原則**——資料在系統裡就夠了，視覺化是隨叫隨生的，不是預先做好的。下面會再展開。

## 為什麼我也沒換成記帳 App

**記帳 App 在 AI 時代對個人使用者來說，劣勢比優勢多。** 我也試過好幾款，但歸納起來有 4 個讓我不舒服的地方：

**資料主權**：你的消費記錄是你的，但放進 App 之後就被鎖在它的雲端。要匯出？通常要付費版，還只能匯出 CSV，圖表和分類是匯不出來的。

**分類被綁死**：App 裡的「餐飲」「交通」「娛樂」是它定義的，你想加「貓咪預算」「副業收入」「禮金往來」？要嘛沒辦法、要嘛要升級到 Pro 版。

**智慧度低**：記帳 App 的「自動分類」基本上是關鍵字比對，看到「全家」就歸「便利商店」。但你跟客戶在全家咖啡座談 4 小時、買了 200 元咖啡和點心——這應該是「業務交際」不是「便利商店消費」。**真正的語意理解需要 LLM，App 內部那個簡單分類引擎做不到。**

**訂閱費**：以台灣常見的幾款付費記帳 App 來看——Moze 4 Pro 訂閱版約 NT$120/月、CWMoney Ex 約 NT$60/月、AndroMoney Pro 一次性付費 NT$300——年成本落在 NT$300-1,500 之間。對比 Claude Pro 的 USD $20/月，**Claude Pro 一個訂閱解所有事，而且這個訂閱還能拿來做別的事**——寫文章、寫程式、查資料、做 [**SEO 分析**](/posts/claude-code-search-console-seo-analysis/)、追蹤[**台股投資**](/posts/claude-code-finmind-stock-tracking/)。一個訂閱多份用途。

加總起來，**記帳 App 解決的問題比較少、限制比較多、成本反而沒有比較低**。

## 三種記帳方式怎麼選？

把這三種方案放在一張表上比較會更清楚：

| 維度 | Google Sheet | 記帳 App | Claude Code |
|------|-------------|----------|------------|
| **資料主權** | 你的 Google 帳號 | 廠商雲端 | 你的本機 / 你選的雲端 |
| **視覺化** | 內建圖表 | App 預設報表 | AI on-demand 隨時生 |
| **客製欄位** | 自由（會用公式） | 廠商定義 | 一句話就改 |
| **智慧分類** | 公式比對 | 關鍵字比對 | LLM 語意理解 |
| **月費** | 免費 | NT$60-200 | USD $20（含其他用途） |
| **入門門檻** | 中（要會公式） | 低 | 低（會講話就行） |
| **手機操作** | 試算表 App 操作慢 | App 順手 | Remote Control 對話 |
| **跨平台 / 匯出** | 容易（CSV、Excel） | 受限於廠商 | 完全自由 |

簡單講：
- **想要免費 + 完全自由**：Google Sheet 還是好選擇
- **想要極度方便、不在意被綁住**：記帳 App
- **想同時要自由 + 方便 + 智慧**：Claude Code 是目前唯一同時做到的

## 對話式記帳工作流長什麼樣子？

**整套流程的核心是：用 Claude Code 的 project 當記帳容器，用 Remote Control 讓手機隨時能跟它對話。** 4 個 Step：

### Step 1：開一個 Claude Code project，放一個記帳檔

我有一個個人 wiki 專案，裡面就有一個 `expenses.md` 檔（其實 csv 也可以，看你習慣）。在 `CLAUDE.md` 裡定義好記帳格式：每一筆要有日期、金額、項目、分類，以及自動分類的規則。

設好之後 Claude Code 每次開新對話，都會讀 `CLAUDE.md`，自動知道要怎麼幫我記帳。**這是讓系統可以重複使用的關鍵。**

### Step 2：手機開 Claude Code Remote Control

這是整套工作流的 wow moment。

Claude Code 有一個 [**Remote Control**](https://docs.claude.com/en/docs/claude-code/remote-control) 功能（Anthropic 官方文件），可以讓你在手機 App 上跟桌機的 Claude Code session 對話。換句話說，你在外面吃完午餐，掏出手機就能跟你電腦上的 Claude Code 講「中午便當 120」，它就會幫你寫進檔案。

**不需要打開電腦、不需要連 VPN、不需要 SSH。** 就跟用 LINE 一樣自然。

### Step 3：對話式記帳

實際對話可能像這樣：

> 我：中午便當 120
>
> Claude Code：已記錄 → 2026-05-04，午餐，便當，120 元，分類：餐飲

或者複雜一點：

> 我：剛跟客戶在咖啡廳，咖啡和茶點 480
>
> Claude Code：已記錄 → 2026-05-04，下午，咖啡廳，480 元，分類：業務交際

這個跟一般記帳 App 的差別：**它真的看得懂語境**。「跟客戶」這三個字會讓它分類成業務交際，而不是個人餐飲。

如果分類錯了，下一句直接糾正：

> 我：那是個人的，分類改成餐飲
>
> Claude Code：好，已更新

它就修好了。下次遇到類似情境也不會再分錯。

### Step 4：想看數據隨時生

月底想看支出狀況？直接問。

> 我：幫我做這個月的支出分類圖

Claude Code 會去讀 `expenses.md`，依照分類加總，畫出一張圓餅圖或長條圖（HTML / SVG / 直接 ASCII art 都可以，看你要什麼形式）。

想看趨勢？

> 我：最近三個月的餐飲支出有沒有增加

它就讀檔、算數字、給你答案。

**這就是「on-demand」視覺化。** 不需要先做好 dashboard，想看才生。

如果是每個月固定要看的圖（例如「月支出總覽」），就讓 Claude Code 把生成程式寫成 script 存起來，下次跑一次就出圖，不用每次重生。

## 為什麼 dashboard 開始被 on-demand 取代？

**這是這整件事背後的核心概念，我把它叫做「On-Demand Visualization」。**

傳統的工具設計（包含記帳 App、財務 dashboard、Google Sheet）都遵循一個模式：

> 先設計好 UI 跟報表 → 使用者只能在這個既定的框架裡看資料

要看新的東西？要加新的圖？得改程式、上版本、等更新。**能看什麼就看什麼。**

但 AI 工具改變了這個邏輯：

> 系統有資料就夠了 → 想看什麼就叫 AI 即時生

加新分析不用等出版週期，問就有。

這個位移不是只發生在記帳，所有「資料 + 視覺化」的場景都在發生：

- **看公司業績** → 不需要做好 BI dashboard，問 Claude「上週業績比上月同期如何」
- **追蹤投資組合** → 不需要做好損益試算表，問「我的台積電現在賺多少」
- **追蹤健身數據** → 不需要 fancy 健身 App，叫 AI 讀 Apple Health 匯出的 XML 直接畫圖

dashboard 沒有完全消失，**它退到「每天固定要看的核心指標」這個角色**。其他「臨時想知道的事」都用 on-demand 處理。

如果這個概念你覺得有共鳴，可以對照看 [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/) 那篇，討論的是同樣的位移，只是切的角度不一樣。

## 你怎麼開始用 Claude Code 記帳？

**4 個 Step 就能跑起來。** 假設你已經有 [Claude Pro](https://www.anthropic.com/pricing) 訂閱跟 Claude Code 安裝好：

**Step 1：開一個 Claude Code project，準備一個記帳檔**

可以是 `expenses.md`，可以是 `expenses.csv`，看你喜歡哪種格式。

**Step 2：在 CLAUDE.md 裡寫清楚規則**

這是讓系統可以「不用每次重新解釋」的關鍵。內容大概包含：

- 記帳檔的位置和格式
- 你想要的分類有哪些
- 自動分類的規則（例如「『跟客戶』『跟廠商』關鍵字 → 業務交際」）
- 加新筆記的格式

寫完之後，下次你說「中午便當 120」的時候，Claude Code 讀完 CLAUDE.md 就知道怎麼處理。

**Step 3：啟用 Claude Code Remote Control**

開啟 Remote Control 之後，下載對應的手機 App，連線到你的桌機 session。設定一次，之後手機隨時都能跟它對話。

**Step 4：開始用，邊用邊調**

第一週可能會發現分類規則不夠完整、某些情境分錯。**這時候直接跟 Claude Code 說「以後遇到 XX 就分類成 YY，更新到 CLAUDE.md」。** 它會自己把規則寫進去，下次就照做了。

整個系統會隨著你越用越聰明，這跟記帳 App 的差別是——**App 規則是廠商寫的，你的規則是你自己定的**。

## 常見問題

### Claude Code 記帳跟 ChatGPT 記帳有什麼差別？

**最大差別在於「能不能直接寫進你自己的檔案」。** ChatGPT 對話完內容停留在它的 web 介面，要把帳寫進你自己的 Google Sheet 或 Telegram，得透過 Make / Zapier / iOS 捷徑這類中介工具，設定門檻不低。Claude Code 是一個跑在你電腦上的 agent，本來就能讀寫本機檔案，加上 Remote Control 直接把對話入口搬到手機，整個 pipeline 是直連的。

### 用 AI 記帳資料安全嗎？會不會被拿去訓練？

**Anthropic 官方政策：API 跟 Claude Pro 預設不會用你的對話訓練模型**（除非你主動開啟分享）。記帳的檔案本身存在你自己的本機（或你選的私人雲端），Claude 只是「讀」資料來分類跟回答，不會主動上傳到任何地方。如果是高度敏感的資料（例如商業機密級的支出），還是建議用 enterprise 等級方案。

### 一定要會寫程式才能用嗎？

不用。**你會講「中午便當 120」就會用了。** Step 1 跟 Step 2 的設定可以讓 Claude Code 自己幫你建——你跟它說「幫我建一個記帳系統，欄位包含日期、金額、項目、分類」，它會自動寫好 `expenses.md` 跟 `CLAUDE.md`。整個流程跟學一個新 App 差不多，但少了選分類、按按鈕的步驟。

### Claude Code Remote Control 怎麼用？

[官方說明在這](https://docs.claude.com/en/docs/claude-code/remote-control)。簡單講：在桌機上開一個 session 並啟用 Remote Control，會拿到一個連線資訊；在手機上下載對應的 Anthropic Claude App，登入同一個帳號，就能看到桌機上開的 session 並直接對話。

### 沒有 Google Sheet 那要怎麼跟會計師對帳 / 報稅？

**檔案是 markdown 或 csv，匯出成 Excel 或 Google Sheet 是一句話的事。** 「幫我把這個月的帳轉成 Excel 檔，按分類分頁」就生出來了。資料主權還是在你手上，要對帳的時候才產出對外格式，平常自己用對話就好。

### 我可以混用嗎？例如 Claude Code 收資料 + Google Sheet 給家人看？

當然可以。**這是混合模式：本機檔案當 source of truth，Google Sheet 當「給人看的展示層」。** Claude Code 每天/每週把帳同步到一個共用的 Google Sheet，家人看 Sheet 就好，你自己用對話介面記。兩邊各取所需。

## 結語

這整件事最讓我有感的是：**Claude Code 改變的不只是工具，是工作流的邊界本身**。

以前我們會問「該選哪個記帳 App」「該用 Excel 還是 Google Sheet」，因為這些是預先存在的容器，我們的記帳行為要塞進這些容器才能運作。

現在 AI 改變了這個關係。**容器可以為你的行為而生，而不是你為容器服務。** 你想用 markdown 就 markdown、想用 CSV 就 CSV、想要哪些欄位你自己決定、想看什麼圖隨時生。

這個轉變一旦發生，回頭看那些 fancy 的記帳 App 跟 dashboard 工具，會覺得它們解決的問題其實沒有那麼大——它們大部分的功能，**是為了補償「沒有 AI」的世界裡，使用者跟資料之間缺少的那座橋**。橋現在有了，工具的角色自然要重新定位。

如果你也覺得手上的記帳工具用得不爽，或是好奇 Claude Code 這類 AI Coding Agent 在生活應用上能做什麼，這個工作流真的值得試試看。設定好之後，每天花不到 30 秒，記帳這件事就完全融進你的生活。

延伸閱讀：
* [**用 Google 表單來記帳**](/posts/google-sheet-how-to-do-bookkeeping/) — 5 年前的做法，現在還是很多人在用
* [**用 Claude Code 建台股追蹤系統 — AI 幫你接 API、管持倉，你只要說你買了什麼**](/posts/claude-code-finmind-stock-tracking/) — 同一個對話式工作流，用在投資追蹤
* [**Claude Code 接 Google Search Console — 用 AI 幫你做 SEO 分析**](/posts/claude-code-search-console-seo-analysis/) — Claude Code 串接外部資料的另一個案例
* [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/) — 為什麼 AI 工具的角色正在從顧問變成同事

希望這篇對大家有一丁點兒的幫助～掰掰～👋

---

*本文 2026-05-05 首次發布。如果 Claude Code Remote Control 或相關工具有重大更新，會回來修正。*

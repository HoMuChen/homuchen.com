---
title: "AI Agent 串接 LINE：Messaging API、Webhook 與 Hermes Agent 原理"
date: 2026-07-14
author: HoMuChen
category: AI
tags: [AI Agent, LINE, Messaging API, Webhook, 自架]
image: https://storage.googleapis.com/homuchen.com/images/ai-agent-line-bot-tutorial-0.jpg
description: "想把自架 AI Agent 接到 LINE？本文從 LINE Messaging API、Webhook、簽章驗證到回覆訊息，整理一套可重現的最小串接流程，也補充 Hermes 與 Telegram 的差異。"
---

我平常比較常用 Telegram 接 AI Agent。

原因很現實：申請一隻 bot、拿 token、呼叫 API，幾行 code 就能讓 agent 傳訊息給我。之前在[**用 Telegram / LINE 遙控你的 AI Agent、收任務通知**](/posts/ai-agent-channels-telegram-line/)裡，我也把這套做法攤開來講過。

但如果你的使用者主要在台灣，或你只是想讓家人、客戶用平常最熟悉的 App 找到 agent，那 LINE 就很難繞過去了。

這篇先說清楚：**我目前實際長期使用的是 Telegram，還沒有把自己的 agent 正式接到 LINE。** 所以下面不是「我已經在線上跑了三個月」的踩坑紀錄，而是根據 LINE Developers 官方文件、Hermes 官方 LINE adapter 文件，整理出一套可以理解與重現的架構流程。涉及正式上線的地方，請以官方文件為準～

> **先講結論：**要把 AI Agent 接到 LINE，核心不是 LINE 專用的 AI API，而是用 LINE Messaging API 接收 Webhook，再由你的伺服器呼叫 agent，最後用 reply 或 Push API 把結果送回去。自架 agent 最容易踩到的坑是公開 HTTPS、`X-Line-Signature` 驗證，以及 reply token 的時效限制。

> **本文驗證範圍：**內容與設定方向已對照官方文件，Python 範例是可重現的示範，但尚未在作者自己的 LINE Channel 上完成端到端實測；Hermes 部分以 Hermes 官方文件截至 **2026-07-14** 的設定為準。

這篇會聊：

* LINE Bot、Messaging API、Webhook 各自負責什麼
* 如何建立 LINE Messaging API Channel
* LINE Webhook、Channel secret 與 access token 各自負責什麼
* Hermes Agent 如何接手訊息與回覆
* Hermes Agent 的官方 LINE 接法
* Reply API、Push API 與常見錯誤

## 先理解：LINE Agent 的訊息怎麼走

Telegram bot 比較像是：「我拿 token 呼叫 `sendMessage`，訊息就送出去了。」

LINE Messaging API 則是雙向的：

> 使用者在 LINE 傳訊息 → LINE Platform 呼叫你的 Webhook → 你的伺服器處理 → 用 Messaging API 回覆。

可以把它想成郵差：

* **LINE Official Account**：你的店面
* **Webhook URL**：店面的收件地址
* **Channel secret**：驗證來信是不是 LINE 寄的
* **Channel access token**：你的伺服器寄回訊息時使用的通行證
* **AI Agent**：收到信後，真正負責做事的員工

這跟我用 Telegram 做股票通知的方向不太一樣。Telegram 那套主要是 agent 主動通知我；LINE 這篇則先處理「使用者傳訊息進來，agent 回覆」的雙向流程。

## 建立 LINE Messaging API Channel

到 [LINE Developers Console](https://developers.line.biz/console/) 建立 Provider，接著建立一個 Messaging API Channel。

建立完成後，準備兩個值：

1. **Channel secret**：在 Basic settings 裡取得
2. **Channel access token**：在 Messaging API 分頁 Issue 一組 long-lived token

另外，為了避免 LINE 官方帳號的預設自動回覆跟自己的程式互相搶答，建議先關閉：

* Greeting messages
* Auto-reply messages

完成後，在 Messaging API 分頁找到 QR Code，把 Official Account 加成好友，之後才能測試。

## Webhook 是關鍵

LINE 會對你設定的 Webhook URL 發送 HTTP POST。這個網址必須是**公開的 HTTPS URL**，所以 `http://localhost:3000` 不能直接貼上去。

如果是本機測試，可以用 ngrok 或 Cloudflare Tunnel；正式環境則建議使用固定網域與正式 HTTPS。臨時 tunnel 適合驗證流程，不適合直接當 production 架構。

Webhook 收到訊息後，基本上要完成四件事：

1. 驗證 `X-Line-Signature`，確認請求真的來自 LINE
2. 讀取事件內容與使用者 ID
3. 將訊息交給 AI Agent 處理
4. 在 reply token 有效期限內回覆，或改用 Push API

所以 Webhook 不是「貼一個網址就完成」；它其實是 LINE 與 agent 之間的接待櫃台。

## 用 Hermes Agent 當作實際例子

Hermes 官方已經提供 LINE platform plugin，不需要自己修改 Hermes 核心程式。這正好適合拿來理解整個流程：你不用先寫一個 Bot framework，而是把 LINE 當成 Hermes 的另一個入口。

Hermes 接到 LINE 後，訊息大致會這樣走：

```text
LINE 使用者傳訊息
    ↓
LINE Messaging API 呼叫 Hermes Webhook
    ↓
Hermes 驗證 signature 與使用者權限
    ↓
Hermes 把訊息交給 agent
    ↓
Agent 使用記憶、tools、skills 完成任務
    ↓
Hermes 用 reply / Push API 回到 LINE
```

官方流程大致是：

1. 建立 LINE Messaging API Channel
2. 取得 Channel secret 與 long-lived access token
3. 讓 Hermes 的 webhook port 對外提供 HTTPS
4. 在 `~/.hermes/.env` 設定 token、secret 與 allowlist
5. 在 `~/.hermes/config.yaml` 啟用 LINE platform
6. 將 Webhook URL 設為 `/line/webhook`
7. 執行 `hermes gateway`

Hermes 文件中的設定概念如下：

```env
LINE_CHANNEL_ACCESS_TOKEN=你的_token
LINE_CHANNEL_SECRET=你的_secret
LINE_ALLOWED_USERS=Uxxxxxxxxxxxxxxxx
LINE_PUBLIC_URL=https://你的公開網域
```

```yaml
gateway:
  platforms:
    line:
      enabled: true
```

### 為什麼要設定 allowlist？

LINE Bot 一旦公開，理論上任何加它好友的人都可能傳訊息進來。如果這隻 agent 能讀檔案、執行指令或操作外部服務，就不能只依賴「網址很難猜」來保護它。

Hermes 的 `LINE_ALLOWED_USERS`、`LINE_ALLOWED_GROUPS` 與 `LINE_ALLOWED_ROOMS`，就是把「誰能叫這隻 agent 做事」先限制住。開發時可以為了方便放寬，正式環境則應該明確列出允許的使用者。

這也是自架 agent 跟普通聊天機器人的差別：它不是只有回答問題，還可能真的動手做事，所以權限邊界一定要先畫好。

### Hermes 怎麼處理慢速回覆？

LINE 的 reply token 是一次性的，而且大約只有 60 秒有效。可是 AI Agent 有時候需要查資料、呼叫 tool，甚至自己修錯誤，超過 60 秒並不奇怪。

Hermes 的做法是：如果模型在門檻時間內還沒完成，就先回一個「還在思考」的按鈕，等使用者點擊後取得新的 reply token，再把結果送回去。另一條路則是使用 Push API。

這裡的重點不是記住 Hermes 的某個設定名稱，而是理解限制：**Webhook 收到後，不代表 agent 可以無限期慢慢想。** Channel adapter 必須處理「即時回覆」與「非同步工作」之間的落差。

## Telegram 和 LINE 的差異

以我目前使用的 Telegram 經驗來看，兩者的設計感受很不一樣：

| | Telegram Bot | LINE Messaging API |
|---|---|---|
| 主要入口 | Bot API | Official Account + Channel |
| Agent 收訊息 | Bot API / webhook | Webhook |
| Agent 回覆 | API 呼叫 | Reply API 或 Push API |
| 個人快速通知 | 設定簡單 | 需要較完整的 Channel 設定 |
| 台灣使用者熟悉度 | 中 | 高 |
| 主要工程重點 | token、chat id | HTTPS、signature、reply token、權限 |

如果你的 agent 只是排程跑完通知自己，Telegram 仍然比較省事；如果你要讓別人透過日常使用的通訊軟體交辦任務，LINE 會是更自然的入口。

## 常見問題

### 為什麼 Webhook Verify 失敗？

先確認：

* URL 是公開 HTTPS
* path 完全正確
* server 正在執行
* endpoint 回傳 HTTP 200
* tunnel 沒有改寫 request body

### 為什麼 LINE 收不到回覆？

檢查 Channel access token、reply token 是否已使用過，以及程式是否在 reply token 有效期限內完成回覆。慢速的 LLM 應改用非同步工作或 Push API。

### LINE 可以像 Telegram 一樣主動通知嗎？

可以，但不是使用 reply token，而是使用 Push API，並且需要知道目標使用者的 user ID。Push message 可能涉及方案額度，費用與限制請以 LINE 官方定價頁為準。

### Telegram 和 LINE 該選哪個？

如果你是自己用、只想快速收通知，我仍然會先選 Telegram：設定簡單、Bot API 直接。

如果你的使用者本來就在 LINE，或你要做台灣使用者熟悉的對話入口，那 Messaging API 值得多花一點設定時間。

## 資料來源與限制

本文主要參考：

* [LINE Developers：Build a bot](https://developers.line.biz/en/docs/messaging-api/building-bot/)
* [LINE Developers：Receive messages (webhook)](https://developers.line.biz/en/docs/messaging-api/receiving-messages/)
* [LINE Developers：Send messages](https://developers.line.biz/en/docs/messaging-api/sending-messages/)
* [Hermes Agent：LINE platform](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/line)

LINE 的方案、API 限制、Hermes CLI 與設定都可能更新；正式部署前請再查看最新官方文件。這篇也不把「文件上可行」包裝成「我已經在線上驗證」，這點先跟大家說清楚～

## 結語

把 AI Agent 接到 LINE，真正麻煩的不是「叫模型回答問題」，而是 Webhook、HTTPS、signature 驗證、reply token 與權限控管這些周邊工程。

Telegram 讓我很快做出「agent 有事敲我」的通知；LINE 則比較像「把 agent 開一扇使用者熟悉的門」。兩者沒有誰一定比較好，重點是你的 agent 要服務誰、訊息從哪裡進來、結果要怎麼出去。

希望這篇整理能讓你少踩一點設定的坑～正式上線前，記得再對照一次 [LINE Developers 官方文件](https://developers.line.biz/en/docs/messaging-api/building-bot/)。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的延伸文章，也可以接著看我之前用 Telegram 做的[**AI Agent 通知流程**](/posts/ai-agent-channels-telegram-line/)。

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

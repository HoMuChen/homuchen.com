---
title: "用 Telegram / LINE 遙控你的 AI Agent、收任務通知 — 自架 AI Agent 實戰（五）"
date: 2026-06-05
author: HoMuChen
category: AI
tags: [AI Agent, Claude Code, Telegram, LINE, Remote Control]
image: https://storage.googleapis.com/homuchen.com/images/ai-agent-channels-telegram-line-0.jpg
description: "AI Agent 不該只活在終端機。分享我怎麼用 Claude Code Remote Control 手機遙控 agent、用 Telegram bot 收任務通知（盤中股票訊號就這樣來），還有 LINE、官方 Channel、OpenClaw/Hermes 多 channel 的選擇。自架 AI Agent 實戰系列 #5。"
---

前陣子某個交易日的盤中，我在開會，手機震了一下。

是 Telegram，我那隻台股 bot 傳來的：「🔔 2330 台積電【波動率擠壓】，突破上軌、量能達標、動量轉正。」**那個當下我完全沒在看盤**，是它自己盯著、到點了主動敲我。

再往前一點，某天中午我在外面吃便當，掏出手機打了一句「中午便當 120」，我電腦上的 Claude Code 就把這筆帳分類好、寫進檔案。**我人不在電腦前，但 agent 在。**

這兩件事有一個共通點：**我的 AI Agent 沒有被關在終端機裡。** 它能在我日常用的手機 App 裡跟我對話、也能主動跑來找我。

在 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的總論裡，我把一隻自主 agent 拆成四層：**Context（它知道什麼）→ 能力（它能做什麼）→ 溝通（它怎麼跟你來往）→ 自動化（它什麼時候自己動）**。這篇要講的就是第三層——**溝通，也就是 Channel**。

這篇會聊這些：

* 為什麼 agent 不該只活在終端機
* 兩種溝通模式：你遙控它 vs 它主動回報你
* 模式一：用 Claude Code Remote Control 手機遙控（我的記帳就靠這個）
* 模式二：自己接一隻 Telegram bot 收通知（我的股票訊號就靠這個）
* LINE 怎麼辦？官方 Channel 又是什麼？
* 把 channel 做到極致的開源 agent：OpenClaw 與 Hermes
* 你可以怎麼開始

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。文中這兩套——Remote Control 記帳、Telegram 股票通知——都是我自己天天在跑的，本文是第一手實作紀錄，不是規格表整理。

> 利益揭露：本文沒有業配、沒有聯盟連結。提到的工具（Claude Code、Telegram、OpenClaw、Hermes）都是我自己實際用過或研究過的。

## 為什麼 agent 不該只活在終端機

**一隻只能在終端機操作的 agent，等於一個只能在你辦公桌前找到的員工。** 你一離開電腦，它就停擺。

但真實生活不是這樣運作的。你會在通勤、在開會、在吃飯、在睡前想到事情；你需要被通知的時刻，往往也正好是你不在電腦前的時候（盤中、半夜跑批次、某個監控數字爆掉）。

所以 channel 這層在解決的，其實是一個很樸素的問題：

> **怎麼讓你跟你的 agent，在「你本來就會用的地方」相遇？**

對多數人來說，那個地方就是手機上的通訊軟體。Channel 做的事，就是把 agent 的入口，從「電腦上的終端機」搬到「你口袋裡的 Telegram / LINE」。

## 兩種溝通模式

把 channel 想清楚，其實只有兩個方向：

| 模式 | 方向 | 你在做的事 | 我的真實案例 |
|------|------|-----------|------------|
| **遙控** | 你 → agent | 在手機上下指令，叫電腦上的 agent 幹活 | 對話式記帳 |
| **通知** | agent → 你 | agent 自己跑，遇到事情主動敲你 | 盤中股票訊號 |

大部分實用的 agent，最後都是這兩種混著用：你偶爾下指令遙控它，它平常自己跑、有事才回報你。下面分開講，順便把我自己在跑的兩套攤開來看。

## 模式一：用 Claude Code Remote Control 手機遙控

**如果你用的是 Claude Code，最省事的遙控方式是官方的 Remote Control。**

[Claude Code Remote Control](https://code.claude.com/docs/zh-TW/remote-control)（官方文件）讓你在手機的 Claude App 上，直接跟你桌機上正在跑的 Claude Code session 對話。在終端機裡輸入 `/rc` 開啟，手機 App 切到 Code 分頁，就能即時遙控電腦上的 agent。

重點是：**所有運算和檔案操作還是留在你的電腦上跑，手機只是一個遙控器。** 不需要 SSH、不需要 VPN、不需要把你的專案丟上雲端。

我的[**對話式記帳工作流**](/posts/claude-code-remote-control-conversational-bookkeeping/)就是靠這個。電腦上有一個記帳專案，`CLAUDE.md` 裡寫好記帳規則，然後我在外面用手機講一句：

> 我：剛跟客戶在咖啡廳，咖啡和茶點 480
>
> Claude Code：已記錄 → 業務交際，480 元

它看得懂「跟客戶」要分到業務交際，而不是個人餐飲。整個記帳行為從「打開 App、選分類、填數字、按儲存」變成只剩一句話。

Remote Control 的好處是**幾乎零設定**——它就是 Claude Code 內建的功能，開了就能用。缺點是它偏向「你主動找它」：你得打開 App、找到那個 session。要讓 agent **主動來找你**，就得看第二種模式。

## 模式二：自己接一隻 Telegram bot 收通知

**當你要的是「agent 自己跑、有事主動敲你」，最通用的做法是接一隻 Telegram bot。**

我的[**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/)就是這樣：它盤中每 10 分鐘自己醒來掃一輪，只有當某檔股票「該滿足的條件全部滿足」時，才發一則 Telegram 給我。開頭那則台積電的通知，就是它傳來的。

為什麼選 Telegram 而不是 LINE？因為 **Telegram 的 Bot API 是所有通訊軟體裡最好接的**——免審核、免企業帳號、一個 token 就能發訊息。對自己跑的個人 agent 來說，門檻最低。

### 三步驟做一隻會發通知的 bot

**Step 1：跟 BotFather 要一個 bot**

在 Telegram 搜尋 `@BotFather`，輸入 `/newbot`，照著取名字、設 username（結尾要是 `bot`），它會給你一串 **API Token**。這串就是你 bot 的鑰匙。

**Step 2：拿到你的 chat id**

點進你剛建的 bot、按 Start、隨便傳一句話，然後在瀏覽器打開：

```
https://api.telegram.org/bot<你的Token>/getUpdates
```

在回傳的 JSON 裡找 `chat` 底下的 `id`，那個數字就是你的 **chat id**——agent 要把訊息發到哪裡，靠的就是它。

**Step 3：寫一個最小的 notify 函式**

剩下的就是讓你的 agent 在需要時呼叫一個發訊息的函式。最小可動版本長這樣：

```python
# notify.py — 最小可動的 Telegram 通知
import requests

BOT_TOKEN = "跟 BotFather 要來的 token"
CHAT_ID   = "你剛抓到的 chat id"

def notify(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
    )

if __name__ == "__main__":
    notify("🔔 測試：你的 agent 上線了")
```

就這樣。我的股票 bot 偵測到訊號時，呼叫的就是這種等級的東西，把那則「2330 台積電…」組好字串丟進 `notify()`。**而且這整段 code 我幾乎沒自己寫**——我跟 Claude Code 說「幫我寫一個 notify.py，串 Telegram Bot API，把傳進來的文字發給我」，它就生出來了。

### 一個比 code 更重要的設計原則：通知別太吵

做通知最容易犯的錯，是**什麼都通知**。

我的股票 bot 有一條鐵則：**只有「條件全部滿足」的才發 Telegram，接近但還沒到齊的，只默默寫進 log。**

為什麼？因為通知一旦太吵，你最後一定會把它靜音，那就等於沒做。一個會 cry wolf 的 agent，比沒有 agent 還糟。**好的通知，是你看到它震動就知道「這值得我現在抬頭」。** 設計 channel 的時候，「什麼不該通知」往往比「什麼要通知」更重要。

## LINE 怎麼辦？官方 Channel 又是什麼？

講到這裡你可能會問兩個問題。

**第一，台灣人最多用 LINE，可以嗎？**

可以，但要誠實說：**LINE 官方沒有像 Telegram 那樣對個人開發者友善的 Bot API**，要嘛走 LINE 官方帳號 + Messaging API（設定較繁、有額度限制），要嘛用社群開源的串接方案。我自己是直接用 Telegram，因為對「自己跑的個人 agent」來說它最省事。如果你非 LINE 不可，後面會提到的 OpenClaw 其實內建支援 LINE，可以省掉自己接的功夫。

**第二，Claude Code 不是有官方的 Channel 功能嗎？**

有。Claude Code 的 **Channel** 功能是一套基於 MCP 的訊息推播機制，官方支援 **Telegram 和 Discord**，可以把外部事件即時推進一個正在跑的 Claude Code session，做到「雙向」——你發訊息進去、agent 也能推訊息出來。

那我為什麼還自己接 Telegram bot？因為官方 Channel 目前有個限制：**一個 channel 只能綁一個 session，而且那個 session 必須一直開著**（電腦關機、休眠、terminal 關掉，訊息就不會被處理）。我的股票 bot 是 crontab 定時叫醒的獨立腳本、跑完就結束，不是一個常駐 session，所以自己接一隻 bot 反而更乾淨。

簡單說：

- **想要雙向、又剛好在用 Claude Code 常駐 session** → 官方 Channel 最快
- **agent 是排程跑、跑完就關，只需要單向通知** → 自己接 Telegram bot 最穩
- **只是想用手機下指令遙控** → Remote Control 就夠

選哪個不是信仰問題，是看你的 agent 怎麼活。

## 把 channel 做到極致：OpenClaw 與 Hermes

前面講的是「在現有工具上接 channel」。但有一類開源 agent，是**從骨子裡就把 channel 當核心**設計的，值得認識（這兩隻系列之後會各寫一篇深入，這裡先讓你有概念）。

**[OpenClaw](https://github.com/openclaw/openclaw)** 是一隻 local-first、always-on 的個人助理 agent。它最招牌的就是那層 **Gateway**——一隻 agent 可以同時住在 **20 多個通訊軟體裡**（Telegram、WhatsApp、Slack、Discord、Signal、iMessage，**連 LINE、WeChat 都有**），而且[跨 channel 共用同一套記憶](https://docs.openclaw.ai/channels)。你在 Telegram 跟它講的事，換到 WhatsApp 它也記得。如果你是 LINE 重度使用者，這是少數原生支援 LINE 的選擇。

**[Hermes](https://github.com/NousResearch/hermes-agent)**（Nous Research 開源）則有兩個入口：一個是終端機 UI（`hermes`），另一個是 gateway——同樣能接 [Telegram](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)、Discord、Slack、WhatsApp、Signal、Email。它的重點不在 channel 多，而在「越用越懂你」（這留到 Hermes 那篇講）。

這兩隻告訴我們一件事：**channel 不是 agent 的附加功能，而是它跟世界的介面。** 當你開始認真養 agent，「它住在哪些地方」會變成一個重要的設計決定。

## Channel + 自動化 = 真正的主動

最後補一個關鍵的銜接。

單獨的 channel，還是要有人或有事去觸發。真正讓 agent「主動」起來的，是 **channel（溝通）+ crontab（自動化）** 兜在一起：

> 排程時間到 → agent 自己醒來幹活 → 透過 channel 把結果推給你

我的股票 bot 就是這個組合——crontab 排盤中每 10 分鐘叫醒它，它跑完掃描、有訊號就用 Telegram 敲我。**channel 是嘴巴，crontab 是生理時鐘，兩個加起來才是一隻會自己上工、又會回報的員工。**

crontab 這層怎麼設計，是這個系列接下來會專門寫的一篇。你也可以先回 [**系列總論**](/posts/self-hosted-ai-agent/) 看四層怎麼串。

## 你可以怎麼開始

不用一次到位，照你的需求挑一條路：

1. **只想手機遙控、又在用 Claude Code** → 開 `/rc` Remote Control，五分鐘上手，先把[對話記帳](/posts/claude-code-remote-control-conversational-bookkeeping/)那套抄一遍最有感。
2. **想要 agent 主動通知你某件事** → 跟 BotFather 要一隻 Telegram bot，把上面那段 `notify.py` 抄進你的腳本，先讓它在跑完時跟你說一聲。
3. **想要一隻常駐、多 channel、住在通訊軟體裡的助理** → 去玩玩 OpenClaw。

關鍵心法只有一句：**先讓 agent 能跟你說上話，再慢慢加它要說什麼。** 第一個通知哪怕只是「我跑完了」，那個「手機震一下、是我的 agent」的感覺，會讓你開始想把更多事交給它。

## 常見問題

### Claude Code Remote Control 跟 Channel 差在哪？

**Remote Control 偏「你遙控它」，Channel 偏「雙向訊息推播」。** Remote Control 是你用手機 App 接管桌機 session、像坐在電腦前一樣操作；Channel 是基於 MCP 的訊息管道，可以把外部事件推進 session、也能讓 agent 推訊息出來，官方支援 Telegram 和 Discord。想單純手機操作用 Remote Control，想做「事件進來/通知出去」的雙向流用 Channel。

### 一定要會寫程式才能接 Telegram 嗎？

不太需要。**申請 bot（BotFather）、拿 chat id 都是點一點、複製貼上的事**；唯一的 code 就是那段十行的 `notify.py`，而且你可以直接叫 Claude Code 幫你寫、幫你測。你要做的是看懂它在幹嘛、告訴它哪裡要改。

### 為什麼你選 Telegram 不選 LINE？

純粹因為**對個人 agent 來說 Telegram 最好接**——免審核、一個 token 就能發訊息。LINE 要走官方帳號 + Messaging API，設定較繁、有額度限制。如果你非用 LINE 不可，可以考慮原生支援 LINE 的 OpenClaw，省掉自己串接的功夫。

### 把 token 寫在程式裡安全嗎？

不建議直接寫死。**正式一點的做法是把 `BOT_TOKEN`、`CHAT_ID` 放進環境變數或 `.env` 檔，不要進版控。** 上面範例為了好懂才寫死。另外 Telegram bot 只會發給你設定的 chat id，別人拿不到你的 token 就發不了，所以 token 保管好是重點。

### 我的 agent 是排程跑、跑完就關，適合用哪種？

**自己接一隻 Telegram bot 最穩。** 官方 Channel 需要一個常駐、開著的 session，而排程型 agent（像我的股票 bot 被 crontab 叫醒、跑完就結束）不是常駐的，自己接 bot 發單向通知反而更乾淨可靠。

## 結語

回頭看，channel 這層的價值其實很單純：**它把 agent 從「你要走到電腦前才找得到」，變成「它在你口袋裡隨時找得到你」。**

我自己這兩套——Remote Control 拿來記帳、Telegram bot 拿來收股票訊號——都不是什麼高深的東西，一個是內建功能開個開關，一個是十行 code 加一隻 BotFather 申請的 bot。但它們實實在在地改變了我跟 agent 的關係：**它不再是一個我打開才會用的工具，而是一個我隨時能交辦、也會主動回報我的同事。**

如果你也想養一隻這樣的 agent，但卡在「自己兜不起來」或「沒空慢慢試」，這正是我在做的事——我有提供 [**AI Agent 的諮詢與代建服務**](/ai-automation-workflow/)，幫你看怎麼設計你的 agent，或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第五篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**我的 Claude Code 對話式記帳工作流**](/posts/claude-code-remote-control-conversational-bookkeeping/) — 模式一（Remote Control 遙控）的完整案例
* [**用 Claude Code 打造台股 AI Agent：盤中盯盤、訊號到就發 Telegram**](/posts/claude-code-stock-agent-monitor-alert/) — 模式二（Telegram 通知）的完整案例
* [**用 Claude Code + FinMind 追蹤台股**](/posts/claude-code-finmind-stock-tracking/) — 這一切的起點

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

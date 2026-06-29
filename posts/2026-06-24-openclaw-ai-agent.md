---
title: "OpenClaw 是什麼：用四層觀念，看懂這隻爆紅 AI Agent 的設計 — 自架 AI Agent 實戰（八）"
date: 2026-06-24
author: HoMuChen
category: AI
tags: [AI Agent, OpenClaw, 開源, heartbeat, 自架]
image: https://storage.googleapis.com/homuchen.com/images/openclaw-ai-agent-0.jpg
description: "OpenClaw 是什麼？這隻 2026 爆紅的開源 AI Agent（暱稱『龍蝦🦞』）住在你的 Telegram/WhatsApp 裡、會自己 heartbeat 醒來幹活。繁中安裝教學已經一堆，這篇不重複——我用『自架 AI Agent 四層觀念』帶你看懂它為什麼這樣設計：多 channel、heartbeat、Markdown 檔案記憶、可攜 skill。自架 AI Agent 實戰 #8。"
---

2026 年初，工程圈突然開始流行一句很怪的話：「**你養龍蝦了沒？**」

那隻「龍蝦」就是 **OpenClaw**（logo 是隻龍蝦🦞）——一個 2026 年 1 月底開源、然後在 GitHub 上以誇張速度衝上數十萬星的 AI Agent。它紅到什麼程度？繁體中文的安裝教學、懶人包、評測已經一大票了。

所以這篇我**不打算再寫第 11 篇安裝教學**（那些別人寫得很好了，文末我也會幫你連幾篇）。我想做一件更有價值、也更少人做的事：

> **用這個系列建立的「四層觀念」，帶你看懂 OpenClaw 為什麼長這樣。** 看完你不只會「裝」它，還會「讀懂」它的設計——這對你之後自己組 agent，比照著步驟貼指令有用太多。

前一篇 [**Claude Code vs Codex**](/posts/claude-code-vs-codex/) 我說那兩隻其實很像；而從 OpenClaw 開始的這兩篇（加上下一篇的 Hermes），才是**設計理念真的很不一樣**的對照組。OpenClaw 的特別之處，在於它把我們系列講過的 [**溝通（channel）**](/posts/ai-agent-channels-telegram-line/) 跟 [**自動化（cron）**](/posts/crontab-ai-agent-schedule/) 兩層，推到了極致。

這篇會聊這些：

* OpenClaw 到底是什麼（一句話講清楚）
* 為什麼值得用「觀念框架」看它，而不是只看安裝步驟
* 用四層觀念解剖 OpenClaw：channel、heartbeat、記憶、skill
* heartbeat 為什麼是「cron 的聰明版」
* local-first 的意義，跟它適合 / 不適合誰

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。我自己電腦上長期養著幾隻自架 agent（[**股票盯盤**](/posts/claude-code-stock-agent-monitor-alert/) 那隻就是），OpenClaw 我研究過、也實際跑來玩過，這篇是用我自己組 agent 的經驗去解讀它的設計。

> 利益揭露：本文沒有業配、沒有聯盟連結。OpenClaw 是 MIT 開源專案，我跟它沒有任何利益關係，純粹覺得它的設計值得拿來當教材。

## OpenClaw 是什麼

先一句話講清楚：

> **OpenClaw 是一個開源、跑在你自己機器上的「always-on 個人 AI 助理」——它住在你日常用的通訊軟體裡（Telegram、WhatsApp、Slack…），會自己定時醒來幹活，還能把記憶存成你電腦上的檔案。**

幾個關鍵特徵（截至 2026 年中，[官方 repo](https://github.com/openclaw/openclaw) 為準）：

- **開源、MIT 授權**：核心完全免費，程式攤在陽光下。
- **Local-first（本地優先）**：它跑在你自己的機器上，記憶與資料存成本地的 Markdown 檔，不是丟到別人雲端。
- **住在通訊軟體裡**：透過一個 gateway 接上 Discord、iMessage、Signal、Slack、Telegram、WhatsApp 等十幾種 app，你用平常傳訊息的方式就能指揮它。
- **會自己動（heartbeat）**：有一個「心跳」排程器，定時喚醒它去看狀態、決定要不要行動，不用你戳。
- **能裝技能（skills）**：用一種可攜的 skill 格式擴充能力，社群還能互相分享。
- **門檻不高**：任何能跑 Node.js 22+ 的機器都行——Mac mini、家裡的舊 PC、樹莓派、VPS 都可以。

暱稱「龍蝦」就是這樣來的，社群還很愛講「養龍蝦」——因為它真的像養一隻住在你電腦裡、隨時待命的寵物兼員工。

## 為什麼要用「觀念框架」看它

這裡是這篇跟其他 OpenClaw 文章最不一樣的地方。

大部分教學會帶你「怎麼裝、怎麼設定、怎麼接 Telegram」。這些很實用，但它們很少回答一個更重要的問題：**OpenClaw 為什麼要這樣設計？** 而這個「為什麼」，剛好可以用我們這個系列一路建立的[**四層觀念**](/posts/self-hosted-ai-agent/)完美解釋。

還記得那四層嗎？**Context（它知道什麼）→ 能力（它能做什麼）→ 溝通（它怎麼跟你來往）→ 自動化（它什麼時候自己動）。** OpenClaw 厲害的地方，是它把其中**溝通**跟**自動化**這兩層做到了一般人很難自己兜出來的程度。下面一層一層拆給你看。

## 用四層觀念解剖 OpenClaw

### 溝通（channel）：把 #5 推到極致

我在 [**系列第五篇講 channel**](/posts/ai-agent-channels-telegram-line/) 時說：好的 agent 不該只活在終端機，要住進你日常用的軟體。OpenClaw 根本是把這句話當成它的**核心賣點**。

它最招牌的設計，就是一個「**gateway（閘道器）**」——把十幾種通訊軟體（Telegram、WhatsApp、Slack、Signal、Discord、iMessage…）統一接進來。你在哪個 app 跟它講話都行，它都接得住。**你不用為了用 agent 改變習慣，它直接搬進你已經在用的對話框。** 這正是 channel 這層觀念能想像到的最完整形態。

### 自動化（heartbeat）：#6 cron 的聰明版

這是我最想跟你分享的一點，而且我在 [**系列第六篇講 crontab**](/posts/crontab-ai-agent-schedule/) 時就先埋了伏筆。

還記得 crontab 的天生限制嗎？它是「**死的時間觸發**」——時間到就無腦執行，不管現在該不該做。OpenClaw 的 **heartbeat（心跳）** 把這件事做得更聰明：

> heartbeat 是一個排程器，**定時喚醒 agent，讓它「醒來看一下現在的狀態」，再自己決定要不要行動**——而不是無腦執行固定指令。

（[官方文件](https://docs.openclaw.ai/gateway/heartbeat)說它預設每 30 分鐘跳一次，可調、也可關。）

差別在哪？cron 是「九點到了就跑這個腳本」；heartbeat 是「每隔一段時間醒來看看，有事就處理、沒事就繼續睡」。**它多了一層判斷。** 這就是我在 #6 說的——當你開始嫌 cron 太死板，heartbeat 就是下一站。OpenClaw 把這個概念變成了產品內建的核心機制。

### 記憶：就是 #3 講的「用檔案當記憶」

[**系列第三篇講記憶**](/posts/ai-agent-memory-file-system/) 時，我主張最樸素也最強的記憶方案就是「把知識寫成檔案」。OpenClaw 完全是這個信仰的實踐者——**它的記憶與資料，就存成你硬碟上的 Markdown 檔。**

這不只是技術選擇，更是哲學選擇：你的資料看得到、改得動、備份方便、而且**不出你的機器**。跟我那隻股票 agent 用 `data/` 資料夾當記憶，是一模一樣的思路。

### 能力：可攜的 skill（#4）

最後，[**系列第四篇講能力**](/posts/mcp-tools-skills/) 時提到的 skill，OpenClaw 也有——而且做成一種**可攜、可分享**的格式，社群可以互相交換技能。要它多會一件事，裝個 skill 就好，跟我們講的「skill 是教 agent 怎麼做事的工作流文件」完全呼應。

一張表把上面收攏起來，你就有 OpenClaw 的完整骨架了：

| 四層觀念 | OpenClaw 的實作 | 對應系列篇 |
|---------|----------------|-----------|
| **溝通（channel）** | gateway 接 14+ 通訊軟體，住進你已在用的對話框 | [#5 channels](/posts/ai-agent-channels-telegram-line/) |
| **自動化** | heartbeat 定時醒來、看狀態再決定行動 | [#6 crontab](/posts/crontab-ai-agent-schedule/) |
| **Context（記憶）** | 記憶存成本地 Markdown 檔 | [#3 memory](/posts/ai-agent-memory-file-system/) |
| **能力** | 可攜、可分享的 skill 格式 | [#4 MCP/Tools/Skills](/posts/mcp-tools-skills/) |

> 看到這你應該有感覺了：**OpenClaw 不是什麼魔法，它就是把我們系列講的四層觀念，每一層都做出一個漂亮的實作。** 你懂了四層，就等於懂了它的骨架。

## local-first 的意義：資料不出門

特別講一下「local-first」這件事，因為這是 OpenClaw（以及下一篇 Hermes）很核心的價值主張。

跑在你自己機器上、記憶存本地、還能搭配[**本地模型**](/posts/self-hosted-ai-agent/)（像 Ollama），意味著——**你的對話、你的資料、你交辦的事，可以完全不離開你的電腦。** 對於在意隱私、或處理敏感資料的人，這是雲端 SaaS 給不了的安全感。當然你也可以接 GPT / Claude 這種商業模型（效果更好但資料會經過雲端），這是你自己的取捨。

這也呼應了整個[**自架 AI Agent**](/posts/self-hosted-ai-agent/)系列的精神：**把 agent 養在自己家，主控權在你手上。**

## 適合誰、不適合誰

老實說，OpenClaw 不是萬靈丹。給你一個誠實的判斷：

**適合你，如果——**
- 你想要一隻**住在手機通訊軟體裡、隨時待命**的個人助理。
- 你喜歡 always-on、會自己醒來幹活的感覺（heartbeat 那種）。
- 你在意資料隱私，想要 local-first、甚至接本地模型。
- 你願意花一點時間設定（它不難，但不是零設定）。

**可能還不適合你，如果——**
- 你只是想要一隻「寫程式的 agent」——那 [**Claude Code 或 Codex**](/posts/claude-code-vs-codex/) 更對口。
- 你完全不想碰任何設定、連 Node.js 都不想裝——那可能先從 GUI 的 [**Claude Cowork**](/posts/claude-cowork-ai-from-chat-to-work/) 入門更輕鬆。
- 你的需求很單一（只要定時抓個資料）——那自己寫支 script 配 [**crontab**](/posts/crontab-ai-agent-schedule/) 可能更簡單，殺雞不用牛刀。

## 你可以怎麼開始

這篇我刻意不寫安裝步驟（網路上已經很多寫得很好的），但給你一個務實的上手順序：

1. **先看官方** [**OpenClaw repo**](https://github.com/openclaw/openclaw) **跟** [**官方文件**](https://docs.openclaw.ai/)，確認你的機器能跑（Node.js 22+）。
2. **繁中入門教學**可以參考 [grenade 的這篇](https://grenade.tw/blog/openclaw-ai/) 或 [ohya 的完整指南](https://ohya.co/blog/openclaw-complete-guide-2026)，跟著裝一遍。
3. **先接一個你最常用的 channel**（台灣很多人用 Telegram），讓它能跟你對話。
4. **heartbeat 先關著或設長一點**，等你信任它了再縮短——別一上來就讓它每 30 分鐘自己亂跑。

關鍵心法：**帶著「四層觀念」去裝它。** 你每設定一個東西，問自己「這是在設哪一層？」——接 Telegram 是溝通層、開 heartbeat 是自動化層、給它 skill 是能力層。這樣你裝完不只會用，還真的懂了。

## 常見問題

### OpenClaw 是什麼？

**OpenClaw 是一個開源（MIT）、跑在你自己機器上的 always-on 個人 AI 助理，暱稱「龍蝦🦞」。** 它透過一個 gateway 接上 Telegram、WhatsApp、Slack 等十幾種通訊軟體，讓你用傳訊息的方式指揮它；還能靠 heartbeat 定時自己醒來幹活、把記憶存成本地 Markdown 檔。2026 年 1 月底開源後在 GitHub 爆紅。

### OpenClaw 跟 Claude Code / Codex 有什麼不一樣？

**定位不同。** [**Claude Code / Codex**](/posts/claude-code-vs-codex/) 是 terminal-native 的泛用（偏 coding）agent，你主動下指令它才動；OpenClaw 是 always-on 的**個人助理**，住在你的通訊軟體裡、會自己 heartbeat 醒來主動幹活。前者像「你打開來用的工具」，後者像「住在你家、隨時待命的員工」。

### OpenClaw 的 heartbeat 是什麼？跟 crontab 差在哪？

**heartbeat 是 OpenClaw 內建的排程器，定時喚醒 agent 去看狀態、再自己決定要不要行動。** 跟 [**crontab**](/posts/crontab-ai-agent-schedule/) 的差別是：cron 是「時間到就無腦執行固定指令」，heartbeat 是「時間到先醒來看看、再聰明地決定做不做」，多了一層判斷。可以把它想成 cron 的進化版。預設每 30 分鐘跳一次，可調可關。

### OpenClaw 免費嗎？資料安全嗎？

**核心程式 MIT 開源、完全免費。** 它是 local-first，記憶與資料存在你自己機器上的 Markdown 檔，不出你的電腦——這是它主打的隱私優勢。費用主要來自你接的 AI 模型：接 GPT / Claude 商業 API 會依用量計費；若改接本地模型（如 Ollama）則可做到幾乎零模型成本、資料完全不出門。

### 我需要會寫程式才能用 OpenClaw 嗎？

需要一點點。**它要求你的機器能跑 Node.js 22+、會照文件做基本設定**，但不需要你自己寫程式。如果你連終端機都不想碰，建議先從 GUI 的 [**Claude Cowork**](/posts/claude-cowork-ai-from-chat-to-work/) 入門，觀念相通、之後再進階到 OpenClaw 這種自架方案。

## 結語

OpenClaw 會爆紅不是沒道理——它把「在自己電腦養一隻會自己幹活的 AI 員工」這件事，做成了一個任何人都能裝起來的產品。但我更想讓你帶走的，不是「我裝了龍蝦」，而是——

> **你已經有能力「讀懂」它了。** channel、heartbeat、檔案記憶、skill，這些它的招牌設計，全都是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 一路講過的四層觀念。看懂框架，你看任何一隻 agent 都會變透明。

下一篇要講的 [**Hermes**](/posts/self-hosted-ai-agent/)，跟 OpenClaw 是很有意思的對照：OpenClaw 把「溝通＋自動化」推到極致，做成一隻 always-on 的貼身助理；而 Hermes 走的是另一條路——把「**記憶＋自我改進**」推到極致，做成一隻**越用越強、會自己長出新技能**的 agent。兩隻的設計哲學，剛好補上光譜的兩端。

如果你看完想養一隻像 OpenClaw 這樣的 agent，但卡在「設定兜不起來」或「想客製成我自己的工作流」——這正是我在做的事。我有提供 [**AI Agent 的諮詢顧問與代建服務**](/ai-automation-workflow/)，幫你看怎麼設計、或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第八篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**用 Telegram / LINE 遙控你的 AI Agent、收任務通知**](/posts/ai-agent-channels-telegram-line/) — 系列 #5，OpenClaw 的 channel 就是這層的極致
* [**用 Crontab 讓 AI Agent 自己定時開工**](/posts/crontab-ai-agent-schedule/) — 系列 #6，heartbeat 是 cron 的聰明版
* [**AI Agent 的記憶與檔案系統：memory、檔案記錄、漸進式揭露**](/posts/ai-agent-memory-file-system/) — 系列 #3，OpenClaw 用 Markdown 當記憶的同一套思路

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

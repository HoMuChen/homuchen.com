---
title: "自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工"
date: 2026-06-02
author: HoMuChen
category: AI
tags: [AI Agent, Claude Code, 自動化, Agentic AI]
image: https://storage.googleapis.com/homuchen.com/images/self-hosted-ai-agent-0.jpg
description: "我電腦上固定跑著五隻 AI agent：幫我記帳、盯盤、分析 SEO、顧電商訂單、維護個人 wiki。這篇是「自架 AI Agent 實戰」系列總論，用一隻會自己盯盤的 agent 拆解自主 agent 的四層結構，以及為什麼 2026 你該自己養一隻。"
---

前幾天盤中，我手機震了一下。

是我電腦上那隻股票 bot 傳來的：某檔股票觸發了我設定的訊號，它附上當下的價量、算好的指標、還有一句「要不要看一下」。

重點是——**那個當下我根本沒坐在電腦前，也沒打開任何程式。** 它自己在盤中每隔幾分鐘醒來看一次行情，收盤後自己去補資料、跑分析，偵測到我關心的訊號才主動敲我。

我愣了一下，然後意識到一件事：這隻 bot 已經不像是「我打開來用的工具」了，比較像是**住在我電腦裡、會自己開工的員工**。

這篇是「**自架 AI Agent 實戰**」系列的第一篇，也是整個系列的地圖。我想先把一個問題講清楚：

> 什麼叫「自架一隻能自主幹活的 AI Agent」？它跟 ChatGPT、跟雲端的 AI 產品差在哪？要自己養一隻，到底需要哪些東西？

這篇會聊這些：

* 「自架自主 agent」到底是什麼，跟 chatbot、雲端 AI 產品差在哪
* 為什麼是 2026 這個時間點
* 拆解一隻 agent 的四層結構：**Context → 能力 → 溝通 → 自動化**
* 用我那隻股票 bot 當例子，走完這四層
* 講老實話：它沒有電影那麼科幻
* 你可以怎麼開始（以及這個系列接下來會寫什麼）

---

## 先分清楚：chatbot、雲端 AI 產品、自架 agent

很多人講「AI Agent」其實講的是三種很不一樣的東西，我們先把它們分開。

**第一種：chatbot。** 你問一句，它答一句。像 ChatGPT 的對話框，你不問它就不動，答完就結束。它很聰明，但它是被動的。我之前在 [**AI Agent 到底是什麼？跟 ChatBot 差在哪**](/posts/what-is-ai-agent-vs-chatbot/) 這篇有用「問路人 vs 助理」的比喻講過——chatbot 像問路人，agent 像助理。

**第二種：雲端 AI 產品。** 別人做好的 SaaS，你登入、付月費、用它規定好的功能。好處是開箱即用，壞處是它能做的事被框死了，你的資料也在別人的伺服器上。

**第三種，也是這個系列的主角：自架自主 agent。** 它跑在**你自己的電腦或工作站**上，你給它目標和工具，它自己規劃步驟、動手執行、檢查結果。它能讀寫你的檔案、執行指令、上網查資料、定時自己開工，做完再回報你。

差別在哪？簡單說：

> chatbot 是「會聊天的腦袋」，雲端產品是「別人替你綁好的雙手」，**自架 agent 是「住在你家、聽你的、用你的工具、替你幹活的那個人」。**

整理成一張表會更清楚：

| | chatbot | 雲端 AI 產品 | 自架自主 agent |
|---|---|---|---|
| 跑在哪 | 別人的伺服器 | 別人的伺服器 | **你自己的電腦/工作站** |
| 誰決定能做什麼 | 你問什麼答什麼 | 產品框死的功能 | **你給目標，它自己規劃** |
| 能不能讀寫你的檔案 | 不行 | 看產品 | **可以** |
| 會不會自己開工 | 不會 | 不會 | **排程到了自己跑** |
| 資料在誰手上 | 對方 | 對方 | **你自己** |

如果你完全不想碰終端機，想用圖形介面的方式體驗這件事，我之前寫的 [**Claude Cowork — 當 AI 從聊天變成工作**](/posts/claude-cowork-ai-from-chat-to-work/) 是比較親民的入口。而這個系列要走的是 builder 路線：我們要自己動手，把一隻 agent 從零組起來。

## 為什麼是 2026？

幾年前要做到「一隻會自己幹活的 agent」，你得自己接一堆 API、寫一堆膠水程式、處理一堆瑣碎的工程。門檻高到大部分人會直接放棄。

2026 變了，原因有三個：

1. **模型夠強了。** 現在的模型不只會回答問題，還會「規劃」。你給它一個目標，它會自己拆成步驟。我在 [**AI Agent 怎麼「思考」**](/posts/ai-agent-how-it-thinks/) 那篇拆解過這個流程。
2. **工具成熟了。** Claude Code、Codex 這類能直接在你電腦上跑、能讀寫檔案執行指令的 agent runner 出現了，把最難的那層膠水都包好了。
3. **開源也跟上了。** OpenClaw、Hermes 這些開源專案，讓你可以把 agent 接到通訊軟體、定時排程、甚至用本地模型跑到「資料完全不出門」。

我自己的體感是：這一年我的產出整個翻倍，不是因為我打字變快，而是**有東西在替我做事**。這件事我在 [**五月才過七天，我快有 500 個 commits**](/posts/ai-labor-not-tool-500-commits/) 那篇講得更白——AI 對我來說已經不是工具，是勞動力。

那一隻能自主幹活的 agent，到底由什麼組成？這就是這個系列要一層一層拆的東西。

## 我電腦上現在養了五隻

在開始拆解之前，先讓你知道我不是在講空話。我電腦上現在固定在跑五隻 agent：

1. **記帳 agent**——手機傳一句「中午便當 120」，它自動分類寫進檔案，想看圖隨時生。分類正確率約 9 成，分錯下次糾正就學會。（[**對話式記帳工作流**](/posts/claude-code-remote-control-conversational-bookkeeping/)）
2. **股市策略研究 agent**——也就是這篇的主角：盤前自動選股、盤中每 10 分鐘盯盤、偵測訊號就發 Telegram 通知我。（完整做法：[**用 Claude Code 打造台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/)；資料層的前身：[**FinMind 股票追蹤**](/posts/claude-code-finmind-stock-tracking/)）
3. **SEO 分析 agent**——接 Search Console，定期分析我哪些文章在掉、該更新哪篇。（[**Search Console SEO 分析**](/posts/claude-code-search-console-seo-analysis/)）
4. **電商助理 agent**——接 Shopify Admin API，幫我查訂單、整理商品資料。（[**Shopify 電商助理**](/posts/claude-code-shopify-admin-api-ecommerce-assistant/)）
5. **個人 wiki agent**——幫我維護一個自己長大的知識庫，讀過的東西它幫我記、幫我連。（[**LLM 維護的個人 wiki**](/posts/llm-maintained-personal-wiki/)）

這五隻長得不一樣，但拆開來看，**它們的骨架是同一套**。接下來就講這套骨架。

## 一隻 agent 的四層結構

我把一隻自架 agent 拆成四層，剛好對應你要給它的四種東西：

> **Context（它知道什麼）→ 能力（它能做什麼）→ 溝通（它怎麼跟你來往）→ 自動化（它什麼時候自己動）**

下面我用那隻股票 bot 當例子，一層一層走給你看。它原本只是 [**用 Claude Code + FinMind 追蹤股票**](/posts/claude-code-finmind-stock-tracking/) 那篇裡的雛形，後來我加上 crontab 跟一些 scripts，它就長成現在這隻會自己盯盤的員工了。

### 第一層：Context — 它知道什麼

Context 是一隻 agent 的根基，它又分成兩塊。

**一是 Instruction，agent 的「憲法」。** 我寫了一份指令給股票 bot：它該關心哪些訊號、風險邊界在哪、算出來要用什麼格式回報我、什麼情況該主動敲我、什麼情況閉嘴就好。指令寫得好不好，幾乎決定了這隻 agent 靠不靠譜。完整做法（好 vs 壞 instruction、該寫哪五塊、`CLAUDE.md` / `AGENTS.md` 怎麼擺）我整理在 [**系列第二篇：怎麼寫 AI Agent 的「憲法」**](/posts/agent-instruction-claude-md/)。

**二是 Memory 與檔案，agent 的「記憶」。** 模型本身是會「失憶」的——每次對話結束，它就忘了。所以我讓 bot 把每天的行情、算好的指標、判斷的理由，**通通寫進檔案**。久了這些檔案就變成它的資料庫。而且我用「索引檔連到細節檔」的方式組織，讓它每次只讀需要的那部分，不用一次把所有東西塞進腦袋——這招叫**漸進式揭露（progressive disclosure）**。我那篇 [**讓 LLM 自己維護的個人 wiki**](/posts/llm-maintained-personal-wiki/) 就是同一套思路的應用。完整做法（context window 為什麼不是記憶、用檔案當記憶、漸進式揭露怎麼做）我整理在 [**系列第三篇：AI Agent 的記憶與檔案系統**](/posts/ai-agent-memory-file-system/)。

### 第二層：能力 — 它能做什麼

光有腦袋和記憶還不夠，agent 得能「動手」。動手的能力來自三種東西：**Tools、MCP、Skills**。

- **Tools** 是單一動作：抓一次股價、寫一個檔案、跑一段計算。
- **MCP** 是一條標準管道，讓 agent 連到外部世界——我的股票 bot 透過它接上 FinMind 拿資料。
- **Skills** 是教它「怎麼做」的工作流文件：先抓哪些資料、怎麼算、什麼門檻算訊號。

用個比喻：MCP 是食材庫和設備，Skill 是食譜和手藝。**MCP 是管道，Skill 是流過管道的水**，兩個一起，agent 才會做菜。

### 第三層：溝通 — 它怎麼跟你來往

agent 不該只活在終端機裡，不然你得一直盯著螢幕。它要能在你**日常用的軟體**裡跟你來往。

我的股票 bot 偵測到訊號，就直接傳訊息到我手機。台灣最順手的是 LINE，國際上很多人用 Telegram，Claude Code 本身也有遠端遙控功能，可以用手機app指揮電腦上的 agent。我那套 [**手機對話式記帳工作流**](/posts/claude-code-remote-control-conversational-bookkeeping/) 就是這層的代表作——一句「中午便當 120」，agent 自動分類寫檔。

溝通有兩個方向：**你下指令遙控它**，以及**它主動回報通知你**。兩個方向都接上，這隻 agent 才算真的住進你的生活。完整做法（Remote Control 遙控、自己接 Telegram bot 收通知、LINE 與官方 Channel 的取捨）我整理在 [**系列第五篇：用 Telegram / LINE 遙控你的 AI Agent**](/posts/ai-agent-channels-telegram-line/)。

### 第四層：自動化 — 它什麼時候自己動

最後一層，也是讓 agent 從「我叫它它才動」變成「它自己會開工」的關鍵：**排程**。

最基本的工具就是老牌的 **crontab**。我用它讓股票 bot 盤中每隔幾分鐘醒來看一次行情、收盤後自己去補資料跑分析。它不再需要我打開、不再需要我下指令，**時間到了它自己上工**。完整做法（crontab 入門、把指令換成 agent、跟 Claude 雲端 Routines 的取捨）都在 [**系列第六篇：用 Crontab 讓 AI Agent 自己定時開工**](/posts/crontab-ai-agent-schedule/)。

這一層接上之後，前面三層才真正活起來：到點自動跑（自動化）→ 用工具完成任務（能力）→ 把結果寫進檔案（記憶）→ 偵測到訊號傳到我手機（溝通）。一隻完整的、會自己幹活的 agent，就是這四層轉起來的樣子。

## 講點老實話：它沒有電影那麼科幻

寫到這裡，我得誠實一下，免得你期待錯方向。

常有人問我：「它會不會自己亂搞、自己做一堆你沒叫它做的事？」

老實說……**還好欸 XD。** 我這幾隻 agent 最讓我滿意的地方，其實就是「**好好把我交代的事做完**」而已。它不會自己暴衝，也不會給我驚喜亂入。

唯一比較「聰明」的時刻，是在**規劃階段**——當我交代一件事，它有時會提出一些我原本沒想到的建議、補上我漏掉的步驟。就這樣，這樣對我來說就已經很夠了。

所以別被科幻電影帶歪了。自架 agent 的價值不是「它有自我意識」，而是**它可靠、它不會累、它時間到了就上工、它把你教它的流程一絲不苟地重複執行**。把它當成一個認真、聽話、還會提醒你的員工，期待值就抓對了。

## 你可以怎麼開始

如果這篇讓你也想養一隻，我的建議是：

**別想一次到位。** 不要一開始就想做出那種四層全開、會自己盯盤的怪物。先挑一件你每天/每週都要做、又有點煩的重複工作——記帳、整理檔案、抓某個網站的資料——讓 agent 先把這一件做好。

然後再一層一層加上去：先給它清楚的指令，再讓它把結果寫進檔案，接著接上工具、接上通知，最後排個 crontab 讓它自己跑。**這個系列接下來就是照這個順序，一篇一篇手把手帶你做。**

### 「自架 AI Agent 實戰」系列地圖

這個系列預計這樣走（後面每篇上線後，我會回來把連結補上）：

**觀念篇**

1. 系列總論：在自己電腦養一隻會自己開工的 AI 員工（就是這篇）
2. [**Agent Instruction：怎麼寫 agent 的「憲法」**](/posts/agent-instruction-claude-md/)
3. [**Memory 與檔案系統：記憶、檔案記錄、漸進式揭露**](/posts/ai-agent-memory-file-system/)
4. MCP / Tools / Skills：agent 的三種能力擴充
5. [**用 Telegram / LINE 遙控你的 agent、收任務通知**](/posts/ai-agent-channels-telegram-line/)
6. [**用 Crontab 讓 agent 自己定時開工**](/posts/crontab-ai-agent-schedule/)

**工具篇**（同樣的觀念，在不同工具上怎麼實現）

7. Claude Code vs Codex：監督式 vs 全自動的 CLI 泛用 agent
8. OpenClaw：always-on、會 heartbeat、住在通訊軟體裡的 agent
9. Hermes：會自我改進的 agent——記憶與自動長技能的設計理念

**案例篇**：把上面的觀念落到真實專案（記帳、[**盯盤**](/posts/claude-code-stock-agent-monitor-alert/)、SEO 分析、電商、個人 wiki）。

## 結語

把 AI 從「我打開來用的工具」，變成「住在我電腦裡、會自己開工的員工」——這就是自架 agent 這件事最迷人的地方。

而拆開來看，一隻能自主幹活的 agent 其實沒那麼神秘，就是四層：**它知道什麼（Context）、它能做什麼（能力）、它怎麼跟你來往（溝通）、它什麼時候自己動（自動化）。** 接下來整個系列，我們就一層一層把它組起來。

如果你看完想自己動手，但卡在「不知道從哪一層開始」或「想做的東西有點複雜、自己搞不定」——這其實正是我在做的事。我有提供 [**AI Agent 的諮詢顧問與代建服務**](/ai-automation-workflow/)，幫你看你的需求適合怎麼設計，或是直接幫你做出來。我接個人戶、也接中小企業（沒有要服務超級大公司啦😂）。想了解可以看 [**服務說明**](/ai-automation-workflow/)，或直接下面加我 LINE 聊聊。

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

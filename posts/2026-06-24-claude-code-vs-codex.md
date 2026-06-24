---
title: "Claude Code vs Codex：兩隻終端機 AI Agent，其實比你想的像 — 自架 AI Agent 實戰（七）"
date: 2026-06-24
author: HoMuChen
category: AI
tags: [AI Agent, Claude Code, Codex, CLI, AI coding]
image: https://storage.googleapis.com/homuchen.com/images/claude-code-vs-codex-0.jpg
description: "Claude Code vs Codex 該選哪個？我兩個都天天在用，老實說——它們比你想的像：都能 plan 先審、都能 full-auto 放手、都能 sandbox。真正的差別不是『監督 vs 全自動』，而是模型家族、生態系、加上少數 emphasis（hooks 治理 vs kernel sandbox）。這篇幫你看懂真正該怎麼選。自架 AI Agent 實戰 #7。"
---

「Claude Code 跟 Codex，到底要用哪個？」

這大概是我最近被問到爛的問題。每次有人知道我在自己電腦上養 agent，十之八九都會接著問這句。而我的答案，可能跟你在很多比較文看到的不太一樣——**老實說，這兩隻比大家以為的「像」太多了。**

網路上很愛把它們寫成「設計哲學的對決」，好像一個天生謹慎、一個天生放飛。但我兩個都天天在用，越用越覺得：**它們其實是同一類工具，能做的事、運作的方式高度重疊。** 真正該煩惱的差別，根本不是那些行銷話術講的東西。

這篇我想誠實地拆給你看——它們到底哪裡像、哪裡才是真的不一樣、以及你該怎麼選。

前面六篇，我們把一隻自架 agent 的[**四層觀念**](/posts/self-hosted-ai-agent/)（Context → 能力 → 溝通 → 自動化）都講完了。從這篇開始進入**工具篇**，第一棒就用大家最常碰到的兩隻泛用 agent——**Claude Code 與 Codex**——當對照組。

這篇會聊這些：

* 一個反直覺的結論：它們其實很像（都能 plan、都能 full-auto、都能 sandbox）
* 為什麼大家會以為它們很不同
* 真正的差別在哪：模型家族、生態系、少數 emphasis
* 用「股票分析」任務看，差別到底有沒有感
* 那到底該怎麼選＋為什麼有人兩個都用

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。Claude Code 和 Codex 我自己都付費天天在用，本文是第一手使用心得——包括「它們其實很像」這個跟主流比較文不太一樣的結論。

> 利益揭露：本文沒有業配、沒有聯盟連結。兩隻工具都是我自己付費在用的，會盡量講平衡——不吹任何一邊。

## 反直覺的結論：它們其實很像

先講最重要、也最可能顛覆你印象的一點：**Claude Code 和 Codex 的運作模式高度重疊。** 你以為的「一個監督、一個全自動」，其實兩隻都做得到。

直接把核心功能擺一起看：

| 能力 | Claude Code | Codex |
|------|-------------|-------|
| **Plan mode（先出計畫等你審）** | 有（plan 模式） | 有（先寫計畫、你簽核才動） |
| **逐步詢問（每個動作問你）** | 有（default 預設就是問） | 有（suggest 預設就是問） |
| **全自動放手（不問一路做完）** | 有（auto mode、`--dangerously-skip-permissions`） | 有（`--full-auto`、bypass） |
| **Sandbox 隔離** | 有 | 有（OS kernel 層） |
| **吃指令檔** | `CLAUDE.md` | `AGENTS.md` |
| **MCP / script / skill** | 都支援 | 都支援 |

看出來了嗎？**「先審再做」還是「放手全自動」，在兩隻身上都只是一個可以調的設定，不是它們各自的天性。** 你可以把 Claude Code 開成全自動、也可以把 Codex 設成每步都問你。它們是同一條光譜上、可以自由滑動的兩隻工具，不是光譜兩端的兩種物種。

> 所以如果有人跟你說「Claude Code 是監督式、Codex 是全自動」——那是把預設值跟行銷印象當成本質。實際上兩隻都能監督、都能全自動。

（不信可以對照官方文件：[Claude Code 的 permission modes](https://code.claude.com/docs/en/permission-modes) 從 default→acceptEdits→plan→bypass 一路可調；[Codex 的 approval modes](https://developers.openai.com/codex/agent-approvals-security) 從 suggest→auto-edit→full-auto 也是一整排。兩邊根本是鏡像。）

## 那為什麼大家以為它們很不同？

因為**早期的第一印象**還沒更新。

Codex 剛紅的時候主打「雲端、full-auto、丟了再回來收」，Claude Code 早期則主打「plan mode、hooks、讓你把關」。於是大家腦中就刻下「一個放飛、一個謹慎」的印象。

但這一兩年它們**互相抄作業、瘋狂收斂**：Claude Code 後來補上了 auto mode（甚至用一個分類器模型幫你即時把關，讓你能安心放手長跑）；Codex 也一直有 plan、有逐步審核模式。**該有的對方都補上了。** 所以那個「哲學對立」的印象，其實是停留在舊版的記憶。

這也是為什麼我覺得多數比較文有點誤導——它們還在複述兩年前的差異。

## 真正的差別在哪

那它們就完全一樣？也不是。把表面的「監督 vs 全自動」拿掉之後，剩下的才是**真正值得你拿來做決定**的差別：

### 1. 模型家族（這才是最大的體感差）

Claude Code 跑的是 Claude、Codex 跑的是 GPT。**你每天感受到的「它聰不聰明、合不合拍」，九成來自背後的模型，而不是 CLI 本身。** 不同模型在不同任務上手感不同——這是最該在意、卻最常被比較文跳過的點。

### 2. Emphasis 與深度（強調的東西不同）

兩隻都有的功能，投入的深度不一樣：

- **Claude Code 的 hooks 治理更深**：它的生命週期攔截點多，適合做細緻的「程式化規矩」（像 [**#2 instruction**](/posts/agent-instruction-claude-md/) 之外再加一層自動防呆）。
- **Codex 更強調 OS kernel 級 sandbox**：安全隔離做在作業系統核心層，放手讓它衝時更有底。

注意：是**強調點不同**，不是「一個有一個沒有」。

### 3. 生態系與訂閱

Claude Code 在 Anthropic 生態（還有 GUI 版的 Claude Cowork）；Codex 綁 OpenAI 的 ChatGPT 方案。**你本來就付費在用哪一家，往往直接決定了你該先用哪隻**——這個現實因素，比任何 benchmark 都實際。

### 4. Benchmark（看方向就好）

跑分會一直變，抓大方向（截至 2026 年中）：**SWE-bench 上兩邊基本打平**；**終端機原生任務（Terminal-Bench）Codex 略強**。想看詳細數字參考 [Morph 的比較](https://www.morphllm.com/comparisons/codex-vs-claude-code)，但別讓零點幾分綁架你——那不是你天天有感的東西。

## 用「股票分析」走一遍，差別有感嗎？

抽象的講完，用我熟的場景試試。假設我要做一隻[**分析台股的 agent**](/posts/claude-code-stock-agent-monitor-alert/)，同一個需求「幫我把這檔股票的訊號分析做出來」——

老實說，**兩隻做起來的流程幾乎一樣**：都可以先 plan 給我看、我點頭後它去讀 FinMind 資料（[**跑我寫的 script**](/posts/mcp-tools-skills/)）、算指標、判斷訊號、整理結果。我要它一步步問、或要它整套自動跑，兩隻也都設定得出來。

真正讓我「換著用」的原因其實是：**想試試不同模型對同一份盤勢的判斷有沒有不一樣**、以及**哪家的訂閱額度還夠**。你看，連我自己的實際取捨，都落在「模型 + 訂閱」，而不是「監督 vs 全自動」。

## 那到底該怎麼選

把上面收斂成可以行動的判斷：

| 你的情況 | 建議 |
|---------|------|
| **已經在付費用 Claude / ChatGPT 其中一家** | 直接用對應的那隻，別折騰 |
| **重視 hooks 那種細緻的程式化治理** | 偏 Claude Code |
| **工作很「終端機」（DevOps、腳本、CLI），想要 kernel 級隔離** | 偏 Codex |
| **想比較不同模型對同任務的判斷** | 兩隻都裝，交叉用 |
| **完全沒包袱、只想挑一隻入門** | 隨便挑一隻都行，它們夠像，學會一隻另一隻很快上手 |

我的真心話：**先別糾結。** 挑你手上訂閱有的那隻、或隨便挑一隻先做出東西來，比你研究三天比較文有用得多。它們夠像，你之後要換、要兩隻併用都不難。

## 不想碰 CLI 的人怎麼辦

這系列從頭到尾偏 builder、要碰終端機。但我知道有些朋友看到 CLI 就頭痛——沒關係，這條路也有 GUI 版本。

Claude 有桌面版的 **Claude Cowork**，把同一套「AI 幫你做事」的能力包成圖形介面，不用打指令也能用。我寫過一整個 [**Claude Cowork 系列**](/posts/claude-cowork-ai-from-chat-to-work/)，就是給不想碰 CLI 的人看的。**觀念是相通的——只是換個比較親切的門進來。**

## 為什麼有人兩個都用

既然它們這麼像，幹嘛兩個都裝？我自己的理由很實際：

- **想要兩家模型的手感**：同一個任務，偶爾換另一隻看看不同模型的判斷，等於多一個第二意見。
- **額度分流**：一家訂閱額度用完了，還有另一家可以頂著。
- **少數 emphasis 任務**：要做很細的 hooks 治理就開 Claude Code，要 kernel 級隔離放手跑就用 Codex。

> 但說真的，**對絕大多數人，一隻就夠了。** 兩個都用是進階玩法，不是必須。別因為「聽說要兩個都用」就給自己找麻煩。

## 你可以怎麼開始

別想太多，照這個順序最不會卡：

1. **看你手上有哪家訂閱**——有 Claude 就先 Claude Code、有 ChatGPT 就先 Codex。沒有的話隨便挑一隻。
2. **拿一個小任務真的跑一遍**——讓它幫你寫個小腳本、整理個檔案，感受它的工作流。
3. **想要的時候再把另一隻補上**——因為它們夠像，第二隻幾乎沒有學習成本。

關鍵心法：**它們是同一類工具的兩個品牌，不是兩種哲學。** 與其糾結選哪個，不如先動手——你會發現重點從來不是工具，是你怎麼用它。

## 常見問題

### Claude Code 跟 Codex 最核心的差別是什麼？

**比你想的小。** 兩隻都能 plan 先審、都能 full-auto 放手、都能 sandbox、都吃指令檔與 MCP/skill——「監督 vs 全自動」只是可調設定，不是天性。真正的差別是：**背後的模型家族（Claude vs GPT）、生態系與訂閱、以及少數強調點（Claude Code 的 hooks 治理更深、Codex 的 kernel sandbox 更強）。**

### Claude Code 和 Codex 該選哪個？

**最實際的判準是「你已經在付費用哪家模型」**——有 Claude 訂閱就用 Claude Code，有 ChatGPT 就用 Codex。其次：想要細緻 hooks 治理偏 Claude Code、工作很終端機且要 kernel 隔離偏 Codex。它們夠像，先挑一隻動手做比研究比較文有用，之後要換不難。

### 它們真的差很多嗎？我看比較文講得很不一樣。

多數比較文還停在**兩年前的印象**（那時 Codex 主打雲端 full-auto、Claude Code 主打 plan）。但這一兩年兩隻互相補齊、高度收斂：Claude Code 補了 auto mode、Codex 一直有 plan 與逐步審核。**現在該有的對方大多都有了**，所以差異比那些文章講的小很多。

### Claude Code 和 Codex 可以一起用嗎？

可以，但**不是必須**。兩個都用的好處是：拿到兩家模型的手感（多個第二意見）、額度分流、以及少數 emphasis 任務各取所長。但對絕大多數人，**一隻就夠了**，別為了「聽說要兩個都用」自找麻煩。

### 不會用終端機 / CLI，也能用嗎？

可以。Claude 有桌面 GUI 版的 **Claude Cowork**，不用打指令也能用同一套「AI 幫你做事」的能力，我寫過 [**Claude Cowork 系列**](/posts/claude-cowork-ai-from-chat-to-work/) 給不想碰 CLI 的人。觀念相通，建議先用 GUI 入門、之後再進階到 CLI 自架。

## 結語

繞了一圈，Claude Code 與 Codex 的真相，其實有點反高潮：**它們沒有你以為的那種哲學對立，反而越長越像。** 該 plan 的都能 plan、該放手的都能放手。真正值得你拿來做決定的，是背後的模型、你已經在用的生態系、跟少數強調點——而不是比較文最愛渲染的「監督 vs 全自動」。

看懂這個，你就不會被那些製造對立的文章帶著跑，而是回到最務實的問題：「我手上有哪家、我這個任務想要什麼手感？」——然後動手。

這也是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 工具篇想帶你看的：同一套四層觀念，落在不同 agent 上。接下來我會再寫兩隻**真的很不一樣**的開源 agent——[**OpenClaw（always-on、住在通訊軟體裡）跟 Hermes（會自我改進、自己長技能）**](/posts/self-hosted-ai-agent/)——那才是設計理念差很多的對照組。

如果你想導入這些工具、但不確定怎麼搭你的工作流，或想直接養一隻幫你幹活的 agent——這正是我在做的事。我有提供 [**AI Agent 的諮詢顧問與代建服務**](/ai-automation-workflow/)，幫你看怎麼選、怎麼搭，或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第七篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**Agent Instruction：怎麼寫 AI Agent 的「憲法」**](/posts/agent-instruction-claude-md/) — 兩隻吃的 `CLAUDE.md` / `AGENTS.md` 怎麼寫
* [**MCP / Tools / Skills：AI Agent 的三種能力擴充**](/posts/mcp-tools-skills/) — 兩隻都支援的能力擴充
* [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/) — 不想碰 CLI？從 GUI 版入門

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

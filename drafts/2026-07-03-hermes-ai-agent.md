---
title: "Hermes Agent 是什麼：會自己長記憶、長技能的 AI Agent — 自架 AI Agent 實戰（九）"
date: 2026-07-03
author: HoMuChen
category: AI
tags: [AI Agent, Hermes, 開源, 記憶, Skill, 自架]
image: https://storage.googleapis.com/homuchen.com/images/hermes-ai-agent-0.jpg
description: "Hermes Agent 是什麼？Nous Research 2026 年開源的自主 AI Agent，招牌是 persistent memory 跨 session 記憶＋做完任務自動把流程寫成 skill——越用越強。這篇用『自架 AI Agent 四層觀念』解讀它的設計，並跟 OpenClaw 對照：一隻住進你的通訊軟體，一隻專心變聰明。自架 AI Agent 實戰 #9。"
---

不知道你有沒有這種經驗：花了一個晚上，帶著 AI 一步一步把一件麻煩事搞定——查資料、試錯、修正、終於跑通。結果隔天再開一個新對話，問它同一件事……

它像完全沒發生過一樣，從零開始重新踩一遍昨天的坑。😫

這就是我在 [**系列第三篇**](/posts/ai-agent-memory-file-system/) 說過的：**context window 不是記憶**，session 一關，agent 就失憶。我們在那篇聊了怎麼用檔案系統幫 agent 補記憶；在 [**第四篇**](/posts/mcp-tools-skills/) 聊了怎麼把「做事的方法」寫成 skill。但這兩件事有個共同點——**都是你手動幫它做的**。

那有沒有一隻 agent，是**自己會做這兩件事**的？做完任務自己把心得寫進記憶、自己把流程整理成 skill，下次直接套用——**越用越強**？

有，它叫 **Hermes**。這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第九篇，也是工具篇的最後一隻：上一篇的 [**OpenClaw**](/posts/openclaw-ai-agent/) 把「溝通＋自動化」推到極致，這篇的 Hermes 則把「**記憶＋能力**」推到極致。兩隻擺在一起，剛好補滿四層觀念光譜的兩端。

這篇會聊這些：

* Hermes Agent 到底是什麼（一句話講清楚）
* 招牌設計一：persistent memory——它怎麼記住你
* 招牌設計二：自動長 skill——它怎麼越用越強
* 五階段學習迴圈：「自我改進」到底是怎麼運作的
* 用四層觀念解剖 Hermes ＋ 跟 OpenClaw 的設計哲學對照
* 適合誰、不適合誰，以及怎麼開始

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。我自己電腦上長期養著幾隻自架 agent（[**股票盯盤**](/posts/claude-code-stock-agent-monitor-alert/) 那隻就是），記憶跟 skill 都是我自己一個檔案一個檔案手動設計的——所以看到 Hermes 把這兩件事「自動化」的做法時特別有感，這篇是用我自己組 agent 的經驗去解讀它的設計。

> 利益揭露：本文沒有業配、沒有聯盟連結。Hermes 是 MIT 開源專案，我跟 Nous Research 沒有任何利益關係，純粹覺得它的設計值得拿來當教材。

## Hermes Agent 是什麼

先一句話講清楚：

> **Hermes 是 Nous Research 在 2026 年 2 月開源的自主 AI Agent——它跑在你自己的機器上，會把學到的東西存成跨 session 的長期記憶，還會在做完任務後自動把流程整理成可重用的 skill。用官方的說法：它跑得越久，能力越強。**

幾個關鍵特徵（截至 2026 年中，[官方 repo](https://github.com/NousResearch/hermes-agent) 為準）：

- **開源、MIT 授權**：由做開源模型起家的 [Nous Research](https://nousresearch.com/) 打造，主體用 Python 寫成。
- **Persistent memory（持久記憶）**：記憶存成你機器上的 Markdown 檔（如 `memory.md`、`user.md`），過去的對話還能全文搜尋——它記得你是誰、你們做過什麼。
- **自動長 skill**：完成複雜任務後，它會自己判斷「這個流程值不值得留下來」，值得就寫成 skill 檔，下次直接重用，而且 skill 會在使用中繼續被改進。
- **Local-first、資料不出門**：跑在你自己的機器上，無 telemetry、無追蹤；從一台 5 美金的 VPS 到自家舊電腦都能跑。
- **模型自由**：可接 OpenAI、Anthropic、OpenRouter、自訂 endpoint，透過 Nous Portal 更號稱支援 300+ 種模型——不被任何一家綁死。
- **門檻很低**：Linux / macOS / WSL2 一行 `curl` 指令裝完；2026 年 6 月初還推出了 desktop app（公開預覽版），連終端機都可以少碰一點。

如果說 OpenClaw 像「住在你通訊軟體裡、隨時待命的助理」，那 Hermes 更像「**一個會寫工作日誌、會整理 SOP、還會自己精進手藝的員工**」。

## 招牌設計一：Persistent Memory——它怎麼記住你

還記得我在 [**#3 記憶篇**](/posts/ai-agent-memory-file-system/) 的主張嗎？最樸素也最強的記憶方案，就是「**把知識寫成檔案**」。Hermes 完全是同一個信仰，但它把「寫檔案」這個動作**自動化**了。它的記憶有三塊：

1. **Markdown 記憶檔**：`memory.md` 記事實與偏好、`user.md` 記「你是誰」。重點是——當你糾正它或偏好改變時，**它會自己動手改檔案**，不是嘴巴上說「好的我記住了」然後下個 session 忘光。下次開機，更新後的記憶直接就在。
2. **對話全文搜尋**：過去的 session 存在本地 SQLite 資料庫裡，配上全文檢索（FTS5）——它可以**搜尋自己的過去**，「我們上個月是怎麼處理這個的？」這種問題答得出來。
3. **定期自我檢視（nudge）**：官方設計是**每 10 個對話回合，它會自己回頭看一次最近的對話**，問自己：「有沒有什麼該存進長期記憶？有沒有什麼流程該變成 skill？」——不等你提醒。

發現了嗎？這三塊我們在 #3 都講過概念版：檔案當記憶、索引與檢索、定期整理。Hermes 做的事就是把「**你手動維護記憶**」變成「**agent 自己維護自己的記憶**」。就像我那個 [**丟給 LLM 自己維護的個人 wiki**](/posts/llm-maintained-personal-wiki/)——只是 Hermes 把這件事做成了產品內建。

## 招牌設計二：自動長 Skill——它怎麼越用越強

這是 Hermes 最有記憶點的設計，也是我覺得最值得你搬回自己 agent 上的觀念。

在 [**#4 能力篇**](/posts/mcp-tools-skills/) 我說過：**skill 就是教 agent「怎麼做事」的工作流文件**——食譜。但食譜是誰寫的？在我們自己組的 agent 裡，是你：你做完一件事，覺得流程值得留，就手動整理成 skill 檔。

Hermes 把這步也自動化了。它完成任務後會自己評估「這值不值得寫成 skill」，官方設計的觸發訊號很具體，像是：

- 這個任務用了 **5 次以上的 tool call**（夠複雜，值得留 SOP）
- 過程中**從錯誤中恢復過**（踩過的坑，最值錢）
- **你糾正過它**（下次不要再犯）
- 一個**不明顯、但成功了的流程**（自己摸出來的路）

符合條件，它就把流程寫成一個 `SKILL.md` 檔案存起來（跟 [agentskills.io](https://agentskills.io/) 的開放標準相容）——**不是一筆 log，而是一份下次可以直接照著做的指令集**，之後還能當成 slash command 直接呼叫。更妙的是，skill 不是寫完就定案：之後每次用到，它還會**在使用中繼續修訂**這份 skill。

> 用一句話總結這個設計：**你踩過的坑、修過的錯、摸出來的流程，都會變成它的資產，而不是隨著 session 關閉蒸發。**

這也回答了很多人用 AI 的深層挫折——不是 AI 不夠聰明，是它**不累積**。Hermes 的賭注就是：與其等更聰明的模型，不如先讓 agent 學會累積。

## 五階段學習迴圈：「自我改進」是怎麼運作的

把上面兩個招牌設計串起來，就是 Hermes 官方說的**學習迴圈（learning loop）**，一共五階段：

1. **執行任務**（execute）
2. **評估結果**（evaluate）——成了還是砸了？
3. **萃取模式**（extract）——把可重用的推理流程抽出來，寫成有名字的 skill
4. **持續精煉**（refine）——skill 在後續使用中被繼續修改進化
5. **檢索套用**（retrieve）——新任務來了，先找找過去長出來的 skill 能不能直接用

注意一件事：這裡「自我改進」改的**不是模型本身**（模型參數沒有變），改的是 **agent 層**——記憶檔、skill 檔、工作流程。這其實是很務實的設計：模型會一直換（反正它支援 300+ 種），但**你們共事累積下來的記憶與 SOP 是你的，換模型也帶得走**。這跟我在 [**AI 是勞動力，不是工具**](/posts/ai-labor-not-tool-500-commits/) 講的觀念完全呼應——你在經營的不是一個工具，是一個會成長的勞動力。

## 用四層觀念解剖 Hermes

照慣例，用系列的[**四層觀念**](/posts/self-hosted-ai-agent/)把它收攏成一張表：

| 四層觀念 | Hermes 的實作 | 對應系列篇 |
|---------|--------------|-----------|
| **Context（記憶）** | 🌟 招牌：Markdown 記憶檔＋SQLite 全文搜尋＋每 10 回合自我檢視 | [#3 memory](/posts/ai-agent-memory-file-system/) |
| **能力（skill）** | 🌟 招牌：做完任務自動長 skill、使用中持續精煉 | [#4 MCP/Tools/Skills](/posts/mcp-tools-skills/) |
| **溝通（channel）** | Telegram、Discord、Slack、WhatsApp、Signal、Email、CLI 統一接入 | [#5 channels](/posts/ai-agent-channels-telegram-line/) |
| **自動化** | 內建排程器，用自然語言就能設定定時任務（每日報告、夜間備份…） | [#6 crontab](/posts/crontab-ai-agent-schedule/) |

四層都有，但重心一目瞭然：**OpenClaw 的星星畫在下面兩層（溝通＋自動化），Hermes 的星星畫在上面兩層（記憶＋能力）。**

### 跟 OpenClaw 的設計哲學對照

兩隻都是 2026 年爆紅的開源自主 agent、都 local-first、都接一堆通訊軟體、都能自己動——但骨子裡的追求完全不同：

| | [OpenClaw](/posts/openclaw-ai-agent/) 🦞 | Hermes |
|---|---|---|
| **核心追求** | 隨時找得到它（always-on 助理） | 越用越強（self-improving worker） |
| **招牌機制** | gateway 接 14+ 通訊軟體、heartbeat 自己醒來 | persistent memory、自動長 skill |
| **像什麼** | 住在你手機裡、隨傳隨到的貼身助理 | 會寫日誌、整理 SOP、自己精進的資深員工 |
| **時間帶來什麼** | 更多完成的任務 | 更多完成的任務**＋更強的它** |

沒有誰比較好，是**你要哪一種員工**的問題。甚至——很多人是兩隻都養，各司其職。

## 適合誰、不適合誰

老實說，給你一個誠實的判斷：

**適合你，如果——**

- 你的需求是**重複性高、有累積價值**的工作流（定期報告、資料處理、維運雜務）——skill 累積的複利在這裡最明顯。
- 你受夠了「每次都要重新教 AI 一遍」，想要一隻**記得你**的 agent。
- 你在意資料隱私，想要 local-first、模型還能自由換。
- 你不怕終端機（它是 CLI-first，雖然 2026/6 出了 desktop app，但骨子裡還是給 builder 用的）。

**可能還不適合你，如果——**

- 你要的是「隨時在手機上敲它」的貼身助理體驗——那 [**OpenClaw**](/posts/openclaw-ai-agent/) 的多 channel 更對口。
- 你主要是寫程式——[**Claude Code / Codex**](/posts/claude-code-vs-codex/) 在 coding 場景還是更成熟。
- 你完全不想碰任何設定——先從 GUI 的 [**Claude Cowork**](/posts/claude-cowork-ai-from-chat-to-work/) 入門吧，觀念都相通。

## 你可以怎麼開始

跟上一篇一樣，我不寫安裝流水帳（官方一行指令真的沒什麼好教的😂），給你務實的上手順序：

1. **看官方** [**repo**](https://github.com/NousResearch/hermes-agent) 確認環境：Linux / macOS / WSL2 一行 `curl` 裝完，Windows 也有原生支援；怕終端機的可以直接抓 desktop app（公開預覽版）。
2. **先接一個模型**：有 OpenAI / Anthropic 的 API key 就能跑，想省錢或資料完全不出門可以走本地模型路線。
3. **頭幾天故意跟它多聊**：糾正它、教它你的偏好——然後去看 `memory.md` 和 `user.md` 怎麼被它自己改掉，你會對「agent 自己維護記憶」很有感。
4. **做一件複雜的事，然後看它長 skill**：找一個你每週都要做的多步驟任務帶它跑一次，看它把流程寫成 `SKILL.md`——下次同樣的事，一句話就完成。

關鍵心法還是那句：**帶著四層觀念去玩它**。你觀察它改記憶檔，就是在看 Context 層；看它長 skill，就是在看能力層。看懂了，這些設計你都能搬回自己手工組的 agent 上。

## 常見問題

### Hermes Agent 是什麼？

**Hermes 是 Nous Research 在 2026 年 2 月開源（MIT）的自主 AI Agent，跑在你自己的機器上，招牌是「會自我改進」**：它把學到的東西存成跨 session 的持久記憶（persistent memory），並在完成任務後自動把流程整理成可重用的 skill——跑得越久、越懂你、能力越強。

### Hermes 跟 OpenClaw 差在哪？

**設計哲學不同。** [**OpenClaw**](/posts/openclaw-ai-agent/) 把「溝通＋自動化」推到極致——接 14+ 種通訊軟體、heartbeat 自己醒來，是一隻 always-on 的貼身助理；Hermes 把「記憶＋能力」推到極致——自動維護記憶、自動長 skill，是一隻越用越強的 worker。要「隨時找得到」選前者，要「越養越聰明」選後者，也有人兩隻都養。

### Hermes 可以接 LINE 嗎？

**官方內建的 channel 目前沒有 LINE**（截至 2026 年中，內建支援 Telegram、Discord、Slack、WhatsApp、Signal、Email 與 CLI）。台灣使用者想用 LINE 收通知或遙控 agent，得自己透過 LINE Messaging API 加 webhook 橋接——做法的觀念我在 [**系列第五篇 channels**](/posts/ai-agent-channels-telegram-line/) 有講。最省事的替代方案是先用 Telegram，內建支援、五分鐘就能接起來。

### Hermes 的「自我改進」會改模型本身嗎？

**不會，它改進的是 agent 層，不是模型參數。** 變強的是它的記憶檔、skill 庫與工作流程——選對 skill、記得你的偏好、不再犯你糾正過的錯。好處是這些累積**不綁定任何模型**：它支援 OpenAI、Anthropic、OpenRouter 等 300+ 種模型，之後換更強的模型，累積下來的記憶與 skill 都帶得走。

### Hermes 免費嗎？要什麼硬體才能跑？

**程式本身 MIT 開源、完全免費**，費用來自你接的模型 API（依用量計費；接本地模型可近乎零成本）。硬體門檻很低——官方說法是從 5 美金/月的 VPS 到你家舊電腦都能跑，Linux / macOS / WSL2 一行指令安裝。不確定要準備什麼機器的話，我之後會寫一篇專門聊自架 agent 的硬體選擇。

## 結語

寫到這篇，這個系列的觀念篇＋工具篇就補完了。回頭看很有意思——

> **四層觀念（Context → 能力 → 溝通 → 自動化）是地圖；Claude Code / Codex、OpenClaw、Hermes 是三種在地圖上插旗位置完全不同的答案。** 看懂地圖，你就不會被「又一隻爆紅 agent」的新聞牽著跑，因為你一眼就能看出：喔，它是把哪一層推到極致的那種。

而 Hermes 留給我們最值錢的一課，我覺得不是「快去裝它」，而是它示範了一個方向：**agent 的價值不只在模型多聰明，更在它會不會累積。** 就算你不用 Hermes，「做完事把心得寫進記憶、把流程寫成 skill」這個習慣，你今天就可以幫你自己手工組的 agent 加上——手動版的學習迴圈，一樣香。

如果你看完想養一隻會累積的 agent，但卡在「不知道從我的工作流哪裡下手」——這正是我在做的事。我有提供 [**AI Agent 的諮詢顧問與代建服務**](/ai-automation-workflow/)，幫你看怎麼設計、或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第九篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**OpenClaw 是什麼：用四層觀念看懂這隻爆紅 AI Agent 的設計**](/posts/openclaw-ai-agent/) — 系列 #8，跟 Hermes 對照的另一端
* [**AI Agent 的記憶與檔案系統：memory、檔案記錄、漸進式揭露**](/posts/ai-agent-memory-file-system/) — 系列 #3，Hermes 記憶設計的觀念版
* [**MCP / Tools / Skills：AI Agent 的三種能力擴充**](/posts/mcp-tools-skills/) — 系列 #4，skill 到底是什麼
* [**AI 是勞動力，不是工具**](/posts/ai-labor-not-tool-500-commits/) — 為什麼「會累積」這件事這麼重要

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

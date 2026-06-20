---
title: "MCP / Tools / Skills：AI Agent 的三種能力擴充 — 自架 AI Agent 實戰（四）"
date: 2026-06-20
author: HoMuChen
category: AI
tags: [AI Agent, MCP, Agent Skills, Claude Code, Tools]
image: https://storage.googleapis.com/homuchen.com/images/mcp-tools-skills-0.jpg
description: "MCP、Tools、Skills 到底差在哪？這篇把關係講準：Tool 是動作的最小單位，要把它交到 agent 手上有兩條路——接 MCP（標準插座）或自己寫 script（DIY），而 Skill 是教 agent 怎麼把動作串起來做對、還能復用。用我真實在跑、其實沒用到 MCP 的股票 agent 當例子，帶你判斷何時該寫 MCP、何時 script + skill 就夠。自架 AI Agent 實戰 #4。"
---

我第一次幫股票 agent 接上抓股價的能力時，超有成就感——它終於能去 FinMind 拿即時行情了！

結果一上場我就傻眼：它確實抓得到資料，卻**完全不知道該怎麼用**。我問它「台積電現在的狀況」，它就把一坨原始數字丟回來，不會算指標、不會判斷強弱、更不會挑出我在意的訊號。就像你請了一個廚師，給了他全套廚具跟滿冰箱的食材，結果他站在廚房中間發呆，因為——**沒有人給他食譜，他不知道要煮什麼、怎麼煮。**

這就帶出今天的主題：一隻 agent 要能「幹活」，背後其實是 **Tools、MCP、Skills** 在分工。但很多文章把這三個講成「三個平行的功能」，結果越看越糊。這篇我想把**它們真正的關係**講清楚——你會發現它們根本不在同一個層次上。

在 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 裡，我把一隻自主 agent 拆成四層：**Context（它知道什麼）→ 能力（它能做什麼）→ 溝通（它怎麼跟你來往）→ 自動化（它什麼時候自己動）**。前面 [**instruction**](/posts/agent-instruction-claude-md/) 跟 [**memory**](/posts/ai-agent-memory-file-system/) 講完了 Context 這層（它的腦袋），這篇要進到第二層——**能力，也就是讓它能「動手做事」的那一層。**

這篇會聊這些：

* 為什麼光有聰明的腦袋還不夠，agent 得能「動手」
* Tool 是什麼：能力的最小單位（一個概念，不是一種產品）
* 把 tool 交到 agent 手上的兩條路：接 **MCP** vs 自己寫 **script**
* Skill 是什麼：教 agent 怎麼把動作串起來做對、而且能復用
* 取捨判斷：什麼時候該寫 MCP、什麼時候 script + skill 就夠

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。文中的做法都是我自己電腦上 agent 真的在跑的，本文是第一手實作紀錄——包括「我其實沒用 MCP」這件事，後面會老實講。

> 利益揭露：本文沒有業配、沒有聯盟連結。提到的工具都是我自己用過或研究過的。

## 為什麼光有腦袋還不夠

前面三篇，我們把 agent 的「腦袋」養好了：給它規則（instruction）、給它記憶（memory）。但你有沒有發現，到目前為止這隻 agent 還只能「想」，不能「做」？

它沒辦法真的去抓一筆股價、寫一個檔案、寄一封信。**一個只會思考、不能動手的 agent，本質上還是個聊天機器人。** 要讓它變成會幹活的員工，就得給它「手腳」——這就是「能力」這一層在做的事。

而這層手腳，常被講成 Tools、MCP、Skills 三樣東西。但與其說它們是「三個並列的功能」，不如先把它們擺回**正確的位置**——因為它們其實是三個不同層次的概念。

## Tool 是什麼：能力的最小單位

先從最底層的講起。**Tool 是能力的最小單位，就是「一個明確的動作」。** 抓一次股價、讀一個檔案、跑一段計算、發一則訊息——每一個都是一個 tool。

它的特色是**單純、原子化**：給它輸入、它給你輸出，做完一件事就結束。用大廚比喻，tool 就是廚師手上的單一技能——「切」就是切、「煎」就是煎。

這裡有個很多人會搞混、但其實很關鍵的點：

> **Tool 是一個「概念」，不是一種特定產品。** 它指的是「agent 能呼叫的一個動作」，至於這個動作**怎麼被提供給 agent**，有不只一種做法。

而 agent 厲害的地方，就是它會**自己決定什麼時候用哪個 tool、怎麼把好幾個 tool 串起來**完成大任務。但前提是：這些 tool 得先存在、它得拿得到。**那要怎麼把一個 tool 交到 agent 手上？這就是 MCP 跟 script 上場的地方——它們是兩條不同的路。**

## 把 tool 交到 agent 手上：兩條路

要讓 agent 多一個動作（一個 tool），最常見的有兩條路。搞懂這兩條路的差別，你就懂 MCP 到底是什麼了。

### 路線一：接 MCP（標準插座）

**MCP（Model Context Protocol）是一套標準協定，讓外部服務能用統一格式，把自己的 tools 和資料「暴露」給任何支援 MCP 的 agent。** 它由 Anthropic 在 2024 年底提出，現在已經是跨工具的[開放標準](https://modelcontextprotocol.io/)。

關鍵在「**標準**」兩個字。在 MCP 出現之前，你想讓 AI 接上某個服務，每一個都得自己刻一套對接。MCP 的價值是：**它定義了一套大家都遵守的「插座規格」，任何服務只要照規格做成 MCP server，你的 agent 插上就能用、還能跟別人分享。**

> 所以更精準地說：**MCP 不是「一種 tool」，而是「把 tool 標準化地遞送給 agent 的一條管道」。** 它像 USB——USB 本身不是裝置，是讓裝置即插即用的統一接頭。

MCP 適合的場景：**你要接的服務已經有現成的 MCP server**（很多熱門服務都有了），或者你想做一個**能跨工具、能分享給別人**的標準連接。這時候 MCP 很香。

### 路線二：自己寫 script（DIY）

但這裡要老實講一件事：**我自己那隻股票 agent，其實沒有用 MCP。**

我的做法是這樣：我叫 [**Claude Code**](/posts/claude-code-stock-agent-monitor-alert/) 去讀 [**FinMind**](/posts/claude-code-finmind-stock-tracking/) 的 API 文件，然後**寫一支 Python script 直接打那個 API**、把資料拿回來。agent 要用的時候，就透過一個通用的「執行腳本」能力去跑這支 script。**從頭到尾沒碰 MCP。**

這就是第二條路——**自己寫 script**。它沒有 MCP 那種跨工具標準，但換來的是：**直接、快、完全你說了算。** 想接什麼就接什麼，不用等別人做好 server、也不用學一套協定。

> 這兩條路殊途同歸，都是「給 agent 一個能拿到外部資料的 tool」。差別只在：**MCP 是用標準插座，script 是自己接管線。**

而且老實說，對自架的個人 agent 來說，**第二條路常常更實際**。很多時候你需要的東西沒有現成 MCP server，與其自己從頭寫一個符合協定的 server，不如叫 AI 直接幫你寫一支 script 打 API，快得多。

## Skill 是什麼：教 agent 怎麼把事做對

好，現在 agent 有手（tool）、也拿得到食材了（不管走 MCP 還是 script）。但就像我開頭那位發呆的廚師——**它還是不知道「該怎麼把這些組合起來做出一道菜」。** 這就是 Skills 要解決的，而且它跟前面兩條路**完全不在同一個層次**。

**Skill 是一份用自然語言寫的「工作流文件」，教 agent 在特定任務上該怎麼做——先做什麼、再做什麼、用什麼標準判斷。** 它本質上就是一份 SOP 手冊，通常是一個 Markdown 檔，而且可以把要用到的 script 一起包進去。

回到我的例子：我把「抓哪幾項 FinMind 資料、用那支 script 怎麼跑、算什麼指標、漲跌幅和量能到什麼門檻才算訊號、算完用什麼格式整理」整套寫成一個**股票分析 skill**。於是這套流程就**復用**了——以後 agent 每次要分析股票，打開這個 skill 就照著做，我不用每次重講。**我那位發呆的廚師，缺的就是這份食譜。**

Skill 有兩個很迷人的特點：

1. **不用寫程式。** 它就是一份用人話寫的文件（裡面可以引用你寫好的 script，但 skill 本身是說明）。你會打字、能把流程講清楚，就能寫 skill。
2. **它天生用了[漸進式揭露](/posts/ai-agent-memory-file-system/)。** 還記得上一篇講的嗎？一份 skill 平常只露出一句簡短描述，agent 判斷「這次需要它」才把細節展開來讀。所以你可以掛幾十個 skill，也不會一次塞爆 context。**Skills 可以說就是漸進式揭露的最佳實踐。**

> 如果你對「Skill 到底是什麼」想要更入門的講解，我在 Claude Cowork 系列寫過一篇 [**Skill 是什麼？讓 AI Agent 從通才變專家**](/posts/what-is-ai-agent-skill/)，用不碰 CLI 的角度從頭講，適合搭配著看。

## 把它們擺回正確的位置

現在你應該看出來了——Tools、MCP、Skills **根本不是三個平行的東西**，它們在不同層次：

| 角色 | 它是什麼 | 大廚比喻 | 要寫程式嗎 |
|---|---|---|---|
| **Tool** | 能力的最小單位（一個動作，是個概念） | 切菜、開火 | —（它是被「提供」的） |
| **MCP** | 把 tool 標準化遞送的協定（路線一） | 標準規格的宅配系統 | 用現成的不用；自製要 |
| **自己寫 script** | DIY 給 agent 一個動作（路線二） | 自己上市場採買 | 要（但可叫 AI 幫你寫） |
| **Skill** | 教 agent 怎麼把動作串起來做對、可復用 | 食譜與手藝 | 不用 |

用我的股票 agent 走一遍完整流程，你就秒懂它們怎麼合作：

1. **盤中時間到**，agent 醒來要分析台積電。
2. 它打開「股票分析 **skill**」——這份 SOP 告訴它整套流程怎麼走。
3. skill 說「先去拿即時行情」，於是 agent 去跑我寫好的那支 FinMind **script**（這就是它的 tool，走的是路線二，沒有 MCP）。
4. 拿回原始資料後，再照 skill 裡的公式算指標、比門檻，判斷出「爆量突破」這個訊號。
5. 最後跑「發 Telegram」這個動作，把結果傳到我手機。

看到了嗎？**skill 是劇本（怎麼做）、tool 是一個個具體動作（做什麼）、而 tool 從哪來（MCP 還是 script）是底下的實作選擇。** 三層合起來，agent 才從「會想」變成「會做」。

## 取捨判斷：什麼時候用哪個

這是這篇我最想給你的東西，因為多數文章只解釋「是什麼」，不告訴你「何時用」。

**第一個決定：要不要寫 skill？** 幾乎永遠是要。只要這個任務有一套「固定該怎麼做」的流程，就把它寫成 skill。這是最該優先投資的，因為它不用寫程式、又最能提升 agent 把事做對的成功率。**八成的人卡住的不是「接不接得到資料」，而是「agent 不知道怎麼用資料」——那就是缺 skill。**

**第二個決定：tool 走 MCP 還是自己寫 script？**

- **服務已經有現成的 MCP server，或你想做能分享、跨工具的標準連接** → 走 MCP，插上就用，省事又乾淨。
- **沒有現成 MCP、你想快速搞定、或只是自己用** → 直接叫 AI 幫你寫支 script 打 API，像我的股票 agent 那樣。對個人自架來說，這條路常常更快。
- **真的沒有現成、又是長期重度使用、還想標準化** → 才值得花工自己寫一個 MCP server。

> 一個簡單的心法：**先問「它知道怎麼做嗎」（skill），再問「它接得到嗎」（tool）；而接得到這件事，先找現成 MCP，沒有就寫 script。** 別一開始就糾結「我是不是該寫個 MCP」——那通常是最後才需要操心的事。

## 常見的兩個誤解

**誤解一：「一定要用 MCP 才專業。」** 完全不是。MCP 是「標準化、可分享」的優點，但不是必需品。我那隻天天在跑的股票 agent 就完全沒用 MCP，靠 script + skill 一樣跑得好好的。**能用 script 快速解決的，就別為了「看起來正規」硬寫 MCP。**

**誤解二：「Skills 是來取代 MCP 的。」** 不是，它們根本不在同一層。MCP（或 script）管「agent 拿不拿得到、做不做得到」，Skill 管「agent 知不知道怎麼把事做對」。你會同時用到，不是二選一。

## 你可以怎麼開始

不用三個一起上，照這個順序最輕鬆：

1. **先從一個 skill 開始。** 挑一件你 agent 常做、又有固定步驟的事，把流程用人話寫成一份 Markdown，就是你的第一個 skill。
2. **需要外部資料時，先看有沒有現成 MCP；沒有就叫 AI 幫你寫支 script。** 別卡在「要不要寫 MCP」，多數情況一支 script 就夠了。
3. **把那支 script 的用法寫進 skill 裡一起復用**，下次 agent 就會自己照著做。

關鍵心法：**大部分人需要的是更好的 skill（教 agent 怎麼做對），而不是更複雜的 MCP（接更多東西）。** 而且這些——skill 也好、script 也好——你都可以直接叫 AI 幫你寫。

## 常見問題

### Tool 跟 MCP 到底差在哪？

**Tool 是「一個動作」這個概念（抓股價、寫檔案），MCP 是「把 tool 標準化地遞送給 agent 的一條管道」。** 兩者不在同一層：tool 是被提供的東西，MCP 是提供它的方式之一。而且 MCP 不是唯一方式——你也可以自己寫一支 script，讓 agent 透過「執行腳本」這個動作去用它，完全不碰 MCP。

### MCP 跟自己寫 script，我該選哪個？

**有現成 MCP server、或想做能分享/跨工具的標準連接 → 走 MCP；沒有現成、想快速搞定、或只是自己用 → 寫 script。** 對個人自架 agent 來說，script 這條路常常更快——像我的股票 agent 就是叫 AI 讀 FinMind 文件、寫 script 直接打 API，沒用 MCP。只有「沒現成、長期重度用、又想標準化」時，才值得自己寫一個 MCP server。

### MCP 跟 Skill 差在哪？要用哪個？

**它們不在同一層，不是二選一。** MCP（或 script）解決「agent 接不接得到外部」，Skill 解決「agent 知不知道怎麼把事做對」。你通常兩個都要：用 MCP/script 讓它拿得到資料，用 skill 教它怎麼分析。多數人卡住的其實是後者。

### 寫 Skill 需要會程式嗎？

不用。**Skill 就是一份用自然語言寫的工作流文件（通常是 Markdown）**，你會打字、能把「先做什麼、再做什麼、用什麼標準判斷」講清楚就能寫。裡面可以引用你寫好的 script，但 skill 本身是說明文件。甚至可以直接叫 AI 幫你把流程整理成 skill。

### 為什麼掛很多 skill 不會把 context 塞爆？

因為 skill 用了**漸進式揭露**：平常每個 skill 只露出一句簡短描述，agent 判斷「這次需要它」時，才把該 skill 的細節展開來讀。所以你可以掛幾十個 skill，每次實際載入 context 的量還是很小。這跟 [**上一篇講記憶**](/posts/ai-agent-memory-file-system/) 用索引檔的道理一模一樣。

## 結語

繞了一圈，agent 的「能力」這層，重點不是背三個名詞，而是看懂它們的層次：**Tool 是動作的最小單位；要把 tool 交到 agent 手上，有 MCP（標準插座）和自己寫 script（DIY）兩條路；而 Skill 是教它怎麼把這些動作串起來做對、還能復用的那層知識。** 我開頭那位對著食材發呆的廚師，缺的不是手、也不是食材，而是一份食譜——也就是 skill。

搞懂這個，你就不會再傻傻地什麼都想寫成 MCP（像我自己，根本沒用 MCP 也跑得好好的），而是先問對問題：「它知道怎麼做嗎？它接得到嗎？」

到這裡，[**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 前兩層就完整了：Context（[instruction](/posts/agent-instruction-claude-md/) + [memory](/posts/ai-agent-memory-file-system/)）給它腦袋，能力（Tool / MCP / script / Skill）給它手腳。一隻有腦、有手、會判斷的 agent，骨架就成形了。接下來系列會進到工具篇，看 [**Claude Code、Codex、OpenClaw、Hermes**](/posts/self-hosted-ai-agent/) 這些實際的 agent，是怎麼把這些觀念做到極致的。

如果你想幫自己的 agent 設計這層能力，但卡在「該寫 MCP 還是 script、流程怎麼拆成 skill」——這正是我在做的事。我有提供 [**AI Agent 的諮詢顧問與代建服務**](/ai-automation-workflow/)，幫你看能力這層怎麼設計，或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第四篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**AI Agent 的記憶與檔案系統：memory、檔案記錄、漸進式揭露**](/posts/ai-agent-memory-file-system/) — 系列 #3，skill 的漸進式揭露就是這套
* [**Skill 是什麼？讓 AI Agent 從通才變專家**](/posts/what-is-ai-agent-skill/) — 不碰 CLI 的 skill 入門講解
* [**用 Claude Code 打造台股 AI Agent：盤中盯盤、訊號到就發 Telegram**](/posts/claude-code-stock-agent-monitor-alert/) — 本篇 script + skill 範例的完整案例

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

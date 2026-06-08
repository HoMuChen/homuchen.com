---
title: "用 Crontab 讓 AI Agent 自己定時開工 — 自架 AI Agent 實戰（六）"
date: 2026-06-08
author: HoMuChen
category: AI
tags: [AI Agent, Claude Code, crontab, 自動化, 排程]
image: https://storage.googleapis.com/homuchen.com/images/crontab-ai-agent-schedule-0.jpg
description: "AI Agent 不該你不開它就不動。這篇教你用 crontab 在自己電腦排程 AI Agent，從『定時跑指令』躍遷到『定時觸發 agent 完成任務』，用我天天在跑的股票盯盤、Threads 爬蟲當例子，並誠實對照 Claude 雲端 Routines 的 1 小時/3 天限制。自架 AI Agent 實戰 #6。"
---

早上八點，我還在睡。

但我的電腦已經醒了——它把今天台股值得盯的股票掃了一輪、選好、算好每檔的觸發條件，靜靜躺在一個檔案裡等開盤。我沒有設鬧鐘叫自己做這件事，也沒有手動打開任何程式。

是 **crontab** 叫我的 agent 起床上工的。

在 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 裡，我把一隻自主 agent 拆成四層：Context（它知道什麼）→ 能力（它能做什麼）→ 溝通（它怎麼跟你來往）→ **自動化（它什麼時候自己動）**。前一篇講完了[**溝通（channel）**](/posts/ai-agent-channels-telegram-line/)，這篇要講最後一層、也是讓 agent 真正「活起來」的那一層——**自動化**。

這篇會聊這些：

* 為什麼 agent 接了通知還不夠，得有東西「觸發」它
* crontab 30 秒入門（看懂那五個數字就會了）
* 關鍵躍遷：從「定時跑指令」到「定時觸發一隻 agent」
* 我自己天天在跑的兩個排程：股票盯盤、Threads 爬蟲 + 早報
* macOS 上的雷：cron 為什麼常常「沒反應」
* 自己的 crontab vs Claude 雲端 Routines，到底差在哪、怎麼選
* 進階：OpenClaw / Hermes 的 heartbeat 是 cron 的聰明版

> 關於作者：我是工程師阿穆，寫程式十多年，這幾年在做 AI Agent 與電商系統開發。文中這些排程都是我自己電腦上天天在跑的，本文是第一手實作紀錄。

> 利益揭露：本文沒有業配、沒有聯盟連結。提到的工具都是我自己用過或研究過的；Claude Cloud Routines 我自己沒在用，相關規格依官方說明、我會清楚標示。

## 為什麼「接了通知」還不夠

上一篇我們讓 agent 學會了在 Telegram 上跟你說話。但你有沒有發現一個缺口：**訊息要被「誰」觸發？**

一個只會回應你訊息的 agent，本質上還是被動的——你不戳它，它就不動。可是我們要的「員工」不是這樣：好的員工會自己看時間、自己知道什麼時候該做什麼，不用你每件事都交代。

> agent 的 channel 是它的**嘴巴**，而 crontab 是它的**生理時鐘**。兩個加起來，它才會「時間到了自己起床、做完事再回報你」。

所以這一層在解決的問題很單純：**怎麼讓 agent 不用你催，自己照表操課。** 而在自己電腦上，最老牌、最可靠、免費又不用連網的答案，就是 Unix 內建的 **crontab**。

## crontab 30 秒入門

**crontab 是 Unix/Linux/macOS 內建的排程工具，你給它一個時間表，它就會在指定時間自動幫你執行指令。** 不用裝任何東西，打開終端機就有。

兩個指令先記住：

- `crontab -e`：編輯你的排程表
- `crontab -l`：列出目前排了哪些

每一行排程就是一個任務，格式是**五個時間欄位 + 要執行的指令**：

```
┌── 分鐘 (0-59)
│ ┌── 小時 (0-23)
│ │ ┌── 日 (1-31)
│ │ │ ┌── 月 (1-12)
│ │ │ │ ┌── 星期幾 (0-7，0 和 7 都是週日)
│ │ │ │ │
* * * * *  要執行的指令
```

看幾個例子就懂了：

```bash
0 8 * * *      每天早上 8:00
*/10 * * * *   每 10 分鐘一次
0 9 * * 1-5    週一到週五的早上 9:00
0 3 1 * *      每個月 1 號的凌晨 3:00
```

`*` 就是「每一個都算」，`*/10` 是「每隔 10」，`1-5` 是「範圍」。**會看這五個數字，crontab 你就學會八成了。** 想看更完整的語法，繁中我推薦 [G.T. Wang 的這篇](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/) 跟 [鳥哥的章節](https://linux.vbird.org/linux_basic/centos7/0430cron.php)，講得很細。

## 關鍵躍遷：從「定時跑指令」到「定時觸發一隻 agent」

到這裡為止，都還是傳統 crontab 教學會教的東西。**但繁中幾乎沒人講的，是下一步那個躍遷。**

過去我們用 crontab 排的，是**死板的腳本**——備份資料庫、清 log、寄一封固定格式的報表。它每天做一模一樣的事，不會判斷、不會變通。

現在不一樣了。crontab 後面接的那個指令，可以是**一隻會判斷、會用工具、會回報的 AI Agent**：

```bash
# 傳統 cron：跑一個死腳本
0 9 * * *  python3 backup.py

# 現在的 cron：觸發一隻會思考的 agent
0 9 * * *  cd ~/my-agent && claude -p "讀今天的收件匣，把重要的整理成摘要傳到我 Telegram"
```

下面那行的差別在於：它不是執行固定步驟，而是**把一個任務交給 agent，讓 agent 自己決定怎麼完成**。今天信件多就多整理一點、有急件就標出來——這是死腳本做不到的。

> crontab 沒有變，變的是它後面那個東西：從「一條指令」變成「一個會幹活的同事」。

這就是自架 AI Agent 最迷人的地方：**你用最樸素的老工具（cron），搭上最新的 agent，就能讓一隻會思考的東西照表上工。** 下面用我自己在跑的兩個例子讓你有感。

## 我天天在跑的兩個排程

### 例子一：股票 bot 的一張作息表

我的[**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/) 一天會自己醒來四次，靠的就是一張 crontab 作息表：

```bash
# 盤前 08:00 選股，產生今天的觀察清單
0 8 * * 1-5    python3 scan.py --no-update > data/morning_watchlist.txt

# 盤中 09–13 每 10 分鐘盯盤，條件到齊就發 Telegram
*/10 9-13 * * 1-5   python3 monitor.py >> data/monitor.log

# 收盤 18:00 補當天股價
0 18 * * 1-5   python3 stock_cache.py today

# 盤後 22:00 補三大法人、融資融券籌碼
0 22 * * 1-5   python3 broker_cache.py today
```

注意那行 `*/10 9-13 * * 1-5`——**盤中每 10 分鐘、只在週一到週五跑**。這四行排程兜起來，就是「收盤補資料 → 盤前選股 → 盤中盯盤發訊號」這個天天自己轉的循環，我完全不用碰。等等講到雲端方案時，這個「每 10 分鐘」會變成一個關鍵的分水嶺。

### 例子二：Threads 爬蟲 + 每天早上的 AI 早報

第二個是我用來經營 [**Threads**](https://www.threads.net/@homuchen.build.ai) 的。我請 Claude Code 幫我寫了一隻爬蟲，定期把相關的貼文資料爬下來、存進一個本地資料庫，然後每天早上叫 agent 讀這個資料庫、整理成一份趨勢摘要傳給我。拆成兩行 cron：

```bash
# 每天凌晨 3 點，跑 AI 寫好的爬蟲，更新貼文資料庫
0 3 * * *   /usr/bin/python3 ~/threads-db/crawl.py >> ~/threads-db/crawl.log 2>&1

# 每天早上 10 點，叫 agent 讀資料庫、整理成今日摘要傳給我
0 10 * * *  cd ~/threads-db && claude -p "讀昨天爬到的貼文，整理成今天的趨勢早報，傳到我的 Telegram"
```

這個組合很值得玩味：**爬蟲負責「把資料弄進來」（死腳本就夠），agent 負責「把資料變成洞見」（需要會思考）。** 一個是力氣活、一個是判斷活，用 cron 串在一起，我每天早上 10 點就會收到一份不用自己整理的早報。

這也呼應上一篇 channel 的設計——**排程（cron）負責叫它起床，通知（channel）負責把成果送到我面前**。兩層接起來才完整。

## 設計模式：排程 → 自主執行 → 回報

把上面兩個例子抽象出來，自架排程 agent 幾乎都是同一個模式：

> **crontab 時間到 → 喚醒 agent → agent 自主完成任務 → 透過 channel 把結果回報你**

記住這個三段式，你會發現很多「每天/每週固定要做、又很耗時間」的事都能套：

- 每天早上把收件匣整理成摘要
- 每週一自動產上週的數據報表
- 每天定時抓某個網站/某個數字，有異常才通知你
- 每晚把當天的筆記歸檔、更新你的[**個人 wiki**](/posts/llm-maintained-personal-wiki/)

**重點不是「股票」或「Threads」，而是這個「定時喚醒一隻會思考的 agent」的思路。** 你手上那件每天重複、又有點需要動腦的雜事，很可能就是下一個候選。

## macOS 上的雷：為什麼你的 cron「沒反應」

**十個人在 mac 上第一次用 cron 排 agent，有八個會卡在「明明排了卻沒跑」。** 這幾乎都是同幾個坑，先幫你踩過：

**1. cron 是「最小環境」，不會讀你的 shell 設定。** 你在終端機打 `python3`、`claude` 會動，是因為你的 `.zshrc` 設好了 PATH。但 cron 不讀這些檔，所以要嘛用**絕對路徑**（`/usr/bin/python3` 而不是 `python3`），要嘛在 crontab 最上面自己設好：

```bash
PATH=/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin
ANTHROPIC_API_KEY=sk-ant-...
```

**2. API key 之類的環境變數要自己帶進去。** agent 要呼叫 API，但 cron 環境沒有你平常的環境變數，記得在 crontab 裡設、或讓腳本自己讀 `.env`。

**3. macOS 的權限保護。** mac 會擋背景程式存取某些資料夾，必要時要去「系統設定 → 隱私權與安全性 → 完整磁碟取用權」把 `cron`（或你的終端機）加進去。

**4. 一律把輸出導到 log。** 像上面 `>> crawl.log 2>&1` 那樣，不然出錯你完全看不到原因。debug cron 第一步永遠是看 log。

> 如果你覺得 cron 在 mac 上太多坑，也可以改用 macOS 原生的 **launchd**，或在 Python 裡用 **APScheduler** 自己排——殊途同歸，挑你順手的就好。

## 自己的 crontab vs Claude 雲端 Routines

講到排程 agent，2026 年有個你一定會遇到的問題：**Claude Code 現在有官方的雲端排程功能（Cloud Routines / Scheduled Tasks），那我還需要自己搞 crontab 嗎？**

先說它是什麼：Claude Code 的 Routines 可以用**排程、API、或 GitHub 事件**三種方式觸發，跑在 Anthropic 的雲端，**就算你關機、闔上筆電也能執行**。聽起來很香，對吧？

但它有兩個關鍵限制（依官方說明，我自己沒在用所以照規格講）：**最小排程間隔是 1 小時**、而且**任務大約 3 天後會自動過期**（安全機制）。

把兩條路擺一起比：

| 維度 | 自己的 crontab | Claude Cloud Routines |
|------|---------------|----------------------|
| **跑在哪** | 你自己的電腦 | Anthropic 雲端 |
| **電腦要開著嗎** | 要（關機就不跑） | 不用，關機也跑 |
| **最小間隔** | 每分鐘都行 | 最小 1 小時 |
| **會過期嗎** | 不會，永遠在 | 約 3 天後過期 |
| **資料在哪** | 不出你的機器 | 經過雲端 |
| **費用** | 免費（系統內建） | 看方案 |
| **設定難度** | 要懂一點 cron + 環境 | 較簡單 |

關鍵分水嶺就在我前面埋的那個伏筆——**我的股票 bot 盤中要每 10 分鐘跑一次**。Cloud Routines 最小間隔 1 小時，**這件事它做不到**。需要高頻、需要永久長跑、又希望資料不出自己機器的任務，自己的 crontab 還是唯一解。

所以我的判斷是：

- **要高頻（< 1 小時）、長期常駐、資料敏感** → 自己的 crontab（像我的股票盯盤）
- **低頻（幾小時/每天一次）、又懶得讓電腦一直開著** → 雲端 Routines 很方便
- **很多人會兩個混用**：高頻的留本機、低頻又想關機跑的丟雲端

這不是信仰問題，是看你的任務「多頻繁、多敏感、能不能讓電腦開著」。

## 進階：heartbeat 是 cron 的聰明版

最後補一個你之後一定會遇到的進化版概念。

crontab 有個天生的笨——**它是「死的時間觸發」**。時間到就跑，不管現在該不該跑、有沒有意義。每 10 分鐘檢查一次，就算盤勢一灘死水，它還是每 10 分鐘醒來檢查。

有一類開源 agent 把這件事做得更聰明，叫做 **heartbeat（心跳）**：

- [**OpenClaw**](https://github.com/openclaw/openclaw) 的 heartbeat 機制，是讓 agent 定時「醒來看一下狀態」，再**自己決定要不要行動**——比死板的 cron 多了一層判斷。它本質上就是「cron + 檔案狀態 + agent 自主判斷」的組合。
- [**Hermes**](https://github.com/NousResearch/hermes-agent)（Nous Research 開源）則把重點放在「醒來後能累積記憶、把學到的東西留下來」，讓每次定時醒來都比上次更懂你。

你可以把 heartbeat 想成 **crontab 的進化型**：cron 是「時間到就無腦執行」，heartbeat 是「時間到先醒來看看、再聰明地決定做不做」。這兩隻工具我會在系列後面各寫一篇深入聊，這裡先讓你知道：**當你開始嫌 cron 太死板，heartbeat 就是下一站。**

## 你可以怎麼開始

不用想太複雜，三步就能讓你的第一隻 agent 自己上工：

1. **先有一個「跑一次會完成某件事」的 agent 腳本**——可以是 `claude -p "..."` 一句話，也可以是你請 Claude Code 幫你寫好的 Python。先確定你手動跑它會動。
2. **`crontab -e` 加一行**，前面五個數字排好時間，後面接你的指令。**記得用絕對路徑、把輸出導到 log。**
3. **先排一個簡單、低風險的**——例如每天早上 9 點叫 agent 跟你說一句「今天的待辦有這些」。確認它真的會自己跑起來，那個「我沒做任何事但它動了」的瞬間會讓你上癮。

關鍵心法：**先讓 agent 學會自己起床，再慢慢加它起床要做的事。**

## 常見問題

### 為什麼我 crontab 排了卻沒跑？

**九成是環境問題。** cron 不讀你的 `.zshrc`，所以平常打得動的 `python3`、`claude` 在 cron 裡可能找不到。解法：用絕對路徑、在 crontab 最上面設 `PATH` 和 `ANTHROPIC_API_KEY`、把輸出 `>> log 2>&1` 導出來看錯誤。macOS 還要注意「完整磁碟取用權」。

### 電腦關機的時候 cron 就不跑了，怎麼辦？

對，crontab 跑在你自己電腦上，**關機/休眠就不會跑**。如果你的任務需要關機也能執行，可以考慮 Claude 的 Cloud Routines（雲端，但最小間隔 1 小時、約 3 天過期），或把 agent 跑在一台不關機的機器/小主機上。高頻又敏感的任務，還是建議留在自己常開的電腦上。

### crontab 和 Claude Cloud Routines 我該用哪個？

**要高頻（每分鐘到每幾分鐘）、長期常駐、資料不想出本機 → crontab；低頻又想關機也能跑、懶得設定 → Cloud Routines。** 我的股票盤中盯盤要每 10 分鐘，雲端最小 1 小時做不到，就只能用 crontab。很多人是兩個混用。

### 一定要會寫程式才能排 agent 嗎？

不一定。**最簡單的形式就是 `claude -p "你要它做的事"` 接在 crontab 後面**，一行就能跑。爬蟲、複雜邏輯那種才需要腳本，而且你可以直接叫 Claude Code 幫你把腳本寫好。你要做的是把「什麼時候做、做什麼」講清楚。

### cron 在 mac 上一直怪怪的，有替代方案嗎？

有。macOS 原生的 **launchd** 更貼合 mac，或在 Python 裡用 **APScheduler** 自己管排程，都能達到一樣的效果。如果你已經有一隻常駐的 agent（像 OpenClaw），也可以直接用它的 heartbeat 機制，連 cron 都不用碰。

## 結語

到這裡，[**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的四層就湊齊了：給它規則（instruction）、給它記憶（memory）、接上嘴巴（channel）、最後排好生理時鐘（cron）。**一隻會自己選股、自己爬資料、自己整理早報、做完還會傳訊息給你的 agent，骨子裡就是這四層轉起來而已。**

而 crontab 這層最迷人的地方，是它用一個幾十年的老工具，做到了一件很新的事——**讓一隻會思考的東西，照著你的作息表自己上工**。你不再需要記得「欸今天要掃一下」，因為它比你還準時。

如果你也有「每天固定要做一輪、又有點花腦力」的事，很適合養一隻 agent 用 cron 幫你顧著。要是你想做、但卡在「自己兜不起來」或「沒空慢慢試」，這正是我在做的事——我有提供 [**AI Agent 的諮詢與代建服務**](/ai-automation-workflow/)，幫你看怎麼設計、或直接幫你做出來。

這是 [**自架 AI Agent 實戰系列**](/posts/self-hosted-ai-agent/) 的第六篇，想看完整的四層觀念與其他篇，可以從總論進去。

延伸閱讀：

* [**自架 AI Agent 實戰（一）：在自己電腦養一隻會自己開工的 AI 員工**](/posts/self-hosted-ai-agent/) — 系列總論，四層觀念地圖
* [**用 Telegram / LINE 遙控你的 AI Agent、收任務通知**](/posts/ai-agent-channels-telegram-line/) — 系列 #5，cron 喚醒後靠 channel 回報你
* [**用 Claude Code 打造台股 AI Agent：盤中盯盤、訊號到就發 Telegram**](/posts/claude-code-stock-agent-monitor-alert/) — 本篇股票作息表的完整案例
* [**用 Claude Code + FinMind 追蹤台股**](/posts/claude-code-finmind-stock-tracking/) — 這一切的起點

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 聊聊你想做的 agent，或有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

掰掰～👋

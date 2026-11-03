# 下一批主題文章：GSC × Ahrefs 選題研究

> 建立日期：2026-11-03
> 資料來源：Google Search Console（sc-domain:homuchen.com；近 28 天 2026-10-05～11-01，對照 09-07～10-04；近 90 天 08-04～11-01）＋ Ahrefs Keywords Explorer / SERP Overview（台灣，2026-11-02）
> homuchen.com Ahrefs DR：**1.8**

## 一、GSC 現況（近 28 天）

### Top 頁面

| 頁面 | Clicks | 曝光 | CTR | 排名 | vs 前 28 天 |
|------|-------:|-----:|----:|-----:|------------|
| claude-code-finmind-stock-tracking | 463 | 7,764 | 6.0% | 5.7 | −135（−23%），排名 +0.5 |
| claude-code-stock-agent-monitor-alert | 440 | 3,583 | 12.3% | 4.8 | −137（−24%），排名 −0.1 |
| self-hosted-ai-agent | 240 | 2,741 | 8.8% | 5.6 | +30 |
| google-sheet-how-to-do-bookkeeping | 216 | 2,646 | 8.2% | 5.5 | −16 |
| markdown-tutorial | 183 | 11,447 | 1.6% | 6.5 | −96（−34%） |
| google-sheet-stock-income-statement | 153 | 2,921 | 5.2% | 5.6 | — |
| mcp-tools-skills | 80 | 1,297 | 6.2% | 5.1 | +7 |
| claude-code-shioaji-auto-trading-bot | 77 | 790 | 9.8% | 5.4 | 新文 |

- 前兩名股票文點擊各掉約 23%，但**排名沒掉**（±0.5 內），問題出在需求或 CTR 端，不是排名被搶走。
- 10 月交易系列新文合計帶來約 +170 clicks（shioaji 77、淨值儀表板 29、小台積 29、AI 助理 20、bug 文 16…），抵掉一部分跌幅。
- `stock-futures-tsmc-mini-futures-guide` 3,125 曝光、CTR 0.93%；`markdown` 5,772 曝光、CTR 1.5% → 兩篇都在 10/27 改過 title，**先觀察，不動**（基準見 memory `gsc-mcp-account`）。

### 關鍵觀察：泛 AI 大字我們吃不到，交集長尾才吃得到

| 文章 | 對應大字（Ahrefs 台灣月量） | 90 天 GSC 曝光 |
|------|---------------------------|---------------:|
| openclaw-ai-agent | openclaw 49,000 | 34 |
| claude-cowork-ai-from-chat-to-work | claude cowork 11,000 | 150 |
| what-is-ai-agent-vs-chatbot | ai agent 是什麼 1,300 | 233 |
| what-is-ai-agent-skill | claude skills 3,400 | 175 |
| hermes-ai-agent | hermes agent 14,000 | 1,986（CTR 1.7%） |

對照 `claude 股票`（Ahrefs 300/月）我們排 2.6、90 天 114 clicks。結論：**DR 1.8 的站打泛用大字很吃力，「Claude/AI × 具體場景（股票、記帳、自架）」的交集長尾才是我們的主場**。這跟 `seo-strongest-cluster` 的判斷一致，而且更明確了。

## 二、GSC 浮現、現有文章沒接好的意圖

| 意圖群 | 代表查詢（90 天曝光 / 排名） | 群組合計 | 目前落點 |
|--------|---------------------------|---------|---------|
| **股票 × Skill** | claude 股票 分析 skill 197/7.2、claude 股票 skill 189/6.8、claude 股票分析skills 90/7.3、股票skill 20、股票分析skill 20、股票 skill 16、股票 skills 14、claude 投資 skill 11 | ~557 曝光、排名 7 上下 | 沒有專文 |
| **AI 選股 / 指令** | 股票ai工具 95/9.2、ai選股指令 47/9.0、ai 股票 指令 43/10.3、ai 股票 分析 指令 25/13.3、ai 分析 股票 指令 23/13.3、ai股票分析程式 23/8.1、claude 選股 25/**1.4**（CTR 36%） | ~280 曝光 | 落在 stock-agent 文的一個段落 |
| **AI agent × LINE** | hermes agent line 174/8.6、claude 串 接 line 87/8.0、hermes agent line bot 67/6.9、串接 line 46/6.3、line 設定 36/8.4 | ~440 曝光 | channels 文（概念），**草稿 `drafts/2026-07-14-ai-agent-line-bot-tutorial.md` 還沒發** |
| **Codex vs Claude Code** | codex和claude code 8/11.1、codex 跟 claude code 差別 7/10.1、claude vs codex 8/18.1、claude codex 14/16.4…數十個變體 | 排名 10–20 | claude-code-vs-codex（title 沒對準「差別／比較」） |

## 三、Ahrefs 關鍵字與 SERP

### 搜尋量（台灣）

| 群組 | 關鍵字（月量 / KD / Traffic Potential） |
|------|----------------------------------------|
| AI 選股 | ai選股 400 / 0 / 200；ai 選股 150；股票ai分析工具 250；ai炒股 150；ai 股票 分析 指令 100；ai選股軟體 90；ai 股票 分析 提示 詞 80；ai選股app 80；ai量化交易 100 |
| 回測 | 回測 1,300 / 0 / **1,100**；回 測 350；股票回測 300 / 0 / 450；回測 意思 200 / 0 / 1,000；回測工具 200；台股回測 150；股票回測工具 150；股票回測意思 100；etf回測 100；0050回測 100 / 2 / 3,900 |
| 量化 / 程式交易 | 量化交易 3,100 / 0 / 200；程式交易 1,400 / 1 / 300；量化交易是什麼 300；量化交易策略 100；程式交易軟體 100 |
| Claude Skills | claude skills 3,400 / 2 / 1,000；claude skill 1,100；claude code skill 900；claude code skills 800；claude skills 教學 350 |
| Claude Code | claude code 教學 5,600 / 1 / 1,100；claude code 費用 2,700 / 0 / **3,300**；claude 費用 3,000；claude 方案 1,800；claude code 安裝 600 |
| 其他 | 股票損益計算 600 / 4 / **13,000**（我們排 8–10）；永豐 api 250；台股 api 100 |

### SERP 競爭判斷

| 關鍵字 | Top 10 長相 | 競爭程度 |
|--------|------------|---------|
| **ai選股** | 第 4 是 CMoney 論壇，第 5–6 是 DR 1–2 的小站（月流量約 20），其餘是新聞跟 App Store；**沒有完整的繁中實作教學** | **極低～低** |
| **回測** | 第 2 是 rich01（DR 52，流量約 780），第 3 是 ETF 比較工具，第 6–10 都很弱（流量 <60） | **低～中** |
| 量化交易 | 第 2 名 **FinLab（DR 17，主打 AI + Python 回測）**，接著是永豐、XQ、TEJ、元大等券商內容 | 中 |
| 程式交易 | FinLab DR 17 #2、期貨商、rich01 | 中 |
| claude skills | 官方 Help Center DR 92、數位時代 DR 77、104 DR 89、yu-wenhao DR 24… 8 篇以上 | 中～高（泛用字） |
| claude code 教學 | yu-wenhao（DR 24）#2、raymondhouch DR 39、數位時代、frankknow、iThome… 8 篇以上 | 中～高（飽和） |
| claude code 費用 | 數位時代 DR 77 #2，但 DR 5–12 的小站也拿到 500–875 流量 | 中 |

FinLab（DR 17）排得上「量化交易」、yu-wenhao（DR 24）排得上「claude code 教學」→ DR 低不代表完全沒機會，**內容切得準就有機會**。只是泛用字繁中文章已經很多，我們的差異化空間比交集長尾小。

## 四、建議選題（優先級）

| 優先級 | 文章 | 主要關鍵字 | 理由 |
|--------|------|-----------|------|
| **最高** | **A. AI 選股實戰：用 Claude Code + FinMind 打造自己的台股選股器（附指令）** | ai選股、ai 選股、股票ai分析工具、ai 股票 分析 指令 | SERP 幾乎沒人做完整教學；位在最強 cluster；`claude 選股` 已經排 1.4；memory 早就記錄「選股是沒被滿足的意圖」 |
| **最高** | **B. Claude 股票分析 Skill：把你的看盤／選股流程寫成 Skill（附範本）** | claude 股票 分析 skill、claude 股票 skill、股票 skill；次要 claude skills 範例 | 我們自己的 GSC 已有約 557 曝光在排名 7，但沒有專文接；用股票當切入口，避開泛用「claude skills」的紅海 |
| **高** | **C. 回測是什麼？不會寫程式也能用 AI 回測台股策略** | 回測、股票回測、回測 意思、台股回測、回測工具 | 整個群組約 2,900/月、KD 0、TP 1,100；4 篇回測文是現成素材（網格、進階網格、槓桿、選股策略），可以當 pillar 串起來，往課程 waitlist 導 |
| 中 | D. 量化交易／程式交易是什麼：散戶用 AI 入門 | 量化交易、程式交易、量化交易是什麼 | 量大（4,500/月）但 TP 只有 200–300，又有券商跟 FinLab 在搶；等 C 上線、站內回測主題成形後再做 |
| 中 | E. Claude Code 費用實測：Pro / Max / API 怎麼選 | claude code 費用、claude 費用、claude 方案 | TP 3,300、小站也排得上；但價格會變、要持續維護，而且要放你自己的真實用量才有差異化 |
| 中 | F. Claude Code 教學 hub：非工程師的 N 個實戰用途 | claude code 教學 | 量最大但已飽和；只有寫成「用途型目錄」、把站內案例（股票、記帳、Shopify、GSC、部落格）都串起來才值得做 |

### 不用寫新文的快速收穫

1. **發布 LINE 草稿** `drafts/2026-07-14-ai-agent-line-bot-tutorial.md`：約 440 曝光（hermes agent line / claude 串接 line）在等它。
2. **claude-code-vs-codex 改 title**：加入「差別／比較」，接住排名 10–20 的那一大串變體（Ahrefs：codex vs claude code 600、codex claude code 比較 450）。
3. **hermes-ai-agent 改 title**：1,986 曝光、CTR 1.7%，對準「hermes agent 是什麼／記憶／安裝」。
4. **google-sheet-stock-income-statement refresh**：股票損益計算 600–700/月、TP 13,000、我們排 8–10；SERP 頂端可能是計算機型頁面，可以考慮補一個試算範本。

## 五、A／B／C 關鍵字映射

### A. AI 選股

| 類型 | 關鍵字 |
|------|--------|
| 主要 | ai選股 |
| 次要 | ai 選股、股票ai分析工具、ai選股軟體 |
| 長尾 | ai 股票 分析 指令、ai選股指令、ai 股票 分析 提示詞、claude 選股 |
| 意圖 / 階段 | Informational + Commercial / Consideration → Implementation |
| 競爭 | 極低～低 |
| SEO 筆記 | 用「指令／提示詞」接聊天型使用者（ChatGPT、Claude 網頁版），再升級到 Claude Code + FinMind 的自動化選股；要誠實寫 AI 選股的限制（CMoney 那篇在談盲點，這是使用者在意的點）；內容邊界：只用回測數字 |
| 內鏈 | finmind-stock-tracking（top 1，反向灌權重）、stock-agent-monitor-alert、finmind-taiwan-stock-api-guide、mcp-tools-skills |

### B. Claude 股票分析 Skill

| 類型 | 關鍵字 |
|------|--------|
| 主要 | claude 股票 分析 skill |
| 次要 | claude 股票 skill、股票分析 skill、claude skills 範例 |
| 長尾 | claude 投資 skill、台股 skill、claude code skill 怎麼寫 |
| 意圖 / 階段 | Implementation |
| 競爭 | 低（股票 × skill 交集）；泛用 claude skills 為中～高 |
| SEO 筆記 | 附可以直接複製的 SKILL.md 範本；股票 agent 是 script + skill 接 FinMind，**不是 MCP**；跟 A 互相連結（A 講要選什麼，B 講怎麼打包成可重複使用的流程） |

### C. 回測是什麼

| 類型 | 關鍵字 |
|------|--------|
| 主要 | 回測 |
| 次要 | 股票回測、回測 意思、台股回測 |
| 長尾 | 回測工具、股票回測工具、etf回測、0050回測、ai 回測 |
| 意圖 / 階段 | Informational / Awareness → Consideration |
| 競爭 | 低～中 |
| SEO 筆記 | BLUF 先給定義，接著講回測常見的坑（過度擬合、倖存者偏差、交易成本），再用自己的網格／槓桿回測當 worked example；導向 ai-auto-trading-course waitlist；只用回測數字 |

## 六、跨平台發布狀態表

| 產出 | 類型 | 狀態 | 檔案路徑 | 發布連結 |
|------|------|------|---------|---------|
| A. AI 選股實測（140 個策略） | 部落格 | 已發布（2026-11-03） | `posts/2026-11-03-ai-stock-picking-taiwan-backtest.md` | https://homuchen.com/posts/ai-stock-picking-taiwan-backtest/ |
| A 篇 Threads ×6（拆 idea） | Threads | 已撰寫（approved，hq VM 排程每天發一則） | `threads/2026-11-03-ai-stock-picking-taiwan-backtest-01.md`～`-06.md` | — |
| B. Claude 股票分析 Skill | 部落格 | 規劃中 | — | — |
| C. 回測是什麼 | 部落格 | 規劃中 | — | — |
| LINE 串接草稿 | 部落格 | 草稿待發 | `drafts/2026-07-14-ai-agent-line-bot-tutorial.md` | — |
| claude-code-vs-codex title | 部落格更新 | 待做 | `posts/2026-06-24-claude-code-vs-codex.md` | — |
| hermes-ai-agent title | 部落格更新 | 待做 | `posts/2026-07-03-hermes-ai-agent.md` | — |

## 七、A 篇的素材與公開邊界（2026-11-03 使用者決定）

- 素材來源：`../../fire-auto/research/v2/`（`README.md` 假設總表、`HYPOTHESES.md` 數字、`experiments.jsonl` 289 筆執行紀錄）。`finance.homuchen.com` 跟選股關係不大，留給之後「AI 概念股／資產配置」主題。
- 實盤策略 H136：只講「股價強勢＋營收驚喜」的因子方向與回測數字；不寫精確公式、檔數、換股規則，也不說它是實盤策略。
- 6/4 股票 agent 文的舊策略已被重驗推翻：新文不提、舊文不改（見 memory `old-stock-strategy-no-retraction`）。
- 外部來源（財經 YouTuber 口訣、法人選股課程、社群圖卡）一律匿名。
- 角度：研究故事＋可複製方法。

## 八、寫作前需要確認的個人素材

- A：選股條件能公開到什麼程度？有沒有選股策略的全市場回測數字可以用？
- B：股票 agent 現在實際用的 skill 檔能不能拿來當範本（去掉敏感參數）？
- C：除了網格跟槓桿，還有沒有其他回測可以拿來當例子？有沒有回測做錯、後來才發現的經驗？
- E（如果要寫）：目前訂的是哪個方案、每月實際用量大概多少？

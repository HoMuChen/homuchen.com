# Personalized Style Guide — @homuchen.build.ai

> Generated from the user's historical Threads posts by `/setup`.
> Last updated: 2026-04-21
> Observational document — describes what the style is, not what it should be.

---

## Data Coverage

- Historical posts analyzed: 31
- Posts with reliable view data: 31 / 31
- Posts with reliable reply data: 31 / 31（10 篇有實際留言 thread）
- Time range covered: 2025-09-05 → 2026-04-17
- Confidence level: **Strong**（20–49 篇，可作為穩定工作基準；跨維度切片開始有意義但仍敏感於離群值）

---

## Style Snapshot

- Dominant content types: `opinion` 19 / `tutorial` 8 / `data-insight` 4
- Dominant hook types: 工具名 + 斷句（"Claude Code token 救星！"）、數字 / 研究錨（"Google DeepMind 跟 MIT..."）、日誌式開場（"今日辦公室！"、"最近..."）
- Typical word-count range: 中文字 42–475 chars，中位數 **319 chars**
- Typical paragraph count: 中位數 **6 段**（2–12）
- Typical ending patterns: 連結 + emoji 收束（`😎` `🎉` `😂`）、CTA 呼籲留言／追蹤、hashtag 片尾
- Typical emotional arcs: 資訊揭露型（發現 → 驗證 → 結論）、個人實驗型（痛點 → build → 展示）
- Typical register: 口語、輕鬆、帶繁中軟化語氣（`～`、`呢`、`惹`、`吧`），技術名詞保留英文

---

## Top-Quartile Patterns

> Top 25% = 7 篇（views 663+）。以下是其中重複出現的樣態。

| Pattern | Evidence Count | Performance Signal | Notes |
|---------|----------------|--------------------|-------|
| 工具名直接出現在第一行 | 4/7 | 平均 views 4,169 | Claude Code、Claude Cowork、NotebookLM、Codex；辨識度高、精準吸 in-group |
| 具體數字在前半段出現 | 5/7 | top 3 爆文都有（1/71.5、180 agents、515%） | 數字是錨，不是裝飾，直接支撐核心論點 |
| 標題式斷句開頭（12 字內收） | 4/7 | 平均 views 4,169 | "Claude Code token 救星！" 「一句話！用...」——先給鉤子再展開 |
| 反直覺或認知衝突的中段 | 3/7 | replies 顯著偏高（7–11） | agent 數量遞減、AI 味從哪來、粉絲數不能預測互動 |
| 中篇長度（150–400 chars） | 5/7 | 整體中篇 avg 1,558 views | 長文（400+）反而掉到 169 |

---

## Hook Types

| Hook Type | Usage Count | Avg Views | Avg Replies | Top-Quartile Hit Rate | Notes |
|-----------|-------------|-----------|-------------|-----------------------|-------|
| 工具名 / 產品名 hook | ~12 | ~1,700 | 1.9 | ~33% | 目前最可複製的 hook 家族 |
| 研究 / 數據錨頭 | 3 | ~1,280 | 4.0 | ~33% | 留言動機最強（Google DeepMind 論文 11 留言） |
| 問句 hook | 3 | ~3,290 | 2.3 | 1/7 | 樣本少但命中率高（AI味 9,653 即此類） |
| 日誌 / 個人實驗開場 | ~8 | ~570 | 0.9 | 1/7 | 親和力強，但擴散有限 |
| 系列標號開場 | 6 | ~140 | 0.2 | 0/7 | "Day N / 觀察 N" 目前帶不動外部流量 |

**Reference Strength**：工具名 hook（Usable）、問句 hook（Weak，僅 3 筆）、系列 hook（Weak，集中在兩個系列）。

---

## Hook Promise Fulfillment

| Pattern | Evidence Count | Performance Signal | Notes |
|---------|----------------|--------------------|-------|
| 第一段就拋核心結論 | 6/7 top quartile | 高 views + 高 likes 同步 | Graphify 第一句就講「token 省救星」，第二段立刻給 1/71.5 |
| 用具體數字兌現抽象承諾 | 4/7 top quartile | replies 偏高 | DeepMind 文把「agent 報酬遞減」兌現成 67 vs 21 vs 14 任務 |
| 結論在前 30% 就給讀者 | 5/7 top quartile | 符合 hook-payoff 最安全型態 | 即使滑走也拿得到一句結論 |
| hook 強 + 正文弱（危險型態） | ~2/31 整體 | 明顯低 views（<100） | 如：拋問題但未給答案的互動型貼文 |

---

## Ending Patterns

| Ending Type | Usage Count | Avg Views | Avg Replies | Share Signal | Notes |
|-------------|-------------|-----------|-------------|--------------|-------|
| 結論 + 單句金句收束 | ~9 | ~1,900 | 2.3 | 高 reposts | 爆文 pattern（Graphify 救星吧😎、515% overhead） |
| 附外部連結（blog / app） | 8 | ~1,540 | 0.6 | 中等 | 外部 link 不拖累，但留言動機會弱化 |
| 「連結附留言 👇」 | 2 | 顯著高於該主題均值 | 中等 | 高 | 演算法偏好：讀者被導到留言區 |
| Hashtag 串收尾 | 11 | ~440 | 0.4 | 低 | 大多是生活/vibe coding 系列，擴散不強 |
| 開放式提問 / 邀請留言 | 6 | ~250 | 1.0 | 低 | 意願有但無 signal 支撐 |

---

## Word Count And Structure

- Best-performing word-count band: **150–400 chars（中篇）**，n=16，avg views 1,558
- Typical paragraph-count band: 5–8 段，善用空行製造呼吸感
- Notes:
  - **短文（<150 chars）** n=8，avg 575 — 是日誌型，天花板低
  - **中篇（150–400）** n=16，avg 1,558 — **明顯的 sweet spot**
  - **長文（400–800）** n=7，avg 169 — 反直覺：**越長表現越差**，可能因資訊密度散掉、讀者中斷

| Structure Pattern | Usage Count | Performance Signal | Notes |
|-------------------|-------------|--------------------|-------|
| 鉤子 → 數字佐證 → 解釋 → 金句收 | ~6 | 穩定進入 top 25% | Graphify、DeepMind、Claude Cowork 都是此結構 |
| 鉤子 → 對照清單（A vs B） | ~3 | 擴散中等但 reposts 強 | Codex CLI 對照 Claude Code、Gemini vs Claude |
| 鉤子 → 故事錨 → 類比到 AI | ~2 | 留言動機佳 | ATM 比喻 AI、帕金森定律 |
| 功能清單 + emoji 條列 | ~5 | views 偏低 | Day 系列最常用此結構 |

---

## Pronoun And Register Use

| Feature | Baseline | Notes |
|---------|----------|-------|
| I / 我 / 自己 density | 高 | 大量第一人稱敘事，強化 parasocial 親近感 |
| You / 你 / 大家 density | 中 | 中度，常在 hook 與 CTA 使用（「大家有沒有覺得」、「你以為...」） |
| We / 我們 density | 低 | 不常用 in-group framing，可作為未來槓桿 |
| 軟化語氣標記 | 「～」6/31、「呢」「惹」「吧」零星 | 親和力來源，爆文仍保留 |
| Emoji 密度 | 平均 1.8 / 篇 | 收束點為主，正文不多；`😂` `😎` `🎉` 三神器 |
| 技術名詞 | 英文原文保留 | Claude Code、agent、Notion、webhook 不翻譯 |

---

## Content Types

| Content Type | Usage Count | Avg Views | Avg Replies | Avg Shares | Notes |
|--------------|-------------|-----------|-------------|------------|-------|
| tutorial | 8 | **2,529** | 2.4 | 高（Graphify reposts=23） | **單篇期望值最高**，但使用次數少 |
| data-insight | 4 | 1,037 | **3.0** | 中 | **留言密度最高**，最能引發討論 |
| opinion | 19 | 333 | 0.6 | 低 | 使用最多但單篇期望值最低 |

**關鍵觀察：** tutorial + data-insight 合計只佔 39% 的發文量，卻貢獻絕大多數爆文與留言。opinion 發最多，回報最弱。

---

## Emotional Arcs

| Emotional Arc | Usage Count | Avg Views | Avg Replies | Notes |
|---------------|-------------|-----------|-------------|-------|
| 發現 → 驗證 → 結論（資訊揭露型） | ~7 | ~2,100 | 2.6 | Graphify、DeepMind、AI 味、數據觀察 |
| 痛點 → build → 展示（個人工程日誌） | ~8 | ~280 | 0.9 | Day 系列、會議 app；親和但擴散弱 |
| 觀察 → 反直覺 → 建議（認知衝突） | ~3 | ~1,860 | 3.3 | 粉絲互動、agent 遞減 — 留言命中率最高 |
| 清單 / 工具推薦（低 arousal） | ~6 | ~440 | 0.3 | 轉發性弱，不觸發分享動機 |
| 觀光 / 咖啡廳 / 生活 | ~3 | ~110 | 0 | 目前不是主力 |

---

## Share And DM Drivers

| Driver | Evidence Count | Performance Signal | Notes |
|--------|----------------|--------------------|-------|
| 具體節省效益（token、時間、金錢） | 3 | reposts 9–23 | 1/71.5、省 token、自動化 — 有明確帶走的實用價值 |
| 讓讀者秒懂的對照 / 清單 | 2 | reposts 2+ | Codex vs Claude Code 對照、Gemini vs Claude |
| 反直覺論點 + 數據 | 2 | reposts 9 + reply 11 | 「agent 越多越好嗎」→ 挑戰既有信念 |
| 工具連結 + 可立即用 | ~6 | 穩定 repost 1–2 | 有 Practical Value 但身份訊號弱 |
| 心情 / 生活紀錄 | ~5 | reposts 0 | 不具 retellability，讀完沒有可傳給朋友的東西 |

**DM-forwardability 最強的一句話：** "每次查詢的 token 用量只需要原本的 1/71.5"（可直接複製丟給工程師朋友）。

---

## Topic Clusters And Repetition Pressure

| Topic Cluster | Usage Count | Recent Frequency | Performance Signal | Notes |
|---------------|-------------|------------------|--------------------|-------|
| Claude Code / Claude Cowork / Agent 工具 | ~13 | 高（近 2 週密集） | 平均表現高，但有疲勞風險 | 建議加入其他角度（案例/失敗/比較） |
| Vibe Coding / Build in Public 日誌 | ~7 | 中（2025-09–10 集中） | 弱擴散 | 系列停在 Day 3，未完的 open loop |
| Threads 數據 / 平台觀察 | 3 | 新興（3 篇內） | 留言密度高 | 最具差異化的 cluster，可擴展 |
| AI × 工作 / 職涯 / 替代 | ~4 | 低 | 中等 | ATM 比喻、Fiverr 下滑 — 可放大 |
| 生活 / 咖啡廳 / 旅行 | ~3 | 低 | 擴散弱 | 與主線 brand 脫節 |
| 讀書 / 思維模型（原子習慣、帕金森） | 2 | 低 | 擴散弱但留言 2 | 若與 AI 工作流結合可能升級 |

**疲勞風險：** `Claude Code + agent 工具` 近 2 週 5 篇以上，已進入 semantic cluster 密度警戒區。建議下一篇換 cluster，或從「失敗」「比較」「人機協作」的新角度切入。

---

## Topic Freshness Budget

> 本節在 `/setup` 階段為 baseline。跑 `scripts/update_topic_freshness.py` 後會填入精確的 semantic cluster 分數。

| Semantic Cluster | Similar Recent Posts | Days Since Last Similar Post | Freshness Signal | Fatigue Risk | Notes |
|------------------|----------------------|------------------------------|------------------|--------------|-------|
| Claude Code 工具 / token 省 | 6+ | < 3 | 偏低 | **高** | 需換 lens |
| Agent 架構 / 多 agent 爭論 | 2 | 5 | 中 | 低 | 可再深挖 |
| Threads 演算法觀察 | 2 | 10 | 高 | 低 | 最新鮮，有繼續產文空間 |
| 個人生產力工具（會議、桌面 app） | 4 | 14+ | 中 | 低 | 可回溫 |
| 自動化 / n8n / 檔案 | 4 | 40+ | 高 | 低 | 已退場久，可回來重啟 |

---

## Timing Notes

- Best posting windows（Asia/Taipei）：
  - **23:00**：n=8，avg 1,567 views（最大 9,699）— 最常用也最容易出爆文
  - **21:00**：n=4，avg 2,474 views（最大 9,653）— 樣本小但命中率高
  - **11:00**：n=1，avg 3,647 — 單筆 outlier（DeepMind 論文）
- Worst windows：14–19 時段普遍 < 600 views，職場時段競爭激烈且 AI 類內容訊號偏弱
- Day-of-week effects: 尚不可靠（樣本不足按週拆）
- Reliability of timing data: **中**，夜晚時段資料厚，白天時段單筆為主

---

## Signature Phrases

- "～"（中斷句軟化音，非問尾，6 次）
- "欸"／"惹"／"吧"（口語語助詞，零散出現於結尾）
- "有興趣的可以去看看" / "反應熱烈的話再加快" （CTA 軟邀請）
- "跟大家分享一下" / "分享一個" （導入句）
- "救星" / "神器" / "超猛" （工具讚嘆詞）

---

## Confidence Notes

- **Strong claims**（資料穩固）：
  - tutorial / data-insight 的期望值顯著高於 opinion
  - 中篇（150–400 chars）是表現 sweet spot
  - 工具名 hook 是 top quartile 最常見的 hook 家族
  - Claude Code 主題已進入疲勞警戒

- **Weak / thin-sample claims**（需更多資料）：
  - 問句 hook 命中率（僅 3 筆）
  - 21:00 vs 23:00 哪個更好（樣本差距大）
  - 系列文真正表現（Day 系列停在 Day 3、數據觀察僅 2 篇）
  - Day-of-week 與星期效應

- **Missing data caveats**：
  - `algorithm_signals` / `psychology_signals` 所有欄位目前為 `null`，需 `/analyze` 或 `/review` 逐步回填
  - 外部 discovery surface（Threads / IG / FB 來源比例）未知，API 目前不提供
  - 留言內文只有 10 篇 post 抓到；其餘可能是沒留言或 API 限制

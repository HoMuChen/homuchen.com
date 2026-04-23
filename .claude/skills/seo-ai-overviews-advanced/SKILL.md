---
name: seo-ai-overviews-advanced
description: |
  進階 AI 搜尋最佳化：Google AI Overviews、ChatGPT、Perplexity、Gemini 的
  per-platform 戰術、query fan-out、AI visibility audit、brand gap analysis、
  LLMO 10 招、llms.txt 決策、AI traffic 追蹤。比通用 `ai-seo` 更深入，
  專注在「可量測、可追蹤、跨平台差異」的戰術。
  當使用者提到「AI Overviews」「query fan-out」「llms.txt」「LLMO」
  「AI visibility」「讓 ChatGPT/Perplexity 引用我」「AI 流量怎麼看」
  「各個 AI 搜尋平台差異」時使用。也適用於規劃 AI 能見度 audit。
---

# SEO AI Overviews 進階戰術

處理 AI 搜尋時代的可量測戰術：如何讓內容被不同 AI 平台引用、怎麼做 visibility audit、怎麼追蹤 AI 流量、各平台的差異化最佳化。基於 15 篇 Ahrefs 深度文章方法論萃取。詳細方法論見 `REFERENCE.md`。

---

## When to Use

- 想知道「為什麼 ChatGPT 都不引用我的文章」
- 要做 AI visibility audit（完整盤點 AI 曝光）
- 追蹤 AI 帶來的流量（ChatGPT / Perplexity / Google AI Mode）
- 規劃 per-platform 的 AI SEO 戰術（不同 AI 引用邏輯不同）
- 評估要不要做 llms.txt
- 分析競品在 AI 搜尋的優勢
- 寫 AI 相關主題文章，想被 LLM 引用

如果只是基本 AI SEO 觀念，用通用 `ai-seo` skill 即可。

---

## 核心心智模型：Query Fan-Out

**最重要的一個觀念**：一個使用者 query 在 AI Overviews 底下，會被拆解成 **9-11 個 sub-queries** 平行查詢。

拆解維度：
- **Disambiguation**（澄清模糊意圖）
- **Entity attributes**（屬性平行探索）
- **Journey stages**（決策階段）
- **Trust signals**（高風險 query 的可信度驗證）
- **Comparison criteria**（比較維度）

**對 SEO 的意涵**：排 #1 已經不夠。要被引用，必須在 fan-out 變體中都有覆蓋。**跨多個 fan-out query 都排得上的頁面，被引用機率提高 161%**。

**戰術**：用 Qforia 類工具抽出 Google 對主要關鍵字的 fan-out sub-queries，把內容覆蓋到這些角度。

---

## Content Structure for LLM Citability

### Bottom Line Up Front（BLUF）結構

LLM 是 RAG 系統，會把內容切成 chunk 做 retrieval。你的每個 section 都要能「被單獨擷取出來回答問題」。

**每段的結構**：
1. **開場陳述**：直接回答（1-2 句）
2. **支撐 context**：為什麼重要（2-3 句）
3. **詳細說明**：細節、例子、證據
4. **下一步**：相關 query 或行動

### 章節設計

- 用問句做 heading（符合使用者 query 格式）
- 列點清單、表格多用（方便 chunk 擷取）
- 實作 schema markup：`Article`、`HowTo`、`FAQPage`、`Speakable`
- 自然段長度約 200 字（RAG 擷取甜蜜點）
- **內容長度目標**：引用最大化的 plateau 約在 540 字，超過沒有增益，topic 決定長度不是字數

### Entity Proximity 戰術

LLM 透過 embedding + 詞彙鄰近判斷意義。把你的品牌放在有商業價值的 entity 旁邊：
- 與權威品牌語意共提
- 結構性鄰近（同段、同列表）
- 用 Google Natural Language API 或 Inlinks Entity Analyzer 做 entity 研究（比 keyword 更有效）

---

## llms.txt：該不該做？

**目前建議：先不要**（2026 狀態）

- OpenAI / Anthropic / Google 都還沒承諾會 parse
- 沒有證據它會提升引用、流量、精確度
- 類比：等同被棄用的 keywords meta tag

**如果要低風險 prep**：
1. 在 `/llms.txt` 放一個 Markdown 檔
2. 用 H2：`## Docs`、`## Policies`、`## Products`、`## Setup`
3. 連結結構化、markdown-friendly 的內容
4. 只在你本來就有高度結構化內容時做
5. 監控主要 LLM 提供商是否採用

---

## AI Visibility Audit 8 步驟框架

**用於**：完整盤點品牌在 AI 搜尋的曝光，對應實作優先順序。

1. **定義範圍** — 選平台（AI Overviews / ChatGPT / Perplexity / Gemini / Copilot / Claude）、列品牌 entity（本名、縮寫、子品牌）、選區域語言、設定 baseline
2. **Benchmark 當前曝光** — mentions、citations、impressions、AI Share of Voice、搜尋需求趨勢
3. **分析品牌相關回應** — AI 如何描述你？準確度、sentiment、差異化、權威訊號、CTA
4. **盤點非品牌 query + 主題關聯** — 競品有但你沒有的主題、未擁有的 query 機會、主題權威缺口
5. **找高被引用頁面** — AI 最常引用哪些頁？內容結構、長度、freshness 模式
6. **評估品牌提及** — 誰在提你？權威度如何？第三方提及怎麼影響 AI 回應？
7. **競品比較** — 跟前 3-5 名競品對比所有指標
8. **行動策略** — Fix（修正錯誤） / Build（新建內容） / Influence（外部提及）三類，按 ROI 排序

**工具**：
- Ahrefs Brand Radar（多平台引用追蹤）
- Ahrefs Site Explorer（organic rank + AI Overview 可見度）
- Site Audit（technical issues）
- GA4 custom channel grouping

---

## Brand Gap Analysis：為什麼 AI 搜尋看不到你

六種核心缺口：

| 缺口類型 | 說明 |
|---------|------|
| **Visibility Gap** | 比競品少出現 |
| **Narrative Gap** | AI 描述你 vs 你想的定位不同 |
| **Topic Gap** | 你該擁有但被競品佔領的主題 |
| **Format Gap** | 缺少 AI 常引用的內容格式（how-to、comparison、best-of） |
| **Web Mentions Gap** | 外部站提競品但沒提你 |
| **Demand Gap** | 未開發的品牌搜尋機會 |

### 7 步驟診斷流程

1. **定義品牌 entity 與主題** — 列所有變體（本名、縮寫、產品名）
2. **Benchmark 當前曝光** — 用主題 cluster 看 share of voice，不是單一關鍵字
3. **找未擁有的品牌字** — 你不排第 1 的品牌搜尋
4. **分析 AI 搜尋缺口**（最關鍵）— 競品在但你不在的 AI 回應；你被提錯/不完整的地方；競品內容為什麼被引用？
5. **Audit 網路提及** — 對手出現在哪些媒體？你沒出現？
6. **跟競品對標** — 3-5 個競品完整分析
7. **優先排序 + 溝通** — Fix / Build / Influence 三分類

---

## 10 招 LLMO 戰術（讓品牌進入 AI 回答）

### 1. PR for Topical Association
- 拿到新聞報導把品牌跟關鍵主題連在一起
- 發 press release 強調主題-品牌關聯性
- 跟互補品牌合作
- 做研究報告建立主題權威
- 數位 PR 從高權威域名導流提及

### 2. Content with Quotes & Statistics
**金句與統計提升 RAG 被引用機率**：Quotes +27.2%、Statistics +25.2%
- 原創研究與資料
- 可信的第三方引用
- 高層管理權威發言
- 獨特洞見與統計
- 用易擷取格式發布

### 3. Entity Research 不是 Keyword Research
- 用 Google Natural Language API 找相關 entity
- 用 Inlinks Entity Analyzer 做主題地圖
- 用 Ahrefs AI Content Helper 做 entity gap 分析
- 繞著 entity cluster 建內容

### 4. Brand Radar 持續監控
- 追蹤跨平台 mentions vs 競品
- Benchmark 關鍵主題的 share of voice
- 發現 partnership / citation 機會
- 月度 citation 趨勢報告

### 5. Wikipedia 條目（高槓桿）
LLM 大量訓練於 Wikipedia。若達 notability：
- 嚴格遵守 notability guidelines
- 只引可信來源
- 保持中立觀點
- 揭露利益衝突
- 建立主題相關的 Wikipedia 回鏈

### 6. Brand Question 最佳化
- 用 Ahrefs Matching Terms + "Questions" + "Brand" filter
- 監控 LLM auto-complete 的新興品牌問題
- 用 BLUF 結構回答
- 追蹤哪些 brand question 引用率最高

### 7. Reddit UGC（社群建立）
Reddit 是關鍵 LLM 訓練資料：
- 在相關 subreddit 做 AMA
- 跟 KOL 合作拿到真實推薦
- 鼓勵 UGC 與評論
- 監控 subreddit 對話找提及機會
- **忌：不要 spam**

### 8. LLM Feedback 直接訓練
- 用 Gemini feedback 工具修正資訊
- 評分 ChatGPT 提到你品牌的回應
- Claude Projects custom training 提供修正
- 偵測到品牌錯誤資訊就 flag

### 9. 維持核心 SEO
Organic 排名跟 LLM 提及相關係數約 **0.65**。排名還是最重要。
- 別因為 AI SEO 就放掉傳統 SEO
- 鎖定前 10 名 SERP 位置
- 技術 SEO 仍然關鍵

### 10. 避免黑帽
別做 prompt injection、假引用、假第三方提及、刻意 decoy 內容餵 LLM 爬蟲。長期會被反噬。

---

## 追蹤 AI 流量（實作方法）

### Method 1: GA4 Custom Channel

Regex pattern：
```
.*chatgpt\.com.*|.*perplexity.*|.*gemini\.google\.com.*|.*copilot\.microsoft\.com.*|.*openai\.com.*|.*claude\.ai.*
```

1. GA4 admin → Data Stream
2. 建立 custom event parameter 偵測 AI 平台
3. 用 regex match referrer URL
4. 歸入 "AI Platforms" channel
5. 跟 organic search 分開追蹤

**限制**：24-48 小時歸因延遲

### Method 2: Ahrefs Web Analytics
- 輕量替代，即時顯示（1 分鐘內）
- 內建 AI 平台 filter
- 決策更快

### Method 3: Ahrefs Brand Radar
- Site Explorer 總覽 AI Overview citations
- 用紫色 "AI Overview" checkbox filter
- 看個別 prompt、競品定位、新勝關鍵字 alerts

### Method 4: 關鍵字層級追蹤
Site Explorer → Organic Keywords → filter "SERP features > Current > Include target in > AI Overview"

---

## Per-Platform 最佳化差異

### Google AI Overviews
- **前提**：必須排進 organic top 10（中位數 #2）
- **觸發**：Why 問題觸發 59.8% overviews、7+ 字 query 觸發 46.4%
- **訊號**：brand mentions 相關係數最高（0.664）
- **結構**：schema markup（Article、HowTo、FAQPage）
- **freshness**：更新過的內容偏好 +13.1%
- **資料點**：76% 被引用域名也排進 organic top 10

### ChatGPT
- **重點**：quotes +27.2%、statistics +25.2%
- **原創**：原創研究與資料
- **Entity**：你的品牌在 embedding 中被哪些 entity 包圍
- **Bot 存取**：讓 GPTBot 爬（約 5.9% 網站不必要地擋了）
- **Freshness**：比 organic 新 25.7%

### Perplexity（學術式取用）
- **多來源驗證**：要跟競品一起被引用才會穩
- **學術可信度**：研究類主題表現好
- **第三方驗證**：跟權威的共提很關鍵
- **技術內容**：Perplexity 對技術/研究類超偏好
- **作者可信度**：個人專業 + 資歷比企業名氣重要

### Google Gemini / AI Mode
- **Freshness**：比傳統 Google 還看重
- **更新速度**：常更新的頁面勝出
- **多平台**：YouTube 提及相關係數 0.740（最強）
- **"Best of" 清單**：48.90% AI Overviews 引用，要主動讓品牌進入
- **UGC**：Reddit、YouTube、評論加權很高

### Copilot（entity recognition）
- Wikipedia 槓桿比 Google 系統還高
- Knowledge Graph entity linking
- LinkedIn / 企業資料平台 / 業界資料庫
- Yelp、業界評論
- Microsoft 生態系提及（Azure、M365）

### Claude（Constitutional AI）
- 清楚 attribution（來源必須可驗證）
- 事實準確性（hallucination penalty 高）
- 透過 feedback 工具修正錯誤重要
- Peer-reviewed / 公認媒體來源
- 透明（說明限制與不確定性）

---

## 關鍵成功指標

| 指標 | 工具 | 頻率 |
|------|------|------|
| 總 AI citation 數 | Brand Radar | 月 |
| 平台別 citation | Brand Radar | 月 |
| AI 流量 | GA4 / Ahrefs | 日 |
| 主題 Share of Voice | Brand Radar | 季 |
| Top-cited 頁面 | Brand Radar | 月 |
| 新勝關鍵字 | Ahrefs Alerts | 週 |
| 傳統 SERP 排名 | Site Explorer | 週 |
| 網路品牌提及 | Brand Radar | 月 |
| 內容 freshness | Site Explorer | 季 |
| Fan-out query 覆蓋 | 手動 audit | 季 |

---

## Humanize AI Content：遇到寫作被標記為 AI 時

**核心問題**：傳統 humanization 流程根本是自我毀滅（工程師基本上從頭改寫，AI 的速度優勢歸零）。

**替代作法**：把 AI 當 ideation / outlining / drafting 輔助，不是主要產生器。

1. Ideation：用 AI 探索主題角度
2. Outline：讓 AI 建議結構
3. Research：AI 初步研究 + 第一手來源驗證
4. Draft：人類大幅改寫 AI 草稿
5. Overlay：加上個人經驗、案例、原創洞見
6. Tone：重寫成品牌聲音

**被標記為 AI 的補救**：
- 用原創研究/資料開場
- 加入第一人稱經驗與案例
- 引用專家與權威來源
- 用口語化語言
- 圍繞真實故事建構敘事
- 有反主流意見或獨特觀點
- 強調個人專業領域

---

## 參考資料

完整方法論、所有 Ahrefs 具體數據、各平台細節見同資料夾 `REFERENCE.md`。

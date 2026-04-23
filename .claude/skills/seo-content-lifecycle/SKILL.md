---
name: seo-content-lifecycle
description: |
  內容生命週期管理：偵測文章衰退（content decay）、決定要更新還是剪枝、
  建構主題地圖（topical map）、辨識搜尋意圖轉變、為 AI 時代寫出「deep content」。
  當使用者提到「文章沒流量了」「要不要更新舊文」「這篇要砍嗎」「內容怎麼老化」
  「topical authority」「content refresh」「republish」「content pruning」時使用。
  也適用於規劃主題地圖、決定文章之間該怎麼串起來。
---

# SEO 內容生命週期管理

處理既有內容在時間推移下的維護決策：要更新、要剪枝、還是放著不動。基於 Ahrefs 89 篇精選文章的方法論萃取。詳細方法論見同資料夾的 `REFERENCE.md`。

---

## When to Use

- 某篇舊文流量掉了，不知道是什麼問題
- 手上有 100+ 篇文章，不確定該維護哪些
- 要規劃新系列，不知道怎麼排主題結構
- 想知道「刪掉低流量文章」到底有沒有用
- 寫 AI 時代的文章，想知道什麼內容才會被 LLM 引用

---

## Core Decision Tree

```
文章流量下滑
    ↓
用 GSC 看 Impressions × CTR
    ↓
├─ Impressions ↓ + CTR ↓  → 典型 decay（過時/意圖漂移）→ 評估 refresh
├─ Impressions ↓ + CTR ↑  → SERP 排名掉了（內容還相關）→ 強化權威訊號
├─ Impressions → + CTR ↓  → SERP feature 吃掉點擊（AIO/snippet）→ 重新設計答案結構
└─ Impressions → + CTR →  → 不是 decay，監控其他因素
```

---

## 核心判斷：該 Refresh、Prune、還是放著？

### Refresh（更新並重發）— 四個條件都成立才做

1. 主題仍對應部落格核心定位與讀者
2. 問題是內容品質，不是沒有外部連結
3. 搜尋需求沒有持續 YoY 衰退（不是進入 Decline 階段）
4. 搜尋意圖沒有根本轉變（用 Ahrefs "Identify Intents" 確認）

### Prune（剪枝刪除）— 必須全部成立

- 月流量 < 50、幾乎沒有 backlink
- 主題已經不符合部落格方向
- 沒有可以合併過去的更強文章
- 沒有歷史/品牌/支援價值

### 放著不動

- 主題還對，但流量也還 OK
- 在做 SEO 之外的價值（例如：被當 portfolio 或個人故事）

---

## ⚠️ 最重要的地雷：Date Change Trap

**絕對不要**只改 publish date、不做實質更新。Google 會偵測這種「化妝式更新」，反而更糟。每次 refresh 必須：

- 新增有資訊增益（information gain）的內容（新資料、新觀點、新案例）
- 全文改寫目標：50% 以上是新內容
- 快速更新目標：修正過時數據、補充遺漏的 subtopic

---

## Refresh 8 步驟工作流

1. **找候選人** — 從 GSC 找下滑頁面（YoY > 20% 跌幅）
2. **看競品怎麼更新** — 他們版本加了什麼？減了什麼？
3. **看 AI 引用變化** — 如果競品 AI 引用數暴增，抽取他們新加的主題
4. **跑四條件 checklist** — 任一條件失敗就改成 redirect 或 prune
5. **補 topical gap** — 用 SERP 前 3 名對比自己的文章，找缺的 subtopic
6. **On-page 優化** — title 加年份、meta description 重寫、H2/H3 重構、加入新內部連結、schema 更新 dateModified
7. **加資訊增益** — 新數據、原創觀點、訪談、案例
8. **重新推播 + 追蹤** — Email 名單、社群、內部連結強化；追蹤 3-4 週

---

## Topical Map 建構 7 步驟（系列文章規劃用）

寫系列文章前必走。輸出是一份表格：`Main Topic | Subtopic | Brand Relevance (0-3) | Traffic Potential | Existing URL | New URL | Priority`

1. **定義 Main Topic** — 部落格核心定位（例：「AI 協作工作流」「個人生產力」）
2. **腦力激盪 Sub-topics** — 用 Ahrefs Parent Topic、Wikipedia 大綱、競品 site map、PAA、「People Also Search」
3. **Rate Brand Relevance 0-3**
   - 0 = 完全不符合品牌定位
   - 1 = 邊緣，轉換潛力低
   - 2 = 合適，跟現有內容有連結
   - 3 = 核心主題，必寫
4. **驗證 Traffic Potential** — 聚合相關關鍵字的 TP 總和，<50 可降優先
5. **Finalize** — 剔除 Brand Relevance + TP 雙指標都 < 2 的
6. **Map URLs** — 已存在/尚未寫的分開標記
7. **Priority Score** — TP(40%) + Brand Relevance(30%) + 競品缺口(20%) + 可行性(10%)

---

## Search Intent Shift 診斷

六種意圖漂移的模式：
1. 重大新聞事件（例：疫情期間「遠端工作」整個 SERP 被重寫）
2. 文化趨勢
3. 人物爆紅（KOL/CEO/名人）
4. 縮寫含意改變（LLM 從「法學碩士」變「大型語言模型」）
5. 新產品問世搶走關鍵字
6. 細微的語意漂移（例：「跑鞋」往「恢復型跑鞋」漂移）

**診斷方法**：Ahrefs Keywords Explorer → SERP Overview → 選兩個時間點 → Identify Intents 對比比例。

**三種應對方式**：
| 方式 | 什麼時候用 | 成功率 |
|------|----------|-------|
| Rewrite & realign | 確認是永久轉變 | 60-80% |
| 策略性觀望 | 疑似暫時現象（新聞事件） | 85%+ |
| 接受並 redirect | 永久且低價值（縮寫改變） | 100% |

---

## Fresh Content 訊號清單

**關鍵發現**：AI 引用的內容，比 Google organic 結果新 25.7%。LLM 偏愛比一般搜尋結果新 393-458 天的 URL。對 AI SEO 來說，freshness 比傳統 SEO 還重要。

**具體動作（依影響力排序）**：
1. 替換過時數據（> 2 年的數據全部檢查）
2. 更新產品版本（截圖、價格、功能）
3. 在季節性需求尖峰前 3 個月更新
4. 在文章顯眼處放「最後更新日期」（header/footer，ISO 格式）
5. 更新 schema markup 的 `dateModified`
6. 加入更新的內部連結（從較新的文章連過來）
7. 用 IndexNow 通知搜尋引擎重新爬
8. 重新推播（Email、社群）

---

## Deep Content for AI Era

**核心原則**：LLM 會引用「難以自動生成」的內容。如果內容只是常識整理，LLM 自己就能產，不會引用你。

**會被 LLM 引用的內容類型**：
- ✅ 原創研究 + 統計（引用率最高）
- ✅ 實作框架 / 決策樹 / checklist
- ✅ 有實作細節 + 踩雷經驗的 hands-on tutorial
- ✅ 真實 case study + 具體結果

**會被 LLM 跳過的內容類型**：
- ❌ 純程序性教學（「怎麼重灌 macOS」）
- ❌ 常識重組（AI 自己就能寫）
- ❌ 觸發 featured snippet 的 query（通常太淺）

**Depth Checklist（發文前跑過一次）**：
- [ ] 不只講 What，也講 Why 和 When applicable
- [ ] 有決策框架（「如果 X 則 Y；如果 Z 則 W」）
- [ ] 有原創數據或未公開研究
- [ ] 提供模板、下載工具、或 checklist
- [ ] 有具體結果的真實例子
- [ ] 需要專業知識才能合成（不是顯而易見）

---

## 關鍵字三角色（單篇文章內的關鍵字架構）

一篇文章的關鍵字不是越多越好，而是有結構：

### Role 1: Focus Keyword（主關鍵字，一篇一個）
放在：URL slug、title（前 60 字元）、H1、meta description、首 100 字。

### Role 2: Secondary Keywords（次關鍵字，3-5 個）
同一個 Parent Topic、同一個搜尋意圖。自然融入 body、H2/H3、alt text。
**不要**另開頁面去排，那是 cannibalization。

### Role 3: Topical Relevance（主題相關性）
透過 5-10 個語意相關詞彙 + 模仿 SERP 前 3 名的結構 + 回答 PAA 問題，讓 Google 判定這篇「覆蓋完整」。

---

## 文章寫完的最後 check（在 commit / 發布前）

- [ ] 關鍵字三角色都有策略性處理（focus + secondary + topical）
- [ ] 結構跟 SERP 前 3 名相比沒有遺漏 subtopic
- [ ] 有 information gain（不是別人寫過的東西重組）
- [ ] 如果是 refresh：> 50% 內容是新的，不是只改日期
- [ ] `dateModified` 的 schema 已更新
- [ ] 至少有 3 個內部連結（從新文章連過來 + 連到相關舊文）

---

## 參考資料

完整方法論、具體 metrics、更多案例見同資料夾 `REFERENCE.md`。

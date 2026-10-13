# 用 AI 打造自動化交易系統 — 課程大綱 v1

---

## 課程總覽

- **總時數：6-8 小時**
- **章節數：7 章 + Bonus**
- **核心理念：每一章都有實作 demo，全程用 Claude Code 對話完成，學員不需要自己手寫程式**
- **貫穿案例：小型台積電期貨（QFF）網格機器人**——跟 fire-auto 的真實系統同一條路線，但課程內用教學用參數，不公開作者實盤設定
- **環境：** macOS / Linux / WSL、Python（uv）、Claude Code、FinMind 帳號、永豐金證券帳戶（Ch5 起需要；沒有帳戶可只跑到 Ch4）

---

## 第一章：資料層——先讓 AI 拿到乾淨的資料（45 分鐘）

### 觀念
- 為什麼資料是交易系統最容易出錯、又最不會報錯的地方
- 日 K vs 30 分 K：網格需要盤中波動，日 K 會低估成交
- 本地快取：抓一次、存成 CSV，回測跑一百次都不用重抓

### 實作 Demo
- 叫 Claude Code 寫 FinMind 抓取腳本 + 本地快取
- 期貨資料的眉角：同月雙代碼、近月連續合約

### 案例 Demo ①：FinMind 一次只回 N 筆的坑
重現 #6 第 1 個 bug（資料筆數上限被默默截斷），示範「用真實資料抽查」怎麼抓到它。

---

## 第二章：策略研究——叫 Claude 幫你做實驗（1 小時）

### 觀念
- 把「我覺得」變成「可以被回測的規則」
- 網格交易是什麼、適合什麼市場、什麼時候會凍結
- 一次只改一個變數：實驗紀錄怎麼寫（`strategies/*.md`）

### 實作 Demo
- 跟 Claude Code 對話：從一句話策略 → 規則 → 第一版回測
- 讓 AI 自動跑參數掃描、把結果寫成研究筆記

### 案例 Demo ②：網格收租實驗
用台積電 6 年資料重跑 #2 的研究：99% 的月份有收入，卻輸給買進持有——教學員怎麼誠實看待「看起來很好」的結果。

---

## 第三章：回測與防過擬合（1 小時）

### 觀念
- 成本一定要算：手續費、交易稅、滑價、轉倉成本
- 參數高原 vs 參數尖峰：好參數附近也要好
- 群組驗證 / 分期驗證：不要只在一段歷史上好看
- 報酬的分母：有補保證金就要算進本金

### 實作 Demo
- 叫 Claude 加成本模型、畫參數熱力圖
- 槓桿 1x / 2x / 3x 對照（#4）：報酬翻倍、回撤從 −22% 變 −62%

### 案例 Demo ③：轉倉回補的假獲利
重現 #6 第 2 個 bug（back-adjust 讓回測多出不存在的獲利），示範怎麼要求 AI 列出它的假設。

---

## 第四章：提醒模式——先讓它喊，不讓它下（45 分鐘）

### 觀念
- 兩階段上線：提醒模式 → 下單模式
- 訊號邏輯和下單邏輯分開，提醒模式就是「下單程式的乾跑」
- 盤中排程：cron、交易時段判斷、假日

### 實作 Demo
- 訊號腳本 + Telegram Bot 通知
- crontab 排程（銜接 [/posts/crontab-ai-agent-schedule/](https://homuchen.com/posts/crontab-ai-agent-schedule/)）

### 案例 Demo ④：盤中成交量縮水
重現 #6 盤中 K 棒還沒收完就拿來判斷的 bug。

---

## 第五章：下單模式——Shioaji 串接（1.5 小時）

### 觀念
- 永豐 Shioaji API：申請、憑證、API 同意書、模擬環境（文字說明流程）
- 限價單 vs 市價單、委託狀態、部分成交、撤單
- 期貨合約選擇與轉倉時機

### 實作 Demo
- 叫 Claude Code 讀 Shioaji 官方文件 / skill，寫登入、查部位、下單、撤單
- 在模擬環境讓 agent 自己跑一輪完整流程

### 案例 Demo ⑤：OrderStatus 前綴與轉倉順序寫反
重現 #6 的委託狀態判斷 bug 與轉倉順序 bug，示範「先平舊再建新」為什麼重要。

---

## 第六章：安全機制與對帳——把 AI 關在籠子裡（1 小時）

### 觀念
- 前提：**假設程式一定有你沒發現的 bug**
- 9 道安全機制（對應 #1 總表）：opt-in 旗標、kill switch、每輪先跟券商對帳、下單前查真實保證金、槓桿上限（對真實權益）、口數硬上限、每輪最多 1 張單、限價單 + 逾時撤單、出任何例外就停機
- 對帳：本地帳本 vs 券商部位，不一致就停

### 實作 Demo
- 逐一加上安全機制，並刻意製造會被擋下的情境測試
- 叫 AI 寫一致性檢查

### 案例 Demo ⑥：槓桿上限只看保證金 → 實際 ~7 倍
重現 #6 第 6 個 bug，示範為什麼上限要用「名目價值 / 權益」算，以及 derisk=0 被當成門檻的坑。

---

## 第七章：上線維運（45 分鐘）

### 觀念
- 部署：本機常駐 vs 小主機、log 與通知
- 自動轉倉、到期日提早收盤
- 記帳與月報：讓 AI 每月幫你整理交易紀錄
- 什麼時候該關掉它：策略失效的訊號

### 實作 Demo
- cron + log rotate + 異常通知
- 每月自動產出交易摘要

---

## Bonus：網格進階手法實測（30 分鐘）

- 移動停利：有效（回測 CAGR 7.0% → 7.8%、乾旱月 7 → 4）
- ATR 動態格距、加大格距：回撤更差
- RSI 過濾：毒藥（CAGR 掉到 2.8%、乾旱 18 個月）
- 對應文章 #5（待寫）

---

## 每章素材對照

| 章 | 對應文章 | fire-auto 素材 |
|----|---------|---------------|
| 1 | [/posts/claude-code-finmind-stock-tracking/](https://homuchen.com/posts/claude-code-finmind-stock-tracking/) | `stock_cache.py`、`research/futures_cache.py` |
| 2 | [/posts/grid-trading-backtest-tsmc/](https://homuchen.com/posts/grid-trading-backtest-tsmc/) | `strategies/tsmc_grid_income.md`、`research/tsmc_grid_income.py` |
| 3 | [/posts/futures-leverage-backtest/](https://homuchen.com/posts/futures-leverage-backtest/) | `research/tsmc_futures_grid_30min.py` |
| 4 | [/posts/claude-code-stock-agent-monitor-alert/](https://homuchen.com/posts/claude-code-stock-agent-monitor-alert/) | `futures_grid_monitor.py`、`notify.py` |
| 5 | [/posts/claude-code-shioaji-auto-trading-bot/](https://homuchen.com/posts/claude-code-shioaji-auto-trading-bot/)、[/posts/stock-futures-tsmc-mini-futures-guide/](https://homuchen.com/posts/stock-futures-tsmc-mini-futures-guide/) | `futures_live.py` |
| 6 | [/posts/ai-coding-trading-bot-bugs/](https://homuchen.com/posts/ai-coding-trading-bot-bugs/) | `futures_live.py`、fix commits |
| 7 | — | cron、ledger |

> 錄課時所有畫面的金額、口數、參數都用教學值或打碼，不出現實盤設定。

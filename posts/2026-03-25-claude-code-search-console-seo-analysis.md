---
title: "Claude Code 接 Google Search Console — 用 AI 幫你做 SEO 分析"
date: 2026-03-25
author: HoMuChen
category: AI
tags: [AI, Claude Code, SEO, Google Search Console, MCP]
image: https://storage.googleapis.com/homuchen.com/images/claude-code-search-console-seo-analysis-0.jpg
description: "手把手教你用 Claude Code 接上 Google Search Console，讓 AI 幫你分析搜尋數據、找出排名機會、追蹤關鍵字趨勢。從安裝 MCP Server 到實際下指令，完整教學一次搞定。"
---

前幾天我在看自己部落格的 Google Search Console 數據，想找找看有沒有什麼排名機會可以優化。

打開 Search Console 後台，篩選條件選一選、日期範圍調一調、匯出 CSV、打開試算表排序⋯⋯光是「找出曝光高但點擊低的關鍵字」這件事，就花了我快半小時。

然後我突然想到 — 欸，我不是每天都在用 Claude Code 嗎？它能不能直接幫我查？

答案是：**可以，而且超方便。**

只要裝一個 MCP Server，Claude Code 就能直接連上你的 Google Search Console，用對話的方式查詢搜尋數據。不用再開後台、不用匯出 CSV、不用自己排序篩選。你只要跟 Claude 說「幫我找排名機會」，它就幫你找好了。

今天來分享怎麼設定，以及實際能做哪些事：

* MCP Server 是什麼（30 秒解釋）
* 安裝與設定步驟
* 10 個實用的 SEO 分析指令
* 我自己的實際使用範例

## MCP Server 是什麼？

**MCP（Model Context Protocol）就是讓 AI 連接外部工具的標準協定。**

打個比方，Claude Code 本身很聰明，但它只能讀你電腦上的檔案。如果你想讓它查 Google Search Console 的數據、操作 Notion、或是讀 GitHub Issues，它需要一個「翻譯員」來幫忙串接。這個翻譯員就是 MCP Server。

每個 MCP Server 負責一個服務。今天我們要裝的就是 **Google Search Console 的 MCP Server**，裝完之後 Claude Code 就多了一組 SEO 分析工具。

如果你對 AI Agent 的運作原理有興趣，可以看我之前寫的 [**AI Agent 到底是什麼？跟 ChatBot 差在哪？**](/posts/what-is-ai-agent-vs-chatbot/)，MCP Server 就是讓 Agent 能夠「使用工具」的那個機制。

## 安裝與設定（5 分鐘搞定）

整個設定分三步：安裝套件、Google OAuth 認證、設定 Claude Code。

### Step 1：安裝 MCP Server

打開終端機，執行：

```bash
npm install -g google-searchconsole-mcp
```

這會全域安裝 Google Search Console 的 MCP Server。

### Step 2：Google OAuth 認證

```bash
gsc-mcp-auth
```

執行後會自動打開瀏覽器，讓你登入 Google 帳號並授權。選擇你有 Search Console 權限的那個 Google 帳號就好。

認證成功後，token 會存在 `~/.gsc-mcp/tokens/` 目錄下，之後不需要重新認證。

### Step 3：設定 Claude Code

把 MCP Server 加到 Claude Code 的設定檔 `~/.claude.json`。找到 `mcpServers` 這個區塊，加入以下設定：

```json
{
  "mcpServers": {
    "google-search-console": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "google-searchconsole-mcp"],
      "env": {}
    }
  }
}
```

> **注意**：如果你的 `mcpServers` 裡已經有其他 server（像是 context7），記得用逗號分隔，不要覆蓋掉原本的設定。

設定完成後，重啟 Claude Code，輸入 `/mcp` 確認 `google-search-console` 顯示 `✔ connected` 就成功了！

大功告成～～🎉🎉🎉

## Claude Code 能幫你做的 10 件 SEO 分析

連上 Search Console 之後，你可以直接用自然語言跟 Claude Code 對話來分析 SEO 數據。以下是 10 個我最常用的指令：

### 1. 查看整體表現

> 「幫我查 homuchen.com 最近 28 天的搜尋表現」

Claude 會回傳總點擊數、總曝光數、平均 CTR 和平均排名。這是最基本的健康檢查。

### 2. 找出排名機會

> 「找出曝光高但 CTR 低的關鍵字」

這是 SEO 優化的金礦 — 這些關鍵字代表 Google 已經在展示你的頁面，但使用者看到後沒有點進來。通常優化標題和描述就能顯著提升點擊率。

### 3. 查看熱門頁面

> 「列出流量最高的前 20 個頁面」

快速了解哪些文章帶來最多流量，幫你決定要優先優化哪些內容。

### 4. 追蹤特定關鍵字趨勢

> 「追蹤 'hash function' 這個關鍵字最近 3 個月的排名變化」

看某個關鍵字的排名是在上升還是下降，判斷你的優化策略有沒有效果。

### 5. 品牌 vs 非品牌分析

> 「分析品牌搜尋和非品牌搜尋的比例」

了解有多少流量來自搜尋你的品牌名稱（品牌搜尋），多少來自通用關鍵字。品牌搜尋比例太高，代表你的內容 SEO 還有很大的成長空間。

### 6. 比較不同時段

> 「比較這個月和上個月的搜尋表現」

追蹤成長趨勢，看看哪些指標在進步、哪些在退步。

### 7. 檢查 URL 索引狀態

> 「檢查 /posts/google-sheet-stock-income-statement/ 的索引狀態」

某篇文章沒有出現在搜尋結果？用這個指令檢查 Google 有沒有正確索引它。

### 8. 依裝置分析

> 「分別看桌機和手機的搜尋表現」

如果手機的 CTR 特別低，可能是你的文章標題在手機上被截斷了。

### 9. 查看 Sitemap 狀態

> 「列出目前的 Sitemap 和它的提交狀態」

確認你的 Sitemap 是否正常運作，有沒有錯誤。

### 10. 組合分析

> 「找出排名在 5-15 名、曝光超過 100 次的關鍵字，並列出對應的頁面」

這才是 Claude Code 真正厲害的地方 — 你可以用自然語言描述複雜的篩選條件，不需要自己寫公式或寫程式。排名 5-15 名的關鍵字最有機會推進到前 3 名，是投資報酬率最高的優化目標。

## 實際案例：我的部落格分析

讓我用自己的部落格來示範。以下是我用 Claude Code 查到的真實數據（2025/12/25 ~ 2026/03/25）。

### 流量最高的頁面

| 頁面 | 點擊 | 曝光 | CTR |
|------|------|------|-----|
| Google Sheet 股票損益計算 | 433 | 8,066 | 5.37% |
| Database Cache 策略 | 382 | 5,328 | 7.17% |
| Google Sheet 記帳教學 | 296 | 5,129 | 5.77% |
| Google Sheet 下拉選單 | 189 | 6,182 | 3.06% |
| HTTP Headers | 167 | 7,189 | 2.32% |

### 排名機會（高曝光、低 CTR）

| 關鍵字 | 曝光 | 點擊 | 排名 | 潛在提升 |
|--------|------|------|------|---------|
| hash | 4,594 | 3 | 8.7 | +227 |
| curl | 2,880 | 1 | 9.6 | +143 |
| replication | 2,088 | 15 | 5.4 | +89 |
| isp 是什麼 | 1,360 | 1 | 5.0 | +67 |
| pagination | 1,004 | 1 | 7.1 | +49 |

看到這些數據，我就知道接下來該做什麼了：

1. **「hash」有 4,594 次曝光但只有 3 次點擊** — 我的 Hash Function 文章標題和 meta description 需要優化，讓搜尋者更想點進來
2. **「isp 是什麼」排名 5.0 但只有 1 次點擊** — 排名已經不錯了，問題可能出在標題不夠吸引人
3. **「replication」是表現最好的** — 有 15 次點擊和 5.4 的排名，可以考慮加強這篇文章的內容深度

這些分析如果自己手動做，可能要花一兩個小時。用 Claude Code？**一句話，30 秒。**

## 實戰：用 Claude Code 直接改標題和描述

光是看數據還不夠，重點是**採取行動**。

我看到 hash 那篇文章有 4,594 次曝光但只有 3 次點擊，馬上請 Claude Code 幫我查這篇文章被哪些關鍵字搜到：

> 「查 what-is-hash-function 這個頁面被哪些關鍵字搜到」

結果發現，最多人搜的是「hash」和「hash functions」，但我的舊標題是「什麼是Hash Function? 有什麼特性及用途?」— 太學術了，搜「hash」的人看到這個標題不會想點。

所以我直接跟 Claude Code 說：

> 「幫我把這篇文章的標題改成『Hash 是什麼？一次搞懂 Hash Function 的原理、特性與應用』，description 改成 ...，然後更新到 Ghost」

Claude Code 就透過 Ghost Admin API，一次幫我更新了標題、meta title、meta description、custom excerpt。**整個過程不到 30 秒，不需要登入 Ghost 後台。**

我用同樣的方式一口氣改了三篇：

| 文章 | 舊標題 | 新標題 |
|------|--------|--------|
| Hash | 什麼是Hash Function? 有什麼特性及用途? | **Hash 是什麼？一次搞懂 Hash Function 的原理、特性與應用** |
| ISP | [Networking]什麼是網路？...ISP | **ISP 是什麼？網路服務供應商如何讓你連上網路** |
| Pagination | REST API Design: Pagination | **Pagination 是什麼？API 分頁設計完整指南** |

改標題的邏輯很簡單：

1. **把最多人搜的關鍵字放到標題最前面**（hash、ISP、Pagination）
2. **加上「是什麼？」的問句**，對應搜尋者的意圖
3. **用中文描述內容**，讓繁中搜尋者更想點進來

**改標題是 SEO 裡投資報酬率最高的動作** — 花 10 分鐘改三篇標題，就可能每月多出 100-200 次點擊。而用 Claude Code，連 10 分鐘都不用。

![用 Claude Code 更新 Ghost 文章標題](https://storage.googleapis.com/homuchen.com/images/claude-code-search-console-seo-analysis-1.jpg)

## 進階玩法：搭配內容策略

光是查數據只是第一步。真正厲害的是把 Search Console 數據結合你的寫作流程。

舉個例子，我現在寫文章前的流程是：

1. **用 Claude Code 查 Search Console**，看看哪些關鍵字有搜尋量但我還沒寫過
2. **找到內容缺口**，決定下一篇要寫什麼主題
3. **用 Claude Code 做關鍵字研究**，確認競爭程度和搜尋意圖
4. **寫完文章後再回來追蹤**，看排名有沒有慢慢爬上去

整個過程都在 Claude Code 裡完成，不需要在不同工具之間切來切去。

如果你也是部落客或內容創作者，這套流程真的會省下很多時間。就像我之前在 [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/) 裡說的，AI 最大的價值不是幫你回答問題，而是幫你把重複性的工作自動化。

## 常見問題

### Claude Code 是什麼？

Claude Code 是 Anthropic 推出的命令列 AI 工具。你可以在終端機裡用自然語言跟 Claude 對話，它能直接讀寫你電腦上的檔案、執行指令、串接外部服務。簡單來說，就是把 AI 助理搬到你的開發環境裡。

### MCP Server 需要付費嗎？

Google Search Console 的 MCP Server 是**免費開源**的。你只需要有 Claude Code 的使用權限（需要 Anthropic 帳號）和 Google Search Console 的存取權限。

### 資料安全嗎？

所有資料都在你的本機端處理。MCP Server 跑在你自己的電腦上，Search Console 的認證 token 也存在本機。資料不會經過第三方伺服器。

### 支援多個網站嗎？

支援。如果你的 Google 帳號有多個網站的 Search Console 權限，Claude Code 都能存取。用 `list_sites` 就能看到所有可用的網站。

### 除了 Search Console，還能接什麼？

MCP 的生態系非常豐富，截至 2026 年初已有超過 3,000 個公開可用的 MCP Server。常見的包括 GitHub、Notion、Slack、Google Drive 等。未來我會再寫文章介紹其他實用的 MCP Server。

## 結語

以前做 SEO 分析，要開 Search Console 後台、匯出 CSV、用試算表排序篩選。現在只要一句話，Claude Code 就幫你搞定。

對我來說，這不只是省時間而已。當分析數據的門檻降低了，你就會更頻繁地去看數據、更快地發現問題、更早地採取行動。**AI 的價值不在於取代你的判斷，而在於讓你能更快地做出判斷。**

如果你是部落客、內容創作者、或是任何需要做 SEO 的人，真的推薦試試這套流程。設定只要 5 分鐘，但省下的時間是持續累積的。

延伸閱讀：
* [**Claude Cowork — 當 AI 從「陪你聊天」變成「幫你做事」**](/posts/claude-cowork-ai-from-chat-to-work/)
* [**AI Agent 到底是什麼？跟 ChatBot 差在哪？**](/posts/what-is-ai-agent-vs-chatbot/)
* [**AI 時代，軟體工程師怎麼辦？一個工程師的真實觀察**](/posts/software-engineer-in-ai-era/)

希望這篇對大家有一丁點兒的幫助～掰掰～👋

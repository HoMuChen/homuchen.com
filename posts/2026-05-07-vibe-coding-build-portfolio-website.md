---
title: "Vibe Coding 做網頁完整實戰：給 AI 一個資料夾，5 步驟做出可部署的作品集網站"
date: 2026-05-07
author: HoMuChen
category: AI
tags: [Vibe Coding, Claude Code, AI, 教學, 作品集網站]
image: https://storage.googleapis.com/homuchen.com/images/vibe-coding-build-portfolio-website-0.jpg
description: "Vibe Coding 做網頁的完整工作流：把作品放進一個資料夾、跟 AI 對話描述風格、預覽迭代、用 Vercel 一行指令部署。Claude Code、Cursor、Codex、Antigravity 任一個都能跑這個流程，附 7 個可直接複製的 prompt。"
---

最近朋友跟我說他想做一個個人作品集網站，但「光是學 HTML/CSS 加上 React 就學了三個月，還是沒做出來」😂。我聽完覺得很可惜——他作品其實做得很好，是被「網站怎麼蓋」這件事卡住了。

我跟他說：「你不用學那麼多，現在用 Vibe Coding 30 分鐘就做得出來。」他半信半疑，我們當天晚上就一起做完了。

這篇文章就把那天的工作流寫下來。重點是這個方法**不限工具**——Claude Code、Cursor、Antigravity、Codex 都可以，重點在於「**怎麼跟 AI 對話**」這件事。

這篇會討論：

* Vibe Coding 是什麼？跟以前用 AI 寫 code 有什麼不同？
* 這方法適合誰？不適合誰？
* 5 步驟工作流：從資料夾到上線
* 7 個可以直接複製的 prompt
* AI 寫出來的常見踩雷與修法
* 進階：自訂網域、加 analytics
* 常見問題 FAQ

> 💡 **揭露**：這篇提到的工具（Claude Code、Cursor、Vercel、Plausible 等）都不是聯盟連結，沒有任何抽成。純分享。

---

## Vibe Coding 是什麼？跟以前用 AI 寫 code 有什麼不同？

**Vibe Coding** 這個詞是 OpenAI 共同創辦人 Andrej Karpathy 在 2025 年 2 月提出的，他形容這種寫法：「**你完全投入這個 vibe，擁抱指數性，甚至忘記 code 是存在的**」。

簡單講，跟以前用 AI 寫 code 最大的差別是：

| 維度 | 以前用 AI（2024） | Vibe Coding（2026） |
|------|-----------------|--------------------|
| 你做什麼 | 寫 prompt → 複製 code → 自己組 → debug | 講話 → 看結果 → 講話 → 看結果 |
| 需要會程式嗎 | 需要（要看得懂 AI 寫的東西） | 不需要 |
| AI 的身份 | 助理（給你建議） | Agent（直接動手） |
| 反覆改 | 你開 IDE 自己改 | 跟 AI 講「這邊改一下」 |
| 跑起來 | 你自己 setup | AI 開 server 給你看 |

我之前寫過[**Vibe Coding 怎麼擺脫 AI 味，做出高質感網站**](/posts/vibe-coding-avoid-ai-style-how-to-make-high-quality-website/)裡面有更完整介紹。一句話總結：

> 你**用講的**描述要做什麼、AI 寫 code、你預覽、有問題再用講的修，反覆迭代直到滿意。

不寫一行 HTML/CSS/JS 也可以做出能跑的網站。**你的工作從「寫」變成「描述」**。

---

## 這方法適合誰？不適合誰？

| ✅ 適合 | ❌ 不適合 |
|--------|---------|
| 有作品但卡在「網站怎麼蓋」 | 想學前端基本功的學生 |
| 設計師、攝影師、寫作者、研究者 | 要做大型 SaaS / 多人系統 |
| 想 30 分鐘上線一個 demo | 高度客製化的互動效果（像 awwwards 等級） |
| 學前端但不想被語法卡住 | 公司商業網站（要交給工程師） |
| 想試「用講的」做東西的人 | 預算為零、不想付任何工具費的 |

Vibe Coding 這個詞常被理解成「給不會 code 的人用的方式」，但我作為工程師反而**用得更頻繁**——個人網站、demo prototype、自動化腳本、內部小工具，過去兩年大大小小累積做了 30+ 個，公開分享過的有 [**Shopify 整合工具**](/posts/claude-code-shopify-admin-api-ecommerce-assistant/)、[**FinMind 股票追蹤**](/posts/claude-code-finmind-stock-tracking/)、[**對話式記帳**](/posts/claude-code-remote-control-conversational-bookkeeping/)。**會寫 code 不代表凡事都該手刻**——該交給 AI 的交出去，自己專心想架構跟產品就好。

---

## 工作流總覽

整個流程就 5 步：

1. **準備資料夾** — 把你想放上網站的東西丟進去（照片、描述）
2. **選工具** — Claude Code / Cursor / Codex / Antigravity 任選
3. **對話 + 貼參考** — 描述你想要的風格，貼幾張參考網站給 AI 看
4. **預覽 + 迭代** — 看生成結果、用講的修改
5. **`vercel` 一行部署** — 上線、拿到網址

整個下來最快 30 分鐘，慢一點也不會超過 2 小時。重點是**沒有任何一步需要你手寫 code**。

---

## Step 1：把資料夾準備好

這是整個流程裡最重要的一步——**你給 AI 什麼，AI 就用什麼做**。

### 推薦的資料夾結構

```
my-portfolio/
├── works/
│   ├── project-1/
│   │   ├── cover.jpg
│   │   ├── detail-1.jpg
│   │   ├── detail-2.jpg
│   │   └── description.md
│   ├── project-2/
│   │   ├── cover.jpg
│   │   └── description.md
│   └── project-3/
│       ├── cover.jpg
│       └── description.md
├── about.md          # 自我介紹
├── avatar.jpg        # 大頭照
└── contact.md        # 聯絡方式
```

`description.md` 裡面就用純文字寫：作品名稱、年份、用什麼做的、想說的話。例如：

```markdown
# 海邊的咖啡店設計

Year: 2024
Tools: Figma, Midjourney
Description: 為一間花蓮的小咖啡店做的品牌識別與菜單設計。
業主希望保留「海風」感但又不要太老氣，做了三輪提案才定稿。
```

不用糾結格式——AI 看得懂。**你的工作就是把「能塞的素材」全部塞進去就好**。

### 我自己的小撇步

- **每個作品至少 1 張封面圖** — 沒有圖 AI 會自動跳過或者隨便產一個 placeholder
- **檔名用英文 / 數字** — 中文檔名有時 AI 處理會出錯
- **描述用 Markdown 格式** — AI 解析得比較好，未來也能直接搬到別的地方用

---

## Step 2：選工具（任意一個都行）

### 主流選擇（CLI / IDE 派）

| 工具 | 適合場景 | 收費 |
|------|---------|------|
| **Claude Code** | 終端機友好、agent 模式最強 | 訂閱 Claude $20+/月，或 API |
| **Cursor** | 有 IDE 介面、適合視覺型使用者 | $20/月 |
| **Codex** | OpenAI 的 CLI、跟 ChatGPT 帳號連動 | 訂閱 ChatGPT |
| **Antigravity** | Google 的 IDE，2026 還在 beta 階段 | 免費 beta |

### 純瀏覽器派（不用裝任何東西）

| 工具 | 適合場景 | 收費 |
|------|---------|------|
| **Bolt.new** | 直接在瀏覽器對話做網頁，做完直接 deploy | 有免費額度 |
| **v0.dev** | Vercel 出的，做 React component / 網頁很順 | 有免費額度 |
| **Lovable** | 偏設計感，做出來的網站比較有 taste | 有免費額度 |

**我自己用 Claude Code**（這個 blog 也是這樣寫的），但這篇講的工作流跟工具無關，**重點都在「對話的方式」**。

如果完全沒裝過任何 CLI 工具想最快開始，**從 Bolt.new 或 v0 開始最快**——但這兩個的限制是：你的資料夾要先上傳到瀏覽器。如果作品集照片很多，反而 Claude Code / Cursor 直接讀本地資料夾比較方便。

延伸閱讀：[**Claude Cowork：把 AI 從聊天變成幫你做事**](/posts/claude-cowork-ai-from-chat-to-work/)。

---

## Step 3：對話 + 貼參考

這是 Vibe Coding 最有趣的一步。**你不用懂 HTML/CSS，你只要會描述「你想要的感覺」**。

### Prompt #1：開場 — 告訴 AI 你要做什麼

```
你看一下我這個資料夾的結構（cd 到資料夾後）。

我想要做一個個人作品集網站，把 works/ 底下的每個作品都展示出來。
about.md 是我自我介紹、avatar.jpg 是我大頭照、contact.md 是聯絡方式。

請先讀完所有資料，然後跟我確認你看到了哪些作品，
最後再給我一個建議的網站結構。不要直接開始寫 code。
```

**重點是「不要直接寫 code」這句**。AI 預設會直接動手，但這樣你就失去了討論的機會。**先讓 AI 讀完、跟你 align，再開始寫**——這也是擺脫 AI 味的核心。

### Prompt #2：描述風格

這時候 AI 會問你「想要什麼風格」，把參考拿出來：

```
風格參考：
- https://brittanychiang.com — 我喜歡這種暗色 + 一頁式 + sticky sidebar
- https://rauno.me — 字體跟極簡感參考這個
- 不要用 framework（沒有 React / Vue），純 HTML + CSS + 一點 JS 就好
- 配色：黑底 + 米白文字 + 一個亮色（你決定）
- 字體：等寬字 + sans-serif

技術要求：
- 響應式，手機要好看
- 圖片要 lazy load
- SEO meta tag 要完整
```

**訣竅**：給 AI 看**真實網站連結**比文字描述強 10 倍。如果方便也可以**截圖貼給 AI**，AI 會分析配色、字體、layout，自己抓出設計語言。

### Prompt #3：放手讓他寫

```
OK，照剛剛確認過的結構跟風格，請開始做。
做完後跑一個 local server 讓我預覽。
```

這時候 AI 會：

- 讀 `works/*/description.md` 自動填入內容
- 把 `works/*/cover.jpg` 自動接到 `<img>` tag
- 寫好 `index.html`、`style.css`、`script.js`
- 跑 `python -m http.server` 或 `npx serve` 開 preview

**通常第一版要 3–10 分鐘**，看你作品數量多少。

---

## Step 4：預覽 + 對話迭代

預覽打開的瞬間——99% 的機率你會皺眉頭😂。第一版**一定有 AI 味**：配色像 Bootstrap default、字體預設無印良品感、間距都太大或太小。(如果一開始就很讚，那恭喜你～)

但這就是 Vibe Coding 的精髓——**你不用回去改 code，你用講的就好**。

### Prompt #4：修風格

```
看了一下要修：
1. 整個太亮了，背景改 #0a0a0a
2. 標題字太大、body 太小，整體縮小 15%
3. 作品縮圖之間的間距太擠，加大 50%
4. hover 在作品上要有放大 + 陰影效果
5. sidebar 的 nav link 顏色太淡，加深一點
```

**具體 + 量化**的描述比「我覺得不對」有用 100 倍。如果你不知道怎麼描述，就**截圖標出來**——AI 看得懂。

### Prompt #5：細節打磨

```
- about 區塊加一個「Currently 正在做什麼」的小區
- 每個作品點進去要有 lightbox 預覽（不要跳新頁）
- footer 加上社群連結（GitHub、Twitter、Email）
- favicon 用 avatar.jpg 自動產一個
```

### Prompt #6：擺脫 AI 味（重要！）

**這是 9 成人忽略的步驟**。AI 第一版幾乎一定會有：

- 對齊太完美（看起來像模板）
- 配色太「協調」（沒有個人 taste）
- 文案太正向陽光（像產品官網）

```
這個版本太「AI 樣板感」了，調整一下：
- 標題不要對齊置中，改靠左
- 用一個微微 off-grid 的元素（例如 hero 標題往左偏 -3px）
- 文案改成口語、第一人稱，不要用「打造」「呈現」「致力於」這種詞
- 加一個小巧思（例如 cursor 跟蹤、滾動視差等）
```

擺脫 AI 味是讓網站有個性的關鍵。我之前寫過一整篇 [**Vibe Coding 怎麼擺脫 AI 味，做出高質感網站**](/posts/vibe-coding-avoid-ai-style-how-to-make-high-quality-website/)，可以搭配看。

---

## Step 5：`vercel` 一行部署

當網站長得你滿意後，部署超簡單：

### 第一次部署

```bash
# 裝 Vercel CLI（一次就好）
npm i -g vercel

# 在 portfolio 資料夾裡
vercel
```

跟著問題回答（基本上都按 Enter）：

- Set up and deploy? → **y**
- Which scope? → **你的帳號**
- Link to existing project? → **n**
- Project name? → **你想要的網址**
- In which directory is your code? → **./**

跑完會給你一個 `xxx.vercel.app` 的網址，**就上線了**。

### 之後每次更新

```bash
vercel --prod
```

整個工作流結束。從打開資料夾到網站上線，**最快 30 分鐘可以做完**。

### Vercel 之外的免費替代方案

如果你不想用 Vercel，下面這些都跑得起來純 HTML：

| 服務 | 適合場景 | 部署方式 |
|------|---------|---------|
| **GitHub Pages** | 已經在用 GitHub | push 到 `gh-pages` branch |
| **Cloudflare Pages** | 流量大、想要 CDN 快 | 連 GitHub repo 自動部署 |
| **Netlify** | 跟 Vercel 體驗最像 | drag-and-drop 或連 GitHub |

跟 AI 講「**幫我用 Cloudflare Pages 部署**」，他會自動幫你切換流程。

---

## 7 個可直接複製的 Prompt 速查表

| 階段 | Prompt 重點 |
|------|------------|
| 1. 開場 | `先讀完資料夾，跟我確認你看到什麼，不要直接寫 code` |
| 2. 描述風格 | `風格參考：[網址1][網址2]，配色 X、字體 Y、技術 Z` |
| 3. 開始寫 | `照剛剛確認的去做，做完跑 local server 我預覽` |
| 4. 修風格 | `具體列點：1. 太暗 → #xxx 2. 字太大 → 縮 15%` |
| 5. 細節 | `加 lightbox、加 social links、加 favicon` |
| 6. 擺脫 AI 味 | `太樣板感了，加 off-grid 元素、文案口語化` |
| 7. 部署 | `幫我用 Vercel 部署，先 vercel CLI 再 vercel --prod` |

---

## 常見踩雷

### 雷 1：圖片路徑出錯

AI 有時會用絕對路徑（`/Users/...`），結果線上版本看不到圖。

**修法**：

```
所有圖片改用相對路徑（works/project-1/cover.jpg），不要用絕對路徑。
```

### 雷 2：響應式做了但破版

AI 會自動加 media query，但通常會抓錯斷點。

**修法**：

```
手機（< 768px）下：
- sidebar 收起來變成漢堡選單
- 作品縮圖改 1 column
- 字體縮小 10%
```

### 雷 3：SEO meta 忘記寫

第一版 AI 經常漏 `<meta>` tag，導致分享到 LINE / FB 沒有預覽圖。

**修法**：

```
補完整 meta tags：title、description、og:image、og:title、og:description、twitter:card
og:image 用 avatar.jpg
```

### 雷 4：作品描述被 AI 改寫

AI 有時會「擅自精簡」你的描述。

**修法**：

```
作品描述請完整保留 description.md 的原文，不要改寫、不要精簡。
```

---

## 進階：自訂網域 + Analytics

### 自訂網域（5 分鐘搞定）

1. 在 Vercel dashboard 的 Project → Settings → Domains 加你的網域
2. Vercel 會給你一組 DNS 記錄
3. 到你買網域的地方（Namecheap / Gandi / GoDaddy）設 DNS
4. 等 5–30 分鐘 DNS 生效

跟 AI 講：

```
我要把網站綁到 myname.com，幫我列出 Vercel 跟我的 DNS provider 各要設什麼。
```

### Analytics（看誰來看你的網站）

```
幫我加 Plausible Analytics（不要用 Google Analytics，太重）。
我的 domain 是 myname.com。
```

或免費版本：

```
加 Vercel 內建的 Web Analytics（免費版，每月 2,500 events 額度）
```

---

## 常見問題 FAQ

### Q1：Vibe Coding 做網頁需要會程式嗎？

**不需要。** 你只要會描述「想要什麼樣子」就好。AI 會處理 HTML / CSS / JS、跑 server、修 bug。但**會看一點 code 會比較快**——比如知道圖片路徑錯了、知道 hover effect 是 CSS 在做。完全不會也行，多花一點對話迭代而已。

### Q2：用 Vibe Coding 做的網站質感會不會很差？

第一版**一定會有 AI 味**，這是事實。但這是「預設」不是「天花板」。透過具體描述風格、貼參考網站、用「擺脫 AI 味」的 prompt 改造，做出來的東西可以跟手刻網站 90% 接近。重點是你**願意迭代多少次**。

### Q3：Claude Code、Cursor、Codex 哪個最適合做網頁？

**做作品集這種小網站，4 個都能用。** 我自己用 Claude Code 因為它是 terminal-first，agent 模式可以放手讓他做完。如果你習慣 IDE 介面用 Cursor 比較舒服。Codex 適合本來就用 ChatGPT 的人。**重點不是工具，是對話的方式**。

### Q4：30 分鐘是真的還是行銷話術？

**「資料夾準備好」的前提下，30 分鐘是合理的。** 我朋友那次扣掉準備素材的時間是 28 分鐘上線。但如果你還要邊整理作品邊想風格，加上要「擺脫 AI 味」的迭代，**第一次上手通常 1.5–2 小時**比較貼近現實。第二個專案開始就會壓到 30 分鐘以內。

### Q5：要花多少錢？

純做一個作品集網站**最低成本可以是 0 元**（用 Bolt 免費額度 + GitHub Pages）。最常見的組合是 Claude $20/月 + Vercel 免費版 = **每月 $20**，做完一個專案後可以暫停訂閱。網域如果要自訂大概一年 $10–15 USD。

### Q6：可以用 Vibe Coding 做更複雜的網站嗎？

**可以，但有上限。** 一頁式作品集、落地頁、簡單部落格、文件站、表單工具都很適合。**多人系統 / 後台 / 複雜資料庫**就不建議了——AI 寫得出來但你看不懂的話沒辦法 maintain。我寫過[**用 Claude Code 做 Shopify 整合工具**](/posts/claude-code-shopify-admin-api-ecommerce-assistant/)是中等複雜度的真實案例。

### Q7：跟 Wix、Squarespace、Gamma 這種「AI 做網站」工具差在哪？

| 維度 | Vibe Coding | Wix / Squarespace / Gamma |
|------|------------|--------------------------|
| 自由度 | 想做什麼都可以 | 只能用模板裡有的東西 |
| 學習曲線 | 要會描述（但不用會 code） | 拖拉介面，最低 |
| 移植性 | 純 HTML/CSS，到處能搬 | 鎖在平台上 |
| 客製化 | 可以做出獨特風格 | 跟別人的網站長很像 |
| 月費 | $0–20 | $14–50 |

如果你想要「**獨特、不被綁架、可帶走**」，就選 Vibe Coding；想要「**最快、最省心**」就用 Wix 系列。

---

## 結語

Vibe Coding 做網頁的核心其實不在「寫」這件事——是在**怎麼描述**。

你的資料夾準備得好、風格描述清楚、迭代時具體量化，AI 幾乎一次就能給你 80 分的成品。剩下 20% 用對話補就好。

如果你身邊也有朋友卡在「想做網站但學不完前端」這個坎，把這篇丟給他——這條路省下來的學習時間，可以拿去做更多作品。

延伸閱讀：

* [**Vibe Coding 怎麼擺脫 AI 味，做出高質感網站**](/posts/vibe-coding-avoid-ai-style-how-to-make-high-quality-website/)
* [**Claude Cowork：把 AI 從聊天變成幫你做事**](/posts/claude-cowork-ai-from-chat-to-work/)
* [**Claude Code 用 FinMind 追台股**](/posts/claude-code-finmind-stock-tracking/)
* [**Claude Code 對話式記帳：在通勤路上把帳記完**](/posts/claude-code-remote-control-conversational-bookkeeping/)

---

**喜歡這篇文章嗎？**

📧 [訂閱 Newsletter](https://homuchen.com/#/portal/signup) — 新文章直接寄到你信箱
🎬 [追蹤我的 YouTube](https://www.youtube.com/@homuchen-build-ai) — 看 AI / 工具實作影片
💬 [加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 有問題隨時問我
🧵 [追蹤 Threads](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆

希望對你做網站有幫助～這條路省下來的學習時間，可以拿去做更多作品，掰掰～👋

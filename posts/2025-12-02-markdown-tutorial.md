---
title: "Markdown 語法完整教學：讓你的文字排版又快又美"
date: 2025-12-02
author: HoMuChen
category: Web Development
tags: [Web Development, Web, Markdown]
image: "https://images.unsplash.com/photo-1583521214690-73421a1829a9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDF8fGZpbGVzfGVufDB8fHx8MTc2NDYyNTc1MXww&ixlib=rb-4.1.0&q=80&w=2000"
description: "Markdown 語法完整教學：從標題、粗體、列表、連結、圖片、引用、程式碼區塊、表格到任務清單，整理常用 Markdown 排版範例與速查表。"
---

如果你曾經在 GitHub 上看過漂亮的專案說明文件、在 Notion 裡快速排版筆記、或是用 Obsidian 建立個人知識庫，那你其實已經跟 Markdown 打過照面了。今天這篇文章，就是要帶你徹底搞懂這個簡單卻超強大的標記語言！

> 好的工具讓你專注在內容，而不是排版

## Markdown 是什麼？

Markdown 是一種**輕量級標記語言**，由 John Gruber 在 2004 年創造。它的設計哲學很簡單：用最少的符號，達到最直觀的排版效果。

你不需要像 Word 那樣點來點去選字體大小，也不用記一堆複雜的 HTML 標籤，只要在純文字中加入一些符號，就能產生標題、粗體、列表、連結等格式。

舉個例子，當你想要一個粗體字，在 Word 裡你要選取文字 → 點粗體按鈕，但在 Markdown 裡，你只需要：

    **這是粗體**

就這樣，簡單到不行。

## 哪些地方會用到 Markdown？

你可能會想：「學這個幹嘛？我平常用 Word 就好了啊。」

其實 Markdown 早就滲透到我們日常使用的各種工具裡了，以下是幾個最常見的應用場景：

### 1. GitHub / GitLab

幾乎所有的開源專案都會有一個 `README.md` 檔案，這就是用 Markdown 寫的。專案說明、安裝步驟、API 文件，全部都是 Markdown。如果你想要參與開源社群或是展示自己的作品，學會 Markdown 是基本功。

### 2. 筆記軟體

現在最紅的筆記軟體幾乎都支援 Markdown：

| 軟體     | Markdown 支援度         |
|----------|-------------------------|
| Notion   | 部分支援，可混用        |
| Obsidian | 完整支援，原生 Markdown |
| Logseq   | 完整支援                |
| HackMD   | 完整支援，還能協作      |
| Typora   | 完整支援，即時預覽      |

### 3. 部落格與靜態網站

Jekyll、Hugo、Hexo、Astro 這些靜態網站生成器，文章都是用 Markdown 寫的。包括你現在看到的這篇文章，也是 Markdown！

### 4. 技術文件

幾乎所有的技術文件、API 文件都是用 Markdown 撰寫，像是 GitBook、Docusaurus、VuePress 等文件工具，都是以 Markdown 為核心。

### 5. 通訊軟體

Discord、Slack、Telegram 都支援 Markdown 語法，你可以在聊天時快速標記重點、貼程式碼，看起來專業又清楚。

## 基本語法教學

好，接下來就是重頭戲了！我會把最常用的語法整理出來，每個都附上範例，讓你馬上就能用～

### 標題

使用 `#` 符號來建立標題，越多個 `#` 層級越低：

```markdown
# 這是 H1 標題
## 這是 H2 標題
### 這是 H3 標題
#### 這是 H4 標題
```

**小技巧**：一篇文章通常只會有一個 H1，其他內容用 H2、H3 來組織結構，這樣對 SEO 也比較好。

### 文字樣式

```markdown
**粗體文字**
*斜體文字*
***粗斜體***
~~刪除線~~
`行內程式碼`
```

效果：

- **粗體文字**
- *斜體文字*
- ***粗斜體***
- ~~刪除線~~
- `行內程式碼`

### 列表

**無序列表**（用 `-`、`*` 或 `+` 都可以）：

```markdown
- 項目一
- 項目二
  - 子項目
  - 子項目
- 項目三
```

**有序列表**：

```markdown
1. 第一步
2. 第二步
3. 第三步
```

**小技巧**：有序列表的數字其實不用照順序寫，Markdown 會自動幫你排好，所以你全部寫 `1.` 也可以：

```markdown
1. 第一步
1. 第二步
1. 第三步
```

### 連結與圖片

**連結**：

```markdown
[顯示文字](https://example.com)
[Google](https://www.google.com)
```

**圖片**：

```markdown
![替代文字](圖片網址)
![可愛的貓咪](https://example.com/cat.jpg)
```

記住：圖片就是連結前面多一個 `!`。

### 引用

使用 `>` 來建立引用區塊：

```markdown
> 這是一段引用
> 可以寫很多行
>
> 空一行繼續引用
```

效果：

> 這是一段引用
> 可以寫很多行
>
> 空一行繼續引用

### 程式碼區塊

行內程式碼用單個反引號包起來：

```markdown
使用 `console.log()` 來輸出訊息
```

多行程式碼區塊用三個反引號，還可以指定語言來啟用語法高亮：

````markdown
```javascript
function sayHello(name) {
  console.log(`Hello, ${name}!`);
}
```
````

### 分隔線

用三個以上的 `-`、`*` 或 `_` 來建立分隔線：

```markdown
---
***
___
```

### 表格

表格的語法稍微複雜一點，但非常實用：

```markdown
|欄位一    |欄位二    |欄位三    |
|---------|---------|---------|
|內容 A    |內容 B    |內容 C    |
|內容 D    |內容 E    |內容 F    |
```

效果：

| 欄位一 | 欄位二 | 欄位三 |
|--------|--------|--------|
| 內容 A | 內容 B | 內容 C |
| 內容 D | 內容 E | 內容 F |

**對齊方式**：

```markdown
|靠左      |置中      |靠右      |
|:--------|:-------:|---------:|
|左對齊    |中間對齊   |右對齊    |
```

冒號 `:` 的位置決定對齊方式，左邊是靠左，兩邊都有是置中，右邊是靠右。

## 進階語法

學會基本語法後，這裡再補充幾個進階用法，讓你的文件更上一層樓！

### 任務清單

```markdown
- [x] 已完成的任務
- [ ] 未完成的任務
- [ ] 另一個待辦事項
```

效果：

- [x] 已完成的任務
- [ ] 未完成的任務
- [ ] 另一個待辦事項

GitHub 跟 Notion 都支援這個語法，超適合拿來做 Todo List！

### 註腳

```markdown
這是一段文字，需要附上參考資料[^1]。

[^1]: 這是註腳的內容，會顯示在頁面底部。
```

### 折疊區塊（HTML）

如果你想要可以展開/收合的內容，可以用 HTML 的 `<details>` 標籤：

```markdown
<details>
<summary>點我展開</summary>

這裡是隱藏的內容，可以放很多東西。

- 列表也可以
- 沒問題的

</details>
```

## 語法速查表

最後整理一張速查表，方便你隨時查閱：

| 功能       | 語法                        |
|------------|-----------------------------|
| 標題       | `# H1` `## H2` `### H3`     |
| 粗體       | `**文字**`                  |
| 斜體       | `*文字*`                    |
| 刪除線     | `~~文字~~`                  |
| 行內程式碼 | `` `code` ``                |
| 連結       | `[文字](URL)`               |
| 圖片       | `![alt](URL)`               |
| 引用       | `> 內容`                    |
| 無序列表   | `- 項目`                    |
| 有序列表   | `1. 項目`                   |
| 分隔線     | `---`                       |
| 任務清單   | `- [x] 完成` `- [ ] 未完成` |

## Summary

Markdown 的魅力就在於它的**簡單**和**通用性**。

一旦學會了 Markdown，你就能在 GitHub、Notion、部落格、技術文件、甚至聊天軟體裡，用同一套語法快速產出漂亮的內容。不用再煩惱排版問題，專注在你真正想表達的內容上。

開始在你的下一份筆記或文件裡試試看 Markdown 吧，保證你會愛上它的！🚀

---

## 延伸閱讀

- [CommonMark 官方規範](https://commonmark.org/?ref=homuchen.com)
- [GitHub Flavored Markdown 規範](https://github.github.com/gfm/?ref=homuchen.com)
- [Markdown Guide](https://www.markdownguide.org/?ref=homuchen.com)

# HoMuChen — Slide 風格設計指南

> 基於 Anthropic Claude 品牌配色延伸，**深色為預設模式**，適用於簡約風格簡報製作

---

## 1. 色彩系統 Color Palette

### 主色 Primary Colors（深色模式預設）

| 角色 | 色碼 | 用途 |
|------|------|------|
| **Dark** | `#141413` | 主背景色 |
| **Warm White** | `#FAF9F5` | 主標題文字 |
| **Dark Card** | `#1E1E1D` | 卡片底色、區塊背景 |
| **Dark Divider** | `#2A2A28` | 分隔線、邊框、subtle 區隔 |
| **Mid Gray** | `#B0AEA5` | 次要文字、說明文字、icon 輔助色 |

### 強調色 Accent Colors

| 角色 | 色碼 | 用途 |
|------|------|------|
| **Terracotta Orange** | `#D97757` | 主強調色 — CTA、highlight、重點數字、accent border |
| **Muted Blue** | `#6A9BCC` | 輔助強調 — 圖表、連結、次要重點 |
| **Sage Green** | `#788C5D` | 第三強調 — 正面語意、成長、完成狀態 |

### 延伸色 Extended

| 角色 | 色碼 | 用途 |
|------|------|------|
| **Warm Gold** | `#E8B87A` | 發光效果、glow、premium 感 |
| **Forest Green** | `#3D5A3A` | 深色區塊變體、深色版 icon |
| **Soft Peach** | `#F2DDD0` | 僅亮色模式變體使用（見 §7） |

### 色彩使用比例

```
60% — Dark (#141413) 背景
25% — Warm White (#FAF9F5) + Mid Gray (#B0AEA5) 文字層
10% — Dark Card (#1E1E1D) + Dark Divider (#2A2A28) 區塊與分隔
 5% — Accent 強調色（一張 slide 最多使用 1-2 種）
```

---

## 2. 字體系統 Typography

### 推薦字體配對

| 層級 | 英文字體 | 中文字體 | 備選 |
|------|---------|---------|------|
| **標題 H1** | **Poppins SemiBold** | **Noto Sans TC Bold** | Arial Black / 思源黑體 Bold |
| **副標 H2** | **Poppins Medium** | **Noto Sans TC Medium** | Arial / 思源黑體 Medium |
| **內文** | **Lora Regular** | **Noto Sans TC Regular** | Georgia / 思源黑體 Regular |
| **說明文字** | **Lora Italic** | **Noto Sans TC Light** | Georgia Italic |

### 字級規範

| 元素 | 字級 | 字重 | 顏色 | 行高 |
|------|------|------|------|------|
| 主標題 | 40–48pt | SemiBold (600) | `#FAF9F5` | 1.2 |
| 副標題 | 24–28pt | Medium (500) | `#FAF9F5` | 1.3 |
| 短描述 | 16–18pt | Regular (400) | `#B0AEA5` | 1.5 |
| 數字 Callout | 56–72pt | Bold (700) | `#D97757` | 1.0 |
| 標籤/Caption | 10–12pt | Regular (400) | `#B0AEA5` | 1.4 |

### 排版原則

- 標題**置左對齊**，不要置中（保持專業簡潔感）
- 描述文字保持 **2 行以內**
- 中英混排時，英文使用 Poppins，中文使用 Noto Sans TC，確保視覺高度一致
- 避免全部大寫（ALL CAPS），保持親切感

---

## 3. 間距系統 Spacing

### 基本單位

以 **8px grid** 為基礎系統：

| Token | 數值 | 用途 |
|-------|------|------|
| `xs` | 8px | icon 與文字間距 |
| `sm` | 16px | 同區塊內元素間距 |
| `md` | 24px | 段落之間 |
| `lg` | 40px | 區塊之間 |
| `xl` | 64px | 主要區域分隔 |

### Slide 邊距

```
┌─────────────────────────────────┐
│         margin: 64px            │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │      Content Area         │  │
│  │                           │  │
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

- **四邊留白**: 最少 64px（約 0.67 inch）
- **標題與內容間距**: 40px
- **元素之間最小間距**: 24px
- **大量留白** — 寧可空也不要擠

### 畫布規格與 Letterbox 處理

簡報主要用於 YouTube 補充畫面、教學影片、投影機投影，畫布規格固定為 16:9：

- **長寬比**: 16:9（所有 slide 統一，不混用其他比例）
- **製作解析度**: 1920×1080 px（YouTube / 投影機通用基準）
- **縮放方式**: `transform: scale()` 等比縮放至視窗大小，**永不裁切、永不變形**

#### 當瀏覽器視窗不是 16:9（letterbox 處理）

slide 縮放後會在左右或上下留 letterbox 空間。為了讓畫面看起來連續、不突兀：

- **`<body>` 背景色 = 當前 active slide 的背景色**，讓 letterbox 跟 slide 融為一體
- 預設深色（`#141413`）；若該張 slide 是亮色變體，body 同步切到 `#FAF9F5`
- 加 200ms `background-color` 過渡，讓切換滑順

實作參考：

```css
body {
  background: #141413;        /* 預設 = 深色 slide 背景 */
  transition: background-color 200ms ease;
}
body.light-active { background: #FAF9F5; }  /* 切到亮色變體時 */
```

```js
function show(i) {
  // ... toggle active slide
  const isLight = slides[i].classList.contains('light');
  document.body.classList.toggle('light-active', isLight);
}
```

> ⚠️ **不要為了「填滿視窗」就拉伸或裁切 slide**——會破壞 16:9 比例，影響後製剪輯。letterbox 是正確處理方式，只是用色彩讓它「隱形」。

---

## 4. 視覺元素 Visual Elements

### Icon 風格

- **線條式 (Line icons)**，線寬 2px
- 圓角風格，corner radius ≥ 4px
- 單色使用，顏色從 Accent 色或 Mid Gray 中選一
- 推薦 icon set: **Lucide**、Phosphor、Tabler Icons
- 尺寸: 24×24px（內文旁）或 48×48px（獨立展示）

### 幾何裝飾

- **圓形**: 用於 icon 背景 — 填充 `#1E1E1D`（Dark Card）或 `#2A2A28`（Dark Divider）
- **圓角矩形**: corner radius 12–16px，用於卡片與區塊（背景 `#1E1E1D`）
- **細線**: 1px `#2A2A28`，用於分隔，不要用粗線
- **小圓點**: 8px 直徑，`#D97757`，用於列表裝飾或路徑節點
- **電路紋路**: 可作為底部裝飾帶，使用 `#D97757` 低透明度

### 裝飾原則

```
✓ 右下角放一組小幾何圖形（圓 + 線段）
✓ 頁面底部 5% 區域用淡色裝飾帶
✓ Icon 放在填色圓形內
✗ 不要放超過 3 個裝飾元素
✗ 不要使用漸層（保持 flat）
✗ 不要使用陰影（保持平面風格）
```

---

## 5. 佈局模板 Layout Templates

### Template A — 標題頁

```
┌─────────────────────────────────┐
│  背景: #141413                  │
│                                 │
│     [品牌 Logo / Icon]          │
│                                 │
│     大標題                       │
│     Poppins 48pt #FAF9F5        │
│                                 │
│     副標題描述                    │
│     16pt #B0AEA5                │
│                                 │
│                          ● ○ ○  │  ← 裝飾圓點 (Coral / Card / Divider)
└─────────────────────────────────┘
```

### Template B — 單一重點

```
┌─────────────────────────────────┐
│                                 │
│  標題 28pt                      │
│  ─────────── (accent line)      │
│                                 │
│      ┌──────────────────┐       │
│      │   72pt 數字/關鍵字  │       │
│      │   #D97757         │       │
│      │                   │       │
│      │   16pt 說明        │       │
│      └──────────────────┘       │
│                                 │
└─────────────────────────────────┘
```

### Template C — 左文右圖

```
┌─────────────────────────────────┐
│                                 │
│  標題 28pt          ┌────────┐  │
│                     │        │  │
│  描述文字 16pt       │  圖示   │  │
│  最多 2-3 行         │  Icon  │  │
│                     │  區域   │  │
│  ● 重點 1            │        │  │
│  ● 重點 2            └────────┘  │
│                                 │
└─────────────────────────────────┘
```

### Template D — 三欄並列

```
┌─────────────────────────────────┐
│  標題 28pt                      │
│                                 │
│  ┌────────┐ ┌────────┐ ┌─────┐ │
│  │ ◉ Icon │ │ ◉ Icon │ │ ◉   │ │
│  │        │ │        │ │     │ │
│  │ 小標題  │ │ 小標題  │ │小標題│ │
│  │ 說明    │ │ 說明    │ │說明  │ │
│  └────────┘ └────────┘ └─────┘ │
│                                 │
└─────────────────────────────────┘

欄間距: 24px
卡片底色: #1E1E1D
Icon 背景圓: 48px, fill #2A2A28
```

---

## 6. Do's & Don'ts

### ✓ Do

- 每張 slide 只傳達 **一個核心訊息**
- 善用留白，讓內容呼吸
- 數字和關鍵字用 **Accent Orange `#D97757`** 突出
- Icon 保持同一套風格（全部 line style 或全部 filled）
- 整份簡報統一深色，**避免亮深混用**（除非刻意做章節對比）

### ✗ Don't

- 不要超過 3 種顏色同時出現在一張 slide
- 不要使用漸層、陰影、3D 效果
- 不要放超過 30 個字在一張 slide 上
- 不要混用不同 icon 風格
- 不要在標題下方加裝飾底線（AI 生成感很重）
- 不要使用預設 PowerPoint 模板配色
- 不要把純白 `#FFFFFF` 當文字色（用 Warm White `#FAF9F5`，深色背景上才不刺眼）

---

## 7. 亮色模式變體 Light Mode（次要）

預設為深色，但若特定場合（白色簡報投影機、列印給長輩看、特定平台需求）需要亮色版，依下表對照替換：

| 元素 | 深色（預設） | 亮色變體 |
|------|------------|---------|
| 背景 | `#141413` | `#FAF9F5`（Warm White）|
| 標題文字 | `#FAF9F5` | `#141413`（Dark）|
| 描述文字 | `#B0AEA5` | `#5C5C58`（Slate）或維持 `#B0AEA5` |
| 卡片/區塊底色 | `#1E1E1D` | `#FAF9F5`（與背景同）+ 1px 邊框 |
| 分隔線 | `#2A2A28` | `#E8E6DC`（Light Gray）|
| 強調色 Coral | `#D97757`（不變）| `#D97757`（不變）|
| 裝飾用 Soft Peach | — | `#F2DDD0`（亮色限定）|

> 亮色變體加 class `.slide.light` 在 section 上即可切換；body 也跟著切（見 §3 letterbox 章節）。

---

## 8. 快速取用 Quick Reference

```
背景:           #141413  (Dark)
標題文字:        #FAF9F5  (Warm White)
次要文字:        #B0AEA5  (Mid Gray)
卡片底:         #1E1E1D  (Dark Card)
分隔線:         #2A2A28  (Dark Divider)
強調橘:         #D97757  (Coral)
強調藍:         #6A9BCC  (Muted Blue)
強調綠:         #788C5D  (Sage Green)

標題字體:  Poppins SemiBold / Noto Sans TC Bold
內文字體:  Lora / Noto Sans TC Regular
標題字級:  40-48pt
內文字級:  16-18pt

邊距:     64px (最小) / 96px (推薦)
元素間距:  24px
圓角:     12-16px (卡片) / 50% (icon 圓)
```

---

*Style Guide v2.0 — HoMuChen Brand for Slides (Dark-first)*
*Based on Anthropic Claude palette + illustration style analysis*

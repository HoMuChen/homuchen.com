#!/usr/bin/env python3
"""Create three service pages on Ghost from services.md content."""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Load .env BEFORE importing upload_to_ghost
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_to_ghost import generate_ghost_token, md_to_html, html_to_lexical

GHOST_URL = os.environ.get("GHOST_URL", "").rstrip("/")

# ── Three service pages ──────────────────────────────────────────────────────

PAGES = [
    {
        "title": "AI 自動化工作流",
        "slug": "ai-automation-workflow",
        "custom_excerpt": "不是裝個 ChatGPT 就叫自動化。我幫你設計真正跑在生產環境的 AI Agent 工作流，從內容行銷、電商營運到資訊收集，把每天重複做的事交給 AI。",
        "meta_title": "AI 自動化工作流設計｜讓 AI Agent 幫你處理重複性工作",
        "meta_description": "不是裝個 ChatGPT 就叫自動化。我幫你設計真正跑在生產環境的 AI Agent 工作流，從內容行銷、電商營運到資訊收集，把每天重複做的事交給 AI。",
        "markdown": """
你有沒有算過，每天花多少時間在「其實不需要你親自做」的事情上？

整理資料、複製貼上、從 A 系統搬到 B 系統、寫那些格式差不多的東西、每天早上固定要查一輪的數據⋯⋯這些工作不難，但就是吃時間。而且最煩的是——它們每天都會回來找你。

我做的事情，就是幫你把這些重複性的流程，設計成 AI Agent 自動化工作流。不是那種「幫你生一段文字」的玩具，而是真正串接你的工具、跑在你的業務流程裡、每天自己跑的生產級系統。

## 這不是 demo，是真的在跑的東西

我自己就有三套 AI Agent 工作流跑在生產環境：

### 內容行銷自動化

從 SEO 關鍵字研究 → 系列文章規劃 → 用我的寫作風格產出文章 → 自動建立內部連結 → 發布到 Ghost CMS，整條內容產線自動化。原本寫一篇 SEO 友善的部落格文章要花半天到一天，現在整個流程大幅壓縮，而且 SEO 結構的一致性比人工更穩定。

### 電商營運自動化

商品上下架、圖片更新、部落格內容產出——這些電商日常營運裡最重複的動作，交給 Agent 處理。人只需要做決策，執行的事讓 AI 來。

### 量化交易資訊收集

自動收集基本面、技術面、籌碼面的資訊，做策略研究跟持倉追蹤。以前每天早上要花一兩小時才能看完的資訊量，現在 Agent 幫我整理好重點，我只要看結論就好。

## 適合你嗎？

如果你的工作裡有這些狀況，我們可以聊聊：

- **每天有固定要跑一輪的流程**——資料收集、報表整理、內容發布
- **常常在不同系統之間搬資料**——從 Excel 到 ERP、從 Email 到 CRM
- **有大量格式相近的產出**——客戶報告、週報、商品描述
- **需要定期監控和追蹤**——法規更新、競品動態、市場數據

重點不是「這件事 AI 能不能做」，而是「你願不願意把這件事從你的待辦清單上永遠刪掉」。

## 我怎麼幫你

1. **了解你的流程** — 先聊你目前的工作流程，找出最值得自動化的環節
2. **設計 Agent 架構** — 根據你的場景設計 AI Agent 的工具串接、知識來源、決策邏輯
3. **建置與部署** — 把 Agent 跑起來，串進你現有的系統和工具
4. **持續調校** — 上線後根據實際使用情況優化 Agent 的表現

技術棧主要是 Claude API / Agent SDK、Supabase、GCP Cloud Run，但這些是我的事，你不用管。你只需要告訴我：「這件事我不想再自己做了。」

## 聊聊吧

如果你對 AI 自動化有興趣，或只是好奇你的工作流程有沒有自動化的可能，歡迎找我聊～ 不一定要馬上做，先聊聊你的狀況，我可以幫你評估看看哪些環節最適合先動手。
""",
    },
    {
        "title": "AI 客製化系統建置",
        "slug": "ai-custom-system",
        "custom_excerpt": "十年軟體工程經驗，為企業打造客製化 AI 系統。從 LINE 智能客服到企業內部知識庫助理，資料不外洩、流程量身設計，不是套模板。",
        "meta_title": "AI 客製化系統建置｜企業級 AI 助理與智能客服平台",
        "meta_description": "十年軟體工程經驗，為企業打造客製化 AI 系統。從 LINE 智能客服到企業內部知識庫助理，資料不外洩、流程量身設計，不是套模板。",
        "markdown": """
市面上有很多「AI 客服」產品，大多是丟個 FAQ 進去、串個 ChatGPT，然後跟你說可以自動回覆了。

但你真正需要的，可能不只是一個會回答問題的聊天機器人。你需要的是一套真正理解你業務、能串接你的系統、能處理你客戶實際問題的 AI 系統。

這是我在做的事。

## 不只是聊天機器人

我目前正在開發的是一套多租戶 AI Agent 平台，第一個合作客戶是會計事務所。這不是一個通用的客服 bot——它能做到的事包括：

- **接上 Google Drive**，自動讀取事務所的文件、報價單、服務說明，客戶透過 LINE 問問題時，Agent 從你的真實資料裡找答案
- **查詢案件進度**，客戶問「我的營所稅申報到哪了？」，Agent 直接從文件系統裡找到狀態回覆，不用人工轉接
- **費用報價查詢**，Agent 讀取 Google Sheets 裡的報價資料，自動回覆對應的服務費用
- **多步驟任務處理**，一個問題需要查多個來源時，Agent 會自己拆解、分頭查詢、彙整回覆

而且最重要的——**每個客戶的資料完全隔離**。會計事務所 A 的資料，不會被事務所 B 的 Agent 看到。

## 我的背景讓我能做這件事

白天，我在企業端幫上市櫃公司建置地端 AI 系統，核心要求就是資料不外洩、隱私安全可控。所以我對企業在導入 AI 時最擔心的事——資安、準確性、穩定性——有很實際的理解。

晚上，我自己在造 AI Agent。十年的軟體工程經驗加上持續在 AI Agent 領域的深耕，讓我能從「企業真正的需求」出發來設計系統，而不是從「AI 能做什麼」出發硬套。

## 適合什麼樣的企業

- **專業服務業**（會計、法律、顧問）— 客戶常問重複問題、需要查文件回覆、報稅季人力吃緊
- **電商與零售**（Shopify、自有品牌）— 需要 AI 客服串接商品資料、訂單查詢、自動回覆
- **服務型企業**（診所、設計公司、教育機構）— 需要預約管理、服務諮詢、資料收集

共通的特徵是：你的客戶會透過 LINE 或網頁找你問問題，而這些問題裡有 60-70% 是重複的。

## 系統怎麼建

1. **場景訪談** — 了解你的業務流程、客戶常見問題、現有系統
2. **知識庫建置** — 把你的文件、FAQ、報價單等結構化，讓 AI 能精準擷取
3. **Agent 設計** — 設計對話邏輯、工具串接（Google Drive / Sheets / Calendar 等）、回覆的 guardrail
4. **渠道串接** — LINE Official Account、網頁 Widget，未來可擴展 Messenger 等
5. **上線與調校** — 初期陪跑，根據真實對話紀錄持續優化回覆品質

**資料安全**方面，可以選擇雲端部署（GCP Cloud Run + Supabase，資料加密隔離）或地端部署（完全不上雲），視你的需求而定。

## 不是套模板，是量身打造

每個企業的流程都不一樣。會計事務所需要的 Agent 跟電商需要的 Agent 完全不同。所以我不會拿一個通用模板貼上你的 logo 就交差——我會從你的業務場景出發，設計一套真正符合你需求的系統。

如果你正在想「我們公司有沒有可能用 AI 來⋯⋯」，不管那個想法多模糊都可以，歡迎找我聊聊。我們可以一起把那個模糊的想法，變成一套真的會跑的系統。
""",
    },
    {
        "title": "電商網站與品牌網站建置",
        "slug": "ecommerce-brand-website",
        "custom_excerpt": "用 Shopify 幫你打造專業電商網站，或建置品牌形象官網。從主題選擇、風格設計到上線，一條龍搞定。適合中小企業、設計公司、個人品牌。",
        "meta_title": "電商網站與品牌網站建置｜Shopify 開店 & 品牌官網設計",
        "meta_description": "用 Shopify 幫你打造專業電商網站，或建置品牌形象官網。從主題選擇、風格設計到上線，一條龍搞定。適合中小企業、設計公司、個人品牌。",
        "markdown": """
想做一個自己的網站，但不知道從哪裡開始？

你可能在 Instagram 或 LINE 上已經有客戶了，但總覺得少了一個「正式的家」。或者你已經在用蝦皮、Pinkoi 這些平台，但想要有自己的品牌官網，讓客戶覺得你更專業一點。

又或者，你是一間公司，需要一個乾淨好看的官網來展示你的服務跟作品，但不想花大錢找設計公司報價動輒十幾二十萬。

這些，我都可以幫你。

## 我能做什麼

### Shopify 電商網站

如果你有東西要賣，Shopify 是我最推薦的方案。不是因為它最便宜，而是因為它最穩定、生態系最完整、未來要擴展最方便。

我幫你處理的事包括：

- **主題選擇與客製化** — 根據你的品牌風格選對主題，不用從零刻起
- **商品上架結構** — 分類、標籤、SEO 設定，讓你的商品容易被找到
- **金流與物流串接** — 台灣常用的付款和寄送方式設定好
- **品牌視覺調整** — 配色、字體、整體氛圍符合你的品牌定位

不需要自己管主機、不用擔心網站掛掉、有問題 Shopify 官方客服也能幫忙——你專心賣東西就好。

### 品牌形象官網

如果你不需要電商功能，只是想要一個好看的官網來展示服務、作品集、或公司簡介，我也可以幫你做。

之前幫一間設計公司做的就是這種——不賣東西，就是展示設計案例、放影片、讓客戶了解服務流程。選了一個職人風格的 Shopify 主題（對，Shopify 不只能做電商），用柔和的配色和乾淨的排版，把作品集呈現得很有質感。

品牌官網的重點不在功能多複雜，而在於：打開網站的那一刻，客戶對你的第一印象是什麼。

## 為什麼找我做

跟一般網頁設計公司不同的是，我本身是軟體工程師。這意味著：

- **技術問題我自己能解** — 不用轉來轉去等工程師回覆
- **SEO 我一起幫你顧** — 不只做好看，還要讓 Google 找得到你
- **未來要加 AI 功能直接接** — 想在網站上加 AI 客服？直接串，不用再找人

而且，如果你未來想在網站上加入 AI 自動化（像是智能客服、自動商品推薦），我可以直接幫你銜接，不用再另外找人重做。

## 適合誰

- **個人品牌 / 自媒體** — 需要一個專業的個人網站，放作品集、部落格、聯絡方式
- **中小企業** — 需要公司官網但預算有限，不想花大錢
- **電商創業者** — 想從平台轉自有品牌官網，或是從零開始做電商
- **設計 / 創意產業** — 需要好看的作品展示網站

## 怎麼進行

1. **聊需求** — 你想做什麼樣的網站？有沒有喜歡的參考網站？目標客群是誰？
2. **選方案** — 根據你的需求選擇最適合的平台和主題
3. **設計與建置** — 我來處理所有技術面的事，你只需要提供內容和素材
4. **上線與教學** — 網站上線後教你怎麼自己更新內容，不用每次都找我

整個流程通常 2-4 週可以完成，視複雜度而定。

## 先聊聊你的想法

不管你現在是完全沒有網站、還是已經有但想改版，都歡迎找我聊聊。跟我說你的情況，我可以幫你建議最適合的做法，不一定要做最貴的方案～
""",
    },
]

# ── Main ─────────────────────────────────────────────────────────────────────

def create_page(page_config):
    html_content = md_to_html(page_config["markdown"])
    lexical = html_to_lexical(html_content)

    page_data = {
        "pages": [{
            "title": page_config["title"],
            "slug": page_config["slug"],
            "lexical": lexical,
            "custom_excerpt": page_config["custom_excerpt"],
            "meta_title": page_config["meta_title"],
            "meta_description": page_config["meta_description"],
            "custom_template": "custom-service",
            "tags": [{"name": "#service"}],
            "status": "draft",
        }]
    }

    token = generate_ghost_token()
    url = f"{GHOST_URL}/ghost/api/admin/pages/"
    data = json.dumps(page_data, ensure_ascii=False).encode("utf-8")

    req = Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Ghost {token}")
    req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urlopen(req) as resp:
            result = json.loads(resp.read())
            page = result["pages"][0]
            return page
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"  Error {e.code}: {error_body[:200]}")
        return None


def main():
    if not GHOST_URL:
        print("Error: GHOST_URL must be set in .env")
        return

    for page_config in PAGES:
        print(f"\nCreating: {page_config['title']}")
        page = create_page(page_config)
        if page:
            print(f"  Slug: {page['slug']}")
            print(f"  Template: {page.get('custom_template', 'default')}")
            print(f"  Edit: {GHOST_URL}/ghost/#/editor/page/{page['id']}")

if __name__ == "__main__":
    main()

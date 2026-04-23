#!/usr/bin/env python3
"""Create the Claude Cowork course sales page as a Ghost Page."""

import os
import sys
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Load .env before importing upload_to_ghost
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

# Now import from upload_to_ghost (it reads env at import time)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_to_ghost import generate_ghost_token, md_to_html, html_to_lexical

GHOST_URL = os.environ.get("GHOST_URL", "").rstrip("/")

# ── Page config ──────────────────────────────────────────────────────────────

TITLE = "不寫程式也能用 AI 自動化：Claude Cowork 實戰課"
SLUG = "ai-agent-course"
CUSTOM_EXCERPT = "用 Claude Cowork 打造你的 AI 數位同事，不寫程式也能自動化工作流程。適合中小企業老闆、自由工作者、電商賣家。"
CUSTOM_TEMPLATE = "custom-course"
TAGS = [{"name": "#course"}]

MARKDOWN_CONTENT = """
你有沒有算過，每天花多少時間在「不是你該做，但只有你能做」的事情上？

整理客戶丟來的一堆文件、寫第 87 封差不多的報價回覆、從 A 系統複製資料貼到 B 系統、每週手動整理一次報表⋯⋯這些事不難，但就是吃時間。而且最煩的是——**它們每天都會回來找你**。

你可能想過：「AI 不是很厲害嗎？能不能幫我做這些？」

答案是可以。但不是你以為的那種「問 ChatGPT 一個問題，它給你一段文字」的方式。

## 我說的是讓 AI 真的去「做」，不只是「說」

2026 年初，Anthropic 推出了一個叫 **Claude Cowork** 的工具。簡單講，它就是一個住在你電腦裡的 AI 同事。

你給它一個資料夾的權限，告訴它要做什麼，它就會自己規劃步驟、讀你的檔案、整理資料、產出文件——然後跟你說「做好了」。

不用寫程式、不用開終端機、不用懂什麼 API。你只要會打字、會描述你想要的結果就好。

**聽起來太好了？我自己實測給你看。**

我把會計事務所客戶丟來的 50 份 PDF 發票放進資料夾，跟 Cowork 說：「辨識每份發票的供應商、金額、日期，重新命名檔案，然後產出一份彙整的 Excel 表。」

10 分鐘後，50 份檔案全部按照「日期\\_供應商\\_金額」格式重新命名，Excel 表也做好了。原本要花一個下午的事情。

## 這門課會教你什麼

這門課不教你寫程式、不教你搞技術。我教你的是：**怎麼把你的工作邏輯教給 AI，讓它變成真的懂你業務的數位同事。**

### 第一章：搞懂 Cowork 是什麼（30 分鐘）

- Claude Cowork 跟 ChatGPT 差在哪？（一個只會回答，一個會做事）
- 安裝、設定、選資料夾——5 分鐘上手
- 你的第一個任務：讓 Cowork 整理你的下載資料夾

### 第二章：建立你的 AI 知識庫（1 小時）

- 把你的公司資料變成 AI 看得懂的格式
- 服務說明、報價邏輯、FAQ、SOP——哪些該放、怎麼放
- SKILL.md：教 AI 你的做事風格和品牌語調
- 實作：讓 Cowork 根據你的資料回答客戶問題

### 第三章：串接你的工具（1 小時）

- Connectors 是什麼？讓 AI 連上你的 Gmail、Google Drive、Notion
- 實作一：掃描信箱，自動產出今日待辦清單
- 實作二：讀取 Google Sheets 報價表，自動回覆客戶詢價
- 實作三：串接瀏覽器，做競品分析報告

### 第四章：讓 AI 自己跑——排程與自動化（45 分鐘）

- 排程功能：每天早上自動產出晨間簡報
- 每週自動跑的競品監控、法規追蹤、Email 整理
- 設定 Cowork 的 Global Instructions，讓它記住你的偏好

### 第五章：進階技巧（45 分鐘）

- Projects：把不同業務線的任務分開管理
- Plugins：安裝產業專用的擴充功能
- 成本控制：怎麼用最少的錢完成最多的事
- 常見問題排除：它做錯了怎麼辦？

### Bonus：產業實戰模板

- 會計事務所模板：文件分類 + 催收信 + 法規追蹤
- 電商賣家模板：商品描述 + 評價分析 + 社群貼文
- 自由工作者模板：報價回覆 + 內容產出 + 收據記帳
- 設計公司模板：需求整理 + 作品集描述 + 工時估算

## 這門課適合誰

- **中小企業老闆**——每天被行政雜事綁住，想把時間留給真正重要的事
- **自由工作者**——一個人當三個人用，需要 AI 幫你分擔日常營運
- **專業服務業者**（會計、法律、顧問）——客戶量大、文件多、重複工作多
- **電商賣家**——商品描述、客服回覆、社群經營全部自己來，快撐不住了

## 這門課不適合誰

- 想學寫程式的人（這門課零程式碼）
- 想學 n8n 或其他 no-code 自動化平台的人（我們只用 Claude Cowork）
- 還沒有具體業務需求的學生（這門課是解決實際工作問題的）

## 誰在教這門課

我是阿穆，台大電機畢業，軟體工程師十年。白天在輿情大數據公司幫聯詠等企業建置地端 AI 系統，晚上自己做 AI Agent 開發。

我有三個跑在生產環境的 AI Agent——部落格內容自動化、電商營運自動化、量化交易資訊收集。最近在幫會計事務所建置 LINE 智能客服系統。

我不是那種只會講概念的人。我是真的把這些東西做出來、每天在用的人。這門課裡的每個案例，都是我自己或我客戶真實遇到的場景。

## 常見問題

**Q：我需要先會用 Claude 嗎？**
不用。課程從零開始教。你只需要一台電腦和一個 Claude 帳號（Pro 方案 $20/月）。

**Q：跟 ChatGPT 的差別是什麼？**
ChatGPT 是你問它問題，它給你答案。Claude Cowork 是你告訴它要做什麼，它真的去做——讀你的檔案、產出文件、整理資料、寫信。是「做事」不是「聊天」。

**Q：我的資料安全嗎？**
Cowork 在你的電腦本地運作，你選擇讓它看哪個資料夾。不想給它看的，它碰不到。

**Q：跟 n8n 課程差在哪？**
n8n 是一個需要自己架設的自動化平台，學習曲線比較陡。Cowork 是打開 app 就能用，零設定。兩者可以互補，但如果你完全沒技術背景，Cowork 是更好的起點。

**Q：課程有時效性嗎？Cowork 更新了怎麼辦？**
Cowork 的核心用法（資料夾 + 知識庫 + Connectors + 排程）不太會變。功能更新我會在社群裡同步補充內容。

## 課程定價

**早鳥價 NTD 3,980**（原價 NTD 5,980）

包含：

- 完整課程影片（4-5 小時）
- 4 套產業實戰模板（SKILL.md + 資料夾結構 + 範例指令）
- 專屬 LINE 社群（問問題 + 更新通知）
- 未來新增內容免費取得
"""

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not GHOST_URL:
        print("Error: GHOST_URL must be set in .env")
        return

    # Markdown → HTML → Lexical (same pipeline as upload_to_ghost.py)
    html_content = md_to_html(MARKDOWN_CONTENT)
    lexical = html_to_lexical(html_content)

    # Build page payload
    page_data = {
        "pages": [{
            "title": TITLE,
            "slug": SLUG,
            "lexical": lexical,
            "custom_excerpt": CUSTOM_EXCERPT,
            "custom_template": CUSTOM_TEMPLATE,
            "tags": TAGS,
            "status": "draft",
        }]
    }

    # POST to Ghost Admin API (Pages endpoint)
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
            print(f"Page created successfully!")
            print(f"  Title: {page['title']}")
            print(f"  Slug: {page['slug']}")
            print(f"  Status: {page['status']}")
            print(f"  Template: {page.get('custom_template', 'default')}")
            print(f"  Edit URL: {GHOST_URL}/ghost/#/editor/page/{page['id']}")
            print(f"  Preview: {GHOST_URL}/{page['slug']}/")
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}")

if __name__ == "__main__":
    main()

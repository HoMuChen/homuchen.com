#!/usr/bin/env python3
"""Create the AI auto-trading course waitlist (coming soon) page as a Ghost Page."""

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

TITLE = "用 AI 打造自動化交易系統（即將推出）"
SLUG = "ai-auto-trading-course"
CUSTOM_EXCERPT = "用 Claude Code 把交易想法做成會自己下單、出錯會自己停下來的系統。課程籌備中，加 LINE 說「交易課」搶先收到開課通知。"
CUSTOM_TEMPLATE = None  # 用預設 page.hbs；custom-course 模板寫死了價格區塊
FEATURE_IMAGE = "https://storage.googleapis.com/homuchen.com/images/claude-code-shioaji-auto-trading-bot-0.jpg"
TAGS = [{"name": "#course"}]
LINE_URL = "https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539"

MARKDOWN_CONTENT = f"""
> 🚧 這門課還在籌備中，想搶先知道開課消息的話，[**加我的 LINE**]({LINE_URL}) 跟我說一聲「**交易課**」就好～

我自己用 Claude Code + 永豐 Shioaji API，做了一隻會自己下單的小型台積電期貨網格機器人，現在每天都在用真錢運行。

整個過程我幾乎沒有自己寫程式碼，但修過的 bug 一個比一個嚇人——回測多算了不存在的獲利、槓桿上限其實沒擋住、轉倉順序寫反……**它們沒有一個會報錯。**

所以這門課不是教你一個會賺錢的策略，而是教你：**讓 AI 幫你做研究、回測、寫下單程式，並且用安全機制把它關在籠子裡。**

## 預計會教什麼

1. **資料層**：用 FinMind 拿到乾淨的資料，避開默默被截斷的坑
2. **策略研究**：叫 Claude 幫你做實驗、寫研究筆記
3. **回測與防過擬合**：成本、轉倉、參數高原、群組驗證
4. **提醒模式**：先讓它喊，不讓它下
5. **下單模式**：永豐 Shioaji 串接、限價單、撤單、轉倉
6. **安全機制與對帳**：9 道保險，出錯就停機
7. **上線維運**：排程、log、異常通知、什麼時候該關掉它

## 適合誰

- 已經會用 Claude Code，看過 [**FinMind 股票追蹤**](/posts/claude-code-finmind-stock-tracking/) 或 [**台股 AI Agent**](/posts/claude-code-stock-agent-monitor-alert/) 這兩篇
- 已經有看盤通知，想再往「自動下單」走一步
- 有自己的交易想法，想用資料驗證，而不是憑感覺

## 先講清楚

這門課教的是**怎麼把工具做出來、做得安全**。不報明牌、不推薦個股、不保證賺錢😂 期貨有槓桿，可能損失超過保證金；回測結果也不代表未來。

## 等開課前，可以先看這些

- [**用 Claude Code + Shioaji 打造自動下單機器人：我的台積電期貨網格實戰**](/posts/claude-code-shioaji-auto-trading-bot/)
- [**網格交易回測：用台積電 6 年資料實測，99% 的月份有收入，卻輸給買進持有**](/posts/grid-trading-backtest-tsmc/)
- [**個股期貨是什麼？小型台積電期貨的保證金、轉倉、槓桿**](/posts/stock-futures-tsmc-mini-futures-guide/)
- [**期貨槓桿開幾倍才安全？同一個策略開 1、2、3 倍回測**](/posts/futures-leverage-backtest/)
- [**AI 寫程式的 7 個坑：我用 Claude Code 寫自動交易程式，真實修過的 bug**](/posts/ai-coding-trading-bot-bugs/)

💬 想上這門課，[**加我的 LINE**]({LINE_URL}) 跟我說一聲「**交易課**」，開課時第一個通知你～
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
            "feature_image": FEATURE_IMAGE,
            "tags": TAGS,
            "status": "published",
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

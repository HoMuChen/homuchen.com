#!/usr/bin/env python3
"""Create (or update) the /contact/ page on Ghost. Idempotent by slug."""

import os
import sys
import json
from datetime import datetime, timezone, timedelta

import jwt
import requests

# Load .env BEFORE importing upload_to_ghost
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'").strip('"')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_to_ghost import md_to_html, html_to_lexical

GHOST_URL = os.environ.get("GHOST_URL", "").rstrip("/")
GHOST_ADMIN_API_KEY = os.environ.get("GHOST_ADMIN_API_KEY", "")

PAGE = {
    "title": "聯絡我",
    "slug": "contact",
    "custom_excerpt": "有想自動化的工作流程，或想自架一隻 AI Agent 卻不知從哪開始？第一次諮詢免費，挑你順手的管道找我聊——LINE、Email 或 Threads 都可以。",
    "meta_title": "聯絡 HoMuChen｜預約免費 AI Agent 諮詢",
    "meta_description": "有想自動化的工作流程，或想自架一隻 AI Agent 卻不知從哪開始？第一次諮詢免費，挑你順手的管道找我聊——LINE、Email 或 Threads 都可以。",
    "markdown": """
有什麼想聊的，這裡都找得到我。

不管你是看完文章想問個問題、有個 AI Agent 的點子想討論，還是想直接預約諮詢——挑你順手的管道就好，我都會看到。

## 預約免費諮詢

如果你有想自動化的工作流程、或想自架一隻 AI Agent 但不知道從哪開始，歡迎找我聊。**第一次諮詢免費**，先了解你的狀況，我幫你看哪個環節最適合先動手——不一定要馬上做，先聊聊、評估一下都可以。

想先了解我提供的服務，可以看 [**AI 自動化工作流**](/ai-automation-workflow/)。

## 怎麼找我

- 💬 **LINE（最快）**：[加我的 LINE](https://line.me/R/ti/p/@673duklg?oat_content=url&ts=04121539) — 預約諮詢、問問題都歡迎
- 📧 **Email**：[homuchen.build.ai@gmail.com](mailto:homuchen.build.ai@gmail.com) — 合作、報價這類比較正式的事
- 🧵 **Threads**：[@homuchen.build.ai](https://www.threads.net/@homuchen.build.ai) — 平常的工程隨筆，也可以私訊我

不用客氣，先打聲招呼、跟我說你的狀況就好～

掰掰～👋
""",
}


def generate_jwt():
    kid, secret = GHOST_ADMIN_API_KEY.split(":")
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"iat": int(now.timestamp()),
         "exp": int((now + timedelta(minutes=5)).timestamp()),
         "aud": "/admin/"},
        bytes.fromhex(secret), algorithm="HS256",
        headers={"alg": "HS256", "typ": "JWT", "kid": kid},
    )


def main():
    if not GHOST_URL or not GHOST_ADMIN_API_KEY:
        print("Error: GHOST_URL / GHOST_ADMIN_API_KEY must be set in .env")
        sys.exit(1)

    H = {"Authorization": f"Ghost {generate_jwt()}", "Content-Type": "application/json"}
    lexical = html_to_lexical(md_to_html(PAGE["markdown"]))
    fields = {
        "title": PAGE["title"],
        "slug": PAGE["slug"],
        "lexical": lexical,
        "custom_excerpt": PAGE["custom_excerpt"],
        "meta_title": PAGE["meta_title"],
        "meta_description": PAGE["meta_description"],
        "status": "published",
    }

    # Idempotent: update if exists, else create
    r = requests.get(f"{GHOST_URL}/ghost/api/admin/pages/slug/{PAGE['slug']}/", headers=H, timeout=30)
    if r.status_code == 200:
        existing = r.json()["pages"][0]
        fields["updated_at"] = existing["updated_at"]
        r = requests.put(f"{GHOST_URL}/ghost/api/admin/pages/{existing['id']}/",
                         headers=H, data=json.dumps({"pages": [fields]}, ensure_ascii=False).encode("utf-8"), timeout=30)
        action = "更新"
    else:
        r = requests.post(f"{GHOST_URL}/ghost/api/admin/pages/",
                          headers=H, data=json.dumps({"pages": [fields]}, ensure_ascii=False).encode("utf-8"), timeout=30)
        action = "建立"

    if r.status_code not in (200, 201):
        print(f"FAIL {r.status_code}: {r.text[:400]}")
        sys.exit(1)
    page = r.json()["pages"][0]
    print(f"✅ 已{action}：{page['url']} (status={page['status']})")


if __name__ == "__main__":
    main()

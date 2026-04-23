#!/usr/bin/env python3
"""依 slug 更新既有 Ghost 文章的 HTML 內容（保留狀態、標題等其他欄位）"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import jwt
import requests
import markdown
import yaml


def load_env(env_path):
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip("'").strip('"')
    return env_vars


def generate_jwt(api_key):
    key_id, secret = api_key.split(":")
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"iat": int(now.timestamp()),
         "exp": int((now + timedelta(minutes=5)).timestamp()),
         "aud": "/admin/"},
        bytes.fromhex(secret),
        algorithm="HS256",
        headers={"alg": "HS256", "typ": "JWT", "kid": key_id},
    )


def parse_frontmatter(content):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not m:
        raise ValueError("no frontmatter")
    return yaml.safe_load(m.group(1)), m.group(2)


def md_to_html(body):
    body = re.sub(r'\{:target=["\']_blank["\']\}', "", body)
    return markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "toc", "attr_list", "codehilite", "nl2br"],
        extension_configs={"codehilite": {"css_class": "highlight", "guess_lang": False}},
    )


def slug_from_filename(path):
    name = re.sub(r"\.md$", "", os.path.basename(path))
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def update_post(ghost_url, token, slug, html):
    headers = {"Authorization": f"Ghost {token}"}

    # 找文章
    r = requests.get(
        f"{ghost_url}/ghost/api/admin/posts/slug/{slug}/",
        headers=headers, timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"找不到 slug={slug}：{r.status_code} {r.text[:200]}")
    post = r.json()["posts"][0]
    post_id = post["id"]
    updated_at = post["updated_at"]

    # PUT 更新
    r = requests.put(
        f"{ghost_url}/ghost/api/admin/posts/{post_id}/?source=html",
        headers={**headers, "Content-Type": "application/json"},
        json={"posts": [{"html": html, "updated_at": updated_at}]},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"更新失敗：{r.status_code} {r.text[:300]}")
    return r.json()["posts"][0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--env", default=".env")
    args = parser.parse_args()

    env = load_env(args.env)
    ghost_url = env["GHOST_URL"].rstrip("/")
    api_key = env["GHOST_ADMIN_API_KEY"]

    with open(args.file, encoding="utf-8") as f:
        _, body = parse_frontmatter(f.read())
    html = md_to_html(body)
    slug = slug_from_filename(args.file)

    print(f"🔄 更新 slug={slug}")
    token = generate_jwt(api_key)
    post = update_post(ghost_url, token, slug, html)
    print(f"   ✅ 已更新：{post['url']} (status={post['status']})")


if __name__ == "__main__":
    main()

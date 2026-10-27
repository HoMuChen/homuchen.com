#!/usr/bin/env python3
"""依 slug 更新既有 Ghost 文章的 HTML 內容（保留狀態、標題等其他欄位）

加 --meta 則只更新 title / custom_excerpt / meta_description，不動內文。
"""

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


def update_post(ghost_url, token, slug, fields, source_html=True):
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
    query = "?source=html" if source_html else ""
    r = requests.put(
        f"{ghost_url}/ghost/api/admin/posts/{post_id}/{query}",
        headers={**headers, "Content-Type": "application/json"},
        json={"posts": [{**fields, "updated_at": updated_at}]},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"更新失敗：{r.status_code} {r.text[:300]}")
    return r.json()["posts"][0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--env", default=".env")
    parser.add_argument("--meta", action="store_true",
                        help="只更新 title / custom_excerpt / meta_description（依 frontmatter），不動內文")
    args = parser.parse_args()

    env = load_env(args.env)
    ghost_url = env["GHOST_URL"].rstrip("/")
    api_key = env["GHOST_ADMIN_API_KEY"]

    with open(args.file, encoding="utf-8") as f:
        fm, body = parse_frontmatter(f.read())
    slug = slug_from_filename(args.file)

    if args.meta:
        fields = {"title": fm["title"]}
        if fm.get("description"):
            fields["custom_excerpt"] = fm["description"]
            fields["meta_description"] = fm["description"]
    else:
        fields = {"html": md_to_html(body)}

    print(f"🔄 更新 slug={slug}" + ("（meta）" if args.meta else ""))
    token = generate_jwt(api_key)
    post = update_post(ghost_url, token, slug, fields, source_html=not args.meta)
    print(f"   ✅ 已更新：{post['url']} (status={post['status']})")
    if args.meta:
        print(f"   title: {post['title']}")
        print(f"   meta_description: {post['meta_description']}")


if __name__ == "__main__":
    main()

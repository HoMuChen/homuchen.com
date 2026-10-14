#!/usr/bin/env python3
"""Validate / read / update a threads/*.md repurposed thread file.

  thread_file.py check <file>                 驗證格式與規則，有錯就印出並 exit 1
  thread_file.py posts-json <file> <out.json> 把各則貼文寫成 post_threads.py 吃的 JSON 陣列
  thread_file.py set-status <file> <status> [url]
  thread_file.py field <file> <key>           印出 frontmatter 欄位值
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAX_CHARS = 500
MIN_POSTS, MAX_POSTS = 3, 10
REQUIRED = ["date", "type", "source", "source_post", "tags", "status", "threads_url"]


def split(path: str) -> tuple[str, dict, list[str]]:
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("缺少 frontmatter")
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    posts = [p.strip() for p in re.split(r"\n---\n", body) if p.strip()]
    return fm_raw, fm, posts


def check(path: str) -> list[str]:
    errors = []
    try:
        _, fm, posts = split(path)
    except ValueError as e:
        return [str(e)]
    for k in REQUIRED:
        if k not in fm:
            errors.append(f"frontmatter 缺 {k}")
    if fm.get("type") != "thread":
        errors.append("type 必須是 thread")
    if fm.get("source") != "repurposed":
        errors.append("source 必須是 repurposed")
    if fm.get("status") not in ("draft", "approved"):
        errors.append(f"status 必須是 draft 或 approved（現在是 {fm.get('status')}）")

    sp = fm.get("source_post", "")
    m = re.fullmatch(r"/posts/([a-z0-9-]+)/", sp)
    if not m:
        errors.append(f"source_post 格式錯誤：{sp}")
    else:
        slug = m.group(1)
        if not glob.glob(os.path.join(ROOT, "posts", f"*-{slug}.md")):
            errors.append(f"source_post 對應的文章不存在：posts/*-{slug}.md")
        others = [
            f for f in glob.glob(os.path.join(ROOT, "threads", "*.md"))
            if os.path.abspath(f) != os.path.abspath(path)
            and re.search(rf"^source_post:\s*{re.escape(sp)}\s*$", open(f, encoding="utf-8").read(), re.M)
        ]
        if others:
            errors.append(f"這篇已經改寫過：{[os.path.relpath(o, ROOT) for o in others]}")
        if not os.path.basename(path).endswith(f"-{slug}.md"):
            errors.append("檔名必須是 {date}-{source_post slug}.md")

    if not MIN_POSTS <= len(posts) <= MAX_POSTS:
        errors.append(f"串文則數 {len(posts)}，要在 {MIN_POSTS}–{MAX_POSTS} 則")
    for i, p in enumerate(posts, 1):
        if len(p) > MAX_CHARS:
            errors.append(f"第 {i} 則 {len(p)} 字，超過 {MAX_CHARS}")
        if "掰掰" in p:
            errors.append(f"第 {i} 則有「掰掰」（Threads 不用）")
        has_link = bool(re.search(r"https?://", p))
        if i < len(posts) and has_link:
            errors.append(f"第 {i} 則有連結（只有最後一則可以放）")
    if posts and m:
        url = f"https://homuchen.com/posts/{m.group(1)}/"
        if url not in posts[-1]:
            errors.append(f"最後一則必須放原文連結 {url}")
    return errors


def set_status(path: str, status: str, url: str = "") -> None:
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^status:.*$", f"status: {status}", text, count=1, flags=re.M)
    if url:
        text = re.sub(r"^threads_url:.*$", f"threads_url: {url}", text, count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(text)


def main() -> int:
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "check":
        errors = check(path)
        for e in errors:
            print(f"✗ {e}")
        if not errors:
            print("✓ OK")
        return 1 if errors else 0
    if cmd == "posts-json":
        _, _, posts = split(path)
        json.dump(posts, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False)
        return 0
    if cmd == "set-status":
        set_status(path, sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
        return 0
    if cmd == "field":
        print(split(path)[1].get(sys.argv[3], ""))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())

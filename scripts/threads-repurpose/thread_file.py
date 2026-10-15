#!/usr/bin/env python3
"""Validate / read / update a threads/*.md repurposed post file.

  thread_file.py check <file>                 驗證格式與規則，有錯就印出並 exit 1
  thread_file.py posts-json <file> <out.json> 寫成 post_threads.py 吃的 JSON（{"posts": [...], "topic_tag": ...}）
  thread_file.py set-status <file> <status> [url]   改成 published 時順便記 published_at
  thread_file.py order                        approved 的檔案，依發布順序（最久沒發的文章優先）
  thread_file.py field <file> <key>           印出 frontmatter 欄位值

檔名：threads/{date}-{slug}-{nn}.md（一篇文章拆成多個 idea，同一批共用日期）
type: single → 1 則，或 1 則＋1 則回覆（補充或放連結）
type: thread → 3–6 則
"""

import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MAX_CHARS = 500
REQUIRED = ["date", "type", "source", "source_post", "tags", "status", "threads_url"]
BATCH_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9-]+)-(\d{2})\.md$")


def split(path: str) -> tuple[dict, list[str]]:
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("缺少 frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    posts = [p.strip() for p in re.split(r"\n---\n", m.group(2)) if p.strip()]
    return fm, posts


def batch_date(path: str) -> str | None:
    m = BATCH_NAME.match(os.path.basename(path))
    return m.group(1) if m else None


def check(path: str) -> list[str]:
    errors = []
    try:
        fm, posts = split(path)
    except ValueError as e:
        return [str(e)]
    for k in REQUIRED:
        if k not in fm:
            errors.append(f"frontmatter 缺 {k}")
    kind = fm.get("type")
    if kind not in ("single", "thread"):
        errors.append("type 必須是 single 或 thread")
    if fm.get("source") != "repurposed":
        errors.append("source 必須是 repurposed")
    if fm.get("status") not in ("draft", "approved"):
        errors.append(f"status 必須是 draft 或 approved（現在是 {fm.get('status')}）")
    topic = fm.get("topic", "")
    if topic and re.search(r"[.&]", topic):
        errors.append("topic 不能有 . 或 &")

    name = os.path.basename(path)
    m_name = BATCH_NAME.match(name)
    sp = fm.get("source_post", "")
    m = re.fullmatch(r"/posts/([a-z0-9-]+)/", sp)
    if not m:
        errors.append(f"source_post 格式錯誤：{sp}")
    else:
        slug = m.group(1)
        if not glob.glob(os.path.join(ROOT, "posts", f"*-{slug}.md")):
            errors.append(f"source_post 對應的文章不存在：posts/*-{slug}.md")
        if not m_name or m_name.group(2) != slug:
            errors.append("檔名必須是 {date}-{source_post slug}-{nn}.md")
        # 同一篇文章只能有一批（同一個日期前綴）；別批已經改寫過就不行
        mine = batch_date(path)
        others = []
        for f in glob.glob(os.path.join(ROOT, "threads", "*.md")):
            if os.path.abspath(f) == os.path.abspath(path):
                continue
            if re.search(rf"^source_post:\s*{re.escape(sp)}\s*$", open(f, encoding="utf-8").read(), re.M):
                if batch_date(f) != mine or mine is None:
                    others.append(os.path.relpath(f, ROOT))
        if others:
            errors.append(f"這篇已經改寫過：{others}")

    if kind == "single" and len(posts) not in (1, 2):
        errors.append(f"single 要 1 則（或 1 則＋1 則回覆），現在 {len(posts)} 則")
    if kind == "thread" and not 3 <= len(posts) <= 6:
        errors.append(f"thread 要 3–6 則，現在 {len(posts)} 則")
    for i, p in enumerate(posts, 1):
        if len(p) > MAX_CHARS:
            errors.append(f"第 {i} 則 {len(p)} 字，超過 {MAX_CHARS}")
        if "掰掰" in p:
            errors.append(f"第 {i} 則有「掰掰」（Threads 不用）")
        if re.search(r"https?://", p) and (i == 1 or (kind == "thread" and i < len(posts))):
            errors.append(f"第 {i} 則有連結（主貼文不放；串文只有最後一則可以放）")
    return errors


def set_status(path: str, status: str, url: str = "") -> None:
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^status:.*$", f"status: {status}", text, count=1, flags=re.M)
    if url:
        text = re.sub(r"^threads_url:.*$", f"threads_url: {url}", text, count=1, flags=re.M)
    if status == "published":
        now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
        if re.search(r"^published_at:", text, re.M):
            text = re.sub(r"^published_at:.*$", f"published_at: {now}", text, count=1, flags=re.M)
        else:
            text = re.sub(r"^(threads_url:.*)$", rf"\1\npublished_at: {now}", text, count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(text)


def publish_order() -> list[str]:
    """approved 的檔案依發布優先順序排：最久沒發過的文章優先（從沒發過的最先），同一篇照檔名。
    這樣不同文章的 idea 會交錯發，不會同一篇連發好幾天。"""
    last: dict[str, str] = {}  # source_post → 最後一次發布時間
    approved = []
    for f in sorted(glob.glob(os.path.join(ROOT, "threads", "*.md"))):
        try:
            fm, _ = split(f)
        except ValueError:
            continue
        sp = fm.get("source_post", "")
        if fm.get("status") == "approved":
            approved.append((sp, os.path.relpath(f, ROOT)))
        elif fm.get("status") == "published" and sp:
            when = fm.get("published_at") or fm.get("date", "")
            last[sp] = max(last.get(sp, ""), when)
    return [f for sp, f in sorted(approved, key=lambda x: (last.get(x[0], ""), x[1]))]


def main() -> int:
    if sys.argv[1:] == ["order"]:
        print("\n".join(publish_order()))
        return 0
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "check":
        errors = check(path)
        for e in errors:
            print(f"✗ {os.path.basename(path)}: {e}")
        if not errors:
            print(f"✓ {os.path.basename(path)}")
        return 1 if errors else 0
    if cmd == "posts-json":
        fm, posts = split(path)
        out = {"posts": posts}
        if fm.get("topic"):
            out["topic_tag"] = fm["topic"]
        json.dump(out, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False)
        return 0
    if cmd == "set-status":
        set_status(path, sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
        return 0
    if cmd == "field":
        print(split(path)[0].get(sys.argv[3], ""))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""homuchen.com 的 SEO lint：發布前檢查單篇文章，或產出全站健檢報告。

用法（從 repo 根目錄執行）：
    python3 scripts/seo_lint.py drafts/2026-07-14-ai-agent-line-bot-tutorial.md
    python3 scripts/seo_lint.py --all                       # 全站報告（Markdown，印到 stdout）
    python3 scripts/seo_lint.py --all --out _resources/seo-health.md
    python3 scripts/seo_lint.py --all --live                # 另外抓線上頁面核對 meta / canonical
    python3 scripts/seo_lint.py --all --format json

等級：
    error  發布前一定要修（壞掉的站內連結、frontmatter 必填欄位錯誤）
    warn   應該修（缺 description、沒有站內連結進來、圖片沒有 alt…）
    info   參考（長度可能被截斷、經過 redirect 的舊連結…）

單篇模式有 error 時 exit code 為 1，可以接在發布流程前面。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://homuchen.com"
CATEGORIES = {"生活", "讀書筆記", "Web Development", "AI"}
IMAGE_FMT = "https://storage.googleapis.com/homuchen.com/images/{slug}-0.jpg"
SIGNOFF = "掰掰"

# 長度用「字寬」算：中日韓全形字算 2，其他算 1（跟 CLAUDE.md 的「150-160 字元」同一把尺）
DESC_MIN, DESC_MAX = 60, 200
TITLE_MAX = 70

# 這天以前的舊文（Jekyll 時期）不套用新慣例：image 用 {path: ...}、結尾沒有「掰掰～👋」
LEGACY_BEFORE = "2025-01-01"

# Ghost 的固定路由（docs/routes.yaml）
STATIC_ROUTES = [r"^/$", r"^/services/$", r"^/courses/$", r"^/posts/$",
                 r"^/tag/[^/]+/$", r"^/author/[^/]+/$"]
# 在 Ghost 後台建的獨立頁面（不在 repo 裡）；新增頁面時補在這裡
KNOWN_PAGES = {"/ai-automation-workflow/"}

LINK_RE = re.compile(
    r"""(?:\]\(|href=["'])(?:https?://(?:www\.)?homuchen\.com)?(/[^)\s"'#?]*)""")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def date_str(fm: dict) -> str:
    return str(fm.get("date") or "")[:10]


def image_url(fm: dict):
    """跟 upload_to_ghost.py 一樣：image 可以是字串或 {path: ...}。"""
    image = fm.get("image")
    return image.get("path") if isinstance(image, dict) else image


def title_tokens(title: str) -> set:
    """英文字詞 + 中文雙字詞，用來找標題相近的文章。"""
    t = title.lower()
    words = set(re.findall(r"[a-z][a-z0-9]+", t))
    for run in re.findall(r"[一-鿿]+", t):
        words |= {run[i:i + 2] for i in range(len(run) - 1)}
    return words


@dataclass
class Post:
    path: str
    slug: str
    fm: dict
    body: str
    published: bool
    links: list = field(default_factory=list)   # 站內路徑（已去掉 code block）


@dataclass
class Issue:
    level: str
    code: str
    msg: str


def strip_code(body: str) -> str:
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", body))


def load_post(path: str) -> Post:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    fm, body = ({}, text)
    if m:
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            fm = {"__yaml_error__": True}
        body = m.group(2)
    slug = DATE_PREFIX_RE.sub("", os.path.basename(path)[:-3]).lower()   # Ghost 的 slug 一律小寫
    rel = os.path.relpath(os.path.abspath(path), REPO)
    if rel.startswith(".."):
        rel = os.path.abspath(path)
    post = Post(rel, slug, fm, body, rel.startswith("posts" + os.sep))
    post.links = [p for p in LINK_RE.findall(strip_code(body))]
    return post


def load_redirects() -> list:
    path = os.path.join(REPO, "docs", "redirects.yaml")
    if not os.path.exists(path):
        return []
    data = yaml.safe_load(open(path, encoding="utf-8")) or {}
    out = []
    for code in data.values():
        for src, dst in (code or {}).items():
            try:
                out.append((re.compile(src), dst))
            except re.error:
                pass
    return out


class Site:
    def __init__(self, extra_files: list[str] = ()):
        self.posts: dict[str, Post] = {}
        self.drafts: dict[str, Post] = {}
        for p in sorted(glob.glob(os.path.join(REPO, "posts", "*.md"))):
            post = load_post(p)
            self.posts[post.slug] = post
        for p in sorted(glob.glob(os.path.join(REPO, "drafts", "*.md"))):
            post = load_post(p)
            self.drafts[post.slug] = post
        for p in extra_files:   # 不在 posts/ drafts/ 的檔案也能檢查
            post = load_post(p)
            if post.slug not in self.posts and post.slug not in self.drafts:
                self.drafts[post.slug] = post
        self.redirects = load_redirects()
        self.inbound: dict[str, set] = {s: set() for s in {**self.posts, **self.drafts}}
        for src in self.posts.values():          # 只算已發布文章給的連結
            for path in src.links:
                m = re.match(r"^/posts/([^/]+)/?$", path)
                t = m.group(1).lower() if m else None
                if t and t in self.inbound and t != src.slug:
                    self.inbound[t].add(src.slug)

    def get(self, slug: str):
        return self.posts.get(slug) or self.drafts.get(slug)

    def redirect_target(self, path: str):
        for rx, dst in self.redirects:
            if rx.search(path):
                return dst
        return None

    def related(self, post: Post, n: int = 3) -> list[str]:
        """沒有連結進來的文章：找 tag／標題／分類最接近、還沒連過它的已發布文章。"""
        lower = lambda xs: {str(x).lower() for x in (xs or [])}
        cat = post.fm.get("category")
        tags = lower(post.fm.get("tags")) - {str(cat).lower()}
        words = title_tokens(str(post.fm.get("title") or ""))
        scored = []
        for other in self.posts.values():
            if other.slug == post.slug or other.slug in self.inbound[post.slug]:
                continue
            shared_tags = len(tags & lower(other.fm.get("tags")))
            shared_words = len(words & title_tokens(str(other.fm.get("title") or "")))
            score = 3 * shared_tags + min(shared_words, 5) + (other.fm.get("category") == cat)
            if score >= 3:
                scored.append((score, date_str(other.fm), other.slug))
        scored.sort(reverse=True)
        return [s for _, _, s in scored[:n]]


def check_post(post: Post, site: Site) -> list[Issue]:
    issues: list[Issue] = []
    fm = post.fm
    add = lambda lv, code, msg: issues.append(Issue(lv, code, msg))

    if fm.get("__yaml_error__"):
        add("error", "frontmatter", "frontmatter 不是合法 YAML")
        return issues
    if not fm:
        add("error", "frontmatter", "沒有 frontmatter")
        return issues

    # --- frontmatter
    title = str(fm.get("title") or "").strip()
    if not title:
        add("error", "title", "缺 title")
    elif width(title) > TITLE_MAX:
        add("info", "title-long", f"title 字寬 {width(title)}（>{TITLE_MAX}），搜尋結果可能被截斷")
    if not fm.get("date"):
        add("error", "date", "缺 date")
    legacy = bool(fm.get("date")) and date_str(fm) < LEGACY_BEFORE
    cat = fm.get("category")
    if cat not in CATEGORIES:
        add("error", "category", f"category「{cat}」不在 4 大分類 {sorted(CATEGORIES)}")
    if cat and str(cat).lower() in {str(t).lower() for t in (fm.get("tags") or [])}:
        add("info", "tag-dup", f"tags 重複了 category「{cat}」")
    image = image_url(fm)
    if not image:
        add("warn" if legacy else "error", "image", "缺 image（沒有封面圖，社群分享也沒有預覽圖）")
    elif not legacy and image != IMAGE_FMT.format(slug=post.slug):
        add("info", "image-path", f"image 跟慣例路徑不同：{image}")
    desc = str(fm.get("description") or "").strip()
    if not desc:
        add("warn", "desc-missing", "缺 description（線上會沒有 meta description）")
    else:
        w = width(desc)
        if w < DESC_MIN:
            add("warn", "desc-short", f"description 字寬只有 {w}（<{DESC_MIN}）")
        elif w > DESC_MAX:
            add("info", "desc-long", f"description 字寬 {w}（>{DESC_MAX}），後段可能被截斷")

    # --- 內文
    clean = strip_code(post.body)
    if re.search(r"^# ", clean, re.M):
        add("warn", "body-h1", "內文有 H1（# ），Ghost 已經把 title 當 H1")
    empty_alt = sum(1 for alt in IMG_RE.findall(clean) if not alt.strip())
    if empty_alt:
        add("warn", "img-alt", f"{empty_alt} 張圖片沒有 alt")
    if not legacy and SIGNOFF not in post.body[-400:]:
        add("warn", "signoff", "結尾沒有「掰掰～👋」")

    # --- 站內連結（往外）
    post_links = 0
    for path in sorted(set(post.links)):
        m = re.match(r"^/posts/([^/]+)/?$", path)
        if m:
            slug = m.group(1).lower()
            if slug == post.slug:
                continue
            if slug in site.posts:
                post_links += 1
                if not path.endswith("/"):
                    add("info", "link-slash", f"{path} 少了結尾的 /（會多一次 redirect）")
            elif slug in site.drafts:
                add("warn", "link-draft", f"連到還沒發布的草稿 {path}")
            elif site.redirect_target(path):
                add("info", "link-redirect", f"{path} 會被 redirect 到 {site.redirect_target(path)}")
            else:
                add("error", "link-broken", f"站內連結找不到文章：{path}")
        elif path in KNOWN_PAGES or any(re.match(rx, path) for rx in STATIC_ROUTES):
            continue
        elif site.redirect_target(path):
            add("info", "link-redirect", f"{path} 是舊網址，會 redirect 到 {site.redirect_target(path)}，建議直接連新網址")
        elif re.match(r"^/(content|assets|ghost)/", path):
            continue
        else:
            add("warn", "link-unknown",
                f"{path} 不是文章也不是已知路由（如果是 Ghost 頁面，加進 KNOWN_PAGES）")
    if post_links == 0:
        add("warn", "no-outlinks", "沒有連到任何站內文章")

    # --- 站內連結（進來）
    inbound = site.inbound.get(post.slug, set())
    if not inbound:
        sug = site.related(post)
        hint = f"；可以從這幾篇補連結：{', '.join(sug)}" if sug else ""
        level = "warn" if post.published else "info"
        add(level, "orphan", f"沒有任何已發布文章連到這篇{hint}")
    return issues


def check_live(post: Post) -> list[Issue]:
    url = f"{SITE}/posts/{post.slug}/"
    issues = []
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (seo-lint)"})
        with urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", "ignore")
            final = r.geturl()
    except HTTPError as e:
        return [Issue("error", "live-status", f"線上回應 HTTP {e.code}：{url}")]
    except (URLError, TimeoutError) as e:
        return [Issue("info", "live-fetch", f"抓不到線上頁面：{e}")]
    if final.rstrip("/").lower() != url.rstrip("/").lower():
        issues.append(Issue("info", "live-redirect", f"線上被轉到 {final}"))
    if not re.search(r'<meta name="description" content="[^"]+"', html):
        issues.append(Issue("warn", "live-desc", "線上頁面沒有 meta description"))
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canon:
        issues.append(Issue("warn", "live-canonical", "線上頁面沒有 canonical"))
    elif canon.group(1).rstrip("/").lower() != url.rstrip("/").lower():
        issues.append(Issue("warn", "live-canonical", f"canonical 指向 {canon.group(1)}"))
    if 'property="og:image"' not in html:
        issues.append(Issue("warn", "live-ogimage", "線上頁面沒有 og:image"))
    if '"@type": "Article"' not in html and '"@type":"Article"' not in html:
        issues.append(Issue("info", "live-schema", "線上頁面找不到 Article 結構化資料"))
    return issues


ICON = {"error": "✖", "warn": "▲", "info": "·"}
ORDER = {"error": 0, "warn": 1, "info": 2}


def print_single(post: Post, issues: list[Issue], site: Site) -> None:
    inbound = len(site.inbound.get(post.slug, ()))
    print(f"\n{post.path}  （進站連結 {inbound} 篇）")
    if not issues:
        print("  ✔ 沒有問題")
    for i in sorted(issues, key=lambda x: ORDER[x.level]):
        print(f"  {ICON[i.level]} [{i.level}] {i.msg}")


def site_report(site: Site, results: dict, live: bool) -> str:
    posts = list(site.posts.values())
    counts: dict[str, list] = {}
    by_level: dict[tuple, set] = {}
    for slug, issues in results.items():
        for i in issues:
            counts.setdefault(i.code, []).append(slug)
            by_level.setdefault((i.level, i.code), set()).add(slug)
    n = len(posts)
    has_desc = n - len(counts.get("desc-missing", []))
    orphans = [p for p in posts if not site.inbound[p.slug]]
    lines = [
        "# homuchen.com SEO 健檢",
        "",
        f"> 產生時間：{time.strftime('%Y-%m-%d %H:%M')}；範圍：`posts/` {n} 篇已發布、`drafts/` {len(site.drafts)} 篇草稿"
        + ("；含線上檢查" if live else "；只檢查本機檔案（加 `--live` 會抓線上頁面）"),
        "",
        "## 總覽",
        "",
        "| 項目 | 數字 |",
        "|---|---:|",
        f"| 有 description | {has_desc} / {n} |",
        f"| 沒有任何文章連進來（孤兒頁） | {len(orphans)} |",
        f"| 只有 1 篇文章連進來 | {sum(len(site.inbound[p.slug]) == 1 for p in posts)} |",
        f"| 沒有連到任何站內文章 | {len(counts.get('no-outlinks', []))} |",
        f"| 壞掉的站內連結（篇數） | {len(set(counts.get('link-broken', [])))} |",
        "",
        "## 問題分類",
        "",
        "| 等級 | 代碼 | 篇數 |",
        "|---|---|---:|",
    ]
    for (level, code), slugs in sorted(by_level.items(), key=lambda kv: (ORDER[kv[0][0]], -len(kv[1]))):
        lines.append(f"| {level} | `{code}` | {len(slugs)} |")

    lines += ["", "## 孤兒頁與建議補連結的來源", "",
              "| 文章 | 日期 | 可以從這些文章連過來 |", "|---|---|---|"]
    for p in sorted(orphans, key=lambda p: date_str(p.fm), reverse=True):
        sug = ", ".join(f"`{s}`" for s in site.related(p)) or "（找不到 tag 或標題相近的文章）"
        lines.append(f"| `{p.slug}` | {date_str(p.fm)} | {sug} |")

    lines += ["", "## 每篇的 error / warn", ""]
    for slug, issues in sorted(results.items()):
        bad = [i for i in issues if i.level != "info"]
        if bad:
            post = site.get(slug)
            lines.append(f"- **`{slug}`**（{post.path}）")
            for i in sorted(bad, key=lambda x: ORDER[x.level]):
                lines.append(f"  - {i.level}：{i.msg}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="要檢查的文章（.md）")
    ap.add_argument("--all", action="store_true", help="檢查 posts/ 全部文章並產出報告")
    ap.add_argument("--live", action="store_true", help="另外抓線上頁面核對 meta / canonical / og:image")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--out", help="報告寫到這個檔案（預設印到 stdout）")
    args = ap.parse_args()
    if not args.files and not args.all:
        ap.print_help()
        return 2

    site = Site(extra_files=args.files)
    targets = list(site.posts.values()) if args.all else [load_post(f) for f in args.files]
    targets = [site.get(t.slug) or t for t in targets]

    results: dict[str, list] = {}
    for post in targets:
        issues = check_post(post, site)
        if args.live and post.published:
            issues += check_live(post)
            time.sleep(0.3)
        results[post.slug] = issues

    if args.format == "json":
        out = json.dumps({s: [i.__dict__ for i in iss] for s, iss in results.items()},
                         ensure_ascii=False, indent=2)
    elif args.all:
        out = site_report(site, results, args.live)
    else:
        for post in targets:
            print_single(post, results[post.slug], site)
        out = None

    if out is not None:
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"已寫入 {args.out}", file=sys.stderr)
        else:
            print(out)
    has_error = any(i.level == "error" for iss in results.values() for i in iss)
    return 1 if (has_error and not args.all) else 0


if __name__ == "__main__":
    sys.exit(main())

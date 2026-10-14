#!/usr/bin/env python3
"""Google Search Console (sc-domain:homuchen.com) read-only queries via a service account.

Subcommands:
  query      Search Analytics with any dimensions / filters / date range
  top-posts  Per-post clicks for /posts/{slug}/ (merges URL variants), flags repurposed posts
  sitemaps   List submitted sitemaps and their status

Examples:
  gsc.py query --dimensions query --filter "page contains /posts/markdown-tutorial/" --limit 20
  gsc.py query --dimensions date --days 90 --filter "query includingRegex claude"
  gsc.py query --dimensions query --compare --min-impressions 50
  gsc.py top-posts --not-repurposed --limit 10
  gsc.py sitemaps

Credentials: GSC_SERVICE_ACCOUNT_FILE (default ~/.config/gsc-service-account.json).
The service account must be a (restricted) user on the Search Console property.
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
import time
from datetime import date, timedelta
from urllib.parse import quote, urlparse

import jwt
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SITE = os.environ.get("GSC_SITE", "sc-domain:homuchen.com")
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://searchconsole.googleapis.com/webmasters/v3"
DATA_DELAY_DAYS = 3  # GSC 資料約延遲 2-3 天
OPERATORS = ["equals", "notEquals", "contains", "notContains", "includingRegex", "excludingRegex"]
DIMENSIONS = ["query", "page", "date", "country", "device", "searchAppearance"]


def access_token() -> str:
    key_file = os.path.expanduser(os.environ.get("GSC_SERVICE_ACCOUNT_FILE", "~/.config/gsc-service-account.json"))
    if not os.path.exists(key_file):
        sys.exit(f"找不到 service account 金鑰：{key_file}（可用 GSC_SERVICE_ACCOUNT_FILE 指定）")
    with open(key_file) as f:
        sa = json.load(f)
    now = int(time.time())
    assertion = jwt.encode(
        {"iss": sa["client_email"], "scope": SCOPE, "aud": TOKEN_URL, "iat": now, "exp": now + 3600},
        sa["private_key"],
        algorithm="RS256",
        headers={"kid": sa["private_key_id"]},
    )
    r = requests.post(
        TOKEN_URL,
        data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def api(token: str, method: str, path: str, body: dict | None = None) -> dict:
    r = requests.request(
        method,
        f"{API}/sites/{quote(SITE, safe='')}{path}",
        headers={"Authorization": f"Bearer {token}"},
        json=body,
        timeout=60,
    )
    if r.status_code == 403:
        sys.exit(f"403：service account 沒有 {SITE} 的權限。\n{r.text[:300]}")
    if r.status_code >= 400:
        sys.exit(f"API 錯誤 {r.status_code}: {r.text[:500]}")
    return r.json()


def date_range(args) -> tuple[date, date]:
    end = date.fromisoformat(args.end) if args.end else date.today() - timedelta(days=DATA_DELAY_DAYS)
    start = date.fromisoformat(args.start) if args.start else end - timedelta(days=args.days - 1)
    return start, end


def parse_filter(s: str) -> dict:
    parts = s.split(None, 2)
    if len(parts) != 3 or parts[0] not in DIMENSIONS or parts[1] not in OPERATORS:
        sys.exit(f"filter 格式：'<dimension> <operator> <expression>'，dimension ∈ {DIMENSIONS}，operator ∈ {OPERATORS}")
    return {"dimension": parts[0], "operator": parts[1], "expression": parts[2]}


def search_analytics(token: str, start: date, end: date, args) -> list[dict]:
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": args.dimensions,
        "type": args.type,
        "rowLimit": 25000,
    }
    if args.filter:
        body["dimensionFilterGroups"] = [{"filters": [parse_filter(f) for f in args.filter]}]
    rows = api(token, "POST", "/searchAnalytics/query", body).get("rows", [])
    out = []
    for row in rows:
        rec = dict(zip(args.dimensions, row.get("keys", [])))
        rec.update(
            clicks=row["clicks"],
            impressions=row["impressions"],
            ctr=round(row["ctr"], 4),
            position=round(row["position"], 1),
        )
        out.append(rec)
    return out


def emit(rows: list[dict], fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    if not rows:
        print("(no rows)")
        return
    cols = list(rows[0].keys())
    if fmt == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
        return
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if r[c] is None else (f"{r[c]:.1%}" if c.endswith("ctr") else str(r[c])) for c in cols))


def cmd_query(args) -> None:
    token = access_token()
    start, end = date_range(args)
    rows = search_analytics(token, start, end, args)
    if args.compare:
        span = (end - start).days + 1
        prev = search_analytics(token, start - timedelta(days=span), start - timedelta(days=1), args)
        prev_by_key = {tuple(r[d] for d in args.dimensions): r for r in prev}
        for r in rows:
            p = prev_by_key.get(tuple(r[d] for d in args.dimensions))
            r["prev_clicks"] = p["clicks"] if p else 0
            r["prev_impressions"] = p["impressions"] if p else 0
            r["prev_position"] = p["position"] if p else None
            r["clicks_delta"] = r["clicks"] - r["prev_clicks"]
    rows = [r for r in rows if r["impressions"] >= args.min_impressions]
    sort_key = "date" if args.dimensions == ["date"] else args.sort
    rows.sort(key=lambda r: r[sort_key], reverse=sort_key != "date" and sort_key != "position")
    print(f"# {SITE} {start} ~ {end}{' (vs previous period)' if args.compare else ''}", file=sys.stderr)
    emit(rows[: args.limit], args.format)


def repurposed_posts() -> set[str]:
    done = set()
    for path in glob.glob(os.path.join(ROOT, "threads", "*.md")):
        with open(path) as f:
            m = re.search(r"^source_post:\s*(\S+)", f.read(), re.M)
        if m:
            done.add(m.group(1).rstrip("/") + "/")
    return done


def cmd_top_posts(args) -> None:
    args.dimensions = ["page"]
    args.filter = ["page contains /posts/"]
    token = access_token()
    start, end = date_range(args)
    done = repurposed_posts()
    pages: dict[str, dict] = {}
    for row in search_analytics(token, start, end, args):
        m = re.match(r"^/posts/([^/]+)/", urlparse(row["page"]).path)
        if not m:
            continue
        key = f"/posts/{m.group(1)}/"
        p = pages.setdefault(key, {"post": key, "clicks": 0, "impressions": 0, "_pos": 0.0})
        p["clicks"] += row["clicks"]
        p["impressions"] += row["impressions"]
        p["_pos"] += row["position"] * row["impressions"]
    rows = []
    for p in pages.values():
        imp = p["impressions"]
        p["ctr"] = round(p["clicks"] / imp, 4) if imp else 0
        p["position"] = round(p.pop("_pos") / imp, 1) if imp else None
        p["repurposed"] = p["post"] in done
        if not (args.not_repurposed and p["repurposed"]):
            rows.append(p)
    rows.sort(key=lambda p: (p["clicks"], p["impressions"]), reverse=True)
    print(f"# {SITE} {start} ~ {end}", file=sys.stderr)
    emit(rows[: args.limit], args.format)


def cmd_sitemaps(args) -> None:
    rows = [
        {
            "path": s.get("path"),
            "lastSubmitted": s.get("lastSubmitted"),
            "lastDownloaded": s.get("lastDownloaded"),
            "isPending": s.get("isPending"),
            "errors": s.get("errors"),
            "warnings": s.get("warnings"),
        }
        for s in api(access_token(), "GET", "/sitemaps").get("sitemap", [])
    ]
    emit(rows, args.format)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, with_range=True):
        p.add_argument("--format", choices=["table", "json", "csv"], default="table")
        if with_range:
            p.add_argument("--days", type=int, default=28, help="區間長度（預設 28，結束日為今天 -3 天）")
            p.add_argument("--start", help="YYYY-MM-DD（覆蓋 --days）")
            p.add_argument("--end", help="YYYY-MM-DD")
            p.add_argument("--limit", type=int, default=30)
            p.add_argument("--type", default="web", choices=["web", "image", "video", "news", "discover", "googleNews"])

    q = sub.add_parser("query", help="Search Analytics 任意查詢")
    common(q)
    q.add_argument("--dimensions", type=lambda s: s.split(","), default=["query"],
                   help=f"逗號分隔，可用：{','.join(DIMENSIONS)}（預設 query）")
    q.add_argument("--filter", action="append", help="'<dimension> <operator> <expression>'，可重複（AND）")
    q.add_argument("--sort", default="clicks", choices=["clicks", "impressions", "ctr", "position"])
    q.add_argument("--min-impressions", type=int, default=0)
    q.add_argument("--compare", action="store_true", help="附上前一個等長區間的數字")
    q.set_defaults(func=cmd_query)

    t = sub.add_parser("top-posts", help="每篇 /posts/ 文章的點擊（合併 URL 變體）")
    common(t)
    t.add_argument("--not-repurposed", action="store_true", help="排除 threads/ 已有 source_post 指向的文章")
    t.set_defaults(func=cmd_top_posts)

    s = sub.add_parser("sitemaps", help="列出已提交的 sitemap")
    common(s, with_range=False)
    s.set_defaults(func=cmd_sitemaps)

    args = ap.parse_args()
    if getattr(args, "dimensions", None):
        bad = [d for d in args.dimensions if d not in DIMENSIONS]
        if bad:
            sys.exit(f"不支援的 dimension：{bad}")
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""列出 homuchen.com 各篇文章在 Google Search Console 的點擊/曝光（用 service account 唯讀）。

用法：
  python3 scripts/gsc_top_pages.py [--days 28] [--limit 30] [--json] [--not-repurposed]

  --not-repurposed  排除 threads/ 裡已經有 source_post 指向的文章

憑證：GSC_SERVICE_ACCOUNT_FILE（預設 ~/.config/gsc-service-account.json）。
該 service account 需在 Search Console 被加為 sc-domain:homuchen.com 的使用者（受限即可）。
"""

import argparse
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "sc-domain:homuchen.com"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
TOKEN_URL = "https://oauth2.googleapis.com/token"


def access_token(key_file: str) -> str:
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


def query(token: str, days: int) -> list[dict]:
    # GSC 資料約延遲 2-3 天
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=days - 1)
    r = requests.post(
        f"https://searchconsole.googleapis.com/webmasters/v3/sites/{quote(SITE, safe='')}/searchAnalytics/query",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": ["page"],
            "dimensionFilterGroups": [{"filters": [{"dimension": "page", "operator": "contains", "expression": "/posts/"}]}],
            "rowLimit": 1000,
        },
        timeout=60,
    )
    if r.status_code == 403:
        sys.exit(f"403：service account 還沒被加進 Search Console 的 {SITE}。\n{r.text[:300]}")
    r.raise_for_status()
    return r.json().get("rows", [])


def repurposed_posts() -> set[str]:
    done = set()
    for path in glob.glob(os.path.join(ROOT, "threads", "*.md")):
        with open(path) as f:
            m = re.search(r"^source_post:\s*(\S+)", f.read(), re.M)
        if m:
            done.add(m.group(1).rstrip("/") + "/")
    return done


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--not-repurposed", action="store_true")
    args = ap.parse_args()

    key_file = os.path.expanduser(os.environ.get("GSC_SERVICE_ACCOUNT_FILE", "~/.config/gsc-service-account.json"))
    rows = query(access_token(key_file), args.days)
    done = repurposed_posts()

    pages = {}
    for row in rows:
        path = urlparse(row["keys"][0]).path
        m = re.match(r"^/posts/([^/]+)/", path)
        if not m:
            continue
        key = f"/posts/{m.group(1)}/"
        p = pages.setdefault(key, {"post": key, "clicks": 0, "impressions": 0, "_pos": 0.0})
        p["clicks"] += row["clicks"]
        p["impressions"] += row["impressions"]
        p["_pos"] += row["position"] * row["impressions"]

    result = []
    for p in pages.values():
        imp = p["impressions"]
        p["ctr"] = round(p["clicks"] / imp, 4) if imp else 0
        p["position"] = round(p.pop("_pos") / imp, 1) if imp else None
        p["repurposed"] = p["post"] in done
        if not (args.not_repurposed and p["repurposed"]):
            result.append(p)
    result.sort(key=lambda p: (p["clicks"], p["impressions"]), reverse=True)
    result = result[: args.limit]

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    print(f"{'clicks':>6} {'impr':>7} {'ctr':>6} {'pos':>5}  T  post")
    for p in result:
        print(f"{p['clicks']:>6} {p['impressions']:>7} {p['ctr']:>6.1%} {p['position'] or 0:>5}  "
              f"{'✓' if p['repurposed'] else ' '}  {p['post']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

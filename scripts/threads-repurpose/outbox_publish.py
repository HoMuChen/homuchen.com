#!/usr/bin/env python3
"""透過 outbox（https://outbox.homuchen.com）發一則 Threads 貼文或串文。

  outbox_publish.py <posts.json> <idempotency_key> [--ids-out ids.json]

  posts.json：thread_file.py posts-json 產生的 {"posts": [...], "topic_tag": ...}
  idempotency_key：同一個檔案固定用同一個（threads-repurpose:{檔名}），重跑不會發兩次

環境變數（systemd 從 ~/.config/threads-repurpose.env 讀）：
  OUTBOX_API_KEY   outbox 的存取金鑰（obx_…），由 outbox 的 ops key:create 產生
  OUTBOX_URL       預設 https://outbox.homuchen.com

結束碼：
  0  已發出（--ids-out 寫入 {"send_id", "ids", "permalink"}）
  1  沒發成（失敗、部分發出、被拒絕、檢查沒過）：不要自動重試，Threads 上可能有部分貼文，要人看
  3  還沒有結果（outbox 連不上、還在重試、等核准）：下次用同一個 key 再呼叫，拿到的是同一筆
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

URL = os.environ.get("OUTBOX_URL", "https://outbox.homuchen.com").rstrip("/")
DONE = {"sent"}
FAILED = {"failed", "partial", "rejected", "expired", "canceled"}
WAIT_SEC = 10 * 60  # outbox 自動重試（30 秒、2 分鐘、8 分鐘）最多等這麼久


class Pending(Exception):
    """還沒有結果，下次再問。"""


def call(method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(
        f"{URL}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {os.environ['OUTBOX_API_KEY']}",
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        # 401：金鑰沒設好，什麼都還沒發，修好設定下次再來
        if e.code >= 500 or e.code in (401, 429):
            raise Pending(f"outbox {e.code}: {detail}") from e
        raise SystemExit(f"outbox {e.code}: {detail}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise Pending(f"outbox 連不上：{e}") from e


def main() -> int:
    args = sys.argv[1:]
    ids_out = None
    if "--ids-out" in args:
        i = args.index("--ids-out")
        ids_out = Path(args[i + 1])
        del args[i : i + 2]
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    if not os.environ.get("OUTBOX_API_KEY"):
        print("Missing OUTBOX_API_KEY", file=sys.stderr)
        return 3
    data = json.loads(Path(args[0]).read_text())
    body = {"posts": data["posts"], "idempotency_key": args[1]}
    if data.get("topic_tag"):
        body["topic_tag"] = data["topic_tag"]

    try:
        send = call("POST", "/api/v1/threads/publish", body)
        print(f"outbox send {send['send_id']}: {send['status']}")
        deadline = time.time() + WAIT_SEC
        while send["status"] in ("queued", "sending") and time.time() < deadline:
            time.sleep(15)
            send = call("GET", f"/api/v1/sends/{send['send_id']}")
    except Pending as e:
        print(e, file=sys.stderr)
        return 3

    status = send["status"]
    for p in send["parts"]:
        print(f"  {p['index']}. {p['status']} {p.get('id', '')} {p.get('error', '')}".rstrip())
    if status in DONE:
        permalink = send["parts"][0].get("permalink")
        print(f"Permalink: {permalink}")
        if ids_out:
            ids_out.write_text(json.dumps({"send_id": send["send_id"],
                                           "ids": [p.get("id") for p in send["parts"]],
                                           "permalink": permalink}))
        return 0
    if status in FAILED:
        print(f"outbox send {send['send_id']} {status}: {send.get('error', '')}", file=sys.stderr)
        return 1
    print(f"outbox send {send['send_id']} still {status}, will check again next run", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())

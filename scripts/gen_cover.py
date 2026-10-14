#!/usr/bin/env python3
"""用 OpenAI Images API 生成部落格封面。

產出：
  _resources/images/{slug}-0.png  原圖（1536x1024）
  _resources/images/{slug}-0.jpg  裁成 1200x630 的封面（上下各裁一點，重要內容請放中間）

用法：
  set -a && source .env && set +a
  python3 scripts/gen_cover.py <slug> "<prompt>" [--ref _resources/images/xxx-0.jpg] [--quality high]

--ref 會把既有封面當風格參考（走 /v1/images/edits），沒給就走 /v1/images/generations。
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "_resources", "images")
MODEL = "gpt-image-2"
SIZE = "1536x1024"


def multipart(fields, files):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, path in files:
        with open(path, "rb") as f:
            data = f.read()
        ctype = "image/png" if path.endswith(".png") else "image/jpeg"
        body += (
            f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; '
            f'filename="{os.path.basename(path)}"\r\nContent-Type: {ctype}\r\n\r\n'
        ).encode() + data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def generate(prompt, ref, quality):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY 沒設定（先 set -a && source .env && set +a）")
    if ref:
        body, ctype = multipart(
            {"model": MODEL, "prompt": prompt, "size": SIZE, "quality": quality, "n": "1"},
            [("image[]", ref)],
        )
        url = "https://api.openai.com/v1/images/edits"
    else:
        body = json.dumps({"model": MODEL, "prompt": prompt, "size": SIZE, "quality": quality, "n": 1}).encode()
        ctype = "application/json"
        url = "https://api.openai.com/v1/images/generations"
    req = Request(url, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
    try:
        with urlopen(req, timeout=600) as resp:
            data = json.load(resp)
    except HTTPError as e:
        sys.exit(f"API 錯誤 {e.code}: {e.read().decode()[:500]}")
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("prompt")
    ap.add_argument("--ref", help="風格參考圖（既有封面）")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    args = ap.parse_args()

    png = os.path.join(IMAGES, f"{args.slug}-0.png")
    jpg = os.path.join(IMAGES, f"{args.slug}-0.jpg")
    prompt = args.prompt
    if args.ref:
        prompt = "參考這張圖的視覺風格（配色、版面、插畫風格），但內容換成以下描述，不要照抄原圖的文字：\n" + prompt
    with open(png, "wb") as f:
        f.write(generate(prompt, args.ref, args.quality))

    # 1536x1024 → 寬縮成 1200（1200x800）→ 置中裁成 1200x630
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
                    "--resampleWidth", "1200", png, "--out", jpg], check=True, capture_output=True)
    subprocess.run(["sips", "-c", "630", "1200", jpg], check=True, capture_output=True)
    print(png)
    print(jpg)


if __name__ == "__main__":
    main()

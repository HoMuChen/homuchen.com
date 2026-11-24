"""ghost_sync.py 用的 patch 引擎：在 Ghost 現有的 Lexical 上做最小修改。

支援：新增段落、清單加一項（真的 list，或 Ghost 上「段落 + 換行 + `* `」的假清單）、
句尾接文字、替換句子（Ghost 上的格式必須跟 repo 舊版一致）、表格儲存格、程式碼單行替換。

不重新產生整篇，所以 Ghost 上獨有的內容（圖片說明、刪除線、後台改過的字）都不會被動到。
任何一個改動找不到「唯一」對應位置就丟 PatchError，整篇不改。
"""
import copy
import difflib
import html as htmlmod
import json
import re

import upload_to_ghost as U


class PatchError(Exception):
    pass


def norm(s):
    s = htmlmod.unescape(s or "")
    return re.sub(r"[\s*​]", "", s)


def md_text(md):
    h = U.md_to_html(md)
    return norm(re.sub(r"<[^>]+>", "", h))


def ltext(n):
    if "text" in n and isinstance(n["text"], str):
        return n["text"]
    t = n.get("type")
    if t == "html":
        return re.sub(r"<[^>]+>", "", n.get("html", ""))
    if t in ("codeblock", "code"):
        return n.get("code", "")
    if t == "markdown":
        return n.get("markdown", "")
    return "".join(ltext(c) for c in n.get("children", []))


def walk(n, parent=None):
    yield n, parent
    for c in n.get("children", []) or []:
        yield from walk(c, n)


def render_nodes(md):
    return json.loads(U.html_to_lexical(U.md_to_html(md)))["root"]["children"]


def inline_children(md):
    nodes = render_nodes(md)
    if len(nodes) != 1:
        raise PatchError(f"片段不是單一區塊：{md[:40]}")
    n = nodes[0]
    if n["type"] == "list":
        n = n["children"][0]
    kids = n.get("children", [])
    # listitem 裡如果包了 paragraph，取出 inline
    if len(kids) == 1 and kids[0].get("type") == "paragraph":
        kids = kids[0].get("children", [])
    return kids


def is_item(line):
    return re.match(r"^\s*[\*\-\+] ", line) is not None


def unique(cands, what):
    if len(cands) != 1:
        raise PatchError(f"{what}：找到 {len(cands)} 個位置（需要剛好 1 個）")
    return cands[0]


# ---------------------------------------------------------------- operations

def insert_block(root, anchor_md, new_md, before=False):
    target = md_text(anchor_md)
    tops = root["children"]
    cands = [i for i, n in enumerate(tops) if target and target in norm(ltext(n))]
    i = unique(cands, f"段落錨點「{anchor_md.strip()[:30]}」")
    if tops[i]["type"] in ("html", "markdown"):
        raise PatchError(f"錨點在 {tops[i]['type']} 卡片裡，無法安全插入")
    new_nodes = render_nodes(new_md)
    pos = i if before else i + 1
    tops[pos:pos] = new_nodes
    return md_text(new_md)


def insert_item(root, anchor_md, new_md):
    target = md_text(anchor_md)
    new_inline = inline_children(new_md)
    # (a) 真的 list：找 listitem
    items = [(n, p) for n, p in walk(root) if n.get("type") == "listitem" and target and target == norm(ltext(n))]
    if not items:
        items = [(n, p) for n, p in walk(root) if n.get("type") == "listitem" and target and target in norm(ltext(n))]
    if items:
        n, parent = unique(items, f"清單錨點「{anchor_md.strip()[:30]}」")
        li = copy.deepcopy(render_nodes(new_md)[0]["children"][0])
        k = parent["children"].index(n)
        parent["children"].insert(k + 1, li)
        for v, c in enumerate(parent["children"], 1):
            if "value" in c:
                c["value"] = v
        return md_text(new_md)
    # (b) 段落 + linebreak 的「假清單」：在錨點那一行後面插一行
    paras = []
    for n, _ in walk(root):
        if n.get("type") != "paragraph":
            continue
        segs, cur = [], []
        for idx, c in enumerate(n.get("children", [])):
            if c.get("type") == "linebreak":
                segs.append(cur)
                cur = []
            else:
                cur.append(idx)
        segs.append(cur)
        for seg in segs:
            if seg and target == norm("".join(ltext(n["children"][j]) for j in seg)):
                paras.append((n, seg))
    n, seg = unique(paras, f"清單錨點（段落換行）「{anchor_md.strip()[:30]}」")
    first = n["children"][seg[0]]
    m = re.match(r"^\s*([\*\-\+] )", first.get("text", ""))
    bullet = m.group(1) if m else "* "
    text_node = {"detail": 0, "format": 0, "mode": "normal", "style": "", "text": bullet,
                 "type": "extended-text", "version": 1}
    ins = [{"type": "linebreak", "version": 1}, text_node] + copy.deepcopy(new_inline)
    at = seg[-1] + 1
    n["children"][at:at] = ins
    return md_text(new_md)


def text_nodes_exact(root, target):
    kinds = ("paragraph", "listitem", "extended-heading", "heading", "extended-quote", "quote", "tablecell")
    out = []
    for n, p in walk(root):
        if n.get("type") in kinds:
            own = [c for c in n.get("children", []) if c.get("type") != "list"]
            if norm("".join(ltext(c) for c in own)) == target:
                out.append(n)
    return out


def append_text(root, old_md, suffix_md):
    target = md_text(old_md)
    n = unique(text_nodes_exact(root, target), f"接續錨點「{old_md.strip()[:30]}」")
    add = copy.deepcopy(inline_children(suffix_md.lstrip()))
    kids = n["children"]
    k = next((i for i, c in enumerate(kids) if c.get("type") == "list"), len(kids))
    kids[k:k] = add
    return md_text(suffix_md)


def replace_inline(root, old_md, new_md):
    target = md_text(old_md)
    n = unique(text_nodes_exact(root, target), f"替換錨點「{old_md.strip()[:30]}」")
    # Ghost 上這段的 inline 格式必須跟 repo 舊版渲染一致，才不會洗掉後台改過的格式
    strip = lambda ns: [{k: v for k, v in c.items() if k in ("type", "text", "format", "url")} for c in ns]
    if strip(n["children"]) != strip(inline_children(old_md)):
        raise PatchError(f"「{old_md.strip()[:30]}」在 Ghost 上的格式跟 repo 不同，不替換")
    n["children"] = copy.deepcopy(inline_children(new_md))
    return None


def html_card_replace(root, old_frag, new_frag):
    cands = [n for n, _ in walk(root) if n.get("type") == "html" and n.get("html", "").count(old_frag) == 1]
    n = unique(cands, f"HTML 卡片裡的「{old_frag[:30]}」")
    n["html"] = n["html"].replace(old_frag, new_frag)


def code_replace(root, old_line, new_line):
    old_s, new_s = old_line.strip(), new_line.strip()
    cands = [n for n, _ in walk(root) if n.get("type") in ("codeblock", "code") and n.get("code", "").count(old_s) == 1]
    if not cands:  # 有時 code 存成 text node
        cands = [n for n, _ in walk(root) if isinstance(n.get("text"), str) and n["text"].count(old_s) == 1
                 and n.get("type") in ("extended-text", "text", "code-highlight")]
    n = unique(cands, f"程式碼「{old_s[:30]}」")
    key = "code" if "code" in n else "text"
    n[key] = n[key].replace(old_s, new_s)


# ---------------------------------------------------------------- diff → ops

def in_code(lines, idx):
    fences = sum(1 for l in lines[:idx] if l.lstrip().startswith("```"))
    return fences % 2 == 1


def prev_nonempty(lines, i):
    j = i - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    return (lines[j] if j >= 0 else None), j


def next_nonempty(lines, i):
    j = i
    while j < len(lines) and not lines[j].strip():
        j += 1
    return lines[j] if j < len(lines) else None


def patch(lexical_json, old_body, new_body, ghost_html=""):
    """回傳 (新 lexical json 字串, 操作說明清單, 預期新增的文字清單, 預期的文字替換清單)。"""
    root = json.loads(lexical_json)["root"]
    a, b = old_body.split("\n"), new_body.split("\n")
    ops, added, replaced, ctx = [], [], [], []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old_l = [l for l in a[i1:i2] if l.strip()]
        new_l = [l for l in b[j1:j2] if l.strip()]
        if not old_l and not new_l:
            continue
        if tag == "insert" or (not old_l and new_l):
            anchor, _ = prev_nonempty(a, i1)
            block = "\n".join(new_l)
            if all(is_item(l) for l in new_l) and anchor and is_item(anchor):
                for l in new_l:
                    added.append(insert_item(root, anchor, l))
                    ctx.append(md_text(anchor) + added[-1])
                    ops.append(f"清單加一項：{l.strip()[:60]}")
                    anchor = l
            else:
                nxt = next_nonempty(a, i1)
                try:
                    added.append(insert_block(root, anchor, block))
                    ctx.append(md_text(anchor) + added[-1])
                except PatchError:
                    if not nxt:
                        raise
                    added.append(insert_block(root, nxt, block, before=True))
                    ctx.append(added[-1] + md_text(nxt))
                ops.append(f"新增段落：{block.strip()[:60]}")
        elif len(old_l) == 1 and len(new_l) == 1:
            o, n = old_l[0], new_l[0]
            if in_code(a, a.index(o, i1)):
                code_replace(root, o, n)
                replaced.append((norm(o), norm(n)))
                ops.append(f"改程式碼：{o.strip()[:40]} → {n.strip()[:40]}")
            elif o.startswith("|") and n.startswith("|"):
                ca = [c.strip() for c in o.strip("|").split("|")]
                cb = [c.strip() for c in n.strip("|").split("|")]
                for x, y in zip(ca, cb):
                    if x != y:
                        hx, hy = (re.sub(r"^<p>|</p>$", "", U.md_to_html(s).strip()) for s in (x, y))
                        try:
                            html_card_replace(root, hx, hy)
                        except PatchError:
                            replace_inline(root, x, y)
                        ops.append(f"表格儲存格加連結：{y[:60]}")
            elif n.startswith(o.rstrip()):
                suffix = n[len(o.rstrip()):]
                added.append(append_text(root, o, suffix))
                ctx.append(md_text(o) + added[-1])
                ops.append(f"句尾接上：{suffix.strip()[:60]}")
            else:
                replace_inline(root, o, n)
                replaced.append((md_text(o), md_text(n)))
                ops.append(f"替換句子：{n.strip()[:60]}")
        else:
            raise PatchError(f"無法處理的改動（{tag} {len(old_l)}→{len(new_l)} 行）：{(new_l or old_l)[0][:50]}")
    return json.dumps({"root": root}, ensure_ascii=False), ops, added, replaced, ctx

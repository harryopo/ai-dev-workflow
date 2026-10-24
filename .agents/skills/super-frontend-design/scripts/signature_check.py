#!/usr/bin/env python3
"""Signature landing checker for generated UI code (stdlib only).

The skill's review check #12 is the only *positive* check in the whole table:
the other eleven only remove things that are definitely wrong. This script
makes the "definitely right" half mechanically decidable.

Contract (see subskills/design/SKILL.md "签名落地" and subskills/review/SKILL.md
§0 check #12):

* the implementation must carry at least one `/* signature: ... */` marker;
* markers must not all be parked in low-visibility zones (footer / copyright
  line / collapsed region) -- a signature nobody can see is not a signature;
* a scan that examined zero files exits 2 -- an empty scan is not a verdict.

Design notes learned the hard way:

* comment bodies are matched, so this file's own examples are never counted;
* the marker is a comment, therefore it survives minifiers and bundlers, which
  is exactly why the contract mandates a comment marker instead of a data
  attribute that would be stripped;
* findings carry the measured count and the threshold, not a vibe.

Usage:
    python scripts/signature_check.py <file-or-dir> [...] [--json] [--strict]
                                     [--min N] [--require-marker "text"]
Exit: 0 clean, 1 findings, 2 bad invocation / nothing to scan.
"""

import argparse
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

SIGNATURE_MARKER = re.compile(r"/\*\s*signature:\s*(?P<body>[^*]*?)\*/", re.I)
# 行式标记只认行首 //：# 与 CSS id 选择器（#signature:hover）同形，
# 而扫描范围里的文件类型没有任何一种用 # 作行注释——它是纯歧义源；
# <!-- 形式由 HTML_COMMENT_MARKER 在 original 上处理，rest 里不存在
SIGNATURE_LINE = re.compile(
    r"(?i)^[ \t]*//[ \t]*signature:\s*(?P<body>.*?)[ \t]*$")

# 低关注度容器：签名落在这些容器的内部 = 没人看得见
LOW_VISIBILITY_TAGS = ("footer", "copyright", "legal", "disclaimer",
                       "colophon", "footnote")

# 版权行文本特征
COPYRIGHT_TEXT = re.compile(
    r"(?i)(©|\(c\)\s*\d{4}|all\s+rights\s+reserved|copyright\s+©?)"
)

# 判定"落在低关注区"时向上下各看的行数——版权文本行可能紧邻标记
CONTEXT_LINES = 2

SCAN_SUFFIXES = {".html", ".htm", ".css", ".scss", ".sass", ".less",
                  ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro"}


class ScanError(Exception):
    pass


def gather(paths):
    files = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.is_file() and f.suffix.lower() in SCAN_SUFFIXES:
                    files.append(f)
        else:
            raise ScanError("路径不存在：%s" % p)
    # 去重且保持稳定顺序
    seen, uniq = set(), []
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def read_lines(path):
    return path.read_bytes().decode("utf-8", errors="replace").split("\n")


def low_visibility_spans(lines):
    """Line numbers (1-based) that sit inside a low-visibility container.

    A marker is invisible only when it lives INSIDE such a container, not
    merely near one -- a hero marker three lines above a <footer> is fine.
    """
    spans = set()
    for tag in LOW_VISIBILITY_TAGS:
        opens = [i for i, ln in enumerate(lines, start=1)
                 if re.search(r"(?i)<%s(?=[\s>])" % tag, ln)]
        closes = [i for i, ln in enumerate(lines, start=1)
                  if re.search(r"(?i)</%s\s*>" % tag, ln)]
        for o in opens:
            later = [c for c in closes if c >= o]
            end = later[0] if later else o
            spans.update(range(o, end + 1))
    return spans


def copyright_lines(lines):
    return {i for i, ln in enumerate(lines, start=1) if COPYRIGHT_TEXT.search(ln)}


def strip_html_comments(lines):
    """Split each line into (html_comment_spans, remaining_text).

    An HTML comment is itself a legal marker carrier (`<!-- signature: ... -->`),
    so it cannot be blanked out wholesale. But a `/* signature: */` nested
    *inside* an HTML comment is an example, not a landing. So: report the HTML
    comment spans separately, and let the caller search block/line forms only
    in the remaining text.
    """
    out = []
    for line in lines:
        spans, rest = [], line
        for m in re.finditer(r"<!--(.*?)-->", rest, flags=re.S):
            spans.append((m.start(), m.end()))
        # 去掉所有 HTML 注释区间，保留其余文本
        pieces, last = [], 0
        for s, e in spans:
            pieces.append(rest[last:s])
            last = e
        pieces.append(rest[last:])
        out.append(("".join(pieces), spans, rest))
    return out


HTML_COMMENT_MARKER = re.compile(r"(?i)<!--\s*signature:\s*(?P<body>.*?)\s*-->", re.S)


def scan_file(path):
    """Return list of markers: [{line, body, file, low_visibility}]."""
    markers = []
    raw = read_lines(path)
    parsed = strip_html_comments(raw)
    spans = low_visibility_spans(raw)
    copy_lines = copyright_lines(raw)

    def is_low(idx):
        if idx in spans:
            return True
        near = range(max(1, idx - CONTEXT_LINES), idx + CONTEXT_LINES + 1)
        return any(n in copy_lines for n in near)

    for idx, (rest, _spans, original) in enumerate(parsed, start=1):
        low = is_low(idx)
        # 1) HTML 注释形式
        for m in HTML_COMMENT_MARKER.finditer(original):
            markers.append({"file": str(path), "line": idx,
                            "body": m.group("body").strip(),
                            "low_visibility": low})
        # 2) 块注释 / 行注释形式（只在 HTML 注释之外找）
        for m in SIGNATURE_MARKER.finditer(rest):
            body = m.group("body").strip()
            markers.append({"file": str(path), "line": idx, "body": body,
                            "low_visibility": low})
        m2 = SIGNATURE_LINE.search(rest)
        if m2 and not SIGNATURE_MARKER.search(rest):
            markers.append({"file": str(path), "line": idx,
                            "body": m2.group("body").strip(),
                            "low_visibility": low})
    return markers


def main(argv=None):
    ap = argparse.ArgumentParser(description="检查签名识别符是否已落地到实现代码")
    ap.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="警告也判失败")
    ap.add_argument("--min", type=int, default=1, help="签名落点最少数量，默认 1")
    ap.add_argument("--require-marker", default=None,
                    help="要求至少一个落点的标记正文包含该子串（用于核对指定签名）")
    ns = ap.parse_args(argv)

    try:
        if ns.min < 1:
            raise ScanError("--min 必须 ≥ 1（零落点等于没做）")
        files = gather(ns.paths)
        if not files:
            raise ScanError("没有可扫描的代码文件——空扫描不等于通过")
    except ScanError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2
    except OSError as exc:
        sys.stderr.write("ERROR  输入不可读: %s\n" % exc)
        return 2

    markers = []
    for f in files:
        try:
            markers += scan_file(f)
        except OSError as exc:
            sys.stderr.write("ERROR  读不了 %s: %s\n" % (f, exc))
            return 2

    hard, warn = [], []

    if len(markers) < ns.min:
        hard.append({
            "rule": "signature-landing-missing",
            "file": files[0].name,
            "line": 0,
            "message": "实现代码里没有签名落点——签名是反模板的唯一原料，零落点等于交付模板",
            "measured": len(markers),
            "threshold": ns.min,
        })

    # 目录扫描：陌生人首先看到的是首页，首页必须带签名
    entry_files = [f for f in files if f.name.lower() in ("index.html", "index.htm")]
    for entry in entry_files:
        if not any(m["file"] == str(entry) for m in markers):
            hard.append({
                "rule": "signature-entry-missing",
                "file": entry.name,
                "line": 0,
                "message": "首页没有签名落点——陌生人第一眼看的就是这个页面",
                "measured": 0,
                "threshold": 1,
            })

    if markers and all(m["low_visibility"] for m in markers):
        hard.append({
            "rule": "signature-landing-invisible",
            "file": markers[0]["file"],
            "line": markers[0]["line"],
            "message": "签名落点全部在低关注区（页脚/版权行/折叠区）——看不见的签名等于没有签名",
            "measured": sum(1 for m in markers if m["low_visibility"]),
            "threshold": len(markers),
        })

    if ns.require_marker:
        needle = ns.require_marker.strip()
        if not any(needle in m["body"] for m in markers):
            hard.append({
                "rule": "signature-marker-mismatch",
                "file": files[0].name,
                "line": markers[0]["line"] if markers else 0,
                "message": "没有任何落点的标记正文包含指定签名 %r" % needle,
                "measured": sum(1 for m in markers if needle in m["body"]),
                "threshold": 1,
            })

    if not markers:
        warn.append({
            "rule": "signature-empty",
            "file": files[0].name,
            "line": 0,
            "message": "未发现任何 /* signature: */ 标记注释",
            "measured": 0,
        })
    else:
        invisible = sum(1 for m in markers if m["low_visibility"])
        if invisible and invisible < len(markers):
            warn.append({
                "rule": "signature-partially-invisible",
                "file": markers[0]["file"],
                "line": markers[0]["line"],
                "message": "部分签名落点在低关注区，建议移到视觉焦点区",
                "measured": invisible,
            })

    if ns.json:
        print(json.dumps({"scanned": len(files), "markers": markers,
                          "hard": hard, "warn": warn},
                         ensure_ascii=False, indent=2))
    else:
        for m in markers:
            flag = " (低关注区)" if m["low_visibility"] else ""
            print("SIG   %s:%s  %s%s" % (Path(m["file"]).name, m["line"], m["body"], flag))
        for x in hard:
            print("FAIL  %-40s %s:%s  %s (measured %s / threshold %s)"
                  % (x["rule"], x["file"], x["line"], x["message"], x["measured"], x["threshold"]))
        for x in warn:
            print("WARN  %-40s %s:%s  %s (%s)"
                  % (x["rule"], x["file"], x["line"], x["message"], x["measured"]))
        print("-" * 72)
        print("scanned=%d markers=%d hard=%d warn=%d"
              % (len(files), len(markers), len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())

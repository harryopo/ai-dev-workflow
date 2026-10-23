#!/usr/bin/env python3
"""Composition contract checker for generated UI code (stdlib only).

`references/macrostructures.md` defines 21 page shapes, each with six elements
(title anchor / body columns / divider / imagery / entrance). Selecting one
used to be fire-and-forget: the name was recorded, the shape was not built.
This script makes the *declaration* mechanically checkable so review can spend
its attention on whether the code actually matches the claim.

Contract (see references/composition-contract.md):

* all six `composition:` fields must be present;
* `focus-hierarchy` must be 1, 2 or 3;
* the composition markers and the macrostructure stamp must live in the same
  file -- a stamp in one file and the contract in another means the contract
  was written for a different page;
* a scan that examined zero files exits 2 -- an empty scan is not a verdict.

What this script CANNOT check: whether the code matches the declaration. It
proves the contract was *stated*; review check #13 proves it was *built*.
Neither replaces the other.

Usage:
    python scripts/composition_check.py <file-or-dir> [...] [--json] [--strict]
                                      [--require-macrostructure "01·Bento Grid"]
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

# 六要素契约字段，顺序即契约顺序
CONTRACT_FIELDS = ("heading-anchor", "body-columns", "divider",
                   "imagery", "entrance", "focus-hierarchy")

# 载体必须匹配项目形态：Tailwind / 单文件 HTML 项目没有独立 CSS 文件，
# 标记只能写在 HTML 注释里。只认 CSS 块注释会让这类项目必然误判为
# 「没有任何契约」——与 signature_check 的双载体口径保持一致。
COMPOSITION_MARKER = re.compile(
    r"/\*\s*composition:\s*(?P<key>[a-z\-]+)\s*=\s*(?P<value>.*?)\s*\*/", re.I)
COMPOSITION_MARKER_HTML = re.compile(
    r"<!--\s*composition:\s*(?P<key>[a-z\-]+)\s*=\s*(?P<value>.*?)\s*-->", re.I)
MACROSTRUCTURE_STAMP = re.compile(
    r"/\*\s*macrostructure:\s*(?P<value>.*?)\*/", re.I | re.S)
MACROSTRUCTURE_STAMP_HTML = re.compile(
    r"<!--\s*macrostructure:\s*(?P<value>.*?)\s*-->", re.I | re.S)
# stamp 形如 `01·Bento Grid · theme: Tally · genre: SaaS`——结构名自身含 `·`，
# 所以按 "key: value" 形态切分，遇到第一个带冒号的段即停。
STAMP_PART = re.compile(r"^[a-zA-Z][a-zA-Z0-9_\-]*\s*:")

CARRIER_CSS = "css"
CARRIER_HTML = "html"


def stamp_structure_name(raw):
    """从 stamp 正文里取出 macrostructure 名称部分。"""
    parts = [p.strip() for p in raw.split("·")]
    kept = []
    for p in parts:
        if STAMP_PART.match(p):
            break
        if p:
            kept.append(p)
    return "·".join(kept).strip()

VALID_FOCUS = {"1", "2", "3"}

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
    seen, uniq = set(), []
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def read_text(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def scan_file(path):
    """Return (fields dict, has_stamp bool, stamp_value str|None, carrier str|None).

    carrier 记录契约写在哪类载体上——CSS 块注释、HTML 注释，或两者混用。
    只用于 JSON 输出的可诊断性，不影响判定。
    """
    src = read_text(path)
    fields = {}
    carriers = set()
    for m in COMPOSITION_MARKER.finditer(src):
        key = m.group("key").lower()
        fields.setdefault(key, m.group("value").strip())
        carriers.add(CARRIER_CSS)
    for m in COMPOSITION_MARKER_HTML.finditer(src):
        key = m.group("key").lower()
        fields.setdefault(key, m.group("value").strip())
        carriers.add(CARRIER_HTML)

    stamp = MACROSTRUCTURE_STAMP.search(src) or MACROSTRUCTURE_STAMP_HTML.search(src)
    stamp_value = None
    if stamp:
        stamp_value = stamp_structure_name(stamp.group("value"))
        if stamp.re is MACROSTRUCTURE_STAMP_HTML:
            carriers.add(CARRIER_HTML)
        else:
            carriers.add(CARRIER_CSS)
    carrier = "+".join(sorted(carriers)) if carriers else None
    return fields, bool(stamp), stamp_value, carrier


def main(argv=None):
    ap = argparse.ArgumentParser(description="检查构图契约六要素是否齐全并与 macrostructure 同文件")
    ap.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="警告也判失败")
    ap.add_argument("--require-macrostructure", default=None,
                    help="要求 stamp 中的 macrostructure 名称包含该子串")
    ns = ap.parse_args(argv)

    try:
        files = gather(ns.paths)
        if not files:
            raise ScanError("没有可扫描的代码文件——空扫描不等于通过")
    except ScanError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2
    except OSError as exc:
        sys.stderr.write("ERROR  输入不可读: %s\n" % exc)
        return 2

    hard, warn = [], []
    total_fields = set()
    stamped_files = 0
    carriers_seen = set()

    for f in files:
        try:
            fields, has_stamp, stamp_value, carrier = scan_file(f)
        except OSError as exc:
            sys.stderr.write("ERROR  读不了 %s: %s\n" % (f, exc))
            return 2

        if not fields:
            continue
        total_fields |= set(fields)
        if carrier:
            carriers_seen.add(carrier)
        if has_stamp:
            stamped_files += 1
        else:
            hard.append({
                "rule": "composition-without-stamp",
                "file": f.name,
                "line": 0,
                "message": "同一文件里有构图契约标记但没有 macrostructure stamp —— "
                           "契约与结构名对不上，等于没有契约",
                "measured": 0,
                "threshold": 1,
            })

        missing = [k for k in CONTRACT_FIELDS if k not in fields]
        if missing:
            hard.append({
                "rule": "composition-fields-missing",
                "file": f.name,
                "line": 0,
                "message": "构图契约缺要素：%s" % "、".join(missing),
                "measured": len(CONTRACT_FIELDS) - len(missing),
                "threshold": len(CONTRACT_FIELDS),
            })

        focus = fields.get("focus-hierarchy", "")
        if focus and focus not in VALID_FOCUS:
            hard.append({
                "rule": "composition-focus-invalid",
                "file": f.name,
                "line": 0,
                "message": "focus-hierarchy 取值非法：%r（只能是 1 / 2 / 3）" % focus,
                "measured": 1,
                "threshold": 1,
            })

        empty = [k for k, v in fields.items() if not v]
        if empty:
            hard.append({
                "rule": "composition-field-empty",
                "file": f.name,
                "line": 0,
                "message": "构图契约要素取值为空：%s" % "、".join(empty),
                "measured": len(empty),
                "threshold": 1,
            })

        if ns.require_macrostructure and has_stamp:
            needle = ns.require_macrostructure.strip()
            if needle and needle not in stamp_value:
                hard.append({
                    "rule": "macrostructure-mismatch",
                    "file": f.name,
                    "line": 0,
                    "message": "stamp 里的 macrostructure 不含 %r（实际：%r）"
                               % (needle, stamp_value),
                    "measured": 0,
                    "threshold": 1,
                })

    # 全局层面：一份实现里若有契约，就必须六项齐全
    if total_fields and not set(CONTRACT_FIELDS).issubset(total_fields):
        missing = [k for k in CONTRACT_FIELDS if k not in total_fields]
        hard.append({
            "rule": "composition-contract-incomplete",
            "file": files[0].name,
            "line": 0,
            "message": "整个实现里缺构图契约要素：%s" % "、".join(missing),
            "measured": len(set(CONTRACT_FIELDS) & total_fields),
            "threshold": len(CONTRACT_FIELDS),
        })

    if not total_fields:
        hard.append({
            "rule": "composition-absent",
            "file": files[0].name,
            "line": 0,
            "message": "未发现任何构图契约标记（CSS 块注释 /* composition: */ "
                       "或 HTML 注释 <!-- composition: -->）——"
                       "构图契约是必填项，不是不填也不犯错的加分项",
            "measured": 0,
            "threshold": len(CONTRACT_FIELDS),
        })

    if ns.json:
        print(json.dumps({"scanned": len(files), "stamped_files": stamped_files,
                          "fields": sorted(total_fields),
                          "carriers": sorted(carriers_seen),
                          "hard": hard, "warn": warn},
                         ensure_ascii=False, indent=2))
    else:
        for x in hard:
            print("FAIL  %-40s %s:%s  %s (measured %s / threshold %s)"
                  % (x["rule"], x["file"], x["line"], x["message"],
                     x["measured"], x["threshold"]))
        for x in warn:
            print("WARN  %-40s %s:%s  %s (%s)"
                  % (x["rule"], x["file"], x["line"], x["message"], x["measured"]))
        print("-" * 72)
        print("scanned=%d stamped=%d fields=%d hard=%d warn=%d"
              % (len(files), stamped_files, len(total_fields), len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())

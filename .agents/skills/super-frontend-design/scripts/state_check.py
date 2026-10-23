#!/usr/bin/env python3
"""State contract gate -- does the page handle the states it declares?

This script backs review check #14. It answers one narrow question: *if the
implementation says it covers loading/empty/error, is there evidence in the
code that it actually does?*

It deliberately does NOT judge whether the states are designed well -- a
skeleton that misaligns with the real content is a real defect, but it is a
human judgement (review #14). The script only proves "declared" and "landed".
Mixing the two would produce a gate that fails good work and passes box-ticking.

Evidence is matched loosely (class / attribute / copy) because the point is
coverage, not a specific implementation idiom. Declared-but-not-landed is the
hard failure -- that is the lie the gate exists to catch.
"""

import argparse
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

# 派生规则：交互复杂度 → 必须声明的状态集合
COMPLEXITY_REQUIREMENTS = {
    "static": set(),                                   # 静态页豁免
    "basic": {"error", "success"},
    "moderate": {"loading", "empty", "error"},
    "complex": {"loading", "empty", "error", "no-permission"},
    "app": {"loading", "empty", "error", "success", "no-permission"},
}

# 每个状态的证据模式。刻意宽松：只证明"这个状态在代码里出现过"。
# 判"做得好不好"是 review 的人工职责，不是脚本的。
STATE_EVIDENCE = {
    "loading": (
        r"\bis-loading\b", r"data-state\s*=\s*[\"']loading", r"aria-busy",
        r"骨架屏", r"加载中", r"载入中", r"loading\.\.\.",
    ),
    "empty": (
        r"\bis-empty\b", r"data-state\s*=\s*[\"']empty", r"\bempty-state\b",
        r"空态", r"暂无", r"没有(?:任何)?(?:数据|记录|结果|内容)",
    ),
    "error": (
        r"\bis-error\b", r"data-state\s*=\s*[\"']error", r"aria-invalid",
        r"错误态", r"出错了", r"失败", r"重试", r"请重试",
    ),
    "success": (
        r"\bis-success\b", r"data-state\s*=\s*[\"']success", r"已成功", r"成功",
    ),
    "no-permission": (
        r"no-permission", r"data-state\s*=\s*[\"']no-permission",
        r"无权限", r"没有权限", r"申请权限",
    ),
    "offline": (
        r"\bis-offline\b", r"data-state\s*=\s*[\"']offline", r"离线", r"网络(?:异常|中断|错误)",
    ),
}

STATES_MARKER_CSS = re.compile(
    r"/\*\s*states:\s*(?P<body>[^*]*?)\*/", re.I)
STATES_MARKER_HTML = re.compile(
    r"<!--\s*states:\s*(?P<body>.*?)\s*-->", re.I | re.S)

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


def parse_states(src):
    """Return (declared set, carriers set). Handles both CSS and HTML carriers."""
    declared, carriers = set(), set()
    for m in STATES_MARKER_CSS.finditer(src):
        body = m.group("body")
        carriers.add("css")
        for tok in re.split(r"[,，、\s]+", body):
            tok = tok.strip().lower()
            if tok:
                declared.add(tok)
    for m in STATES_MARKER_HTML.finditer(src):
        body = m.group("body")
        carriers.add("html")
        for tok in re.split(r"[,，、\s]+", body):
            tok = tok.strip().lower()
            if tok:
                declared.add(tok)
    return declared, carriers


def state_evidence(src, state):
    patterns = STATE_EVIDENCE.get(state)
    if not patterns:
        return False
    return any(re.search(p, src, re.I) for p in patterns)


def validate_complexity(value):
    if value is None:
        return None
    v = value.strip().lower()
    if not v:
        return None
    if v not in COMPLEXITY_REQUIREMENTS:
        raise ScanError(
            "--complexity 取值 %r 不在 %s 中"
            % (value, " / ".join(sorted(COMPLEXITY_REQUIREMENTS))))
    return v


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="检查页面级状态契约：声明的状态是否在代码里有真实证据")
    ap.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="警告也判失败")
    ap.add_argument("--complexity", default=None,
                    help="research 得出的交互复杂度：static/basic/moderate/complex/app；"
                         "缺省时只检查声明与实现一致，不启用派生规则")
    ns = ap.parse_args(argv)

    try:
        complexity = validate_complexity(ns.complexity)
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
    declared_anywhere = set()
    landed_anywhere = set()
    carriers_seen = set()

    for f in files:
        try:
            src = read_text(f)
        except OSError as exc:
            sys.stderr.write("ERROR  读不了 %s: %s\n" % (f, exc))
            return 2

        declared, carriers = parse_states(src)
        carriers_seen |= carriers

        # 本文件声明的状态，必须在本文件里有证据
        for state in sorted(declared):
            declared_anywhere.add(state)
            if state not in STATE_EVIDENCE:
                warn.append({
                    "rule": "state-unknown",
                    "file": f.name,
                    "line": 0,
                    "message": "未知状态名 %r——不是 %s 之一"
                               % (state, "/".join(sorted(STATE_EVIDENCE))),
                    "measured": 1,
                })
                continue
            if not state_evidence(src, state):
                hard.append({
                    "rule": "state-declared-not-landed",
                    "file": f.name,
                    "line": 0,
                    "message": "声明了 %s 状态但代码里找不到任何实现证据——"
                               "声明不是通行证" % state,
                    "measured": 0,
                    "threshold": 1,
                })
            else:
                landed_anywhere.add(state)

        # 代码里有证据但没声明：不阻塞（可能是实现先于声明）
        for state, patterns in STATE_EVIDENCE.items():
            if state in declared:
                continue
            if any(re.search(p, src, re.I) for p in patterns):
                landed_anywhere.add(state)
                warn.append({
                    "rule": "state-landed-not-declared",
                    "file": f.name,
                    "line": 0,
                    "message": "代码里有 %s 状态的实现，但契约声明里没有它" % state,
                    "measured": 1,
                })

    if not declared_anywhere and not landed_anywhere:
        # 声明与实现都没有——这才是"没考虑过状态"
        # 静态页豁免：没有异步数据的页面不要求状态声明
        if complexity == "static":
            warn.append({
                "rule": "state-absent-exempt",
                "file": files[0].name,
                "line": 0,
                "message": "interaction-complexity=static，静态页豁免状态声明",
                "measured": 0,
            })
        else:
            hard.append({
                "rule": "state-absent",
                "file": files[0].name,
                "line": 0,
                "message": "未发现任何 /* states: */ 或 <!-- states: --> 契约标记——"
                           "页面级状态是必填项（static 场景除外）",
                "measured": 0,
                "threshold": len(COMPLEXITY_REQUIREMENTS["app"]),
            })

    # 派生规则：复杂度要求的状态，声明里缺
    if complexity and complexity != "static":
        required = COMPLEXITY_REQUIREMENTS[complexity]
        missing = sorted(required - declared_anywhere)
        if missing:
            hard.append({
                "rule": "state-required-missing",
                "file": files[0].name,
                "line": 0,
                "message": "interaction-complexity=%s 要求状态 %s，声明里缺 %s"
                           % (complexity,
                              "/".join(sorted(required)),
                              "/".join(missing)),
                "measured": len(required) - len(missing),
                "threshold": len(required),
            })

    if ns.json:
        print(json.dumps({"scanned": len(files),
                          "declared": sorted(declared_anywhere),
                          "landed": sorted(landed_anywhere),
                          "carriers": sorted(carriers_seen),
                          "complexity": complexity,
                          "hard": hard, "warn": warn},
                         ensure_ascii=False, indent=2))
    else:
        for x in hard:
            print("FAIL  %-32s %s:%s  %s (measured %s / threshold %s)"
                  % (x["rule"], x["file"], x["line"], x["message"],
                     x["measured"], x["threshold"]))
        for x in warn:
            print("WARN  %-32s %s:%s  %s (%s)"
                  % (x["rule"], x["file"], x["line"], x["message"],
                     x["measured"]))
        print("-" * 72)
        print("scanned=%d declared=%d landed=%d hard=%d warn=%d"
              % (len(files), len(declared_anywhere),
                 len(landed_anywhere), len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())

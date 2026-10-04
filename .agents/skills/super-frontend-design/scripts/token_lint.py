#!/usr/bin/env python3
"""Design-token gate: undefined references, dead tokens, DESIGN.md reconciliation.

Stdlib only. Answers the question the skill asks in every phase — "所有颜色/间距/字体
是否走语义 Token" — without a browser and without npm.

Usage:
    python scripts/token_lint.py <file.css|file.html> [...] [--design DESIGN.md]
                                 [--json] [--strict]
Exit: 0 clean, 1 findings, 2 bad invocation / nothing scanned. An empty scan is
never a pass.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Windows 下 stdout 默认 gbk，中文结论会变乱码，门禁输出统一强制 UTF-8
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

KNOWN = {"--design", "--json", "--strict"}
# 自定义属性名必须是 -- 后接字母/下划线，否则 --- 这种 Markdown 围栏会被当成 token
TOKEN = r"--[A-Za-z_][\w-]*"
VAR_USE = re.compile(r"var\(\s*(%s)\s*(,[^)]*)?\)" % TOKEN)
VAR_DECL = re.compile(r"(%s)\s*:" % TOKEN)
FM_TOKEN_LINE = re.compile(
    r"\s*([\w.-]+)\s*:\s*[\"']?(?:#[0-9a-fA-F]{3,8}|\d+(?:\.\d+)?(?:px|rem|ms|%)|\"[^\"]+\")[\"']?\s*$")


class LintError(Exception):
    pass


def read(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def strip_css_noise(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return text


def css_from(path):
    raw = read(path)
    if path.suffix.lower() == ".css":
        return raw
    blocks = re.findall(r"(?is)<style[^>]*>(.*?)</style>", raw)
    inline = re.findall(r"(?is)style=(['\"])(.*?)\1", raw)
    return "\n".join(blocks + [i[1] for i in inline])


def design_tokens(path):
    """Token names declared in a DESIGN.md contract file.

    Accepts YAML front matter (`tokens:` 下的 key 会自动补 -- 前缀)、`--token:` 行、
    或 `| --token |` 表格。找不到任何 token 时返回 None，让调用方说"未比对"而不是编结论。
    """
    if not path:
        return None
    text = read(path)
    names = set(re.findall(TOKEN, text))
    fm = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if fm:
        # 逐行取 key：整块匹配会让 tokens: 这种父键吃掉下一行的值
        names |= {"--" + m.group(1) for line in fm.group(1).splitlines()
                  for m in [FM_TOKEN_LINE.match(line)] if m}
    return names or None


def lint(paths, design_path):
    defined, used = set(), set()
    declared_in = {}
    per_file = {}
    for p in paths:
        css = strip_css_noise(css_from(p))
        decl = set(VAR_DECL.findall(css))
        uses = set()
        fallback = {}
        for name, fb in VAR_USE.findall(css):
            uses.add(name)
            fallback[name] = bool((fb or "").strip()) or fallback.get(name, False)
        per_file[p] = {"declared": decl, "used": uses, "fallback": fallback}
        for name in decl:
            declared_in.setdefault(name, p)
        defined |= decl
        used |= uses

    findings = []
    for p, info in per_file.items():
        for name in sorted(info["used"] - defined):
            if info["fallback"].get(name):
                findings.append(mk(p, "undefined-with-fallback", "warn", name, "有定义",
                                   "var() 引用的 token 全项目都没定义，靠 fallback 兜底；"
                                   "运行时取值是 fallback，等于 Token 系统失效"))
            else:
                findings.append(mk(p, "undefined-token", "hard", name, "有定义",
                                   "var() 引用了从未定义过的 token（且无 fallback，运行时会被判 invalid）"))
    for name in sorted(defined - used):
        findings.append(mk(declared_in[name], "dead-token", "warn", name, "被引用",
                           "定义了但整份代码里没人 var() 引用"))

    contract = design_tokens(design_path) if design_path else None
    if contract is None and design_path:
        findings.append(mk(design_path, "design-md-no-tokens", "warn",
                           str(design_path), "-", "DESIGN.md 里找不到可比对的 token 声明"))
    elif contract:
        for name in sorted(contract - defined):
            findings.append(mk(design_path, "contract-token-missing", "hard", name, "在代码里定义",
                               "设计契约声明了这个 token，代码里没有"))
        for name in sorted(defined - contract):
            findings.append(mk(design_path, "undocumented-token", "warn", name, "写进契约",
                               "代码用了但设计契约里没有记录"))
    return findings


def mk(path, rule, severity, measured, threshold, message):
    return {"file": str(path), "rule": rule, "severity": severity,
            "measured": measured, "threshold": threshold, "message": message}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for a in argv:
        if a.startswith("-") and a.split("=")[0] not in KNOWN:
            sys.stderr.write("ERROR  未知参数 %r（可用：%s）\n" % (a, ", ".join(sorted(KNOWN))))
            return 2
    ap = argparse.ArgumentParser(prog="token_lint.py", add_help=False, allow_abbrev=False)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--design", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ns = ap.parse_args(argv)

    try:
        files = []
        for a in ns.paths:
            p = Path(a)
            if p.is_dir():
                files += [f for f in sorted(p.rglob("*"))
                          if f.suffix.lower() in (".css", ".html", ".htm")
                          and "node_modules" not in f.parts]
            elif p.is_file():
                files.append(p)
            else:
                raise LintError("no such path: %s" % a)
        if not files:
            raise LintError("没有可检查的 css/html —— 空扫描不等于通过")
        design = Path(ns.design) if ns.design else None
        if design and not design.is_file():
            raise LintError("DESIGN.md 不存在: %s" % design)
    except LintError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2

    findings = lint(files, design)
    hard = [x for x in findings if x["severity"] == "hard"]
    warn = [x for x in findings if x["severity"] == "warn"]
    if ns.json:
        print(json.dumps({"files": len(files), "design": str(design) if design else None,
                          "hard": hard, "warn": warn}, ensure_ascii=False, indent=2))
    else:
        for x in hard:
            print("FAIL  %-24s %s  %s (%s)" % (x["rule"], Path(x["file"]).name, x["message"], x["measured"]))
        for x in warn:
            print("WARN  %-24s %s  %s (%s)" % (x["rule"], Path(x["file"]).name, x["message"], x["measured"]))
        print("-" * 64)
        print("files=%d hard=%d warn=%d" % (len(files), len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Contract tests for scripts/slop_scan.py — run with: python tests/test_slop_scan.py

Each assertion is the scanner's promise. A green run here is what licenses the
"自动扫描" claim in the skill; without it the claim is decoration.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Windows 下 stdout 默认 gbk，FAIL 正文会变乱码
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCANNER = SKILL / "scripts" / "slop_scan.py"
RULES = SKILL / "rules" / "slop-table.json"


def run(*args):
    return subprocess.run([sys.executable, str(SCANNER)] + list(args),
                          capture_output=True, text=True, encoding="utf-8")


def rule_ids():
    return [r["id"] for r in json.loads(RULES.read_bytes().decode("utf-8"))["rules"]]


def test_red_catches_every_rule(fails):
    res = run(str(HERE / "slop_red.html"), "--json", "--strict")
    if res.returncode != 1:
        fails.append("red fixture should exit 1, got %s (%s)" % (res.returncode, res.stderr[:120]))
        return
    hits = {x["rule"] for x in json.loads(res.stdout)["hard"] + json.loads(res.stdout)["warn"]}
    missing = [r for r in rule_ids()
               if r not in hits and r != "ignore-without-reason"]
    if missing:
        fails.append("red fixture missed rules: %s" % ", ".join(missing))


def test_clean_is_silent(fails):
    res = run(str(HERE / "slop_clean.html"), "--json", "--strict")
    if res.returncode != 0:
        data = json.loads(res.stdout) if res.stdout.startswith("{") else {}
        sample = ["%s:%s %s" % (x["rule"], x["line"], x["measured"])
                  for x in data.get("hard", []) + data.get("warn", [])][:5]
        fails.append("clean fixture reported findings (exit %s): %s"
                     % (res.returncode, "; ".join(sample)))


def test_line_numbers_point_at_the_right_line(fails):
    """Regression: masking used to swallow newlines and shift every later line.

    Asserted against concrete anchors rather than the measured blob, because a
    blob-derived probe can differ from the source text for legitimate reasons.
    """
    res = run(str(HERE / "slop_red.html"), "--json")
    lines = (HERE / "slop_red.html").read_bytes().decode("utf-8").split("\n")
    anchors = {"transition-all": "transition: all",
               "placeholder-cdn": "unsplash",
               "lazy-loaded-lcp": 'loading="lazy"',
               "autoplay-with-sound": "<video",
               "side-stripe-card": "border-left"}
    got = {}
    for x in json.loads(res.stdout)["hard"]:
        got.setdefault(x["rule"], []).append(x["line"])
    for rule, needle in anchors.items():
        if rule not in got:
            fails.append("anchor rule %s did not fire at all" % rule)
            continue
        texts = [lines[n - 1] for n in got[rule]]
        if not any(needle in t for t in texts):
            fails.append("no hit of %s lands on a line containing %r; lines were %s"
                         % (rule, needle, [t.strip()[:50] for t in texts]))


def test_empty_input_is_not_a_pass(fails):
    empty = HERE / "_empty_scan_dir"
    empty.mkdir(exist_ok=True)
    try:
        res = run(str(empty))
        if res.returncode != 2:
            fails.append("scanning a dir with no html/css must exit 2, got %s" % res.returncode)
    finally:
        empty.rmdir()


def test_unknown_flag_fails_closed(fails):
    res = run(str(HERE / "slop_clean.html"), "--stric")
    if res.returncode == 0 and "PASS" in res.stdout:
        fails.append("a typo'd flag must not silently scan and print PASS")


def test_waiver_requires_reason(fails):
    res = run(str(HERE / "slop_red.html"), "--allow", "transition-all")
    if res.returncode != 2:
        fails.append("--allow without =reason must exit 2, got %s" % res.returncode)
    res = run(str(HERE / "slop_red.html"), "--json", "--allow", "transition-all=设计确认过")
    if res.returncode == 1 and "transition-all" in " ".join(
            x["rule"] for x in json.loads(res.stdout)["hard"]):
        fails.append("--allow RULE=reason did not suppress the rule")


def test_inline_ignore_without_reason_is_reported(fails):
    tmp = HERE / "_ignore_probe.html"
    tmp.write_text("<!DOCTYPE html><html><body><style>"
                   ".a{transition: all 1s} /* slop-scan-ignore */ </style></body></html>",
                   encoding="utf-8")
    try:
        res = run(str(tmp), "--json")
        rules = {x["rule"] for x in json.loads(res.stdout)["hard"]}
        if "ignore-without-reason" not in rules:
            fails.append("a bare slop-scan-ignore with no reason must be reported")
    finally:
        tmp.unlink()


def test_emoji_rule_is_position_sensitive(fails):
    """句中提到的 emoji 不是图标；标题首字符的 emoji 才是（两类都曾判错）。"""
    tmp = HERE / "_emoji_probe.html"
    tmp.write_text('<!DOCTYPE html><html><body>'
                   '<ul><li>正文标 ⚠️ 的降级引用只告警，不阻断交付</li></ul>'
                   '</body></html>', encoding="utf-8")
    try:
        rules = {x["rule"] for x in json.loads(run(str(tmp), "--json").stdout)["hard"]}
        if "emoji-as-icon" in rules:
            fails.append("a prose mention of an emoji must not count as an icon")
        tmp.write_text('<!DOCTYPE html><html><body><h3>\U0001F9FE 证据账本</h3>'
                       '</body></html>', encoding="utf-8")
        rules = {x["rule"] for x in json.loads(run(str(tmp), "--json").stdout)["hard"]}
        if "emoji-as-icon" not in rules:
            fails.append("a leading emoji outside the old hand-picked list must still fire")
    finally:
        tmp.unlink()


def main():
    fails = []
    for fn in (test_red_catches_every_rule, test_clean_is_silent,
               test_line_numbers_point_at_the_right_line, test_empty_input_is_not_a_pass,
               test_unknown_flag_fails_closed, test_waiver_requires_reason,
               test_inline_ignore_without_reason_is_reported,
               test_emoji_rule_is_position_sensitive):
        fn(fails)
    for f in fails:
        print("FAIL  %s" % f)
    print("-" * 60)
    print("checks=%d failures=%d" % (8, len(fails)))
    print("RESULT: PASS" if not fails else "RESULT: FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

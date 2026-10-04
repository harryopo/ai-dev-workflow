#!/usr/bin/env python3
"""Contract tests for scripts/render_probe.py — run with: python tests/test_render_probe.py

Everything here needs a real browser: the probe measures rendered contrast and
rendered overflow, so a run without Playwright is reported as SKIP, not as a pass.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
PROBE = SKILL / "scripts" / "render_probe.py"
CLEAN = HERE / "slop_clean.html"
RED = HERE / "slop_red.html"
TMP = tempfile.mkdtemp(prefix="sfd-probe-")


def run(*args):
    env = dict(os.environ)
    env.pop("PYTHONIOENCODING", None)
    return subprocess.run([sys.executable, str(PROBE)] + list(args),
                          capture_output=True, env=env, timeout=180)


def decoded(res):
    try:
        return res.stdout.decode("utf-8"), res.stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError("输出不是 UTF-8（Windows 下退回 gbk 会乱码）：%s" % exc)


def data(res):
    out, _ = decoded(res)
    return json.loads(out)


def browser_ready():
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            b.close()
    except Exception:
        return False
    return True


def write(tmp, name, body):
    path = Path(tmp) / name
    path.write_text("<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
                    "</head><body>%s</body></html>" % body, encoding="utf-8")
    return str(path)


def test_clean_renders_clean(fails):
    res = run(str(CLEAN), "--json")
    if res.returncode != 0:
        out, err = decoded(res)
        fails.append("clean fixture must exit 0, got %s: %s" % (res.returncode, (out + err)[:200]))
        return
    d = data(res)
    if d["hard"] or d["warn"]:
        fails.append("clean fixture rendered findings: %s"
                     % [x["rule"] for x in d["hard"] + d["warn"]])


def test_planted_contrast_deficits_are_measured(fails):
    """slop_red.html 里埋了两段低对比文字，探针必须都抓到。"""
    res = run(str(RED), "--json")
    d = data(res)
    hits = [x for x in d["hard"] if x["rule"] == "text-contrast-below-threshold"]
    selectors = " ".join(x["measured"] for x in hits)
    if len(hits) < 2:
        fails.append("expected >=2 contrast findings, got %d (%s)" % (len(hits), selectors))
    for want in ("p.faint", "ratio"):
        if want not in selectors:
            fails.append("contrast hit missing %r; got %s" % (want, selectors))


def test_missing_alt_is_measured(fails):
    res = run(str(RED), "--json")
    if not any(x["rule"] == "img-missing-alt" for x in data(res)["hard"]):
        fails.append("the fixture's <img> without alt must be reported")


def test_horizontal_overflow_is_measured_both_ways(fails):
    wide = write(TMP, "wide.html", '<div style="width:2000px;background:#eee">很宽</div>')
    clipped = write(TMP, "clipped.html",
                    '<style>html,body{overflow-x:clip}</style>'
                    '<div style="width:2000px;background:#eee">很宽</div>')
    d = data(run(wide, "--json", "--widths", "320"))
    if not any(x["rule"] == "h-scroll-at-320px" for x in d["hard"]):
        fails.append("a 2000px block at 320px viewport must report h-scroll-at-320px")
    d = data(run(clipped, "--json", "--widths", "320"))
    if any(x["rule"] == "h-scroll-at-320px" for x in d["hard"]):
        fails.append("overflow-x:clip on html AND body should stop the h-scroll finding")


def test_bad_invocation_exits_2(fails):
    page = write(TMP, "p.html", "<p>正文</p>")
    cases = [("bogus flag", (page, "--widhts", "320")),
             ("bad widths value", (page, "--widths", "375,abc")),
             ("empty widths list", (page, "--widths", ",")),
             ("missing path", (str(Path(TMP) / "gone.html"),)),
             ("no path at all", ())]
    for label, args in cases:
        res = run(*args)
        if res.returncode != 2:
            out, err = decoded(res)
            fails.append("%s must exit 2, got %s (%s)" % (label, res.returncode, (out + err)[:80]))
    empty = Path(TMP) / "emptydir"
    empty.mkdir(exist_ok=True)
    res = run(str(empty))
    if res.returncode != 2:
        fails.append("probing a dir with no html must exit 2, got %s" % res.returncode)


def test_findings_are_readable_utf8(fails):
    res = run(str(RED))
    out, _ = decoded(res)
    if "对比度" not in out and "深底深字" not in out:
        fails.append("expected Chinese finding text to survive; got %r" % out[:120])


def main():
    fails = []
    if not browser_ready():
        print("SKIP  本机没有可用的 Playwright/Chromium，render_probe 的 6 项契约测试未实测")
        print("-" * 60)
        print("checks=0 failures=0 skipped=6")
        # 没量到不等于量对了：退出码 2，禁止把"跑不了"读成"通过"
        print("RESULT: SKIP（未实测，不作为通过证据）")
        return 2
    tests = [test_clean_renders_clean, test_planted_contrast_deficits_are_measured,
             test_missing_alt_is_measured, test_horizontal_overflow_is_measured_both_ways,
             test_bad_invocation_exits_2, test_findings_are_readable_utf8]
    for fn in tests:
        try:
            fn(fails)
        except AssertionError as exc:
            fails.append(str(exc))
        except Exception as exc:
            fails.append("%s crashed: %s" % (fn.__name__, exc))
    shutil.rmtree(TMP, ignore_errors=True)
    for f in fails:
        print("FAIL  %s" % f)
    print("-" * 60)
    print("checks=%d failures=%d" % (len(tests), len(fails)))
    print("RESULT: PASS" if not fails else "RESULT: FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Contract tests for scripts/visual_diff.py — run with: python tests/test_visual_diff.py

diff-mode cases build their own PNGs with Pillow, so they run without a browser.
The shot/check cases need Playwright; when it is missing they are reported as
SKIP rather than pretending to pass.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows 下 stdout 默认 gbk，FAIL 正文会变乱码
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TOOL = SKILL / "scripts" / "visual_diff.py"

try:
    from PIL import Image
except Exception:
    Image = None


def run(*args):
    env = dict(os.environ)
    env.pop("PYTHONIOENCODING", None)
    return subprocess.run([sys.executable, str(TOOL)] + list(args),
                          capture_output=True, env=env)


def decoded(res):
    try:
        return res.stdout.decode("utf-8"), res.stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError("输出不是 UTF-8（Windows 下退回 gbk 会乱码）：%s" % exc)


def report(res):
    out, _ = decoded(res)
    return json.loads(out)


def make_img(path, size, ink_fraction):
    """White canvas with a black block covering `ink_fraction` of the pixels."""
    w, h = size
    img = Image.new("RGB", (w, h), "white")
    block_h = max(1, int(h * ink_fraction))
    img.paste((0, 0, 0), (0, 0, w, block_h))
    img.save(str(path))
    return str(path)


def test_identical_is_zero_diff(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    res = run("diff", a, a, "--json")
    if res.returncode != 0:
        fails.append("identical images must pass, got exit %s" % res.returncode)
        return
    if report(res)["metrics"]["diff_percent"] != 0:
        fails.append("identical images reported non-zero diff_percent")


def test_layout_change_is_hard(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    b = Image.new("RGB", (400, 400), "white")
    b.paste((0, 0, 0), (0, 200, 400, 320))
    bp = Path(tmp) / "b.png"
    b.save(str(bp))
    res = run("diff", a, str(bp), "--json")
    if res.returncode != 1:
        fails.append("moved content must exit 1, got %s" % res.returncode)
    if "diff-over-threshold" not in {x["rule"] for x in report(res)["hard"]}:
        fails.append("moved content must raise diff-over-threshold")


def test_blank_candidate_is_hard(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    blank = make_img(Path(tmp) / "blank.png", (400, 400), 0.0)
    res = run("diff", a, blank, "--json")
    rules = {x["rule"] for x in report(res)["hard"]}
    if "blank-candidate" not in rules:
        fails.append("an all-white candidate must raise blank-candidate, got %s" % rules)
    if res.returncode != 1:
        fails.append("blank candidate must exit 1, got %s" % res.returncode)


def test_blank_candidate_survives_low_pixel_diff(fails, tmp):
    """白底页面占比高，逐像素差可能不到 2%，墨量兜底必须还在。"""
    a = make_img(Path(tmp) / "a.png", (600, 600), 0.2)
    b = make_img(Path(tmp) / "b.png", (600, 600), 0.0)
    d = report(run("diff", a, b, "--json"))["metrics"]
    if d["candidate_ink_fraction"] >= 0.005:
        fails.append("fixture is not blank any more; the regression it guards is untested")


def test_blank_reference_is_hard(fails, tmp):
    blank = make_img(Path(tmp) / "blank.png", (400, 400), 0.0)
    a = make_img(Path(tmp) / "a2.png", (400, 400), 0.2)
    res = run("diff", blank, a, "--json")
    if "blank-reference" not in {x["rule"] for x in report(res)["hard"]}:
        fails.append("an all-white reference must raise blank-reference")


def test_ink_shift_is_warn(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    b = make_img(Path(tmp) / "b.png", (400, 400), 0.02)
    res = run("diff", a, b, "--json")
    if "ink-fraction-shift" not in {x["rule"] for x in report(res)["warn"]}:
        fails.append("content density dropped 90%%, ink-fraction-shift must warn")


def test_size_mismatch_states_unmeasured_area(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    b = make_img(Path(tmp) / "b.png", (400, 200), 0.2)
    res = run("diff", a, b, "--json")
    warn = {x["rule"]: x["measured"] for x in report(res)["warn"]}
    if "size-mismatch" not in warn:
        fails.append("different sizes must warn size-mismatch")
    elif "未比对面积" not in warn["size-mismatch"]:
        fails.append("size-mismatch must say how much was not compared, got %r"
                     % warn["size-mismatch"])


def test_degenerate_crop_refuses_a_verdict(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (20, 20), 0.2)
    b = make_img(Path(tmp) / "b.png", (20, 20), 0.0)
    res = run("diff", a, b, "--json")
    d = report(res)
    if "degenerate-crop" not in {x["rule"] for x in d["hard"]}:
        fails.append("a 20x20 comparison must be refused as degenerate")
    if d["metrics"]:
        fails.append("degenerate comparison still returned metrics: %s" % d["metrics"])


def test_unknown_flag_fails_closed(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    res = run("diff", a, a, "--maxdif", "1")
    out, _ = decoded(res)
    if res.returncode == 0 or "PASS" in out:
        fails.append("a typo'd flag must not print PASS (exit %s)" % res.returncode)


def test_missing_inputs_are_errors(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    for args in (("diff", a), ("diff", a, str(Path(tmp) / "nope.png")),
                 ("shot", str(Path(tmp) / "nope.html")), ("check", a),
                 ("check", str(Path(tmp) / "nope.html"), "--reference", a),
                 ("check", str(HERE / "token_clean.css"), "--reference", str(Path(tmp) / "gone.png")),
                 ("bogus", a)):
        res = run(*args)
        out, err = decoded(res)
        if res.returncode != 2:
            fails.append("%s must exit 2, got %s (%s)" % (" ".join(Path(x).name for x in args),
                                                          res.returncode, (out + err)[:80]))


def test_missing_reference_does_not_open_a_browser(fails, tmp):
    """回归：原先先截图再查参考图，参考图打错字也要等一次浏览器。"""
    res = run("check", str(SKILL / "tests" / "slop_clean.html"),
              "--reference", str(Path(tmp) / "gone.png"))
    out, err = decoded(res)
    if res.returncode != 2 or "参考图" not in err:
        fails.append("missing reference should fail before screenshotting: exit %s %s"
                     % (res.returncode, (out + err)[:120]))


def test_findings_are_readable_utf8(fails, tmp):
    a = make_img(Path(tmp) / "a.png", (400, 400), 0.2)
    b = make_img(Path(tmp) / "b.png", (400, 400), 0.0)
    res = run("diff", a, b)
    out, _ = decoded(res)
    if "近乎空白" not in out:
        fails.append("expected Chinese finding text to survive; got %r" % out[:120])


def test_shot_and_check_roundtrip(fails, tmp):
    if not _has_playwright():
        return "SKIP"
    shot = Path(tmp) / "shot.png"
    res = run("shot", str(SKILL / "tests" / "slop_clean.html"), "--out", str(shot))
    if res.returncode != 0 or not shot.is_file():
        out, err = decoded(res)
        fails.append("shot must produce a png (exit %s): %s" % (res.returncode, (out + err)[:160]))
        return
    res = run("check", str(SKILL / "tests" / "slop_clean.html"),
              "--reference", str(shot), "--out", str(Path(tmp) / "again.png"))
    if res.returncode != 0:
        out, err = decoded(res)
        fails.append("self-check of the same page should pass, got exit %s: %s"
                     % (res.returncode, (out + err)[:200]))


def _has_playwright():
    try:
        import playwright.sync_api  # noqa: F401
    except Exception:
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            b.close()
    except Exception:
        return False
    return True


def main():
    if Image is None:
        print("FAIL  Pillow 不可用，本套测试无法运行")
        return 1
    fails = []
    skipped = []
    tmp = tempfile.mkdtemp(prefix="sfd-visual-")
    tests = [test_identical_is_zero_diff, test_layout_change_is_hard,
             test_blank_candidate_is_hard, test_blank_candidate_survives_low_pixel_diff,
             test_blank_reference_is_hard, test_ink_shift_is_warn,
             test_size_mismatch_states_unmeasured_area, test_degenerate_crop_refuses_a_verdict,
             test_unknown_flag_fails_closed, test_missing_inputs_are_errors,
             test_missing_reference_does_not_open_a_browser, test_findings_are_readable_utf8,
             test_shot_and_check_roundtrip]
    for fn in tests:
        try:
            if fn(fails, tmp) == "SKIP":
                skipped.append(fn.__name__)
        except AssertionError as exc:
            fails.append(str(exc))
        except Exception as exc:
            fails.append("%s crashed: %s" % (fn.__name__, exc))
    shutil.rmtree(tmp, ignore_errors=True)
    for f in fails:
        print("FAIL  %s" % f)
    for s in skipped:
        print("SKIP  %s（本机 Playwright/Chromium 不可用，未实测）" % s)
    print("-" * 60)
    print("checks=%d failures=%d skipped=%d" % (len(tests), len(fails), len(skipped)))
    print("RESULT: PASS" if not fails else "RESULT: FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

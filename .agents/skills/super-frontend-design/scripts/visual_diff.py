#!/usr/bin/env python3
"""Reference-vs-output visual gate, plus blank-page detection. Stdlib + Pillow + numpy.

Closes the gap the skill claims but could not do: compare a generated page against
a reference image, and prove the page actually painted something. No npm, no cloud
service, no network.

Usage:
    python scripts/visual_diff.py shot <page.html> --out shot.png [--width 1440] [--height 900]
    python scripts/visual_diff.py diff <a.png> <b.png> [--max-diff 2.0] [--json]
    python scripts/visual_diff.py check <page.html> --reference ref.png [--max-diff 2.0]

Exit: 0 within threshold, 1 over threshold or blank page, 2 bad invocation / missing
dependency. A missing reference is reported, never treated as a pass.
"""

import argparse
import json
import sys
from pathlib import Path

# Windows 下 stdout 默认 gbk，中文结论会变乱码，门禁输出统一强制 UTF-8
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

SUBCOMMANDS = ("shot", "diff", "check")
TOLERANCE = 16          # per-channel difference still counted as "same"
BLANK_INK_FRACTION = 0.005   # <0.5% non-background pixels  ==>  nothing painted
INK_SHIFT_RATIO = 0.5   # 实测：纯白页 vs 设计稿的逐像素差只有 1.9%，靠墨量比才能兜住


class DiffError(Exception):
    pass


def require_imaging():
    try:
        from PIL import Image
        import numpy  # noqa: F401
        return Image, numpy
    except Exception as exc:
        raise DiffError("需要 Pillow + numpy（当前不可用）：%s" % exc)


def clean_path(value, what):
    """门禁路径契约：拒绝空值与 .. 段，展开 ~，产出规整后的 Path。

    本工具是本地 CLI，路径来自操作者本人；这道校验不是安全边界，
    而是把"手滑写出 ../ 相对层级"挡在读写盘之前，fail-closed 报错而非猜意图。
    """
    text = str(value).strip()
    if not text:
        raise DiffError("%s 路径不能为空" % what)
    p = Path(text).expanduser()
    if ".." in p.parts:
        raise DiffError("%s 路径不允许包含 .. 段（请传绝对路径或当前目录内相对路径）：%s" % (what, text))
    return p


def screenshot(html, out, width, height):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise DiffError("需要 Playwright（当前不可用）：%s" % exc)
    url = Path(html).resolve().as_uri()
    target = Path(out).resolve()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(400)
                page.screenshot(path=str(target), full_page=True)
            finally:
                browser.close()
    except Exception as exc:
        raise DiffError("截图失败：%s" % str(exc).strip().splitlines()[-1][:120])
    if not target.is_file():
        raise DiffError("截图没有产出文件：%s" % target)
    return str(target)


def compare(a_path, b_path, max_diff):
    Image, np = require_imaging()
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    findings = []
    metrics = {}
    w = min(a.width, b.width)
    h = min(a.height, b.height)
    if a.size != b.size:
        unmeasured = 100.0 * (1 - (w * h) / float(max(a.width * a.height, b.width * b.height)))
        findings.append(mk("size-mismatch", "warn", "%s vs %s（未比对面积 %.1f%%）" % (a.size, b.size, unmeasured), "同尺寸",
                           "两张图尺寸不同，只比较了公共区域，未比对部分没有结论（滚动高度差本身可能就是回归）"))
    if w < 40 or h < 40:
        findings.append(mk("degenerate-crop", "hard", "%dx%d" % (w, h), ">=40x40",
                           "可比区域太小，差异结论不成立"))
        return findings, metrics
    A = np.asarray(a.crop((0, 0, w, h)), dtype="int16")
    B = np.asarray(b.crop((0, 0, w, h)), dtype="int16")
    delta = np.abs(A - B)
    per_pixel = delta.max(axis=2)
    diff_pixels = int((per_pixel > TOLERANCE).sum())
    total = w * h
    metrics = {
        "compared": "%dx%d" % (w, h),
        "diff_pixels": diff_pixels,
        "diff_percent": round(diff_pixels * 100.0 / total, 3),
        "mean_abs_error": round(float(delta.mean()), 3),
        "worst_channel_gap": int(per_pixel.max()),
    }
    # 空白页与内容密度检查（check 模式下第二张图是生成页）
    ink = float((np.asarray(b.convert("L"), dtype="int16") < 245).mean())
    ref_ink = float((np.asarray(a.convert("L"), dtype="int16") < 245).mean())
    metrics["reference_ink_fraction"] = round(ref_ink, 4)
    metrics["candidate_ink_fraction"] = round(ink, 4)
    if ink < BLANK_INK_FRACTION:
        findings.append(mk("blank-candidate", "hard", "非白像素占比 %.4f" % ink,
                           ">=%.3f" % BLANK_INK_FRACTION, "生成页面近乎空白（白屏或渲染失败）"))
    elif ref_ink < BLANK_INK_FRACTION:
        findings.append(mk("blank-reference", "hard", "非白像素占比 %.4f" % ref_ink,
                           ">=%.3f" % BLANK_INK_FRACTION, "参考图本身是空白，比对无意义"))
    elif ref_ink >= BLANK_INK_FRACTION:
        shift = abs(ink - ref_ink) / ref_ink
        if shift > INK_SHIFT_RATIO:
            findings.append(mk("ink-fraction-shift", "warn",
                               "墨量 %.4f -> %.4f（变化 %.0f%%）" % (ref_ink, ink, shift * 100),
                               "变化 <= %.0f%%" % (INK_SHIFT_RATIO * 100),
                               "画面内容密度大幅变化，确认是否为预期改动（白底占比高的设计里逐像素差异会被低估）"))
    if metrics["diff_percent"] > max_diff:
        findings.append(mk("diff-over-threshold", "hard",
                           "%.3f%% 像素超容差(>%d)" % (metrics["diff_percent"], TOLERANCE),
                           "<=%.3f%%" % max_diff, "与参考图差异超阈值，需逐项复核"))
    return findings, metrics


def mk(rule, severity, measured, threshold, message):
    return {"rule": rule, "severity": severity, "measured": measured,
            "threshold": threshold, "message": message}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for a in argv:
        if a.startswith("-") and a.split("=")[0] not in {
                "--out", "--width", "--height", "--max-diff", "--json", "--reference", "--timeout"}:
            sys.stderr.write("ERROR  未知参数 %r\n" % a)
            return 2
    ap = argparse.ArgumentParser(prog="visual_diff.py", add_help=False, allow_abbrev=False)
    ap.add_argument("mode", nargs="?")
    ap.add_argument("inputs", nargs="*")
    ap.add_argument("--out", default="visual-shot.png")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--reference", default=None)
    ap.add_argument("--max-diff", type=float, default=2.0)
    ap.add_argument("--json", action="store_true")
    ns = ap.parse_args(argv)

    try:
        ns.out = str(clean_path(ns.out, "--out"))
        ns.inputs = [str(clean_path(x, "输入")) for x in ns.inputs]
        if ns.reference:
            ns.reference = str(clean_path(ns.reference, "--reference"))
    except DiffError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2

    if ns.mode not in SUBCOMMANDS:
        sys.stderr.write("ERROR  需要子命令之一: %s\n" % ", ".join(SUBCOMMANDS))
        return 2
    try:
        if ns.mode == "shot":
            if len(ns.inputs) != 1 or not Path(ns.inputs[0]).is_file():
                raise DiffError("shot 需要 1 个存在的 html 路径")
            out = screenshot(ns.inputs[0], ns.out, ns.width, ns.height)
            findings, metrics = [], {"shot": out}
        else:
            if ns.mode == "diff":
                if len(ns.inputs) != 2:
                    raise DiffError("diff 需要两个 png 路径")
                a, b = ns.inputs
            else:
                if len(ns.inputs) != 1 or not ns.reference:
                    raise DiffError("check 需要 <page.html> 与 --reference ref.png")
                if not Path(ns.inputs[0]).is_file():
                    raise DiffError("no such file: %s" % ns.inputs[0])
                a = ns.reference
                if not Path(a).is_file():
                    raise DiffError("参考图不存在：%s" % a)
                b = screenshot(ns.inputs[0], ns.out, ns.width, ns.height)
            for p in (a, b):
                if not Path(p).is_file():
                    raise DiffError("图片不存在：%s" % p)
            findings, metrics = compare(a, b, ns.max_diff)
    except DiffError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2

    hard = [x for x in findings if x["severity"] == "hard"]
    warn = [x for x in findings if x["severity"] == "warn"]
    if ns.json:
        print(json.dumps({"metrics": metrics, "hard": hard, "warn": warn}, ensure_ascii=False, indent=2))
    else:
        for k, v in metrics.items():
            print("  %-24s %s" % (k, v))
        for x in hard:
            print("FAIL  %-22s %s (measured %s / threshold %s)" % (x["rule"], x["message"], x["measured"], x["threshold"]))
        for x in warn:
            print("WARN  %-22s %s (%s)" % (x["rule"], x["message"], x["measured"]))
        print("-" * 64)
        print("RESULT: FAIL" if hard else "RESULT: PASS")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Contract tests for scripts/structure_lint.mjs — run with: python tests/test_structure_lint.py

This is the only gate that needs node + the project-local .sfd-tools install. When
either is missing the suite reports SKIP and exits 2: "跑不了" must never be read as
"通过". Everything it does assert is measured against the real tools, not a mock.
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
TOOL = SKILL / "scripts" / "structure_lint.mjs"
CLEAN = HERE / "slop_clean.html"
RED = HERE / "slop_red.html"
TOKEN_RED = HERE / "token_red.html"


def run(*args):
    return subprocess.run(["node", str(TOOL)] + [str(a) for a in args],
                          capture_output=True, cwd=str(SKILL))


def decoded(res):
    try:
        return res.stdout.decode("utf-8"), res.stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError("输出不是 UTF-8：%s" % exc)


def data(res):
    out, _ = decoded(res)
    return json.loads(out)


def tools_dir():
    d = os.environ.get("SFD_TOOLS")
    if d and (Path(d) / "node_modules" / "stylelint").is_dir():
        return d
    for p in [SKILL / "../../../.sfd-tools", Path.cwd() / ".sfd-tools"]:
        if (p / "node_modules" / "stylelint").is_dir():
            return str(p.resolve())
    return None


def node_available():
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except Exception:
        return False
    return True


def test_clean_fixture_passes(fails):
    res = run(CLEAN)
    out, err = decoded(res)
    if res.returncode != 0:
        fails.append("clean fixture must exit 0, got %s: %s" % (res.returncode, (out + err)[:300]))


def test_red_fixture_flags_markup(fails):
    res = run(RED, "--json")
    rules = {x["rule"] for x in data(res)["hard"]}
    for want in ("wcag/h37", "no-implicit-button-type"):
        if want not in rules:
            fails.append("red fixture must raise %s, got %s" % (want, sorted(rules)))


def test_hardcoded_color_is_flagged(fails, tmp):
    page = Path(tmp) / "inline-color.html"
    page.write_text("<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
                    "<style>.a{ color: #333; background: white; font-family: Inter; }</style>"
                    "</head><body><p class=\"a\">正文</p></body></html>", encoding="utf-8")
    d = data(run(page, "--json"))
    hits = [x for x in d["hard"] if x["rule"].endswith("declaration-strict-value")]
    if len(hits) < 3:
        fails.append("3 hardcoded values must be flagged, got %d" % len(hits))


def test_var_tokens_are_not_flagged(fails, tmp):
    page = Path(tmp) / "tokens.html"
    page.write_text("<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
                    "<style>:root{--color-ink:#101014}\n"
                    ".a{ color: var(--color-ink); border: 1px solid var(--color-ink);"
                    " outline: 2px solid var(--color-ink); }</style>"
                    "</head><body><p class=\"a\">正文</p></body></html>", encoding="utf-8")
    d = data(run(page, "--json"))
    wrong = [x for x in d["hard"] if x["rule"].endswith("declaration-strict-value")]
    if wrong:
        fails.append("var()-based declarations (incl. 1px solid var() shorthand) must not be flagged: %s"
                     % [(x["file"], x["line"]) for x in wrong])


def test_font_size_requires_token(fails, tmp):
    """字号纳入 strict-value：裸 px 字号必被抓，var() 字号放行。"""
    page = Path(tmp) / "font-size.html"
    page.write_text("<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
                    "<style>:root{--font-size-body:16px}"
                    ".hard{ font-size: 13px; } .ok{ font-size: var(--font-size-body); }</style>"
                    "</head><body><p class=\"hard\">甲</p><p class=\"ok\">乙</p></body></html>", encoding="utf-8")
    d = data(run(page, "--json"))
    hits = [x for x in d["hard"] if x["rule"].endswith("declaration-strict-value")]
    if len(hits) != 1:
        fails.append("exactly the bare 13px font-size must be flagged, got %d" % len(hits))


def test_unknown_property_and_bad_markup_are_flagged(fails, tmp):
    page = Path(tmp) / "typo.css"
    page.write_text(".a { colour: red; }\n", encoding="utf-8")
    if not any(x["rule"] == "property-no-unknown" for x in data(run(page, "--json"))["hard"]):
        fails.append("拼错的属性名 colour 必须被 property-no-unknown 抓到")
    bad = Path(tmp) / "dup-id.html"
    bad.write_text('<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">'
                   '<title>重复 id</title></head>'
                   '<body><div id="x"></div><div id="x"></div></body></html>', encoding="utf-8")
    if not any(x["rule"] == "no-dup-id" for x in data(run(bad, "--json"))["hard"]):
        fails.append("重复 id 必须被 html-validate 的 no-dup-id 抓到")


def test_inline_style_is_warn_not_hard(fails, tmp):
    """动态宽高写法在真实项目里是常规手段：降级为 warn，别把门禁淹没。"""
    page = Path(tmp) / "inline.html"
    page.write_text('<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"></head>'
                    '<body><div style="width:50%">半宽</div></body></html>', encoding="utf-8")
    d = data(run(page, "--json"))
    if any(x["rule"] == "no-inline-style" for x in d["hard"]):
        fails.append("no-inline-style must be downgraded to warn")
    if not any(x["rule"] == "no-inline-style" for x in d["warn"]):
        fails.append("no-inline-style should still be reported as warn")
    strict = run(page, "--strict")
    if strict.returncode != 1:
        fails.append("--strict must turn warns into failures, got %s" % strict.returncode)


def test_bad_invocation_exits_2(fails, tmp):
    page = Path(tmp) / "p.html"
    page.write_text('<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"></head>'
                    '<body><p>正文</p></body></html>', encoding="utf-8")
    for args in ((page, "--widhts", "320"), (page, "--only", "cssx"), (page, "--only", "css-html")):
        res = run(*args)
        out, err = decoded(res)
        if res.returncode == 0 or "PASS" in out:
            fails.append("%s 必须非 0 退出（现在 exit %s）" % (" ".join(str(a) for a in args), res.returncode))
    if run(str(page), "--only", "css").returncode not in (0, 1):
        fails.append("--only css 是合法取值，不该报错")
    empty = Path(tmp) / "empty"
    empty.mkdir()
    if run(empty).returncode != 2:
        fails.append("扫空目录必须 exit 2")
    if run(str(Path(tmp) / "gone.html")).returncode != 2:
        fails.append("路径不存在必须 exit 2")


def test_missing_tools_dir_is_an_error(fails, tmp):
    empty = Path(tmp) / "notools"
    empty.mkdir()
    res = run(str(CLEAN), "--tools", str(empty))
    out, err = decoded(res)
    if res.returncode != 2 or not any(k in err for k in ("--tools 指向", "找不到结构层依赖")):
        fails.append("--tools 指错必须 exit 2 并说明，got exit %s: %s" % (res.returncode, (out + err)[:160]))


def test_misconfigured_rule_is_not_a_green_light(fails, tmp):
    """我配错规则名时，绝不能变成"扫过了、没问题"。"""
    cfg = Path(tmp) / "stylelint.config.json"
    real = json.loads((SKILL / "rules" / "stylelint.config.json").read_bytes().decode("utf-8"))
    real["rules"]["no-such-rule-xyz"] = True
    cfg.write_text(json.dumps(real), encoding="utf-8")
    backup = SKILL / "rules" / "stylelint.config.json"
    original = backup.read_bytes()
    try:
        backup.write_bytes(cfg.read_bytes())
        res = run(str(CLEAN))
        out, err = decoded(res)
        if res.returncode != 2 or not any(k in err for k in ("stylelint 配置无效", "stylelint 配置里有不存在的规则")):
            fails.append("无效规则名必须 exit 2，got exit %s: %s" % (res.returncode, (out + err)[:160]))
    finally:
        backup.write_bytes(original)


def main():
    tests_needs = 10
    if not node_available() or not tools_dir():
        print("SKIP  node 或 .sfd-tools 结构层不可用，structure_lint 的 %d 项契约测试未实测" % tests_needs)
        print("-" * 60)
        print("checks=0 failures=0 skipped=%d" % tests_needs)
        print("RESULT: SKIP（未实测，不作为通过证据）")
        return 2
    fails = []
    tmp = Path(tempfile.mkdtemp(prefix="sfd-structure-"))
    simple = [test_clean_fixture_passes, test_red_fixture_flags_markup]
    with_tmp = [test_hardcoded_color_is_flagged, test_var_tokens_are_not_flagged,
                test_font_size_requires_token,
                test_unknown_property_and_bad_markup_are_flagged,
                test_inline_style_is_warn_not_hard, test_bad_invocation_exits_2,
                test_missing_tools_dir_is_an_error, test_misconfigured_rule_is_not_a_green_light]
    for fn in simple:
        try:
            fn(fails)
        except AssertionError as exc:
            fails.append(str(exc))
        except Exception as exc:
            fails.append("%s crashed: %s" % (fn.__name__, exc))
    for fn in with_tmp:
        try:
            fn(fails, tmp)
        except AssertionError as exc:
            fails.append(str(exc))
        except Exception as exc:
            fails.append("%s crashed: %s" % (fn.__name__, exc))
    shutil.rmtree(tmp, ignore_errors=True)
    for f in fails:
        print("FAIL  %s" % f)
    print("-" * 60)
    print("checks=%d failures=%d" % (len(simple) + len(with_tmp), len(fails)))
    print("RESULT: PASS" if not fails else "RESULT: FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

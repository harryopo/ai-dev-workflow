#!/usr/bin/env python3
"""Contract tests for scripts/token_lint.py — run with: python tests/test_token_lint.py

Every assertion here is a promise the linter makes to the workflow. The inline
declaration case and the `---` front-matter case are regressions found by running
the linter against its own fixtures: a one-line `:root { --a: 1; }` was reported
as "token never defined", and the front-matter fence was collected as a token name.
"""

import json
import os
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
LINTER = SKILL / "scripts" / "token_lint.py"
CLEAN = HERE / "token_clean.css"
RED = HERE / "token_red.html"
CONTRACT = HERE / "design_contract.md"


def run(*args):
    """Run without PYTHONIOENCODING: the script itself must force UTF-8 stdout."""
    env = dict(os.environ)
    env.pop("PYTHONIOENCODING", None)
    return subprocess.run([sys.executable, str(LINTER)] + list(args),
                          capture_output=True, env=env)


def decoded(res):
    try:
        return res.stdout.decode("utf-8"), res.stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError("输出不是 UTF-8（Windows 下退回 gbk 会乱码）：%s" % exc)


def data(res):
    out, _ = decoded(res)
    return json.loads(out)


def names(findings):
    return {(x["rule"], x["measured"]) for x in findings}


def test_clean_is_silent(fails):
    res = run(str(CLEAN), "--strict")
    if res.returncode != 0:
        out, err = decoded(res)
        fails.append("clean css must exit 0, got %s: %s" % (res.returncode, (out + err)[:300]))


def test_inline_declaration_is_not_undefined(fails):
    """`:root { --ink: …; }` on one line is the shape AI-generated pages actually use."""
    res = run(str(RED), "--json")
    hard = data(res)["hard"]
    bad = [x["measured"] for x in hard
           if x["rule"] == "undefined-token" and x["measured"] in ("--ink", "--radius-card")]
    if bad:
        fails.append("token declared on the same line as :root was reported undefined: %s" % bad)


def test_undefined_without_fallback_is_hard(fails):
    res = run(str(RED), "--json")
    if ("undefined-token", "--radius-missing-here") not in names(data(res)["hard"]):
        fails.append("an undefined token with no fallback must be a hard finding")


def test_undefined_with_fallback_is_warn_only(fails):
    res = run(str(RED), "--json")
    d = data(res)
    if ("undefined-with-fallback", "--surface") not in names(d["warn"]):
        fails.append("an undefined token that has a fallback must be reported as warn")
    if any(x["measured"] == "--surface" for x in d["hard"]):
        fails.append("--surface has a fallback, it must not be a hard finding")


def test_dead_token_is_attributed_to_its_own_file(fails):
    res = run(str(CLEAN), str(RED), "--json")
    dead = [x for x in data(res)["warn"] if x["rule"] == "dead-token"]
    if not dead:
        fails.append("expected at least one dead token (--radius-card)")
        return
    wrong = [x["measured"] for x in dead if not x["file"].endswith(str(RED.name))]
    if wrong:
        fails.append("dead-token blamed the first argument instead of the declaring file: %s" % wrong)


def test_contract_missing_token_is_hard(fails):
    res = run(str(CLEAN), "--design", str(CONTRACT), "--json")
    if ("contract-token-missing", "--ghost-token") not in names(data(res)["hard"]):
        fails.append("DESIGN.md front-matter token absent from code must be hard")


def test_contract_documented_tokens_are_not_undocumented(fails):
    res = run(str(CLEAN), "--design", str(CONTRACT), "--json")
    flagged = [x["measured"] for x in data(res)["warn"]
               if x["rule"] == "undocumented-token"]
    if set(flagged) & {"--color-ink", "--space-4"}:
        fails.append("tokens present in both code and contract were called undocumented: %s" % flagged)


def test_code_token_absent_from_contract_is_warn(fails):
    res = run(str(RED), "--design", str(CONTRACT), "--json")
    if ("undocumented-token", "--ink") not in names(data(res)["warn"]):
        fails.append("--ink is used in code but not in the contract; must warn")


def test_front_matter_fence_is_never_a_token(fails):
    res = run(str(CLEAN), "--design", str(CONTRACT), "--json")
    d = data(res)
    fences = [x["measured"] for x in d["hard"] + d["warn"]
              if not x["measured"].startswith("--") or x["measured"].startswith("---")]
    if fences:
        fails.append("non-token values were reported as tokens: %s" % fences)


def test_empty_input_is_not_a_pass(fails):
    tmp = Path(tempfile.mkdtemp())
    res = run(str(tmp))
    if res.returncode != 2:
        fails.append("scanning a dir with no css/html must exit 2, got %s" % res.returncode)


def test_unknown_flag_fails_closed(fails):
    res = run(str(CLEAN), "--desig", str(CONTRACT))
    out, _ = decoded(res)
    if res.returncode == 0 or "PASS" in out:
        fails.append("a typo'd flag must not silently scan and print PASS (exit %s)" % res.returncode)


def test_findings_are_readable_utf8(fails):
    res = run(str(RED))
    out, _ = decoded(res)
    if "从未定义" not in out:
        fails.append("expected Chinese finding text to survive; got %r" % out[:120])


def main():
    fails = []
    for fn in (test_clean_is_silent, test_inline_declaration_is_not_undefined,
               test_undefined_without_fallback_is_hard, test_undefined_with_fallback_is_warn_only,
               test_dead_token_is_attributed_to_its_own_file, test_contract_missing_token_is_hard,
               test_contract_documented_tokens_are_not_undocumented,
               test_code_token_absent_from_contract_is_warn,
               test_front_matter_fence_is_never_a_token, test_empty_input_is_not_a_pass,
               test_unknown_flag_fails_closed, test_findings_are_readable_utf8):
        try:
            fn(fails)
        except AssertionError as exc:
            fails.append(str(exc))
        except Exception as exc:
            fails.append("%s crashed: %s" % (fn.__name__, exc))
    for f in fails:
        print("FAIL  %s" % f)
    print("-" * 60)
    print("checks=%d failures=%d" % (12, len(fails)))
    print("RESULT: PASS" if not fails else "RESULT: FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

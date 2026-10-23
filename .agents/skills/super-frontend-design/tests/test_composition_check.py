#!/usr/bin/env python3
"""Contract tests for scripts/composition_check.py.

This script backs review check #13 -- whether the page was actually built as
the macrostructure it claims. The script can only verify the *declaration*;
the tests therefore attack the false-pass direction:

1. a file with no contract markers must FAIL (not "clean because nothing found")
2. a contract missing any of the six elements must FAIL
3. an invalid focus-hierarchy value must FAIL
4. an empty element value must FAIL
5. contract markers without a macrostructure stamp must FAIL
6. a stamp whose macrostructure does not match the required one must FAIL
7. a complete, valid contract must PASS
8. scanning zero files must exit 2 (empty scan is not a verdict)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1] if len(sys.argv) > 1 else
              Path(__file__).resolve().parent.parent / "scripts/composition_check.py").resolve()

checks = 0
failures = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if cond:
        print("PASS  %s" % name)
    else:
        print("FAIL  %s %s" % (name, detail))
        failures.append(name)


def run(args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True, encoding="utf-8", cwd=cwd)


VALID = """/* macrostructure: 01·Bento Grid · theme: Tally · genre: SaaS */
/* composition: heading-anchor=各模块内 */
/* composition: body-columns=多栏不对称 */
/* composition: divider=负间距/留白 */
/* composition: imagery=混合（部分模块有图，部分无图） */
/* composition: entrance=stagger fade-up */
/* composition: focus-hierarchy=2 */
.bento { display: grid; }
"""

MISSING_ONE = """/* macrostructure: 01·Bento Grid · theme: Tally · genre: SaaS */
/* composition: heading-anchor=各模块内 */
/* composition: body-columns=多栏不对称 */
/* composition: divider=负间距/留白 */
/* composition: imagery=混合 */
/* composition: entrance=stagger fade-up */
.bento { display: grid; }
"""

NO_STAMP = """/* composition: heading-anchor=各模块内 */
/* composition: body-columns=多栏不对称 */
/* composition: divider=负间距/留白 */
/* composition: imagery=混合 */
/* composition: entrance=stagger fade-up */
/* composition: focus-hierarchy=2 */
.bento { display: grid; }
"""

BAD_FOCUS = """/* macrostructure: 04·Stat-Led · theme: Tally · genre: SaaS */
/* composition: heading-anchor=巨大数字 */
/* composition: body-columns=支撑性文字 */
/* composition: divider=hairline rule */
/* composition: imagery=支撑性图表 */
/* composition: entrance=Number Counter动画 */
/* composition: focus-hierarchy=9 */
.stat { font-size: 4rem; }
"""

EMPTY_VALUE = """/* macrostructure: 05·Workbench · theme: Tally · genre: SaaS */
/* composition: heading-anchor=每屏顶部小标题 */
/* composition: body-columns= */
/* composition: divider=negative space */
/* composition: imagery=产品截图 */
/* composition: entrance=fade-up stagger */
/* composition: focus-hierarchy=2 */
.work { }
"""

NO_CONTRACT = """/* macrostructure: 05·Workbench · theme: Tally · genre: SaaS */
.work { display: grid; }
"""


def write(tmp, name, content):
    p = Path(tmp) / name
    p.write_text(content, encoding="utf-8")
    return p


def main():
    with tempfile.TemporaryDirectory() as tmp:
        valid = write(tmp, "valid.css", VALID)
        missing = write(tmp, "missing.css", MISSING_ONE)
        nostamp = write(tmp, "nostamp.css", NO_STAMP)
        badfocus = write(tmp, "badfocus.css", BAD_FOCUS)
        emptyval = write(tmp, "emptyval.css", EMPTY_VALUE)
        nocontract = write(tmp, "nocontract.css", NO_CONTRACT)

        r = run([str(valid)])
        check("valid-contract-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(missing)])
        check("missing-field-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("missing-field-reports-rule",
              "composition-fields-missing" in r.stdout, r.stdout[-300:])

        r = run([str(nostamp)])
        check("no-stamp-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("no-stamp-reports-rule",
              "composition-without-stamp" in r.stdout, r.stdout[-300:])

        r = run([str(badfocus)])
        check("invalid-focus-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("invalid-focus-reports-rule",
              "composition-focus-invalid" in r.stdout, r.stdout[-300:])

        r = run([str(emptyval)])
        check("empty-value-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("empty-value-reports-rule",
              "composition-field-empty" in r.stdout, r.stdout[-300:])

        r = run([str(nocontract)])
        check("no-contract-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("no-contract-reports-rule",
              "composition-absent" in r.stdout, r.stdout[-300:])

        r = run([str(valid), "--require-macrostructure", "Bento Grid"])
        check("matching-macrostructure-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(valid), "--require-macrostructure", "Stat-Led"])
        check("mismatched-macrostructure-fails", r.returncode == 1,
              "exit=%s" % r.returncode)
        check("mismatch-reports-rule",
              "macrostructure-mismatch" in r.stdout, r.stdout[-300:])

        empty = Path(tmp) / "empty"
        empty.mkdir()
        r = run([str(empty)])
        check("empty-scan-exits-2", r.returncode == 2, "exit=%s" % r.returncode)

        r = run([str(Path(tmp) / "nope.css")])
        check("missing-path-exits-2", r.returncode == 2, "exit=%s" % r.returncode)

        r = run([str(valid), "--json"])
        check("json-output-parses", r.returncode == 0 and '"fields"' in r.stdout,
              "exit=%s" % r.returncode)

    print("-" * 60)
    print("checks=%d failures=%d" % (checks, len(failures)))
    print("RESULT: PASS" if not failures else "RESULT: FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Negative control for scripts/audit_integrity.py.

Copies the skill to a scratch dir, injects one known defect at a time (15 cases:
14 injected defects plus one bad-flag rejection), and requires the gate to fail
with the expected check name. A gate that cannot go
red is not measuring anything.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent).resolve()
SCRATCH = Path(sys.argv[2]) if len(sys.argv) > 2 else (
    Path(tempfile.gettempdir()) / ("sfd-gate-red-" + os.environ.get("USER", "x")))

# (name, mutation function, expected check id in output)
CASES = [
    ("stale-rule-count",
     lambda d: (d / "subskills/critique/SKILL.md").write_text(
         (d / "subskills/critique/SKILL.md").read_text(encoding="utf-8")
         .replace("26条确定性探测器", "59条确定性探测器"), encoding="utf-8"),
     "subskill-claim"),
    ("missing-referenced-file",
     lambda d: (d / "references/typography.md").unlink(),
     "broken-reference"),
    ("unbalanced-fence",
     lambda d: (d / "SKILL.md").write_text(
         (d / "SKILL.md").read_text(encoding="utf-8") + "\n``` dangling\n",
         encoding="utf-8"),
     "fence-unbalanced"),
    ("wrong-stack-count",
     lambda d: (d / "subskills/design/SKILL.md").write_text(
         (d / "subskills/design/SKILL.md").read_text(encoding="utf-8")
         .replace("技术栈（14 栈）", "技术栈（10 栈）"), encoding="utf-8"),
     "part-claim"),
    ("stale-checklist-total",
     lambda d: (d / "references/slop-test.md").write_text(
         (d / "references/slop-test.md").read_text(encoding="utf-8")
         .replace("/56", "/57"), encoding="utf-8"),
     "stale-total"),
    ("bogus-flag-must-not-scan-quietly",
     None,
     "unknown flag"),
    ("stale-slop-test-quote",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("56条Slop Test", "59条Slop Test"), encoding="utf-8"),
     "cross-claim"),
    ("stale-rule-table-count",
     lambda d: (d / "SKILL.md").write_text(
         (d / "SKILL.md").read_text(encoding="utf-8")
         .replace("30 条规则", "31 条规则", 1), encoding="utf-8"),
     "cross-claim"),
    ("layer-table-does-not-add-up",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("| 特殊规则（V50-V56） | 7 |", "| 特殊规则（V50-V56） | 5 |"),
         encoding="utf-8"),
     "layer-sum"),
    ("gate-points-at-missing-script",
     lambda d: (d / "rules/gates.json").write_text(
         (d / "rules/gates.json").read_text(encoding="utf-8")
         .replace("scripts/token_lint.py", "scripts/token_lint_renamed.py", 1),
         encoding="utf-8"),
     "gate-inventory"),
    ("gate-count-claim-drift",
     lambda d: (d / "SKILL.md").write_text(
         (d / "SKILL.md").read_text(encoding="utf-8")
         .replace("交付前跑六道门禁", "交付前跑三道门禁", 1), encoding="utf-8"),
     "gate-inventory"),
    ("policy-prose-number-drift",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("首屏强调色使用面积 ≤ 5%", "首屏强调色使用面积 ≤ 12%"), encoding="utf-8"),
     "policy-consistency"),
    ("policy-gate-threshold-drift",
     lambda d: (d / "rules/policy.json").write_text(
         (d / "rules/policy.json").read_text(encoding="utf-8")
         .replace('"value": 3,\n      "also_allowed": [2]',
                  '"value": 4,\n      "also_allowed": [2]', 1),
         encoding="utf-8"),
     "policy-consistency"),
    ("subskill-declares-own-version",
     lambda d: (d / "subskills/research/SKILL.md").write_text(
         (d / "subskills/research/SKILL.md").read_text(encoding="utf-8")
         .replace("name: super-frontend-design:research\n",
                  "name: super-frontend-design:research\nversion: 2.7.0\n", 1),
         encoding="utf-8"),
     "version-field"),
    ("evals-version-lags-skill",
     lambda d: (d / "evals/evals.json").write_text(
         (d / "evals/evals.json").read_text(encoding="utf-8")
         .replace('"version": "2.9.1"', '"version": "2.7.0"', 1),
         encoding="utf-8"),
     "version-field"),
]


def fresh_copy():
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    shutil.copytree(SKILL, SCRATCH)


def main():
    if not (SKILL / "scripts/audit_integrity.py").exists():
        sys.stderr.write("pass the skill directory as arg 1\n")
        return 2
    failures = []
    for name, mutate, expect in CASES:
        if mutate is None:
            r = subprocess.run([sys.executable, str(SKILL / "scripts/audit_integrity.py"),
                                "--skill-drr", str(SKILL)],
                               capture_output=True, text=True)
            ok = r.returncode == 2 and "unknown flag" in (r.stderr + r.stdout)
            print("%-34s exit=%s -> %s" % (name, r.returncode, "OK" if ok else "MISMATCH"))
            if not ok:
                failures.append(name + " (fail-closed on bad flag)")
            continue
        fresh_copy()
        mutate(SCRATCH)
        r = subprocess.run([sys.executable, str(SCRATCH / "scripts/audit_integrity.py"),
                            "--skill-dir", str(SCRATCH)],
                           capture_output=True, text=True, encoding="utf-8")
        hit = expect in (r.stdout or "")
        print("%-34s exit=%s expects[%s] -> %s"
              % (name, r.returncode, expect, "OK" if (r.returncode == 1 and hit) else "MISMATCH"))
        if not (r.returncode == 1 and hit):
            failures.append(name)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    print("-" * 56)
    print("RESULT: FAIL %s" % failures if failures else "RESULT: PASS all mutations detected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

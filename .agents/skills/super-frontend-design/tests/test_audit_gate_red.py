#!/usr/bin/env python3
"""Negative control for scripts/audit_integrity.py.

Copies the skill to a scratch dir, injects one known defect at a time (18 cases:
17 injected defects plus one bad-flag rejection), and requires the gate to fail
with the expected check name. A gate that cannot go
red is not measuring anything.
"""

import os
import re
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
         re.sub(r"交付前跑[一二三四五六七八九十]+道门禁", "交付前跑三道门禁",
                (d / "SKILL.md").read_text(encoding="utf-8"), count=1), encoding="utf-8"),
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
         re.sub(r'"version":\s*"[\d.]+"', '"version": "0.0.0"',
                (d / "evals/evals.json").read_text(encoding="utf-8"), count=1),
         encoding="utf-8"),
     "version-field"),
    ("phase2-divergence-removed",
     lambda d: (d / "subskills/creative/SKILL.md").write_text(
         (d / "subskills/creative/SKILL.md").read_text(encoding="utf-8")
         .replace("方向发散", "单方向"), encoding="utf-8"),
     "phase2-wiring"),
    ("phase2-second-order-removed",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("二阶反射", "一阶"), encoding="utf-8"),
     "phase2-wiring"),
    ("phase2-random-faked",
     lambda d: (d / "scripts/random_draw.py").write_text(
         (d / "scripts/random_draw.py").read_text(encoding="utf-8")
         .replace("os.urandom(4)", "random.randrange(4)"), encoding="utf-8"),
     "phase2-wiring"),
    ("phase3-signature-mining-removed",
     lambda d: (d / "subskills/research/SKILL.md").write_text(
         (d / "subskills/research/SKILL.md").read_text(encoding="utf-8")
         .replace("签名线索", "灵感来源"), encoding="utf-8"),
     "phase3-wiring"),
    ("phase3-signature-landing-removed",
     lambda d: (d / "subskills/design/SKILL.md").write_text(
         (d / "subskills/design/SKILL.md").read_text(encoding="utf-8")
         .replace("签名落地", "风格统一"), encoding="utf-8"),
     "phase3-wiring"),
    ("phase3-signature-review-removed",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("签名可识别性", "整体观感"), encoding="utf-8"),
     "phase3-wiring"),
    ("phase3-signature-checker-gutted",
     lambda d: (d / "scripts/signature_check.py").write_text(
         (d / "scripts/signature_check.py").read_text(encoding="utf-8")
         .replace("signature-landing-missing", "signature-note"), encoding="utf-8"),
     "phase3-wiring"),
    ("phase3-soul-question-orphan-again",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("灵魂验证问题", "标准出处"), encoding="utf-8"),
     "phase3-wiring"),
    ("phase4-composition-contract-removed",
     lambda d: (d / "references/composition-contract.md").unlink(),
     "phase4-wiring"),
    ("phase4-composition-landing-removed",
     lambda d: (d / "subskills/design/SKILL.md").write_text(
         (d / "subskills/design/SKILL.md").read_text(encoding="utf-8")
         .replace("构图契约落地", "风格统一"), encoding="utf-8"),
     "phase4-wiring"),
    ("phase4-focus-hierarchy-removed",
     lambda d: (d / "subskills/design/SKILL.md").write_text(
         (d / "subskills/design/SKILL.md").read_text(encoding="utf-8")
         .replace("focus-hierarchy", "visual-level"), encoding="utf-8"),
     "phase4-wiring"),
    ("phase4-composition-review-removed",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("构图契约一致性", "整体观感"), encoding="utf-8"),
     "phase4-wiring"),
    ("phase4-composition-checker-gutted",
     lambda d: (d / "scripts/composition_check.py").write_text(
         (d / "scripts/composition_check.py").read_text(encoding="utf-8")
         .replace("composition-fields-missing", "composition-note"), encoding="utf-8"),
     "phase4-wiring"),
    ("phase4-composition-stamp-rule-gutted",
     lambda d: (d / "scripts/composition_check.py").write_text(
         (d / "scripts/composition_check.py").read_text(encoding="utf-8")
         .replace("composition-without-stamp", "composition-stamp-note"), encoding="utf-8"),
     "phase4-wiring"),
    ("phase4-composition-absent-downgraded-to-warn",
     lambda d: (d / "scripts/composition_check.py").write_text(
         re.sub(r"if not total_fields:\s*\n(\s*)hard\.append",
                r"if not total_fields:\n\1warn.append",
                (d / "scripts/composition_check.py").read_text(encoding="utf-8"),
                count=1), encoding="utf-8"),
     "phase4-wiring"),
    ("phase5-state-contract-removed",
     lambda d: (d / "references/state-contract.md").unlink(),
     "phase5-wiring"),
    ("phase5-complexity-field-removed",
     lambda d: (d / "subskills/research/SKILL.md").write_text(
         (d / "subskills/research/SKILL.md").read_text(encoding="utf-8")
         .replace("interaction-complexity", "interaction-level"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-state-landing-removed",
     lambda d: (d / "subskills/design/SKILL.md").write_text(
         (d / "subskills/design/SKILL.md").read_text(encoding="utf-8")
         .replace("状态契约落地", "风格统一"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-state-review-removed",
     lambda d: (d / "subskills/review/SKILL.md").write_text(
         (d / "subskills/review/SKILL.md").read_text(encoding="utf-8")
         .replace("状态覆盖完整性", "整体观感"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-state-checker-gutted",
     lambda d: (d / "scripts/state_check.py").write_text(
         (d / "scripts/state_check.py").read_text(encoding="utf-8")
         .replace("state-declared-not-landed", "state-note"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-required-rule-gutted",
     lambda d: (d / "scripts/state_check.py").write_text(
         (d / "scripts/state_check.py").read_text(encoding="utf-8")
         .replace("state-required-missing", "state-note"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-static-exemption-removed",
     lambda d: (d / "scripts/state_check.py").write_text(
         (d / "scripts/state_check.py").read_text(encoding="utf-8")
         .replace('complexity == "static"', "False"), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-state-absent-gutted",
     lambda d: (d / "scripts/state_check.py").write_text(
         (d / "scripts/state_check.py").read_text(encoding="utf-8")
         .replace('"rule": "state-absent",', '"rule": "state-absent-note",'), encoding="utf-8"),
     "phase5-wiring"),
    ("phase5-complexity-tier-gutted",
     lambda d: (d / "scripts/state_check.py").write_text(
         (d / "scripts/state_check.py").read_text(encoding="utf-8")
         .replace('"complex": {', '"complex-x": {'), encoding="utf-8"),
     "phase5-wiring"),
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

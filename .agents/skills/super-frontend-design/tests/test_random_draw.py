#!/usr/bin/env python3
"""Contract tests for scripts/random_draw.py.

The value of this script is that the randomness is REAL. These tests guard the
properties that make it trustworthy:

1. the draw actually varies across many runs (not a constant "random")
2. every candidate can win (no candidate is unreachable)
3. duplicates do not get double probability
4. fewer than 2 candidates is a hard error, not a silent pick
5. the audit trail carries every field the skill tells the model to show

The draw() function is imported directly for the statistical checks (spawning
a subprocess per draw costs ~1s each and makes the suite unusably slow); the
CLI contract is checked through a handful of real subprocess invocations.
"""

import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

SCRIPT = Path(sys.argv[1] if len(sys.argv) > 1 else
              Path(__file__).resolve().parent.parent / "scripts/random_draw.py").resolve()

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


def load_module():
    spec = importlib.util.spec_from_file_location("random_draw", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True, encoding="utf-8")


def main():
    if not SCRIPT.exists():
        sys.stderr.write("script not found: %s\n" % SCRIPT)
        return 2

    rd = load_module()

    # 1. the draw actually varies
    picks = {rd.draw(["a", "b", "c"])[0] for _ in range(200)}
    check("draw-varies", len(picks) > 1, "always picked %r" % picks)

    # 2. every candidate is reachable, and roughly fair
    counts = Counter(rd.draw(["alpha", "beta", "gamma"])[0] for _ in range(3000))
    check("all-candidates-reachable",
          set(counts) == {"alpha", "beta", "gamma"},
          "saw %r" % dict(counts))
    # fair draw over 3 candidates with n=3000 has sd ~22; slack to 3 sd
    spread = max(counts.values()) - min(counts.values())
    check("no-candidate-starved", spread < 120,
          "spread=%d counts=%r" % (spread, dict(counts)))

    # 3. duplicates collapse (no double probability) — CLI level
    r = run(["--json", "only", "only", "other"])
    data = json.loads(r.stdout)
    check("duplicates-collapsed", data["candidates"] == ["only", "other"],
          "got %r" % data["candidates"])

    # 4. single candidate is a hard error
    r = run(["only"])
    check("single-candidate-rejected", r.returncode == 2, "exit=%s" % r.returncode)
    check("single-candidate-explains", "至少 2 个候选" in (r.stdout + r.stderr),
          "stderr=%r" % r.stderr.strip())

    # 5. audit trail completeness
    r = run(["--json", "a", "b"])
    data = json.loads(r.stdout)
    for field in ("candidates", "selected", "entropy_source", "entropy_hex", "timestamp_utc"):
        check("trail-has-%s" % field, field in data and data[field],
              "missing %r" % field)
    check("entropy-hex-length", len(data.get("entropy_hex", "")) == 8,
          "entropy_hex=%r" % data.get("entropy_hex"))

    # 6. selected must be one of the candidates
    check("selected-in-candidates", data["selected"] in data["candidates"],
          "%r not in %r" % (data["selected"], data["candidates"]))

    # 7. plain-text mode still prints the pick
    r = run(["x", "y"])
    check("text-mode-shows-pick", "抽中：" in r.stdout, "stdout=%r" % r.stdout[:120])

    # 8. the entropy source really is os.urandom, not a pseudo-random stand-in
    src = SCRIPT.read_text(encoding="utf-8")
    check("uses-os-urandom", "os.urandom(" in src, "no os.urandom call found")
    check("no-weak-random", "random.choice" not in src and "random.randint" not in src,
          "uses non-cryptographic random")

    print("-" * 56)
    print("checks=%d failures=%d" % (checks, len(failures)))
    print("RESULT: FAIL %s" % failures if failures else "RESULT: PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

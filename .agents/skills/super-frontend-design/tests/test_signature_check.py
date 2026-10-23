#!/usr/bin/env python3
"""Contract tests for scripts/signature_check.py.

This script backs review check #12 -- the only positive check in the table.
If it can silently pass a template, the skill's whole "20% unique choice"
mechanism is theatre. The tests therefore attack the *false pass* direction:

1. a file with no signature marker must FAIL (not "clean because nothing found")
2. a marker buried in a footer must FAIL (invisible == absent)
3. a marker in the hero must PASS
4. a marker that does not match the required signature text must FAIL
5. scanning zero files must exit 2 (empty scan is not a verdict)
6. the checker must not count its own example comments as a landing
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1] if len(sys.argv) > 1 else
              Path(__file__).resolve().parent.parent / "scripts/signature_check.py").resolve()

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


HERO = """<!doctype html>
<html><body>
  <section class="hero">
    <h1>数据中台</h1>
    <!-- signature: 术语等宽独立成版式单元 -->
    <code class="term">hotspot</code>
  </section>
  <footer>© 2026 Example Corp. All rights reserved.</footer>
</body></html>
"""

NO_SIGNATURE = """<!doctype html>
<html><body>
  <section class="hero"><h1>数据中台</h1><p>hello</p></section>
  <footer>© 2026 Example Corp. All rights reserved.</footer>
</body></html>
"""

FOOTER_ONLY = """<!doctype html>
<html><body>
  <section class="hero"><h1>数据中台</h1></section>
  <footer>
    <!-- signature: 术语等宽独立成版式单元 -->
    © 2026 Example Corp. All rights reserved.
  </footer>
</body></html>
"""

CSS_SIGNATURE = """.term {
  font-family: var(--font-mono);
  /* signature: 术语等宽独立成版式单元 */
  letter-spacing: var(--tracking-term);
}
"""

SELF_REFERENCING = """<!doctype html>
<html><body>
  <!-- 这是一个示例：/* signature: 假签名 */ -->
  <p>no real marker here</p>
</body></html>
"""


def write(tmp, name, content):
    p = Path(tmp) / name
    p.write_text(content, encoding="utf-8")
    return p


def main():
    with tempfile.TemporaryDirectory() as tmp:
        hero = write(tmp, "hero.html", HERO)
        nosig = write(tmp, "nosig.html", NO_SIGNATURE)
        footer = write(tmp, "footer.html", FOOTER_ONLY)
        css = write(tmp, "style.css", CSS_SIGNATURE)
        selfref = write(tmp, "self.html", SELF_REFERENCING)

        r = run([str(hero)])
        check("hero-marker-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(nosig)])
        check("missing-marker-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("missing-marker-reports-rule",
              "signature-landing-missing" in r.stdout, r.stdout[-300:])

        r = run([str(footer)])
        check("footer-only-marker-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("footer-only-reports-invisible",
              "signature-landing-invisible" in r.stdout, r.stdout[-300:])

        r = run([str(css)])
        check("css-marker-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(hero), "--require-marker", "术语等宽"])
        check("matching-require-marker-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(hero), "--require-marker", "完全不相关的签名"])
        check("mismatched-require-marker-fails", r.returncode == 1,
              "exit=%s" % r.returncode)
        check("mismatch-reports-rule",
              "signature-marker-mismatch" in r.stdout, r.stdout[-300:])

        r = run([str(selfref)])
        check("nested-comment-not-counted", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        empty = Path(tmp) / "empty"
        empty.mkdir()
        r = run([str(empty)])
        check("empty-scan-exits-2", r.returncode == 2, "exit=%s" % r.returncode)

        r = run([str(Path(tmp) / "does-not-exist.html")])
        check("missing-path-exits-2", r.returncode == 2, "exit=%s" % r.returncode)

        r = run([str(hero), "--min", "0"])
        check("min-zero-rejected", r.returncode == 2, "exit=%s" % r.returncode)

        r = run([str(hero), "--json"])
        check("json-output-parses", r.returncode == 0 and '"markers"' in r.stdout,
              "exit=%s" % r.returncode)

        # 目录扫描：存在 index.html 但首页无签名 → 必须失败
        dir_a = Path(tmp) / "case_a"
        dir_a.mkdir()
        write(dir_a, "index.html", NO_SIGNATURE)
        write(dir_a, "about.html", HERO)
        r = run([str(dir_a)])
        check("dir-scan-detects-missing-entry", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("entry-missing-reports-rule",
              "signature-entry-missing" in r.stdout, r.stdout[-300:])

        # 目录扫描：index.html 带签名 → 通过
        dir_b = Path(tmp) / "case_b"
        dir_b.mkdir()
        write(dir_b, "index.html", HERO)
        write(dir_b, "about.html", NO_SIGNATURE)
        r = run([str(dir_b)])
        check("dir-scan-passes-with-entry", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-400:]))

    print("-" * 60)
    print("checks=%d failures=%d" % (checks, len(failures)))
    print("RESULT: PASS" if not failures else "RESULT: FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Contract tests for scripts/state_check.py.

This script backs review check #14 -- whether the page actually handles the
states it declares. The tests attack the false-pass direction, which for this
gate means three distinct lies:

1. a page that declares nothing must FAIL (not "clean because nothing found")
2. a page that declares a state but implements nothing must FAIL
3. a static page must be EXEMPT (over-strictness trains gate-avoidance)

The exemption is as important as the failures: demanding `/* states: */` on a
static marketing page produces exactly the box-ticking the gate should prevent.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(sys.argv[1] if len(sys.argv) > 1 else
              Path(__file__).resolve().parent.parent / "scripts/state_check.py").resolve()

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


def write(tmp, name, content):
    p = Path(tmp) / name
    p.write_text(content, encoding="utf-8")
    return p


DECLARED_AND_LANDED = """<!-- states: loading,empty,error,success -->
<div class="is-loading">加载中</div>
<div class="empty-state">暂无订单，去新建一个</div>
<div class="is-error">加载失败，请重试</div>
<div class="is-success">保存成功</div>
"""

# 声明了但代码里零实现——这是门禁要抓的核心谎言
DECLARED_NOT_LANDED = """<!-- states: loading,empty,error,success -->
<h1>订单列表</h1>
<div class="card">订单 #1024</div>
"""

# 只有部分落地：loading 有，empty / error / success 没有
PARTIALLY_LANDED = """<!-- states: loading,empty,error,success -->
<div class="is-loading">加载中</div>
<div class="card">订单 #1024</div>
"""

NO_CONTRACT = """<h1>订单列表</h1>
<div class="card">订单 #1024</div>
"""

STATIC_PAGE = """<h1>关于我们</h1>
<p>纯静态营销页，没有任何异步数据。</p>
"""

# 实现了但没声明——不阻塞，但应提示
LANDED_NOT_DECLARED = """<h1>订单列表</h1>
<div class="is-loading">加载中</div>
"""

# CSS 载体（Tailwind 之外的项目）
CSS_CARRIER = """/* states: loading,empty,error */
.card.is-loading { opacity: .5; }
.empty-state { padding: 2rem; }
.is-error { color: #b91c1c; }
"""

# 未知状态名
UNKNOWN_STATE = """<!-- states: loading,whatever -->
<div class="is-loading">加载中</div>
"""

# 声明不能给自己作证：no-permission 的证据模式是裸子串，
# 声明标记本身曾命中它——零实现也 PASS（2026-10-24 探针实证后收口）
SELF_CERTIFYING = """<!-- states: no-permission -->
<h1>设置</h1>
<p>账户偏好设置。</p>
"""

# 真证据：写在实现里的 data-state（不在声明标记里），必须照常通过
PERM_LANDED = """<!-- states: no-permission -->
<div data-state="no-permission" hidden>没有权限查看此分区</div>
"""

# 注释里的示例声明与示例证据都不算——修复前 declared=3 landed=1 全靠注释撑着，
# 示例三态证据凑齐即可零实现过闸（2026-10-24 探针实证后收口）
EXAMPLE_ALL = """<!-- 示例：/* states: loading, empty, error */ -->
<!-- <div class="is-loading">示例加载中</div> -->
<!-- <div class="empty-state">示例空态</div> -->
<!-- <div class="is-error">示例错误</div> -->
<h1>设置</h1>
"""


def main():
    with tempfile.TemporaryDirectory() as tmp:
        ok = write(tmp, "ok.html", DECLARED_AND_LANDED)
        liar = write(tmp, "liar.html", DECLARED_NOT_LANDED)
        partial = write(tmp, "partial.html", PARTIALLY_LANDED)
        nocontract = write(tmp, "nocontract.html", NO_CONTRACT)
        static = write(tmp, "static.html", STATIC_PAGE)
        undeclared = write(tmp, "undeclared.html", LANDED_NOT_DECLARED)
        csscarrier = write(tmp, "carrier.css", CSS_CARRIER)
        unknown = write(tmp, "unknown.html", UNKNOWN_STATE)

        r = run([str(ok)])
        check("declared-and-landed-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        r = run([str(liar)])
        check("declared-not-landed-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("declared-not-landed-reports-rule",
              "state-declared-not-landed" in r.stdout, r.stdout[-300:])
        # 统计口径：假声明不能算成已落地
        check("declared-not-landed-counts-zero",
              "landed=0" in r.stdout, r.stdout[-300:])

        r = run([str(partial)])
        check("partially-landed-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("partially-landed-names-missing",
              "empty" in r.stdout and "error" in r.stdout, r.stdout[-300:])

        r = run([str(nocontract)])
        check("no-contract-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("no-contract-reports-rule",
              "state-absent" in r.stdout, r.stdout[-300:])

        # 静态页豁免——过度严格会训练出堆标记
        r = run([str(static), "--complexity", "static"])
        check("static-page-exempt", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 实现了但没声明：v2.14.1 起拦截——声明是可审计载体，实现先于声明不豁免
        r = run([str(undeclared)])
        check("landed-not-declared-blocks", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("landed-not-declared-reports-rule",
              "state-declared-absent" in r.stdout, r.stdout[-300:])

        # static 场景豁免仍成立：静态页有状态字样的文案也不强制声明
        r = run([str(undeclared), "--complexity", "static"])
        check("static-exempt-even-when-landed", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # CSS 载体
        r = run([str(csscarrier)])
        check("css-carrier-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 派生规则：moderate 要求 loading/empty/error，一个都没声明
        r = run([str(nocontract), "--complexity", "moderate"])
        check("required-missing-fails", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("required-missing-reports-rule",
              "state-required-missing" in r.stdout, r.stdout[-300:])

        # 派生规则：basic 只要求 error/success，declared-and-landed 已覆盖
        r = run([str(ok), "--complexity", "basic"])
        check("basic-complexity-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 复杂度取值越界必须拒跑，不静默按无要求处理
        r = run([str(ok), "--complexity", "whatever"])
        check("invalid-complexity-exits-2", r.returncode == 2,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 未知状态名：提示但不阻塞
        r = run([str(unknown)])
        check("unknown-state-warns", "state-unknown" in r.stdout, r.stdout[-300:])

        # 声明不是证据：no-permission 声明 + 零实现必须失败
        selfcert = write(tmp, "selfcert.html", SELF_CERTIFYING)
        r = run([str(selfcert)])
        check("declaration-is-not-own-evidence", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("self-certify-reports-rule",
              "state-declared-not-landed" in r.stdout, r.stdout[-300:])
        check("self-certify-counts-zero-landed",
              "landed=0" in r.stdout, r.stdout[-300:])

        # 真证据（实现里的 data-state）不受标记剥离影响
        permland = write(tmp, "permland.html", PERM_LANDED)
        r = run([str(permland)])
        check("no-permission-landed-passes", r.returncode == 0,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 注释里的示例声明与示例证据都不算数
        exall = write(tmp, "exall.html", EXAMPLE_ALL)
        r = run([str(exall)])
        check("example-declaration-and-evidence-ignored", r.returncode == 1,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))
        check("example-reports-absent",
              "state-absent" in r.stdout, r.stdout[-300:])

        # JSON 输出可解析
        r = run([str(ok), "--json"])
        try:
            json.loads(r.stdout)
            check("json-output-parses", True)
        except Exception as exc:
            check("json-output-parses", False, "%s / %s" % (exc, r.stdout[-200:]))

        # 空扫描不等于通过
        empty = Path(tmp) / "empty"
        empty.mkdir()
        r = run([str(empty)])
        check("empty-scan-exits-2", r.returncode == 2,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

        # 路径不存在
        r = run([str(Path(tmp) / "nope")])
        check("missing-path-exits-2", r.returncode == 2,
              "exit=%s out=%s" % (r.returncode, r.stdout[-300:]))

    print("-" * 60)
    print("checks=%d failures=%d" % (checks, len(failures)))
    print("RESULT: %s" % ("FAIL" if failures else "PASS"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

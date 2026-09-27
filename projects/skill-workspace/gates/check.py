#!/usr/bin/env python3
"""门一 · 机械校验门（skill-workspace 自检）。

零依赖：只用 Python 标准库，不要求 PyYAML / git / rsync。
两档：--level=warn 恒退出 0（只报告），--level=strict 有 ERROR 时退出 1。
自举：gates/ 自身不纳入体积与引用检查；副本比对忽略行尾差异。
"""

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 官方规范只认这 6 个 frontmatter 字段
SPEC_FIELDS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
# 全仓唯一的版本号来源
VERSION_RE = re.compile(r"^\s*version:\s*['\"]?([0-9]+\.[0-9]+\.[0-9]+)['\"]?\s*$", re.M)
# 两套路径变量都要归零：${SKILL_DIR} 无官方出处，${CLAUDE_SKILL_DIR} 仅 Claude Code 展开
PLACEHOLDER_RE = re.compile(r"\$\{(SKILL_DIR|CLAUDE_SKILL_DIR|_CLAUDE_SKILL_DIR)\}")
# 静态门的抑制通道：一旦出现，门就成了建议
# 静态门的抑制通道：一旦出现，门就成了建议。
# 用字符类而非字面量，否则本脚本会匹配到自己的源码。
EXEMPT_RE = re.compile(r"(gates?\s*:\s*ignore|check\s*:\s*disable|eslint[-_]disable|#\s*noqa)")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
# 反引号/括号里的多段相对路径也要能抓下来：`../references/x.md`、`scripts/y.sh`
# 字符类刻意不含 CJK：Python 的 \w 匹配汉字，会把"新增references/x.md"里的中文吞成路径。
# 段首的 `./` `../` 由 _CODE_SEG 自身含 `.` 覆盖，不必再写前缀组。
_CODE_SEG = r"[A-Za-z0-9_.{}\-]+"
CODE_PATH_RE = re.compile(
    rf"({_CODE_SEG}(?:/{_CODE_SEG})*/?\.(?:md|py|sh|ps1|json|ya?ml|txt))"
)

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".research"}
# 与 tools/export.sh 的排除项一一对应，两边不一致就会产出假红/假绿
EXPORT_SKIP = {"artifacts", ".gitattributes"}
SCAN_EXT = {".md", ".py", ".sh", ".ps1", ".json", ".yaml", ".yml", ".txt"}
BUDGET_EXT = {".md"}
# 只有 "N 分制" 才算一套分制声明。"9 维度总分：85 分" 是示例得分，不是分制。
SCHEME_RE = re.compile(r"(\d{2,3})\s*分制")
# 字母评级写法：A 级 / B级 / ≥ B / ≤ C。只在同一行讲"安全"时才算串台，
# Darwin 质量评级的 A/B/C 是另一套东西，不该被这条误伤。
GRADE_LETTER_RE = re.compile(r"([ABC]\s*级|[≥≤]\s*[ABC](?![A-Za-z]))")


def findings():
    out = []

    def add(check, level, path, msg):
        p = str(path)
        try:
            rel = os.path.relpath(p, str(ROOT)).replace("\\", "/")
        except ValueError:
            rel = p.replace("\\", "/")  # 安装位在别的盘符上，relpath 会抛，退回绝对路径
        out.append((check, level, rel, msg))

    return out, add


def walk_text_files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in SCAN_EXT:
            continue
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        yield p


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def frontmatter(p):
    """行级解析：返回 (字段名->原始值, 字段出现顺序, 是否成对闭合)。不依赖 YAML 库。"""
    lines = read(p).splitlines()
    if not lines or lines[0].strip() != "---":
        return None, [], False
    fields, order = {}, []
    for i, ln in enumerate(lines[1:], start=1):
        if ln.strip() == "---":
            for k, v in _split_body(lines[1:i]):
                fields[k] = v
                order.append(k)
            return fields, order, True
    return fields, order, False


def _split_body(body):
    """只取顶层 key:，缩进行视为上一个值的续体。
    metadata 下的 version 记成 `metadata/*version`，用来判"版本该放哪"。"""
    out = []
    for ln in body:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if ln.startswith((" ", "\t")):
            if out and ln.strip().split(":", 1)[0].strip() == "version":
                out.append((out[-1][0] + "/*version", ln))
            continue
        if ":" in ln:
            out.append((ln.split(":", 1)[0].strip(), ln))
    return out


# ---------- 1 引用路径存在性 + 逃逸检测 ----------
# 文件树示意图（`├── decision-trees.md`）描述的是"要生成出来的结构"，不是包内链接
TREE_CHARS = "│├└┌┐┘┤┬┴┼─"
# 变量锚定的引用：${SKILL_DIR}/references/x.md → 抓到的是 {SKILL_DIR}/references/x.md
VAR_ANCHOR_RE = re.compile(r"^\{[A-Za-z_]+\}/(.+)$")


def _skip_by_content(raw):
    """返回跳过理由；None 表示这条路径要判存在性。

    只跳过"根本不是包内链接"的四类路径，宁可多判也不放走断链。
    """
    if raw.startswith(("http://", "https://", "mailto:", "#")):
        return "外链"
    if raw.startswith("/"):
        return "绝对路径"
    if "/" not in raw:
        # `.dev-memory.md`、`state.json` 这类裸文件名是运行时在用户工程里读写的产物。
        return "运行时产物"
    first = raw.split("/")[0]
    if first.startswith(".") and first not in (".", ".."):
        return "宿主/隐藏配置"  # .trae/mcp.json、.cursor/mcp.json、.claude/settings.json
    low = raw.lower()
    if "xxx" in low or "path/to" in low or "phase-n-" in low:
        return "占位示例"
    if "{" in raw or "}" in raw:
        return "模板占位"  # {全局skills目录}/x.md、report-{date}-{topic}.md
    return None


def _fenced_lines(text):
    """落在 ``` 围栏内的行号集合。

    围栏里通常是"蒸馏出来的技能该长什么样"的示例清单，不是本包的链接；
    所以这些行上的未命中只记 WARN，不阻断。
    """
    lines = text.splitlines()
    fenced, open_at = set(), None
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("```") or s.startswith("~~~"):
            if open_at is None:
                open_at = i
            else:
                fenced.update(range(open_at, i + 1))
                open_at = None
    if open_at is not None:
        fenced.update(range(open_at, len(lines) + 1))
    return fenced


def _ref_skippable(line, m, raw):
    if _skip_by_content(raw):
        return True
    # CODE_PATH_RE 吃不下 scheme，只会从 `https://host/a/b.md` 的 host 起匹配，
    # 所以要看匹配前两个字符是不是 `//`，否则会把 URL 尾巴当成本地相对路径。
    return line[max(0, m.start() - 2):m.start()] == "//"


def _resolves(base, rel):
    """相对 base 解析 rel；逃逸出包根视为不成立。返回 (命中, 逃逸)。"""
    try:
        target = (base / rel.split("#")[0]).resolve()
        target.relative_to(ROOT)
    except ValueError:
        return False, True
    return target.exists(), False


def _skill_anchor(p):
    """${SKILL_DIR} 的第二种可能含义：最近的含 SKILL.md 的祖先目录（不是文件自己所在的目录）。

    references/deploy.md 属于包根技能，锚点就该是包根；用 deploy.md 自己的目录判，
    会把一堆本来正确的 ${SKILL_DIR}/scripts/... 误判成含糊。
    """
    d = p.parent
    while d != ROOT.parent:
        if (d / "SKILL.md").is_file():
            return d
        d = d.parent
    return ROOT


def check_refs(add):
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        if p.relative_to(ROOT).parts[0] == "gates":
            continue
        # artifacts/ 是历次运行的产出报告，里面的路径按当时的布局写，改它等于改历史；
        # ``` 围栏内是引用的示例代码或目录清单；├── 树形图描述"要生成的结构"。
        # 三类都降为 WARN：照样报出来，但不当成包内死链阻断。
        soft_file = p.relative_to(ROOT).parts[0] == "artifacts"
        seen = set()
        text = read(p)
        fenced = _fenced_lines(text)
        for lineno, line in enumerate(text.splitlines(), 1):
            lvl = "WARN" if (soft_file or lineno in fenced or
                             any(c in line for c in TREE_CHARS)) else "ERROR"
            for m in list(MD_LINK_RE.finditer(line)) + list(CODE_PATH_RE.finditer(line)):
                raw = m.group(1).strip()
                var = VAR_ANCHOR_RE.match(raw)
                if var:
                    rel = var.group(1)
                    if _skip_by_content(rel):
                        continue
                    # ${SKILL_DIR} 无官方定义，两种宿主两种含义：包根 or 本技能目录。
                    # 只在"两种锚定都落空"时判死链——变量该用哪套由 placeholder 管。
                    hit_root, _ = _resolves(ROOT, rel)
                    hit_self, _ = _resolves(_skill_anchor(p), rel)
                    if hit_root == hit_self:
                        if not hit_root:
                            add("refs", lvl, p,
                                f"L{lineno} 断链：{raw}（锚定为包根或本技能目录都找不到目标）")
                    else:
                        # 只有一种锚定能命中：换宿主就断，静默放过等于假绿
                        add("refs", "WARN", p,
                            f"L{lineno} 锚定含糊：{raw}（只有"
                            f"{'包根' if hit_root else '本技能目录'}能命中）")
                    continue
                if _ref_skippable(line, m, raw):
                    continue
                target, escaped = _resolves(p.parent, raw)
                if escaped:
                    add("refs", lvl, p, f"L{lineno} 引用逃逸出包根：{raw}")
                    continue
                if target:
                    continue
                if (ROOT / raw.split("#")[0]).exists():
                    # 只在包根存在、在本技能目录下不存在：链接能通，但锚定含糊
                    add("refs", "WARN", p,
                        f"L{lineno} 锚定含糊：{raw}（按包根存在，按本技能目录找不到）")
                    continue
                key = (lineno, raw)
                if key in seen:
                    continue
                seen.add(key)
                add("refs", lvl, p, f"L{lineno} 断链：{raw}")


# ---------- 2 frontmatter 合规 ----------
def check_frontmatter(add):
    for p in sorted(ROOT.rglob("SKILL.md")):
        if p.relative_to(ROOT).parts[0] == "gates":
            continue
        fields, order, closed = frontmatter(p)
        if fields is None:
            add("frontmatter", "ERROR", p, "缺少 frontmatter（首行不是 ---）")
            continue
        if not closed:
            add("frontmatter", "ERROR", p, "frontmatter 未闭合")
            continue
        for k in order:
            top = k.split("/*")[0]
            if top not in SPEC_FIELDS:
                add("frontmatter", "ERROR", p, f"非规范字段：{top}（官方只认 {len(SPEC_FIELDS)} 个）")
        if "name" not in order:
            add("frontmatter", "ERROR", p, "缺 name")
        if "description" not in order:
            add("frontmatter", "ERROR", p, "缺 description")


# ---------- 3 name 与目录同名 ----------
def check_name_dir(add):
    for p in sorted(ROOT.rglob("SKILL.md")):
        if p.relative_to(ROOT).parts[0] == "gates":
            continue
        fields, _, ok = frontmatter(p)
        if not ok or not fields:
            continue
        for k, ln in fields.items():
            if k != "name":
                continue
            m = re.match(r"name:\s*(\S+)", ln.strip())
            if not m:
                continue
            want = ROOT.name if p.parent == ROOT else p.parent.name
            if m.group(1) != want:
                add("name-dir", "ERROR", p, f"name={m.group(1)} 与目录名 {want} 不一致")


# ---------- 4 版本号全仓一致 ----------
def check_version(add):
    seen = {}
    for p in walk_text_files():
        for m in VERSION_RE.finditer(read(p)):
            seen.setdefault(m.group(1), []).append(p)
    if len(seen) > 1:
        for v, ps in sorted(seen.items()):
            add("version", "ERROR", ps[0], f"版本 {v} 出现在 {len(ps)} 个文件（全仓应只有一个值：{sorted(seen)}）")


# ---------- 5 声明式体积预算 ----------
def check_budget(add):
    HARD_CAP = 1200
    for p in sorted(ROOT.rglob("SKILL.md")):
        if p.relative_to(ROOT).parts[0] == "gates":
            continue
        txt = read(p)
        n = len(txt.splitlines())
        m = re.search(r"^\s*(?:size-budget|metadata\.size-budget):\s*(\d+)", txt, re.M)
        if not m:
            add("size-budget", "ERROR", p, f"未声明 size-budget（现 {n} 行）")
            continue
        budget = int(m.group(1))
        if n > budget:
            add("size-budget", "ERROR", p, f"超出声明预算：{n} > {budget}")
        if n > HARD_CAP:
            add("size-budget", "ERROR", p, f"超出硬顶：{n} > {HARD_CAP}")


# ---------- 6 路径变量残留 ----------
def check_placeholders(add):
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        for m in PLACEHOLDER_RE.finditer(read(p)):
            add("placeholder", "ERROR", p, f"残留变量 ${{{m.group(1)}}}")


# ---------- 7 评分体系唯一 ----------
# 禁止某个分制不等于又定义了一套分制：evals 的反例断言、SKILL.md 的"不要混用 120 分制"
# 都会被 SCHEME_RE 抓成第二套分制，所以按行看语境。
NEG_RE = re.compile(r"(不要|不得|禁止|不使用|不用|已废弃|废弃|混用|如果用户提到|立即修正|旧的|而非)")


def check_rubric(add):
    totals = {}
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        for line in read(p).splitlines():
            if NEG_RE.search(line):
                continue
            for m in SCHEME_RE.finditer(line):
                tot = m.group(1)
                if tot:
                    totals.setdefault(tot, set()).add(p)
    if len(totals) > 1:
        for t, ps in sorted(totals.items(), key=lambda kv: -int(kv[0])):
            add("rubric", "ERROR", next(iter(ps)),
                f"全仓并存 {len(totals)} 套分制：{t} 分制见 {sorted(str(x.relative_to(ROOT)).replace(chr(92),'/') for x in ps)[:2]}")


# ---------- 8 安全清单唯一 ----------
# 判据不用"安全词表"这类散文词（包内根本没这么写过，检查会空转）：
# 一个文件真列出 ≥3 个风险条目，就算它定义了一份安全清单。清单散成两份必然漂移。
RISK_TOKENS_RE = re.compile(
    r"(rm\s+-rf|sudo\s+|chmod\s+777|\.ssh[/{]|id_rsa|\.env\b|curl[^|]{0,20}\|\s*sh"
    r"|eval\(|exec\(|--no-verify|force-push|DROP\s+TABLE|mkfs)")


def check_secwords(add):
    owners = []
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        hits = set(m.group(0).strip() for m in RISK_TOKENS_RE.finditer(read(p)))
        if len(hits) >= 3:
            owners.append((p, sorted(hits)))
    if len(owners) > 1:
        add("secwords", "ERROR", owners[0][0],
            f"安全清单散落在 {len(owners)} 个文件，必然漂移："
            + "；".join(f"{o.relative_to(ROOT)}（{len(h)} 条）" for o, h in owners))

    # 四值评级词表（SAFE/WARNING/DANGER/BLOCK）只能有一处定义。
    # 判据取"清单里出现了 `- SAFE：` 这一行"——只有真正定义规则的文件会写它，
    # 报告模板里的 {SAFE / WARNING / DANGER / BLOCK} 占位符不算定义。
    defs = []
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        body = read(p)
        if any(ln.lstrip().startswith(("- SAFE：", "- SAFE:")) for ln in body.splitlines()):
            defs.append(p)
    if len(defs) != 1:
        add("secwords", "ERROR" if defs else "WARN", defs[0] if defs else ROOT,
            "安全评级词表定义了 %d 处（应恰好 1 处）：%s" % (
                len(defs), [str(d.relative_to(ROOT)).replace(chr(92), "/") for d in defs]))

    # 同一行既讲"安全"又用字母评级，就是词表串台（Darwin 质量评级的 A/B/C 不带"安全"二字）
    for p in walk_text_files():
        if p.suffix.lower() not in BUDGET_EXT:
            continue
        for i, ln in enumerate(read(p).splitlines(), 1):
            if "安全" in ln and GRADE_LETTER_RE.search(ln):
                add("secwords", "ERROR", p,
                    f"L{i} 安全评级用了字母评级，与四值词表串台：{ln.strip()[:50]}")


# ---------- 9 副本内容一致 ----------
def check_copies(add):
    targets = [ROOT.parent.parent / ".agents" / "skills" / ROOT.name,
               Path.home() / ".agents" / "skills" / ROOT.name]
    for t in targets:
        if not t.is_dir():
            add("copies", "WARN", t, "安装位不存在（未导出）")
            continue
        # 比对集合必须等于导出集合，否则门会永远报假红：
        # artifacts/ 是历次运行产物、.gitattributes 只在 git 仓库里有意义，两者都不导出。
        skip = EXPORT_SKIP
        src = {q.relative_to(ROOT).as_posix() for q in walk_text_files()
               if not (skip & {q.relative_to(ROOT).parts[0], q.name})}
        dst = {q.relative_to(t).as_posix() for q in
               (x for x in t.rglob("*") if x.is_file() and x.suffix.lower() in SCAN_EXT
                and not (SKIP_DIRS & set(x.relative_to(t).parts)))}
        for rel in sorted(src - dst):
            add("copies", "ERROR", t, f"缺文件：{rel}")
        for rel in sorted(dst - src):
            add("copies", "ERROR", t, f"多余文件：{rel}")
        for rel in sorted(src & dst):
            if read(ROOT / rel).replace("\r\n", "\n") != read(t / rel).replace("\r\n", "\n"):
                add("copies", "ERROR", t, f"内容漂移：{rel}")


# ---------- 10 门的抑制通道必须为零 ----------
def check_exemptions(add):
    for p in walk_text_files():
        for m in EXEMPT_RE.finditer(read(p)):
            add("exemption", "ERROR", p, f"存在自我豁免通道：{m.group(0)}（静态门可被就地关掉即不是门）")


CHECKS = [check_refs, check_frontmatter, check_name_dir, check_version, check_budget,
          check_placeholders, check_rubric, check_secwords, check_copies, check_exemptions]


def main():
    ap = argparse.ArgumentParser(description="门一 · 机械校验门")
    ap.add_argument("--level", choices=["warn", "strict"], default="warn")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    # Windows 控制台默认 GBK，中文报告行会乱码；这里强制 UTF-8 输出
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass

    out, add = findings()
    for fn in CHECKS:
        fn(add)

    errors = [f for f in out if f[1] == "ERROR"]
    warns = [f for f in out if f[1] == "WARN"]

    if args.json:
        import json
        print(json.dumps([{"check": c, "level": l, "path": p, "msg": m} for c, l, p, m in out],
                         ensure_ascii=False, indent=2))
    else:
        for c, l, p, m in out:
            print(f"{l:5} | {c:12} | {p} | {m}")
        tally = {}
        for c, l, _, _ in out:
            k = (c, l)
            tally[k] = tally.get(k, 0) + 1
        print("-" * 72)
        for (c, l), n in sorted(tally.items()):
            print(f"  {c:12} {l:5} × {n}")
        print(f"合计 {len(out)} 条（ERROR {len(errors)} ／ WARN {len(warns)}）｜档位 {args.level}")

    if args.level == "strict" and errors:
        print("❌ 门一 strict 未过：先清 ERROR 再谈发布。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

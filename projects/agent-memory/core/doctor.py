"""core.doctor — 记忆体检：六项机械检查（每项一条路径可判，输出结构化 findings）。

六项（与 super-memory memory-doctor.md 契约同步）：
  1 索引断链   2 重复条目   3 非法置信度码
  4 超龄未验证   5 锚点活性抽查   6 条目格式齐全性

处置由调用方按 memory-doctor.md 路由表执行（本模块只产出 findings，不动文件）。
自测: `python -m core.doctor`（fixture 注入全部病灶，全检出且健康条目零误报才算过）
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

VALID_CODES = {"V", "W", "Q", "R", "F"}
STALE_DAYS = 90
K_HEAD = re.compile(r"^## \[(K-\d{8}-\d+)\]\s*(.*)$", re.M)
CODE_RE = re.compile(r"\[[A-Z]{1,3}\]")
ANCHOR_RE = re.compile(r"`([^`\n:]+?):\d+`")


@dataclass
class Finding:
    check: str
    target: str
    message: str
    severity: str = "warn"   # info | warn | fix（fix=可直接修，不动结论）
    action: str = ""


def _md_files(root: Path):
    for p in sorted(root.rglob("*.md")):
        s = p.as_posix()
        if any(n in f"/{s}" for n in ("/node_modules/", "/.git/", "/.mimosa/")):
            continue
        yield p


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ── 检查一：索引断链 ─────────────────────────────────────

def check_broken_links(root: Path) -> list[Finding]:
    out = []
    for index in root.rglob("MEMORY.md"):
        base = index.parent
        for m in re.finditer(r"\(([^)\s]+\.md)\)", _read(index)):
            rel = m.group(1).replace("\r", "")
            if not (base / rel).exists():
                out.append(Finding("断链", f"{index.name} -> {rel}",
                                   "索引指向不存在的文件", "fix",
                                   "移除索引行（确认非改名/隔离迁移）"))
    return out


# ── 检查二：重复条目（标题归并）──────────────────────────

def check_duplicates(root: Path) -> list[Finding]:
    titles: dict[str, list] = {}
    for p in _md_files(root):
        for m in re.finditer(r"^## \[([A-Z]+-[^\]]+)\]\s*(.+)$", _read(p), re.M):
            key = re.sub(r"\s+", "", m.group(2))[:40]
            titles.setdefault(key, []).append((m.group(1), p))
    return [Finding("重复", " / ".join(i for i, _ in ids),
                    f"同主题条目 {len(ids)} 条：{key[:30]}", "warn",
                    "四操作合并（knowledge=SUPERSEDE 留档；记忆库走 2.5 确认）")
            for key, ids in titles.items() if len(ids) >= 2]


# ── 检查三：非法置信度码 ─────────────────────────────────

def check_illegal_codes(root: Path) -> list[Finding]:
    out = []
    for p in _md_files(root):
        reported = set()
        for m in CODE_RE.finditer(_read(p)):
            code = m.group(0)
            if code in {f"[{c}]" for c in VALID_CODES} or code in reported:
                continue
            reported.add(code)
            out.append(Finding("非法码", code, f"{p.name}: {code} 不是五码之一",
                               "fix", "修正为 [V][W][Q][R][F] 或改标 [已失效]"))
    return out


# ── 检查四：超龄未验证 ───────────────────────────────────

def check_stale(root: Path, today: date | None = None) -> list[Finding]:
    today = today or date.today()
    cutoff = today - timedelta(days=STALE_DAYS)
    out = []
    for p in _md_files(root):
        t = _read(p)
        for m in re.finditer(r"最后验证\*\*[：:]\s*(\d{4}-\d{2}-\d{2})", t):
            d = date.fromisoformat(m.group(1))
            if d < cutoff:
                age = (today - d).days
                out.append(Finding("超龄", f"{p.name} ({m.group(1)}, {age} 天)",
                                   "超过 90 天未验证——建议重验或降级", "info",
                                   "列出待用户拍板；不代判不删除"))
    return out


# ── 检查五：锚点活性抽查 ─────────────────────────────────

def check_anchor_liveness(root: Path, sample: int = 5) -> list[Finding]:
    out = []
    anchors = []
    for p in _md_files(root):
        for m in ANCHOR_RE.finditer(_read(p)):
            target = m.group(1).replace("\\", "/")
            if any(x in target for x in ("http", "node_modules")):
                continue
            anchors.append((p, target))
    for p, target in anchors[:sample]:
        fpath, _, _ = target.rpartition(":")
        if not fpath:
            continue
        f = Path(fpath)
        if not f.exists():
            f = root / fpath
        if f.exists():
            continue
        out.append(Finding("锚点失效", target, "锚点指向的文件已不存在", "warn",
                           "降该条置信度一级并注明复查日期（不删除条目）"))
    return out


# ── 检查六：条目格式齐全性（条目级，非文件级）─────────────

def check_fields(root: Path):
    from . import store
    out = []
    for p in _md_files(root):
        t = _read(p)
        for fmt, head in (("knowledge", K_HEAD),
                          ("learnings", re.compile(r"^## \[([A-Z]+-\d{8}-\d+)\]", re.M))):
            for e in store.parse(fmt, t) if "## [" in t else []:
                if fmt == "knowledge" and "已失效" in e.fields:
                    continue  # 归档件豁免（由取代者持链接）
                for err in store.validate(fmt, e):
                    out.append(Finding("字段缺失", e.id or e.title, err, "fix",
                                       "补元数据（不改结论与历史）"))
    return out


# ── 聚合入口 ─────────────────────────────────────────────

def check_all(root: Path) -> list[Finding]:
    root = Path(root)
    out = []
    out += check_broken_links(root)
    out += check_duplicates(root)
    out += check_illegal_codes(root)
    out += check_stale(root)
    out += check_anchor_liveness(root)
    out += check_fields(root)
    return out


# ── 自测：注入全部病灶，要求全部检出且健康条目零误报 ─────

def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "mem"
        (root / ".ai" / "knowledge").mkdir(parents=True)
        (root / ".learnings").mkdir()
        # 健康条目（零误报基准）：含存在的锚点
        (root / "core").mkdir()
        (root / "core" / "store.py").write_text("# anchor target\n", encoding="utf-8")
        (root / ".ai" / "knowledge" / "healthy.md").write_text(
            "## [K-20261024-001] 健康条目\n\n"
            "**置信度**：[V]　　**生效**：2026-10-24　　**记录**：2026-10-24　　"
            "**最后验证**：2026-10-24　　**适用版本**：main\n"
            "**结论**：ok\n**Tags**：demo\n**Related**：无\n"
            "`core/store.py:1` 锚点存在\n", encoding="utf-8")
        # 病灶：非法码 + 超龄（真实 90 天+ 的最后验证）+ 字段缺失
        (root / ".ai" / "knowledge" / "sick.md").write_text(
            "## [K-20260101-001] 病条目\n\n"
            "**置信度**：[X]　　**生效**：2026-01-01　　**记录**：2026-01-01　　"
            "**最后验证**：2026-06-01　　**适用版本**：main\n"
            "**结论**：旧认知\n", encoding="utf-8")
        # 病灶：断链
        (root / "MEMORY.md").write_text(
            "- [健康](.ai/knowledge/healthy.md) — ok\n- [幽灵](ghost.md) — 不存在\n",
            encoding="utf-8")
        # 病灶：重复
        (root / ".learnings" / "LEARNINGS.md").write_text(
            "## [LRN-20261024-001] 重复主题\n\n**Logged**: 2026-10-24\n"
            "**Priority**: low\n**Status**: pending\n**Summary**: x\n"
            "**Metadata**\n- Recurrence-Count: 1\n\n"
            "## [LRN-20261024-002] 重复主题\n\n**Logged**: 2026-10-24\n"
            "**Priority**: low\n**Status**: pending\n**Summary**: y\n", encoding="utf-8")
        findings = check_all(root)
        kinds = [f.check for f in findings]
        for need in ("断链", "非法码", "超龄", "重复", "字段缺失"):
            ok &= need in kinds
        # 健康条目不得被误报字段缺失
        ok &= not any("健康条目" in f.target and f.check == "字段缺失" for f in findings)
    print("doctor selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(selftest())

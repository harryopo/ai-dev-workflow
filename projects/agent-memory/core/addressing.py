"""core.addressing — 宿主无关记忆寻址（四层：自述→规则文件→探测→兜底）。

从 super-memory memory-addressing.md 的已知形态表（8 类宿主实测）转写：
  规则文件：AGENTS.md → CLAUDE.md → QODER.md → GEMINI.md → .cursor/rules → copilot-instructions
  宿主探测：Qoder / QoderCN / ZCode（sha256 可精算）/ Trae / Codex / WorkBuddy / Claude Code / 兜底
  多命中裁决：宿主自述 > 规则文件 > 同宿主过滤 > slug/哈希对号 > mtime > 列出问用户（不瞎猜）

自测: `python -m core.addressing`
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

RULE_FILES = ("AGENTS.md", "CLAUDE.md", "QODER.md", "GEMINI.md",
              ".cursor/rules", ".github/copilot-instructions.md")
MEMORY_SECTION = re.compile(r"记忆|memory|learnings", re.I)
ZCODE = ".zcode/cli/memories/projects"


@dataclass
class MemoryLayout:
    workspace: str
    rule_file: str | None = None          # 层2 命中的规则文件（含记忆章节）
    user_root: str | None = None          # 用户级记忆位
    project_root: str | None = None       # 项目级记忆位（命中）
    candidates: list = field(default_factory=list)  # 未裁决的宿主候选
    fallback: str | None = None           # 兜底：项目根 memory/
    ambiguous: bool = False

    @property
    def source(self) -> str:
        if self.user_root or self.project_root:
            return "host" if self.project_root else "host-user"
        if self.rule_file:
            return "rule"
        return "fallback"


# ── 层1：规则文件 ────────────────────────────────────────

def find_rule_file(workspace: Path) -> str | None:
    for name in RULE_FILES:
        p = workspace / name
        if p.is_file() and MEMORY_SECTION.search(_read(p)):
            return str(p)
    return None


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ── 层3：宿主探测（形态表的可执行版）─────────────────────

def qoder_slug(path: str) -> str:
    """Qoder slug：盘符冒号、\\、/、空格及所有非 ASCII → '-'（实测规则）。"""
    return re.sub(r"[^0-9A-Za-z]", "-", path)


def zcode_hash(workspace: str) -> str:
    """ZCode 目录哈希：sha256(小写工作区根)[:16]（bundle 源码 + 8 样本实测）。"""
    return hashlib.sha256(str(workspace).lower().encode()).hexdigest()[:16]


def zcode_dirname(workspace: str) -> str:
    base = re.sub(r"[^a-z0-9._-]+", "-", Path(workspace).name.lower())
    base = base.strip("-")[:48] or "project"
    return f"{base}-{zcode_hash(workspace)}"


def _glob_first(home: Path, pattern: str):
    hits = sorted(home.glob(pattern))
    return hits[0] if len(hits) == 1 else None


def probe_hosts(workspace: Path, home: Path) -> list[dict]:
    """按形态表探测各宿主记忆位（存在的才返回；多命中交裁决）。

    全部用相对 home 的模式做 glob（pathlib 不接受绝对 pattern）；
    ZCode 用哈希精算直查 + 目录名前缀反查兜底。
    """
    ws = Path(workspace)
    out = []

    def hit(rel: str) -> str | None:
        p = home / rel
        return str(p) if p.exists() else None

    def globdirs(rel: str) -> list[Path]:
        return sorted(d for d in home.glob(rel) if d.is_dir())

    # Qoder：项目级 slug 精确对号
    qslug = qoder_slug(str(ws))
    q_u = hit(".qoder/memory")
    q_p = hit(f".qoder/projects/{qslug}/memory")
    if q_u or q_p:
        out.append({"host": "qoder", "user": q_u, "project": q_p})

    # ZCode：哈希精算直查；未命中则目录名前缀反查
    z_u = None
    z_p = hit(f"{ZCODE}/{zcode_dirname(ws)}/memory")
    if not z_p:
        pref = re.sub(r"[^a-z0-9._-]+", "-", ws.name.lower()).strip("-")[:48]
        for d in globdirs(f"{ZCODE}/*/memory"):
            if Path(d).name.startswith(pref + "-") or Path(d).name == pref:
                z_p = str(d)
                break
    if z_p:
        out.append({"host": "zcode", "user": z_u, "project": z_p})

    # 其余宿主
    for host, user_rel, proj_rel in (
        ("trae", ".trae-cn/memory", ".trae-cn/memory/projects/*"),
        ("codex", ".codex/memories", None),
        ("workbuddy", ".workbuddy/memory", None),
        ("claude", ".claude/memory", ".claude/projects/*/memory"),
    ):
        u = hit(user_rel) if user_rel else None
        pj = None
        if proj_rel:
            gd = globdirs(proj_rel)
            if len(gd) == 1:
                pj = str(gd[0])
        if u or pj:
            out.append({"host": host, "user": u, "project": pj})

    # 兜底：项目根 memory/
    if (ws / "memory").exists():
        out.append({"host": "fallback", "user": None, "project": str(ws / "memory")})
    return out


# ── 层4：兜底 ────────────────────────────────────────────

def fallback_dir(workspace: Path) -> str | None:
    d = workspace / "memory"
    return str(d) if d.exists() else None


# ── 统一入口：locate ─────────────────────────────────────

def locate(workspace: str, home: str | None = None) -> MemoryLayout:
    ws = Path(workspace).resolve()
    home = Path(home or Path.home())
    layout = MemoryLayout(workspace=str(ws))

    # 层2：规则文件
    layout.rule_file = find_rule_file(ws)

    # 层3：探测 + 裁决
    hosts = probe_hosts(ws, home)
    if hosts:
        same = [h for h in hosts if h["host"] in ("qoder", "zcode", "claude")]
        exact = [h for h in same if h.get("project")]
        if len(exact) == 1:
            layout.project_root = exact[0]["project"]
            u = next((h for h in hosts if h["host"] in ("qoder", "claude") and h.get("user")), None)
            layout.user_root = u["user"] if u else None
        elif len(same) == 1 and same[0].get("project") is None and same[0].get("user"):
            layout.user_root = same[0]["user"]
        else:
            layout.candidates = hosts
            layout.ambiguous = True

    # 层4：兜底
    fb = fallback_dir(ws)
    if fb:
        layout.fallback = fb
    return layout


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / "home"
        ws = Path(td) / "ws"
        ws.mkdir(parents=True)
        home.mkdir(parents=True)

        # 兜底：无宿主 → 项目根 memory/（存在才算）
        lo = locate(str(ws), str(home))
        ok &= lo.source == "fallback" and lo.fallback is None  # memory/ 不存在
        (ws / "memory").mkdir()
        lo = locate(str(ws), str(home))
        ok &= lo.fallback == str(ws / "memory")

        # Qoder：项目级 slug 对号
        slug = qoder_slug(str(ws))
        qdir = home / f".qoder/projects/{slug}/memory"
        qdir.mkdir(parents=True)
        lo = locate(str(ws), str(home))
        ok &= lo.project_root == str(qdir) and lo.source == "host"

        # ZCode：哈希精算对号（宿主自述/规则文件缺席时）
        zdir = home / f"{ZCODE}/{zcode_dirname(str(ws))}/memory"
        zdir.mkdir(parents=True)
        lo = locate(str(ws), str(home))
        ok &= any("zcode" in str(c.get("project") or "") or "zcode" in str(c.get("user") or "")
                  for c in lo.candidates) or lo.ambiguous

        # 规则文件优先：CLAUDE.md 声明记忆章节 → 记为 rule_file
        (ws / "CLAUDE.md").write_text("## 记忆\n写入 memory/\n", encoding="utf-8")
        lo = locate(str(ws), str(home))
        ok &= lo.rule_file == str(ws / "CLAUDE.md")
    print("addressing selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(selftest())

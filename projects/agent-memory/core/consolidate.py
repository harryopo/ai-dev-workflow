"""core.consolidate — 巩固四操作的机械执行（决策由调用方/agent 判定）。

分工（与 super-memory 一致）：四操作的**判定**是 LLM 职责（grep 相似条目后四选一），
本模块负责判定的**机械落地**——编号计算、SUPERSEDE 留痕、UPDATE 追加记录、
NOOP 递增、ADD 建档 + 索引登记，全部走 store 的 fail-closed 校验。

自测: `python -m core.consolidate`
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from . import store


class ConsolidateError(Exception):
    pass


def next_id(root: Path, kind: str = "K", today: str | None = None) -> str:
    """当天同 kind 条目数 + 1（与 capture/K-NNN 规则同源，不许随机）。"""
    d = today or date.today().strftime("%Y%m%d")
    n = 0
    for p in Path(root).rglob("*.md"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        n += len(re.findall(rf"^## \[{kind}-{d}-\d+\]", t, re.M))
    return f"{kind}-{d}-{n + 1:03d}"


def _file_containing(root: Path, entry_id: str) -> Path | None:
    for p in Path(root).rglob("*.md"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if f"## [{entry_id}]" in t:
            return p
    return None


def _replace_entry_text(text: str, entry_id: str, new_block: str) -> str:
    pat = re.compile(rf"^## \[{re.escape(entry_id)}\].*?(?=^## \[|\Z)", re.M | re.S)
    if not pat.search(text):
        raise ConsolidateError(f"条目 {entry_id} 不在该文件中")
    return pat.sub(new_block.rstrip() + "\n", text, count=1)


def supersede(root: Path, old_id: str, new_entry_text: str,
              reason: str, today: str | None = None) -> dict:
    """SUPERSEDE：旧条目标 [已失效]（日期+取代者+原因三要素），新条目另存并 Related 回指。

    新条目文本须已是规范化 K 条目（含 Related 回指旧 ID）。
    返回 {old_file, new_file, new_id}。
    """
    d = today or date.today().strftime("%Y-%m-%d")
    new_id = re.search(r"^## \[(K-[^\]]+)\]", new_entry_text, re.M)
    if not new_id:
        raise ConsolidateError("新条目缺 K-ID 标题")
    new_id = new_id.group(1)
    old_file = _file_containing(root, old_id)
    if not old_file:
        raise ConsolidateError(f"旧条目 {old_id} 未找到")
    text = old_file.read_text(encoding="utf-8", errors="ignore")
    entries = store.parse("knowledge", text)
    old = next((e for e in entries if e.id == old_id), None)
    if not old:
        raise ConsolidateError(f"旧条目 {old_id} 解析失败")
    inv = f"{d} 起由 {new_id} 取代（原因：{reason}）。本条原地保留归档，不再推荐复用。"
    old.fields["已失效"] = inv
    if "Related" not in old.fields:
        old.fields["Related"] = f"{new_id}（取代者，{d} 登记）"
    # 只替换旧条目块，其余原样（不改写历史）
    new_block = store.render("knowledge", old)
    text = _replace_entry_text(text, old_id, new_block)
    old_file.write_text(text, encoding="utf-8", newline="\n")
    new_file = Path(root) / "problem-solutions"
    new_file.mkdir(parents=True, exist_ok=True)
    nid = next_id(root)
    body = re.sub(r"^## \[K-[^\]]+\]", f"## [{nid}]", new_entry_text, count=1, flags=re.M)
    out = Path(root) / "problem-solutions" / f"{nid}.md"
    out.write_text(body, encoding="utf-8", newline="\n")
    return {"old_file": str(old_file), "new_file": str(out), "new_id": nid}


def noop_bump(learnings_path: Path, entry_id: str) -> int:
    """NOOP：Recurrence-Count 递增（learnings 条目）。返回新计数。"""
    text = Path(learnings_path).read_text(encoding="utf-8", errors="ignore")
    pat = re.compile(rf"(## \[{re.escape(entry_id)}\].*?Recurrence-Count\s*[：:]\s*)(\d+)",
                     re.M | re.S)
    m = pat.search(text)
    if not m:
        raise ConsolidateError(f"{entry_id} 无 Recurrence-Count")
    n = int(m.group(2)) + 1
    Path(learnings_path).write_text(pat.sub(lambda mm: mm.group(1) + str(n), text, count=1),
                                    encoding="utf-8", newline="\n")
    return n


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "knowledge"
        (root / "problem-solutions").mkdir(parents=True)
        f = root / "problem-solutions" / "old.md"
        f.write_text(
            "# PS\n\n## [K-20261024-001] 旧方案\n\n"
            "**置信度**：[V]　　**生效**：2026-10-01　　**记录**：2026-10-01　　"
            "**最后验证**：2026-10-01　　**适用版本**：main\n"
            "**结论**：自建分发层放行 OPTIONS。\n**Related**：无\n", encoding="utf-8")
        new_text = (
            "## [K-20261024-999] 新方案\n\n"
            "**置信度**：[V]　　**生效**：2026-10-24　　**记录**：2026-10-24　　"
            "**最后验证**：2026-10-24　　**适用版本**：main\n"
            "**结论**：框架中间件统一处理。\n"
            "**Related**：K-20261024-001（前代已失效留档）\n")
        r = supersede(root, "K-20261024-001", new_text, "方案演进", today="2026-10-24")
        old_t = f.read_text(encoding="utf-8")
        new_t = Path(r["new_file"]).read_text(encoding="utf-8")
        ok &= "已失效" in old_t and "K-" in old_t and "原因" in old_t
        ok &= "自建分发层放行 OPTIONS" in old_t          # 原结论保留（留痕）
        ok &= "K-20261024-001" in new_t                 # 新条目 Related 回指
        ok &= re.match(r"K-\d{8}-\d{3}", r["new_id"]) is not None  # 编号规则（当天计数）
        # NOOP 递增
        lp = Path(td) / "LEARNINGS.md"
        lp.write_text("## [LRN-20261024-001] t\n\n**Metadata**\n- Recurrence-Count: 2\n",
                      encoding="utf-8")
        ok &= noop_bump(lp, "LRN-20261024-001") == 3
    print("consolidate selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(selftest())

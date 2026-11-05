"""core.snapshot — HANDOFF §0 当前快照的生成与刷新（文件级操作）。

核心规则在 store（parse_snapshot/render_snapshot/refresh_handoff/validate_snapshot）；
本模块提供文件级封装：read_file / refresh_file（fail-closed：七槽位缺一拒绝写入）。

自测: `python -m core.snapshot`
"""
from __future__ import annotations

from pathlib import Path

from . import store


class SnapshotError(Exception):
    pass


def read_file(path: str | Path) -> dict:
    """读 HANDOFF 的 §0 快照为槽位 dict；无 §0 返回 {}。"""
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="ignore")
    return store.parse_snapshot(text)


def refresh_file(path: str | Path, state: dict, strict: bool = True) -> dict:
    """刷新 HANDOFF 的 §0（编年部分原样保留）。strict=True 时七槽位缺一拒绝。

    返回 {"missing": [...], "written": True}。
    """
    p = Path(path)
    if not p.exists():
        raise SnapshotError(f"{p} 不存在——首版请走 intake-scaffold，不在此处创建")
    missing = store.validate_snapshot(state)
    if missing and strict:
        raise SnapshotError("快照缺槽位: " + "; ".join(missing) +
                            "——状态三态与七槽位必须写实，拒绝半成品快照")
    text = p.read_text(encoding="utf-8", errors="ignore")
    new = store.refresh_handoff(text, state)
    p.write_text(new, encoding="utf-8", newline="\n")
    return {"missing": missing, "written": True}


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "HANDOFF.md"
        p.write_text(
            "# HANDOFF · t\n\n> 读法：先读 §0\n\n"
            "## ★0. 当前快照\n\n- **目标**：旧\n\n## ★1. 会话概览\n- keep\n",
            encoding="utf-8")
        # strict：缺槽位拒绝
        try:
            refresh_file(p, {"目标": "x"}, strict=True)
            ok = False
        except SnapshotError:
            pass
        # 全槽位写入成功，编年保留
        state = {k: "v" for k in ("目标", "需求与约束", "关键决策", "状态",
                                  "下一步动作", "相关文件", "关键上下文")}
        state["目标"] = "新目标"
        r = refresh_file(p, state, strict=True)
        ok &= r["written"] and not r["missing"]
        t = p.read_text(encoding="utf-8")
        ok &= "目标**：新目标" in t and "## ★1. 会话概览" in t and "- keep" in t
        # read 回读一致
        ok &= read_file(p).get("目标") == "新目标"
    print("snapshot selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(selftest())

"""core.store — 四套记忆格式的读写与 schema 校验（fail-closed）。

四套格式（与 super-memory 格式契约同步）：
  learnings  暂存层  `## [LRN-YYYYMMDD-NNN] 标题` + **Logged** 等英文字段
  knowledge  长期库  `## [K-YYYYMMDD-NNN] 标题` + **置信度/生效/记录/最后验证/适用版本** 头行
  hostlib    宿主库  YAML frontmatter（name/description/last_verified/metadata.type）
  handoff    交接    §0 快照七槽位 + 十节编年

数据结构：Entry（dataclass）——id/title/fields(dict)/meta(dict)/body(str)。
解析宽容（issues 收集），写入严格（ValidationError 拒绝）。
自测：`python -m core.store`
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CONF = re.compile(r"^\[[VF]\]$")


class ValidationError(Exception):
    """schema 校验失败（fail-closed）。"""

    def __init__(self, fmt: str, errors: list[str]):
        self.fmt = fmt
        self.errors = errors
        super().__init__(f"[{fmt}] schema 校验失败: " + "; ".join(errors))


@dataclass
class Entry:
    fmt: str
    id: str = ""
    title: str = ""
    fields: dict = field(default_factory=dict)   # **键**：值（去星号与冒号后）
    meta: dict = field(default_factory=dict)     # frontmatter 或 Metadata 列表
    body: str = ""                               # 除字段外的正文
    issues: list = field(default_factory=list)   # 解析期发现的问题（宽容）


# ── 通用小块 ─────────────────────────────────────────────

def _split_blocks(text: str, head_re):
    """按标题行切块；yield (id, title, block_text)。head_re 为已编译正则（含 re.M）。"""
    matches = list(head_re.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.end():end]
        title = m.group("title").strip()
        eid = m.groupdict().get("id", "") or ""
        yield eid.strip(), title, block


def _field(block: str, key: str):
    """取 **键**：值 / **Key**: 值 / - Key: 值（宽松匹配冒号全半角）。"""
    m = re.search(rf"\*\*{re.escape(key)}\*\*[：:]\s*(.+)", block)
    if m:
        return m.group(1).strip()
    m = re.search(rf"-\s*{re.escape(key)}\s*[：:]\s*(.+)", block)
    return m.group(1).strip() if m else None


# ── learnings ────────────────────────────────────────────

_LEARN_HEAD = re.compile(r"^## \[(?P<id>[A-Z]+-\d{8}-\d+)]\s*(?P<title>.+)$", re.M)
_LEARN_FIELDS = ("Logged", "Priority", "Status", "Summary")


def parse_learnings(text: str) -> list[Entry]:
    out = []
    for eid, title, block in _split_blocks(text, _LEARN_HEAD):
        e = Entry("learnings", eid, title, body=block)
        for k in ("Logged", "Priority", "Status", "Category", "Area", "Summary",
                  "Details", "Suggested Action"):
            v = _field(block, k)
            if v:
                e.fields[k] = v
        for k in ("Source", "Related Files", "See Also", "Recurrence-Count", "Tags"):
            v = _field(block, k)
            if v:
                e.meta[k] = v
        if "Resolution" in block:
            e.fields["Resolution"] = _field(block, "Resolved") or "present"
        out.append(e)
    return out


def validate_learnings(e: Entry) -> list[str]:
    errs = []
    for k in _LEARN_FIELDS:
        if k not in e.fields:
            errs.append(f"缺字段 {k}")
    if "Logged" in e.fields and not DATE.match(e.fields["Logged"]):
        errs.append(f"Logged 非绝对日期: {e.fields['Logged']}")
    if "Status" in e.fields and e.fields["Status"] not in (
            "pending", "in_progress", "resolved", "wont_fix", "promoted"):
        errs.append(f"Status 非法: {e.fields['Status']}")
    if "Priority" in e.fields and e.fields["Priority"] not in (
            "critical", "high", "medium", "low"):
        errs.append(f"Priority 非法: {e.fields['Priority']}")
    return errs


def render_learnings(e: Entry) -> str:
    lines = [f"## [{e.id}] {e.title}", ""]
    for k in ("Logged", "Priority", "Status", "Category", "Area"):
        if k in e.fields:
            lines.append(f"**{k}**: {e.fields[k]}")
    lines.append("")
    if "Summary" in e.fields:
        lines += [f"**Summary**：{e.fields['Summary']}", ""]
    if "Details" in e.fields:
        lines += [f"**Details**：{e.fields['Details']}", ""]
    if "Suggested Action" in e.fields:
        lines += [f"**Suggested Action**：{e.fields['Suggested Action']}", ""]
    if e.meta:
        lines.append("**Metadata**")
        for k in ("Source", "Related Files", "See Also", "Recurrence-Count", "Tags"):
            if k in e.meta:
                lines.append(f"- {k}: {e.meta[k]}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ── knowledge ────────────────────────────────────────────

_K_HEAD = re.compile(r"^## \[(?P<id>K-\d{8}-\d+)]\s*(?P<title>.+)$", re.M)
_K_HEADER_FIELDS = ("置信度", "生效", "记录", "最后验证", "适用版本")


def parse_knowledge(text: str) -> list[Entry]:
    out = []
    for eid, title, block in _split_blocks(text, _K_HEAD):
        e = Entry("knowledge", eid, title, body=block)
        head = re.search(r"\*\*置信度\*\*[：:](.+)", block)
        if head:
            parts = [p.strip() for p in head.group(1).split("　") if p.strip()]
            for p in parts:
                kv = re.match(r"\*\*([^*]+)\*\*[：:]\s*(.+)", p)
                if kv:
                    e.fields[kv.group(1)] = kv.group(2).strip()
                elif re.match(r"^\[[VF]\]$", p):
                    e.fields["置信度"] = p
        for k in ("适用场景", "不适用", "结论", "根因/权衡", "锚点", "来源", "Related", "Tags"):
            v = _field(block, k)
            if v:
                e.fields[k] = v
        if "**已失效**" in block:
            m = re.search(r"\*\*已失效\*\*[：:]\s*(.+)", block)
            e.fields["已失效"] = m.group(1).strip() if m else "present"
        out.append(e)
    return out


def validate_knowledge(e: Entry) -> list[str]:
    errs = []
    for k in _K_HEADER_FIELDS:
        if k not in e.fields:
            errs.append(f"缺头行字段 {k}")
    conf = e.fields.get("置信度", "")
    if conf and not CONF.match(conf) and "已失效" not in e.fields:
        errs.append(f"置信度非 [V]/[F]: {conf}")
    for k in ("生效", "记录", "最后验证"):
        v = e.fields.get(k, "")
        if v and not DATE.match(v):
            errs.append(f"{k} 非绝对日期: {v}")
    if "已失效" in e.fields:
        inv = e.fields["已失效"]
        # 三要素硬校验：日期 + 取代者ID + 原因，缺一即报（日期是子串搜索，不用锚定的 DATE 常量）
        if not (re.search(r"\d{4}-\d{2}-\d{2}", inv) and re.search(r"K-\d{8}", inv) and "原因" in inv):
            errs.append("失效标记缺三要素（日期+取代者ID+原因）")
    elif "Related" not in e.fields:
        # Related 必填仅约束现役条目；已失效归档件由取代者持链接，豁免
        errs.append("缺 Related（无相关也须写'无'，不许留空）")
    return errs


def render_knowledge(e: Entry) -> str:
    head = "　　".join(
        f"**{k}**：{e.fields[k]}" for k in _K_HEADER_FIELDS if k in e.fields)
    lines = [f"## [{e.id}] {e.title}", ""]
    if head:
        lines.append(head)
    if "已失效" in e.fields:
        lines.append(f"**已失效**：{e.fields['已失效']}")
    lines.append("")
    for k in ("适用场景", "不适用", "结论", "根因/权衡", "锚点", "来源", "Tags", "Related"):
        if k in e.fields:
            lines.append(f"**{k}**：{e.fields[k]}")
    return "\n".join(lines).rstrip() + "\n"


# ── hostlib ──────────────────────────────────────────────

_FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", re.S)


def parse_hostlib(text: str, path_hint: str = "") -> list[Entry]:
    m = _FM.match(text)
    if not m:
        e = Entry("hostlib", path_hint, path_hint, body=text,
                  issues=["缺 frontmatter"])
        return [e]
    fm, body = m.group(1), m.group(2)
    meta, cur = {}, None
    for line in fm.splitlines():
        if not line.strip():
            continue
        kv = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        nested = re.match(r"^\s{2,}(\w[\w-]*):\s*(.*)$", line)
        if nested and cur:
            meta.setdefault(cur, {})[nested.group(1)] = nested.group(2).strip()
        elif kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val == "":
                cur = key
            else:
                meta[key] = val
                cur = None
    e = Entry("hostlib", meta.get("name", path_hint),
              meta.get("description", ""), meta=meta, body=body)
    return [e]


def validate_hostlib(e: Entry) -> list[str]:
    errs = []
    m = e.meta
    for k in ("name", "description"):
        if not m.get(k):
            errs.append(f"frontmatter 缺 {k}")
    if m.get("metadata", {}).get("type") not in ("user", "project", "feedback", "reference"):
        errs.append("metadata.type 非法（user|project|feedback|reference）")
    lv = m.get("last_verified")
    if lv and not DATE.match(lv):
        errs.append(f"last_verified 非绝对日期: {lv}")
    for bad in ("token", "password", "sk-", "api_key"):
        if bad.lower() in (e.body or "").lower() and "不写密钥" not in (e.body or ""):
            errs.append(f"正文疑似含敏感词 '{bad}'——按纪律密钥不进记忆库（人工确认）")
            break
    return errs


def render_hostlib(e: Entry) -> str:
    m = dict(e.meta)
    m.setdefault("name", e.id)
    lines = ["---"]
    for k, v in m.items():
        if isinstance(v, dict):
            lines.append(f"{k}:")
            for k2, v2 in v.items():
                lines.append(f"  {k2}: {v2}")
        else:
            lines.append(f"{k}: {v}")
    lines += ["---", "", e.body.rstrip()]
    return "\n".join(lines) + "\n"


# ── handoff（§0 快照部分；编年节由 caller 管理）──────────

_SNAP_SLOTS = ("目标", "需求与约束", "关键决策", "状态", "下一步动作", "相关文件", "关键上下文")


_SNAP_HEAD = re.compile(r"^## [★§]0\.?\s*当前快照.*$", re.M)
_SNAP_BLOCK = re.compile(r"^## [★§]0\.?\s*当前快照.*?(?=^## |\Z)", re.M | re.S)


def parse_snapshot(text: str) -> dict:
    m = _SNAP_BLOCK.search(text)
    if not m:
        return {}
    state = {}
    for line in m.group(0).splitlines()[1:]:
        s = re.match(r"^-\s*\*\*([^*]+)\*\*[：:]\s*(.*)$", line)
        if s:
            state[s.group(1)] = s.group(2).strip()
    return state


def validate_snapshot(state: dict) -> list[str]:
    return [f"快照缺槽位 {k}" for k in _SNAP_SLOTS if not state.get(k)]


def render_snapshot(state: dict, marker: str = "★0") -> str:
    lines = [f"## {marker}. 当前快照（接手者第一眼；每次追加先刷新本节，再追加编年节）", ""]
    for k in _SNAP_SLOTS:
        lines.append(f"- **{k}**：{state.get(k, '（待填）')}")
    return "\n".join(lines) + "\n"


def refresh_handoff(text: str, state: dict, marker: str = "★0") -> str:
    """替换 §0/★0 块（无则插在标题区之后）；编年部分原样保留。

    块头标记双认：★0（super-memory 模板）/ §0（agent-memory README）。
    替换是**块级**的：旧快照的标题与正文整体换掉，不留残行。
    """
    block = render_snapshot(state, marker)
    block_re = re.compile(r"^## [★§]0\. 当前快照.*?(?=^## |\Z)", re.M | re.S)
    if block_re.search(text):
        return block_re.sub(block + "\n", text, count=1)
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            return "".join(lines[:i]) + "\n" + block + "\n" + "".join(lines[i:])
    return text + "\n\n" + block


# ── 统一入口 ─────────────────────────────────────────────

_PARSERS = {"learnings": parse_learnings, "knowledge": parse_knowledge,
            "hostlib": parse_hostlib}
_VALIDATORS = {"learnings": validate_learnings, "knowledge": validate_knowledge,
               "hostlib": validate_hostlib}
_RENDERERS = {"learnings": render_learnings, "knowledge": render_knowledge,
              "hostlib": render_hostlib}


def parse(fmt: str, text: str, path_hint: str = "") -> list[Entry]:
    if fmt not in _PARSERS:
        raise ValueError(f"未知格式: {fmt}")
    return _PARSERS[fmt](text, path_hint) if fmt == "hostlib" else _PARSERS[fmt](text)


def validate(fmt: str, e: Entry) -> list[str]:
    if fmt not in _VALIDATORS:
        raise ValueError(f"未知格式: {fmt}")
    return _VALIDATORS[fmt](e)


def render(fmt: str, e: Entry) -> str:
    if fmt not in _RENDERERS:
        raise ValueError(f"未知格式: {fmt}")
    return _RENDERERS[fmt](e)


def write_strict(fmt: str, e: Entry) -> str:
    """fail-closed 写入：校验不过抛 ValidationError，返回规范化文本。"""
    errs = validate(fmt, e)
    if errs:
        raise ValidationError(fmt, errs)
    return render(fmt, e)


# ── 自测 ────────────────────────────────────────────────

def selftest():
    ok = True

    # knowledge: 健康条目往返一致、缺字段被拒
    good = parse("knowledge", """## [K-20261024-001] t

**置信度**：[V]　　**生效**：2026-10-24　　**记录**：2026-10-24　　**最后验证**：2026-10-24　　**适用版本**：main

**结论**：ok
**Tags**：deploy rsync
**Related**：无
""")
    e = good[0]
    errs = validate("knowledge", e)
    ok &= not errs
    back = parse("knowledge", render("knowledge", e))[0]
    ok &= validate("knowledge", back) == []

    bad = Entry("knowledge", "K-20261024-002", "x", fields={"结论": "缺头行"})
    ok &= bool(validate("knowledge", bad))          # 缺五字段+Related 必须被拒

    # 失效三要素校验
    sup = parse("knowledge", """## [K-20261024-003] old

**置信度**：[V]　　**生效**：2026-10-24　　**记录**：2026-10-24　　**最后验证**：2026-10-24　　**适用版本**：main
**已失效**：2026-10-24 起废弃。
""")
    ok &= any("三要素" in x for x in validate("knowledge", sup[0]))

    # learnings: 骨架字段
    l = parse("learnings", """## [LRN-20261024-001] t

**Summary**：x
""")
    ok &= any("Logged" in x for x in validate("learnings", l[0]))

    # hostlib: type 非法 + 敏感词
    h = parse("hostlib", "---\nname: x\ndescription: y\nmetadata:\n  type: secret\n---\nbody with sk-abc123\n")
    ok &= len(validate("hostlib", h[0])) >= 2

    # snapshot: 七槽位 + 刷新
    st = parse_snapshot("## ★0. 当前快照\n\n- **目标**：t\n- **状态**：已完成 x · 进行中 y · 阻塞 无\n")
    ok &= validate_snapshot(st) == ["快照缺槽位 需求与约束", "快照缺槽位 关键决策",
                                    "快照缺槽位 下一步动作", "快照缺槽位 相关文件",
                                    "快照缺槽位 关键上下文"]
    doc = "# H\n\n## ★0. 当前快照\n\n- **目标**：旧\n\n## ★1. 会话概览\n- keep\n"
    r = refresh_handoff(doc, {"目标": "新", "状态": "已完成 a · 进行中 b · 阻塞 无",
                              "下一步动作": "c", "需求与约束": "-", "关键决策": "-",
                              "相关文件": "-", "关键上下文": "-"})
    ok &= "目标**：新" in r and "目标**：旧" not in r   # 块级替换：旧正文无残留
    ok &= "## ★1. 会话概览" in r and "- keep" in r       # 编年部分原样保留

    print("store selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest())

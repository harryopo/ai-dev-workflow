"""core.retrieval — 记忆排序检索（BM25-lite + CJK 二元组 + Tags 加权）。

从 super-memory scripts/search.py 演进：多查询合并、多库检索、Tags 字段加权。
纯标准库；与 scripts/search.py 同算法（M1 期间两处并存，安装位暂独立）。

用法:
  from core import retrieval
  hits = retrieval.search(["git 提交 门禁"], roots=[Path(".ai"), Path.home()/".qoder/memory"], top=10)
自测: `python -m core.retrieval`
"""
from __future__ import annotations

import math
import re
from pathlib import Path

NOISE = ("/node_modules/", "/.git/", "/dist/", "/build/", "/.mimosa/",
         "/.venv/", "/venv/", "/opensource-reference/", "/.trae/", "/htmlcov/")
CJK = re.compile(r"[\u4e00-\u9fff]")

# 换词三连的同义词表（检索纪律的机器可读版；可按需追加）
SYNONYMS = {
    "错误": ["踩坑", "failure"], "踩坑": ["错误", "pitfall"],
    "交接": ["进度", "handoff"], "进度": ["交接", "progress"],
    "决策": ["拍板", "decision"], "门禁": ["拦截", "gate"],
    "提交": ["commit"], "部署": ["deploy"],
}


def terms(text: str) -> list[str]:
    r"""中英混合切词：拉丁词按 \w 切，CJK 按单字+二元组。"""
    out = []
    for w in re.findall(r"[a-zA-Z0-9_]+", text.lower()):
        if len(w) > 1:
            out.append(w)
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        out.extend(run[i:i + 2] for i in range(len(run) - 1))
        if len(run) == 1:
            out.append(run)
    return out


def expand(query: str) -> list[str]:
    """换词三连的机器版：原查询 + 同义词替换的变体查询。"""
    variants = [query]
    for word, subs in SYNONYMS.items():
        if word in query:
            for s in subs:
                variants.append(query.replace(word, s))
    return list(dict.fromkeys(variants))


def _score_file(path: Path, q_terms, avg_len: float, k1=1.5, b=0.75):
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0.0, []
    tf, total, hits = {}, 0, []
    for i, line in enumerate(raw.splitlines(), 1):
        weight = 3.0 if line.lstrip().startswith("#") else 1.0
        if "**Tags**" in line or line.startswith("- Tags:"):
            weight = 4.0  # Tags 行加权：同义命中主通道
        lt = terms(line)
        total += len(lt)
        for t in set(q_terms):
            c = lt.count(t)
            if c:
                tf[t] = tf.get(t, 0) + c * weight
                if len(hits) < 3 and t in terms(line):
                    hits.append((i, line.strip()[:110]))
    if not q_terms or total == 0:
        return 0.0, []
    score = 0.0
    for t in q_terms:
        f = tf.get(t, 0)
        if f:
            idf = math.log(1 + 1.0)
            score += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * total / max(avg_len, 1)))
    return score, hits


def _iter_md(root: Path, pattern: str = "*.md"):
    for p in root.rglob(pattern):
        s = p.as_posix()
        if any(n in "/" + s for n in NOISE):
            continue
        if p.is_file():
            yield p


def search(queries, roots, top: int = 10, pattern: str = "*.md") -> list[dict]:
    """多查询 × 多库合并检索。

    queries: 查询词列表（换词三连的各变体）；roots: 记忆位目录列表。
    返回 [{file, score, hits:[(line_no, text)]}]，按分数降序、跨库去重。
    """
    q_terms = []
    for q in queries:
        q_terms.extend(terms(q))
    if not q_terms:
        return []
    seen_files, results = set(), []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        files = list(_iter_md(root, pattern))
        avg = 200.0
        for p in files:
            key = p.resolve().as_posix()
            if key in seen_files:
                continue
            s, hits = _score_file(p, q_terms, avg)
            seen_files.add(key)
            if s > 0:
                results.append({"file": p, "score": s, "hits": hits})
    results.sort(key=lambda x: -x["score"])
    return results[:top]


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        (base / "libA").mkdir()
        (base / "libB").mkdir()
        (base / "libA" / "near.md").write_text(
            "# 门禁串联\n\n验证与提交串联必须 && 短路。\n", encoding="utf-8")
        (base / "libB" / "exact.md").write_text(
            "# 钩子拦截\n\n安全钩子（门禁）会拦截 git 提交：正解是终端直提。\n**Tags**：门禁 拦截 git\n",
            encoding="utf-8")
        # 先定库：两库都搜，真目标在 libB
        hits = search(["git 提交 门禁 拦截"], [base / "libA", base / "libB"], top=5)
        files = [h["file"].name for h in hits]
        ok &= "exact.md" in files and files.index("exact.md") < len(files) - 1
        exact = next(h for h in hits if h["file"].name == "exact.md")
        near = next((h for h in hits if h["file"].name == "near.md"), None)
        ok &= near is not None and exact["score"] > near["score"]  # 精确 > 近似
        # 换词扩展
        ok &= len(expand("git 提交 拦截")) >= 2
    print("retrieval selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(selftest())

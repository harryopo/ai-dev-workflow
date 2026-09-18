"""
validate_report.py — 调研报告质量校验门（Quality Gate）  [v6.0 新增]

发布前对"最终报告 md + 证据账本"执行确定性校验，作为闸门：
  校验 1 引用一致性：报告中每个 [N] 引用编号在账本中有对应来源
  校验 2 覆盖充分性：每 topic 至少 1 条 verified claim；全局覆盖率 ≥ 阈值
  校验 3 必需章节：报告包含「执行摘要 / 方法 / 结论 / 来源」四部分
  校验 4 低质源占比：Tier 4 来源占比 < 30%（否则告警）
  校验 5 摘要精简：执行摘要篇幅 ≤ 上限（防空洞）

设计约束：
- 纯确定性规则（正则 + 账本查询），不依赖 LLM，秒级返回
- 退出码：0 = 通过；1 = 未通过；2 = 参数/IO 错误
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ledger import ResearchLedger
except ImportError:
    try:
        from scripts.ledger import ResearchLedger  # 从 scripts/ 作为包运行时
    except ImportError:
        ResearchLedger = None  # type: ignore

DEFAULT_MIN_COVERAGE = 0.6
DEFAULT_MIN_SOURCES = 1
DEFAULT_MAX_SUMMARY_CHARS = 1200
REQUIRED_SECTIONS = {
    '执行摘要': ['执行摘要', '摘要', 'executive summary'],
    '方法': ['调研范围', '调研方法', '方法', 'methodology', '范围与方法'],
    '结论': ['结论', '结论与建议', 'conclusion'],
    '来源': ['来源', '参考资料', '参考文献', 'references'],
}


@dataclass
class ValidationReport:
    """校验结果。"""
    passed: bool
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 核心校验
# ---------------------------------------------------------------------------

def extract_citations(report_md: str) -> List[int]:
    """提取报告中的 [N] 数字引用编号。

    v6.3：排除引用定义行 `[N]:`（Markdown 链接定义）与 Markdown 链接 `[N](url)`，
    只统计正文引用。
    """
    return [int(x) for x in re.findall(r'\[(\d{1,3})\](?!\()(?!:)', report_md)]


def _section_missing(md: str, section: str, keywords: List[str]) -> bool:
    """只有标题行（# 开头）参与章节关键词匹配，避免正文提及造成误判。"""
    heading = ' '.join(l for l in md.splitlines() if re.match(r'^#{1,4}\s', l))
    low = heading.lower()
    for kw in keywords:
        if kw.lower() in low:
            return False
    return True


def validate_report(report_md: str,
                    ledger: Optional[Any] = None,
                    ledger_dir: Optional[str] = None,
                    min_coverage: float = DEFAULT_MIN_COVERAGE,
                    min_sources_per_claim: int = DEFAULT_MIN_SOURCES,
                    max_summary_chars: int = DEFAULT_MAX_SUMMARY_CHARS) -> ValidationReport:
    """执行全部校验项。ledger 与 ledger_dir 二选一。"""
    report = ValidationReport(passed=True, stats={
        'with_ledger': ledger is not None or ledger_dir is not None,
    })

    # ---------- 账本装载 ----------
    if isinstance(ledger, ResearchLedger):
        rep = ledger
    elif ledger_dir:
        rep = ResearchLedger(ledger_dir)
    else:
        rep = None

    # ---------- 校验 3：必需章节 ----------
    for section, kws in REQUIRED_SECTIONS.items():
        if _section_missing(report_md, section, kws):
            report.issues.append(f'「{section}」章节缺失（关键词: {"/".join(kws[:2])}）')

    # ---------- 校验 5：执行摘要篇幅 ----------
    m = re.search(r'(?:^|\n)#{1,3}\s*(?:执行摘要|摘要)\s*\n(.*?)(?=\n#{1,3}\s*\S)', report_md, re.S)
    if m:
        summary_chars = len(_strip_md(m.group(1)))
        report.stats['summary_chars'] = summary_chars
        if summary_chars > max_summary_chars:
            report.warnings.append(
                f'执行摘要过长（{summary_chars} 字 > 上限 {max_summary_chars}），建议精简')
    else:
        report.stats['summary_chars'] = 0

    if rep is None:
        # 无账本时只能做文本级校验
        if not report.issues:
            report.passed = True
        else:
            report.passed = False
        report.stats['mode'] = 'text-only'
        return report

    data = rep.export_json()
    claims = data['claims']
    sources = data['sources']
    stats = data['stats']

    # ---------- 校验 1：引用一致性（v6.3 强契约）----------
    refs = extract_citations(report_md)
    n_sources = len(sources)
    report.stats['citations'] = len(refs)
    report.stats['sources'] = n_sources
    if refs:
        out_of_range = [r for r in refs if r < 1 or r > n_sources]
        if out_of_range:
            report.issues.append(
                f'引用编号越界: {out_of_range[:10]}（账本来源数 {n_sources}）')
        if len(set(refs)) < len(refs):
            report.warnings.append('引用编号存在重复，请核对顺序')
        # v6.3 反查：编号 N 的来源，其 URL/标题须能在报告正文或附录中找到
        # （不止"数字在范围内"，而是引用→具体来源可追溯）
        source_by_index = {s.get('primary_index'): s for s in sources}
        orphan_refs = []
        for r in sorted(set(refs)):
            s = source_by_index.get(r)
            if not s:
                if 1 <= r <= n_sources:      # 无 primary_index 的旧账本回退
                    s = sources[r - 1]
                else:
                    orphan_refs.append(r)
                    continue
            needle = (s.get('url') or '').strip()
            title = (s.get('title') or '').strip()
            if needle and needle not in report_md and (not title or title not in report_md):
                orphan_refs.append(r)
        if orphan_refs:
            report.issues.append(
                f'引用 [{", ".join(map(str, orphan_refs[:8]))}] 无法追溯到具体来源'
                f'（编号存在但对应 URL/标题未出现在报告中）——请补附录来源映射')

    # ---------- 校验 2：覆盖充分性 ----------
    total_claims = len(claims)
    verified_claims = sum(1 for c in claims if c.get('status') == 'verified')
    coverage = (verified_claims / total_claims) if total_claims else 0.0
    report.stats.update({
        'claims': total_claims, 'verified_claims': verified_claims,
        'coverage': round(coverage, 3), 'topics': len(stats),
    })
    if total_claims == 0:
        report.issues.append('账本为空：无任何 claim，无法支撑报告')
    elif coverage < min_coverage:
        report.issues.append(
            f'覆盖率不足: {coverage:.0%} < 阈值 {min_coverage:.0%}'
            f'（verified {verified_claims}/{total_claims}）')

    # 每 topic 至少 1 verified（v6.3：从 warning 升级为 issue——账本分主题后无已证实结论即拦截）
    for t, s in stats.items():
        if s.get('verified', 0) < 1:
            report.issues.append(
                f'子主题「{t}」无 verified claim（{s.get("claims", 0)} 条均非已证实）')

    # ---------- 校验 2b（v6.3）：verified claim 独立来源强度 ----------
    # 每条被引为结论的 verified claim 必须有 ≥2 独立来源（v6.4：转载指纹去重后）
    try:
        from similarity import effective_independent_count
    except ImportError:
        effective_independent_count = lambda srcs, **kw: len({s.get('url') for s in srcs})
    weak_verified = []
    for c in claims:
        if c.get('status') != 'verified':
            continue
        claim_srcs = [s for s in sources if str(s.get('claim_id', '')) == str(c.get('id', ''))]
        n_indep = effective_independent_count(
            [{'title': s.get('title', ''), 'url': s.get('url', ''), 'tier': s.get('tier')}
             for s in claim_srcs])
        if n_indep < max(2, min_sources_per_claim):
            weak_verified.append(c.get('id'))
    report.stats['weak_verified_claims'] = len(weak_verified)
    if total_claims and weak_verified:
        report.issues.append(
            f'{len(weak_verified)} 条 verified claim 独立来源不足（<2）：'
            f'{"、".join(map(str, weak_verified[:5]))}——需补充交叉验证或降级为 pending')

    # ---------- 校验 6（v6.3）：开源调研六维要素 ----------
    # 报告含候选仓库链接（GitHub/Gitee）时，检查六维质量门要素是否齐备
    repo_links = re.findall(r'https://(?:github|gitee)\.com/[\w.-]+/[\w.-]+', report_md)
    if repo_links:
        required_dims = {
            '风险标签': ('🔴', '高风险', '🟠', '中风险', '🟢', '低风险', '风险'),
            '许可证': ('许可证', 'License', 'MIT', 'GPL', 'Apache'),
            '维护/最近提交': ('最近提交', '维护', '停更', 'pushed', '活跃'),
            '适配性': ('适配', '兼容', '技术栈', '改造'),
            '落地成本/计划': ('落地', '成本', '灰度', '回滚', '改造范围'),
            '量化指标': ('指标', '基线', '量化', '预期'),
        }
        missing_dims = [name for name, kws in required_dims.items()
                       if not any(kw in report_md for kw in kws)]
        report.stats['opensource_repos'] = len(set(repo_links))
        if missing_dims:
            report.issues.append(
                f'开源调研六维质量门缺失维度: {"、".join(missing_dims)}'
                f'（报告含 {len(set(repo_links))} 个候选仓库链接）')

    # ---------- 校验 4：低质源占比 ----------
    if sources:
        low = sum(1 for s in sources if s.get('tier') == 4)
        low_ratio = low / len(sources)
        report.stats['low_quality_ratio'] = round(low_ratio, 3)
        if low_ratio >= 0.3:
            report.warnings.append(
                f'低质源（Tier4）占比 {low_ratio:.0%} ≥ 30%，建议补充权威来源后复核')
    else:
        report.stats['low_quality_ratio'] = 0.0
        report.warnings.append('账本中无来源记录，引用链路为空')

    report.stats['mode'] = 'full'
    report.passed = not report.issues
    return report


def _strip_md(text: str) -> str:
    return re.sub(r'[*_`#>|\[\]()]', '', text).strip()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main(argv: Optional[List[str]] = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        print('''\n用法:
  python validate_report.py --report <report.md> --ledger <ledger_dir>
            [--min-coverage 0.6] [--min-sources 1] [--max-summary 1200]''')
        return 0

    def _opt(name: str, default: str = '') -> str:
        # v6.3 容错：尾参缺失（防止 IndexError traceback）
        try:
            i = args.index(name)
        except ValueError:
            return default
        return args[i + 1] if i + 1 < len(args) else default

    report_path = _opt('--report')
    ledger_path = _opt('--ledger', '') or None
    if not report_path or not Path(report_path).exists():
        print(f'报告文件不存在: {report_path}', file=sys.stderr)
        return 2

    md = Path(report_path).read_text(encoding='utf-8', errors='ignore')
    result = validate_report(
        md,
        ledger_dir=ledger_path,
        min_coverage=float(_opt('--min-coverage', '0.6')),
        min_sources_per_claim=int(_opt('--min-sources', '1')),
        max_summary_chars=int(_opt('--max-summary', '1200')),
    )
    import json
    print(json.dumps({
        'passed': result.passed,
        'stats': result.stats,
        'issues': result.issues,
        'warnings': result.warnings,
    }, ensure_ascii=False, indent=2))
    return 0 if result.passed else 1


if __name__ == '__main__':
    sys.exit(_main())
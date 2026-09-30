# -*- coding: utf-8 -*-
"""v6.15 搜索准确度/广度缺陷收口的回归测试。

对应《搜索准确度与广度缺陷清单》X-D16 ~ X-D21。
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ============================================================
# X-D16：编排层把检索参数透传给引擎
# ============================================================

class _Args:
    """最小 argparse 替身：只提供 helper 会读到的属性。"""

    def __init__(self, **kw):
        self.time_range = ''
        self.include_domain = None
        self.exclude_domain = None
        self.effort = None
        self.depth = 'standard'
        for k, v in kw.items():
            setattr(self, k, v)


def test_kwargs_empty_when_nothing_specified():
    """不带任何参数时不得凭空造键——否则引擎行为会与改动前不同。"""
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(_Args(), search_depth='basic')
    assert kw == {'search_depth': 'basic'}


def test_kwargs_omit_empty_values():
    """空串 / 空列表不得进 kwargs：传空值 != 不传，语义不同。"""
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(time_range='', include_domain=[], exclude_domain=[]),
        search_depth='')
    assert kw == {}


def test_kwargs_carry_all_four_params():
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(time_range='month',
              include_domain=['arxiv.org', 'nature.com'],
              exclude_domain=['csdn.net']),
        search_depth='advanced')
    assert kw['search_depth'] == 'advanced'
    assert kw['time_range'] == 'month'
    assert kw['include_domains'] == ['arxiv.org', 'nature.com']
    assert kw['exclude_domains'] == ['csdn.net']


def test_kwargs_strip_whitespace_in_domains():
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(include_domain=[' arxiv.org ', '  ']), search_depth='')
    assert kw['include_domains'] == ['arxiv.org']


# ============================================================
# X-D17：主入口能控制 Tavily 检索深度
# ============================================================

@pytest.mark.parametrize('effort,depth,expected', [
    (None,  'quick',    'fast'),
    (None,  'standard', 'basic'),
    ('deep', None,      'advanced'),
    ('exhaustive', None, 'advanced'),
    (None,  'extreme',  'advanced'),
])
def test_search_depth_derived_from_effort(effort, depth, expected):
    """未显式指定时按档位推导——这是最便宜的一个准确度杠杆，不该让用户手填。"""
    from research import _resolve_search_depth
    assert _resolve_search_depth(_Args(effort=effort, depth=depth),
                                 explicit=None) == expected


def test_search_depth_explicit_overrides_effort():
    from research import _resolve_search_depth
    assert _resolve_search_depth(_Args(effort='deep'),
                                 explicit='ultra-fast') == 'ultra-fast'


def test_search_depth_never_depends_on_unknown_effort_word():
    """exhaustive 归一为 extreme；直接拿 effort 原词查表会落空，此处防回归。"""
    from research import _resolve_search_depth
    assert _resolve_search_depth(_Args(effort='exhaustive'),
                                 explicit=None) == 'advanced'


def test_search_py_depth_accepts_four_tavily_levels():
    """search.py 的 --depth 是 Tavily 检索深度，真实有 4 档，此前只给 2 档。"""
    import re
    src = (Path(__file__).resolve().parent.parent / 'search.py').read_text(
        encoding='utf-8')
    m = re.search(r"'--depth'.*?choices=\[([^\]]+)\]", src, re.S)
    assert m, 'search.py 未找到 --depth 的 choices'
    levels = set(re.findall(r"'([\w-]+)'", m.group(1)))
    assert levels == {'ultra-fast', 'fast', 'basic', 'advanced'}


# ============================================================
# X-D18：每个子问题按信息需求类型扇出 3~5 条查询
# X-D20：检索算子进查询生成层
# ============================================================

@pytest.mark.parametrize('preset', ['quick', 'standard', 'deep', 'extreme'])
def test_each_subquestion_gets_3_to_5_faceted_queries(preset):
    from plan import build_query_facets
    n = len(build_query_facets('向量数据库选型', preset))
    assert 3 <= n <= 5, f'{preset} 档产出 {n} 条，应为 3~5'


def test_queries_are_typed_not_synonymous():
    """同义改写等于白搜：多条必须落在不同信息需求类型上。"""
    from plan import build_query_facets
    facets = build_query_facets('RAG 框架选型', 'deep')
    kinds = {f['facet'] for f in facets}
    assert len(kinds) == len(facets), '存在同类型重复查询'


def test_facet_queries_differ_from_each_other():
    from plan import build_query_facets
    qs = [f['query'] for f in build_query_facets('RAG 框架选型', 'deep')]
    assert len(set(qs)) == len(qs), '生成了字面重复的查询'


def test_only_primary_facet_uses_search_operators():
    """算子只在原始文档类使用——加在 fact/data 上会收窄过头导致 0 结果。"""
    from plan import build_query_facets
    for f in build_query_facets('向量数据库', 'extreme'):
        has_op = any(op in f['query'] for op in ('site:', 'filetype:', 'intitle:'))
        assert has_op == (f['facet'] == 'primary'), \
            f"{f['facet']} 类算子使用不当: {f['query']}"


def test_at_most_one_operator_per_query():
    """一条查询最多 1 个算子：两个以上会过度收窄，直接导致 0 结果。"""
    from plan import build_query_facets
    for f in build_query_facets('向量数据库', 'extreme'):
        hits = sum(f['query'].count(op)
                   for op in ('site:', 'filetype:', 'intitle:'))
        assert hits <= 1, f'单条查询用了 {hits} 个算子: {f["query"]}'


def test_legacy_plan_without_query_facets_still_loads():
    """旧 session 的 plan.json 没有 query_facets，续跑不得崩。

    ResearchPlan.from_dict() 走 SubQuestion(**q)，缺 key 会直接 TypeError，
    所以必须验证白名单化之后旧数据能原样载入。
    """
    from plan import ResearchPlan
    legacy = {
        'topic': '旧主题', 'goal': '', 'depth': 'standard',
        'dimensions': ['性能'], 'time_range': '', 'language': '', 'region': '',
        'issue_tree': [{
            'id': 'q-1', 'question': '旧子问题', 'hypothesis': 'h',
            'data_sources': ['tavily'], 'depth': 0, 'parent_id': None,
            'keywords': ['性能'], 'status': 'pending', 'search_count': 0,
            'findings_count': 0, 'evidence': [], 'confidence': 0.0,
            'search_queries': [], 'reflection_notes': [], 'perspectives': [],
            'evidence_count': 0, 'children': [],
            # 注意：没有 query_facets，正是 v6.14 存盘的形状
        }],
        'created_at': '2026-01-01T00:00:00', 'estimated_duration': '',
        'estimated_sources': 0, 'unanswered_questions': [],
        'dropped_dimensions': [],
    }
    plan = ResearchPlan.from_dict(legacy)
    assert plan.issue_tree[0].query_facets == []


def test_generated_plan_populates_facets_on_subquestions():
    from plan import PlanGenerator
    plan = PlanGenerator().generate_plan(
        topic='向量数据库选型',
        dimensions=['性能', '生态', '成本', '风险', '落地'],
        effort='deep')
    assert plan.issue_tree
    for q in plan.issue_tree:
        assert q.query_facets, f'子问题未生成扇出查询: {q.question}'
        assert len(q.query_facets) >= 3


# ============================================================
# X-D19：MCP 路径默认取正文而非只取摘要
# ============================================================

def test_mcp_default_requests_raw_content():
    src = (Path(__file__).resolve().parent.parent / 'engines' / 'mcp_engines.py') \
        .read_text(encoding='utf-8')
    assert '"include_raw_content": kwargs.get("include_raw_content", True)' in src, \
        'MCP 路径仍默认只要摘要'


# ============================================================
# X-D21：高风险 claim 规则筛查（账本污染防护）
# ============================================================

@pytest.mark.parametrize('text,kind', [
    ('该框架延迟低于 50ms', 'quantitative'),
    ('吞吐达到 12000 QPS', 'quantitative'),
    ('所有用户都采用此方案', 'absolute'),
    ('这是目前最好的方案', 'absolute'),
    ('该方案优于竞品', 'comparative'),
    ('性能远超同类产品', 'comparative'),
])
def test_high_risk_claims_are_screened(text, kind):
    from validate_report import screen_high_risk_claims
    hits = screen_high_risk_claims([{'id': 'c-1', 'text': text}])
    assert len(hits) == 1, f'{text!r} 应命中 1 条，实际 {len(hits)}'
    assert hits[0]['kind'] == kind
    assert hits[0]['claim_id'] == 'c-1'


def test_ordinary_claims_not_flagged():
    """误杀率必须低的样本：正常陈述句不该被拉进待查清单。"""
    from validate_report import screen_high_risk_claims
    ordinary = [
        {'id': 'c-1', 'text': '该项目采用 MIT 许可证'},
        {'id': 'c-2', 'text': '仓库最近一次提交在 2026 年 8 月'},
        {'id': 'c-3', 'text': '官方文档描述了部署步骤'},
        {'id': 'c-4', 'text': '该项目支持 Python 与 JavaScript 两种语言'},
    ]
    assert screen_high_risk_claims(ordinary) == []


def test_screening_does_not_block_report():
    """X-D21 是筛出待查清单，不是阻断——阻断需要 LLM 判定，本轮明确不做。

    误把它写进 issues 会让高风险 claim 反而无法交付，等于逼 Lead 隐瞒风险。
    """
    from validate_report import screen_high_risk_claims
    report = _FakeReport()
    screen_high_risk_claims(
        [{'id': 'c-1', 'text': '该框架延迟低于 50ms'}], report=report)
    assert report.issues == [], '高风险筛查不得写入 issues（会阻断 --stamp）'
    assert report.stats['needs_support_check'] == 1
    assert report.warnings, '必须留下可读告警，不能静默'


def test_screening_never_deletes_or_downgrades():
    """只标记不改数据：删除即 DoS-by-poisoning，攻击者会故意植入特征词躲避。"""
    from validate_report import screen_high_risk_claims
    claims = [{'id': 'c-1', 'text': '所有用户都采用此方案', 'status': 'verified'}]
    snapshot = [dict(c) for c in claims]
    screen_high_risk_claims(claims)
    assert claims == snapshot, '筛查不得修改 claim 本身'


def test_screening_tolerates_empty_ledger():
    from validate_report import screen_high_risk_claims
    assert screen_high_risk_claims([]) == []
    assert screen_high_risk_claims([{'id': 'c-1', 'text': ''}]) == []


# ============================================================
# 测试替身（须在使用它的测试之前定义）
# ============================================================

class _FakeReport:
    """最小 ValidationReport 替身。"""

    def __init__(self):
        self.issues = []
        self.warnings = []
        self.stats = {}

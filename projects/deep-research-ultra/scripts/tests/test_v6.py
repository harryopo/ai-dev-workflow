"""
Deep Research Ultra v6.0 — 新增模块单元测试

覆盖 v6.0 模块与增强：
- tier.py: domain_tier / tier_label / tier_penalty / 覆盖表
- ledger.py: ResearchLedger（init/append/merge/status/export，多子Agent并发写）
- panel.py: PanelReviewer（perspectives / review_outline / review_draft / supplement_questions）
- validate_report.py: validate_report（引用一致性/覆盖率/章节/Tier4占比/摘要长度）
- plan.py: 多视角注入 / evidence_count / unanswered_questions
- reflect.py: evidence_sufficiency / new_claim_marginal 停止信号
- score.py: Tier 加权 / has_low_quality_ratio

运行方式：
    cd scripts
    python -m pytest tests/ -v
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================
# tier.py
# ============================================================

class TestTier:
    """来源 Tier 分级"""

    def test_gov_edu_academic_tier1(self):
        from tier import domain_tier
        assert domain_tier('https://www.gov.cn/xinwen') == 1
        assert domain_tier('https://www.whitehouse.gov/x') == 1
        assert domain_tier('https://arxiv.org/abs/2402.14207') == 1
        assert domain_tier('https://www.stanford.edu/x') == 1
        assert domain_tier('https://content.example.edu.cn/x') == 1

    def test_authoritative_tier2(self):
        from tier import domain_tier
        assert domain_tier('https://docs.github.com/x') == 2
        assert domain_tier('https://www.reuters.com/x') == 2

    def test_community_tier4(self):
        from tier import domain_tier
        assert domain_tier('https://www.zhihu.com/question/1') == 4
        assert domain_tier('https://www.reddit.com/r/x') == 4

    def test_unknown_tier3_and_http_downgrade(self):
        from tier import domain_tier
        assert domain_tier('https://unknown-blog-abc.example.com/x') == 3
        # http 无 TLS → 降级
        assert domain_tier('http://old.example.edu.cn/x') == 2  # Tier1 → 2

    def test_override_persist(self, tmp_path, monkeypatch):
        import tier
        overrides_file = tmp_path / 'tier_overrides.json'
        monkeypatch.setattr(tier, '_OVERRIDES_FILE', overrides_file)
        tier.add_override('mycorp.example', 1)
        assert tier.domain_tier('https://mycorp.example/docs') == 1


# ============================================================
# ledger.py
# ============================================================

class TestLedger:
    """证据账本"""

    def test_init_structure(self, tmp_path):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        assert (tmp_path / 'ledger' / 'ledger.jsonl').exists()
        assert (tmp_path / 'ledger' / 'claims').is_dir()
        assert (tmp_path / 'ledger' / 'sources').is_dir()

    def test_add_claim_and_source(self, tmp_path):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('主流架构', 'topic-a', 'verified', 'domain_expert', 0.9)
        assert c['id'].startswith('c-')
        s = L.add_source(c['id'], 'https://arxiv.org/x', title='方案', tier=1)
        assert s['tier'] == 1
        # 未指定 tier 时自动分级
        s2 = L.add_source(c['id'], 'https://www.gov.cn/x')
        assert s2['tier'] == 1

    def test_status_sufficient(self, tmp_path):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('结论', 'topic-a', 'verified', 'general', 0.8)
        L.add_source(c['id'], 'https://arxiv.org/1')
        L.add_source(c['id'], 'https://arxiv.org/2')
        st = L.status('topic-a')
        assert st['independent_sources'] == 2
        assert st['sufficient'] is True
        # 单源 topic → 不充分
        c2 = L.add_claim('单源', 'topic-b', 'verified', 'general', 0.5)
        L.add_source(c2['id'], 'https://arxiv.org/3')
        assert L.status('topic-b')['sufficient'] is False

    def test_merge_subagent_artifacts(self, tmp_path):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        sub = tmp_path / 'sub'
        sub.mkdir()
        (sub / 'a.jsonl').write_text(
            json.dumps({'type': 'claim', 'id': 'c-sub1', 'text': '子A发现',
                        'topic': 't', 'status': 'verified', 'perspective': 'p', 'confidence': 0.6})
            + '\n', encoding='utf-8')
        (sub / 'a.jsonl').write_text(
            json.dumps({'type': 'claim', 'id': 'c-sub1', 'text': '子A发现',
                        'topic': 't', 'status': 'verified', 'perspective': 'p', 'confidence': 0.6})
            + '\n'
            + json.dumps({'type': 'source', 'claim_id': 'c-sub1', 'url': 'https://a.com/1',
                          'title': 'src', 'tier': 2}) + '\n', encoding='utf-8')
        c, s = L.merge(str(sub))
        assert c == 1 and s == 1
        # 再 merge 一次 → 幂等去重
        c2, s2 = L.merge(str(sub))
        assert c2 == 0 and s2 == 0

    def test_export_md(self, tmp_path):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('结论', 'topic-a', 'verified', 'general', 0.8)
        L.add_source(c['id'], 'https://arxiv.org/1', title='Attention')
        md = L.export_md()
        assert '## topic-a' in md
        assert '格式' in md or 'Attention' in md


# ============================================================
# panel.py
# ============================================================

class TestPanel:
    """专家团评审清单"""

    def test_default_perspectives_roles(self):
        from panel import PanelReviewer
        ps = PanelReviewer().default_perspectives()
        assert len(ps) == 5
        labels = [p['label'] for p in ps]
        assert '域专家' in labels and '怀疑者（红队）' in labels

    def test_review_outline_contract(self):
        from panel import PanelReviewer
        out = PanelReviewer().review_outline('1. 主题A', ['skeptic', 'practitioner'])
        assert set(out['perspectives'][0].keys()) == {'role', 'label', 'focus', 'questions'}
        assert all(q for p in out['perspectives'] for q in p['questions'])

    def test_review_draft_findings(self):
        from panel import PanelReviewer
        d = PanelReviewer().review_draft('草稿内容', 'domain_expert')
        assert set(d.keys()) == {'role', 'label', 'focus', 'findings', '_note'}
        assert all(f['type'] in ('gap', 'contradiction', 'evidence_needed')
                   for f in d['findings'])
        assert all('action' in f for f in d['findings'])


# ============================================================
# validate_report.py
# ============================================================

class TestValidateReport:
    """发布前校验门"""

    def _ledger_with_sources(self, tmp_path, n=3):
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c1 = L.add_claim('结论A', '主题A', 'verified', 'general', 0.9)
        c2 = L.add_claim('结论B', '主题A', 'verified', 'general', 0.8)
        for i in range(n):
            L.add_source(c1['id'], f'https://arxiv.org/{i}', tier=1)
        for i in range(n):
            L.add_source(c2['id'], f'https://arxiv.org/{i+100}', tier=1)
        return L

    def _good_report(self):
        return '''# 报告
## 执行摘要
结论A [1] 与结论B [2]。
## 调研范围与方法
多源检索。
## 结论与建议
结论良好。
## 来源
[1] 来源1 [2] 来源2
'''

    def test_pass(self, tmp_path):
        from validate_report import validate_report
        L = self._ledger_with_sources(tmp_path)
        r = validate_report(self._good_report(), ledger=L)
        assert r.passed is True

    def test_missing_section_fails(self, tmp_path):
        from validate_report import validate_report
        L = self._ledger_with_sources(tmp_path)
        bad = self._good_report().replace('## 来源', '## 附录')
        r = validate_report(bad, ledger=L)
        assert r.passed is False
        assert any('来源' in i for i in r.issues)

    def test_citation_out_of_range_fails(self, tmp_path):
        from validate_report import validate_report
        L = self._ledger_with_sources(tmp_path)
        bad = self._good_report().replace('[2]', '[99]')
        r = validate_report(bad, ledger=L)
        assert r.passed is False
        assert any('越界' in i for i in r.issues)

    def test_low_coverage_warns(self, tmp_path):
        from validate_report import validate_report
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('未验证', '主题X', 'pending', 'general', 0.5)  # 无 verified
        L.add_source(c['id'], 'https://arxiv.org/1')
        r = validate_report(self._good_report(), ledger=L, min_coverage=0.6)
        assert r.passed is False
        assert any('覆盖率' in i for i in r.issues)

    def test_low_quality_warning(self, tmp_path):
        from validate_report import validate_report
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('结论', '主题A', 'verified', 'general', 0.8)
        for i in range(4):
            L.add_source(c['id'], f'http://junk-{i}.example.com/x', tier=4)
        r = validate_report(self._good_report(), ledger=L)
        assert '告警' in str(r.warnings) or '低质源' in str(r.warnings)


# ============================================================
# plan.py（v6.0 增强）
# ============================================================

class TestPlanV6:
    """多视角注入 + unanswered_questions"""

    def test_perspectives_injected_by_default(self):
        from plan import PlanGenerator, DEFAULT_PERSPECTIVES
        plan = PlanGenerator().generate_plan('测试主题', depth='quick')
        assert plan.issue_tree
        assert plan.issue_tree[0].perspectives == DEFAULT_PERSPECTIVES

    def test_perspectives_disabled(self):
        from plan import PlanGenerator
        plan = PlanGenerator().generate_plan('测试主题', depth='quick', perspectives=[])
        assert plan.issue_tree[0].perspectives == []

    def test_perspectives_custom(self):
        from plan import PlanGenerator
        plan = PlanGenerator().generate_plan('测试主题', depth='quick', perspectives=['skeptic'])
        assert plan.issue_tree[0].perspectives == ['skeptic']

    def test_unanswered_questions_populated(self):
        from plan import PlanGenerator
        plan = PlanGenerator().generate_plan('测试主题', depth='quick')
        assert plan.unanswered_questions
        assert len(plan.unanswered_questions) == len(plan.get_leaf_questions())


# ============================================================
# reflect.py（v6.0 增强）
# ============================================================

class TestReflectV6:
    """证据充分性 / 边际 claim 收敛"""

    def test_insufficient_topics_continue(self, tmp_path):
        from reflect import Reflector
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('单源结论', '主题A', 'verified', 'general', 0.6)
        L.add_source(c['id'], 'https://arxiv.org/1', tier=1)  # 仅 1 独立来源
        plan = type('P', (), {'dimensions': ['主题A'], 'issue_tree': [],
                              'get_leaf_questions': lambda self: []})()
        ref = Reflector().reflect(plan, [], 0, None, ledger=L)
        assert '主题A' in ref.insufficient_topics
        assert ref.should_drill_down is True  # 证据不足 → 继续

    def test_low_quality_sources_reported(self, tmp_path):
        from reflect import Reflector
        from ledger import ResearchLedger
        L = ResearchLedger(str(tmp_path / 'ledger')).init()
        c = L.add_claim('结论', '主题A', 'verified', 'general', 0.8)
        L.add_source(c['id'], 'https://arxiv.org/1', tier=1)
        L.add_source(c['id'], 'http://junk.example.com/x', tier=4)
        plan = type('P', (), {'dimensions': ['主题A'], 'issue_tree': [],
                              'get_leaf_questions': lambda self: []})()
        ref = Reflector().reflect(plan, [], 0, None, ledger=L)
        assert any('junk' in u for u in ref.low_quality_sources)

    def test_marginal_convergence(self):
        from reflect import Reflector
        plan = type('P', (), {'dimensions': [], 'issue_tree': [],
                              'get_leaf_questions': lambda self: []})()
        # 覆盖率 0.6（达标线之上但低于阈值）+ 无空白 + 边际率 0.1 → 收敛停止
        r = Reflector()
        ok, reason, _ = r._should_continue(0, 0.6, [], 20,
                                           insufficient_topics=None, new_claim_marginal=0.1)
        assert ok is False
        assert '边际收益低' in reason or '收敛' in reason


# ============================================================
# score.py（v6.0 增强）
# ============================================================

class TestScoreV6:
    """Tier 加权 + 低质源占比"""

    def _score(self, url):
        from score import CraapScorer
        return CraapScorer().score({'title': 't', 'url': url, 'content': 'c' * 10,
                                    'published_date': '2026-01-01'}, query='t')

    def test_tier_field(self):
        s1 = self._score('https://www.gov.cn/x')
        s2 = self._score('http://junk-zz.example.com/x')
        assert s1['tier'] == 1 and s1['tier_label'] == '官方/学术'
        assert s2['tier'] == 4

    def test_tier_adjustment(self):
        s1 = self._score('https://www.gov.cn/x')
        s4 = self._score('http://junk-zz.example.com/x')
        assert s1['total'] > s4['total']  # Tier1 加权高于 Tier4

    def test_has_low_quality_ratio(self):
        from score import has_low_quality_ratio
        from score import CraapScorer
        scorer = CraapScorer()
        r1 = {'title': 'a', 'url': 'http://junk-1.example.com/x', 'content': 'x' * 5,
              'published_date': '2026-01-01'}
        r2 = {'title': 'b', 'url': 'https://arxiv.org/x', 'content': 'y' * 5,
              'published_date': '2026-01-01'}
        scored = [r1, r2]
        for r in scored:
            r['craap_score'] = scorer.score(r, 'x')
        assert has_low_quality_ratio(scored, 0.5) is True
        assert has_low_quality_ratio([r2], 0.3) is False


# ============================================================
# env_check.py（v6.1 环境分级门控）
# ============================================================

class TestEnvCheck:
    """环境分级清单 + 验证器"""

    def test_profiles_defined(self):
        from env_check import PROFILES
        for p in ('minimal', 'opensource', 'academic', 'full'):
            assert p in PROFILES
            assert 'desc' in PROFILES[p]

    def test_opensource_ready_without_optional(self, monkeypatch):
        from env_check import run_env_check
        # 核心必备通过（engines 真实可导入）；可选项缺失仅告警
        monkeypatch.setattr('env_check.shutil.which', lambda name: 'C:\\python.exe')
        monkeypatch.setattr('env_check._check_skill',
                            lambda name: (name == 'oss-finder', 'OK' if name == 'oss-finder' else 'missing'))
        monkeypatch.setattr('env_check._check_net', lambda host, timeout=3.0: (True, 'OK'))
        r = run_env_check('opensource', include_net=True)
        assert r.ready is True          # 可选缺失不阻断
        assert r.warnings               # GITHUB_TOKEN/agent-reach 等为告警

    def test_missing_core_blocks(self, monkeypatch):
        from env_check import run_env_check
        monkeypatch.setattr('env_check.shutil.which', lambda name: None)   # python 缺失 → 阻断
        monkeypatch.setattr('env_check._check_skill', lambda name: (True, 'OK'))
        monkeypatch.setattr('env_check._check_net', lambda host, timeout=3.0: (True, 'OK'))
        r = run_env_check('minimal', include_net=False)
        assert r.ready is False
        assert any(c.name == 'python' for c in r.missing)


# ============================================================
# engines/platform_engines.py（v6.1 国内开源平台）
# ============================================================

class TestPlatformEngines:
    """Gitee / ModelScope 引擎（mock 网络，不依赖外网）"""

    def _mock_get_json(self, monkeypatch, payload):
        import engines.platform_engines as pe
        monkeypatch.setattr(pe, '_http_get_json', lambda url: payload)
        monkeypatch.setattr(pe, '_host_reachable', lambda host, port=443, timeout=3.0: True)

    def test_gitee_parse(self, monkeypatch):
        from engines.platform_engines import GiteeEngine
        self._mock_get_json(monkeypatch, {
            'items': [{
                'full_name': 'oschina/gitee-test', 'html_url': 'https://gitee.com/oschina/x',
                'description': '测试仓库', 'pushed_at': '2026-09-01',
                'owner': {'login': 'oschina'}, 'stargazers_count': 123,
            }]})
        engine = GiteeEngine()
        results = engine.search('测试', max_results=3)
        assert results and results[0].source == 'gitee'
        assert results[0].title == 'oschina/gitee-test'
        assert results[0].url.startswith('https://gitee.com')
        assert engine.is_available() is True

    def test_modelscope_parse(self, monkeypatch):
        from engines.platform_engines import ModelScopeEngine
        self._mock_get_json(monkeypatch, {
            'Data': {'Model': {'Models': [{
                'Path': 'Qwen/Qwen2.5-7B', 'ChineseName': '通义千问',
                'Description': '测试模型', 'Task': 'text-generation',
            }]}}})
        engine = ModelScopeEngine()
        results = engine.search('Qwen', max_results=3)
        assert results and results[0].source == 'modelscope'
        assert 'modelscope.cn/models/Qwen/Qwen2.5-7B' in results[0].url
        assert engine.is_available() is True

    def test_network_failure_returns_none(self, monkeypatch):
        from engines.platform_engines import GiteeEngine
        import engines.platform_engines as pe
        monkeypatch.setattr(pe, '_http_get_json', lambda url: None)   # 网络失败
        monkeypatch.setattr(pe, '_host_reachable', lambda host, port=443, timeout=3.0: False)
        engine = GiteeEngine()
        assert engine.search('x') is None
        assert engine.is_available() is False


# ============================================================
# repo_health.py（v6.2 开源仓库健康/合规/风险扫描）
# ============================================================

class TestRepoHealth:
    """许可证分级 / 维护预警 / OSV 集成（mock API）"""

    def test_license_risk_levels(self):
        from repo_health import license_risk
        assert license_risk('MIT')[0] == 'permissive'
        assert license_risk('Apache-2.0')[0] == 'permissive'
        assert license_risk('LGPL-3.0')[0] == 'weak'
        assert license_risk('GPL-3.0')[0] == 'strong'
        assert license_risk('AGPL-3.0')[0] == 'strong'
        assert license_risk('')[0] == 'unknown'

    def test_parse_repo_ref(self):
        from repo_health import _parse_repo_ref
        assert _parse_repo_ref('langchain-ai/langchain')['host'] == 'github'
        r = _parse_repo_ref('https://gitee.com/oschina/hello-world')
        assert r == {'host': 'gitee', 'owner': 'oschina', 'repo': 'hello-world'}
        assert _parse_repo_ref('not-a-valid-ref!') is None

    def test_stale_repo_high_risk(self, monkeypatch):
        from repo_health import scan_repo
        import repo_health as rh
        monkeypatch.setattr(rh, '_get_json', lambda url: {
            'full_name': 'a/b', 'description': 'd', 'language': 'Python',
            'stargazers_count': 5, 'pushed_at': '2020-01-01T00:00:00Z',
            'archived': False, 'license': {'spdx_id': 'GPL-3.0'}})
        monkeypatch.setattr(rh, '_post_json', lambda url, p: {'vulnerabilities': [
            {'id': 'GHSA-x', 'summary': 's', 'aliases': ['CVE-2024-1']}]})
        h = scan_repo('a/b', with_cve_package='pypi:demo')
        assert h.api_ok
        assert h.overall() == 'high'
        cats = {r['category'] for r in h.risks}
        assert {'maintenance', 'license', 'security', 'adoption'} <= cats

    def test_archived_flag(self, monkeypatch):
        from repo_health import scan_repo
        import repo_health as rh
        monkeypatch.setattr(rh, '_get_json', lambda url: {
            'full_name': 'a/b', 'pushed_at': '2026-08-01T00:00:00Z', 'archived': True,
            'stargazers_count': 100, 'license': {'spdx_id': 'MIT'}})
        monkeypatch.setattr(rh, '_post_json', lambda url, p: None)
        h = scan_repo('a/b')
        assert any(r['category'] == 'maintenance' and '归档' in r['detail'] for r in h.risks)

    def test_api_unavailable(self, monkeypatch):
        from repo_health import scan_repo
        import repo_health as rh
        monkeypatch.setattr(rh, '_get_json', lambda url: None)
        h = scan_repo('a/b')
        assert h.api_ok is False
        assert any(r['category'] == 'api_unavailable' for r in h.risks)
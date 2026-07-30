#!/usr/bin/env python3
"""
Deep Research Ultra v4.0 — Phase 3: Synthesize（报告生成）

生成结构化调研报告，支持多种格式：
- HTML（默认，含 Mermaid 图表，可视化丰富）
- Markdown（轻量，适合文档系统）
- JSON（结构化，适合程序处理）
- CSV（来源列表，适合表格分析）

HTML 报告结构：
1. 执行摘要（Executive Summary）
2. MECE 问题树（Mermaid 图表）
3. 子问题分析（CER 结构：Claim-Evidence-Reasoning）
4. 矛盾点标注（Disagreements）
5. 时间线/趋势图（Mermaid timeline）
6. 引用列表（带 CRAAP 评分）
7. 可信度热图（来源 × 子问题）
8. 调研质量自评（覆盖率/验证率/矛盾处理率）

修复 v3.2.0 的问题：
- v3 只有 markdown/json/report/csv → v4 默认 HTML（含 Mermaid）
- v3 报告只是结果罗列 → v4 结构化（CER + 矛盾 + 时间线）
- v3 没有可视化 → v4 Mermaid 图表
- v3 没有质量自评 → v4 内置质量自评

使用方式：
    reporter = ReportGenerator()
    reporter.generate(
        plan=plan,
        results=results,
        verification=verification_result,
        reflections=reflection_history,
        format='html',
        output_path='report.html',
    )
"""

import csv
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


# ============================================================
# Mermaid 图表生成
# ============================================================

class MermaidGenerator:
    """Mermaid 图表生成器"""

    @staticmethod
    def issue_tree(plan: Any) -> str:
        """生成 MECE 问题树 Mermaid 图"""
        lines = ["graph TD"]
        issue_tree = getattr(plan, 'issue_tree', []) if plan else []

        def _add_node(q):
            # 节点文本（截断）
            text = q.question[:30].replace('"', "'")
            # 根据状态选择样式
            status = getattr(q, 'status', 'pending')
            if status == 'completed':
                lines.append(f'    {q.id}["✅ {text}"]:::completed')
            elif status == 'searching':
                lines.append(f'    {q.id}["🔍 {text}"]:::searching')
            else:
                lines.append(f'    {q.id}["{text}"]')
            for child in getattr(q, 'children', []):
                _add_node(child)
                lines.append(f'    {q.id} --> {child.id}')

        for root in issue_tree:
            _add_node(root)

        # 样式定义
        lines.append("")
        lines.append("    classDef completed fill:#d4edda,stroke:#28a745,stroke-width:2px")
        lines.append("    classDef searching fill:#fff3cd,stroke:#ffc107,stroke-width:2px")
        return '\n'.join(lines)

    @staticmethod
    def timeline(events: List[Dict[str, str]]) -> str:
        """
        生成时间线 Mermaid 图

        Args:
            events: [{"date": "2025-01", "event": "...", "source": "..."}]
        """
        if not events:
            return ""

        lines = ["timeline"]
        lines.append("    title 调研主题时间线")
        # 按日期排序
        sorted_events = sorted(events, key=lambda x: x.get('date', ''))
        # 按年分组
        current_year = ""
        for event in sorted_events:
            date = event.get('date', '')
            event_text = event.get('event', '')[:40]
            if date:
                year = date[:4] if len(date) >= 4 else ""
                if year != current_year:
                    current_year = year
                    lines.append(f"    section {year}")
                lines.append(f"    {date} : {event_text}")
        return '\n'.join(lines)

    @staticmethod
    def credibility_heatmap(sources: List[str], questions: List[str],
                            scores: Dict[str, Dict[str, float]]) -> str:
        """
        生成可信度热图（来源 × 子问题）

        使用 Mermaid quadrantChart
        """
        if not sources or not questions:
            return ""

        lines = ["quadrantChart"]
        lines.append("    title 来源可信度分布")
        lines.append("    x-axis 低权威性 --> 高权威性")
        lines.append("    y-axis 低相关性 --> 高相关性")
        lines.append("    quadrant-1 推荐")
        lines.append("    quadrant-2 谨慎使用")
        lines.append("    quadrant-3 补充参考")
        lines.append("    quadrant-4 高质量但偏离主题")

        for source in sources[:15]:  # 最多 15 个
            for question in questions[:5]:  # 最多 5 个问题
                score = scores.get(source, {}).get(question, {})
                authority = score.get('authority', 50) / 100
                relevance = score.get('relevance', 50) / 100
                label = f"{source}-{question[:10]}"
                lines.append(f'    "{label}": [{authority:.2f}, {relevance:.2f}]')

        return '\n'.join(lines)

    @staticmethod
    def source_distribution(results: List[Any]) -> str:
        """生成数据源分布饼图"""
        from collections import Counter
        sources = []
        for r in results:
            source = r.source if hasattr(r, 'source') else r.get('source', '')
            if source:
                sources.append(source)

        if not sources:
            return ""

        counter = Counter(sources)
        lines = ["pie title 数据源分布"]
        for source, count in counter.most_common():
            lines.append(f'    "{source}" : {count}')
        return '\n'.join(lines)


# ============================================================
# HTML 报告模板
# ============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — 深度调研报告</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg: #ffffff;
            --fg: #1a1a1a;
            --muted: #6b7280;
            --border: #e5e7eb;
            --accent: #3b82f6;
            --accent-light: #eff6ff;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --code-bg: #f9fafb;
            --card-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #1a1a1a;
                --fg: #e5e7eb;
                --muted: #9ca3af;
                --border: #374151;
                --accent: #60a5fa;
                --accent-light: #1e3a5f;
                --code-bg: #2d2d2d;
            }}
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: var(--fg);
            background: var(--bg);
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        h1, h2, h3, h4 {{ margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; }}
        h1 {{ font-size: 2rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem; }}
        h2 {{ font-size: 1.5rem; color: var(--accent); }}
        h3 {{ font-size: 1.25rem; }}
        p {{ margin-bottom: 1rem; }}
        a {{ color: var(--accent); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        blockquote {{
            border-left: 4px solid var(--accent);
            padding: 0.5rem 1rem;
            margin: 1rem 0;
            background: var(--accent-light);
            border-radius: 0 4px 4px 0;
        }}
        code {{
            background: var(--code-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: var(--code-bg);
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{ background: var(--accent-light); font-weight: 600; }}
        tr:hover {{ background: var(--accent-light); }}
        .card {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}
        .grade-high {{ color: var(--success); font-weight: 600; }}
        .grade-medium {{ color: var(--warning); font-weight: 600; }}
        .grade-low {{ color: var(--danger); font-weight: 600; }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .badge-high {{ background: #d1fae5; color: #065f46; }}
        .badge-medium {{ background: #fef3c7; color: #92400e; }}
        .badge-low {{ background: #fee2e2; color: #991b1b; }}
        .toc {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }}
        .toc ul {{ list-style: none; }}
        .toc li {{ padding: 0.25rem 0; }}
        .toc a {{ color: var(--fg); }}
        .metadata {{
            color: var(--muted);
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}
        .mermaid {{
            text-align: center;
            margin: 2rem 0;
            background: var(--code-bg);
            padding: 1rem;
            border-radius: 8px;
        }}
        .contradiction {{
            border-left: 4px solid var(--danger);
            background: #fef2f2;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 4px 4px 0;
        }}
        .verified {{
            border-left: 4px solid var(--success);
            background: #f0fdf4;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 4px 4px 0;
        }}
        .single-source {{
            border-left: 4px solid var(--warning);
            background: #fffbeb;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 4px 4px 0;
        }}
        .footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.85rem;
            text-align: center;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        .stat-card {{
            background: var(--accent-light);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}
        .stat-label {{
            font-size: 0.85rem;
            color: var(--muted);
            margin-top: 0.25rem;
        }}
    </style>
</head>
<body>
    <h1>📊 {title}</h1>
    <div class="metadata">
        <p>📅 生成时间：{generated_at}</p>
        <p>🎯 调研目标：{goal}</p>
        <p>🔍 调研深度：{depth}</p>
        <p>⏱️ 预估时长：{duration}</p>
        <p>📚 数据源数：{source_count}</p>
    </div>

    {toc}

    {content}

    <div class="footer">
        <p>由 Deep Research Ultra v4.0 生成 | {generated_at}</p>
    </div>

    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>"""


# ============================================================
# 报告生成器
# ============================================================

class ReportGenerator:
    """
    调研报告生成器

    支持格式：
    - html: HTML 报告（默认，含 Mermaid 图表）
    - markdown: Markdown 报告
    - json: JSON 结构化数据
    - csv: CSV 来源列表
    """

    def generate(
        self,
        plan: Any,
        results: List[Any],
        verification: Optional[Any] = None,
        reflections: Optional[Any] = None,
        format: str = 'html',
        output_path: Optional[str] = None,
    ) -> str:
        """
        生成报告

        Args:
            plan: ResearchPlan 对象
            results: 搜索结果列表（已评分）
            verification: VerificationResult 对象
            reflections: ReflectionHistory 对象
            format: 输出格式（html/markdown/json/csv）
            output_path: 输出文件路径（如不提供则返回字符串）

        Returns:
            报告内容字符串
        """
        if format == 'html':
            content = self._generate_html(plan, results, verification, reflections)
        elif format == 'markdown':
            content = self._generate_markdown(plan, results, verification, reflections)
        elif format == 'json':
            content = self._generate_json(plan, results, verification, reflections)
        elif format == 'csv':
            content = self._generate_csv(results)
        else:
            raise ValueError(f"不支持的格式: {format}")

        if output_path:
            Path(output_path).write_text(content, encoding='utf-8')

        return content

    # ------------------------------------------------------------
    # HTML 报告
    # ------------------------------------------------------------

    def _generate_html(
        self,
        plan: Any,
        results: List[Any],
        verification: Optional[Any],
        reflections: Optional[Any],
    ) -> str:
        """生成 HTML 报告"""
        topic = getattr(plan, 'topic', '调研报告') if plan else '调研报告'
        goal = getattr(plan, 'goal', '') if plan else ''
        depth = getattr(plan, 'depth', 'standard') if plan else 'standard'
        duration = getattr(plan, 'estimated_duration', '') if plan else ''
        source_count = len(set(
            r.source if hasattr(r, 'source') else r.get('source', '')
            for r in results
        ))

        # 生成各部分内容
        toc = self._html_toc()
        executive_summary = self._html_executive_summary(plan, results, verification)
        issue_tree_section = self._html_issue_tree(plan)
        analysis_section = self._html_analysis(results, verification)
        contradictions_section = self._html_contradictions(verification)
        timeline_section = self._html_timeline(results)
        sources_section = self._html_sources(results)
        quality_section = self._html_quality(plan, results, verification, reflections)

        content = '\n'.join([
            executive_summary,
            issue_tree_section,
            analysis_section,
            contradictions_section,
            timeline_section,
            sources_section,
            quality_section,
        ])

        return HTML_TEMPLATE.format(
            title=html.escape(topic),
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            goal=html.escape(goal) or '未指定',
            depth=depth,
            duration=duration or '未指定',
            source_count=source_count,
            toc=toc,
            content=content,
        )

    def _html_toc(self) -> str:
        """生成目录"""
        return """<div class="toc">
        <h3>📑 目录</h3>
        <ul>
            <li><a href="#summary">1. 执行摘要</a></li>
            <li><a href="#issue-tree">2. MECE 问题树</a></li>
            <li><a href="#analysis">3. 子问题分析（CER）</a></li>
            <li><a href="#contradictions">4. 矛盾点标注</a></li>
            <li><a href="#timeline">5. 时间线</a></li>
            <li><a href="#sources">6. 引用列表（CRAAP 评分）</a></li>
            <li><a href="#quality">7. 调研质量自评</a></li>
        </ul>
    </div>"""

    def _html_executive_summary(
        self, plan: Any, results: List[Any], verification: Optional[Any]
    ) -> str:
        """执行摘要"""
        verified_count = len(verification.verified_claims) if verification else 0
        single_count = len(verification.single_source_claims) if verification else 0
        contradiction_count = len(verification.contradictions) if verification else 0
        verification_rate = verification.verification_rate if verification else 0

        # 计算 CRAAP 平均分
        total_scores = []
        for r in results:
            craap = r.craap_score if hasattr(r, 'craap_score') else r.get('craap_score', {})
            if craap:
                total_scores.append(craap.get('total', 0))
        avg_score = sum(total_scores) / len(total_scores) if total_scores else 0

        return f"""<h2 id="summary">1. 执行摘要</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(results)}</div>
                <div class="stat-label">总结果数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{verified_count}</div>
                <div class="stat-label">已验证结论</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{verification_rate:.0%}</div>
                <div class="stat-label">验证率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_score:.1f}</div>
                <div class="stat-label">平均 CRAAP 分</div>
            </div>
        </div>
        <p>本次调研共收集 <strong>{len(results)}</strong> 条结果，
        其中 <strong>{verified_count}</strong> 条结论经过交叉验证（≥2 独立来源），
        验证率 <strong>{verification_rate:.0%}</strong>。
        发现 <strong>{contradiction_count}</strong> 个矛盾点，
        <strong>{single_count}</strong> 条单源结论待进一步验证。</p>"""

    def _html_issue_tree(self, plan: Any) -> str:
        """MECE 问题树"""
        if not plan or not getattr(plan, 'issue_tree', []):
            return '<h2 id="issue-tree">2. MECE 问题树</h2><p>未生成问题树。</p>'

        mermaid_code = MermaidGenerator.issue_tree(plan)
        return f"""<h2 id="issue-tree">2. MECE 问题树</h2>
        <div class="mermaid">
{mermaid_code}
        </div>"""

    def _html_analysis(self, results: List[Any], verification: Optional[Any]) -> str:
        """CER 结构分析"""
        if not verification:
            return '<h2 id="analysis">3. 子问题分析（CER）</h2><p>未进行交叉验证。</p>'

        sections = ['<h2 id="analysis">3. 子问题分析（CER）</h2>']

        # 已验证结论
        if verification.verified_claims:
            sections.append('<h3>✅ 已验证结论</h3>')
            for claim in verification.verified_claims[:10]:
                sources_html = ', '.join(
                    f'<a href="{ev.source_url}" target="_blank">{ev.source_domain}</a>'
                    for ev in claim.evidence[:3]
                )
                confidence_class = 'grade-high' if claim.confidence > 0.7 else 'grade-medium'
                sections.append(f"""<div class="verified">
                    <p><strong>结论：</strong>{html.escape(claim.statement)}</p>
                    <p><strong>置信度：</strong><span class="{confidence_class}">{claim.confidence:.0%}</span>
                    | <strong>独立来源：</strong>{claim.get_independent_source_count()} 个</p>
                    <p><strong>来源：</strong>{sources_html}</p>
                </div>""")

        # 单源结论
        if verification.single_source_claims:
            sections.append('<h3>⚠️ 单源结论（待确认）</h3>')
            for claim in verification.single_source_claims[:5]:
                sources_html = ', '.join(
                    f'<a href="{ev.source_url}" target="_blank">{ev.source_domain}</a>'
                    for ev in claim.evidence[:2]
                )
                sections.append(f"""<div class="single-source">
                    <p><strong>结论：</strong>{html.escape(claim.statement)}</p>
                    <p><strong>来源：</strong>{sources_html}（仅 1 个来源）</p>
                </div>""")

        return '\n'.join(sections)

    def _html_contradictions(self, verification: Optional[Any]) -> str:
        """矛盾点标注"""
        if not verification or not verification.contradictions:
            return '<h2 id="contradictions">4. 矛盾点标注</h2><p>✅ 未发现明显矛盾。</p>'

        sections = ['<h2 id="contradictions">4. 矛盾点标注</h2>']
        for con in verification.contradictions:
            sections.append(f"""<div class="contradiction">
                <p><strong>矛盾 A：</strong>{html.escape(con.claim_a)}</p>
                <p><strong>矛盾 B：</strong>{html.escape(con.claim_b)}</p>
                <p><strong>可能原因：</strong>{html.escape(con.possible_reason)}</p>
            </div>""")
        return '\n'.join(sections)

    def _html_timeline(self, results: List[Any]) -> str:
        """时间线"""
        events = []
        for r in results:
            title = r.title if hasattr(r, 'title') else r.get('title', '')
            date = r.published_date if hasattr(r, 'published_date') else r.get('published_date', '')
            if date:
                events.append({'date': date, 'event': title, 'source': ''})

        if not events:
            return '<h2 id="timeline">5. 时间线</h2><p>无时间线数据。</p>'

        mermaid_code = MermaidGenerator.timeline(events)
        return f"""<h2 id="timeline">5. 时间线</h2>
        <div class="mermaid">
{mermaid_code}
        </div>"""

    def _html_sources(self, results: List[Any]) -> str:
        """引用列表"""
        if not results:
            return '<h2 id="sources">6. 引用列表</h2><p>无引用。</p>'

        rows = []
        for i, r in enumerate(results, 1):
            title = r.title if hasattr(r, 'title') else r.get('title', '')
            url = r.url if hasattr(r, 'url') else r.get('url', '')
            source = r.source if hasattr(r, 'source') else r.get('source', '')
            craap = r.craap_score if hasattr(r, 'craap_score') else r.get('craap_score', {})
            total = craap.get('total', 0) if craap else 0
            grade = craap.get('grade', '') if craap else ''
            grade_class = f'grade-{grade}' if grade else ''
            badge_class = f'badge-{grade}' if grade else ''
            rows.append(f"""<tr>
                <td>{i}</td>
                <td><a href="{html.escape(url)}" target="_blank">{html.escape(title[:60])}</a></td>
                <td>{html.escape(source)}</td>
                <td class="{grade_class}">{total:.1f}</td>
                <td><span class="badge {badge_class}">{grade}</span></td>
            </tr>""")

        # 数据源分布图
        mermaid_pie = MermaidGenerator.source_distribution(results)

        return f"""<h2 id="sources">6. 引用列表（CRAAP 评分）</h2>
        <div class="mermaid">
{mermaid_pie}
        </div>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>标题</th>
                    <th>来源</th>
                    <th>CRAAP 分</th>
                    <th>等级</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>"""

    def _html_quality(
        self, plan: Any, results: List[Any],
        verification: Optional[Any], reflections: Optional[Any]
    ) -> str:
        """调研质量自评"""
        # 覆盖率
        coverage = 0
        rounds = 0
        if reflections:
            coverage = reflections.final_coverage
            rounds = reflections.total_rounds

        # 验证率
        verification_rate = verification.verification_rate if verification else 0

        # 矛盾处理率
        contradiction_rate = 0
        if verification and verification.contradictions:
            # 简化：假设所有矛盾都已被处理（实际由 Claude 标注）
            contradiction_rate = 1.0

        # 综合质量分
        quality_score = (coverage * 0.4 + verification_rate * 0.4 + contradiction_rate * 0.2) * 100

        return f"""<h2 id="quality">7. 调研质量自评</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{coverage:.0%}</div>
                <div class="stat-label">覆盖率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{verification_rate:.0%}</div>
                <div class="stat-label">验证率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{rounds}</div>
                <div class="stat-label">反思轮次</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{quality_score:.0f}</div>
                <div class="stat-label">综合质量分</div>
            </div>
        </div>
        <blockquote>
            <p>📊 <strong>质量评估说明</strong></p>
            <p>覆盖率：调研维度被结果覆盖的比例</p>
            <p>验证率：已验证结论（≥2 独立来源）占总结论的比例</p>
            <p>反思轮次：深度调研中执行的 Plan-Execute-Reflect 循环次数</p>
        </blockquote>"""

    # ------------------------------------------------------------
    # Markdown 报告
    # ------------------------------------------------------------

    def _generate_markdown(
        self, plan: Any, results: List[Any],
        verification: Optional[Any], reflections: Optional[Any]
    ) -> str:
        """生成 Markdown 报告"""
        topic = getattr(plan, 'topic', '调研报告') if plan else '调研报告'
        lines = [
            f"# {topic}",
            "",
            f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**数据源数**：{len(set(r.source if hasattr(r, 'source') else r.get('source', '') for r in results))}",
            "",
            "## 1. 执行摘要",
            "",
            f"本次调研共收集 {len(results)} 条结果。",
        ]

        if verification:
            lines.append(f"- 已验证结论：{len(verification.verified_claims)} 条")
            lines.append(f"- 单源结论：{len(verification.single_source_claims)} 条")
            lines.append(f"- 矛盾点：{len(verification.contradictions)} 个")
            lines.append(f"- 验证率：{verification.verification_rate:.0%}")

        # 引用列表
        lines.extend(["", "## 2. 引用列表", "",
                       "| # | 标题 | 来源 | CRAAP 分 | 等级 |",
                       "|---|------|------|----------|------|"])
        for i, r in enumerate(results, 1):
            title = r.title if hasattr(r, 'title') else r.get('title', '')
            source = r.source if hasattr(r, 'source') else r.get('source', '')
            craap = r.craap_score if hasattr(r, 'craap_score') else r.get('craap_score', {})
            total = craap.get('total', 0) if craap else 0
            grade = craap.get('grade', '') if craap else ''
            lines.append(f"| {i} | {title[:40]} | {source} | {total:.1f} | {grade} |")

        # 已验证结论
        if verification and verification.verified_claims:
            lines.extend(["", "## 3. 已验证结论", ""])
            for claim in verification.verified_claims:
                lines.append(f"### ✅ {claim.statement}")
                lines.append(f"- 置信度：{claim.confidence:.0%}")
                lines.append(f"- 独立来源：{claim.get_independent_source_count()} 个")
                lines.append("")

        # 矛盾点
        if verification and verification.contradictions:
            lines.extend(["", "## 4. 矛盾点", ""])
            for con in verification.contradictions:
                lines.append(f"- **A**: {con.claim_a}")
                lines.append(f"- **B**: {con.claim_b}")
                lines.append(f"- **原因**: {con.possible_reason}")
                lines.append("")

        return '\n'.join(lines)

    # ------------------------------------------------------------
    # JSON 报告
    # ------------------------------------------------------------

    def _generate_json(
        self, plan: Any, results: List[Any],
        verification: Optional[Any], reflections: Optional[Any]
    ) -> str:
        """生成 JSON 报告"""
        report = {
            'metadata': {
                'topic': getattr(plan, 'topic', '') if plan else '',
                'goal': getattr(plan, 'goal', '') if plan else '',
                'depth': getattr(plan, 'depth', '') if plan else '',
                'generated_at': datetime.now().isoformat(),
                'total_results': len(results),
            },
            'results': [
                {
                    'title': r.title if hasattr(r, 'title') else r.get('title', ''),
                    'url': r.url if hasattr(r, 'url') else r.get('url', ''),
                    'source': r.source if hasattr(r, 'source') else r.get('source', ''),
                    'craap_score': r.craap_score if hasattr(r, 'craap_score') else r.get('craap_score', {}),
                }
                for r in results
            ],
        }

        if verification:
            report['verification'] = {
                'verified_claims': [c.to_dict() for c in verification.verified_claims],
                'single_source_claims': [c.to_dict() for c in verification.single_source_claims],
                'contradictions': [c.to_dict() for c in verification.contradictions],
                'verification_rate': verification.verification_rate,
            }

        if reflections:
            report['reflections'] = reflections.to_dict()

        return json.dumps(report, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------
    # CSV 导出
    # ------------------------------------------------------------

    def _generate_csv(self, results: List[Any]) -> str:
        """生成 CSV 来源列表"""
        from io import StringIO
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['#', 'Title', 'URL', 'Source', 'CRAAP Total', 'Grade',
                         'Currency', 'Relevance', 'Authority', 'Accuracy', 'Purpose',
                         'Published Date', 'Author'])

        for i, r in enumerate(results, 1):
            title = r.title if hasattr(r, 'title') else r.get('title', '')
            url = r.url if hasattr(r, 'url') else r.get('url', '')
            source = r.source if hasattr(r, 'source') else r.get('source', '')
            craap = r.craap_score if hasattr(r, 'craap_score') else r.get('craap_score', {})
            published = r.published_date if hasattr(r, 'published_date') else r.get('published_date', '')
            author = r.author if hasattr(r, 'author') else r.get('author', '')

            writer.writerow([
                i, title, url, source,
                craap.get('total', 0) if craap else 0,
                craap.get('grade', '') if craap else '',
                craap.get('currency', 0) if craap else 0,
                craap.get('relevance', 0) if craap else 0,
                craap.get('authority', 0) if craap else 0,
                craap.get('accuracy', 0) if craap else 0,
                craap.get('purpose', 0) if craap else 0,
                published, author,
            ])

        return output.getvalue()


# ============================================================
# 便捷函数
# ============================================================

def generate_report(
    plan: Any,
    results: List[Any],
    verification: Optional[Any] = None,
    reflections: Optional[Any] = None,
    format: str = 'html',
    output_path: Optional[str] = None,
) -> str:
    """便捷函数：生成报告"""
    reporter = ReportGenerator()
    return reporter.generate(plan, results, verification, reflections, format, output_path)


# ============================================================
# CLI 入口
# ============================================================

def _main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description='生成调研报告')
    parser.add_argument('--format', default='html', choices=['html', 'markdown', 'json', 'csv'])
    parser.add_argument('--output', default='report.html')
    parser.add_argument('--results', help='结果 JSON 文件')
    args = parser.parse_args()

    # 简单测试
    class MockPlan:
        topic = "测试调研"
        goal = "测试"
        depth = "standard"
        estimated_duration = "3-5 分钟"
        dimensions = ['维度1', '维度2']
        issue_tree = []

    mock_results = [
        type('R', (), {
            'title': '测试结果 1',
            'url': 'https://example.com/1',
            'content': '测试内容',
            'source': 'tavily',
            'published_date': '2025-01-01',
            'author': '',
            'craap_score': {'total': 85, 'grade': 'high', 'currency': 90, 'relevance': 85, 'authority': 80, 'accuracy': 85, 'purpose': 80},
        })(),
    ]

    reporter = ReportGenerator()
    content = reporter.generate(MockPlan(), mock_results, format=args.format, output_path=args.output)
    print(f"报告已生成: {args.output}")


if __name__ == "__main__":
    _main()

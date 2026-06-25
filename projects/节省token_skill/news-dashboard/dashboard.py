"""Generate interactive HTML dashboard with inline SVG charts and JS filtering."""

from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).parent / "output" / "dashboard.html"

SOURCE_NAMES = {
    "techdaily": "TechDaily 科技日报",
    "financewatch": "FinanceWatch 财经观察",
    "healthnews": "HealthNews 健康新闻",
}

CATEGORY_NAMES = {
    "tech": "科技",
    "finance": "财经",
    "health": "健康",
    "general": "综合",
}

COLORS = {
    "tech": "#7c3aed",
    "finance": "#10b981",
    "health": "#3b82f6",
    "general": "#f59e0b",
    "techdaily": "#7c3aed",
    "financewatch": "#10b981",
    "healthnews": "#3b82f6",
}


def _bar_chart_svg(data: dict, title: str, color_key: str = "", max_width: int = 400) -> str:
    """Generate an SVG horizontal bar chart."""
    if not data:
        return f"<p>No data for {title}</p>"

    # Handle both plain values and {count, pct} dict values
    flat = {}
    for k, v in data.items():
        flat[k] = v["count"] if isinstance(v, dict) else v
    data = flat

    max_val = max(data.values()) if data else 1
    bar_height = 32
    gap = 8
    label_width = 140
    total_height = len(data) * (bar_height + gap) + 10

    bars = ""
    for i, (key, val) in enumerate(sorted(data.items(), key=lambda x: -x[1])):
        y = i * (bar_height + gap)
        width = (val / max_val) * max_width if max_val > 0 else 0
        color = COLORS.get(key, "#7c3aed") if color_key else "#7c3aed"
        label = SOURCE_NAMES.get(key, CATEGORY_NAMES.get(key, key))
        bars += f'''
        <g transform="translate(0,{y})">
          <text x="{label_width - 8}" y="{bar_height // 2 + 5}" text-anchor="end" fill="#e0e0e8" font-size="13">{label}</text>
          <rect x="{label_width}" y="4" width="{width:.0f}" height="{bar_height - 8}" rx="4" fill="{color}" opacity="0.85"/>
          <text x="{label_width + width + 8}" y="{bar_height // 2 + 5}" fill="#8888a0" font-size="13">{val}</text>
        </g>'''

    return f'''
    <div class="chart-box">
      <h3>{title}</h3>
      <svg width="100%" height="{total_height}" viewBox="0 0 600 {total_height}">{bars}</svg>
    </div>'''


def _trend_chart_svg(trend: list[dict]) -> str:
    """Generate an SVG line chart for daily trend."""
    if not trend or len(trend) < 2:
        return "<p>Not enough data for trend</p>"

    width = 560
    height = 200
    padding = 40

    max_count = max(t["count"] for t in trend)
    x_step = (width - 2 * padding) / (len(trend) - 1)

    points = []
    for i, t in enumerate(trend):
        x = padding + i * x_step
        y = height - padding - (t["count"] / max_count) * (height - 2 * padding)
        points.append(f"{x:.0f},{y:.0f}")

    polyline = " ".join(points)

    dots = ""
    labels = ""
    for i, t in enumerate(trend):
        x = padding + i * x_step
        y = height - padding - (t["count"] / max_count) * (height - 2 * padding)
        dots += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#7c3aed"/>'
        labels += f'<text x="{x:.0f}" y="{height - 10}" text-anchor="middle" fill="#8888a0" font-size="11">{t["date"][5:]}</text>'

    return f'''
    <div class="chart-box">
      <h3>每日文章数量趋势</h3>
      <svg width="100%" height="{height}" viewBox="0 0 {width} {height}">
        <polyline points="{polyline}" fill="none" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        {dots}
        {labels}
      </svg>
    </div>'''


def generate_dashboard(analysis: dict, articles: list[dict], output_path=None) -> Path:
    """Generate the full HTML dashboard."""
    output_path = Path(output_path) if output_path else DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = analysis["summary"]
    source_chart = _bar_chart_svg(analysis["source_dist"], "来源分布", color_key="source")
    category_chart = _bar_chart_svg(analysis["category_dist"], "分类分布", color_key="category")
    trend_chart = _trend_chart_svg(analysis["trend"])

    # Article rows
    article_rows = ""
    for a in articles:
        cat_color = COLORS.get(a.get("category", ""), "#888")
        cat_label = CATEGORY_NAMES.get(a.get("category", ""), a.get("category", ""))
        src_label = SOURCE_NAMES.get(a.get("source", ""), a.get("source", ""))
        article_rows += f'''
        <tr data-source="{a.get('source','')}" data-category="{a.get('category','')}">
          <td>{a['title']}</td>
          <td>{src_label}</td>
          <td><span class="cat-badge" style="background:{cat_color}20;color:{cat_color}">{cat_label}</span></td>
          <td>{a.get('published','')}</td>
          <td>{a.get('word_count',0)}</td>
        </tr>'''

    # Top articles
    top_rows = ""
    for i, a in enumerate(analysis.get("top_articles", []), 1):
        top_rows += f'<tr><td>{i}</td><td>{a["title"]}</td><td>{a["source"]}</td><td>{a["word_count"]}</td></tr>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>新闻聚合数据看板</title>
<style>
  :root {{
    --bg: #0a0a0f; --surface: #12121a; --surface-2: #1a1a26;
    --border: #2a2a3a; --text: #e0e0e8; --text-dim: #8888a0;
    --accent: #7c3aed; --green: #10b981; --blue: #3b82f6;
    --radius: 12px;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 24px; }}
  h1 {{ font-size: 28px; margin-bottom: 8px; }}
  .subtitle {{ color: var(--text-dim); margin-bottom: 32px; }}
  .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }}
  .stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; text-align: center; }}
  .stat-num {{ font-size: 32px; font-weight: 800; color: var(--green); }}
  .stat-label {{ font-size: 12px; color: var(--text-dim); margin-top: 4px; }}
  .charts-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 32px; }}
  .chart-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; }}
  .chart-box h3 {{ font-size: 15px; margin-bottom: 16px; color: var(--text-dim); }}
  .trend-section {{ margin-bottom: 32px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{ text-align: left; padding: 10px 12px; background: var(--surface-2); color: var(--text-dim); font-weight: 600; border-bottom: 1px solid var(--border); }}
  td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); }}
  tr:hover {{ background: var(--surface); }}
  .cat-badge {{ padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
  .filter-bar {{ display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
  .filter-bar select {{ background: var(--surface-2); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; font-size: 13px; }}
  @media (max-width: 768px) {{ .charts-row {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="container">
  <h1>新闻聚合数据看板</h1>
  <p class="subtitle">抓取 3 个新闻源 · 自动生成 · {summary['date_range']}</p>

  <div class="stats-row">
    <div class="stat-card"><div class="stat-num">{summary['total']}</div><div class="stat-label">文章总数</div></div>
    <div class="stat-card"><div class="stat-num">{summary['sources']}</div><div class="stat-label">新闻来源</div></div>
    <div class="stat-card"><div class="stat-num">{summary['categories']}</div><div class="stat-label">内容分类</div></div>
    <div class="stat-card"><div class="stat-num">{summary['avg_word_count']}</div><div class="stat-label">平均字数</div></div>
  </div>

  <div class="charts-row">
    {source_chart}
    {category_chart}
  </div>

  <div class="trend-section">
    {trend_chart}
  </div>

  <h2 style="margin:32px 0 16px; font-size:20px;">热门文章</h2>
  <table>
    <thead><tr><th>#</th><th>标题</th><th>来源</th><th>字数</th></tr></thead>
    <tbody>{top_rows}</tbody>
  </table>

  <h2 style="margin:32px 0 16px; font-size:20px;">全部文章</h2>
  <div class="filter-bar">
    <select id="filterSource" onchange="filterTable()">
      <option value="">全部来源</option>
      <option value="techdaily">TechDaily</option>
      <option value="financewatch">FinanceWatch</option>
      <option value="healthnews">HealthNews</option>
    </select>
    <select id="filterCategory" onchange="filterTable()">
      <option value="">全部分类</option>
      <option value="tech">科技</option>
      <option value="finance">财经</option>
      <option value="health">健康</option>
    </select>
  </div>
  <table id="articleTable">
    <thead><tr><th>标题</th><th>来源</th><th>分类</th><th>日期</th><th>字数</th></tr></thead>
    <tbody>{article_rows}</tbody>
  </table>
</div>

<script>
function filterTable() {{
  const source = document.getElementById('filterSource').value;
  const category = document.getElementById('filterCategory').value;
  document.querySelectorAll('#articleTable tbody tr').forEach(row => {{
    const matchSource = !source || row.dataset.source === source;
    const matchCategory = !category || row.dataset.category === category;
    row.style.display = (matchSource && matchCategory) ? '' : 'none';
  }});
}}
</script>
</body>
</html>'''

    output_path.write_text(html, encoding="utf-8")
    return output_path

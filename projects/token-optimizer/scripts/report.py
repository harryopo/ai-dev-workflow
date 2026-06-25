#!/usr/bin/env python3
"""
Token报告生成脚本 - 生成可视化token使用报告
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_history_path():
    """获取历史记录路径"""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / "data" / "history.json"


def load_history():
    """加载历史记录"""
    history_path = get_history_path()
    if history_path.exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def get_config_path():
    """获取配置文件路径"""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / "config" / "default.json"


def load_config():
    """加载配置"""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "price_per_1k_tokens": 0.015,
        "history_days": 30
    }


def filter_by_period(history, days=None):
    """按时间段过滤历史记录"""
    if days is None:
        return history
    
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for h in history:
        try:
            timestamp = datetime.fromisoformat(h.get("timestamp", ""))
            if timestamp >= cutoff:
                filtered.append(h)
        except:
            continue
    return filtered


def calculate_stats(history):
    """计算统计数据"""
    if not history:
        return {
            "total_original": 0,
            "total_compressed": 0,
            "total_saved": 0,
            "percentage": 0,
            "cost_saved": 0,
            "count": 0
        }
    
    config = load_config()
    price_per_1k = config.get("price_per_1k_tokens", 0.015)
    
    total_original = sum(h.get("original_tokens", 0) for h in history)
    total_compressed = sum(h.get("compressed_tokens", 0) for h in history)
    total_saved = total_original - total_compressed
    percentage = (total_saved / total_original * 100) if total_original > 0 else 0
    cost_saved = (total_saved / 1000) * price_per_1k
    
    return {
        "total_original": total_original,
        "total_compressed": total_compressed,
        "total_saved": total_saved,
        "percentage": round(percentage, 1),
        "cost_saved": round(cost_saved, 2),
        "count": len(history)
    }


def generate_bar_chart(value, max_value, width=30):
    """生成简单的文本柱状图"""
    if max_value == 0:
        return "░" * width
    filled = int((value / max_value) * width)
    return "█" * filled + "░" * (width - filled)


def generate_trend(history, days=7):
    """生成趋势数据"""
    trend = {}
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        trend[date] = {"original": 0, "compressed": 0, "count": 0}
    
    for h in history:
        try:
            timestamp = datetime.fromisoformat(h.get("timestamp", ""))
            date = timestamp.strftime("%Y-%m-%d")
            if date in trend:
                trend[date]["original"] += h.get("original_tokens", 0)
                trend[date]["compressed"] += h.get("compressed_tokens", 0)
                trend[date]["count"] += 1
        except:
            continue
    
    return trend


def generate_full_report(history):
    """生成完整报告"""
    config = load_config()
    
    # 总体统计
    total_stats = calculate_stats(history)
    
    # 今日统计
    today_history = filter_by_period(history, 0)
    today_stats = calculate_stats(today_history)
    
    # 本周统计
    week_history = filter_by_period(history, 7)
    week_stats = calculate_stats(week_history)
    
    # 本月统计
    month_history = filter_by_period(history, 30)
    month_stats = calculate_stats(month_history)
    
    # 趋势数据
    trend = generate_trend(history, 7)
    
    # 生成报告
    report = f"""# Token 使用统计报告

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 总体统计

| 指标 | 数值 |
|------|------|
| 总Token使用 | {total_stats['total_original']:,.0f} |
| 总压缩节省 | {total_stats['total_saved']:,.0f} |
| 节省比例 | {total_stats['percentage']}% |
| 预估节省成本 | ${total_stats['cost_saved']:.2f} |
| 压缩次数 | {total_stats['count']} |

## 节省趋势

{generate_bar_chart(total_stats['total_saved'], total_stats['total_original'])}

```
压缩前: {total_stats['total_original']:>10,.0f} tokens
压缩后: {total_stats['total_compressed']:>10,.0f} tokens
节省:   {total_stats['total_saved']:>10,.0f} tokens ({total_stats['percentage']}%)
```

## 分时段统计

| 时段 | Token使用 | 压缩节省 | 节省比例 | 次数 |
|------|-----------|----------|----------|------|
| 今日 | {today_stats['total_original']:,.0f} | {today_stats['total_saved']:,.0f} | {today_stats['percentage']}% | {today_stats['count']} |
| 本周 | {week_stats['total_original']:,.0f} | {week_stats['total_saved']:,.0f} | {week_stats['percentage']}% | {week_stats['count']} |
| 本月 | {month_stats['total_original']:,.0f} | {month_stats['total_saved']:,.0f} | {month_stats['percentage']}% | {month_stats['count']} |

## 最近7天趋势

| 日期 | Token使用 | 压缩节省 | 次数 |
|------|-----------|----------|------|
"""
    
    for date, data in sorted(trend.items(), reverse=True):
        saved = data['original'] - data['compressed']
        report += f"| {date} | {data['original']:,.0f} | {saved:,.0f} | {data['count']} |\n"
    
    report += f"""
## 最近压缩记录

| 时间 | 压缩前 | 压缩后 | 节省 |
|------|--------|--------|------|
"""
    
    for h in history[-10:]:
        timestamp = h.get("timestamp", "未知")
        original = h.get("original_tokens", 0)
        compressed = h.get("compressed_tokens", 0)
        saved = original - compressed
        report += f"| {timestamp} | {original:,.0f} | {compressed:,.0f} | {saved:,.0f} |\n"
    
    report += """
## 优化建议

"""
    
    suggestions = []
    if total_stats['percentage'] < 30:
        suggestions.append("- 考虑降低压缩阈值，让更多内容参与压缩")
    if total_stats['count'] < 10:
        suggestions.append("- 增加压缩频率，定期压缩长对话")
    if today_stats['total_original'] > 10000:
        suggestions.append("- 今日Token使用较高，建议及时压缩")
    if not suggestions:
        suggestions.append("- 当前使用情况良好，继续保持")
    
    report += "\n".join(suggestions)
    
    return report


def generate_summary(history):
    """生成简要报告"""
    stats = calculate_stats(history)
    
    summary = f"""# Token 使用简报

- 总Token使用：{stats['total_original']:,.0f}
- 总压缩节省：{stats['total_saved']:,.0f} ({stats['percentage']}%)
- 预估节省成本：${stats['cost_saved']:.2f}
- 压缩次数：{stats['count']}
"""
    return summary


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python report.py [full|summary] [days]")
        sys.exit(1)
    
    mode = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    history = load_history()
    
    if days:
        history = filter_by_period(history, days)
    
    if mode == "full":
        report = generate_full_report(history)
    elif mode == "summary":
        report = generate_summary(history)
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)
    
    print(report)
    
    # 保存报告
    report_dir = Path(__file__).parent.parent / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {report_file}")


if __name__ == "__main__":
    main()

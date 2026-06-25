"""Statistics analysis for news aggregation data."""


def analyze(stats: dict, articles: list[dict]) -> dict:
    """Compute insights from database stats and article list."""
    total = stats["total"]

    # Top source
    by_source = stats.get("by_source", {})
    top_source = max(by_source, key=by_source.get) if by_source else "N/A"

    # Top category
    by_category = stats.get("by_category", {})
    top_category = max(by_category, key=by_category.get) if by_category else "N/A"

    # Trend: articles per day
    by_date = stats.get("by_date", {})
    trend = []
    for date in sorted(by_date.keys()):
        trend.append({"date": date, "count": by_date[date]})

    # Top articles by word count (proxy for content depth)
    sorted_articles = sorted(articles, key=lambda a: a.get("word_count", 0), reverse=True)
    top_articles = [
        {
            "title": a["title"],
            "source": a["source"],
            "word_count": a.get("word_count", 0),
        }
        for a in sorted_articles[:5]
    ]

    # Category distribution with percentages
    category_dist = {}
    for cat, cnt in by_category.items():
        category_dist[cat] = {"count": cnt, "pct": round(cnt / total * 100, 1) if total else 0}

    # Source distribution
    source_dist = {}
    for src, cnt in by_source.items():
        source_dist[src] = {"count": cnt, "pct": round(cnt / total * 100, 1) if total else 0}

    return {
        "summary": {
            "total": total,
            "sources": len(by_source),
            "categories": len(by_category),
            "date_range": f"{min(by_date.keys())} ~ {max(by_date.keys())}" if by_date else "N/A",
            "avg_word_count": stats.get("avg_word_count", 0),
        },
        "top_source": {"name": top_source, "count": by_source.get(top_source, 0)},
        "top_category": {"name": top_category, "count": by_category.get(top_category, 0)},
        "category_dist": category_dist,
        "source_dist": source_dist,
        "trend": trend,
        "top_articles": top_articles,
    }

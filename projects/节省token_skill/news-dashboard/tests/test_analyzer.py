"""Tests for analyzer.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from analyzer import analyze


def test_analyze_returns_all_sections():
    stats = {
        "total": 15,
        "by_source": {"techdaily": 5, "financewatch": 5, "healthnews": 5},
        "by_category": {"tech": 6, "finance": 5, "health": 4},
        "by_date": {"2026-05-24": 3, "2026-05-25": 3, "2026-05-26": 3, "2026-05-27": 3, "2026-05-28": 3},
        "avg_word_count": 100,
    }
    articles = [{"title": f"Art {i}", "source": "techdaily", "category": "tech", "published": "2026-05-28", "word_count": 100} for i in range(15)]
    result = analyze(stats, articles)
    assert "summary" in result
    assert "top_source" in result
    assert "top_category" in result
    assert "trend" in result
    assert "top_articles" in result


def test_analyze_empty():
    stats = {"total": 0, "by_source": {}, "by_category": {}, "by_date": {}, "avg_word_count": 0}
    result = analyze(stats, [])
    assert result["summary"]["total"] == 0

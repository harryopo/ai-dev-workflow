"""Tests for parser.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from parser import parse_techdaily, parse_financewatch, parse_healthnews

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_parse_techdaily():
    html = (FIXTURES / "techdaily.html").read_text(encoding="utf-8")
    articles = parse_techdaily(html)
    assert len(articles) == 5
    assert articles[0]["title"] == "2026年大模型推理成本下降70%，中小企业迎来AI普惠时代"
    assert articles[0]["source"] == "techdaily"
    assert articles[0]["author"] == "张明"
    assert articles[0]["published"] == "2026-05-28"
    assert articles[0]["category"] == "tech"
    assert "推理成本" in articles[0]["summary"]


def test_parse_financewatch():
    html = (FIXTURES / "financewatch.html").read_text(encoding="utf-8")
    articles = parse_financewatch(html)
    assert len(articles) == 5
    assert articles[0]["source"] == "financewatch"
    assert "英伟达" in articles[0]["title"]
    assert articles[0]["author"] == "刘伟"


def test_parse_healthnews():
    html = (FIXTURES / "healthnews.html").read_text(encoding="utf-8")
    articles = parse_healthnews(html)
    assert len(articles) == 5
    assert articles[0]["source"] == "healthnews"
    assert "AI诊断" in articles[0]["title"]


def test_category_mapping():
    html = (FIXTURES / "techdaily.html").read_text(encoding="utf-8")
    articles = parse_techdaily(html)
    categories = {a["category"] for a in articles}
    assert "tech" in categories


def test_word_count():
    html = (FIXTURES / "techdaily.html").read_text(encoding="utf-8")
    articles = parse_techdaily(html)
    for a in articles:
        assert a["word_count"] > 0

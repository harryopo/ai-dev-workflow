"""Tests for cleaner.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from cleaner import clean_articles


def test_clean_removes_duplicates():
    articles = [
        {"source": "techdaily", "title": "Test", "url": "https://example.com/1", "published": "2026-05-28", "category": "tech", "author": "A", "summary": "S", "word_count": 10},
        {"source": "techdaily", "title": "Test", "url": "https://example.com/1", "published": "2026-05-28", "category": "tech", "author": "A", "summary": "S", "word_count": 10},
    ]
    result = clean_articles(articles)
    assert len(result) == 1


def test_clean_normalizes_whitespace():
    articles = [
        {"source": "techdaily", "title": "  Test  Title  ", "url": "https://example.com/1", "published": "2026-05-28", "category": "tech", "author": "A", "summary": "  S  ", "word_count": 10},
    ]
    result = clean_articles(articles)
    assert result[0]["title"] == "Test Title"
    assert result[0]["summary"] == "S"


def test_clean_fills_missing_fields():
    articles = [
        {"source": "techdaily", "title": "Test", "url": "https://example.com/1", "published": "", "category": "", "author": "", "summary": "", "word_count": 0},
    ]
    result = clean_articles(articles)
    assert result[0]["published"] != ""
    assert result[0]["category"] == "general"
    assert result[0]["author"] == "Unknown"


def test_clean_validates_url():
    articles = [
        {"source": "techdaily", "title": "Test", "url": "", "published": "2026-05-28", "category": "tech", "author": "A", "summary": "S", "word_count": 10},
    ]
    result = clean_articles(articles)
    assert len(result) == 0  # no URL = filtered out


def test_clean_dedup_by_title():
    articles = [
        {"source": "techdaily", "title": "Same Title", "url": "https://example.com/1", "published": "2026-05-28", "category": "tech", "author": "A", "summary": "S", "word_count": 10},
        {"source": "financewatch", "title": "Same Title", "url": "https://example.com/2", "published": "2026-05-28", "category": "finance", "author": "B", "summary": "S", "word_count": 10},
    ]
    result = clean_articles(articles)
    assert len(result) == 1  # same title = duplicate

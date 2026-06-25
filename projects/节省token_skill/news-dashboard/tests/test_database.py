"""Tests for database.py"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from database import NewsDB

SAMPLE_ARTICLE = {
    "source": "techdaily",
    "title": "Test Article",
    "url": "https://example.com/test",
    "published": "2026-05-28",
    "category": "tech",
    "author": "Test Author",
    "summary": "This is a test summary.",
    "word_count": 150,
}


def test_create_tables(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    tables = db.list_tables()
    assert "articles" in tables
    assert "sources" in tables
    db.close()


def test_insert_and_count(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    assert db.count_articles() == 1
    db.insert_article({**SAMPLE_ARTICLE, "title": "Second", "url": "https://example.com/test2"})
    assert db.count_articles() == 2
    db.close()


def test_insert_batch(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    articles = [{**SAMPLE_ARTICLE, "title": f"Article {i}", "url": f"https://example.com/test{i}"} for i in range(10)]
    db.insert_batch(articles)
    assert db.count_articles() == 10
    db.close()


def test_get_all(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    rows = db.get_all()
    assert len(rows) == 1
    assert rows[0]["title"] == "Test Article"
    db.close()


def test_filter_by_source(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    db.insert_article({**SAMPLE_ARTICLE, "source": "financewatch", "title": "Finance", "url": "https://example.com/finance"})
    assert db.count_articles(source="techdaily") == 1
    assert db.count_articles(source="financewatch") == 1
    db.close()


def test_filter_by_category(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    db.insert_article({**SAMPLE_ARTICLE, "category": "finance", "title": "Finance", "url": "https://example.com/finance"})
    rows = db.get_all(category="tech")
    assert len(rows) == 1
    db.close()


def test_get_stats(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    db.insert_article({**SAMPLE_ARTICLE, "source": "financewatch", "category": "finance", "url": "https://example.com/finance"})
    stats = db.get_stats()
    assert stats["total"] == 2
    assert len(stats["by_source"]) == 2
    assert len(stats["by_category"]) == 2
    db.close()


def test_unique_url_constraint(tmp_path):
    db = NewsDB(tmp_path / "test.db")
    db.insert_article(SAMPLE_ARTICLE)
    db.insert_article(SAMPLE_ARTICLE)  # duplicate URL
    assert db.count_articles() == 1  # should not insert duplicate
    db.close()

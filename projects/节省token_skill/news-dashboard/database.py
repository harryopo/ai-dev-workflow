"""SQLite database layer for news aggregation."""

import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "data" / "news.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    name TEXT PRIMARY KEY,
    display_name TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published TEXT,
    category TEXT,
    author TEXT DEFAULT 'Unknown',
    summary TEXT,
    word_count INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (source) REFERENCES sources(name)
);

CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published);
"""

DEFAULT_SOURCES = [
    ("techdaily", "TechDaily 科技日报", "https://techdaily.example.com"),
    ("financewatch", "FinanceWatch 财经观察", "https://financewatch.example.com"),
    ("healthnews", "HealthNews 健康新闻", "https://healthnews.example.com"),
]


class NewsDB:
    def __init__(self, db_path=None):
        self.db_path = db_path or DEFAULT_DB
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript(SCHEMA)
        for src in DEFAULT_SOURCES:
            self.conn.execute(
                "INSERT OR IGNORE INTO sources (name, display_name, url) VALUES (?, ?, ?)",
                src,
            )
        self.conn.commit()

    def list_tables(self):
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        return [row["name"] for row in cursor.fetchall()]

    def insert_article(self, article: dict):
        try:
            self.conn.execute(
                """INSERT OR IGNORE INTO articles
                   (source, title, url, published, category, author, summary, word_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    article["source"],
                    article["title"],
                    article["url"],
                    article.get("published", ""),
                    article.get("category", "general"),
                    article.get("author", "Unknown"),
                    article.get("summary", ""),
                    article.get("word_count", 0),
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # duplicate URL, skip

    def insert_batch(self, articles: list[dict]):
        for article in articles:
            self.insert_article(article)

    def count_articles(self, source=None):
        if source:
            cursor = self.conn.execute(
                "SELECT COUNT(*) as cnt FROM articles WHERE source=?", (source,)
            )
        else:
            cursor = self.conn.execute("SELECT COUNT(*) as cnt FROM articles")
        return cursor.fetchone()["cnt"]

    def get_all(self, source=None, category=None, limit=100):
        query = "SELECT * FROM articles WHERE 1=1"
        params = []
        if source:
            query += " AND source=?"
            params.append(source)
        if category:
            query += " AND category=?"
            params.append(category)
        query += " ORDER BY published DESC LIMIT ?"
        params.append(limit)
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self):
        total = self.conn.execute("SELECT COUNT(*) as cnt FROM articles").fetchone()["cnt"]

        by_source = {}
        for row in self.conn.execute(
            "SELECT source, COUNT(*) as cnt FROM articles GROUP BY source"
        ).fetchall():
            by_source[row["source"]] = row["cnt"]

        by_category = {}
        for row in self.conn.execute(
            "SELECT category, COUNT(*) as cnt FROM articles GROUP BY category"
        ).fetchall():
            by_category[row["category"]] = row["cnt"]

        by_date = {}
        for row in self.conn.execute(
            "SELECT published, COUNT(*) as cnt FROM articles GROUP BY published ORDER BY published"
        ).fetchall():
            by_date[row["published"]] = row["cnt"]

        avg_word_count = self.conn.execute(
            "SELECT AVG(word_count) as avg_wc FROM articles"
        ).fetchone()["avg_wc"] or 0

        return {
            "total": total,
            "by_source": by_source,
            "by_category": by_category,
            "by_date": by_date,
            "avg_word_count": round(avg_word_count),
        }

    def close(self):
        self.conn.close()

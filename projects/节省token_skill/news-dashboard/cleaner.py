"""Data cleaning and deduplication for news articles."""

from datetime import datetime


def clean_articles(articles: list[dict]) -> list[dict]:
    """Clean, validate, and deduplicate articles."""
    seen_urls = set()
    seen_titles = set()
    cleaned = []

    for article in articles:
        # Normalize whitespace
        for key in ("title", "summary", "author"):
            if key in article and isinstance(article[key], str):
                article[key] = " ".join(article[key].split())

        # Validate: must have URL
        url = article.get("url", "").strip()
        if not url:
            continue
        if url in seen_urls:
            continue

        # Dedup by title
        title = article.get("title", "").strip()
        if not title:
            continue
        title_key = title.lower()
        if title_key in seen_titles:
            continue

        # Fill missing fields
        if not article.get("published"):
            article["published"] = datetime.now().strftime("%Y-%m-%d")
        if not article.get("category"):
            article["category"] = "general"
        if not article.get("author"):
            article["author"] = "Unknown"
        if not article.get("summary"):
            article["summary"] = ""
        if not article.get("word_count"):
            article["word_count"] = len(article["summary"])

        seen_urls.add(url)
        seen_titles.add(title_key)
        cleaned.append(article)

    return cleaned

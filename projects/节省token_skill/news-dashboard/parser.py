"""HTML parsers for each news source. Uses stdlib html.parser."""

import re
from abc import ABC, abstractmethod
from html.parser import HTMLParser


def _estimate_word_count(text: str) -> int:
    """Estimate word count: Chinese chars count as 1 word, English words split by space."""
    chinese = len(re.findall(r"[一-鿿]", text))
    english = len(re.findall(r"[a-zA-Z]+", text))
    return chinese + english


def _normalize_category(raw: str, source: str) -> str:
    """Map source-specific categories to standard names."""
    mapping = {
        "AI": "tech",
        "开发": "tech",
        "商业": "tech",
        "市场": "finance",
        "宏观": "finance",
        "加密": "finance",
        "政策": "finance",
        "创投": "finance",
        "研究": "health",
        "药品": "health",
        "心理": "health",
        "营养": "health",
    }
    return mapping.get(raw.strip(), "general")


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class BaseNewsParser(HTMLParser, ABC):
    """Base class for news HTML parsers.

    Provides common state management (tag stack, text buffer, article
    collection) and a template-method parsing flow.  Subclasses implement
    detection hooks for article / title / summary boundaries and
    site-specific metadata extraction.
    """

    def __init__(self, source_name: str, base_url: str):
        super().__init__()
        self.articles: list[dict] = []
        self._current: dict = {}
        self._tag_stack: list[str] = []
        self._text_buffer = ""
        self._source_name = source_name
        self._base_url = base_url
        self._in_article = False
        self._in_title = False
        self._in_summary = False

    # -- abstract detection hooks ----------------------------------------

    @abstractmethod
    def _is_article_start(self, tag: str, attrs_dict: dict) -> bool:
        """Does *tag* mark the beginning of a new article?"""

    @abstractmethod
    def _is_article_end(self, tag: str) -> bool:
        """Does *tag* mark the end of the current article?"""

    @abstractmethod
    def _is_title_start(self, tag: str, attrs_dict: dict) -> bool:
        """Does *tag* open the title region?"""

    @abstractmethod
    def _title_end_tag(self) -> str:
        """Tag name that closes the title region."""

    @abstractmethod
    def _is_summary_start(self, tag: str, attrs_dict: dict) -> bool:
        """Does *tag* open the summary / body region?"""

    @abstractmethod
    def _summary_end_tag(self) -> str:
        """Tag name that closes the summary / body region."""

    # -- overridable hooks -----------------------------------------------

    def _make_article(self) -> dict:
        """Return the initial dict for a new article."""
        return {"source": self._source_name, "author": "Unknown", "word_count": 0}

    def _try_extract_url(self, tag: str, attrs_dict: dict) -> bool:
        """Extract a URL from *tag* while inside the title region.

        Return ``True`` if the tag was handled.
        """
        if tag == "a":
            href = attrs_dict.get("href", "")
            if href:
                self._current["url"] = f"{self._base_url}{href}"
            return True
        return False

    def _parse_span_metadata(self, data: str) -> None:
        """Common span-text parser: ISO date -> published, unknown -> author,
        short tag -> category.  Used by FinanceWatch and HealthNews."""
        stripped = data.strip()
        parent = self._tag_stack[-1] if self._tag_stack else ""
        if parent == "span":
            if re.match(r"\d{4}-\d{2}-\d{2}", stripped):
                self._current["published"] = stripped
            elif self._current.get("author") == "Unknown" and len(stripped) > 1:
                self._current["author"] = stripped
            elif len(stripped) <= 4 and stripped not in ("", " "):
                self._current["_raw_category"] = stripped

    def _on_starttag_in_article(self, tag: str, attrs_dict: dict) -> None:
        """Extra starttag logic while inside an article."""

    def _on_endtag_in_article(self, tag: str) -> None:
        """Extra endtag logic while inside an article."""

    def _on_data_in_article(self, data: str) -> None:
        """Extra character-data logic while inside an article."""

    def _finalize_article(self) -> None:
        """Store the current article if it has a title, then reset."""
        if "title" in self._current:
            raw_cat = self._current.pop("_raw_category", "general")
            self._current["category"] = _normalize_category(raw_cat, self._source_name)
            self.articles.append(self._current)
        self._current = {}

    # -- template methods ------------------------------------------------

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._tag_stack.append(tag)

        if self._is_article_start(tag, attrs_dict):
            self._in_article = True
            self._current = self._make_article()
        elif self._in_article:
            if self._is_title_start(tag, attrs_dict):
                self._in_title = True
                self._text_buffer = ""
            elif self._in_title and self._try_extract_url(tag, attrs_dict):
                pass  # URL captured
            elif self._is_summary_start(tag, attrs_dict):
                self._in_summary = True
                self._text_buffer = ""
            self._on_starttag_in_article(tag, attrs_dict)

    def handle_endtag(self, tag):
        just_ended_content = False
        if self._in_title and tag == self._title_end_tag():
            self._in_title = False
            self._current["title"] = self._text_buffer.strip()
            just_ended_content = True
        if self._in_summary and tag == self._summary_end_tag():
            self._in_summary = False
            summary = self._text_buffer.strip()
            self._current["summary"] = summary
            self._current["word_count"] = _estimate_word_count(summary)
            just_ended_content = True
        if self._in_article:
            self._on_endtag_in_article(tag)
        if not just_ended_content and self._is_article_end(tag):
            self._in_article = False
            self._finalize_article()
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._in_title or self._in_summary:
            self._text_buffer += data
        elif self._in_article:
            self._on_data_in_article(data)


# ---------------------------------------------------------------------------
# TechDaily
# ---------------------------------------------------------------------------

class TechDailyParser(BaseNewsParser):
    """Parser for TechDaily (techdaily.example.com)."""

    def __init__(self):
        super().__init__("techdaily", "https://techdaily.example.com")
        self._in_meta = False

    def _is_article_start(self, tag, attrs_dict):
        return tag == "article"

    def _is_article_end(self, tag):
        return tag == "article"

    def _is_title_start(self, tag, attrs_dict):
        return tag == "h2" and "post-title" in attrs_dict.get("class", "")

    def _title_end_tag(self):
        return "h2"

    def _is_summary_start(self, tag, attrs_dict):
        return tag == "p" and "post-summary" in attrs_dict.get("class", "")

    def _summary_end_tag(self):
        return "p"

    def _on_starttag_in_article(self, tag, attrs_dict):
        if tag == "div" and "post-meta" in attrs_dict.get("class", ""):
            self._in_meta = True
        elif tag == "span" and "author" in attrs_dict.get("class", ""):
            self._text_buffer = ""
        elif tag == "time":
            dt = attrs_dict.get("datetime", "")
            if dt:
                self._current["published"] = dt
            self._text_buffer = ""
        elif tag == "span" and "category" in attrs_dict.get("class", ""):
            self._text_buffer = ""

    def _on_endtag_in_article(self, tag):
        if self._in_meta and tag == "div":
            self._in_meta = False

    def _on_data_in_article(self, data):
        stripped = data.strip()
        parent = self._tag_stack[-1] if self._tag_stack else ""
        if parent == "span":
            if len(stripped) > 1 and not any(c.isdigit() for c in stripped):
                if self._current.get("author") == "Unknown":
                    self._current["author"] = stripped
                else:
                    self._current["_raw_category"] = stripped


def parse_techdaily(html: str) -> list[dict]:
    parser = TechDailyParser()
    parser.feed(html)
    return parser.articles


# ---------------------------------------------------------------------------
# FinanceWatch
# ---------------------------------------------------------------------------

class FinanceWatchParser(BaseNewsParser):
    """Parser for FinanceWatch (financewatch.example.com)."""

    def __init__(self):
        super().__init__("financewatch", "https://financewatch.example.com")
        self._in_meta = False

    def _is_article_start(self, tag, attrs_dict):
        return tag == "div" and "news-item" in attrs_dict.get("class", "")

    def _is_article_end(self, tag):
        return (
            tag == "div"
            and self._in_article
            and not self._in_title
            and not self._in_meta
            and not self._in_summary
            and "title" in self._current
        )

    def _is_title_start(self, tag, attrs_dict):
        return tag == "h3" and "headline" in attrs_dict.get("class", "")

    def _title_end_tag(self):
        return "h3"

    def _is_summary_start(self, tag, attrs_dict):
        return tag == "div" and "excerpt" in attrs_dict.get("class", "")

    def _summary_end_tag(self):
        return "div"

    def _on_starttag_in_article(self, tag, attrs_dict):
        if tag == "a" and "news-link" in attrs_dict.get("class", ""):
            href = attrs_dict.get("href", "")
            if href:
                self._current["url"] = f"{self._base_url}{href}"
        elif tag == "div" and "meta" in attrs_dict.get("class", ""):
            self._in_meta = True
        elif tag == "span":
            cls = attrs_dict.get("class", "")
            if cls in ("reporter", "tag", "date"):
                self._text_buffer = ""

    def _on_endtag_in_article(self, tag):
        if self._in_meta and tag == "div":
            self._in_meta = False

    def _on_data_in_article(self, data):
        self._parse_span_metadata(data)


def parse_financewatch(html: str) -> list[dict]:
    parser = FinanceWatchParser()
    parser.feed(html)
    return parser.articles


# ---------------------------------------------------------------------------
# HealthNews
# ---------------------------------------------------------------------------

class HealthNewsParser(BaseNewsParser):
    """Parser for HealthNews (healthnews.example.com)."""

    def __init__(self):
        super().__init__("healthnews", "https://healthnews.example.com")
        self._entry_depth = 0

    def _is_article_start(self, tag, attrs_dict):
        return tag == "div" and "article-entry" in attrs_dict.get("class", "")

    def _is_article_end(self, tag):
        return self._in_article and tag == "div" and self._entry_depth == 0

    def _is_title_start(self, tag, attrs_dict):
        return tag == "div" and "article-title" in attrs_dict.get("class", "")

    def _title_end_tag(self):
        return "div"

    def _is_summary_start(self, tag, attrs_dict):
        return tag == "div" and "article-body" in attrs_dict.get("class", "")

    def _summary_end_tag(self):
        return "div"

    def _make_article(self):
        self._entry_depth = 1
        return super()._make_article()

    def _try_extract_url(self, tag, attrs_dict):
        if tag == "a" and self._in_title:
            href = attrs_dict.get("href", "")
            if href:
                self._current["url"] = f"{self._base_url}{href}"
            self._text_buffer = ""
            return True
        return False

    def _on_starttag_in_article(self, tag, attrs_dict):
        if tag == "div":
            self._entry_depth += 1
        elif tag == "span":
            self._text_buffer = ""

    def _on_endtag_in_article(self, tag):
        if tag == "div" and self._entry_depth > 0:
            self._entry_depth -= 1

    def _on_data_in_article(self, data):
        self._parse_span_metadata(data)


def parse_healthnews(html: str) -> list[dict]:
    parser = HealthNewsParser()
    parser.feed(html)
    return parser.articles


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

def parse_all(fixtures_dir) -> list[dict]:
    """Parse all fixture files and return combined article list."""
    from pathlib import Path

    fixtures_dir = Path(fixtures_dir)
    all_articles = []

    parsers = {
        "techdaily.html": parse_techdaily,
        "financewatch.html": parse_financewatch,
        "healthnews.html": parse_healthnews,
    }

    for filename, parse_fn in parsers.items():
        filepath = fixtures_dir / filename
        if filepath.exists():
            html = filepath.read_text(encoding="utf-8")
            articles = parse_fn(html)
            all_articles.extend(articles)

    return all_articles

"""Main pipeline orchestrator. Runs the full news aggregation flow."""

import argparse
import sys
from pathlib import Path

from parser import parse_all
from cleaner import clean_articles
from database import NewsDB
from analyzer import analyze
from dashboard import generate_dashboard


def run_pipeline(fixtures_dir=None, db_path=None, output_path=None) -> dict:
    """Run the full pipeline: parse → clean → store → analyze → dashboard."""
    base_dir = Path(__file__).parent
    fixtures_dir = Path(fixtures_dir) if fixtures_dir else base_dir / "fixtures"

    # Step 1: Parse
    print("[1/5] Parsing HTML sources...")
    raw_articles = parse_all(fixtures_dir)
    print(f"  Parsed {len(raw_articles)} articles from {len(set(a['source'] for a in raw_articles))} sources")

    # Step 2: Clean
    print("[2/5] Cleaning and deduplicating...")
    cleaned = clean_articles(raw_articles)
    print(f"  {len(cleaned)} articles after cleaning (removed {len(raw_articles) - len(cleaned)} duplicates)")

    # Step 3: Store
    print("[3/5] Storing in SQLite...")
    db = NewsDB(db_path)
    db.insert_batch(cleaned)
    stored = db.count_articles()
    print(f"  {stored} articles in database")

    # Step 4: Analyze
    print("[4/5] Analyzing...")
    stats = db.get_stats()
    all_articles = db.get_all(limit=1000)
    analysis = analyze(stats, all_articles)
    print(f"  Top source: {analysis['top_source']['name']} ({analysis['top_source']['count']} articles)")
    print(f"  Top category: {analysis['top_category']['name']} ({analysis['top_category']['count']} articles)")

    # Step 5: Dashboard
    print("[5/5] Generating dashboard...")
    out = generate_dashboard(analysis, all_articles, output_path)
    print(f"  Dashboard saved to: {out}")

    db.close()

    return {
        "articles_parsed": len(raw_articles),
        "articles_after_clean": len(cleaned),
        "articles_in_db": stored,
        "output_path": str(out),
    }


def main():
    parser = argparse.ArgumentParser(description="News Aggregation Pipeline")
    parser.add_argument("--fixtures", type=str, help="Path to fixtures directory")
    parser.add_argument("--db", type=str, help="Path to SQLite database")
    parser.add_argument("--output", type=str, help="Path to output HTML dashboard")
    args = parser.parse_args()

    result = run_pipeline(
        fixtures_dir=args.fixtures,
        db_path=args.db,
        output_path=args.output,
    )

    print(f"\nPipeline complete!")
    print(f"  Articles: {result['articles_parsed']} parsed → {result['articles_in_db']} stored")
    print(f"  Dashboard: {result['output_path']}")


if __name__ == "__main__":
    main()

"""Integration test: full pipeline end-to-end."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from main import run_pipeline


def test_full_pipeline(tmp_path):
    fixtures_dir = Path(__file__).parent.parent / "fixtures"
    db_path = tmp_path / "test.db"
    output_path = tmp_path / "dashboard.html"

    result = run_pipeline(fixtures_dir=fixtures_dir, db_path=db_path, output_path=output_path)

    assert result["articles_parsed"] == 15
    assert result["articles_after_clean"] <= 15
    assert result["articles_in_db"] > 0
    assert output_path.exists()
    html = output_path.read_text(encoding="utf-8")
    assert "新闻聚合数据看板" in html
    assert "filterTable" in html

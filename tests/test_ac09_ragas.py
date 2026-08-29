"""AC-09: RAGAS report tests."""

import json

from src.config import REPORTS_DIR


def test_ragas_report_exists_and_valid():
    path = REPORTS_DIR / "ragas_report.json"
    if not path.exists():
        import pytest

        pytest.skip("RAGAS report not generated yet. Run scripts/eval_ragas.py")

    metrics = json.loads(path.read_text(encoding="utf-8"))
    for key in ["context_precision", "context_recall", "faithfulness", "answer_relevancy"]:
        assert key in metrics
        assert 0.0 <= float(metrics[key]) <= 1.0

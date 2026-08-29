"""AC-10: Two-model comparison tests."""

import json

from src.config import GEMINI_MODEL, GEMINI_MODEL_ALT, REPORTS_DIR


def test_model_comparison_report():
    path = REPORTS_DIR / "model_comparison.json"
    if not path.exists():
        import pytest

        pytest.skip("Model comparison not generated yet. Run scripts/model_comparison.py")

    data = json.loads(path.read_text(encoding="utf-8"))
    assert len(data) >= 2
    models = [entry["model"] for entry in data]
    assert GEMINI_MODEL in models
    assert GEMINI_MODEL_ALT in models
    assert len(set(models)) == 2

    for entry in data:
        assert entry["evaluation_count"] >= 20
        assert "metrics" in entry
        for metric_value in entry["metrics"].values():
            assert isinstance(metric_value, (int, float))

"""Compare two Gemini models on the golden evaluation set."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from src.config import EVAL_DIR, GEMINI_MODEL, GEMINI_MODEL_ALT, GEMINI_REQUEST_DELAY, REPORTS_DIR
from src.pipeline import RAGPipeline
from src.schema import RAGResponse

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _score_response(response: RAGResponse, expected_contexts: list[str]) -> dict:
    citation_ids = {c.clause_id for c in response.citations}
    doc_ids = {c.document_id for c in response.citations}
    expected_hits = sum(
        1
        for ctx in expected_contexts
        if ctx in citation_ids or ctx in doc_ids
    )
    recall = expected_hits / len(expected_contexts) if expected_contexts else (1.0 if not response.grounded else 0.0)
    abstention_correct = (not expected_contexts and not response.grounded) or (
        bool(expected_contexts) and response.grounded
    )
    return {
        "grounded_rate": 1.0 if response.grounded else 0.0,
        "context_hit_rate": recall,
        "abstention_correct": 1.0 if abstention_correct else 0.0,
        "confidence": response.confidence,
    }


def compare_models() -> dict:
    golden_path = EVAL_DIR / "golden_set.json"
    items = json.loads(golden_path.read_text(encoding="utf-8"))
    pipeline = RAGPipeline()

    results = []
    for model in [GEMINI_MODEL, GEMINI_MODEL_ALT]:
        per_item = []
        for item in items:
            response = pipeline.ask(item["question"], model_name=model)
            per_item.append(_score_response(response, item.get("expected_contexts", [])))
            time.sleep(GEMINI_REQUEST_DELAY)

        metrics = {
            "grounded_rate": sum(x["grounded_rate"] for x in per_item) / len(per_item),
            "context_hit_rate": sum(x["context_hit_rate"] for x in per_item) / len(per_item),
            "abstention_correct": sum(x["abstention_correct"] for x in per_item) / len(per_item),
            "avg_confidence": sum(x["confidence"] for x in per_item) / len(per_item),
        }
        results.append(
            {
                "model": model,
                "evaluation_count": len(items),
                "metrics": metrics,
            }
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "model_comparison.json"
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    logger.info("Model comparison saved to %s", report_path)
    return {"models": results}


if __name__ == "__main__":
    compare_models()

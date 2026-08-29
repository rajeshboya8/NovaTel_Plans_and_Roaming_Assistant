"""RAGAS evaluation with Gemini judge.

Expected runtime (full 22-question golden set on Gemini free tier):
  Phase 1 — generate answers: ~5-8 minutes (22 API calls + 13s delay each)
  Phase 2 — RAGAS judge metrics: ~15-25 minutes (80+ API calls, quota retries)

Use a smaller sample for a quick check:
  python scripts/eval_ragas.py 5
"""

from __future__ import annotations

from src.eval_utils import ensure_ragas_imports

ensure_ragas_imports()

import json
import logging
import math
import os
import time

from datasets import Dataset
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

from src.config import EMBEDDING_MODEL, EVAL_DIR, GEMINI_EVAL_MODEL, GEMINI_REQUEST_DELAY, REPORTS_DIR
from src.generation.gemini import generate_answer
from src.pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _gemini_llm():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set")

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=GEMINI_EVAL_MODEL, google_api_key=api_key)


def _gemini_embeddings():
    return LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    )


def _safe_metric(result, metric_name: str) -> float:
    raw = result._repr_dict.get(metric_name)
    if raw is not None and not (isinstance(raw, float) and math.isnan(raw)):
        return float(raw)

    scores = result._scores_dict.get(metric_name, [])
    valid = [
        float(score)
        for score in scores
        if score is not None and not (isinstance(score, float) and math.isnan(score))
    ]
    if not valid:
        return 0.0
    return sum(valid) / len(valid)


def run_ragas_eval(sample_size: int | None = None) -> dict:
    golden_path = EVAL_DIR / "golden_set.json"
    items = json.loads(golden_path.read_text(encoding="utf-8"))
    if sample_size:
        items = items[:sample_size]

    pipeline = RAGPipeline()
    questions: list[str] = []
    answers: list[str] = []
    contexts: list[list[str]] = []
    ground_truths: list[str] = []

    total = len(items)
    logger.info(
        "Phase 1/2: generating answers for %s question(s) (~%s min on free tier)",
        total,
        max(1, round(total * GEMINI_REQUEST_DELAY / 60)),
    )

    for index, item in enumerate(items, start=1):
        question = item["question"]
        logger.info("Phase 1/2: question %s/%s — %s", index, total, question[:80])
        evidence = pipeline.retriever.retrieve(question)
        response = generate_answer(
            question=question,
            evidence_with_scores=evidence,
            model_name=GEMINI_EVAL_MODEL,
        )
        questions.append(question)
        answers.append(response.answer)
        contexts.append([chunk.display_text() for chunk, _ in evidence])
        ground_truths.append(item["reference_answer"])
        if index < total:
            time.sleep(GEMINI_REQUEST_DELAY)

    logger.info(
        "Phase 2/2: running RAGAS metrics (4 metrics x %s samples; "
        "expect ~15-25 min with quota retries on free tier)",
        total,
    )

    dataset = Dataset.from_dict(
        {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths,
        }
    )

    llm = _gemini_llm()
    embeddings = _gemini_embeddings()
    result = evaluate(
        dataset,
        metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        llm=llm,
        embeddings=embeddings,
        raise_exceptions=False,
    )

    required = {"context_precision", "context_recall", "faithfulness", "answer_relevancy"}
    metrics = {key: _safe_metric(result, key) for key in required}

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "ragas_report.json"
    report_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    logger.info("RAGAS report saved to %s", report_path)
    return metrics


if __name__ == "__main__":
    import sys

    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_ragas_eval(sample_size=sample_size)

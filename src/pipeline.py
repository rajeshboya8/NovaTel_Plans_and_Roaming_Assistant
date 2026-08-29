"""End-to-end RAG pipeline."""

from __future__ import annotations

import logging

from src.config import GEMINI_EVAL_MODEL, RERANKER_TOP_K
from src.generation.gemini import generate_answer
from src.retrieval.hybrid import HybridRetriever
from src.schema import RAGResponse

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        self.retriever = HybridRetriever()

    def ask(
        self,
        question: str,
        model_name: str | None = None,
        eval_mode: bool = False,
    ) -> RAGResponse:
        question = question.strip()
        if not question:
            return RAGResponse(
                answer="Please enter a question.",
                grounded=False,
                confidence=0.0,
            )

        evidence = self.retriever.retrieve(question, top_k=RERANKER_TOP_K)
        logger.info("Retrieved %s evidence chunks for question.", len(evidence))
        from src.config import GEMINI_EVAL_MODEL, GEMINI_MODEL

        selected_model = model_name or (GEMINI_EVAL_MODEL if eval_mode else GEMINI_MODEL)

        return generate_answer(
            question=question,
            evidence_with_scores=evidence,
            model_name=selected_model,
        )

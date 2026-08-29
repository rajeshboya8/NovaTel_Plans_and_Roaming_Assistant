"""Hybrid retrieval orchestration."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from src.chunking import Chunk
from src.config import (
    BM25_INDEX_PATH,
    BM25_TOP_K,
    CHUNKS_PATH,
    RERANKER_TOP_K,
    SEMANTIC_TOP_K,
)
from src.query_transform import (
    DATA_PATTERN,
    PRICE_PATTERN,
    _extract_plan_name,
    _normalize_plan_aliases,
    transform_query,
)
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.reranker import rerank_candidates
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.semantic import SemanticRetriever

logger = logging.getLogger(__name__)


def _boost_candidates(
    question: str,
    candidates: list[tuple[Chunk, float]],
) -> list[tuple[Chunk, float]]:
    normalized = _normalize_plan_aliases(question)
    plan = _extract_plan_name(normalized)
    boosted: list[tuple[Chunk, float]] = []

    for chunk, score in candidates:
        adjusted = float(score)
        if not chunk.clause_id:
            adjusted -= 3.0
        if plan:
            plan_token = plan.lower().replace(" ", "_")
            if plan_token in chunk.document_id.lower() or plan.lower() in chunk.document_name.lower():
                adjusted += 2.0
        if PRICE_PATTERN.search(normalized) and "PRICE" in chunk.clause_id:
            adjusted += 3.0
        if DATA_PATTERN.search(normalized) and "DATA" in chunk.clause_id:
            adjusted += 3.0
        boosted.append((chunk, adjusted))

    return sorted(boosted, key=lambda item: item[1], reverse=True)


class HybridRetriever:
    def __init__(self):
        self.bm25 = BM25Retriever.load(BM25_INDEX_PATH)
        self.semantic = SemanticRetriever()
        self.chunks = self.bm25.chunks

    def retrieve(self, question: str, top_k: int = RERANKER_TOP_K) -> list[tuple[Chunk, float]]:
        queries = transform_query(question)
        logger.info("Transformed queries: %s", queries)

        bm25_results: list[tuple[Chunk, float]] = []
        semantic_results: list[tuple[Chunk, float]] = []
        for query in queries:
            bm25_results.extend(self.bm25.search(query, top_k=BM25_TOP_K))
            semantic_results.extend(self.semantic.search(query, top_k=SEMANTIC_TOP_K))

        fused = reciprocal_rank_fusion([bm25_results, semantic_results])
        candidate_count = max(top_k * 3, 15)
        candidates = _boost_candidates(question, fused[:candidate_count])
        reranked = rerank_candidates(question, candidates, top_k=top_k)
        return reranked


def save_chunks(chunks: list[Chunk], path: Path = CHUNKS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            **chunk.to_metadata(),
            "content": chunk.content,
        }
        for chunk in chunks
    ]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_chunks(path: Path = CHUNKS_PATH) -> list[Chunk]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        Chunk(
            chunk_id=item["chunk_id"],
            document_id=item["document_id"],
            source=item["source"],
            document_name=item["document_name"],
            document_type=item["document_type"],
            section=item["section"],
            clause_id=item["clause_id"],
            content=item["content"],
        )
        for item in payload
    ]

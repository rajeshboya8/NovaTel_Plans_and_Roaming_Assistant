"""CrossEncoder reranking."""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import CrossEncoder

from src.chunking import Chunk
from src.config import RERANKER_MODEL, RERANKER_TOP_K


@lru_cache(maxsize=1)
def get_reranker() -> CrossEncoder:
    return CrossEncoder(RERANKER_MODEL)


def rerank_candidates(
    query: str,
    candidates: list[tuple[Chunk, float]],
    top_k: int = RERANKER_TOP_K,
) -> list[tuple[Chunk, float]]:
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, chunk.display_text()) for chunk, _ in candidates]
    scores = model.predict(pairs)
    reranked = sorted(
        zip([chunk for chunk, _ in candidates], scores),
        key=lambda item: float(item[1]),
        reverse=True,
    )
    return [(chunk, float(score)) for chunk, score in reranked[:top_k]]

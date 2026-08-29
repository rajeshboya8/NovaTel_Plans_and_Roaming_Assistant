"""Reciprocal Rank Fusion for hybrid retrieval."""

from __future__ import annotations

from src.chunking import Chunk
from src.config import RRF_K


def reciprocal_rank_fusion(
    ranked_lists: list[list[tuple[Chunk, float]]],
    k: int = RRF_K,
) -> list[tuple[Chunk, float]]:
    scores: dict[str, float] = {}
    chunk_map: dict[str, Chunk] = {}

    for ranked in ranked_lists:
        for rank, (chunk, _score) in enumerate(ranked, start=1):
            chunk_map[chunk.chunk_id] = chunk
            scores[chunk.chunk_id] = scores.get(chunk.chunk_id, 0.0) + (1.0 / (k + rank))

    fused = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [(chunk_map[chunk_id], score) for chunk_id, score in fused]

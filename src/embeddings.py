"""Shared embedding model loader."""

from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return [vector.tolist() for vector in vectors]

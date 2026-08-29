"""BM25 lexical retrieval."""

from __future__ import annotations

import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from src.chunking import Chunk
from src.config import BM25_INDEX_PATH, BM25_TOP_K


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.corpus_tokens = [_tokenize(chunk.content) for chunk in chunks]
        self.index = BM25Okapi(self.corpus_tokens)

    def search(self, query: str, top_k: int = BM25_TOP_K) -> list[tuple[Chunk, float]]:
        if not self.chunks:
            return []
        scores = self.index.get_scores(_tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
        results: list[tuple[Chunk, float]] = []
        for idx, score in ranked[:top_k]:
            if score > 0:
                results.append((self.chunks[idx], float(score)))
        return results

    def save(self, path: Path = BM25_INDEX_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "chunks": [
                {
                    **chunk.to_metadata(),
                    "content": chunk.content,
                }
                for chunk in self.chunks
            ]
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path = BM25_INDEX_PATH) -> "BM25Retriever":
        payload = json.loads(path.read_text(encoding="utf-8"))
        chunks = [
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
            for item in payload["chunks"]
        ]
        return cls(chunks)

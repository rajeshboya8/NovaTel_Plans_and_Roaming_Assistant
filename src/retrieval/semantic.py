"""Chroma semantic retrieval."""

from __future__ import annotations

import chromadb
from chromadb.config import Settings

from src.chunking import Chunk
from src.config import CHROMA_COLLECTION, CHROMA_DIR, SEMANTIC_TOP_K
from src.embeddings import embed_texts


class SemanticRetriever:
    def __init__(self, collection=None):
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = collection or self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    def index_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        try:
            self.client.delete_collection(CHROMA_COLLECTION)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.to_metadata() for chunk in chunks]
        embeddings = embed_texts(documents)
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def search(self, query: str, top_k: int = SEMANTIC_TOP_K) -> list[tuple[Chunk, float]]:
        if self.collection.count() == 0:
            return []
        query_embedding = embed_texts([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        chunks: list[tuple[Chunk, float]] = []
        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chunk = Chunk(
                chunk_id=meta["chunk_id"],
                document_id=meta["document_id"],
                source=meta["source"],
                document_name=meta["document_name"],
                document_type=meta["document_type"],
                section=meta["section"],
                clause_id=meta["clause_id"],
                content=doc,
            )
            similarity = 1.0 - float(distance)
            chunks.append((chunk, similarity))
        return chunks

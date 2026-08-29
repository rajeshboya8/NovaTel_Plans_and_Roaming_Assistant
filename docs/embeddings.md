# Embedding Model Selection

## Selected Model

`sentence-transformers/all-MiniLM-L6-v2`

## Rationale

- 384-dimensional embeddings — fast and lightweight for local indexing
- Strong baseline on semantic similarity benchmarks for short factual passages
- Runs fully locally with no API cost
- Compatible with Chroma cosine search

## Usage

The embedding model is loaded once via `functools.lru_cache` in `src/embeddings.py` and reused across ingestion and query-time semantic search.

## Alternatives Considered

Larger models (e.g., BGE, E5) offer marginal retrieval gains at higher latency and memory cost. For a learning-focused capstone with 33 short synthetic documents, MiniLM provides the best simplicity-to-quality trade-off.

"""Corpus ingestion and indexing."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

from src.chunking import chunk_corpus
from src.config import CORPUS_DIR, INGEST_MANIFEST_PATH, VECTORSTORE_DIR
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import save_chunks
from src.retrieval.semantic import SemanticRetriever

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_manifest(corpus_dir: Path) -> dict[str, str]:
    return {path.name: _file_hash(path) for path in sorted(corpus_dir.glob("*.md"))}


def ingest(force: bool = False) -> int:
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    corpus_dir = CORPUS_DIR
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    current_manifest = _build_manifest(corpus_dir)
    previous_manifest: dict[str, str] = {}
    if INGEST_MANIFEST_PATH.exists():
        previous_manifest = json.loads(INGEST_MANIFEST_PATH.read_text(encoding="utf-8"))

    if not force and current_manifest == previous_manifest:
        logger.info("Corpus unchanged. Skipping re-ingestion.")
        return 0

    logger.info("Ingesting %s documents...", len(current_manifest))
    chunks = chunk_corpus(corpus_dir)
    save_chunks(chunks)
    bm25 = BM25Retriever(chunks)
    bm25.save()
    semantic = SemanticRetriever()
    semantic.index_chunks(chunks)

    INGEST_MANIFEST_PATH.write_text(
        json.dumps(current_manifest, indent=2),
        encoding="utf-8",
    )
    logger.info("Ingestion complete. Indexed %s chunks.", len(chunks))
    return len(chunks)


if __name__ == "__main__":
    ingest(force=True)

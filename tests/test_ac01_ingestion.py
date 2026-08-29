"""AC-01: Ingestion tests."""

from pathlib import Path

from src.config import BM25_INDEX_PATH, CHROMA_DIR, CORPUS_DIR, INGEST_MANIFEST_PATH
from src.ingest import ingest
from src.retrieval.hybrid import load_chunks


def test_corpus_has_at_least_30_documents():
    docs = list(CORPUS_DIR.glob("*.md"))
    assert len(docs) >= 30


def test_ingestion_is_idempotent():
    first = ingest(force=True)
    second = ingest(force=False)
    assert second == 0 or second == first


def test_chunks_have_required_metadata(chunks):
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.document_id
        assert chunk.source
        assert chunk.document_name
        assert chunk.document_type
        assert chunk.section is not None


def test_persisted_indexes_exist():
    assert BM25_INDEX_PATH.exists()
    assert CHROMA_DIR.exists()
    assert INGEST_MANIFEST_PATH.exists()


def test_clause_ids_present(chunks):
    clause_chunks = [c for c in chunks if c.clause_id]
    assert len(clause_chunks) >= 30

# Acceptance Criteria

| ID | Criterion | Test Coverage |
|---|---|---|
| AC-01 | Ingest ≥30 synthetic docs; idempotent indexing | `tests/test_ac01_ingestion.py` |
| AC-02 | Grounded answers with clause citations | `tests/test_ac02_citations.py` |
| AC-03 | BM25 + semantic + RRF | `tests/test_ac03_hybrid_retrieval.py` |
| AC-04 | CrossEncoder reranking before Top-K | `tests/test_ac04_reranker.py` |
| AC-05 | Abstention when unsupported | `tests/test_ac05_abstention.py` |
| AC-06 | Pydantic structured output | `tests/test_ac06_schema.py` |
| AC-07 | Query transformation | `tests/test_ac07_query_transform.py` |
| AC-08 | Golden set ≥20 questions | `tests/test_ac08_golden_set.py` |
| AC-09 | RAGAS metrics report | `tests/test_ac09_ragas.py` |
| AC-10 | Two-model comparison | `tests/test_ac10_model_comparison.py` |

"""AC-03: BM25 + semantic + RRF tests."""

from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.semantic import SemanticRetriever


def test_bm25_finds_price_clause():
    bm25 = BM25Retriever.load()
    results = bm25.search("NovaTel Start Lite monthly price")
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "PLAN-001-PRICE-01" in clause_ids


def test_semantic_finds_move_plus_data():
    semantic = SemanticRetriever()
    results = semantic.search("included data NovaTel Move Plus 35 GB")
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "PLAN-002-DATA-01" in clause_ids


def test_rrf_combines_rankings(retriever: HybridRetriever):
    bm25 = BM25Retriever.load()
    semantic = SemanticRetriever()
    query = "EU roaming charges"
    bm25_results = bm25.search(query)
    semantic_results = semantic.search(query)
    fused = reciprocal_rank_fusion([bm25_results, semantic_results])
    assert fused
    scores = [score for _, score in fused]
    assert scores == sorted(scores, reverse=True)


def test_hybrid_retrieval_eu_roaming(retriever: HybridRetriever):
    results = retriever.retrieve("What are the roaming charges in the EU?")
    doc_types = {chunk.document_type for chunk, _ in results}
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "roaming_tariff" in doc_types or any("ROAM-EU" in cid for cid in clause_ids)

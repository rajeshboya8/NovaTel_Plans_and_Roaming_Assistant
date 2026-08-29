"""AC-04: CrossEncoder reranking tests."""

from src.config import RERANKER_TOP_K
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import rerank_candidates


def test_reranker_reorders_candidates(retriever: HybridRetriever):
    from src.query_transform import transform_query
    from src.retrieval.bm25 import BM25Retriever
    from src.retrieval.semantic import SemanticRetriever
    from src.retrieval.rrf import reciprocal_rank_fusion
    from src.config import BM25_TOP_K, SEMANTIC_TOP_K

    query = "What is the monthly price of NovaTel Move Plus?"
    bm25 = BM25Retriever.load()
    semantic = SemanticRetriever()
    fused = reciprocal_rank_fusion(
        [
            bm25.search(query, top_k=BM25_TOP_K),
            semantic.search(query, top_k=SEMANTIC_TOP_K),
        ]
    )
    reranked = rerank_candidates(query, fused[:15], top_k=RERANKER_TOP_K)
    assert reranked
    top_clause = reranked[0][0].clause_id
    assert top_clause in {"PLAN-002-PRICE-01", "PLAN-002-DATA-01"}


def test_final_top_k_after_rerank(retriever: HybridRetriever):
    results = retriever.retrieve("How much data is included in NovaTel Move Plus?")
    assert len(results) <= RERANKER_TOP_K
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "PLAN-002-DATA-01" in clause_ids

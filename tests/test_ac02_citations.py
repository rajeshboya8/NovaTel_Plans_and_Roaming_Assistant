"""AC-02: Citation tests."""

from src.retrieval.hybrid import HybridRetriever
from src.schema import Citation, RAGResponse


def test_retrieval_returns_clause_ids(retriever: HybridRetriever):
    results = retriever.retrieve("What is the monthly price of NovaTel Start Lite?")
    assert results
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "PLAN-001-PRICE-01" in clause_ids


def test_citation_schema_validation():
    citation = Citation(
        document_id="NOVATEL_START_LITE",
        document_name="Novatel Start Lite",
        section="Pricing",
        clause_id="PLAN-001-PRICE-01",
    )
    response = RAGResponse(
        answer="Monthly price is $15.00.",
        citations=[citation],
        grounded=True,
        confidence=0.7,
    )
    assert response.citations[0].clause_id == "PLAN-001-PRICE-01"


def test_move_plus_price_citation(retriever: HybridRetriever):
    results = retriever.retrieve("What is the monthly price of NovaTel Move Plus?")
    clause_ids = {chunk.clause_id for chunk, _ in results}
    assert "PLAN-002-PRICE-01" in clause_ids

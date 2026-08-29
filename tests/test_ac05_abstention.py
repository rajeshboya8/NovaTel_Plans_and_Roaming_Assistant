"""AC-05: Abstention tests."""

from src.config import ABSTENTION_THRESHOLD
from src.generation.gemini import generate_answer
from src.retrieval.hybrid import HybridRetriever


def test_unsupported_plan_low_evidence(retriever: HybridRetriever):
    results = retriever.retrieve("What is the price of the NovaTel Mars Plan?")
    if results:
        top_score = max(score for _, score in results)
        # Mars plan should not have a direct clause; top score may be low relevance
        assert top_score < 5.0 or not any(
            "mars" in chunk.content.lower() for chunk, _ in results
        )


def test_abstention_threshold_configured():
    assert 0.0 < ABSTENTION_THRESHOLD < 1.0


def test_empty_evidence_abstains():
    response = generate_answer("What is NovaTel Mars Plan price?", [])
    assert response.grounded is False
    assert response.confidence == 0.0
    assert "insufficient" in response.answer.lower() or "could not" in response.answer.lower()

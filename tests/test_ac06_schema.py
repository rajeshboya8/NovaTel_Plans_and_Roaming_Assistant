"""AC-06: Pydantic structured output tests."""

import pytest
from pydantic import ValidationError

from src.generation.gemini import _normalize_text_field
from src.schema import Citation, RAGResponse


def test_rag_response_required_fields():
    response = RAGResponse(
        answer="Test answer",
        citations=[],
        applicable_plan_or_tariff="Move Plus",
        tariff_clause="PLAN-002-PRICE-01",
        charge_or_limit="$25.00",
        conditions="Excluding taxes",
        grounded=True,
        confidence=0.65,
    )
    assert response.answer == "Test answer"
    assert response.charge_or_limit == "$25.00"
    assert 0.0 <= response.confidence <= 1.0


def test_confidence_bounds():
    with pytest.raises(ValidationError):
        RAGResponse(answer="x", confidence=1.5)


def test_citation_model():
    c = Citation(
        document_id="NOVATEL_MOVE_PLUS",
        document_name="Novatel Move Plus",
        section="Pricing",
        clause_id="PLAN-002-PRICE-01",
    )
    assert c.clause_id.startswith("PLAN-")


def test_conditions_list_normalized_to_string():
    assert _normalize_text_field(["excluding taxes"]) == "excluding taxes"
    assert _normalize_text_field(["excluding taxes", "valid ID required"]) == (
        "excluding taxes; valid ID required"
    )

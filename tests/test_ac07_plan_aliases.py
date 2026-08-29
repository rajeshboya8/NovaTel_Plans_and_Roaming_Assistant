"""AC-07: Plan alias normalization tests."""

from src.query_transform import _normalize_plan_aliases, transform_query


def test_novatel_plus_alias_maps_to_move_plus():
    question = "what is monthly plan for novatel plus?"
    normalized = _normalize_plan_aliases(question)
    assert "Move Plus" in normalized


def test_novatel_plus_query_expansion():
    queries = transform_query("what is monthly plan for novatel plus?")
    assert any("Move Plus" in query for query in queries)
    assert any("monthly price" in query.lower() for query in queries)

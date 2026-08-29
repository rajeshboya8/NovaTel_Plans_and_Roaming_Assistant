"""AC-07: Query transformation tests."""

from src.query_transform import decompose_query, transform_query


def test_simple_query_not_over_decomposed():
    question = "What is the monthly price of Move Plus?"
    queries = transform_query(question)
    assert queries[0] == question
    assert len(queries) <= 3


def test_multi_part_query_decomposition():
    question = "What is the price of Move Plus and what happens after 35 GB?"
    queries = decompose_query(question)
    assert len(queries) >= 2


def test_roaming_query_expansion():
    question = "What are the roaming charges in the EU?"
    queries = transform_query(question)
    assert any("roaming" in q.lower() for q in queries)


def test_fair_usage_expansion():
    question = "What is the fair-usage limit for the premium plan?"
    queries = transform_query(question)
    assert any("fair" in q.lower() for q in queries)


def test_novatel_plus_alias_normalization():
    question = "what is monthly plan for novatel plus?"
    queries = transform_query(question)
    assert any("move plus" in q.lower() for q in queries)

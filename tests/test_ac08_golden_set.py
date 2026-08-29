"""AC-08: Golden set validation tests."""

import json

from src.config import EVAL_DIR


def test_golden_set_structure():
    path = EVAL_DIR / "golden_set.json"
    items = json.loads(path.read_text(encoding="utf-8"))
    assert len(items) >= 20

    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids))

    ac_ids = {item["ac_id"] for item in items}
    for ac in [f"AC-{i:02d}" for i in range(1, 11)]:
        assert ac in ac_ids

    for item in items:
        assert item["question"].strip()
        assert item["reference_answer"].strip()
        assert "expected_contexts" in item


def test_golden_set_clause_references(chunks):
    valid_clause_ids = {c.clause_id for c in chunks if c.clause_id}
    valid_doc_ids = {c.document_id for c in chunks}
    items = json.loads((EVAL_DIR / "golden_set.json").read_text(encoding="utf-8"))

    for item in items:
        for ctx in item["expected_contexts"]:
            assert ctx in valid_clause_ids or ctx in valid_doc_ids

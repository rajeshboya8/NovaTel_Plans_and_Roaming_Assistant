"""Run the eight manual RAG validation questions."""

from __future__ import annotations

import json
from pathlib import Path

from src.pipeline import RAGPipeline

TESTS = [
    {
        "name": "Start Lite",
        "question": "What is the monthly price of NovaTel Start Lite?",
        "clause": "PLAN-001-PRICE-01",
        "text": "$15.00",
        "require_grounded": True,
    },
    {
        "name": "Move Plus price",
        "question": "What is the monthly price of NovaTel Move Plus?",
        "clause": "PLAN-002-PRICE-01",
        "text": "$25.00",
        "require_grounded": True,
    },
    {
        "name": "Move Plus data",
        "question": "How much data is included in NovaTel Move Plus?",
        "clause": "PLAN-002-DATA-01",
        "text": "35 GB",
        "require_grounded": True,
    },
    {
        "name": "Move Plus 35GB",
        "question": "What happens after 35 GB on NovaTel Move Plus?",
        "clause": "PLAN-002-DATA-02",
        "text": "1 Mbps",
        "require_grounded": True,
    },
    {
        "name": "EU roaming",
        "question": "What are the roaming charges in the EU?",
        "clause": "ROAM-EU",
        "text": None,
        "require_grounded": True,
    },
    {
        "name": "Fair usage",
        "question": "What is the fair-usage limit for the premium plan?",
        "clause": "FUP-PREM-01",
        "text": "500 GB",
        "require_grounded": True,
    },
    {
        "name": "Multi-part query",
        "question": "What is the monthly price of Move Plus and what happens after 35 GB?",
        "clause": "PLAN-002",
        "text": None,
        "require_grounded": True,
        "require_clauses": ["PLAN-002-PRICE-01", "PLAN-002-DATA-02"],
    },
    {
        "name": "Unsupported query",
        "question": "What is the price of the NovaTel Mars Plan?",
        "clause": None,
        "text": None,
        "require_grounded": False,
    },
]


def main() -> None:
    pipeline = RAGPipeline()
    results = []
    for test in TESTS:
        response = pipeline.ask(test["question"])
        clause_ids = [c.clause_id for c in response.citations]
        passed = True
        if test["require_grounded"]:
            passed = response.grounded
            if test.get("require_clauses"):
                passed = passed and all(
                    any(required in cid for cid in clause_ids)
                    for required in test["require_clauses"]
                )
            elif test["clause"]:
                passed = passed and any(test["clause"] in cid for cid in clause_ids)
            if test["text"]:
                combined = f"{response.answer} {response.charge_or_limit}"
                passed = passed and test["text"] in combined
        else:
            passed = response.grounded is False

        results.append(
            {
                "name": test["name"],
                "status": "PASS" if passed else "FAIL",
                "grounded": response.grounded,
                "citations": clause_ids,
                "charge_or_limit": response.charge_or_limit,
            }
        )
        print(f"{test['name']}: {'PASS' if passed else 'FAIL'}")

    report_path = Path("reports/manual_tests.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

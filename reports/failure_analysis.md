# Failure Analysis

Based on golden-set evaluation and manual RAG tests.

## Retrieval Failure

- **Symptom:** Correct clause not in reranked Top-K.
- **Observed:** Rare for targeted plan/tariff questions. Retrieval correctly ranked `PLAN-002-DATA-02` for the 35 GB throttle question in isolation.
- **Mitigation:** Hybrid BM25 + semantic + RRF + CrossEncoder reranking is working for clause-level documents.

## Grounding Failure

- **Symptom:** Gemini returns `grounded=false` or empty citations despite good retrieval.
- **Observed:** Several manual-test failures coincided with Gemini API `429` quota errors, not retrieval misses.
- **Mitigation:** Added API retry backoff parsing `retry in Ns` from Gemini errors and `GEMINI_REQUEST_DELAY` between batch evaluation calls.

## Synthesis / Generation Failure

- **Symptom:** Answer omits explicit charge/limit values present in evidence.
- **Observed:** When API calls succeed, price/data questions extract `$25.00`, `35 GB`, and `500 GB` correctly.
- **Mitigation:** Prompt requires explicit extraction and Pydantic schema validation strips invalid citations.

## Abstention

- **Symptom:** Fabricated answers for unsupported plans.
- **Observed:** `NovaTel Mars Plan` correctly returns `grounded=false` with no citations.

## Next Improvements

1. Add plan-name validation against retrieved document titles before generation.
2. Cache embedding/reranker models across Streamlit reruns (already cached).
3. Re-run full RAGAS after API quota resets.

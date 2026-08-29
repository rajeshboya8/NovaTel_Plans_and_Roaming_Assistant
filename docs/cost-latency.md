# Cost and Latency (Conceptual)

## Representative Query

"What is the monthly price of NovaTel Move Plus?"

## Approximate Latency

| Stage | Estimate |
|---|---|
| Query transformation | < 10 ms |
| BM25 + semantic search | 100–300 ms |
| CrossEncoder rerank (15 pairs) | 200–500 ms |
| Gemini generation | 1–3 s |
| **Total** | **~2–4 s** |

## Approximate Cost per Query

- Embeddings/reranker: local — $0
- Gemini 2.0 Flash: ~$0.001–0.005 per query (depends on prompt/evidence size)

Batch evaluation over 22 golden-set questions: roughly $0.05–0.15 in API usage.

# NovaTel Plans & Roaming Assistant

Retrieval-augmented assistant for synthetic NovaTel plans, tariffs, and roaming policies.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Add your GOOGLE_API_KEY to .env
python scripts/generate_corpus.py
python -m src.ingest
streamlit run src/main.py
```

## Evaluation

```powershell
python scripts/eval_ragas.py
python scripts/model_comparison.py
python -m pytest -q
python -m pytest -v
```

## Pipeline

Query transformation → BM25 + Chroma semantic search → RRF fusion → CrossEncoder reranking → Gemini grounded generation → Pydantic structured output.

## Stack

- Python 3.12, pip
- Google Gemini (`gemini-3.5-flash`, `gemini-3.5-flash-lite`)
- sentence-transformers/all-MiniLM-L6-v2 (embeddings)
- cross-encoder/ms-marco-MiniLM-L-6-v2 (reranker)
- Chroma (vector store)
- rank_bm25 (lexical retrieval)
- RAGAS (evaluation)
- Streamlit (UI)

## Notes

- Set `GOOGLE_API_KEY` in `.env` (never commit it).
- Batch evaluation scripts use `GEMINI_REQUEST_DELAY` to respect free-tier rate limits.
- If `gemini-3.5-flash` is unavailable in your account, update model names in `src/config.py` using `python -c` with the Gemini model list API.

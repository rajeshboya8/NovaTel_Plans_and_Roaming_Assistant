"""Central configuration for retrieval, models, and paths."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_DIR = DATA_DIR / "corpus"
EVAL_DIR = DATA_DIR / "eval"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"
CHROMA_DIR = VECTORSTORE_DIR / "chroma"
CHUNKS_PATH = VECTORSTORE_DIR / "chunks.json"
BM25_INDEX_PATH = VECTORSTORE_DIR / "bm25_corpus.json"
INGEST_MANIFEST_PATH = VECTORSTORE_DIR / "ingest_manifest.json"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval
BM25_TOP_K = 10
SEMANTIC_TOP_K = 10
RRF_K = 60
RERANKER_TOP_K = 5
ABSTENTION_THRESHOLD = 0.15

# Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
GEMINI_MODEL = "gemini-3.5-flash"
GEMINI_MODEL_ALT = "gemini-3.5-flash-lite"
GEMINI_EVAL_MODEL = "gemini-3.5-flash-lite"
CHROMA_COLLECTION = "novatel_corpus"

# API
GEMINI_MAX_RETRIES = 3
GEMINI_RETRY_DELAY = 1.0
GEMINI_REQUEST_DELAY = 13.0

"""Shared pytest fixtures."""

from __future__ import annotations

import json
import pytest

from src.ingest import ingest
from src.retrieval.hybrid import HybridRetriever, load_chunks


@pytest.fixture(scope="session", autouse=True)
def ensure_indexed_corpus():
    ingest(force=True)
    yield


@pytest.fixture(scope="session")
def retriever() -> HybridRetriever:
    return HybridRetriever()


@pytest.fixture(scope="session")
def chunks():
    return load_chunks()

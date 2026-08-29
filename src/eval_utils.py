"""Shared import shims for evaluation tooling."""

from __future__ import annotations

import sys
import types


def ensure_ragas_imports() -> None:
    vertexai_stub = types.ModuleType("langchain_community.chat_models.vertexai")

    class _ChatVertexAIStub:  # pragma: no cover
        pass

    vertexai_stub.ChatVertexAI = _ChatVertexAIStub
    sys.modules["langchain_community.chat_models.vertexai"] = vertexai_stub

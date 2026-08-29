"""Gemini generation with retries and structured output."""

from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv

from src.chunking import Chunk
from src.config import (
    ABSTENTION_THRESHOLD,
    GEMINI_MAX_RETRIES,
    GEMINI_MODEL,
    GEMINI_MODEL_ALT,
    GEMINI_RETRY_DELAY,
)
from src.schema import Citation, RAGResponse

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are NovaTel's Plans, Tariffs & Roaming assistant.
Answer ONLY from the supplied evidence.

Rules:
1. Do not invent facts.
2. Every factual answer must include provenance.
3. Cite document_id, section, and clause_id for each citation.
4. Extract charge_or_limit only if explicitly present in evidence.
5. Extract conditions only if supported by evidence.
6. If evidence is insufficient, set grounded=false and abstain.
7. Do not provide definitive legal/financial/billing advice.
8. Return valid JSON only.
9. If the user uses an informal or partial plan name (e.g. "NovaTel Plus"), answer from the matching plan in the evidence when it is clearly the same product.
"""


def _load_api_key() -> str:
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key:
        raise ValueError("GOOGLE_API_KEY is not set in the environment.")
    return key


def configure_gemini(model_name: str = GEMINI_MODEL) -> genai.GenerativeModel:
    genai.configure(api_key=_load_api_key())
    return genai.GenerativeModel(model_name)


def _build_prompt(question: str, evidence: list[Chunk]) -> str:
    evidence_blocks = []
    for index, chunk in enumerate(evidence, start=1):
        evidence_blocks.append(
            f"[Evidence {index}]\n"
            f"document_id: {chunk.document_id}\n"
            f"document_name: {chunk.document_name}\n"
            f"section: {chunk.section}\n"
            f"clause_id: {chunk.clause_id}\n"
            f"content:\n{chunk.content}\n"
        )
    evidence_text = "\n".join(evidence_blocks)
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"USER QUESTION:\n{question}\n\n"
        f"EVIDENCE:\n{evidence_text}\n\n"
        "Return JSON with keys:\n"
        "answer, citations (list of document_id, document_name, section, clause_id), "
        "applicable_plan_or_tariff, tariff_clause, charge_or_limit, conditions (plain string, not a list), "
        "grounded, confidence\n"
    )


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _validate_citations(
    citations: list[Citation],
    evidence: list[Chunk],
) -> list[Citation]:
    valid_clause_ids = {chunk.clause_id for chunk in evidence if chunk.clause_id}
    valid_docs = {chunk.document_id for chunk in evidence}
    validated: list[Citation] = []
    for citation in citations:
        if citation.clause_id in valid_clause_ids and citation.document_id in valid_docs:
            validated.append(citation)
    return validated


def _compute_confidence(
    rerank_scores: list[float],
    grounded: bool,
    citations: list[Citation],
) -> float:
    if not grounded or not rerank_scores:
        return 0.0
    top_score = max(rerank_scores)
    normalized = max(0.0, min(1.0, top_score / 10.0))
    citation_bonus = 0.1 if citations else 0.0
    return round(min(1.0, normalized + citation_bonus), 3)


def _abstention_response(question: str, reason: str) -> RAGResponse:
    return RAGResponse(
        answer=(
            "I could not find sufficient evidence in the NovaTel corpus to answer this question. "
            f"{reason}"
        ),
        citations=[],
        applicable_plan_or_tariff="",
        tariff_clause="",
        charge_or_limit="Not identified from the evidence.",
        conditions="",
        grounded=False,
        confidence=0.0,
    )


def _retry_delay_for_error(exc: Exception, attempt: int) -> float:
    message = str(exc)
    match = re.search(r"retry in ([0-9.]+)s", message, re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1.0
    return GEMINI_RETRY_DELAY * attempt



def _is_quota_error(exc: Exception) -> bool:
    return "429" in str(exc)


def _normalize_text_field(value: Any, default: str = "") -> str:
    """Coerce Gemini output to a display string (lists become prose)."""
    if value is None:
        return default
    if isinstance(value, list):
        parts = [str(item).strip() for item in value if str(item).strip()]
        return "; ".join(parts) if parts else default
    text = str(value).strip()
    return text if text else default


def _parse_response(
    payload: dict[str, Any],
    evidence: list[Chunk],
    evidence_with_scores: list[tuple[Chunk, float]],
) -> RAGResponse:
    citations = [Citation(**item) for item in payload.get("citations", [])]
    citations = _validate_citations(citations, evidence)
    answer = str(payload.get("answer", ""))
    grounded = bool(citations) and not answer.lower().startswith(
        "i could not find sufficient evidence"
    )
    confidence = _compute_confidence(
        [score for _, score in evidence_with_scores],
        grounded,
        citations,
    )
    if not citations:
        grounded = False
        confidence = 0.0
    return RAGResponse(
        answer=answer,
        citations=citations,
        applicable_plan_or_tariff=_normalize_text_field(
            payload.get("applicable_plan_or_tariff", "")
        ),
        tariff_clause=_normalize_text_field(payload.get("tariff_clause", "")),
        charge_or_limit=_normalize_text_field(
            payload.get("charge_or_limit", "Not identified from the evidence."),
            default="Not identified from the evidence.",
        ),
        conditions=_normalize_text_field(payload.get("conditions", "")),
        grounded=grounded,
        confidence=confidence,
    )


def generate_answer(
    question: str,
    evidence_with_scores: list[tuple[Chunk, float]],
    model_name: str = GEMINI_MODEL,
) -> RAGResponse:
    if not evidence_with_scores:
        return _abstention_response(question, "No relevant documents were retrieved.")

    top_score = max(score for _, score in evidence_with_scores)
    if top_score < ABSTENTION_THRESHOLD:
        return _abstention_response(
            question,
            "Retrieved evidence did not meet the confidence threshold.",
        )

    evidence = [chunk for chunk, _ in evidence_with_scores]
    prompt = _build_prompt(question, evidence)

    models_to_try = [model_name]
    if model_name != GEMINI_MODEL_ALT:
        models_to_try.append(GEMINI_MODEL_ALT)

    last_error: Exception | None = None
    for current_model in models_to_try:
        model = configure_gemini(current_model)
        for attempt in range(1, GEMINI_MAX_RETRIES + 1):
            try:
                response = model.generate_content(prompt)
                payload = _extract_json(response.text)
                return _parse_response(payload, evidence, evidence_with_scores)
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Gemini call failed for %s on attempt %s: %s",
                    current_model,
                    attempt,
                    exc,
                )
                if _is_quota_error(exc) and current_model != models_to_try[-1]:
                    break
                if _is_quota_error(exc) and attempt == GEMINI_MAX_RETRIES:
                    break
                time.sleep(min(_retry_delay_for_error(exc, attempt), 15.0))

    return RAGResponse(
        answer=f"Generation failed after retries: {last_error}",
        citations=[],
        applicable_plan_or_tariff="",
        tariff_clause="",
        charge_or_limit="Not identified from the evidence.",
        conditions="",
        grounded=False,
        confidence=0.0,
    )

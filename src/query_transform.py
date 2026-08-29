"""Deterministic query transformation and decomposition."""

from __future__ import annotations

import re

PLAN_ALIASES = {
    "novatel plus": "NovaTel Move Plus",
    "nova plus": "NovaTel Move Plus",
    "start lite": "NovaTel Start Lite",
    "premium unlimited": "NovaTel Premium Unlimited",
    "family share": "NovaTel Family Share",
    "student plan": "NovaTel Student Plan",
    "senior plan": "NovaTel Senior Plan",
    "business pro": "NovaTel Business Pro",
    "business basic": "NovaTel Business Basic",
}

KNOWN_PLANS = [
    "Premium Unlimited",
    "Family Share",
    "Business Pro",
    "Business Basic",
    "Student Plan",
    "Senior Plan",
    "Start Lite",
    "Move Plus",
]

PRICE_PATTERN = re.compile(r"price|cost|monthly|charge|fee", re.IGNORECASE)
DATA_PATTERN = re.compile(r"data|gb|after|throttle|speed|limit", re.IGNORECASE)
ROAMING_PATTERN = re.compile(r"roaming|eu|international|abroad", re.IGNORECASE)
FAIR_USAGE_PATTERN = re.compile(r"fair[- ]?usage|premium", re.IGNORECASE)


def _normalize_plan_aliases(question: str) -> str:
    lowered = question.lower()
    normalized = question
    for alias, canonical in sorted(PLAN_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in lowered:
            normalized = re.sub(re.escape(alias), canonical, normalized, flags=re.IGNORECASE)
            break
    if re.search(r"novatel\s+plus\b", lowered) and "move" not in lowered:
        normalized = re.sub(
            r"novatel\s+plus",
            "NovaTel Move Plus",
            normalized,
            flags=re.IGNORECASE,
        )
    return normalized


def _extract_plan_name(question: str) -> str | None:
    lowered = question.lower()
    for plan in sorted(KNOWN_PLANS, key=len, reverse=True):
        if plan.lower() in lowered:
            return plan
    match = re.search(r"NovaTel\s+([A-Za-z][A-Za-z0-9\s+-]+?)(?:\s+plan|\s+tariff)", question, re.I)
    if match:
        return match.group(1).strip()
    return None


def decompose_query(question: str) -> list[str]:
    """Return one or more retrieval queries for the user question."""
    cleaned = _normalize_plan_aliases(" ".join(question.strip().split()))
    if not cleaned:
        return [cleaned]

    compound_match = re.match(r"^(.*?)\band\b(.+)$", cleaned, flags=re.IGNORECASE)
    if compound_match:
        first = compound_match.group(1).strip(" ?.")
        second = compound_match.group(2).strip(" ?.")
        if first and second:
            plan_name = _extract_plan_name(cleaned)
            queries = [first, second]
            if plan_name:
                queries = [
                    part if plan_name.lower() in part.lower() else f"{part} for NovaTel {plan_name}"
                    for part in queries
                ]
            return queries

    return [cleaned]


def transform_query(question: str) -> list[str]:
    """Rewrite or expand the query when helpful."""
    normalized_question = _normalize_plan_aliases(question)
    queries = decompose_query(normalized_question)
    rewritten: list[str] = [normalized_question]
    plan = _extract_plan_name(normalized_question)
    if plan and PRICE_PATTERN.search(normalized_question):
        rewritten.append(f"NovaTel {plan} monthly price clause")
    if plan and DATA_PATTERN.search(normalized_question):
        rewritten.append(f"NovaTel {plan} included data allowance")
    for query in queries:
        extras: list[str] = [query]
        if PRICE_PATTERN.search(query):
            extras.append(f"{query} monthly price clause")
        if DATA_PATTERN.search(query):
            extras.append(f"{query} included data allowance")
        if ROAMING_PATTERN.search(query):
            extras.append(f"{query} roaming charges tariff")
        if FAIR_USAGE_PATTERN.search(query):
            extras.append(f"{query} fair usage limit policy")
        rewritten.extend(extras)
    seen: set[str] = set()
    unique: list[str] = []
    for item in rewritten:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique

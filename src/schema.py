"""Pydantic schema for structured RAG responses."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    document_id: str
    document_name: str
    section: str
    clause_id: str


class RAGResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    applicable_plan_or_tariff: str = ""
    tariff_clause: str = ""
    charge_or_limit: str = "Not identified from the evidence."
    conditions: str = ""
    grounded: bool = False
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)

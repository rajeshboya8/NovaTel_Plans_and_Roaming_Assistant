"""Structure-aware chunking for markdown corpus documents."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, CORPUS_DIR


CLAUSE_PATTERN = re.compile(
    r"\*\*Clause ID:\*\*\s*([A-Z0-9-]+)",
    re.IGNORECASE,
)
SECTION_PATTERN = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    document_name: str
    document_type: str
    section: str
    clause_id: str
    content: str

    def to_metadata(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "source": self.source,
            "document_name": self.document_name,
            "document_type": self.document_type,
            "section": self.section,
            "clause_id": self.clause_id,
        }

    def display_text(self) -> str:
        return (
            f"Document: {self.document_name}\n"
            f"Section: {self.section}\n"
            f"Clause ID: {self.clause_id}\n"
            f"Content:\n{self.content}"
        )


def _infer_document_type(filename: str, text: str) -> str:
    lowered = f"{filename} {text[:200]}".lower()
    if "roaming" in lowered:
        return "roaming_tariff"
    if "fair" in lowered and "usage" in lowered:
        return "fair_usage_policy"
    if "terms" in lowered or "conditions" in lowered:
        return "terms_and_conditions"
    if "addon" in lowered or "add-on" in lowered:
        return "addon_catalog"
    if "broadband" in lowered or "fibre" in lowered:
        return "broadband_plan"
    return "mobile_plan"


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    parts: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            parts.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return parts


def _extract_sections(text: str) -> list[tuple[str, str]]:
    matches = list(SECTION_PATTERN.finditer(text))
    if not matches:
        return [("General", text.strip())]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((title, body))
    return sections


def _split_section_into_clauses(section_title: str, section_body: str) -> list[tuple[str, str, str]]:
    clause_matches = list(CLAUSE_PATTERN.finditer(section_body))
    if not clause_matches:
        return [(section_title, "", section_body)]

    clauses: list[tuple[str, str, str]] = []
    for index, match in enumerate(clause_matches):
        clause_id = match.group(1).strip()
        start = match.start()
        end = clause_matches[index + 1].start() if index + 1 < len(clause_matches) else len(section_body)
        clause_text = section_body[start:end].strip()
        clauses.append((section_title, clause_id, clause_text))
    return clauses


def chunk_document(path: Path) -> list[Chunk]:
    text = path.read_text(encoding="utf-8")
    document_name = path.stem.replace("_", " ").title()
    document_id = path.stem.upper()
    source = str(path.relative_to(CORPUS_DIR.parent))
    document_type = _infer_document_type(path.name, text)

    chunks: list[Chunk] = []
    for section_title, section_body in _extract_sections(text):
        for section, clause_id, clause_text in _split_section_into_clauses(section_title, section_body):
            for piece in _split_long_text(clause_text, CHUNK_SIZE, CHUNK_OVERLAP):
                stable = f"{document_id}|{section}|{clause_id}|{piece[:120]}"
                chunk_id = hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=document_id,
                        source=source,
                        document_name=document_name,
                        document_type=document_type,
                        section=section,
                        clause_id=clause_id,
                        content=piece,
                    )
                )
    # Drop non-clause overview chunks for plan/tariff docs to avoid retrieval noise.
    if document_type in {"mobile_plan", "broadband_plan", "roaming_tariff"}:
        chunks = [chunk for chunk in chunks if chunk.clause_id]
    return chunks


def chunk_corpus(corpus_dir: Path | None = None) -> list[Chunk]:
    root = corpus_dir or CORPUS_DIR
    all_chunks: list[Chunk] = []
    for path in sorted(root.glob("*.md")):
        all_chunks.extend(chunk_document(path))
    return all_chunks

# Chunking Strategy

## Approach

Structure-aware recursive chunking for markdown corpus files.

1. Split documents on markdown headings (`#`, `##`, `###`).
2. Within each section, split on `**Clause ID:**` boundaries to preserve tariff clauses.
3. If a clause block exceeds `CHUNK_SIZE` (500 chars), apply recursive character splitting with `CHUNK_OVERLAP` (50).

## Metadata Preserved

Each chunk stores:

- `document_id`
- `source`
- `document_name`
- `document_type`
- `section`
- `clause_id`

## Rationale

Telecom documents are organized by plan sections and clause IDs. Preserving clause boundaries ensures retrieval can return citeable units such as `PLAN-002-PRICE-01` without mixing unrelated tariffs.

Fixed-size-only chunking was avoided because it would split price and data clauses across chunks, hurting citation accuracy.

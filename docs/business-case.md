# Business Case — AAIE_022_TEL

## Problem

NovaTel support agents need accurate answers about mobile plans, tariffs, and roaming rules grounded in official documents.

## Target Users

- Customer support agents
- Sales representatives
- Capstone evaluators testing RAG quality

## Corpus

33 synthetic markdown documents covering mobile plans, roaming tariffs, fair-usage policies, add-ons, broadband, and terms.

## Domain Guardrails

- Answer only from retrieved evidence
- Cite clause IDs for every grounded answer
- Abstain when corpus lacks support
- Do not provide legal or billing advice

## Success Metrics

- Hybrid retrieval returns correct clauses for golden-set questions
- RAGAS faithfulness and context precision on committed eval set
- Structured output with charge/limit extraction when explicit in evidence

# Guardrails

## Citation Required

Every grounded answer must include at least one valid clause-level citation from retrieved evidence.

## Abstention

When retrieval scores fall below `ABSTENTION_THRESHOLD` or citations cannot be validated, the system returns `grounded=false`.

## No Invented Charges

`charge_or_limit` is set to `Not identified from the evidence.` unless explicitly stated in retrieved clauses.

## No Legal/Financial Advice

Answers describe plan and tariff clauses; they do not make binding billing or legal decisions.

## Synthetic Data Only

The corpus contains only synthetic NovaTel documents. No real customer data is used or logged.

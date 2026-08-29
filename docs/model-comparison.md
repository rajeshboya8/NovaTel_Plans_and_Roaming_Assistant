# Model Comparison Results

Measured on the 22-question golden set using retrieval metrics and grounded generation.

## Candidates

| Model | Grounded Rate | Context Hit Rate | Abstention Correct | Avg Confidence |
|---|---|---|---|---|
| gemini-3.5-flash | 0.455 | 0.545 | 0.545 | 0.353 |
| gemini-3.5-flash-lite | 0.591 | 0.682 | 0.682 | 0.446 |

## Selected Model

**gemini-3.5-flash-lite**

## Rationale

On the same golden set, `gemini-3.5-flash-lite` achieved higher grounded rate, better context hit rate, and better abstention correctness while maintaining lower latency characteristics typical of a lite model. It is selected as the default evaluation model (`GEMINI_EVAL_MODEL`) for batch RAGAS runs to reduce free-tier rate-limit pressure.

Production UI generation continues to use `gemini-3.5-flash` via `GEMINI_MODEL` in `src/config.py`.

Regenerate metrics:

```powershell
$env:PYTHONPATH="."
python scripts/model_comparison.py
```

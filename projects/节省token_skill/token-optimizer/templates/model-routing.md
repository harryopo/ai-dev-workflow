# Model Routing Template

Use this template for Module 5 model selection.

## Routing Decision Table

| Task Category | Complexity | Recommended Model | Token Cost/1K |
|---------------|-----------|-------------------|---------------|
| Greeting/Chat | Trivial | Haiku | $0.00025 |
| File Read/Search | Trivial | Haiku | $0.00025 |
| Simple Q&A | Trivial | Haiku | $0.00025 |
| Code Generation | Standard | Sonnet | $0.003 |
| Code Review | Standard | Sonnet | $0.003 |
| Bug Fixing | Standard | Sonnet | $0.003 |
| Architecture Design | Complex | Opus | $0.015 |
| Security Review | Complex | Opus | $0.015 |
| Complex Debugging | Complex | Opus | $0.015 |
| Multi-file Refactor | Complex | Opus | $0.015 |

## Cost Estimation Template

```
Model Routing Cost Estimate
═══════════════════════════════════════
Task: [description]
Estimated tokens: ~[X]K input + [Y]K output

Option A: All Sonnet
  Cost: ([X] + [Y]) × $0.003 = $[Z]

Option B: Routed (Haiku/Sonnet/Opus mix)
  Haiku:  [A]K × $0.00025 = $[B]
  Sonnet: [C]K × $0.003   = $[D]
  Opus:   [E]K × $0.015   = $[F]
  Total: $[G]

Savings: $[Z-G] ([X]%)
═══════════════════════════════════════
```

## Advisor Pattern Template

```
Phase 1: Planning (Opus)
  → Analyze requirements
  → Design solution architecture
  → Output: plan.md

Phase 2: Execution (Sonnet)
  → Implement per plan
  → Run tests
  → Output: code + test results

Phase 3: Verification (Opus)
  → Review implementation
  → Check edge cases
  → Output: review.md
```

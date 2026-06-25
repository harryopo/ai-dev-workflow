> Part of Token Optimizer V2. See also: [memory-compression](memory-compression.md), [rtk-integration](rtk-integration.md), [scenario-*](scenario-simple-qa.md)

# Model Routing Example

## Scenario

A developer's typical day: mix of simple lookups, standard coding, and complex architecture work.

## Without Routing (All Sonnet)

| Task | Tokens | Cost |
|------|--------|------|
| "What's the syntax for X?" | 2K | $0.006 |
| Read file and explain | 5K | $0.015 |
| Write a function | 8K | $0.024 |
| Review PR | 10K | $0.030 |
| Design system architecture | 15K | $0.045 |
| Simple status check | 1K | $0.003 |
| Fix a bug | 12K | $0.036 |
| "Thanks!" | 0.5K | $0.002 |
| **Total** | **53.5K** | **$0.161** |

## With Routing

| Task | Model | Tokens | Cost |
|------|-------|--------|------|
| "What's the syntax for X?" | Haiku | 2K | $0.0005 |
| Read file and explain | Haiku | 5K | $0.00125 |
| Write a function | Sonnet | 8K | $0.024 |
| Review PR | Sonnet | 10K | $0.030 |
| Design system architecture | Opus | 15K | $0.225 |
| Simple status check | Haiku | 1K | $0.00025 |
| Fix a bug | Sonnet | 12K | $0.036 |
| "Thanks!" | Haiku | 0.5K | $0.000125 |
| **Total** | | **53.5K** | **$0.317** |

Wait — Opus is expensive! Let me use the Advisor Pattern instead.

## With Advisor Pattern

| Phase | Model | Tokens | Cost |
|-------|-------|--------|------|
| Planning | Opus | 5K | $0.075 |
| Execution | Sonnet | 10K | $0.030 |
| Verification | Opus | 3K | $0.045 |
| **Architecture total** | | **18K** | **$0.150** |

vs. All Opus: 18K × $0.015 = $0.270 (45% savings)

## Decision Flow

```
Task arrives
    │
    ├─ < 100 chars or "read"/"find"/"show" → Haiku
    │
    ├─ "design"/"architect"/"security"/"complex" → Opus (plan)
    │   └─ Then Sonnet (execute) → Opus (verify)
    │
    └─ Everything else → Sonnet
```

# Module: Routing

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

# Module 5: Model Routing

## Three-Layer Routing Strategy

```
Task Input → Classifier → Route → Model
                │
                ├─ Simple/Haiku    → claude-haiku-4-5
                ├─ Standard/Sonnet → claude-sonnet-4-6
                └─ Complex/Opus    → claude-opus-4-7
```

## Task Classification

| Task Type | Complexity | Model | Cost/1K tokens |
|-----------|-----------|-------|----------------|
| Greeting, simple Q&A | Trivial | Haiku | $0.00025 |
| Code generation, analysis | Standard | Sonnet | $0.003 |
| Architecture, complex reasoning | Complex | Opus | $0.015 |
| File reading, search | Trivial | Haiku | $0.00025 |
| Multi-file refactoring | Standard | Sonnet | $0.003 |
| Security review, system design | Complex | Opus | $0.015 |

## Decision Algorithm

```python
def route_model(task):
    # Trivial: short, factual, no reasoning
    if task.type in ["greeting", "lookup", "file_read", "simple_search"]:
        return "haiku"

    # Complex: multi-step reasoning, architecture, security
    if task.type in ["architecture", "security_review", "complex_debug", "system_design"]:
        return "opus"

    # Standard: everything else
    return "sonnet"
```

## Advisor Pattern

For complex tasks, use Opus as advisor, Sonnet as executor:

```
User Request → Opus (plan) → Sonnet (execute) → Opus (verify)
```

Savings: ~70% compared to running everything on Opus.

## Cost Comparison

| Scenario | All Sonnet | With Routing | Savings |
|----------|-----------|--------------|---------|
| 100 requests/day | $3.00 | $1.20 | 60% |
| Mixed tasks | $5.00 | $2.00 | 60% |
| Mostly simple | $1.00 | $0.30 | 70% |
| Mostly complex | $8.00 | $7.50 | 6% |

## Claude Code Model Switching

```bash
# Set model for current session
/model claude-haiku-4-5    # Simple tasks
/model claude-sonnet-4-6   # Standard tasks
/model claude-opus-4-7     # Complex tasks

# Or use /fast for Opus with faster output
/fast
```

## Routing Rules

1. **Default to Sonnet** when unsure
2. **Use Haiku** for: file reads, searches, simple lookups, greetings
3. **Use Opus** for: architecture decisions, security, complex debugging, multi-file refactoring plans
4. **Switch mid-task** if complexity changes
5. **Never use Opus** for: formatting, simple edits, status checks

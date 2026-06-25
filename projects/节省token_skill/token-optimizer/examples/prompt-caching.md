> Part of Token Optimizer V2. See also: [memory-compression](memory-compression.md), [rtk-integration](rtk-integration.md), [scenario-*](scenario-simple-qa.md)

# Prompt Caching Example

## Scenario

Building a chatbot with consistent system prompt across many requests.

## Without Caching

```
Request 1: [System: 3000 tokens] + [History: 500] + [Input: 100] = 3600 tokens
Request 2: [System: 3000 tokens] + [History: 800] + [Input: 150] = 3950 tokens
Request 3: [System: 3000 tokens] + [History: 1100] + [Input: 200] = 4300 tokens
────────────────────────────────────────────────────────────────────
Total input: 11,850 tokens × $0.003/1K = $0.036
```

## With Caching

```
Request 1: [System: 3000 tokens (building cache)] + [History: 500] + [Input: 100]
  → cache_creation: 3000, input: 600
  Cost: 3000 × $0.00375 + 600 × $0.003 = $0.013

Request 2: [System: 3000 tokens (cached)] + [History: 800] + [Input: 150]
  → cache_read: 3000, input: 950
  Cost: 3000 × $0.0003 + 950 × $0.003 = $0.004

Request 3: [System: 3000 tokens (cached)] + [History: 1100] + [Input: 200]
  → cache_read: 3000, input: 1300
  Cost: 3000 × $0.0003 + 1300 × $0.003 = $0.005
────────────────────────────────────────────────────────────────────
Total: $0.022 (39% savings)
```

## Implementation

```python
import anthropic

client = anthropic.Anthropic()

# System prompt with cache control
system = [
    {
        "type": "text",
        "text": """You are a customer support bot for TechCorp.
        Products: Widget A ($99), Widget B ($149), Widget C ($199)
        Policies: 30-day returns, 1-year warranty...
        [Long stable content here]""",
        "cache_control": {"type": "ephemeral"}
    }
]

# First request builds cache
r1 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system=system,
    messages=[{"role": "user", "content": "What's the price of Widget A?"}]
)
print(f"Cache created: {r1.usage.cache_creation_input_tokens}")

# Subsequent requests hit cache
r2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system=system,
    messages=[{"role": "user", "content": "What about Widget B?"}]
)
print(f"Cache hit: {r2.usage.cache_read_input_tokens}")
```

## Verification

Check cache status in response:
```json
{
  "usage": {
    "input_tokens": 950,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 3000,
    "output_tokens": 150
  }
}
```

`cache_read_input_tokens > 0` means cache is working.

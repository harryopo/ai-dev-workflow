# Module: Caching

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

# Module 2: Prompt Caching

## How Prompt Caching Works

Anthropic API supports caching of repeated content blocks. Cached tokens cost 90% less than regular input tokens.

```
Request Structure:
┌─────────────────────────────────────────────┐
│ System Prompt (cached)     ← static         │
│ Tool Definitions (cached)  ← static         │
│ ─── cache breakpoint ───                    │
│ Conversation History       ← dynamic        │
│ User Input                 ← dynamic        │
└─────────────────────────────────────────────┘
```

## Step 1: Check Current Cache Usage

Look at API response `usage` fields:
```json
{
  "usage": {
    "input_tokens": 1200,
    "cache_creation_input_tokens": 5800,
    "cache_read_input_tokens": 0,
    "output_tokens": 450
  }
}
```

- `cache_creation_input_tokens > 0` → First request, building cache
- `cache_read_input_tokens > 0` → Cache hit! 90% cost saving
- Both 0 → Caching not enabled

## Step 2: Optimize Cache Structure

**Rule:** Put stable content first, variable content last.

```
Good:  [System Prompt] [Tools] [History] [User Input]
Bad:   [User Input] [History] [System Prompt] [Tools]
```

Stable content (cache-friendly):
- System prompt
- Tool definitions
- Long reference documents
- Few-shot examples

Variable content (don't cache):
- Conversation history
- User input
- Tool results

## Step 3: Implement Cache Control

```python
# Anthropic SDK example
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a helpful assistant...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)
```

## Step 4: Verify Cache Hits

Check response headers or usage fields after 2+ requests with same system prompt.

Expected savings:
- First request: normal cost (builds cache)
- Subsequent requests: 90% off cached portion
- Cache TTL: 5 minutes (Anthropic default)

## Cache Hit Rate Targets

| Hit Rate | Status | Action |
|----------|--------|--------|
| > 80% | Excellent | Maintain current structure |
| 50-80% | Good | Check for variable content in cached blocks |
| < 50% | Poor | Restructure: move dynamic content after breakpoint |
| 0% | Not working | Verify cache_control is set correctly |

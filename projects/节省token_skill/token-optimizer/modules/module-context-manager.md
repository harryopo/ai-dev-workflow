# Module: Context Manager

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules
> Merged: Audit (module-1) + Compression (module-3) + Depth (module-6)

# Module 1: Context Audit

## Step 1: Estimate Context Distribution

```
Context Breakdown:
┌─────────────────────────────────────────────────┐
│ System Prompt           ~[X] tokens             │
│ Tool Definitions        ~[X] tokens             │
│ Conversation History    ~[X] tokens             │
│ Tool Results            ~[X] tokens             │
│ User Input              ~[X] tokens             │
│ Other                   ~[X] tokens             │
├─────────────────────────────────────────────────┤
│ Total                   ~[X] tokens             │
└─────────────────────────────────────────────────┘
```

Estimation heuristic: 1 token ≈ 4 characters (English) or 1.5 characters (Chinese).

## Step 2: Identify High-Consumption Items

Checklist:
- [ ] Tool results > 500 tokens?
- [ ] Conversation history has > 20 old messages?
- [ ] System prompt has redundant info?
- [ ] Duplicate tool call results?
- [ ] Compressible long text?

## Step 3: Generate Audit Report

```
Token Audit Report
═══════════════════════════════════════════════════
Context: ~[N] tokens
Estimated waste: ~[M] tokens ([X]%)

Top Issues:
1. [Issue] — potential saving: [X] tokens
2. [Issue] — potential saving: [X] tokens

Recommended Actions:
□ [Action]
□ [Action]
═══════════════════════════════════════════════════
```

## Step 4: Map Issues to Modules

| Issue Found | → Module |
|-------------|----------|
| Tool results too long | → Module 3 (Compression) |
| Cache hit rate low | → Module 2 (Caching) |
| Task not structured | → Module 4 (Canvas) |
| Using expensive model for simple task | → Module 5 (Routing) |
| Agent stuck in loop | → Module 7 (Retry Protection) |

---

# Module 3: Context Compression

## Strategy Selection

| Signal | Strategy | Savings |
|--------|----------|---------|
| Tool result > 500 tokens | Strategy 1: Truncate | ~90% |
| > 20 rounds of history | Strategy 2: History Summary | ~94% |
| Scratchpad growing | Strategy 3: State Summary | ~93% |
| Multi-section output | Strategy 4: HTML Artifact | ~93% |

## Strategy 1: Tool Result Truncate

When tool result exceeds threshold:

```json
{
  "content": "[first 500 chars]...[truncated]",
  "file_path": "/path/to/full/result",
  "full_length": 2156,
  "truncated": true,
  "key_facts": ["fact1", "fact2", "fact3"]
}
```

Save full result to `refs/` directory for on-demand recall.

## Strategy 2: History Summary

Compress old conversation history:

```json
{
  "type": "history_summary",
  "task": "what we were doing",
  "summary": "[200 word summary]",
  "key_decisions": ["decision1", "decision2"],
  "current_state": "where we are now",
  "protected_recent": ["last 3 rounds kept in full"]
}
```

**Rule:** Always keep the last 3 rounds uncompressed.

## Strategy 3: Scratchpad State Summary

Compress accumulated tool call outputs:

```json
{
  "attempts_tried": ["what we tried"],
  "current_progress": "where we are",
  "blockers": ["what's blocking us"],
  "next_steps": ["what to do next"]
}
```

## Strategy 4: HTML Artifact

Save as HTML file instead of inline markdown when output contains:
- Multi-section reports
- Comparison tables
- Diffs
- Charts
- Interactive content

```json
{
  "artifact_type": "html",
  "file_path": "/path/to/artifact.html",
  "summary": "[50 word summary]",
  "token_saved": 1400
}
```

## Per-Round Budget

| Mode | Budget | When |
|------|--------|------|
| Normal | 4,000 tokens/round | Default |
| Comfortable | 8,000 tokens/round | Complex tasks |
| Over budget | Possible leak | Investigate |

Budget allocation:
```
System prompt: fixed (cached)
Tool defs: fixed (cached)
Compressed context: ~1,000
Current task state: ~500
User input: ~500
Safety margin: ~1,000
────────────────────
Total: ~4,000
```

## Compression Quality Check

After compressing, verify:
1. Key data not lost → check `key_facts` fields
2. Traceability maintained → check `file_path` pointers
3. Task completion rate unchanged → compare before/after

---

# Module 6: Response Depth Control

## Four Depth Levels

| Level | Token Budget | When to Use |
|-------|-------------|-------------|
| 25% | ~100 tokens | Quick answers, yes/no, status checks |
| 50% | ~250 tokens | Standard explanations, code snippets |
| 75% | ~500 tokens | Detailed analysis, multi-step plans |
| 100% | ~1000 tokens | Full reports, comprehensive reviews |

## Quick Command Map

| User Says | Depth | Output Style |
|-----------|-------|--------------|
| "简短回答" / "brief" / "short" | 25% | One-liner, no explanation |
| "正常" / "default" | 50% | Concise with context |
| "详细" / "detailed" | 75% | Full explanation |
| "完整报告" / "full report" | 100% | Comprehensive |

## Session Persistence

Once set, depth persists for the entire session:
- User says "简短回答" → all subsequent responses at 25%
- User says "详细分析" → all subsequent responses at 75%
- Don't re-ask depth level unless user changes it

## Non-Compressible Content

These must always be included regardless of depth:
- Error messages and warnings
- Security-related information
- Destructive action confirmations
- File paths and line numbers
- Required code changes

## Depth-Aware Output Templates

### 25% (Minimal)
```
Result: [one sentence answer]
```

### 50% (Standard)
```
Answer: [concise explanation]
Key point: [main takeaway]
```

### 75% (Detailed)
```
Analysis:
- [point 1 with context]
- [point 2 with context]
- [point 3 with context]

Recommendation: [suggestion]
```

### 100% (Comprehensive)
```
## Overview
[full context]

## Analysis
[detailed breakdown]

## Options
[alternatives considered]

## Recommendation
[final suggestion with rationale]

## Next Steps
[actionable items]
```

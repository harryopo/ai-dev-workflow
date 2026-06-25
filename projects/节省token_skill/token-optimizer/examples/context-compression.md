> Part of Token Optimizer V2. See also: [memory-compression](memory-compression.md), [rtk-integration](rtk-integration.md), [scenario-*](scenario-simple-qa.md)

# Context Compression Example

## Scenario

User has been working on a debugging task for 25 rounds. Context is growing large with tool results.

## Before Compression

```
Round 1: Read file config.py (800 tokens)
Round 2: Read file utils.py (1200 tokens)
Round 3: grep for "error" (600 tokens)
Round 4: Read log file (2000 tokens)
Round 5: Run test (500 tokens)
... (20 more rounds)
Total: ~25,000 tokens
```

## After Compression

```json
{
  "type": "history_summary",
  "task": "Debugging config loading error in production",
  "summary": "Config loading fails when env var CONFIG_PATH is not set. Root cause: missing default value in config.py line 42. Fixed by adding fallback to /etc/app/config.yaml.",
  "key_decisions": [
    "Identified missing env var as root cause",
    "Added fallback path instead of requiring env var",
    "Tests pass with both set and unset CONFIG_PATH"
  ],
  "current_state": "Fix implemented and tested, ready to commit",
  "protected_recent": ["Round 23-25: final test run and verification"],
  "artifacts": {
    "full_logs": "refs/debug-logs.txt",
    "test_results": "refs/test-output.txt",
    "diff": "refs/config-fix.diff"
  }
}
```

## Token Savings

- Before: ~25,000 tokens
- After: ~500 tokens (summary) + ~1,500 tokens (last 3 rounds)
- Saved: ~23,000 tokens (92%)

## Quality Check

✅ Root cause documented in summary
✅ Fix described with file path and line number
✅ Test results preserved in artifacts
✅ Recent context (last 3 rounds) kept intact
✅ Full logs available via file references

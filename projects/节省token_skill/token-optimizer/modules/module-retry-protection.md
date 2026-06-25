# Module: Retry Protection

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

# Module 7: Retry Protection

## Problem: Agent Loops

Agent gets stuck repeating the same action, consuming tokens without progress.

Common causes:
- Tool call fails silently
- Same error keeps occurring
- No progress detection
- Missing exit condition

## Step 1: Set MAX_STEPS Hard Limit

```json
{
  "max_steps": 10,
  "current_step": 0,
  "action": "halt_if_exceeded"
}
```

When `current_step >= max_steps`:
1. Stop execution
2. Summarize what was tried
3. Ask user for guidance

## Step 2: Implement Idempotency Check

Before each action, check if it was already attempted:

```json
{
  "attempts": [
    {"action": "npm install", "result": "success", "step": 1},
    {"action": "npm test", "result": "failure", "error": "timeout", "step": 2},
    {"action": "npm test", "result": "failure", "error": "timeout", "step": 3}
  ]
}
```

If same action failed 2+ times with same error → stop and report.

## Step 3: Structured Error Format

```json
{
  "error": true,
  "type": "tool_failure",
  "tool": "Bash",
  "command": "npm test",
  "exit_code": 1,
  "stderr": "timeout after 120s",
  "context": "running test suite",
  "suggestion": "increase timeout or run specific test file",
  "retry_count": 2,
  "should_retry": false
}
```

## Step 4: No-Progress Detection

Track progress indicators:

```json
{
  "progress_metrics": {
    "files_changed": 0,
    "tests_passed": 0,
    "errors_fixed": 0,
    "rounds_since_progress": 3
  }
}
```

If `rounds_since_progress > 3` → pause and reassess.

## Emergency Stop Protocol

When loop detected:
1. Stop all tool calls
2. Generate summary:
   ```
   Loop Detected
   ════════════════════════════════════
   Attempts: [N] rounds
   Repeated action: [action description]
   Error: [error message]
   What was tried: [list]
   ════════════════════════════════════
   ```
3. Ask user: "Should I try a different approach or stop?"

## Retry Decision Matrix

| Condition | Action |
|-----------|--------|
| Same error, 1st retry | Retry with adjusted params |
| Same error, 2nd retry | Stop, report, ask user |
| Different error | Continue, reset counter |
| Success after retry | Reset counter, continue |
| MAX_STEPS exceeded | Hard stop |

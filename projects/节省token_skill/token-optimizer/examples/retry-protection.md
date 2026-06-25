> Part of Token Optimizer V2. See also: [memory-compression](memory-compression.md), [rtk-integration](rtk-integration.md), [scenario-*](scenario-simple-qa.md)

# Retry Protection Example

## Scenario

Agent stuck trying to run tests that keep timing out.

## Loop Detection

```json
{
  "attempts": [
    {"step": 1, "action": "npm test", "result": "timeout", "time": "120s"},
    {"step": 2, "action": "npm test", "result": "timeout", "time": "120s"},
    {"step": 3, "action": "npm test", "result": "timeout", "time": "120s"}
  ],
  "loop_detected": true,
  "pattern": "same action, same error, 3 consecutive times"
}
```

## Emergency Stop Output

```
🔴 Loop Detected
═══════════════════════════════════════════════════
Action: npm test
Consecutive failures: 3
Error: timeout after 120s

What was tried:
1. Run full test suite → timeout
2. Run full test suite (retry) → timeout
3. Run full test suite (retry) → timeout

Possible causes:
- Test suite too large for timeout limit
- Infinite loop in test code
- External service dependency hanging

Suggested next steps:
□ Increase timeout: npm test --timeout 300
□ Run specific test: npm test -- --grep "test-name"
□ Check for hanging tests: npm test --detectOpenHandles

Should I try one of these, or do you have another approach?
═══════════════════════════════════════════════════
```

## After User Guidance

```json
{
  "loop_resolved": true,
  "resolution": "User suggested running specific test file",
  "action": "npm test tests/auth.test.js",
  "result": "success",
  "lesson": "When full suite times out, try running individual test files"
}
```

## Prevention Rules

1. **MAX_STEPS = 10** — Hard stop after 10 attempts
2. **Same-error threshold = 2** — Stop after same error twice
3. **No-progress threshold = 3** — Stop if no progress for 3 rounds
4. **Always report** — Never silently retry

# Module: Alerting

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

# Module 8: Alerting & Monitoring

## Token Budget Monitoring

Set budget thresholds and alert when exceeded:

```json
{
  "budget": {
    "daily_limit": 100000,
    "session_limit": 20000,
    "per_request_limit": 5000
  },
  "alerts": {
    "warning_threshold": 0.7,
    "critical_threshold": 0.9
  }
}
```

## Alert Levels

| Level | Threshold | Action |
|-------|-----------|--------|
| Normal | < 70% budget | Continue |
| Warning | 70-90% budget | Suggest optimization |
| Critical | > 90% budget | Pause and compress |
| Exceeded | 100% budget | Stop non-essential work |

## Monitoring Dashboard

```
Token Usage Monitor
═══════════════════════════════════════
Session:  ████████████░░░░░░░░  60% (12,000/20,000)
Daily:    ██████░░░░░░░░░░░░░░  30% (30,000/100,000)
Request:  ████░░░░░░░░░░░░░░░░  20% (1,000/5,000)
═══════════════════════════════════════
Status: Normal | Cache Hit: 75% | Model: Sonnet
```

## Anomaly Detection

Flag unusual patterns:
- Sudden spike in token usage (> 2x normal)
- Cache hit rate drops below 50%
- Same request type costs more than usual
- Output tokens significantly exceeds input

## Alert Actions

### Warning (70%)
```
⚠️ Token usage at 70% of session budget.
Suggestions:
- Compress conversation history (Module 3)
- Switch to Haiku for simple tasks (Module 5)
- Set response depth to 50% (Module 6)
```

### Critical (90%)
```
🔴 Token usage at 90% of session budget.
Actions taken:
- Compressed all non-essential context
- Switched to minimal response mode
- Consider starting new session for new tasks
```

## Cost Tracking Template

```json
{
  "session_id": "abc123",
  "start_time": "2026-05-28T10:00:00Z",
  "model": "claude-sonnet-4-6",
  "requests": 15,
  "tokens": {
    "input": 45000,
    "cached": 30000,
    "output": 8000
  },
  "estimated_cost": 0.15,
  "cache_hit_rate": 0.67
}
```

## Integration with Other Modules

| Alert Trigger | Recommended Module |
|---------------|-------------------|
| High token usage | Module 1 (Audit) |
| Low cache hit | Module 2 (Caching) |
| Context growing | Module 3 (Compression) |
| Simple tasks on Opus | Module 5 (Routing) |
| Verbose responses | Module 6 (Depth) |
| Agent looping | Module 7 (Retry) |

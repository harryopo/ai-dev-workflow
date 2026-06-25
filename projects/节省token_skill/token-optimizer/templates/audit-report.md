# Token Audit Report Template

Use this template for Module 1 audit output.

```
Token Audit Report
═══════════════════════════════════════════════════
Session: [session_id]
Date: [YYYY-MM-DD HH:MM]
Model: [model_name]

Context Distribution:
┌─────────────────────────────────────────────────┐
│ System Prompt           ~[X] tokens ([X]%)      │
│ Tool Definitions        ~[X] tokens ([X]%)      │
│ Conversation History    ~[X] tokens ([X]%)      │
│ Tool Results            ~[X] tokens ([X]%)      │
│ User Input              ~[X] tokens ([X]%)      │
│ Other                   ~[X] tokens ([X]%)      │
├─────────────────────────────────────────────────┤
│ Total                   ~[X] tokens (100%)      │
└─────────────────────────────────────────────────┘

Top Issues:
1. [Issue description] — potential saving: ~[X] tokens
2. [Issue description] — potential saving: ~[X] tokens
3. [Issue description] — potential saving: ~[X] tokens

Recommended Actions:
□ [Action 1] → Module [N]
□ [Action 2] → Module [N]
□ [Action 3] → Module [N]

Estimated Total Savings: ~[X] tokens ([X]%)
═══════════════════════════════════════════════════
```

## Notes

- All token counts are heuristic estimates (±15%)
- Use API response `usage` fields for precise counts when available
- Focus on top 3 issues first — 80/20 rule applies

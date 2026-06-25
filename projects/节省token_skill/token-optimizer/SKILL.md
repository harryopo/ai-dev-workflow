---
name: token-optimizer
description: |
  Token 优化框架。当用户提到"节省token"、"token成本"、"上下文过长"、
  "缓存优化"、"模型路由"、"策略选择"时触发。诊断并优化 token 使用。
  跳过：token 指认证/支付令牌时。
argument-hint: "[策略|诊断|缓存|压缩|画布|路由|深度|重试|监控]"

disable-model-invocation: false
user-invocable: true

context: inline
agent: "general-purpose"
allowed-tools: Read Write Edit Glob Grep
---

# Token Optimizer

Lean router with on-demand module loading. Core: **"Not making Agent remember more, but managing memory better."**

五层架构：L0 路由器（本文件）→ L1 策略选择器 → L2 优化模块 → L3 模板库 → L4 集成层。

## 触发条件

> 触发词已在 description 中定义，此处不重复。关键词 → 模块映射见下方 Decision Tree。

### 不触发
- token 指代认证/支付令牌；用户已设置过响应深度；"优化代码性能"

## Decision Tree

Match user request → load ONE module via `Read`:

```
Keywords                                              → Module
─────────────────────────────────────────────────────────────────
"策略" / "方案选择" / "8种方案" / "哪种策略"          → 0 (Strategy Selector)
"token 多" / "诊断" / "审计" / "浪费" / "压缩"       → 1 (Context Manager)
"缓存" / "cache" / "prompt caching" / "命中率"       → 2 (Caching)
"记忆" / "四层记忆" / "mermaid" / "画布" / "卸载"    → 3 (Memory Architect)
"CLI" / "RTK" / "命令输出" / "测试输出压缩"          → 4 (CLI Compress)
"Skills分层" / "信息分层" / "按需加载" / "拆分"       → 5 (Skills Splitter)
"用什么模型" / "路由" / "haiku/sonnet/opus" / "成本"  → 6 (Model Routing)
"循环" / "重试" / "卡住" / "MAX_STEPS"                → 7 (Retry Protection)
"告警" / "监控" / "花费异常"                          → 8 (Alerting)
未命中                                                → 1 (context audit first)
```

## Module Paths

| # | Module | Path |
|---|--------|------|
| 0 | Strategy Selector | `${CLAUDE_SKILL_DIR}/modules/module-strategy-selector.md` |
| 1 | Context Manager | `${CLAUDE_SKILL_DIR}/modules/module-context-manager.md` |
| 2 | Caching | `${CLAUDE_SKILL_DIR}/modules/module-caching.md` |
| 3 | Memory Architect | `${CLAUDE_SKILL_DIR}/modules/module-memory-architect.md` |
| 4 | CLI Compress | `${CLAUDE_SKILL_DIR}/modules/module-cli-compress.md` |
| 5 | Skills Splitter | `${CLAUDE_SKILL_DIR}/modules/module-skills-splitter.md` |
| 6 | Model Routing | `${CLAUDE_SKILL_DIR}/modules/module-routing.md` |
| 7 | Retry Protection | `${CLAUDE_SKILL_DIR}/modules/module-retry-protection.md` |
| 8 | Alerting | `${CLAUDE_SKILL_DIR}/modules/module-alerting.md` |

Templates: `${CLAUDE_SKILL_DIR}/templates/`
Examples: `${CLAUDE_SKILL_DIR}/examples/`
Evals: `${CLAUDE_SKILL_DIR}/evals/evals.json`（12 条评测：8 core + 3 edge + 1 boundary）

**Load rule:** Read the module file only when the user's request matches its keywords. Don't pre-load all modules.

## Multi-Module Flows

```
Full optimization:  0→1→2→3→4→5→6→7→8
Diagnosis mode:     1→(audit result selects next)
Cost optimization:  5→2→1
Long task:          4→3→7
Emergency (loop):   7→1
Strategy consult:   0→(strategy result selects module)
```

## Estimation Disclaimer

Heuristic estimation, not real tokenizer. Accuracy ~85-90%, deviation +-15%.

# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260528-001] best_practice

**Logged**: 2026-05-28T23:46:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Subagent-Driven 并行执行独立任务效果显著，但需要显式列出所有待处理文件

### Details
Token Optimizer V2 开发中，Tasks 2/3/4/6 并行执行（无依赖），总计节省约 50% 时间。但 Task 5（模块整合）的子代理遗漏了 module-4-canvas.md，因为该文件未在任务描述中显式列出。

### Suggested Action
- 并行派发子代理时，确保每个子代理的任务描述包含完整的文件清单
- 不要假设子代理会扫描目录发现遗漏的文件
- 合并操作应列出源文件和目标文件的完整映射

### Metadata
- Source: conversation
- Related Files: token-optimizer/modules/
- Tags: subagent, parallel-execution, file-operations

---

## [LRN-20260528-002] best_practice

**Logged**: 2026-05-28T23:46:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
文件重命名/合并后，必须同步更新所有引用该文件的路径（SKILL.md、imports、cross-references）

### Details
Task 5 子代理重命名了 5 个模块文件并合并了 2 个，但未更新 SKILL.md 中的 Module Paths 表。导致 SKILL.md 引用了不存在的旧文件名（module-1-audit.md 等）。需要手动修复。

### Suggested Action
- 文件重命名任务应包含"更新所有引用"作为显式步骤
- 考虑在重命名后运行 grep 检查旧文件名是否仍被引用
- SKILL.md 的 Module Paths 表是关键依赖，重命名模块时必须同步更新

### Metadata
- Source: conversation
- Related Files: token-optimizer/SKILL.md
- Tags: rename, cross-references, consistency

---

## [LRN-20260528-003] insight

**Logged**: 2026-05-28T23:46:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
五层架构设计中，L1 策略选择器作为独立模块比内嵌在 SKILL.md 中更灵活

### Details
最初计划将 8 种策略决策树直接放在 SKILL.md 中，后来提取为独立的 module-strategy-selector.md。好处：1) SKILL.md 保持精简（92行）2) 策略选择器可独立更新 3) 符合"按需加载"原则。

### Suggested Action
- 路由器（SKILL.md）只做关键词匹配和模块路由
- 决策逻辑、策略选择等复杂逻辑应放在独立模块中
- 这个模式可复用到其他大型 skill 的设计中

### Metadata
- Source: conversation
- Related Files: token-optimizer/SKILL.md, token-optimizer/modules/module-strategy-selector.md
- Tags: architecture, skill-design, modularity

---

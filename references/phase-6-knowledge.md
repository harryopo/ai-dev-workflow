# 阶段六：知识沉淀指南

> 所属 Skill：`ai-dev-workflow`
> 目标：把开发过程中产生的经验固化为项目知识

---

## 1. 知识四层架构

```
Layer 1: 项目宪法层（稳定，所有 Agent 启动必读）
  CLAUDE.md  |  ADR/*.md  |  Tech Stack

Layer 2: 领域知识层（扩展，中频变更）
  .claude/rules/  |  .claude/skills/  |  patterns/

Layer 3: 动态记忆层（流动，高频变更）
  .learnings/  |  session context  |  memories/

Layer 4: 外部增强层（按需检索）
  RAG 知识库  |  代码图谱  |  历史 Issue/PR
```

---

## 2. 知识流转机制

```
编码中发现 ──┐
审查中发现 ──┤
故障复盘   ──┼──→ .learnings/ ──→ 提炼 ──→ patterns/ ──→ CLAUDE.md
技术讨论   ──┘     (原始记录)     (抽象模式)      (硬性规则)
```

### 何时写 .learnings/

- 遇到一个非显然的 Bug 并解决
- 发现某个库的坑
- 做了一个有争议的设计决策
- 性能优化的技巧

### .learnings/ 文件格式

```markdown
# {日期}-{简短描述}.md

## 问题
...

## 原因
...

## 解决方案
...

## 经验教训
...

## 相关
- 关联 Issue/PR
- 相关 ADR
```

### 何时提升到 CLAUDE.md

当某个模式出现了 3 次以上、或造成了严重问题，应提升为硬性规则：

```
.learnings/ 中出现 3 次同一类问题
→ 提炼为 patterns/ 下的抽象模式
→ 如影响广泛，写入 CLAUDE.md 作为硬性规则
```

---

## 3. CLAUDE.md 更新策略

### 应该加入 CLAUDE.md 的内容

- **硬性规则**：禁止事项（如"禁止直接改 migration 文件"）
- **关键路径说明**：新人最需要知道的信息
- **踩过的坑**：重复出现的问题和正确做法

### 不应加入 CLAUDE.md 的内容

- 冗长的技术文档（放 docs/ 或 README）
- 临时的配置说明（放 .learnings/）
- 代码示例（放 patterns/ 或 wiki）

### 更新频率

- 小更新：每次功能交付后
- 大更新：每个 Sprint 结束时
- 紧急更新：发生重大故障后

---

## 4. 知识沉淀检查清单

在每个功能交付或 Sprint 结束时：

- [ ] .learnings/ 中有新的值得保留的记录？
- [ ] 有没有出现 3 次以上的同类问题？（→ 提升为规则）
- [ ] CLAUDE.md 是否需要更新？
- [ ] ADR 是否需要更新或新增？
- [ ] 有没有新的设计模式需要记录到 patterns/？
- [ ] RAG 知识库索引是否需要刷新？

---

## 5. 上下文管理要点

### 渐进式加载策略

| 层级 | 加载内容 | Token 预算 |
|------|----------|-----------|
| Level 1（启动） | CLAUDE.md + 任务描述 | 5000 |
| Level 2（编码） | 相关文件 ±200 行 + API Spec | 20000 |
| Level 3（审查） | 全量文件 + git diff + 规则 | 80000 |

### Handoff 协议（Agent 交接时）

```
handoff_package:
  - task_summary: "已完成的工作 + 关键决策"
  - unresolved: "未解决的问题 + 阻塞项"
  - next_steps: "下一步行动计划"
  - file_state: "修改过的文件清单"
  - test_status: "当前测试通过率"
```

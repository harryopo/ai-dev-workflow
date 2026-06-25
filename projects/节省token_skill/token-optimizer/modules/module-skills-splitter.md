# Module: Skills Splitter

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

## 信息分层原则

### P0 (Must-Know)
- 定义：核心决策规则，90% 的任务都需要
- 存放位置：CLAUDE.md
- 示例：
  - 架构设计原则
  - 编码风格规范
  - KISS 原则说明

### P1 (Should-Know)
- 定义：详细实现模板，30-50% 的任务需要
- 存放位置：.claude/commands/
- 示例：
  - Controller 代码模板
  - Model 代码模板
  - 交互反馈流程

### P2 (Nice-to-Have)
- 定义：低频工具流程，<20% 的任务需要
- 存放位置：docs/backup/
- 示例：
  - 重构检查清单
  - 第三方库集成流程
  - 部署运维手册

## 三大拆分标准

### 标准 1: 长度标准
- 规则：单个章节 > 100 行 → 候选拆分
- 原理：长内容通常意味着详细模板，不是核心决策规则
- 示例：
  - 50 行的"架构原则" → 不拆分
  - 200 行的"Controller 代码模板" → 拆分为 Skill

### 标准 2: 频率标准
- 规则：调用频率 < 50% → 优先拆分
- 原理：低频内容不应占据每次对话的 Token
- 示例：
  - "编码风格"（100% 调用） → 不拆分
  - "重构流程"（15% 调用） → 拆分为 Skill

### 标准 3: 独立性标准
- 规则：可以不依赖其他章节独立理解 → 可拆分
- 原理：独立内容适合封装为独立的 Skill
- 示例：
  - "Controller 实现"可以独立理解 → 可拆分
  - "Controller 与 Model 的交互"依赖两个概念 → 慎重拆分

## 拆分决策矩阵

| 长度 | 频率 | 独立性 | 决策 |
|------|------|--------|------|
| > 100行 | < 50% | 独立 | ✅ 强烈建议拆分 |
| > 100行 | < 50% | 依赖 | ⚠️ 考虑拆分并添加上下文 |
| > 100行 | > 50% | 独立 | ⚠️ 考虑精简核心规则，详细部分拆出去 |
| < 100行 | < 50% | 独立 | 可选拆分（收益不大） |
| < 100行 | > 50% | - | ❌ 保留 CLAUDE.md |

## 实施步骤

### Step 1: 审计现有文档
创建表格，记录每个章节的特征：

| 章节名称 | 行数 | 调用频率 | 是否详细模板 | 可否独立理解 | 初步分级 |
|----------|------|----------|--------------|--------------|----------|
| 架构设计原则 | 50 | 每次 | 否 | 是 | P0 |
| 编码风格规范 | 30 | 每次 | 否 | 是 | P0 |
| Controller 实现 | 200 | 新建时 | 是 | 是 | P1 |
| 重构流程 | 190 | 低频 | 是 | 是 | P2 |

### Step 2: 设计 Skills 命名规范

**Category 命名原则：**
- workflow/ - 开发流程类
- generate/ - 代码生成类
- tools/ - 辅助工具类

**Skill 命名格式：** /{category}:{name}
- 简洁：单词数 ≤ 3
- 语义化：见名知意
- 无歧义：避免缩写

### Step 3: 提取与转换

**创建 Skill 文件：**
```bash
mkdir -p .claude/commands/{workflow,generate,tools}
touch .claude/commands/generate/controller.md
```

**迁移详细内容：**
从 CLAUDE.md 复制详细内容到 Skill 文件，保持完整性。

**精简 CLAUDE.md：**
保留核心规则 + Skills 指引：
```markdown
## Controller 实现规范
- 职责：表现层组件，使用 `/generate:controller` 获取代码模板
- 关键原则：单一职责、依赖注入、异步优先
- 生命周期：Initialize() → Update() → Dispose()
```

### Step 4: 添加 Skills 索引

在 CLAUDE.md 中添加快速索引表：

```markdown
## ClaudeSkills 快速索引

| Skill 命令 | 用途 | 优先级 | 触发场景 |
|-----------|------|--------|---------|
| /workflow:interactive | 交互反馈流程 | P0 | 所有任务 |
| /generate:controller | Controller 模板 | P1 | 新建 Controller |
| /generate:model | Model 模板 | P1 | 新建 Model |
| /tools:context7 | 第三方库查询 | P2 | 引入新库时 |
| /tools:refactor | 重构检查清单 | P2 | 代码重构时 |
```

### Step 5: 创建备份文档

```bash
mkdir -p docs/backup
cp CLAUDE.md docs/backup/完整开发规范_原始版.md
```

添加降级指南：
```markdown
## ClaudeSkills 故障处理

### Skills 文件丢失
如果 `.claude/commands/` 目录丢失：
1. 恢复命令：`git checkout HEAD -- .claude/commands/`
2. 查看备份：`docs/backup/完整开发规范_原始版.md`

### 降级方案
- 代码生成：查看备份文档的"代码模板"章节
- 工作流程：查看备份文档的"任务处理流程"章节
```

## 定量收益

| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| CLAUDE.md 行数 | 457 行 | 263 行 | -42.5% |
| 基础 Token 消耗 | ~16,000 | ~9,200 | -42.5% |
| 月度 Token 节省 | - | 5.68M tokens | ~$17/月 |

## 三种场景效果

| 场景 | 占比 | 优化前 | 优化后 | 节省 |
|------|------|--------|--------|------|
| 简单问答 | 40% | 16,500 | 9,700 | 41.2% |
| 中等任务 | 45% | 17,500 | 11,200-13,000 | 26-36% |
| 复杂任务 | 15% | 19,000 | 18,900 | 0.5% |

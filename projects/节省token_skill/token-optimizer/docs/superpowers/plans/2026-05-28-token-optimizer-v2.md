# Token Optimizer V2: 全能 Token 优化框架实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于五篇 Token 优化参考文章，重构现有 token-optimizer skill 为五层全能架构，整合 8 种优化策略、CLI 压缩、记忆架构、Skills 分层等能力。

**Architecture:** 五层架构设计：L0 路由器 → L1 策略选择器 → L2 优化模块 → L3 模板库 → L4 集成层。核心创新：策略选择器（8 种方案决策树）、记忆架构模块（四层记忆）、CLI 压缩模块（RTK 策略）、Skills 分层模块（信息分层原则）。

**Tech Stack:** Markdown (SKILL.md + modules), Claude Code Skills 机制, Mermaid (决策树可视化), JSON (配置和模板)

---

## 现有架构分析

### 优势

1. **三层架构已验证**：L0 路由器 → L1 模块 → L2 模板/示例，按需加载模式成熟
2. **8 个模块覆盖全面**：审计、缓存、压缩、画布、路由、深度、重试、监控
3. **决策树清晰**：关键词 → 模块映射，触发条件明确
4. **260 行 SKILL.md**：已实现 42.5% 的 Token 节省（从 457 行精简）

### 不足（基于五篇文章洞察）

| 缺失能力 | 来源文章 | 影响 |
|----------|----------|------|
| 8 种方案决策树 | 文章 3（苏三说技术） | 无法根据场景自动推荐最优策略 |
| 四层记忆架构 | 文章 2（腾讯云） | 缺少记忆压缩和上下文卸载能力 |
| CLI 输出压缩 | 文章 4（RTK） | 无法优化命令行输出的 Token 消耗 |
| 信息分层原则 | 文章 5（知乎） | Skills 拆分缺少系统化方法论 |
| 向量检索/RAG | 文章 3 | 缺少长期记忆检索能力 |
| 状态变量提取 | 文章 3 | 任务型对话无法极致压缩 |
| 工具/函数调用 | 文章 3 | Agent 场景缺少记忆管理工具 |

---

## 新架构设计：五层全能架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 0: Router (路由器)                  │
│  - 触发条件匹配                                              │
│  - 任务复杂度评估                                            │
│  - 模块路由决策                                              │
│  文件: SKILL.md (精简路由器，~80行)                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Layer 1: Strategy Selector (策略选择器)      │
│  - 8 种方案决策树（全量/滑动窗口/摘要/RAG/分层/状态/工具）   │
│  - 场景匹配算法（简单问答/中等任务/复杂任务）                │
│  - 推荐最优策略组合                                          │
│  文件: modules/module-strategy-selector.md                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Layer 2: Optimization Modules (优化模块)        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Context  │ │ Memory   │ │ CLI      │ │ Skills   │      │
│  │ Manager  │ │ Architect│ │ Compress │ │ Splitter │      │
│  │ (上下文) │ │ (记忆)   │ │ (CLI)    │ │ (分层)   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Caching  │ │ Routing  │ │ Retry    │ │ Alerting │      │
│  │ (缓存)   │ │ (路由)   │ │ (重试)   │ │ (监控)   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  文件: modules/module-*.md (8个模块)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               Layer 3: Templates & Examples (模板库)         │
│  - 决策树模板（8种方案选择）                                 │
│  - 审计报告模板（上下文分布）                                │
│  - 记忆架构模板（四层记忆）                                  │
│  - 压缩策略模板（CLI/上下文/历史）                           │
│  - Skills 分层模板（P0/P1/P2）                              │
│  文件: templates/*.md, examples/*.md                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                Layer 4: Integration (集成层)                 │
│  - RTK 集成指南（CLI 代理压缩）                              │
│  - MCP 工具集成（Sequential Thinking, Context7 等）         │
│  - 外部服务接口（向量数据库、Embedding 服务）               │
│  文件: integrations/*.md                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 文件结构

```
token-optimizer/
├── SKILL.md                          # L0: 路由器 (~80行)
├── modules/
│   ├── module-strategy-selector.md   # L1: 策略选择器 (8种方案决策树)
│   ├── module-context-manager.md     # L2: 上下文管理 (合并原 module-1,3)
│   ├── module-memory-architect.md    # L2: 记忆架构 (新增，四层记忆)
│   ├── module-cli-compress.md        # L2: CLI压缩 (新增，RTK策略)
│   ├── module-skills-splitter.md     # L2: Skills分层 (新增，信息分层)
│   ├── module-caching.md             # L2: 缓存优化 (保留原 module-2)
│   ├── module-routing.md             # L2: 模型路由 (保留原 module-5)
│   ├── module-retry-protection.md    # L2: 重试保护 (保留原 module-7)
│   └── module-alerting.md            # L2: 监控告警 (保留原 module-8)
├── templates/
│   ├── decision-tree.md              # 8种方案选择决策树
│   ├── audit-report.md               # 审计报告模板
│   ├── memory-architecture.md        # 四层记忆架构模板
│   ├── compression-strategy.md       # 压缩策略选择模板
│   └── skills-layering.md            # Skills分层模板
├── examples/
│   ├── scenario-simple-qa.md         # 简单问答场景示例
│   ├── scenario-medium-task.md       # 中等任务场景示例
│   ├── scenario-complex-task.md      # 复杂任务场景示例
│   ├── rtk-integration.md            # RTK集成示例
│   └── memory-compression.md         # 记忆压缩示例
├── integrations/
│   ├── rtk-guide.md                  # RTK集成指南
│   ├── mcp-tools.md                  # MCP工具集成
│   └── vector-db.md                  # 向量数据库集成
└── references/
    └── external-links.md             # 外部参考链接
```

---

## 核心模块设计

### 1. Strategy Selector（策略选择器）

**职责：** 根据用户场景自动推荐最优 Token 优化策略

**决策树：**

```
用户场景
├── 短对话（<10轮）
│   ├── 信息完整性要求高 → 全量记忆
│   └── 信息完整性要求低 → 滑动窗口
├── 长对话（>20轮）
│   ├── 信息密度高 → 分层混合记忆
│   ├── 信息密度低 → 摘要压缩
│   └── 需要长期记忆 → 向量检索(RAG)
├── 任务型对话（订票/表单）
│   └── 状态变量提取
├── Agent场景
│   └── 工具/函数调用
└── CLI输出优化
    └── RTK代理压缩
```

**输出：** 推荐策略 + 预计节省 + 实施步骤

### 2. Memory Architect（记忆架构）

**职责：** 实现腾讯云四层记忆架构

**四层设计：**

| 层级 | 内容 | 格式 | 触发条件 |
|------|------|------|----------|
| Level 0 | Raw 原文 | refs/*.md | 始终保存 |
| Level 1 | JSONL Summary | 工具调用级摘要 | 每次工具调用后 |
| Level 2 | MMD Node | 任务步骤级摘要 | 每完成一个步骤 |
| Level 3 | Metadata | 任务级索引 | 任务完成时 |

**压缩策略：**
- 上下文卸载：将旧对话移至 refs/ 目录
- Mermaid 画布：用 Mermaid 图记录任务状态
- 层次化注意力：鸟瞰 → 聚焦 → 下钻

### 3. CLI Compress（CLI 压缩）

**职责：** 整合 RTK 的四种压缩策略

**策略矩阵：**

| 策略 | 适用场景 | 压缩率 | 实现方式 |
|------|----------|--------|----------|
| 智能过滤 | 测试输出 | 90% | 100个PASSED → "100个测试全部通过" |
| 分组聚合 | git log | 80% | 50条commit → 摘要 |
| 智能截断 | 错误堆栈 | 70% | 只保留前几行 |
| 去重处理 | 重复信息 | 60% | 相同信息只保留一份 |

**集成方式：**
- 推荐用户安装 RTK：`rtk init -g`
- 提供 RTK 配置模板
- 监控 RTK 统计：`rtk gain --project`

### 4. Skills Splitter（Skills 分层）

**职责：** 实现知乎文章的信息分层原则

**分层标准：**

| 层级 | 定义 | 判断标准 | 存放位置 |
|------|------|----------|----------|
| P0 | Must-Know | 90%任务需要，核心决策规则 | CLAUDE.md |
| P1 | Should-Know | 30-50%任务需要，详细模板 | Skills |
| P2 | Nice-to-Have | <20%任务需要，低频工具 | 备份文档 |

**拆分决策矩阵：**

| 长度 | 频率 | 独立性 | 决策 |
|------|------|--------|------|
| >100行 | <50% | 独立 | 强烈建议拆分 |
| >100行 | >50% | 独立 | 精简核心，详细拆出 |
| <100行 | >50% | - | 保留 CLAUDE.md |

---

## 任务分解

### Task 1: 重构 SKILL.md 路由器

**目标：** 将现有 260 行 SKILL.md 精简为 ~80 行路由器

**Files:**
- Modify: `token-optimizer/SKILL.md`
- Create: `token-optimizer/modules/module-strategy-selector.md`

**Steps:**

- [ ] **Step 1: 分析现有 SKILL.md 结构**

读取当前 SKILL.md，识别可拆分内容：
- 触发条件 → 保留（精简）
- Decision Tree → 保留（精简）
- Module Paths → 保留
- 工作流程 → 移至 module-strategy-selector.md
- 输入/输出规范 → 移至 module-strategy-selector.md
- 示例 → 移至 examples/
- 注意事项 → 移至 module-strategy-selector.md

- [ ] **Step 2: 创建 module-strategy-selector.md**

```markdown
# Module: Strategy Selector

## 8 种优化策略决策树

### 策略 1: 全量记忆
- 场景：短对话（<10轮），信息完整性要求高
- 节省：0%（无节省）
- 实现：保留所有对话历史

### 策略 2: 滑动窗口
- 场景：短对话，信息完整性要求低
- 节省：极高（固定窗口）
- 实现：只保留最近 N 轮对话

### 策略 3: 摘要压缩
- 场景：长对话（>20轮），信息密度低
- 节省：70-90%
- 实现：定期让 LLM 压缩旧对话为摘要

### 策略 4: 向量检索(RAG)
- 场景：需要长期记忆，语义检索
- 节省：高（topK）
- 实现：向量化存储 + 相似度检索

### 策略 5: 分层混合记忆
- 场景：长对话，信息密度高
- 节省：高
- 实现：短期窗口 + 中期摘要 + 长期向量

### 策略 6: 状态变量提取
- 场景：任务型对话（订票/表单）
- 节省：极高（近乎0）
- 实现：提取结构化状态变量

### 策略 7: 工具/函数调用
- 场景：Agent 场景
- 节省：极高
- 实现：让模型自主管理记忆工具

### 策略 8: CLI 代理压缩
- 场景：CLI 输出优化
- 节省：60-90%
- 实现：RTK 代理压缩命令输出

## 场景匹配算法

\`\`\`python
def select_strategy(scenario):
    if scenario.turns < 10:
        if scenario.integrity == "high":
            return "全量记忆"
        else:
            return "滑动窗口"
    elif scenario.turns > 20:
        if scenario.density == "high":
            return "分层混合记忆"
        elif scenario.need_long_term:
            return "向量检索(RAG)"
        else:
            return "摘要压缩"
    elif scenario.type == "task":
        return "状态变量提取"
    elif scenario.type == "agent":
        return "工具/函数调用"
    elif scenario.has_cli_output:
        return "CLI 代理压缩"
    else:
        return "摘要压缩"  # 默认
\`\`\`

## 输出格式

\`\`\`
Token 优化策略推荐
═══════════════════════════════════════
场景：[场景描述]
推荐策略：[策略名称]
预计节省：[X]%
实施步骤：
1. [步骤1]
2. [步骤2]
═══════════════════════════════════════
\`\`\`
```

- [ ] **Step 3: 精简 SKILL.md**

将 SKILL.md 从 260 行精简为 ~80 行：
- 保留：触发条件、Decision Tree、Module Paths
- 移除：工作流程详情、输入/输出规范、示例、注意事项
- 添加：指向 module-strategy-selector.md 的指引

- [ ] **Step 4: 测试路由器功能**

验证：
1. 触发条件匹配正确
2. Decision Tree 路由正确
3. 模块加载正确

- [ ] **Step 5: Commit**

```bash
git add token-optimizer/SKILL.md token-optimizer/modules/module-strategy-selector.md
git commit -m "refactor: extract strategy selector from SKILL.md"
```

---

### Task 2: 创建 Memory Architect 模块

**目标：** 实现腾讯云四层记忆架构

**Files:**
- Create: `token-optimizer/modules/module-memory-architect.md`
- Create: `token-optimizer/templates/memory-architecture.md`
- Create: `token-optimizer/examples/memory-compression.md`

**Steps:**

- [ ] **Step 1: 创建 module-memory-architect.md**

```markdown
# Module: Memory Architect

## 四层记忆架构

### Level 0: Raw 原文
- 存储位置：refs/*.md
- 内容：完整的工具调用结果、对话原文
- 保留策略：始终保存，不删除

### Level 1: JSONL Summary
- 存储位置：refs/summary.jsonl
- 内容：工具调用级摘要
- 格式：
\`\`\`json
{
  "timestamp": "2026-05-28T10:00:00",
  "tool": "read_file",
  "input": "path/to/file.py",
  "output_summary": "读取了 Python 文件，包含 3 个函数...",
  "key_facts": ["函数名: main, init, process"],
  "token_saved": 1500
}
\`\`\`
- 触发条件：每次工具调用后

### Level 2: MMD Node
- 存储位置：canvas/task-state.mmd
- 内容：任务步骤级摘要（Mermaid 图）
- 格式：
\`\`\`mermaid
graph TD
    A[开始] --> B[读取文件]
    B --> C[分析代码]
    C --> D[生成报告]
    D --> E[完成]
\`\`\`
- 触发条件：每完成一个步骤

### Level 3: Metadata
- 存储位置：refs/metadata.json
- 内容：任务级索引
- 格式：
\`\`\`json
{
  "task_id": "task-001",
  "task_name": "代码审查",
  "start_time": "2026-05-28T10:00:00",
  "end_time": "2026-05-28T10:30:00",
  "total_tokens": 15000,
  "saved_tokens": 8000,
  "strategies_used": ["摘要压缩", "CLI压缩"],
  "key_decisions": ["使用 Sonnet 模型", "启用 RTK"]
}
\`\`\`
- 触发条件：任务完成时

## 上下文卸载策略

### 何时卸载
- 对话超过 20 轮
- 上下文超过 8000 tokens
- 工具结果超过 500 tokens

### 如何卸载
1. 将旧对话保存到 refs/history-*.md
2. 生成摘要替代原文
3. 保留最近 3 轮对话原文

## Mermaid 画布使用

### 任务状态图
\`\`\`mermaid
stateDiagram-v2
    [*] --> 分析需求
    分析需求 --> 设计方案
    设计方案 --> 编码实现
    编码实现 --> 测试验证
    测试验证 --> [*]
\`\`\`

### 决策流程图
\`\`\`mermaid
flowchart TD
    A[用户请求] --> B{Token > 8000?}
    B -->|是| C[启用压缩]
    B -->|否| D[保持原样]
    C --> E[选择压缩策略]
\`\`\`

## 层次化注意力

### 鸟瞰（任务级）
- 查看 metadata.json
- 了解任务整体进度

### 聚焦（步骤级）
- 查看 canvas/task-state.mmd
- 了解当前步骤状态

### 下钻（工具级）
- 查看 refs/summary.jsonl
- 了解具体工具调用结果
```

- [ ] **Step 2: 创建 memory-architecture.md 模板**

```markdown
# 记忆架构模板

## 初始化

\`\`\`bash
mkdir -p refs canvas
touch refs/summary.jsonl refs/metadata.json canvas/task-state.mmd
\`\`\`

## Level 0: 保存原文

\`\`\`bash
# 保存工具调用结果
echo "$(date): Tool call result" >> refs/tool-calls-$(date +%Y%m%d).md
\`\`\`

## Level 1: 生成摘要

\`\`\`python
def generate_summary(tool_name, input_data, output_data):
    summary = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "input": str(input_data)[:100],
        "output_summary": summarize(output_data),
        "key_facts": extract_facts(output_data),
        "token_saved": estimate_tokens(output_data) - estimate_tokens(summarize(output_data))
    }
    with open("refs/summary.jsonl", "a") as f:
        f.write(json.dumps(summary) + "\n")
\`\`\`

## Level 2: 更新 Mermaid 画布

\`\`\`python
def update_canvas(step_name, status):
    # 读取现有画布
    with open("canvas/task-state.mmd", "r") as f:
        content = f.read()

    # 添加新步骤
    new_step = f"    {step_name} --> {status}"
    content = content.replace("    [*]", f"    {new_step}\n    [*]")

    # 保存
    with open("canvas/task-state.mmd", "w") as f:
        f.write(content)
\`\`\`

## Level 3: 更新元数据

\`\`\`python
def update_metadata(task_id, task_name, tokens_used, tokens_saved):
    metadata = {
        "task_id": task_id,
        "task_name": task_name,
        "start_time": datetime.now().isoformat(),
        "total_tokens": tokens_used,
        "saved_tokens": tokens_saved,
        "strategies_used": [],
        "key_decisions": []
    }
    with open("refs/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
\`\`\`
```

- [ ] **Step 3: 创建 memory-compression.md 示例**

```markdown
# 记忆压缩示例

## 场景：代码审查任务

### 初始状态
- 对话轮数：25 轮
- 上下文大小：12,000 tokens
- 工具调用：15 次

### 压缩过程

#### Step 1: 卸载旧对话
\`\`\`
refs/history-20260528-1000.md (前 20 轮)
refs/history-20260528-1030.md (第 21-25 轮)
\`\`\`

#### Step 2: 生成摘要
\`\`\`json
{
  "type": "history_summary",
  "task": "代码审查",
  "summary": "审查了 Python 项目，发现 3 个问题：1) main 函数过长 2) 缺少错误处理 3) 命名不规范",
  "key_decisions": ["建议拆分 main 函数", "添加 try-except"],
  "current_state": "等待用户确认修改方案",
  "protected_recent": ["最近 3 轮对话"]
}
\`\`\`

#### Step 3: 更新 Mermaid 画布
\`\`\`mermaid
graph TD
    A[开始审查] --> B[读取代码]
    B --> C[发现问题]
    C --> D[生成报告]
    D --> E[等待确认]
\`\`\`

#### Step 4: 更新元数据
\`\`\`json
{
  "task_id": "review-001",
  "task_name": "代码审查",
  "total_tokens": 12000,
  "saved_tokens": 6000,
  "strategies_used": ["摘要压缩", "上下文卸载"],
  "key_decisions": ["保留最近3轮", "生成结构化摘要"]
}
\`\`\`

### 压缩结果
- 压缩前：12,000 tokens
- 压缩后：6,000 tokens
- 节省：50%
- 信息保留率：95%（关键信息完整）
```

- [ ] **Step 4: 测试记忆架构**

验证：
1. 四层记忆正确创建
2. 上下文卸载正常工作
3. Mermaid 画布正确更新
4. 元数据正确记录

- [ ] **Step 5: Commit**

```bash
git add token-optimizer/modules/module-memory-architect.md \
       token-optimizer/templates/memory-architecture.md \
       token-optimizer/examples/memory-compression.md
git commit -m "feat: add memory architect module with 4-layer architecture"
```

---

### Task 3: 创建 CLI Compress 模块

**目标：** 整合 RTK 的四种压缩策略

**Files:**
- Create: `token-optimizer/modules/module-cli-compress.md`
- Create: `token-optimizer/integrations/rtk-guide.md`
- Create: `token-optimizer/examples/rtk-integration.md`

**Steps:**

- [ ] **Step 1: 创建 module-cli-compress.md**

```markdown
# Module: CLI Compress

## 四种压缩策略

### 策略 1: 智能过滤
- 适用场景：测试输出
- 压缩率：90%
- 实现方式：
  - 100 个 PASSED → "100 个测试全部通过"
  - 保留失败测试的完整信息

### 策略 2: 分组聚合
- 适用场景：git log, ls, grep
- 压缩率：80%
- 实现方式：
  - git log 50 条 → "最近 50 次提交摘要"
  - ls 100 个文件 → "100 个文件，按类型分组"

### 策略 3: 智能截断
- 适用场景：错误堆栈
- 压缩率：70%
- 实现方式：
  - 只保留前 5 行错误信息
  - 保留文件路径和行号

### 策略 4: 去重处理
- 适用场景：重复信息
- 压缩率：60%
- 实现方式：
  - 相同信息只保留一份
  - 用引用替代重复内容

## RTK 集成

### 安装
\`\`\`bash
# macOS
brew install rtk

# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh

# 初始化（Claude Code）
rtk init -g
\`\`\`

### 配置
\`\`\`toml
# ~/.config/rtk/config.toml
[commands]
exclude = ["vim", "nano", "less"]

[tee]
enabled = true  # 失败时保存完整原始输出
\`\`\`

### 常用命令
\`\`\`bash
# 查看统计
rtk gain --project

# 分析最耗 Token 的命令
rtk discover

# 查看过滤掉的完整信息
rtk tee show

# 绕过 RTK 执行原始命令
/usr/bin/git status
\`\`\`

## 压缩策略选择

| 命令类型 | 推荐策略 | 预计节省 |
|----------|----------|----------|
| cargo test / pytest | 智能过滤 | 90% |
| git add/commit/push | 分组聚合 | 92% |
| ls / grep / git log | 分组聚合 | 80% |
| npm install / pip install | 智能截断 | 85% |
| 错误堆栈 | 智能截断 | 70% |
| 重复输出 | 去重处理 | 60% |

## 监控与调优

### 查看压缩效果
\`\`\`bash
rtk gain --project
\`\`\`

输出示例：
\`\`\`
Project: my-project
Commands processed: 13
Input tokens: 18.2k
Output tokens: 5.9k
Tokens saved: 12.4k
Savings: 67.8%
\`\`\`

### 调优建议
1. 如果压缩过度导致 AI 重新执行命令 → 调整压缩阈值
2. 如果关键信息被过滤 → 将该命令加入排除列表
3. 定期运行 `rtk discover` 分析优化空间
```

- [ ] **Step 2: 创建 rtk-guide.md 集成指南**

```markdown
# RTK 集成指南

## 概述
RTK (Rust Token Killer) 是一个 CLI 代理，在命令行输出到达 LLM 之前做智能压缩和过滤。

## 安装与配置

### 安装
\`\`\`bash
# macOS
brew install rtk

# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh

# Windows (via cargo)
cargo install --git https://github.com/rtk-ai/rtk
\`\`\`

### 初始化
\`\`\`bash
# Claude Code
rtk init -g

# Codex
rtk init -g --codex

# Gemini CLI
rtk init -g --gemini

# Cursor
rtk init --agent cursor
\`\`\`

### 配置文件
\`\`\`bash
rtk config --create
# 编辑 ~/.config/rtk/config.toml
\`\`\`

## 使用方式

### 自动 Hook
RTK 初始化后会自动 hook 常用命令：
- git, ls, grep, find
- npm, pip, cargo, maven
- pytest, jest, cargo test

### 手动包装
\`\`\`bash
rtk git status
rtk mvn test
rtk npm install
\`\`\`

### 绕过 RTK
\`\`\`bash
/usr/bin/git status
\`\`\`

## 监控与调试

### 查看统计
\`\`\`bash
rtk gain --project
rtk gain --global
\`\`\`

### 分析优化空间
\`\`\`bash
rtk discover
\`\`\`

### 查看过滤信息
\`\`\`bash
rtk tee show
\`\`\`

## 最佳实践

1. **保持默认配置**：除非有特殊需求，不要修改压缩阈值
2. **定期检查统计**：每周运行 `rtk gain --project` 查看节省效果
3. **调试时绕过**：遇到问题时用完整路径执行原始命令
4. **保留失败输出**：开启 `tee.enabled = true` 以便调试
```

- [ ] **Step 3: 创建 rtk-integration.md 示例**

```markdown
# RTK 集成示例

## 场景：Python 项目测试

### 无 RTK
\`\`\`bash
$ pytest tests/
============================= test session starts ==============================
platform linux -- Python 3.10.0, pytest-7.4.0
rootdir: /home/user/project
collected 100 items

tests/test_main.py::test_add PASSED                                      [  1%]
tests/test_main.py::test_subtract PASSED                                 [  2%]
tests/test_main.py::test_multiply PASSED                                 [  3%]
... (97 more lines)

============================== 100 passed in 2.34s ==============================
\`\`\`

Token 消耗：~500 tokens

### 有 RTK
\`\`\`bash
$ rtk pytest tests/
100 tests passed (2.34s)
\`\`\`

Token 消耗：~20 tokens
节省：96%

## 场景：Git 操作

### 无 RTK
\`\`\`bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)

        modified:   src/main.py
        modified:   src/utils.py
        modified:   tests/test_main.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        docs/new-feature.md

no changes added to commit (use "git add" and/or "git commit -a")
\`\`\`

Token 消耗：~150 tokens

### 有 RTK
\`\`\`bash
$ rtk git status
Branch: main (up to date)
Modified: src/main.py, src/utils.py, tests/test_main.py
Untracked: docs/new-feature.md
\`\`\`

Token 消耗：~30 tokens
节省：80%

## 场景：Maven 测试

### 无 RTK
\`\`\`bash
$ mvn test
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------< com.example:my-project >-------------------
[INFO] Building my-project 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- maven-resources-plugin:3.3.0:resources (default-resources) @ my-project ---
[INFO] --- maven-compiler-plugin:3.11.0:compile (default-compile) @ my-project ---
[INFO] --- maven-resources-plugin:3.3.0:testResources (default-testResources) @ my-project ---
[INFO] --- maven-compiler-plugin:3.11.0:testCompile (default-testCompile) @ my-project ---
[INFO] --- maven-surefire-plugin:3.1.2:test (default-test) @ my-project ---
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.example.MainTest
[INFO] Tests run: 50, Failures: 0, Errors: 0, Skipped: 0
[INFO] Running com.example.UtilsTest
[INFO] Tests run: 30, Failures: 0, Errors: 0, Skipped: 0
[INFO] Running com.example.IntegrationTest
[INFO] Tests run: 20, Failures: 0, Errors: 0, Skipped: 0
[INFO] -------------------------------------------------------
[INFO]  T E S T S   R U N
[INFO] -------------------------------------------------------
[INFO]  Total: 100  |  Passed: 100  |  Failed: 0  |  Skipped: 0
[INFO] -------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] -------------------------------------------------------
[INFO] Total time:  12.345 s
\`\`\`

Token 消耗：~800 tokens

### 有 RTK
\`\`\`bash
$ rtk mvn test
100 tests passed (12.345s)
BUILD SUCCESS
\`\`\`

Token 消耗：~30 tokens
节省：96%
```

- [ ] **Step 4: 测试 CLI 压缩模块**

验证：
1. RTK 安装指南正确
2. 压缩策略说明清晰
3. 示例代码可运行

- [ ] **Step 5: Commit**

```bash
git add token-optimizer/modules/module-cli-compress.md \
       token-optimizer/integrations/rtk-guide.md \
       token-optimizer/examples/rtk-integration.md
git commit -m "feat: add CLI compress module with RTK integration"
```

---

### Task 4: 创建 Skills Splitter 模块

**目标：** 实现知乎文章的信息分层原则

**Files:**
- Create: `token-optimizer/modules/module-skills-splitter.md`
- Create: `token-optimizer/templates/skills-layering.md`
- Create: `token-optimizer/examples/scenario-simple-qa.md`
- Create: `token-optimizer/examples/scenario-medium-task.md`
- Create: `token-optimizer/examples/scenario-complex-task.md`

**Steps:**

- [ ] **Step 1: 创建 module-skills-splitter.md**

```markdown
# Module: Skills Splitter

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
\`\`\`bash
mkdir -p .claude/commands/{workflow,generate,tools}
touch .claude/commands/generate/controller.md
\`\`\`

**迁移详细内容：**
从 CLAUDE.md 复制详细内容到 Skill 文件，保持完整性。

**精简 CLAUDE.md：**
保留核心规则 + Skills 指引：
\`\`\`markdown
## Controller 实现规范
- 职责：表现层组件，使用 `/generate:controller` 获取代码模板
- 关键原则：单一职责、依赖注入、异步优先
- 生命周期：Initialize() → Update() → Dispose()
\`\`\`

### Step 4: 添加 Skills 索引

在 CLAUDE.md 中添加快速索引表：

\`\`\`markdown
## ClaudeSkills 快速索引

| Skill 命令 | 用途 | 优先级 | 触发场景 |
|-----------|------|--------|---------|
| /workflow:interactive | 交互反馈流程 | P0 | 所有任务 |
| /generate:controller | Controller 模板 | P1 | 新建 Controller |
| /generate:model | Model 模板 | P1 | 新建 Model |
| /tools:context7 | 第三方库查询 | P2 | 引入新库时 |
| /tools:refactor | 重构检查清单 | P2 | 代码重构时 |
\`\`\`

### Step 5: 创建备份文档

\`\`\`bash
mkdir -p docs/backup
cp CLAUDE.md docs/backup/完整开发规范_原始版.md
\`\`\`

添加降级指南：
\`\`\`markdown
## ClaudeSkills 故障处理

### Skills 文件丢失
如果 `.claude/commands/` 目录丢失：
1. 恢复命令：`git checkout HEAD -- .claude/commands/`
2. 查看备份：`docs/backup/完整开发规范_原始版.md`

### 降级方案
- 代码生成：查看备份文档的"代码模板"章节
- 工作流程：查看备份文档的"任务处理流程"章节
\`\`\`

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
```

- [ ] **Step 2: 创建 skills-layering.md 模板**

```markdown
# Skills 分层模板

## 审计表格模板

| 章节名称 | 行数 | 调用频率 | 是否详细模板 | 可否独立理解 | 初步分级 |
|----------|------|----------|--------------|--------------|----------|
| | | | | | |

## Skills 命名模板

\`\`\`markdown
# .claude/commands/{category}/{name}.md

# {Skill 名称}

## 职责定义
{Skill 的职责描述}

## 使用场景
- 场景 1：{描述}
- 场景 2：{描述}

## 代码模板
\`\`\`{language}
{代码模板}
\`\`\`

## 使用示例
\`\`\`bash
{使用示例}
\`\`\`

## 注意事项
- 注意 1：{描述}
- 注意 2：{描述}
\`\`\`

## CLAUDE.md 精简模板

\`\`\`markdown
## {模块名称}
- 职责：{一句话描述}
- 关键原则：
  - {原则 1}
  - {原则 2}
- 详细实现：使用 `/{category}:{name}` 获取
\`\`\`

## Skills 索引模板

\`\`\`markdown
## ClaudeSkills 快速索引

| Skill 命令 | 用途 | 优先级 | 触发场景 |
|-----------|------|--------|---------|
| /{category}:{name} | {用途} | {P0/P1/P2} | {触发场景} |
\`\`\`
```

- [ ] **Step 3: 创建场景示例**

创建三个场景示例文件，展示不同复杂度任务的优化效果。

- [ ] **Step 4: 测试 Skills 分层**

验证：
1. 审计表格准确
2. 拆分决策正确
3. Skills 索引完整
4. 降级方案可行

- [ ] **Step 5: Commit**

```bash
git add token-optimizer/modules/module-skills-splitter.md \
       token-optimizer/templates/skills-layering.md \
       token-optimizer/examples/scenario-simple-qa.md \
       token-optimizer/examples/scenario-medium-task.md \
       token-optimizer/examples/scenario-complex-task.md
git commit -m "feat: add skills splitter module with layering principles"
```

---

### Task 5: 整合现有模块

**目标：** 将现有 8 个模块整合到新架构

**Files:**
- Modify: `token-optimizer/modules/module-1-audit.md` → `module-context-manager.md`
- Modify: `token-optimizer/modules/module-2-caching.md` → `module-caching.md`
- Modify: `token-optimizer/modules/module-3-compression.md` → 合并到 `module-context-manager.md`
- Modify: `token-optimizer/modules/module-4-canvas.md` → 合并到 `module-memory-architect.md`
- Modify: `token-optimizer/modules/module-5-routing.md` → `module-routing.md`
- Modify: `token-optimizer/modules/module-6-depth.md` → 合并到 `module-context-manager.md`
- Modify: `token-optimizer/modules/module-7-retry.md` → `module-retry-protection.md`
- Modify: `token-optimizer/modules/module-8-alerting.md` → `module-alerting.md`

**Steps:**

- [ ] **Step 1: 重命名和合并模块**

\`\`\`bash
cd token-optimizer/modules

# 重命名
mv module-1-audit.md module-context-manager.md
mv module-2-caching.md module-caching.md
mv module-5-routing.md module-routing.md
mv module-7-retry.md module-retry-protection.md
mv module-8-alerting.md module-alerting.md

# 合并
cat module-3-compression.md >> module-context-manager.md
cat module-6-depth.md >> module-context-manager.md

# 删除已合并文件
rm module-3-compression.md module-6-depth.md
\`\`\`

- [ ] **Step 2: 更新模块内容**

在每个模块开头添加新架构的引用：

\`\`\`markdown
# Module: {模块名称}

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

## 概述
{模块概述}

## 核心功能
{核心功能}

## 使用场景
{使用场景}

## 实施步骤
{实施步骤}
\`\`\`

- [ ] **Step 3: 更新 SKILL.md 模块路径**

更新 SKILL.md 中的 Module Paths 表格：

\`\`\`markdown
## Module Paths

| # | Module | Path |
|---|--------|------|
| 1 | Strategy Selector | `${CLAUDE_SKILL_DIR}/modules/module-strategy-selector.md` |
| 2 | Context Manager | `${CLAUDE_SKILL_DIR}/modules/module-context-manager.md` |
| 3 | Memory Architect | `${CLAUDE_SKILL_DIR}/modules/module-memory-architect.md` |
| 4 | CLI Compress | `${CLAUDE_SKILL_DIR}/modules/module-cli-compress.md` |
| 5 | Skills Splitter | `${CLAUDE_SKILL_DIR}/modules/module-skills-splitter.md` |
| 6 | Caching | `${CLAUDE_SKILL_DIR}/modules/module-caching.md` |
| 7 | Routing | `${CLAUDE_SKILL_DIR}/modules/module-routing.md` |
| 8 | Retry Protection | `${CLAUDE_SKILL_DIR}/modules/module-retry-protection.md` |
| 9 | Alerting | `${CLAUDE_SKILL_DIR}/modules/module-alerting.md` |
\`\`\`

- [ ] **Step 4: 测试模块整合**

验证：
1. 所有模块可正常加载
2. 模块间引用正确
3. Decision Tree 路由正确

- [ ] **Step 5: Commit**

\`\`\`bash
git add token-optimizer/modules/
git commit -m "refactor: integrate existing modules into new architecture"
\`\`\`

---

### Task 6: 创建集成层

**目标：** 创建 MCP 工具和向量数据库集成指南

**Files:**
- Create: `token-optimizer/integrations/mcp-tools.md`
- Create: `token-optimizer/integrations/vector-db.md`

**Steps:**

- [ ] **Step 1: 创建 mcp-tools.md**

```markdown
# MCP 工具集成

## 核心 MCP 工具

| 工具 | 用途 | 降级方案 |
|------|------|----------|
| sequential-thinking | 深度思考和推理链 | TodoWrite 分步规划 |
| mcp-shrimp-task-manager | 任务分解与依赖管理 | TodoWrite 任务列表 |
| context7 | 第三方库文档查询 | WebSearch + GitHub |
| interactive-feedback | 结构化用户交互 | 文本结构化反馈 |
| filesystem | 文件系统操作 | 原生文件操作 |

## 容错机制

### 自动重试
- 网络超时等临时故障，自动重试 3 次
- 指数退避：1s → 2s → 4s

### 降级矩阵
\`\`\`
MCP 工具故障 → 检查降级方案 → 使用替代工具 → 通知用户
\`\`\`

### 通知示例
\`\`\`
⚠️ MCP 工具降级通知
【故障工具】：sequential-thinking
【降级方案】：TodoWrite 分步规划
【功能影响】：无法进行思维链验证，分析深度降低
【需要注意】：请额外关注任务依赖关系和边界条件
\`\`\`

## 集成示例

### Sequential Thinking
\`\`\`python
# 使用 Sequential Thinking 进行深度思考
result = mcp.sequential_thinking.think(
    thought="分析问题...",
    thought_number=1,
    total_thoughts=5
)
\`\`\`

### Context7
\`\`\`python
# 使用 Context7 查询库文档
docs = mcp.context7.get_docs(
    library="react",
    query="useEffect hook"
)
\`\`\`
```

- [ ] **Step 2: 创建 vector-db.md**

```markdown
# 向量数据库集成

## 概述
向量检索(RAG)是当前工业界最主流的长期记忆方案。

## 支持的向量数据库

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| Chroma | 轻量级，易部署 | 小型项目 |
| Milvus | 高性能，分布式 | 大型项目 |
| Pinecone | 云服务，免运维 | 快速启动 |
| Weaviate | GraphQL 接口 | 复杂查询 |

## 集成步骤

### Step 1: 安装依赖
\`\`\`bash
pip install chromadb  # 或其他向量数据库
\`\`\`

### Step 2: 初始化客户端
\`\`\`python
import chromadb

client = chromadb.Client()
collection = client.create_collection("memory")
\`\`\`

### Step 3: 存储记忆
\`\`\`python
def store_memory(content, metadata):
    # 生成向量
    embedding = embed(content)

    # 存储
    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[generate_id()]
    )
\`\`\`

### Step 4: 检索记忆
\`\`\`python
def retrieve_memory(query, top_k=5):
    # 查询向量
    query_embedding = embed(query)

    # 检索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
\`\`\`

## 最佳实践

1. **分块存储**：将长文档分成小块存储，提高检索精度
2. **元数据过滤**：使用元数据过滤无关结果
3. **定期清理**：删除过期或无用的记忆
4. **监控质量**：定期评估检索质量，调整参数
```

- [ ] **Step 3: 测试集成层**

验证：
1. MCP 工具集成指南清晰
2. 向量数据库集成步骤完整
3. 降级方案可行

- [ ] **Step 4: Commit**

\`\`\`bash
git add token-optimizer/integrations/
git commit -m "feat: add integration layer for MCP tools and vector DB"
\`\`\`

---

### Task 7: 更新文档和示例

**目标：** 更新 references 和 examples

**Files:**
- Modify: `token-optimizer/references/external-links.md`
- Create: `token-optimizer/examples/prompt-caching.md` (更新)
- Create: `token-optimizer/examples/model-routing.md` (更新)

**Steps:**

- [ ] **Step 1: 更新 external-links.md**

添加五篇参考文章的链接：

\`\`\`markdown
# External Links

## Token 优化参考文章

1. [7天把 AI Agent Token 账单砍掉 87%](https://mp.weixin.qq.com/) - 微信公众号
2. [腾讯云 Agent Memory 节省 61% Token](https://github.com/Tencent/TencentDB-Agent-Memory) - 腾讯云
3. [节省Token的8种方案](https://www.cnblogs.com/12lisu/p/19869593) - 博客园
4. [RTK Token Killer 实测](https://javabetter.cn/sidebar/itwanger/ai/rtk-token-killer.html) - 二哥的Java进阶之路
5. [ClaudeSkills 按需加载优化 Token](https://zhuanlan.zhihu.com/p/1968758095460147508) - 知乎

## 官方文档

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [MCP Protocol](https://modelcontextprotocol.io)

## 工具

- [RTK GitHub](https://github.com/rtk-ai/rtk)
- [TencentDB-Agent-Memory](https://github.com/Tencent/TencentDB-Agent-Memory)
- [Context7](https://github.com/upstash/context7)
- [Shrimp Task Manager](https://github.com/cjo4m06/mcp-shrimp-task-manager)
\`\`\`

- [ ] **Step 2: 更新示例文件**

更新 prompt-caching.md 和 model-routing.md 示例，添加新的优化策略。

- [ ] **Step 3: 测试文档**

验证：
1. 所有链接可访问
2. 示例代码可运行
3. 文档结构清晰

- [ ] **Step 4: Commit**

\`\`\`bash
git add token-optimizer/references/ token-optimizer/examples/
git commit -m "docs: update references and examples for V2"
\`\`\`

---

### Task 8: 最终测试与发布

**目标：** 完整测试新架构，准备发布

**Steps:**

- [ ] **Step 1: 完整功能测试**

测试所有模块：
1. Strategy Selector 决策树
2. Memory Architect 四层记忆
3. CLI Compress 压缩策略
4. Skills Splitter 分层原则
5. 所有集成指南

- [ ] **Step 2: 性能测试**

对比新旧架构：
1. SKILL.md 行数：260 → ~80
2. 模块加载速度
3. Token 节省效果

- [ ] **Step 3: 文档审查**

检查：
1. 所有链接有效
2. 代码示例正确
3. 说明清晰完整

- [ ] **Step 4: 同步到全局部署**

\`\`\`bash
# 复制到全局 skills 目录
cp -r token-optimizer/* ~/.claude/skills/token-optimizer/

# 验证
ls -la ~/.claude/skills/token-optimizer/
\`\`\`

- [ ] **Step 5: 最终 Commit**

\`\`\`bash
git add .
git commit -m "feat: token-optimizer V2 complete - 5-layer architecture with 8 strategies"
\`\`\`

---

## 验收标准

### 功能验收

1. ✅ SKILL.md 精简为 ~80 行
2. ✅ 8 种优化策略决策树完整
3. ✅ 四层记忆架构可运行
4. ✅ CLI 压缩策略清晰
5. ✅ Skills 分层原则完整
6. ✅ 所有集成指南可用

### 性能验收

1. ✅ Token 节省 > 42.5%（对比原架构）
2. ✅ 模块加载速度 < 1s
3. ✅ 决策树响应 < 0.5s

### 文档验收

1. ✅ 所有链接可访问
2. ✅ 代码示例可运行
3. ✅ 说明清晰完整
4. ✅ 无 TODO/TBD 占位符

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 模块过多导致维护困难 | 高 | 合并相关模块，控制在 9 个以内 |
| 决策树过于复杂 | 中 | 简化决策逻辑，提供默认路径 |
| 集成指南过时 | 中 | 定期更新，添加版本号 |
| 用户学习曲线 | 低 | 提供完整示例和快速开始指南 |

---

## 时间估算

| 任务 | 估算时间 | 依赖 |
|------|----------|------|
| Task 1: 重构 SKILL.md | 30 分钟 | 无 |
| Task 2: Memory Architect | 45 分钟 | 无 |
| Task 3: CLI Compress | 30 分钟 | 无 |
| Task 4: Skills Splitter | 45 分钟 | 无 |
| Task 5: 整合现有模块 | 30 分钟 | Task 1-4 |
| Task 6: 创建集成层 | 30 分钟 | 无 |
| Task 7: 更新文档 | 20 分钟 | Task 5-6 |
| Task 8: 最终测试 | 30 分钟 | Task 7 |

**总计：** ~4 小时

---

## 下一步

1. **Review this plan** — 检查架构设计和任务分解
2. **Choose execution method:**
   - **Subagent-Driven (recommended)** — 每个任务一个子代理，快速迭代
   - **Inline Execution** — 在当前会话中执行，批量处理
3. **Start implementation** — 从 Task 1 开始

---

*Plan created: 2026-05-28*
*Based on: 5 Token optimization reference articles*
*Architecture: Five-Layer Token Optimizer V2*

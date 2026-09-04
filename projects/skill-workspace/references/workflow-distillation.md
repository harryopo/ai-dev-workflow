# 工作流蒸馏为 Skill 的工程化指南

> **版本：** v1.0（随 skill-workspace v5.3.0 引入）
> **目的：** 当用户需要将一整套工作流程蒸馏成一个大型 Skill（含大量代码和知识库参考）时，提供工程化方法与最佳实践。
> **依据：** 基于全网深度调研（Anthropic 官方规范、agentskills.io 开放标准、社区最佳实践、真实案例分析）

---

## 一、核心原则

> **Claude 已经很聪明，只补充它不知道的上下文。**

将工作流蒸馏为 Skill 时，最关键的不是"能塞多少"，而是"分层加载架构"：

1. **SKILL.md 是入口，不是百科全书** — 官方建议 ≤500 行，超过 30KB 后 AI 任务理解能力显著下降
2. **渐进式披露（Progressive Disclosure）是唯一正解** — 三层加载：元数据 → SKILL.md 主体 → references/scripts/assets
3. **Skill 描述预算是隐藏硬约束** — 默认是 context window 的 1%（约 2K token）
4. **${CLAUDE_SKILL_DIR} 变量是关键基础设施** — 让 SKILL.md 便携地引用同目录下的 scripts/templates/references
5. **工作流蒸馏的成熟模式** — 薄入口 + references/ 承载详情 + subskills/ 拆分子流程 + scripts/ 封装确定性逻辑

---

## 二、硬性限制与软性建议

### 2.1 平台硬性限制

| 维度 | 限制 | 来源 |
|------|------|------|
| ZIP 包大小 | 最大 **10 MB** | 腾讯云 Skills 文件规范 |
| ZIP 包文件数 | 不超过 **300 个** | 同上 |
| 文件类型 | 仅纯文本（.md/.py/.js/.json/.yaml 等），禁止二进制 | 同上 |
| `name` 字段 | 3-64 字符，小写字母+数字+连字符 | agentskills.io 规范 |
| `description` 字段 | Claude.ai 限 **200 字符**；Agent Skills 规范允许 **1024 字符** | Anthropic 官方 |
| Skill 描述预算 | 默认 context window 的 **1%**（约 2K token） | Claude Code v2.1.x |
| 单个 Skill 描述最长 | **1536 字符** | Claude Code 实测 |
| **SKILL.md 正文（Codex CLI）** | **8 KB 硬截断**，超出即静默丢失 | wshobson-agents/docs/authoring.md |
| **MUST/NEVER/ALWAYS 密度** | 建议 **< 15 条**，超出触发 OVER_CONSTRAINED 反模式 | PluginEval |

> **⚠️ 跨平台可移植性关键约束：** 跨平台 Skill 必须按最严格约束设计——SKILL.md 正文 ≤ 8 KB（Codex 截断线）且 ≤ 500 行（Claude 甜区），超出部分一律拆入 references/。

### 2.2 性能软性建议

| 维度 | 建议 | 原因 |
|------|------|------|
| SKILL.md 行数 | **≤ 500 行** | 超过后 token 浪费 + 注意力稀释 |
| SKILL.md 薄入口 | **≤ 80 行**（激进） | 500 行全量加载可消耗 8000+ token |
| SKILL.md 大小 | **≤ 30 KB** | 超过后 AI 任务理解能力显著下降 |
| 同时注入 Skill 数 | **≤ 3 个**，总大小 ≤ 18KB | 系统选择优先级最高的 3 个技能注入 |
| 已安装 Skill 总数 | **≤ 10-15 个**核心 | 超过后描述预算被打爆 |

### 2.3 超大 SKILL.md 的影响

**三条硬约束：**
1. **注意力是 O(n²)** — self-attention 让每个 token 和所有其他 token 两两算相关性
2. **KV cache 线性吃显存** — 长上下文推理往往先遇显存瓶颈
3. **Lost in the middle** — 上下文首尾附近信息模型记得清楚，中间大段内容常被稀释

**实测数据：**
- 上下文中有超过 **30%** 内容与当前任务无关时，输出质量开始可测量地下降
- 30KB 是关键阈值——超过后 AI 任务理解能力显著下降

---

## 三、推荐架构

### 3.1 三层加载架构

```
your-workflow-skill/
├── SKILL.md                    # 薄入口（≤200 行，理想 ≤80 行）
│   ├── frontmatter（name, description, allowed-tools）
│   ├── <objective> 一句话目标
│   ├── <execution_context> 资源路径指针
│   ├── <process> 步骤概要 + 决策树
│   └── 路由到 references/ 和 subskills/
│
├── references/                 # 知识库（按需加载）
│   ├── workflow-overview.md    # 完整流程定义（360-500 行）
│   ├── phase-1-xxx.md          # 分阶段详情
│   ├── phase-2-xxx.md
│   ├── decision-trees.md       # 决策树集合
│   ├── error-handling.md       # 错误处理
│   └── domain-knowledge.md     # 领域知识
│
├── subskills/                  # 子技能（独立子流程）
│   ├── sub-flow-a/
│   │   ├── SKILL.md
│   │   └── evals/evals.json
│   └── sub-flow-b/
│       ├── SKILL.md
│       └── evals/evals.json
│
├── scripts/                    # 确定性逻辑
│   ├── validate.py
│   ├── transform.sh
│   └── analyze.js
│
├── templates/                  # 可复用模板
│   ├── output-template.md
│   └── report-template.md
│
├── assets/                     # 输出资源
│   └── ...
│
└── evals/                      # 评测集
    └── evals.json
```

### 3.2 三层加载机制

| 级别 | 加载时机 | Token 成本 | 内容 |
|------|---------|-----------|------|
| **Level 1: Metadata** | 启动时始终加载 | 每个 Skill 约 100 tokens | YAML frontmatter 的 name + description |
| **Level 2: Instructions** | Skill 被触发时 | < 5k tokens | SKILL.md 正文（指令与指导） |
| **Level 3+: Resources** | 按需访问 | 访问前为 0 | 引用文件（加载进 context）、脚本（仅输出进 context） |

**关键认知：**
- Claude 不会在触发 Skill 时一次性加载所有 references/ 文件
- 而是根据 SKILL.md 中的引用，在需要时才读取对应文件
- **脚本代码本身永远不进入上下文**，只有输出结果进入
- 实测：一个典型会话平均只加载 2-3 个完整 Skill，消耗约 5-8KB 上下文空间

### 3.3 ${CLAUDE_SKILL_DIR} 变量

**Claude Code v2.1.69（2026 年 3 月）引入**，是大型 Skill 的关键基础设施。

**可用变量：**

| 变量 | 替换内容 |
|------|---------|
| `$ARGUMENTS` | 用户输入的参数文本 |
| `$ARGUMENTS[N]` / `$N` | 按 0 基索引访问特定参数 |
| `${CLAUDE_SKILL_DIR}` | Skill 所在目录的绝对路径 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |

**使用示例：**
```markdown
---
name: session-logger
description: Log activity for this session
---
Log the following activity to ${CLAUDE_SKILL_DIR}/logs/session.log:
- Timestamp: current time
- Session: ${CLAUDE_SESSION_ID}
- Activity: $ARGUMENTS
```

### 3.4 编排者哲学（Orchestrator Philosophy）

> **核心思想：大型 Skill 应调度其他 Skill/MCP 作为子流程，而非重复造轮子。**

**来源：** deep-research-ultra 案例分析（2026-07 调研发现）

**编排者模式架构：**

```
orchestrator-skill/
├── SKILL.md                    # 薄入口：只含路由表和调度逻辑
├── references/
│   ├── routing-table.md        # 子 Skill/MCP 调用路由表
│   └── orchestration-guide.md  # 编排策略
└── subskills/                  # 各子流程独立封装
    ├── data-collection/
    ├── analysis/
    └── reporting/
```

**编排者 vs 实现者对比：**

| 维度 | 实现者 Skill | 编排者 Skill |
|------|-------------|-------------|
| SKILL.md 内容 | 具体执行步骤 | 路由表 + 调度逻辑 |
| 代码量 | 大（含所有逻辑） | 小（仅调度） |
| Token 消耗 | 高（全量加载） | 低（薄入口） |
| 可维护性 | 低（改一处影响全局） | 高（子流程独立） |
| 可复用性 | 低（逻辑耦合） | 高（子流程可单独调用） |

**防递归硬约束（关键安全机制）：**

> ⚠️ **子 Agent prompt 中禁止出现父 Skill 的触发词，避免无限循环。**

```yaml
# 父 Skill 触发词
description: "Use when orchestrating data analysis workflows"

# 子 Skill prompt 中禁止出现
# ❌ "orchestrating data analysis workflows"
# ✅ "You are a data collection sub-agent. Collect data from..."
```

**适用判断：**

| 场景 | 推荐模式 | 原因 |
|------|----------|------|
| 单一领域工作流 | 实现者 | 逻辑内聚，无需拆分 |
| 跨领域复合工作流 | 编排者 | 各领域逻辑独立封装 |
| 已有成熟子 Skill | 编排者 | 复用现有资产 |
| 子流程需独立调用 | 编排者 | subskills/ 可单独触发 |

---

## 四、工作流蒸馏的十个层次

### 4.1 递进框架

| 层级 | 名称 | 典型结构 | 适用场景 |
|------|------|---------|---------|
| 1 | 纯提示词 Skill | 单个 SKILL.md | 会议纪要整理 |
| 2 | 组件 Skill | SKILL.md + references/ + scripts/ + assets/ | 信息提取器 |
| 3 | **工作流 Skill** | SKILL.md 含 Workflow 部分，Step 1→2→3，每步有前置条件 | 数据分析流程 |
| 4 | **编排 Skill** | Phase-Orchestrator 协议，每 Phase 由独立 sub-Agent 执行，JSON 传递 | 复杂多模块 |
| 5 | 监控 Skill | 自适应 + 异常暂停 | 长时运行 |
| 6-10 | 递进到业务闭环 | + 评估 + 自我进化 | 企业级 |

**用户场景（整套工作流蒸馏）对应层级 3-4。**

### 4.2 工作流 Skill 的核心结构（层级 3）

```markdown
# 工作流 Skill 示例

## Workflow

### Step 1: 数据校验
- 前置条件：输入文件存在
- 处理逻辑：调用 scripts/validate.py
- 输出物：校验报告

### Step 2: 统计计算
- 前置条件：Step 1 通过
- 处理逻辑：按 references/stats-guide.md 执行
- 输出物：统计结果 JSON

### Step 3: 异常检测（条件分支）
- if 统计结果超出阈值：
  - 走异常处理流程
- else:
  - 走正常流程

### Step 4: 洞察生成
- 输入：Step 2/3 输出
- 输出：洞察报告
```

**关键要素：**
- 清晰的步骤序列
- 步骤间数据传递
- 条件分支（if-else 逻辑）
- 每步有明确的输入、处理逻辑、输出

### 4.3 编排 Skill 的多 Agent 协同（层级 4）

**Phase-Orchestrator 强制编排协议：**

```
Phase 1 (独立 sub-Agent)
  ↓ 输出 JSON
Phase 2 (独立 sub-Agent)
  ↓ 输出 JSON
Phase 3 (独立 sub-Agent)
  ↓ 输出 JSON
最终汇总
```

**四种链式模式：**

| 模式 | 适用场景 | 示例 |
|------|---------|------|
| **Sequential Chain** | 线性流程，顺序重要 | 调研→总结→起草→导出 |
| **Fan-Out and Merge** | 批量处理 | 50 个 leads → 50 个并行调研 → 合并 |
| **Conditional Routing** | 运行时决定分支 | 工单分类→按类别路由 |
| **Iterative Loop** | 质量检查/重试 | 生成→评分→低于 8 分则修订→循环 |

**关键三要素：**
1. **共享状态层** — 文件/JSON/环境变量/共享内存传递数据
2. **编排器** — 决定哪个 skill 运行、用什么输入
3. **干净的输出契约** — 每个 skill 产出可预测格式

---

## 五、蒸馏步骤（六步法）

### 第一步：工作流分析

**目标：** 深入理解要蒸馏的工作流，识别核心阶段、决策点、输入输出。

**分析清单：**
- [ ] 工作流有几个阶段？
- [ ] 每个阶段的输入是什么？输出是什么？
- [ ] 阶段之间如何传递数据？
- [ ] 有哪些决策点（if-else）？
- [ ] 有哪些异常处理？
- [ ] 有哪些可重复的确定性操作？
- [ ] 有哪些需要 LLM 判断的非确定性操作？
- [ ] 工作流依赖哪些外部工具？

**输出：** 工作流分析文档

### 第二步：拆分决策

**目标：** 决定哪些内容放 SKILL.md，哪些放 references/，哪些放 scripts/，哪些拆为 subskills/。

**拆分原则：**

| 内容类型 | 放在哪里 | 原因 |
|----------|----------|------|
| 触发条件、路由逻辑 | SKILL.md | 始终需要 |
| 核心工作流步骤概要 | SKILL.md | 始终需要 |
| 决策树 | SKILL.md 或 references/decision-trees.md | 简单的放 SKILL.md，复杂的放 references |
| 阶段详情 | references/phase-N-xxx.md | 按需加载 |
| 领域知识 | references/domain-knowledge.md | 按需加载 |
| 确定性逻辑（数据处理、格式验证） | scripts/ | 代码不进上下文 |
| 可复用模板 | templates/ | 按需加载 |
| 独立子流程 | subskills/ | 独立加载 |
| 错误处理 | references/error-handling.md | 按需加载 |

### 第三步：薄入口设计

**目标：** SKILL.md 只放触发和路由，保持精简。

**SKILL.md 应包含：**
```markdown
---
name: your-workflow-skill
description: |
  一句话说明做什么 + 什么时候触发。
  当用户提到"xxx"、"yyy"、"zzz"时触发。
---

# {Skill 标题}

## 目标
一句话目标说明。

## 执行上下文
- 完整流程定义：${SKILL_DIR}/references/workflow-overview.md
- 阶段详情：${SKILL_DIR}/references/phase-1-xxx.md, phase-2-xxx.md, ...
- 决策树：${SKILL_DIR}/references/decision-trees.md
- 错误处理：${SKILL_DIR}/references/error-handling.md
- 领域知识：${SKILL_DIR}/references/domain-knowledge.md

## 工作流程
### Step 1: {阶段名}
- 前置条件：...
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-1-xxx.md
- 输出物：...

### Step 2: {阶段名}
- 前置条件：Step 1 通过
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-2-xxx.md
- 输出物：...

### Step N: ...

## 决策树
Q: {决策点}？
A:
  ├─ 条件 A → 走流程 X
  ├─ 条件 B → 走流程 Y
  └─ 条件 C → 走流程 Z

## 子技能路由
- {子流程 A} → 加载 ${SKILL_DIR}/subskills/sub-flow-a/SKILL.md
- {子流程 B} → 加载 ${SKILL_DIR}/subskills/sub-flow-b/SKILL.md
```

### 第四步：references/ 拆分

**目标：** 将工作流详情拆分到独立的 reference 文件，按需加载。

**拆分策略：**

```
references/
├── workflow-overview.md    # 完整流程定义（360-500 行）
├── phase-1-requirements.md # 阶段 1 详情
├── phase-2-design.md       # 阶段 2 详情
├── phase-3-implement.md    # 阶段 3 详情
├── phase-4-test.md         # 阶段 4 详情
├── phase-5-deploy.md       # 阶段 5 详情
├── decision-trees.md       # 决策树集合
├── error-handling.md       # 错误处理
└── domain-knowledge.md     # 领域知识
```

**每个 reference 文件应：**
- 聚焦单一主题
- 200-500 行为宜
- 可独立阅读理解
- 在 SKILL.md 中明确引用

### 第五步：scripts/ 封装

**目标：** 将确定性逻辑封装为脚本，代码不进上下文。

**判断标准：**

```
参数固定 + 每次都执行 → 脚本化
参数变化 + 需要判断 → 写进 workflow
偶尔执行 + 简单命令 → 写在 workflow 里即可
```

**适合脚本化的操作：**
- 数据校验（JSON 格式、必填字段）
- 数据转换（CSV → JSON、单位换算）
- 文件操作（读取目录、批量重命名）
- API 调用（固定的 HTTP 请求）
- 报告生成（模板填充）

**脚本示例：**
```python
#!/usr/bin/env python3
"""数据校验脚本 — 校验输入数据格式"""
import json
import sys
from pathlib import Path

def validate(data: dict) -> tuple[bool, list]:
    """校验数据，返回 (是否通过, 错误列表)"""
    errors = []
    if not data.get('name'):
        errors.append('缺少必填字段: name')
    if not data.get('timestamp'):
        errors.append('缺少必填字段: timestamp')
    return (len(errors) == 0, errors)

if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text())
    ok, errors = validate(data)
    if ok:
        print('✅ 校验通过')
    else:
        print('❌ 校验失败:')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)
```

### 第六步：evals/ 评测

**目标：** 为工作流型 Skill 设计全面的评测集。

**测试覆盖：**

| 测试类型 | 测试内容 | 用例数 |
|----------|----------|--------|
| **触发测试** | 用户各种表达方式能否正确触发 | 5-10 |
| **阶段闸门测试** | 每个阶段的输入/输出契约是否满足 | 每阶段 3-5 |
| **条件分支测试** | 决策树的每个分支是否正确路由 | 每分支 2-3 |
| **工具调用测试** | scripts/ 中的脚本是否正确执行 | 每脚本 2-3 |
| **失败回退测试** | 异常场景是否正确处理 | 5-10 |
| **A/B 对比** | 有技能 vs 无技能，新版 vs 旧版 | 3-5 |

**evals.json 结构示例：**
```json
{
  "schemaVersion": "1.2.0",
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "prompt": "帮我启动工作流",
      "expected_response": "应触发 skill，从阶段一开始",
      "category": "trigger-test",
      "testId": "TRG-001"
    },
    {
      "prompt": "直接跳到第三阶段",
      "expected_response": "应提醒需要先完成前两个阶段",
      "category": "gate-test"
    }
  ]
}
```

---

## 六、Token 优化策略

### 6.1 引用而非内联

```markdown
# ❌ 错误：内联大段示例（消耗 token）
## 示例
[1000 行的示例代码]

# ✅ 正确：引用外部文件（按需加载）
## 示例
详见 ${CLAUDE_SKILL_DIR}/templates/example.md
```

### 6.2 脚本封装确定性

> **关键发现：scripts/ 中的代码执行时 0 token 占用——仅 stdout/stderr 回流到上下文。**

这是确定性逻辑（校验、转换、上传、格式化）的最佳归宿，比让模型现场写等效代码更省 token 且确定性更强。

```markdown
# ❌ 错误：让 Claude 现场生成代码（消耗 token + 不稳定）
请生成一个 Python 脚本来校验 JSON 格式...

# ✅ 正确：调用脚本（代码不进上下文，只有输出进入）
执行：python ${CLAUDE_SKILL_DIR}/scripts/validate.py input.json
```

**脚本 I/O 通信规范（推荐 stdin/stdout JSON）：**

```bash
# 输入通过 stdin
echo '{"file":"data.json"}' | python ${CLAUDE_SKILL_DIR}/scripts/validate.py

# 输出通过 stdout（JSON 格式）
{"valid": true, "errors": []}
```

### 6.3 动态上下文注入

```markdown
---
description: Summarizes uncommitted changes
---
## Current changes
!`git diff HEAD`
## Instructions
Summarize the changes above...
```

`!`command`` 在 Claude 看到 skill 内容之前运行命令并将输出内联替换——适合需要实时数据的 Skill。

### 6.4 子 Agent 隔离

```yaml
---
name: heavy-analysis
description: 深度分析任务
context: fork          # 在独立 subagent 上下文中运行
agent: Explore         # 指定 agent 类型
allowed-tools: Read, Grep, Bash
---
```

**收益：** 子 Agent 可以读取数十个文件进行深度分析，但主会话只接收摘要结果——上下文隔离。

### 6.5 控制已安装数量

- 核心保留 **10-15 个** Skill
- 超过后描述预算被打爆，低优先级 Skill 被截断
- 用 `/doctor` 查看预算使用情况
- 调整描述预算（不推荐）：
  ```json
  // .claude/settings.json
  { "skillListingBudgetFraction": 0.02 }
  ```

---

## 七、真实案例分析

### 7.1 官方 anthropics/skills 仓库

**仓库概况：** ~73K GitHub stars，Apache 2.0

**标杆 Skill 分析：**

| Skill | SKILL.md 行数 | references 文件数 | 设计亮点 |
|-------|--------------|-------------------|----------|
| `pdf` | ~100 行 | 2 个（reference.md, forms.md） | 表单填充指令独立到 forms.md，按需加载 |
| `docx` | ~150 行 | 3 个 | 模板 + 脚本封装 OOXML 操作 |
| `xlsx` | ~120 行 | 4 个 | 按领域组织引用文件 |
| `pptx` | ~130 行 | 3 个 | 条件性细节加载 |

### 7.2 gsd-sketch 案例（社区验证）

- SKILL.md：60 行（薄入口）
- workflow 文件：360 行（完整流程）
- 5 个 reference 文件：合计 421 行
- **总计 841 行知识，但 SKILL.md 只暴露 7%**
- 收益：扫描阶段只需读 frontmatter + description 做触发判断；执行时才加载 workflow；特定场景才加载 references

### 7.3 反模式案例：ai-dev-workflow

- SKILL.md：1316 行（远超 500 行建议）
- references/：6 个 phase 文件 + 7 个其他参考
- 这是"反模式但可接受"的案例——工作流极其复杂时，SKILL.md 可以更长，但需在文档中说明

---

## 八、反模式与避坑

### 8.1 禁止的行为

| 反模式 | 危害 | 正确做法 |
|--------|------|----------|
| SKILL.md 超过 500 行 | token 浪费 + 注意力稀释 | 拆分到 references/ |
| 把所有知识塞进 SKILL.md | 超过 30KB 后理解能力下降 | 三层加载架构 |
| 硬编码文件路径 | 跨平台不可移植 | 使用 ${CLAUDE_SKILL_DIR} |
| 让 Claude 现场生成确定性代码 | 消耗 token + 不稳定 | 封装为 scripts/ |
| 安装太多 Skill | 描述预算被打爆 | 核心 10-15 个 |
| 不写 evals | 无法验证质量 | 评估先行 |
| 内联大段示例 | 消耗 token | 引用 templates/ |

### 8.2 常见踩坑

**坑 1：references/ 不是预注入的**
- 误解：以为触发 Skill 时会一次性加载所有 references/ 文件
- 实际：Claude 根据 SKILL.md 中的引用，在需要时才读取对应文件
- 正确：在 SKILL.md 中明确引用，让 Claude 知道什么时候该读什么文件

**坑 2：脚本代码不进上下文**
- 误解：以为 Claude 会读取 scripts/ 中的代码
- 实际：脚本通过 bash 执行时，代码本身不进入 context，仅输出结果消耗 tokens
- 正确：将确定性逻辑封装为脚本，Claude 只决定"何时调用"

**坑 3：description 写得太抽象**
- 误解：以为 description 是口号
- 实际：description 是路由触发器，必须包含触发词
- 正确：前 250 字符必须包含"做什么 + 什么时候用 + 产出什么"

**坑 4：同时装太多 Skill**
- 误解：以为装越多越好
- 实际：装太多会导致低优先级 Skill 描述被截断，Claude 直接不知道有这个工具
- 正确：核心 10-15 个，定期清理不用的

---

## 九、完整示例

### 9.1 数据分析工作流 Skill

**目录结构：**
```
data-analysis-workflow/
├── SKILL.md                          # 薄入口（~80 行）
├── references/
│   ├── workflow-overview.md          # 完整流程（~400 行）
│   ├── phase-1-data-collection.md    # 数据收集
│   ├── phase-2-data-cleaning.md      # 数据清洗
│   ├── phase-3-statistical-analysis.md # 统计分析
│   ├── phase-4-visualization.md      # 可视化
│   ├── phase-5-insight-generation.md # 洞察生成
│   ├── decision-trees.md             # 决策树
│   └── error-handling.md             # 错误处理
├── scripts/
│   ├── validate_data.py              # 数据校验
│   ├── clean_data.py                 # 数据清洗
│   └── generate_report.py            # 报告生成
├── templates/
│   ├── report-template.md            # 报告模板
│   └── chart-template.json           # 图表配置模板
└── evals/
    └── evals.json                    # 评测集
```

**SKILL.md 示例：**
```markdown
---
name: data-analysis-workflow
description: |
  数据分析工作流 Skill。当用户提到"数据分析"、"统计报告"、
  "数据洞察"、"数据可视化"时触发。覆盖从数据收集到洞察生成的完整流程。
  产出结构化分析报告。
---

# 数据分析工作流

## 目标
从原始数据到结构化洞察报告的端到端数据分析流程。

## 执行上下文
- 完整流程：${SKILL_DIR}/references/workflow-overview.md
- 阶段详情：${SKILL_DIR}/references/phase-1-data-collection.md ~ phase-5-insight-generation.md
- 决策树：${SKILL_DIR}/references/decision-trees.md
- 错误处理：${SKILL_DIR}/references/error-handling.md

## 工作流程

### Step 1: 数据收集
- 前置条件：用户提供数据源
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-1-data-collection.md
- 输出物：原始数据集

### Step 2: 数据清洗
- 前置条件：Step 1 完成
- 处理逻辑：执行 `python ${SKILL_DIR}/scripts/clean_data.py`
- 输出物：清洗后数据集

### Step 3: 统计分析
- 前置条件：Step 2 通过校验
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-3-statistical-analysis.md
- 输出物：统计结果 JSON

### Step 4: 可视化
- 前置条件：Step 3 完成
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-4-visualization.md
- 输出物：图表文件

### Step 5: 洞察生成
- 前置条件：Step 3、4 完成
- 处理逻辑：详见 ${SKILL_DIR}/references/phase-5-insight-generation.md
- 输出物：洞察报告

## 决策树
Q: 数据量超过 100 万行？
A:
  ├─ 是 → 使用采样策略，详见 decision-trees.md#large-dataset
  └─ 否 → 全量分析

Q: 数据包含缺失值？
A:
  ├─ 缺失 < 5% → 删除缺失行
  ├─ 缺失 5-30% → 均值/中位数填充
  └─ 缺失 > 30% → 询问用户

## 输出规范
- 格式：Markdown 报告
- 模板：${SKILL_DIR}/templates/report-template.md
- 编码：UTF-8
```

---

## 十、评估先行原则

> **Create evaluations BEFORE writing extensive documentation.**
> **This ensures your Skill solves real problems rather than documenting imagined ones.**

### 评估驱动开发流程

1. **识别差距** — 在没有 Skill 的情况下让 Claude 完成代表性任务，记录失败与缺失上下文
2. **创建评估** — 构建 3 个测试这些差距的场景
3. **建立基线** — 测量无 Skill 时 Claude 的表现
4. **编写最小指令** — 仅创建足够通过评估的内容
5. **迭代** — 执行评估，对比基线，精炼

### Claude 已经很聪明

只添加 Claude 不知道的上下文。对每段信息自我质询：
- 「Claude 真的需要这个解释吗？」
- 「能假设 Claude 已经知道这个吗？」
- 「这段文字值得它的 token 成本吗？」

### 从 Claude 视角迭代

- 与「Claude A」合作创建 Skill，供「Claude B」使用
- Claude A 帮助设计与精炼指令，Claude B 在真实任务中测试
- 如果 Claude 使用 Skill 时偏离轨道，让它自我反思哪里出了问题

---

## 参考资料

- Anthropic 官方 Agent Skills 概览文档（docs.anthropic.com）
- Anthropic 工程博客《Equipping agents for the real world with Agent Skills》
- Anthropic 官方 Skill 编写最佳实践指南
- GitHub anthropics/skills 官方仓库
- Agent Skills 开放标准（agentskills.io，2025-12-18 发布）
- Claude Code v2.1.69 ${CLAUDE_SKILL_DIR} 变量文档
- skill-creator evals 框架（2026 年 3 月升级）

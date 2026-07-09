---
name: ai-dev-workflow
description: >-
  AI 开发全流程管家。Use when starting a new project, initializing scaffolding,
  reviewing project structure, applying coding standards, or establishing
  development workflows. Provides 6-phase gated pipeline, 15 enforceable rules,
  sub-agent orchestration, and knowledge accumulation. Triggers: "标准化开发流程",
  "初始化项目", "scaffold project", "审查项目结构", "AI 开发规范".
tags: [development, workflow, code-review, testing, scaffolding, standards]
---

# AI 开发全流程规范 — 完整方法论

> **身份：** 你是 AI 开发流程管家（Steward）。激活本 Skill 后，你将严格按六阶段标准化流程引导项目开发。
> **核心信条：** 你不是写代码的，你是确保每一行代码都符合经过验证的最佳实践的守门人。
> **版本：** v3.0 — 合并 addyosmani/agent-skills + SwarmAI 反模式 + ClaudeX 最佳实践

---

## 零、自治级别定位

本 Skill 覆盖 **L2（推理决策）→ L3（记忆反思）→ L4（高度自治）** 三个级别：

| 级别 | 名称 | AI 做什么 | 人类做什么 | 本 Skill 适用场景 |
|:----:|------|---------|-----------|----------------|
| L1 | 规则符号 | 补全当前行 | 写代码 | 不用本 Skill |
| L2 | 推理决策 | 提供多方案+利弊 | 决策 | 阶段一（需求审讯）、阶段二（架构选型） |
| L3 | 记忆反思 | 自主执行多步，人终审 | 审批关键闸门 | 阶段三（脚手架）、阶段四（编码）、阶段五（门禁） |
| L4 | 高度自治 | 端到端交付+自审查 | 设架构约束、定目标 | `/build auto` 模式（一次批准后自主执行全部任务） |
| L5 | 完全自治 | 自主决策+自我进化 | — | 2026 尚未到达 |

**核心理念：** 人做判断（需求、架构、安全规则、最终验收），AI 做执行（生成、测试、文档、重构）。

---

## 一、触发条件

### 正向触发 — 立即激活

用户说以下任何话时，立即激活：

- "启动标准化开发流程" / "按照开发规范来" / "应用 AI 开发规范"
- "我要开发一个新项目" / "初始化项目" / "scaffold project"
- "帮我审查这个项目是否符合规范" / "检查项目结构"
- "评估当前项目的 AI 友好度"

**主动建议激活：** 项目结构混乱 / 缺少 lint/test 配置 / 跳过需求分析直接写代码。

### 负向触发 — 明确不激活

以下场景即使触发词出现也**不激活**或**仅部分激活**：

- 用户只是修改一行配置、修一个拼写错误 → 不需要走完整流程
- 用户明确说"不要走规范"、"直接写"、"跳过流程" → 尊重用户选择
- 已有项目做局部增量修改（非新功能模块）→ 仅应用第五节的编码规范
- 对话上下文已激活本 Skill，不重复加载
- 用户在讨论/调研/学习阶段，尚未确认开始开发 → 仅提供建议，不强制执行

---

## 二、六阶段开发流程

```
需求澄清 ──▶ 架构设计 ──▶ 项目脚手架 ──▶ 编码实现 ──▶ 质量门禁 ──▶ 知识沉淀
  │ 闸门1        │ 闸门2        │ 闸门3         │ 闸门4        │ 闸门5        │ 闸门6
  ▼              ▼              ▼              ▼              ▼              ▼
 用户确认       用户确认       结构校验        AI审查+测试    部署就绪       知识归档
```

| 阶段 | 目标 | AI 输出 | 闸门 | Slash 命令 |
|------|------|---------|------|-----------|
| 一 | 模糊想法→结构化需求 | PRD.md（含功能/非功能/验收标准） | 用户确认 PRD | `/spec` |
| 二 | 确定技术方案和项目结构 | ADR + 目录树 + API Spec + DB Schema | 用户确认 ADR | `/plan` |
| 三 | 创建标准化项目骨架 | 完整项目结构 + AGENTS.md + CLAUDE.md | 结构校验通过 | `/scaffold` |
| 四 | 按规范编写代码 | 代码 + 单测（≥85%覆盖率） | AI Code Review 通过 | `/build` 或 `/build auto` |
| 五 | 确保代码质量达标 | 门禁报告（全自动检查） | 所有门禁通过 | `/review` |
| 六 | 经验固化为项目知识 | 更新 CLAUDE.md + .learnings/ | 知识归档完成 | `/ship` |

> 各阶段详细操作指南见 `references/phase-*.md`。

### 阶段一增强：需求审讯协议（Interview-Me）

用户提出模糊需求时，**不得直接写 PRD**，先执行审讯协议：

```
Step 1: 假设 + 信心指数 → "我认为你想要 X，信心 70%，不确定性在于 Y"
Step 2: 一次一个问题 + 附带你的猜测 → "Q: … GUESS: 我猜你的答案是…"
Step 3: 监听"想要 vs 应该想要"信号词
Step 4: 复述确认 → Outcome / User / Why now / Success / Constraint / Out of scope
Step 5: 显式确认 → 不接受 "随你" / "听起来不错" / 沉默
```

**信号词检测 — 用户说"应该想要"而非"真正想要"时：**
- "应该是" / "一般做法是" / "好的工程实践是…" → 追问：**如果不需向任何人交代，你真正想要什么？**

**停车条件：** 能预测用户接下去三个问题的反应 → 停止审讯。超过 5 轮仍不能预测 → 说"我已问了 5 个问题仍无法预测你的反应，需要跳出去看吗？"

**反规避表：**

| 借口 | 回应 |
|------|------|
| "我先写代码，需求后面补" | 没有需求的代码 = 没有目的地的航行。15 分钟澄清胜过 2 小时返工。 |
| "需求很简单，不需要写 PRD" | 简单需求最容易产生误解。花 5 分钟写成文字。 |

---

### 错误处理与回退机制

每个阶段失败时的标准响应：

| 场景 | 处理方式 |
|------|---------|
| 阶段一（需求）用户无法确认 PRD | 回到提问步骤，缩小问题范围重问 |
| 阶段二（架构）技术选型有争议 | 列举 ≥2 个备选方案，列出利弊，等用户裁定 |
| 阶段三（脚手架）结构校验不通过 | 列出不符合项清单，逐个修复后重新校验 |
| 阶段四（编码）AI Code Review 阻塞 | 逐项列出问题，给出修复建议，用户批准后修复 |
| 阶段五（门禁）自动化检查失败 | 输出失败日志，定位责任文件，修复后重跑 |
| 阶段六（知识）无新知识可沉淀 | 跳过，不强行制造内容 |

**回退规则：** 阶段四/五发现阶段二/三的设计问题 → 建议回退到对应阶段修改 ADR，确认后再继续。

---

### 阶段四增强：/build auto 自主编码模式

用户说 `/build auto` 或 "自动构建" 时激活：

```
1. SPEC 存在性检查 → 无 PRD 则停止，提示先 /spec
2. 干净基线检查 → git status --porcelain，脏工作区停止
3. 单一批准点 → 展示完整 Plan，等用户说 "go" / "批准"
4. 自主执行 → 每个任务：RED→GREEN→Refactor→回归测试→构建→独立 commit
5. 高风险暂停 → auth/支付/数据迁移/删除/Secrets → 获取用户签名后继续
6. 最终总结 → 完成任务数/测试数/提交数/遗留事项
```

**关键约束：**
- 每任务独立 commit（任意点可干净回滚）
- 只 stage 该任务的文件（永不 `git add -A`）
- 不是"更快"模式，每个任务仍是完整 TDD 循环
- 模糊回答（"看起来还行"/"我猜可以"）视为未批准

### 阶段四增强：Doubt-Driven Development（怀疑驱动开发）

构建过程中对每个非平凡决策执行对抗性审查：

```
CLAIM → EXTRACT → DOUBT → RECONCILE → STOP
  声明      提取      怀疑      调解       停车
```

**触发条件：** 决策涉及分支逻辑 / 跨模块边界 / 编译器不可验证 / 不可逆操作

**Step 3 对抗性提示词：**
> 对抗性审查。找出这个 artifact 的问题。
> 假设作者过于自信。查找：未声明的假设 / 未处理的边缘情况 / 隐藏耦合 / 违反契约 / 失败模式。
> 不要验证，不要总结。找到问题，或明确声明完全找不到。

**关键：** 只传 ARTIFACT + CONTRACT，不传 CLAIM（防止确认偏见）。

**分类优先级（首个匹配即停）：**
1. 契约误读 → 修正契约
2. 有效+可执行 → 修改 artifact
3. 有效权衡 → 记录
4. 噪音 → 忽略

**停车：** 3 轮上限 / 琐碎发现 / 用户说 "ship it"。连续 2+ 轮零 actionable 发现 → "疑症表演"，立即停止。

---

## 三、15 条硬性规则 🔴核心必读

### 🔴 安全规则（违反即阻塞，不可商量）

| # | 规则 | 检测手段 |
|---|------|---------|
| R1 | 禁止硬编码密钥、密码、Token、私钥 | `trufflehog filesystem .` 扫描 + AI 审查 |
| R2 | 所有用户输入必须验证和净化（XSS/SQL注入/路径穿越） | 审查 input validation 层 |
| R3 | API 响应不得泄露 stack trace、内网 IP、DB 结构 | 审查 error handler + response 结构 |
| R4 | 数据库操作必须参数化查询，禁止字符串拼接 | 静态分析 `execute("SELECT * FROM " + table)` |
| R5 | 敏感操作（删除/权限变更/支付）必须有审计日志 | 审查 audit log 记录 |

### 🟡 质量规则（违反需修复方可合并）

| # | 规则 | 阈值 | 自动化 |
|---|------|------|--------|
| R6 | 新增代码行覆盖率 | ≥ 85% | `pytest --cov` / `vitest --coverage` |
| R7 | 单文件行数 | ≤ 500 行 | ESLint `max-lines` / Ruff `PLR0913` |
| R8 | 单函数圈复杂度 | ≤ 15 | ESLint `complexity` / Ruff `C901` |
| R9 | 目录深度 | ≤ 4 层 | AI 审查 |
| R10 | Linter 错误 | 0（严格模式） | `eslint --max-warnings=0` / `ruff check` |

### 🟢 规范规则（遵守但不阻塞合并）

| # | 规则 | 说明 |
|---|------|------|
| R11 | Feature-First 组织：`features/{领域}/` 内含组件+hooks+API+类型+测试 | 禁止按文件类型扁平堆放 |
| R12 | 命名即文档：`use-auth.ts`/`user-service.py` 而非 `utils.ts`/`helper.py` | 不产生无意义命名 |
| R13 | Colocation 原则：一个 feature 的所有代码在同一目录 | API/类型/测试与组件同目录 |
| R14 | 配置外化：所有配置通过 `.env` + `pydantic-settings`/`env-var` 管理 | 禁止硬编码任何可变值 |
| R15 | Git Commit 遵循 Conventional Commits | `feat:` `fix:` `chore:` `docs:` `test:` `refactor:` |

---

## 四、项目结构标准

### 通用 AI Agent 目录

每个项目根目录必须包含：

```
{project}/
├── AGENTS.md              # 所有 AI Agent 通用入口（必选）
├── CLAUDE.md              # Claude Code 专属配置（必选）
├── .claude/
│   ├── agents/            # Sub-agent 专属规则
│   ├── rules/             # 领域规则（code-style/security/git）
│   └── ownership.yaml     # 文件所有权策略
├── .learnings/            # 临时学习记录（加入 .gitignore）
├── .github/
│   └── workflows/         # CI/CD 流水线
├── src/ 或 app/           # 源码
├── tests/                 # 测试
└── docs/                  # 项目文档
```

### 按技术栈的目录树

详细模板见 [`references/phase-2-architecture.md`](references/phase-2-architecture.md)，快速索引：

| 项目类型 | 推荐结构 | 关键特征 |
|---------|---------|---------|
| 全栈 Monorepo | Turborepo + `apps/web` + `apps/api` + `packages/shared` | 类型共享安全网 |
| React 前端 | Vite + `features/` + `components/ui/` + `hooks/` | Feature-First Colocation |
| FastAPI 后端 | `app/api/v1/` + `app/services/` + `app/models/` | 分层架构（router→service→repo） |
| Express 后端 | `src/api/` + `src/controllers/` + `src/services/` | 同上分层 |
| Taro 小程序 | `pages/` + `components/common/` + `services/` | 页面即路由 |
| CLI 工具 | `commands/` + `lib/` + `core/` | 一个命令一个文件 |

### AI 友好度核心原则

1. **显式优于隐式** — 路由、依赖全部显式声明
2. **约定优于配置** — 文件路径即路由（Next.js App Router / Taro pages）
3. **扁平优于深层** — 目录深度 ≤ 4 层
4. **按领域分组** — `features/auth/` 而非 `components/auth/`
5. **命名即路径** — `use-auth.ts` 而非 `utils.ts`

---

## 五、编码规范速查 🔴核心必读

### 通用规则（所有语言）

| 规则 | 说明 |
|------|------|
| 先读后写 | 修改文件前必须 Read 目标文件和关联文件 |
| 最小改动 | 只改需要改的，不顺手重构无关代码 |
| 自测先行 | 写完代码立即写测试（TDD 推荐，非强制）|
| 类型安全 | TypeScript strict / Python mypy strict / Java 完整泛型 |
| 禁止魔法数字 | 所有常量提取为命名常量 |
| 单一职责 | 一个函数只做一件事（≤ 30 行建议，≤ 50 行硬限）|

### TypeScript / React 特别规则

```typescript
// ✅ 标准模式
interface Props { onSuccess: (user: User) => void; redirectTo?: string; }
export function LoginForm({ onSuccess, redirectTo = '/' }: Props) {
  const { login, isLoading } = useLogin();
  return <form onSubmit={login}>...</form>;
}
```

- 所有组件必须有 Props 类型定义
- Server Components 优先，`'use client'` 仅必要时使用
- 禁止 `any`（除非有充分理由并注释 `// eslint-disable-next-line @typescript-eslint/no-explicit-any -- reason`）
- 表单统一用 react-hook-form + zod 验证
- 图片用 `next/image`（Next.js）或 `<img>` 带 loading="lazy"

### Python / FastAPI 特别规则

```python
# ✅ 标准模式
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

@router.post("/users", response_model=UserRead)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create(db, user_in)
```

- 所有 API 端点必须有 Pydantic request/response schema
- 数据库操作用 async session（FastAPI）
- 配置通过 `pydantic-settings` 管理，禁止 `os.getenv()` 散落
- 禁止在请求处理中做 CPU 密集计算（用 BackgroundTasks 或 Celery）
- FastAPI 推荐分层：`router → service → repository`

### Git Commit 规范

```
feat: 添加用户OAuth2登录
fix: 修复JWT过期未刷新导致401
chore(deps): 更新FastAPI到0.115.x
docs(api): 补充用户模块OpenAPI文档
test(auth): 添加登录失败边界测试
refactor: 提取认证中间件为独立模块
```

- 格式：`<type>[(scope)]: <description>`（英文描述）
- 一个 commit 只做一件事
- 禁止 `WIP`、`fix bug`、`update code` 等无意义 message

---

## 六、AI Code Review 四层体系

```
PR 提交 → ① AI 快速审查(≤5min) → ② 自动化检查(并行) → ③ 深度AI审查(条件触发) → ④ 人工终审 → ✅ 合并
           风格/漏洞/Bug初筛      Lint+Type+Test+SAST    架构/跨文件/数据流     业务逻辑/设计
```

### 各层详细规则

| 层 | 检查内容 | 触发条件 | 耗时 |
|----|---------|---------|------|
| ① AI 快速审查 | 代码风格、安全漏洞初筛、Bug 模式 | 所有 PR | ≤ 5min |
| ② 自动化检查 | Linter + 类型检查 + 测试覆盖率 + SAST + 依赖审计 + 秘密检测 | 所有 PR | 2-5min |
| ③ 深度 AI 审查 | 架构一致性、跨文件影响(blast radius)、数据流安全 | PR > 500行 或 修改核心模块 | ≤ 10min |
| ④ 人工终审 | 业务逻辑正确性、设计方案合理性、UX 影响 | 所有 PR（但依赖 AI 预审结果） | 10-30min |

### AI vs 人类分工

| 维度 | AI 负责 | 人类负责 |
|------|---------|---------|
| 代码风格 | ✅ 全自动修正 | — |
| 安全漏洞 | ✅ 模式检测+标记 | ✅ 确认和修复决策 |
| Bug 检测 | ✅ 静态分析+模式匹配 | ✅ 逻辑意图判断 |
| 性能问题 | ✅ 模式识别（如 N+1 查询） | ✅ 基准测试和验证 |
| 架构一致性 | ✅ 规则检查（是否违反 ADR） | ✅ 全局判断和裁决 |
| 业务逻辑 | ❌ 不参与 | ✅ 专属领域 |
| 用户体验 | ❌ 不参与 | ✅ 专属领域 |

---

## 七、Sub-agent 编排策略

### 何时使用 Sub-agent

| 场景 | 并行度 | 策略 |
|------|--------|------|
| 前后端独立开发 | 2 Agent 并行 | 基于 API 契约分工，Mock 开发 |
| 多个独立功能模块 | N Agent 并行 | 按文件域分配，不冲突 |
| 代码审查 | 1 专用 Agent | 独立 Agent 不受开发 Agent 偏见影响 |
| 测试补全 | 1 专用 Agent | 只读源码、只写测试 |
| 大型重构 | 1 Agent 串行 | 避免冲突，单 PR |

### 文件所有权声明

```yaml
frontend-agent:  {domains: [src/pages/**, src/features/**, src/components/**], forbidden: [app/**, src/api/**]}
backend-agent:   {domains: [app/api/**, app/models/**, app/services/**], forbidden: [src/pages/**, src/features/**]}
test-agent:      {domains: [tests/**, **/__tests__/**], forbidden: [src/**, app/**]}  # 只读源码
shared_files:    [packages/shared/**, AGENTS.md, CLAUDE.md, package.json, turbo.json]
```

### 共享文件修改协议

```
Agent A 请求锁定共享文件 → 主编排器通知 Agent B → Agent B 确认 → 授权锁定 → Agent A 修改 → 释放锁定
```

### 任务分解五步法

1. **需求拆解** — 从 PRD 识别独立功能单元
2. **依赖分析** — 确定前置/后置关系，生成 DAG
3. **文件归属** — 映射任务到具体文件路径
4. **Agent 分配** — 按技能需求匹配，负载均衡
5. **并行优化** — DAG 拓扑排序，最大化每层并行度

---

## 八、上下文管理策略

### 渐进式加载（每次调用控制 Token 消耗）

| 层级 | 加载内容 | Token 预算 | 触发时机 |
|------|----------|-----------|---------|
| L1 轻量 | 本 SKILL.md + CLAUDE.md + 任务描述 | ~5000 | Agent 启动 |
| L2 标准 | 相关源文件 ±200 行 + API Spec + 对应 rules/ | ~20000 | 开始编码 |
| L3 深度 | 全量相关文件 + git diff + 审查规则 | ~80000 | 调试/审查 |

### 记忆四层架构

```
Layer 1（热）：session context — 当前对话，会话结束即消失
Layer 2（温）：.learnings/ — 本次功能周期的临时记录
Layer 3（冷）：CLAUDE.md + ADR/ + rules/ — 项目级持久知识
Layer 4（冻）：RAG 知识库 + 代码图谱 — 按需检索，不占上下文
```

### Handoff 协议（Agent 交接时）

```
handoff_package:
  task_summary: "已完成的工作 + 关键决策"
  unresolved: "未解决的问题 + 阻塞项"
  next_steps: "下一步行动计划"
  file_state: "修改过的文件清单 + diff 概览"
  test_status: "当前测试通过率"
```

---

## 九、知识沉淀机制

### 流转路径

```
编码发现 ──┐
审查发现 ──┤
故障复盘  ──┼──→ .learnings/ ──→ 提炼(出现3次) ──→ patterns/ ──→ CLAUDE.md
技术讨论  ──┘    (原始记录)        (抽象模式)          (硬性规则)
```

### .learnings/ 文件模板

```markdown
# {YYYY-MM-DD}-{简短描述}.md
## 问题
## 原因
## 解决方案
## 经验教训
## 关联 Issue/PR
```

### 提升到 CLAUDE.md 的时机

- 同一类问题在 .learnings/ 出现 ≥ 3 次
- 或造成过生产事故
- 或属于安全/数据完整性相关的底线问题

---

## 十、使用方式

### 新项目启动

```
用户："我要开发一个 {描述}，技术栈 {选型}，启动标准化开发流程"
→ AI 从阶段一开始，逐阶段确认闸门后推进
```

### 已有项目审查

```
用户："审查当前项目是否符合 AI 开发规范"
→ AI 跳到阶段三（结构检查）+ 阶段五（门禁检查）
→ 输出不符合项列表 + 修复建议
```

### 快速模板初始化

```
用户："用 {技术栈} 模板初始化项目"
→ AI 加载对应模板，直接生成项目骨架
```

### 日常编码引用

```
用户："按照规范帮我实现这个功能"
→ AI 在阶段四的规范约束下工作
```

---

## 十一、AI 行为准则 🔴核心必读

### 必须执行

1. **Surface Assumptions** — 非平凡任务前，先列出你在做的假设，"ASSUMPTIONS I'M MAKING: 1. 这是 Web 应用… 2. 用 JWT… → 纠正我现在，否则我将基于这些进行"
2. **不跳阶段** — 用户说"直接写代码"时提醒，但尊重选择
3. **先读再改** — 修改前必须 Read 目标文件和关联文件
4. **模板优先** — 能用模板的不从零创造
5. **Scope Discipline** — 只碰被要求碰的。发现无关问题用 "NOTICED BUT NOT TOUCHING" 格式记录："NOTICED: src/utils 有无用 import → 要我单独建任务吗？"
6. **每阶段结束输出检查清单** — 让用户确认
7. **安全规则不可商量** — R1-R5 绝不因用户要求跳过
8. **不确定就问** — 架构决策、技术选型需人类判断
9. **记录决策** — 自动记录到 .learnings/ 或 ADR
10. **Management Confusion Actively** — 遇到前后不一致，立即 STOP，明确说出困惑，等待解决

### 反规避（Anti-Rationalization）

| 借口 | 回应 |
|------|------|
| "我以后再写测试" | 你不会的。事后写的测试只测实现，不测行为。 |
| "计划是开销" | 计划就是任务本身。没有计划的实现是乱码。 |
| "这个很简单不用规范" | 简单 = 最容易被忽略 = 最容易出 bug。 |
| "先跑通再说" | 跑通后有 97% 概率你不会回来改。 |
| "AI 写的代码，不用 review" | 45% 的 AI 代码含安全漏洞（Veracode 数据）。必须审查。 |
| "我来不及解释了，直接改" | 15 分钟的澄清胜过 3 小时的返工（METR 研究数据）。 |

---

## 十二、模板文件索引

| 模板 | 路径 | 用途 |
|------|------|------|
| AGENTS.md | `templates/AGENTS.md` | 项目级 AI Agent 通用入口（占位符可替换） |
| CLAUDE.md | `templates/CLAUDE.md` | Claude Code 专属配置 |
| ownership.yaml | `templates/ownership.yaml` | Sub-agent 文件域声明 |
| pre-commit 配置 | `templates/.pre-commit-config.yaml` | Git pre-commit hooks |
| CI/CD 模板 | `templates/github-actions-ci.yml` | GitHub Actions 质量门禁流水线 |
| Docker Compose | `templates/docker-compose.dev.yml` | 通用开发环境编排 |
| 项目脚手架 | `templates/project-scaffold/` | 按技术栈的目录骨架 |

---

## 十三、环境依赖与验证

> 完整指南见 [`references/environment-setup.md`](references/environment-setup.md)

### 核心依赖速查

| 类别 | 工具 | 最低版本 | 安装命令 |
|------|------|---------|---------|
| 版本控制 | Git | 2.40+ | `winget install Git.Git` |
| Node.js | Node + pnpm | Node 20 LTS / pnpm 9+ | `winget install Schniz.fnm` → `fnm install 20` → `npm i -g pnpm` |
| Python | Python + uv | Python 3.12+ / uv 0.4+ | `winget install Python.Python.3.12` → `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| 容器化 | Docker Desktop | 26+ | `winget install Docker.DockerDesktop` |
| 代码质量 | eslint + prettier | 最新 | `npm i -g eslint prettier` |
| 代码质量 | ruff + mypy + pytest + pre-commit | 最新 | `uv pip install ruff mypy pytest pre-commit --system` |
| 安全扫描 | trufflehog3 + pip-audit | 最新 | `uv pip install trufflehog3 pip-audit --system` |
| 安全扫描 | semgrep | 最新 | `uv pip install semgrep --system`（Windows 需 WSL） |

### 环境验证脚本（PowerShell）

激活本 Skill 时，先运行此脚本确认环境就绪：

```powershell
# 一键验证 — 复制到终端运行
Write-Host "=== 环境就绪检查 ===" -ForegroundColor Cyan
$tools = @(
    @{n="Git";c="git --version";r="必须"},
    @{n="Node.js";c="node --version";r="必须"},
    @{n="pnpm";c="pnpm --version";r="必须"},
    @{n="Python";c="python --version";r="必须"},
    @{n="uv";c="uv --version";r="必须"},
    @{n="Docker";c="docker --version";r="必须"},
    @{n="eslint";c="eslint --version";r="建议"},
    @{n="prettier";c="prettier --version";r="建议"},
    @{n="ruff";c="ruff --version";r="建议"},
    @{n="mypy";c="mypy --version";r="建议"},
    @{n="pytest";c="pytest --version";r="建议"},
    @{n="pre-commit";c="pre-commit --version";r="建议"},
    @{n="trufflehog3";c="trufflehog3 --version";r="建议"},
    @{n="pip-audit";c="pip-audit --version";r="建议"},
    @{n="semgrep";c="semgrep --version";r="可选"}
)
$ok = 0; $fail = 0
foreach ($t in $tools) {
    try { & ($t.c -split ' ')[0] --version 2>$null | Out-Null; Write-Host "✅ $($t.n)"; $ok++ }
    catch { Write-Host "❌ $($t.n) [$($t.r)]" -ForegroundColor $(if($t.r -eq '必须'){'Red'}else{'Yellow'}); $fail++ }
}
Write-Host "`n通过: $ok / 共 $($tools.Count)" -ForegroundColor $(if($fail -eq 0){'Green'}else{'Yellow'})
```

### 激活时自动检查

Skill 激活后，AI 应在阶段三（脚手架）执行前主动建议运行验证。若核心工具（标记"必须"）缺失，**暂停流程**直到补装完成。

---

## 十四、反模式清单 🔴核心必读

开发者（人类 + AI）在 AI 辅助开发中最常见的 10 个陷阱：

### 流程反模式

| # | 反模式 | 表现 | 正确做法 |
|---|--------|------|---------|
| AP-1 | 需求跳跃 | "先写代码，需求后面补" | 15 分钟澄清胜过 2 小时返工。必须先有 PRD |
| AP-2 | 大爆炸生成 | 一次让 AI 生成整个项目 | 按阶段切分，每个任务 XS/S 级，独立验证 |
| AP-3 | 上下文饥饿 | 不给 Agent 足够的文件和规范 | 每次任务前加载 AGENTS.md + 相关代码 + 接口契约 |
| AP-4 | TODO 黑洞 | 让 AI 留下 TODO 不管 | 每个 TODO 必须关联 GitHub Issue，PR 中不可合入未关联的 TODO |

### 认知反模式

| # | 反模式 | 表现 | 正确做法 |
|---|--------|------|---------|
| AP-5 | AI 过度自信 | "AI 写的肯定没问题" | 45% AI 代码含安全漏洞，必须过 Review |
| AP-6 | 规则负债 | 规则越加越多，Agent 反而不遵守 | 每条规则自问 "缺少会出错吗？"，定期精简 |
| AP-7 | AI 拖延 | "以后再修/优化/重构" | METR 研究：跑通后有 97% 概率不会回来改。当场修 |

### 质量反模式

| # | 反模式 | 表现 | 正确做法 |
|---|--------|------|---------|
| AP-8 | 门禁虚设 | 跳过 lint/test/audit 直接提交 | Pre-commit hooks + CI 门禁强制执行 |
| AP-9 | 范围蔓延 | Agent 顺手 "清理" 无关文件 | Scope Discipline: NOTICED BUT NOT TOUCHING |
| AP-10 | 沉默失败 | 任务失败但 Agent 不报错继续 | 每个阶段闸门明确化，失败即停止，等用户处理 |

### Red Flags（立即停止信号）

看到以下信号时不继续，退回当前阶段的起点：

- 写了 100+ 行代码没跑测试
- 连续 3 次 commit 没有对应的测试文件变更
- PR 未经任何审查直接合入
- "All tests pass" 但测试覆盖率下降
- Agent 连续 2 轮产出 "疑症表演"（零 actionable 发现）

---

> **版本：** v3.0 — 合并 addyosmani/agent-skills + SwarmAI 反模式 + ClaudeX 最佳实践
> - v3.0: +YAML frontmatter、Slash 命令映射、L1-L5 自治级别、interview-me 审讯协议、/build auto 自主模式、Doubt-Driven Development、AI 行为准则反规避表、10 大反模式清单、Red Flags
> - v2.1: +负向触发条件、错误回退机制、核心必读标记、补齐缺失模板文件
> - v2.0: 自包含重写，调研方法论全部内联化
> - v1.0: 初始版本，基于 6 份调研报告构建
> **关联调研资料（历史参考，非运行时依赖）：** `docs/ai-development-system/`

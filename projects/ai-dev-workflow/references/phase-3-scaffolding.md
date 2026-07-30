# 阶段三：项目脚手架详细步骤

> 所属 Skill：`ai-dev-workflow`
> 目标：按阶段二的设计，创建标准化的项目骨架

---

## 1. 脚手架创建步骤

### 步骤 1：初始化基础结构

```
# 全栈 Monorepo
pnpm create turbo@latest

# React 前端
pnpm create vite@latest --template react-ts

# FastAPI 后端
mkdir -p app/api/v1/endpoints app/core app/models app/schemas app/services
touch app/__init__.py app/main.py

# Taro 小程序
npx @tarojs/cli init
```

### 步骤 2：创建 AI Agent 配置文件

必须按以下优先级创建：

1. **AGENTS.md** — 所有 AI Agent 的通用入口（最先创建）
2. **CLAUDE.md** — Claude Code 专属配置
3. **.claude/agents/** — Sub-agent 专属规则
4. **.claude/rules/** — 领域规则
5. **.claude/ownership.yaml** — 文件所有权策略

### 步骤 3：配置开发工具链

- [ ] Linter（ESLint / Ruff）
- [ ] Formatter（Prettier）
- [ ] Type checker（tsc --strict / mypy strict）
- [ ] Pre-commit hooks（Husky / pre-commit）
- [ ] Git ignore（.gitignore）
- [ ] CI/CD 配置（.github/workflows/）

---

## 2. 脚手架验证清单

创建完成后，运行以下检查：

```bash
# 结构完整性检查
ls AGENTS.md CLAUDE.md                    # ✅ 存在
ls .claude/agents/ .claude/rules/          # ✅ 存在
ls .claude/ownership.yaml                  # ✅ 存在
ls src/ tests/ docs/                       # ✅ 存在

# 工具链验证
pnpm lint          # ✅ 通过
pnpm type-check    # ✅ 通过
pnpm test          # ✅ 0 tests（但框架可用）
```

---

## 3. .gitignore 标准配置

```gitignore
# 依赖
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# 环境变量
.env
.env.local
.env.*.local

# 构建产物
dist/
build/
.next/
out/

# IDE
.idea/
.vscode/
*.swp
*.swo

# 学习记录（保留目录结构，忽略内容）
.learnings/*.md

# OS
.DS_Store
Thumbs.db
```

---

## 4. 配置文件模板引用

- AGENTS.md → [`templates/AGENTS.md`](../templates/AGENTS.md)
- CLAUDE.md → [`templates/CLAUDE.md`](../templates/CLAUDE.md)
- ownership.yaml → [`templates/ownership.yaml`](../templates/ownership.yaml)

---

## 5. v3.1 增强：业务分层 + Feature-First + AGENTS.md 渐进式披露

### 5.1 业务逻辑分层铁律（v3.1 核心升级）

```
项目根/
├── core/                   # ⭐ 业务核心（解析/验证/转换/计算）
│   ├── parsing/            # 配置解析、文件解析
│   ├── validation/         # 输入验证、业务规则
│   ├── transformation/     # 数据转换、ETL
│   └── computation/        # 业务计算、定价、统计
├── cli/ 或 mcp/ 或 ui/     # 薄表现层（IO 转发，无业务逻辑）
├── api/                    # 薄路由（仅入参校验 + 委派 core/）
├── features/               # Feature-First 模块（前端）
└── core/__init__.py        # 暴露 Facade API
```

**铁律（v3.1 红线）**：
- ❌ 业务逻辑禁止放在 `cli/`、`mcp/`、`ui/`、`api/`、`pages/`
- ✅ 所有解析/验证/转换/计算必须经过 `core/`
- ✅ 薄层文件 ≤ 200 行（`.pre-commit-config.yaml` check-core-layer 强制）
- ✅ `core-agent` 拥有 `core/**`，其他 agent 的 `forbidden` 列表必须包含 `core/**`

### 5.2 Feature-First 目录组织（替代 Layer-First）

**❌ Layer-First（不推荐）**：

```
src/
├── components/    # 所有组件混在一起
├── hooks/         # 所有 hooks 混在一起
├── api/           # 所有 API 混在一起
├── types/         # 所有类型混在一起
└── tests/         # 所有测试混在一起
```

**✅ Feature-First（v3.1 推荐）**：

```
src/features/
├── auth/
│   ├── components/      # 登录表单、注册表单
│   ├── hooks/           # useAuth, useLogin
│   ├── api/             # /api/auth/*
│   ├── types.ts         # Auth 相关类型
│   ├── store.ts         # 状态管理
│   ├── index.ts         # 公开 API
│   └── __tests__/       # co-located 测试
├── order/
│   ├── components/
│   ├── hooks/
│   ├── api/
│   ├── types.ts
│   └── ...
└── payment/
    ├── components/
    └── ...
```

**优势**：
- 删除一个 feature = 删除一个目录（无残留）
- 跨 feature 引用强制走 `index.ts`（API 边界清晰）
- AI 写代码时域范围明确，避免无关扩散

### 5.3 AGENTS.md 渐进式披露（v3.1 ≤ 150 行硬约束）

**铁律**：
- AGENTS.md 是 **Map**（索引）不是 **Encyclopedia**（百科全书）
- 硬上限：**≤ 150 行**（`.pre-commit-config.yaml` + GitHub Actions 双重检查）
- 超出后必须拆分到 `docs/agent-handbook.md` 或多个 `docs/{topic}.md`

**AGENTS.md 必须包含的 4 段（v3.1 共识）**：

```markdown
# AGENTS.md（≤ 150 行）

## 1. Project Overview（项目概述）
- 项目名、一句话、目标用户、核心价值
- 技术栈、关键依赖

## 2. Build & Test Commands（构建与测试命令）
- `pnpm install` / `pnpm test` / `pnpm lint`
- 关键命令必须列出，AI 不能靠猜

## 3. Directory Conventions（目录约定）
- 必含 `core/`、`features/`、`cli/`、`api/`
- 引用 `docs/directory.md` 详情

## 4. Code Style & Forbidden（代码风格与禁止项）
- 必含：薄表现层 ≤ 200 行、单函数 ≤ 50 行、TDD 强制
- 必含：业务逻辑必须放 `core/`
- 引用 `docs/code-style.md` 详情
```

**❌ 错误做法**（一次性塞入所有规范）：

```markdown
# ❌ AGENTS.md 写到 500 行
- 安装 50 行的依赖说明
- 详细的 TypeScript 配置
- 完整的 Git 教程
- 整套 ESLint 规则
- 数据库设计指南
...
```

**✅ 正确做法**（索引 + 外链）：

```markdown
# AGENTS.md（150 行内）
- 简述：项目做什么
- 关键命令
- 目录约定
- 速查禁止项
→ 详情：见 docs/agent-handbook.md
```

### 5.4 AGENTS.md vs CLAUDE.md 关系

| 文件 | 范围 | 谁读 |
|------|------|------|
| **AGENTS.md** | 通用规范（所有 AI Agent 读） | Claude Code、Cursor、Aider、Copilot |
| **CLAUDE.md** | Claude Code 特定扩展 | 仅 Claude Code |

**v3.1 推荐：symlink 模式**

```bash
# Linux / macOS / WSL
ln -s AGENTS.md CLAUDE.md

# Windows PowerShell
New-Item -ItemType Junction -Path "CLAUDE.md" -Target "AGENTS.md"
```

或 git 仓库内 `git config core.symlinks true` 后提交真正的 symlink。

### 5.5 agent-neutral 路径规范

v3.1 起，模板中禁止使用 Claude 特定路径：

```
❌ ${CLAUDE_SKILL_DIR}/scripts/xxx.py
✅ ${SKILL_DIR}/scripts/xxx.py     # 通用变量
```

模板示例详见 `templates/AGENTS.md`、`templates/CLAUDE.md`。

### 5.6 v3.1 脚手架新增文件

新增以下 v3.1 必备文件：

```
.github/
├── CODEOWNERS                     # 业务分层所有权（v3.1 新增）
├── PULL_REQUEST_TEMPLATE.md       # PR 模板（含 Assisted-by 强制项）
└── workflows/
    └── quality-gates.yml          # 4 大门禁 CI（详见 templates/github-actions-ci.yml）
```

详细配置见 `templates/branch-protection.md` 与 `templates/pr-template.md`。

---

## 6. v3.2 增强章节（基于用户反馈 2026-07-22 · 减法重构）

> **v3.2 关键变化：** v3.1 强制 AGENTS.md ≤ 150 行 + 强制 CLAUDE.md 软链 + 9 个模板全部必填被证明**过于严苛**。v3.2 改为按项目类型选择模板，AGENTS.md 软性建议 ≤ 200 行。

### 6.1 阶段 3 的规范应用强度（v3.2 重构）

| 规范 | v3.1 状态 | v3.2 状态 | 何时强化 | 何时弱化 |
|------|----------|----------|---------|---------|
| AGENTS.md ≤ 150 行 | 🔴 硬卡 | 🟡 ≤ 200 推荐 | 大型 monorepo | 小项目、CLI 工具 |
| CLAUDE.md 必填 | 🔴 必填 | 🟡 推荐 | 多 AI Agent 协作 | 单 AI 工具使用 |
| 9 个模板全必填 | 🔴 必填 | 🟡 按项目类型 | 企业项目、长期项目 | 原型、一次性脚本 |
| Feature-First 强制 | 🔴 强制 | 🟡 推荐 | Web 前端大型项目 | CLI 工具、小型 API |
| 业务分层强制 | 🔴 强制 | 🟡 推荐 | 大型 monorepo | 单端应用、CLI 工具 |

### 6.2 v3.2 模板选择决策树

```
Q: 这个项目需要哪些模板？
A:
  ├─ 长期项目（> 3 个月）→ 9 个模板全选（AGENTS.md + CLAUDE.md + .pre-commit + CI + PR + CODEOWNERS + branch-protection + docker + README）
  ├─ 短期项目（< 1 个月）→ 4 个核心模板（AGENTS.md + .pre-commit + CI + README）
  └─ 一次性脚本/原型 → 1-2 个模板（AGENTS.md 可选 + README）
```

### 6.3 阶段 3 反模式（v3.2 新增）

**AP-16 规范过度严苛：** 阶段 3 强制所有 9 个模板 + AGENTS.md ≤ 150 行 → 300 行单文件 CLI 也要写完整模板

**AP-20 模板仪式化：** 复制模板但不根据项目类型调整 → 内容与实际需求脱节

### 6.4 v3.2 阶段 3 核心判断

```markdown
Q: 脚手架应该多完整？
A: 取决于 3 个问题：
  1. 项目周期？（< 1 周可极简，> 3 个月需完整）
  2. 团队规模？（单人可选关键模板，团队需完整）
  3. AI 协作深度？（多用 AI 需更多模板，少用可简化）
```

> **v3.2 哲学转变：** 规范是参考书，不是宪法。开发者判断 > 死规则。

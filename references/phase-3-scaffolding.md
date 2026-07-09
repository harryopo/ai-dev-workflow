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

# 阶段二：架构设计详细指南

> 所属 Skill：`ai-dev-workflow`
> 目标：确定技术方案、项目结构和 API 契约

---

## 1. 本阶段目标

基于阶段一的 PRD，产出：

- 技术栈选型决策
- 项目目录结构设计
- 核心 API 接口定义（OpenAPI / GraphQL Schema）
- 数据库 Schema 草案
- 架构决策记录 (ADR)

---

## 2. 技术栈推荐矩阵

### 按项目类型推荐

| 项目类型 | 前端推荐 | 后端推荐 | 数据库 | Monorepo |
|---------|---------|---------|--------|----------|
| 全栈 Web 应用 | Next.js 14 + React 18 + Tailwind + shadcn/ui | FastAPI (Python) 或 NestJS (Node) | PostgreSQL + Redis | Turborepo |
| 纯前端 SPA | Vite + React 18 | — | — | pnpm workspace |
| API 服务 | — | FastAPI 或 Express | PostgreSQL + Redis | — |
| 小程序 | Taro (React) | FastAPI | PostgreSQL | — |
| CLI 工具 | — | Python (Click/Typer) 或 Node.js (Commander) | — | — |
| AI/ML 项目 | Streamlit / Gradio | FastAPI | PostgreSQL + pgvector | — |

### 选型检查清单

- [ ] 技术栈在团队能力范围内？
- [ ] 社区活跃度和长期维护性？（GitHub Stars、最近更新 < 3 个月）
- [ ] 许可协议是否合规？（MIT/Apache2 优先，避免 GPL 传染）
- [ ] 是否与现有基础设施兼容？
- [ ] AI 友好度如何？（类型注解、约定优于配置、显式依赖）

---

## 3. 项目目录结构模板

### 3.1 全栈 Monorepo（Turborepo）⭐ 首推

```
{project-name}/
├── apps/
│   ├── web/                          # Next.js 前端
│   │   ├── src/
│   │   │   ├── app/                 # App Router
│   │   │   │   ├── layout.tsx       # 根布局
│   │   │   │   ├── page.tsx         # 首页
│   │   │   │   ├── loading.tsx
│   │   │   │   ├── error.tsx
│   │   │   │   └── (routes)/        # 路由组
│   │   │   ├── features/            # 按业务领域组织
│   │   │   │   ├── auth/
│   │   │   │   │   ├── components/login-form.tsx
│   │   │   │   │   ├── hooks/use-auth.ts
│   │   │   │   │   ├── api.ts
│   │   │   │   │   ├── types.ts
│   │   │   │   │   └── __tests__/
│   │   │   │   └── dashboard/
│   │   │   ├── components/
│   │   │   │   ├── ui/              # shadcn/ui 原子组件
│   │   │   │   └── layouts/         # 布局组件
│   │   │   ├── lib/                 # 工具 + API 客户端
│   │   │   ├── stores/              # Zustand 状态
│   │   │   ├── hooks/               # 全局 Hooks
│   │   │   └── types/               # 全局类型
│   │   ├── public/
│   │   ├── next.config.ts
│   │   ├── package.json
│   │   └── Dockerfile
│   └── api/                          # FastAPI 后端
│       ├── app/
│       │   ├── api/v1/
│       │   │   ├── router.py        # 路由聚合
│       │   │   └── endpoints/       # 端点文件
│       │   │       ├── auth.py
│       │   │       └── users.py
│       │   ├── core/                # 基础设施
│       │   │   ├── config.py        # pydantic-settings
│       │   │   ├── security.py      # JWT/bcrypt
│       │   │   ├── database.py      # async engine
│       │   │   └── exceptions.py
│       │   ├── models/              # SQLAlchemy ORM
│       │   ├── schemas/             # Pydantic request/response
│       │   ├── services/            # 业务逻辑
│       │   └── main.py
│       ├── alembic/                 # DB 迁移
│       ├── tests/
│       ├── pyproject.toml
│       └── Dockerfile
├── packages/
│   └── shared/                       # 前后端共享类型
│       └── src/
│           ├── types.ts              # User, Product, Order...
│           └── validation.ts         # zod schemas
├── tools/                            # 构建/代码生成工具
├── turbo.json                        # Turborepo 管道
├── pnpm-workspace.yaml
├── docker-compose.yml
├── docker-compose.dev.yml
├── AGENTS.md
├── CLAUDE.md
├── .env.example
└── .gitignore
```

### 3.2 React 前端（Vite）

```
{project-name}/
├── src/
│   ├── app/                       # App.tsx + router + providers
│   ├── pages/                     # 路由页面（薄层，只做路由入口）
│   ├── features/                  # Feature-First 模块
│   │   └── {feature}/
│   │       ├── components/
│   │       ├── hooks/
│   │       ├── api.ts
│   │       ├── types.ts
│   │       └── __tests__/
│   ├── components/
│   │   ├── ui/                    # 原子组件
│   │   └── layouts/
│   ├── hooks/                     # 全局 Hooks
│   ├── lib/                       # 工具/API 客户端
│   ├── stores/                    # 全局状态 (Zustand)
│   ├── types/                     # 全局类型
│   └── styles/
├── tests/
├── AGENTS.md
└── CLAUDE.md
```

### 3.3 FastAPI 后端

```
{project-name}/
├── app/
│   ├── api/v1/
│   │   ├── router.py
│   │   └── endpoints/
│   ├── core/
│   │   ├── config.py              # pydantic-settings
│   │   ├── security.py            # JWT + password hashing
│   │   └── database.py            # async SQLAlchemy engine
│   ├── models/                    # SQLAlchemy ORM
│   ├── schemas/                   # Pydantic request/response
│   ├── services/                  # 业务逻辑（纯函数/类）
│   ├── repositories/              # DB 操作（可选，大型项目推荐）
│   ├── middleware/                 # CORS, auth, logging
│   └── main.py                    # FastAPI app 工厂
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
├── pyproject.toml                 # uv/poetry 项目定义
├── Dockerfile
├── AGENTS.md
├── CLAUDE.md
└── .env.example
```

### 3.4 Express 后端（Node.js/TypeScript）

```
{project-name}/
├── src/
│   ├── api/                          # 路由定义
│   │   ├── index.ts                  # 路由聚合
│   │   ├── auth.routes.ts
│   │   └── user.routes.ts
│   ├── controllers/                  # 请求处理（薄层）
│   ├── services/                     # 业务逻辑
│   ├── repositories/                 # 数据访问
│   ├── models/                       # Prisma/Drizzle ORM
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── validate.middleware.ts    # zod 验证
│   ├── config/
│   │   ├── index.ts
│   │   ├── database.ts
│   │   └── env.ts                    # 环境变量类型校验
│   ├── types/
│   └── app.ts                        # Express 实例
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── tests/
├── AGENTS.md
└── CLAUDE.md
```

### 3.5 Taro 小程序

```
{project-name}/
├── src/
│   ├── pages/                     # 页面（每个页面一个目录）
│   │   └── {page}/
│   │       ├── index.tsx
│   │       ├── index.config.ts
│   │       └── index.scss
│   ├── components/
│   │   ├── common/
│   │   └── business/
│   ├── services/                  # API 服务
│   ├── stores/
│   ├── hooks/
│   ├── utils/
│   └── app.config.ts
├── AGENTS.md
└── CLAUDE.md
```

---

## 4. ADR 模板

每个关键架构决策必须记录为 ADR（Architecture Decision Record）：

```markdown
# ADR-{序号}: {决策标题}

## 状态
{提议中 / 已接受 / 已废弃 / 已取代}

## 背景
为什么需要做这个决策？

## 决策
我们决定采用什么方案？

## 后果
### 正面影响
- ...
### 负面影响
- ...
### 需要关注的
- ...

## 备选方案
| 方案 | 优点 | 缺点 | 为何未选择 |
|------|------|------|-----------|
| 方案A | ... | ... | ... |
| 方案B | ... | ... | ... |
```

---

## 5. 闸门检查清单

- [ ] 技术栈选型有明确理由？
- [ ] 目录结构符合选定模板？
- [ ] 核心 API 接口已定义（至少 P0 功能）？
- [ ] 数据库核心表已设计？
- [ ] 安全威胁已识别并制定缓解方案？
- [ ] 用户已确认 ADR？

---

## 6. v3.2 增强章节（基于用户反馈 2026-07-22 · 减法重构）

> **v3.2 关键变化：** v3.1 强制 core/cli/mcp 分层 + 200 行硬卡被证明**对小项目和 CLI 工具过于严苛**。v3.2 改为按项目类型建议。

### 6.1 阶段 2 的规范应用强度（v3.2 重构）

| 规范 | v3.1 状态 | v3.2 状态 | 何时强化 | 何时弱化 |
|------|----------|----------|---------|---------|
| 必须写完整 ADR | 🔴 红线 | 🟡 软性建议 | 长期项目、多模块 | 一次性脚本 |
| 业务逻辑在 core/ | 🔴 红线（200 行硬卡） | 🟡 软性建议 | 大型 monorepo | CLI 工具、单文件应用 |
| Feature-First 组织 | 🔴 强制 | 🟡 建议 | 大型项目 | 小项目可按类型分 |
| 必须有 OpenAPI | 🔴 API 项目必填 | 🟡 推荐 | API 服务、库 | 内部脚本 |
| 单文件 ≤ 800 行 | 🔴 硬卡 | 🟡 ≤ 2000 推荐 | 业务代码 | 桌面 GUI、生成代码 |

### 6.2 5 种项目类型的目录结构（v3.2 新增）

| 项目类型 | 推荐结构 | 关键特征 |
|---------|---------|---------|
| 🌐 **Web 前端 / 全栈** | `features/{domain}/` + `components/ui/` + `hooks/` | Feature-First Colocation |
| 🖥️ **桌面应用** | `src/main/` + `src/renderer/` + `src/preload/` | Electron IPC 分层 |
| 📱 **移动端 App** | `screens/` + `components/` + `services/` | 平台适配优先 |
| 🔌 **API 服务** | `app/api/v1/`（薄） + `app/core/`（业务） + `app/models/` | 严格分层（API 场景需要） |
| ⚙️ **CLI 工具** | `commands/` + `core/`（可选） + `lib/` | 重点是易用性 |

### 6.3 阶段 2 反模式（v3.2 新增）

**AP-16 规范过度严苛：** 阶段 2 过度设计、强制分层、要求所有项目都用同一套结构 → CLI 工具和单页应用痛苦

**AP-17 轻量即正义：** 调研时以"不够轻量"为由删除 2-3 个有价值的备选方案 → 用户选择空间被压缩

**AP-19 单文件应用被强制分层：** 给 300 行单文件 CLI 强加 core/ + cli/ 分层 → 反而更难维护

### 6.4 阶段 2 的 v3.2 决策树

```
Q: 这个项目应该用哪种目录结构？
A:
  ├─ Web 前端 / 全栈 → Feature-First（features/auth/ 包含 components + hooks + api）
  ├─ 桌面应用 → Electron 标准结构（main + renderer + preload）
  ├─ 移动端 App → 按平台（screens/ + services/）
  ├─ API 服务 → 严格分层（api/ 薄 + core/ 业务 + models/）
  └─ CLI 工具 → 极简（一个文件即可，业务逻辑与命令共存）
```

### 6.5 v3.2 阶段 2 核心判断

```markdown
Q: 阶段 2 应该做多深？
A: 取决于 3 个问题：
  1. 项目类型？（API 服务需要完整 OpenAPI，CLI 工具可省略）
  2. 团队规模？（多人协作需 ADR，单人可简化）
  3. 复用需求？（多端复用需分层，单一端可简化）
```

> **v3.2 哲学转变：** 规范是参考书，不是宪法。开发者判断 > 死规则。

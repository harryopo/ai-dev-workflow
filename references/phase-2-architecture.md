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

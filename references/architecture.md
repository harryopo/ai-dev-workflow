# 阶段二：架构设计与目录结构

> 所属 Skill：`ai-dev-workflow`
> 目标：基于 PRD 确定技术方案、项目目录结构、API 契约、DB Schema

---

## 1. 产出物

- 技术栈选型决策
- 完整项目目录树
- 核心 API 接口定义（OpenAPI / GraphQL Schema）
- 数据库 Schema 草案（核心表）
- 架构决策记录 (ADR)

---

## 2. 技术栈推荐矩阵

| 项目类型 | 前端 | 后端 | 数据库 | 包管理 | Monorepo 方案 |
|---------|------|------|--------|--------|-------------|
| 全栈 Web | Next.js 14 + React 18 + Tailwind + shadcn/ui | FastAPI (Python) / NestJS (Node) | PostgreSQL + Redis | pnpm + uv | Turborepo |
| 纯前端 SPA | Vite + React 18 + Tailwind | — | — | pnpm | pnpm workspace |
| API 服务 | — | FastAPI / Express / Spring Boot | PostgreSQL + Redis | uv / pnpm / gradle | — |
| 小程序 | Taro (React) + NutUI | FastAPI | PostgreSQL | pnpm + uv | — |
| CLI 工具 | — | Python (Click/Typer) / Node (Commander) | SQLite | uv / pnpm | — |
| AI/ML | Streamlit / Gradio | FastAPI | PostgreSQL + pgvector | uv | — |

### 选型检查清单

- [ ] 技术栈在团队能力范围内？
- [ ] 社区活跃度 OK？（GitHub Stars、最近更新 < 3 个月）
- [ ] 许可协议合规？（MIT/Apache2 优先，避免 GPL 传染）
- [ ] 与现有基础设施兼容？
- [ ] AI 友好度如何？评判标准：
  - 有完整类型注解（TypeScript / Python type hints）
  - 约定优于配置（Next.js 文件路由 / Rails 约定）
  - 显式依赖声明（package.json / pyproject.toml）

---

## 3. 项目目录结构模板

### 3.1 全栈 Monorepo（Turborepo）⭐ 首推

```
{project}/
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
│   │   └── package.json
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
{project}/
├── src/
│   ├── app/                          # App.tsx + router + providers
│   ├── pages/                        # 路由页面（薄层，只做路由入口）
│   ├── features/                     # 业务功能模块
│   │   └── {feature}/
│   │       ├── components/           # 功能专属组件
│   │       ├── hooks/                # 功能专属 Hooks
│   │       ├── api.ts                # 功能 API 调用
│   │       ├── types.ts              # 功能类型定义
│   │       └── __tests__/            # 功能测试
│   ├── components/
│   │   ├── ui/                       # 无状态原子组件
│   │   └── layouts/                  # 布局
│   ├── hooks/                        # 全局共享 Hooks
│   ├── lib/                          # api-client + utils
│   ├── stores/                       # 全局状态(Zustand)
│   ├── types/                        # 全局类型
│   └── styles/                       # 全局样式 + tokens
├── tests/
├── vite.config.ts
├── tsconfig.json
├── AGENTS.md
└── CLAUDE.md
```

### 3.3 FastAPI 后端

```
{project}/
├── app/
│   ├── api/v1/
│   │   ├── router.py
│   │   └── endpoints/
│   ├── core/
│   │   ├── config.py                 # pydantic-settings
│   │   ├── security.py               # JWT + password hashing
│   │   ├── database.py               # async SQLAlchemy engine
│   │   └── exceptions.py             # 自定义异常 + handlers
│   ├── models/                       # SQLAlchemy ORM 模型
│   ├── schemas/                      # Pydantic request/response
│   ├── services/                     # 业务逻辑（纯函数/类）
│   ├── repositories/                 # DB 操作（可选，大型项目推荐）
│   ├── middleware/                    # CORS, auth, logging
│   └── main.py                       # FastAPI app 工厂
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py                   # 共享 fixtures
│   ├── test_api/
│   └── test_services/
├── scripts/                          # 种子数据、运维脚本
├── pyproject.toml                    # uv/poetry 项目定义
├── Dockerfile
├── AGENTS.md
├── CLAUDE.md
└── .env.example
```

### 3.4 Express 后端（Node.js/TypeScript）

```
{project}/
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
{project}/
├── src/
│   ├── pages/                        # 页面（每个一个目录）
│   │   └── {page}/
│   │       ├── index.tsx
│   │       ├── index.config.ts       # 页面配置
│   │       └── index.scss
│   ├── components/
│   │   ├── common/                   # 通用组件
│   │   └── business/                 # 业务组件
│   ├── services/                     # API 封装
│   ├── stores/                       # 状态管理
│   ├── hooks/                        # 自定义 Hooks
│   ├── utils/                        # 工具函数
│   ├── constants/
│   ├── types/
│   └── app.config.ts                 # 全局配置
├── config/
│   ├── index.ts                      # Taro 编译配置
│   ├── dev.ts
│   └── prod.ts
├── AGENTS.md
└── CLAUDE.md
```

---

## 4. ADR 模板

```markdown
# ADR-{序号}: {决策标题}

## 状态
提议中 / 已接受 / 已废弃 / 已被 ADR-XXX 取代

## 背景
为什么需要做这个决策？上下文是什么？

## 决策
我们决定采用什么方案？

## 后果
### 正面
-
### 负面
-
### 需关注
-

## 备选方案
| 方案 | 优点 | 缺点 | 未选择原因 |
|------|------|------|-----------|
```

---

## 5. 闸门检查清单

- [ ] 技术栈选型有明确理由？通过了选型检查清单？
- [ ] 目录结构符合选定模板？（AI 逐项对比检查）
- [ ] 核心 API 接口已定义（至少覆盖 P0 功能）？
- [ ] 数据库核心表已设计（ER 图或 DDL 草案）？
- [ ] 安全威胁已识别并制定缓解方案？
- [ ] ADR 已生成并经用户确认？
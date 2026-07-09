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
| 全栈 Web 应用 | Next.js 14 + React 18 | FastAPI (Python) 或 NestJS | PostgreSQL | Turborepo |
| 纯前端 SPA | Vite + React 18 | - | - | pnpm workspace |
| API 服务 | - | FastAPI 或 Express | PostgreSQL + Redis | - |
| 小程序 | Taro (React) | FastAPI | PostgreSQL | - |
| CLI 工具 | - | Python (Click/Typer) 或 Node.js (Commander) | - | - |
| AI/ML 项目 | Streamlit/Gradio | FastAPI | PostgreSQL + 向量库 | - |

### 选型检查清单

- [ ] 技术栈在团队能力范围内？
- [ ] 社区活跃度和长期维护性？（GitHub Stars、最近更新时间）
- [ ] 许可协议是否合规？
- [ ] 是否与现有基础设施兼容？
- [ ] AI 友好度如何？（类型注解、约定优于配置、显式依赖）

---

## 3. 项目目录结构模板

### 3.1 全栈 Monorepo（Turborepo）— 推荐

```
{project-name}/
├── apps/
│   ├── web/                       # Next.js 前端
│   │   ├── src/
│   │   │   ├── app/              # App Router（文件路由）
│   │   │   ├── features/         # 功能模块（Feature-First）
│   │   │   │   ├── auth/
│   │   │   │   │   ├── components/
│   │   │   │   │   ├── hooks/
│   │   │   │   │   ├── api.ts
│   │   │   │   │   └── types.ts
│   │   │   │   └── dashboard/
│   │   │   ├── components/
│   │   │   │   ├── ui/           # shadcn/ui 基础组件
│   │   │   │   └── layouts/
│   │   │   ├── lib/              # 工具函数
│   │   │   ├── stores/           # 状态管理
│   │   │   └── types/            # 全局类型
│   │   ├── public/
│   │   ├── tests/
│   │   └── package.json
│   └── api/                       # FastAPI / NestJS 后端
│       ├── app/
│       │   ├── api/v1/endpoints/
│       │   ├── core/             # config, security, database
│       │   ├── models/           # ORM 模型
│       │   ├── schemas/          # Pydantic 验证
│       │   ├── services/         # 业务逻辑
│       │   └── main.py
│       ├── migrations/
│       └── pyproject.toml
├── packages/
│   └── shared/                    # 前后端共享类型
│       └── src/
│           ├── types.ts
│           └── validation.ts
├── turbo.json
├── pnpm-workspace.yaml
├── AGENTS.md
├── CLAUDE.md
└── docker-compose.yml
```

### 3.2 React 前端（Vite）

```
{project-name}/
├── src/
│   ├── app/                       # 应用壳（router, providers）
│   ├── pages/                     # 页面组件
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
│   ├── stores/                    # 全局状态
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
│   │   ├── security.py
│   │   └── database.py
│   ├── models/                    # SQLAlchemy ORM
│   ├── schemas/                   # Pydantic
│   ├── services/                  # 业务逻辑
│   └── main.py
├── alembic/                       # 数据库迁移
├── tests/
├── AGENTS.md
└── CLAUDE.md
```

### 3.4 Taro 小程序

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

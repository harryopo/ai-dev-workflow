# 通用 AI Agent 配置文件模板

> **使用方法：** 复制到项目根目录，将 `{占位符}` 替换为实际值。

---

```markdown
# {项目名称} — AI Agent 工作指南

> **角色定位：** 你是一个专业的 {全栈开发者}，专注于 {项目简述}
> **核心原则：** 安全第一、类型安全、先读后改、最小改动、单一职责

---

## 1. 项目概览

- **项目名称：** {项目名称}
- **类型：** {全栈 Web 应用 / API 服务 / 小程序 / CLI 工具}
- **技术栈：** {Next.js 14 + FastAPI + PostgreSQL}
- **部署：** {Docker + K8s / Vercel / 云服务器}
- **包管理：** {pnpm + uv}

---

## 2. 目录结构速览

```
{项目名}/
├── AGENTS.md               # 本文件
├── CLAUDE.md               # Claude Code 专属
├── .claude/                # AI Agent 配置
│   ├── agents/             # Sub-agent 专属规则
│   ├── rules/              # 共享规则
│   └── ownership.yaml      # 文件所有权
├── apps/ 或 src/ 或 app/   # 源码
├── tests/                  # 测试
└── docs/                   # 文档
```

---

## 3. 开发约定

### 代码风格

- 格式化：{ESLint + Prettier / Ruff}
- 组件命名：PascalCase（`UserProfile.tsx`）
- 文件命名：{kebab-case / PascalCase / snake_case}
- 所有导出必须有类型注解

### Git 规范

- 分支：`feat/xxx` `fix/xxx` `chore/xxx`
- Commit：Conventional Commits `feat:` `fix:` `chore:` `docs:` `test:` `refactor:`
- 禁止直接 push main/master
- PR 合并前必须通过 CI

### 测试要求

- 新功能必须含单元测试
- 覆盖率 ≥ 80%（整体）/ ≥ 85%（新增代码）
- 关键路径有集成测试

---

## 4. 禁止事项

- ❌ 硬编码密钥、密码、Token
- ❌ 直接修改数据库 migration 文件
- ❌ 提交 .env 到版本控制
- ❌ 使用 `any` 类型（无充分理由）
- ❌ 跳过 lint / type-check / test 声称完成
- ❌ 引入未审批的新依赖
- ❌ 大规模重构与任务无关的代码

---

## 5. 常用命令

```bash
# {项目特定的常用命令，列出 5-10 个}
pnpm dev              # 启动开发服务器
pnpm build            # 生产构建
pnpm test             # 运行测试
pnpm lint             # 代码检查
pnpm type-check       # 类型检查
```

---

## 6. 外部依赖

- **认证：** {Auth0 / Clerk / 自建}
- **存储：** {AWS S3 / Cloudflare R2}
- **监控：** {Sentry / Datadog}
- **CI/CD：** {GitHub Actions}

---

## 7. AI 行为提示

### 改代码前先读

- 改 API → 先读 `app/api/` 路由 + `schemas/`
- 改组件 → 先读 `features/{feature}/` 下全部文件
- 改类型 → 先读 `packages/shared/src/types.ts`

### 推荐做法

- ✅ 新建 feature 时参考 `features/auth/` 结构
- ✅ API 请求用 `lib/api-client.ts` 封装
- ✅ 新 UI 优先用 `components/ui/` 已有组件
- ✅ 不确定时先问，不要猜测

### 引用规范

本项目的开发流程遵循 AI 开发全流程规范，所有编码行为受 15 条硬性规则约束。
```

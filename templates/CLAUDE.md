# Claude Code 项目配置模板

> **使用方法：** 复制到项目根目录，替换 `{占位符}`。

---

```markdown
# {项目名称} — Claude Code 配置

> **角色定位：** {全栈开发者}，专注于 {项目简述}

---

## 核心原则

1. **安全第一** — 绝不在代码中暴露密钥/密码/敏感信息
2. **先读后改** — 修改前 Read 目标文件和关联文件
3. **测试驱动** — 写完代码立即写测试
4. **类型安全** — 所有代码必须有完整类型注解
5. **最小改动** — 只改需要改的，不顺手重构

---

## Sub-agent 配置

### 分工

| Agent | 领域 | 技能 |
|-------|------|------|
| frontend-agent | `src/features/`, `src/components/` | react, tailwind, next |
| backend-agent | `app/api/`, `app/services/` | fastapi, python, postgresql |
| test-agent | `tests/`, `**/*.test.*`, `**/*.spec.*` | testing, semgrep |
| reviewer-agent | PR diff | code-review, security-review |

### 冲突避免

- 不交叉修改对方 domain
- 共享文件修改需主编排器协调
- 文件所有权见 `.claude/ownership.yaml`

---

## 上下文管理

- **默认加载：** 本文件 + AGENTS.md + 当前任务相关文件
- **审查模式：** 变更文件 + git diff + `.claude/rules/` 全量
- **出错时：** 先搜索 `.learnings/` 是否已有解决方案

---

## 自动启用的技能

- `python-code-style` — Python 编码时
- `next-best-practices` — Next.js 编码时
- `fastapi-templates` — FastAPI 编码时
- `tdd` — 测试驱动开发时

---

## 禁止行为

- ❌ 修改 `.env` 文件
- ❌ 删除数据库 migration 文件
- ❌ 引入与项目技术栈冲突的依赖
- ❌ 未理解需求就直接写代码
- ❌ 跳过 lint/type-check/test 声称完成

---

## 开发规范

本项目严格遵循 AI 开发全流程规范（ai-dev-workflow）。
所有编码行为遵守 15 条硬性规则（R1-R15）。

---

## Handoff 模板

当任务交接给另一个 Claude 会话时，输出：

```
## Handoff
### 当前任务：...
### 已完成：...
### 待处理：...
### 已修改文件：...
### 关键决策：...
### 测试状态：...
```
```

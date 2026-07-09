# 阶段四：编码规范详细指南

> 所属 Skill：`ai-dev-workflow`
> 目标：确保所有代码符合硬性规则和最佳实践

---

## 1. 编码前检查

在开始编写任何代码前，AI 必须完成：

1. [ ] 读取 `CLAUDE.md` 和 `AGENTS.md`（理解项目约定）
2. [ ] 读取相关 feature 的现有代码（理解上下文）
3. [ ] 确认文件归属（不会修改其他 Agent 的领域）
4. [ ] 加载需要的 Skill（如 `python-code-style`、`next-best-practices`）

---

## 2. 语言特定规范

### 2.1 TypeScript / React

```typescript
// ✅ 正确：函数式组件 + 类型定义
interface LoginFormProps {
  onSuccess: (user: User) => void;
  redirectTo?: string;
}

export function LoginForm({ onSuccess, redirectTo = '/' }: LoginFormProps) {
  const { login, isLoading, error } = useLogin();
  // 逻辑 Hook 在上，UI 在下
  return <form>...</form>;
}

// ❌ 错误
// - 缺少类型定义
// - 没有分离逻辑和 UI
// - 使用 any
```

**硬性规则：**
- 所有组件必须有 Props 类型定义
- `use client` 只在必要时使用（Server Components 优先）
- 禁止使用 `any`（除非有充分理由并注释）
- 图片使用 `next/image`，禁止裸 `<img>`
- 表单使用 react-hook-form + zod 验证

### 2.2 Python / FastAPI

```python
# ✅ 正确：类型注解 + Pydantic 验证
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

@router.post("/users", response_model=UserRead)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建新用户。"""
    user = await user_service.create(db, user_in)
    return user

# ❌ 错误
# - 缺少类型注解
# - 没有 Pydantic 验证
# - 在路由中直接操作数据库
```

**硬性规则：**
- 所有 API 端点必须有 Pydantic schema
- 数据库操作必须异步（async session）
- 敏感操作必须有审计日志
- 配置通过 pydantic-settings 管理
- 禁止在请求处理中做 CPU 密集计算

### 2.3 Git Commit 规范

```
feat: 添加用户登录功能
fix: 修复 JWT token 过期未刷新问题
chore: 更新依赖版本
docs: 更新 API 文档
test: 添加用户模块单元测试
refactor: 提取公共认证逻辑
```

- 一个 commit 只做一件事
- Commit message 格式：`<type>: <description>`
- 禁止 `WIP`、`fix bug`、`update` 等无意义 message

---

## 3. Sub-agent 使用规范

当任务复杂时，使用 Sub-agent 分解：

### 3.1 何时使用 Sub-agent

| 场景 | 策略 |
|------|------|
| 前/后端同时开发 | 分派前端 Agent + 后端 Agent 并行 |
| 独立功能模块 | 分派独立 Agent |
| 代码审查 | 专用 review Agent |
| 测试编写 | 专用 test Agent |

### 3.2 Sub-agent 分配规则

```yaml
# .claude/ownership.yaml
frontend-agent:
  domains: ["src/pages/**", "src/features/**", "src/components/**"]
  skills: ["react-state-management", "tailwind-design-system", "next-best-practices"]
  forbidden: ["src/api/**", "src/db/**"]

backend-agent:
  domains: ["app/api/**", "app/models/**", "app/services/**"]
  skills: ["fastapi-templates", "python-code-style", "postgresql-table-design"]
  forbidden: ["src/pages/**", "src/features/**"]

test-agent:
  domains: ["tests/**", "**/__tests__/**"]
  forbidden: ["src/**", "app/**"]  # 只读

shared_files: ["packages/shared/**", "AGENTS.md", "CLAUDE.md"]
```

### 3.3 冲突避免

- 共享文件修改需要主编排器协调
- Agent A 修改共享文件前 → 请求锁定 → Agent B 确认 → 修改 → 释放
- 不同 Agent 绝不修改对方的 domain 文件

---

## 4. AI 编码行为约束

1. **先读再写** — 修改前必须先读取目标文件和关联文件
2. **最小改动** — 只改需要改的，不顺手重构无关代码
3. **自测先行** — 写完代码立即写测试
4. **类型安全** — TypeScript strict / Python mypy strict
5. **命名即文档** — 变量名、函数名清晰表达意图
6. **禁止魔法数字** — 所有常量提取到命名常量
7. **单一职责** — 一个函数只做一件事

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

---

## 5. v3.1 增强：TDD 强制 + Immutability + 薄层铁律

### 5.1 TDD 强制（RED → GREEN → IMPROVE）

**v3.1 铁律**：禁止"先实现后补测试"。

```
RED        → 先写失败的测试（不写实现）
              AI 必须引导用户运行测试并确认失败
GREEN      → 写最小实现让测试通过
              AI 必须引导用户运行测试并确认通过
IMPROVE    → 重构（消除重复、改善命名、提取函数）
              AI 必须保持测试全部通过
```

**示例对话**（v3.1 标准）：

```
用户：帮我写一个函数，计算订单总价（含税）
AI：  我先写测试用例：
      it('订单总价含税', () => {
        expect(calcTotal(100, 0.1)).toBe(110);
      });
      请先确认这个测试用例是否覆盖你的需求，然后再让我写实现。
用户：ok，开始
AI：  实现已写完。请运行 `pnpm test` 确认通过。
      通过后我们再讨论是否有重复代码可以重构。
```

### 5.2 不可变性原则（Immutability）

**v3.1 铁律**：禁止原地修改，全部创建新对象。

| ❌ 错误（变异） | ✅ 正确（不可变） |
|---------------|-----------------|
| `arr.push(x)` | `[...arr, x]` |
| `arr.splice(i, 1)` | `[...arr.slice(0, i), ...arr.slice(i + 1)]` |
| `obj.key = v` | `{ ...obj, key: v }` |
| `obj.delete('k')` | `Object.fromEntries(Object.entries(obj).filter(...))` |

**为什么**：
- 避免副作用（debug 时不知道哪一步改了状态）
- 便于推理（state 改变 = 引用改变）
- time-travel debugging（Redux DevTools 友好）
- 并发安全（race condition 更少）

**框架级支持**：
- React：`useState((prev) => [...prev, x])`
- Redux Toolkit：内部用 Immer，写"变异"代码自动转不可变
- Python：`dataclasses.replace(obj, key=v)`、`frozen=True`

### 5.3 薄表现层铁律（CLI/MCP/UI/API）

**文件长度硬约束**（`.pre-commit-config.yaml` check-core-layer 强制）：

```
cli/parse-config.ts   ≤ 200 行  → 超出必须把逻辑移到 core/
mcp/handler.ts        ≤ 200 行  → 超出同上
ui/UserForm.tsx       ≤ 200 行  → 超出必须拆分子组件
api/auth.ts           ≤ 200 行  → 超出必须委派 core/ + 加 sub-route
```

**为什么 ≤ 200 行**：
- 表现层只做 IO 转发，逻辑都在 core/
- 超出 = 业务逻辑泄漏到表现层
- 薄层是 sub-agent 重叠区域（前后端共用），大了就难以协调

**应对步骤**（发现 cli/ 写到 300 行）：

```bash
# 1. 识别业务逻辑
grep -E "(if|switch|calc|validate)" cli/parse-config.ts

# 2. 提取到 core/parse-config.ts
# 3. cli/parse-config.ts 只保留：
#    - 参数解析
#    - 调用 core.parseConfig()
#    - 输出格式化
```

### 5.4 业务逻辑必须放 core/

**绝对禁止**（v3.1 红线）：

```typescript
// ❌ 错误：cli/ 里写业务判断
// cli/parse-config.ts
export function parseConfig(path: string) {
  const config = fs.readFileSync(path, 'utf-8');
  // ❌ 业务判断在 cli/ 层
  if (!config.includes('version')) {
    throw new Error('Config missing version');
  }
  // ❌ 业务转换在 cli/ 层
  const version = config.match(/version: (.*)/)[1];
  return { version: parseInt(version) };
}
```

```typescript
// ✅ 正确：cli/ 只做 IO，core/ 做业务
// core/parsing/config.ts
export function parseConfigContent(content: string): Config {
  validateConfigHasVersion(content);  // 业务验证
  return extractVersion(content);     // 业务转换
}

// cli/parse-config.ts
export function parseConfig(path: string) {
  const content = fs.readFileSync(path, 'utf-8');  // IO
  return parseConfigContent(content);                // 委派 core/
}
```

### 5.5 Sub-agent 矩阵扩展（v3.1 升级到 20+ 角色）

v3.0 是 6 个 agent，v3.1 扩展到 20+：

| Agent | 域 | 触发场景 |
|-------|-----|----------|
| **core-agent** | `core/**` | 业务逻辑（解析/验证/转换/计算） |
| frontend-agent | `src/features/**`, `src/components/**` | UI 开发 |
| backend-agent | `app/api/**`, `app/models/**` | API 路由 |
| cli-agent | `cli/**` | CLI 入口 |
| mcp-agent | `mcp/**` | MCP server 工具 |
| ui-agent | `ui/**` | 桌面 UI |
| mobile-agent | `apps/mobile/**` | React Native / Flutter |
| data-agent | `models/**`, `migrations/**` | 数据库 schema |
| payment-agent | `features/payment/**` | 支付集成 |
| notification-agent | `features/notification/**` | 邮件/短信 |
| search-agent | `features/search/**` | 搜索/索引 |
| auth-agent | `features/auth/**` | 认证/授权 |
| i18n-agent | `locales/**`, `i18n/**` | 国际化 |
| infra-agent | `infra/**`, `docker/**` | 基础设施 |
| devops-agent | `.github/`, `Dockerfile` | CI/CD |
| security-agent | `auth/**`, `security/**` | 安全 |
| test-writer | `**/__tests__/**`, `tests/**` | 编写测试 |
| reviewer-agent | （只读） | 代码审查 |
| docs-agent | `docs/**` | 文档 |
| migration-agent | `migrations/**` | 数据库迁移 |

**路由策略**：
- 主编排器读取 `ownership.yaml` 自动路由
- 冲突时按 `forbidden` 列表拒绝越权
- `core-agent` 拥有最高优先级（任何业务逻辑变更必经 core-agent）

### 5.6 FIRST / AAA / Right-BICEP 测试原则

**FIRST**（测试本身的质量）：

```
F - Fast       单元测试 < 100ms
I - Independent 测试间不共享状态
R - Repeatable 在任何环境结果一致
S - Self-validating 无需人工判断（pass/fail 明确）
T - Timely     与产品代码同步编写（RED 阶段）
```

**AAA**（测试结构）：

```typescript
it('订单总价含税', () => {
  // Arrange
  const order = { items: [...], taxRate: 0.1 };

  // Act
  const total = calcTotal(order);

  // Assert
  expect(total).toBe(110);
});
```

**Right-BICEP**（决定测什么）：

```
B - Boundary   边界（0, -1, MAX_INT, 空数组）
I - Inverse    反向验证（encode/decode 互逆）
C - Cross-check 交叉验证（用其他方法算同样结果）
E - Error      错误条件（无效输入、异常路径）
P - Performance 性能（在合理时间内完成）
```

---

## 6. v3.1 编码阶段总检查清单

- [ ] TDD RED 阶段：测试先写，确认失败
- [ ] TDD GREEN 阶段：实现最小代码，确认通过
- [ ] TDD IMPROVE 阶段：重构保持绿色
- [ ] 业务逻辑全部在 `core/`（检查 `cli/`、`mcp/`、`ui/`、`api/` 无业务）
- [ ] 不可变原则（无 `.push()`、`.splice()`、原地 mutation）
- [ ] 单文件 ≤ 800 行（`.pre-commit-config.yaml` 强制）
- [ ] 薄表现层 ≤ 200 行（`check-core-layer` 钩子强制）
- [ ] 单元测试覆盖新代码
- [ ] commit message 包含 `Assisted-by:` trailer
- [ ] 无 console.log / 调试代码残留
- [ ] 无 TODO/FIXME 阻塞性遗留

---

## 8. v3.2 增强章节（基于用户反馈 2026-07-22 · 减法重构）

> **v3.2 关键变化：** v3.1 强制不可变（禁止 .push()）、单文件 ≤ 800 行硬卡、TDD 全流程被证明**过于严苛**。v3.2 改为软性建议 + 关键路径优先。

### 8.1 阶段 4 的规范应用强度（v3.2 重构）

| 规范 | v3.1 状态 | v3.2 状态 | 何时强化 | 何时弱化 |
|------|----------|----------|---------|---------|
| 不可变原则 | 🔴 红线（禁止 .push()） | 🟡 软性建议 | 状态管理（Redux/Zustand） | 高性能循环、原生 API 桥接 |
| 单文件 ≤ 800 行 | 🔴 硬卡 | 🟡 ≤ 2000 推荐 | 业务代码、库 | 桌面 GUI、生成代码、单文件可执行 |
| 薄层 ≤ 200 行 | 🔴 硬卡 | 🟡 ≤ 500 推荐 | Web/Mobile/API | CLI 工具（豁免） |
| TDD 强制（85% 覆盖率） | 🔴 红线 | 🟡 软性建议 | 金融/医疗/支付 API、库 | 原型/UI/演示项目 |
| 必带 Assisted-by | 🔴 必填 | 🟡 推荐 | 长期项目 | 个人项目、紧急修复 |
| .push() 禁用 | 🔴 红线 | 🟡 推荐 | 业务核心 | 性能敏感代码 |

### 8.2 关键路径优先原则（v3.2 核心）

**v3.2 关键路径（必须测试 + 重点 Code Review）：**
- 🔐 认证、授权、密码哈希
- 💰 支付、订单、退款
- 🗄️ 数据完整性、事务、一致性
- 🛡️ 安全红线 R1-R5（密钥、SQL 注入、XSS、错误处理、审计）

**v3.2 非关键路径（可简化）：**
- 🟢 UI 组件（按钮、表单、列表）
- 🟢 一次性脚本、批处理
- 🟢 原型、演示项目
- 🟢 性能优化（明确标 TODO）

### 8.3 不可变原则的 v3.2 软化

**v3.1 红线（删除）：**
- ❌ 禁止所有 `.push()`、`.splice()`、原地 mutation

**v3.2 软性建议（保留但软化）：**
- 🟡 业务核心、状态管理 → 推荐不可变
- 🟡 React/Redux/Zustand → 推荐不可变
- 🟢 高性能循环、大数据处理 → 可用 `.push()`（性能优先）
- 🟢 原生 API 桥接（DOM 操作、Canvas）→ 可用原地修改（API 限制）

**判断原则：**
```markdown
问：这个 mutation 会影响其他模块吗？
├─ 否（局部变量、临时数据）→ 🟢 允许
├─ 是（共享状态、跨模块数据）→ 🟡 推荐不可变
└─ 不确定 → 默认不可变
```

### 8.4 TDD 原则的 v3.2 软化

**v3.1 红线（删除）：**
- ❌ 强制 TDD（RED → GREEN → IMPROVE）
- ❌ 85% 覆盖率硬卡

**v3.2 软性建议（保留但软化）：**
- ✅ 关键路径必须有测试
- ✅ 库/SDK/公开 API 必须有测试
- 🟡 业务逻辑推荐有测试
- 🟢 UI 组件、一次性脚本、原型 → 可有可无

**v3.2 紧急情况处理：**
- 🔴 线上事故修复 → 可先 hotfix 后补测试
- 🟡 紧急功能交付 → 可先实现后补测试（v3.2 允许）
- 🟢 原型/演示 → 手动测试即可

### 8.5 阶段 4 反模式（v3.2 新增）

**AP-16 规范过度严苛：** 阶段 4 强制不可变、强制 TDD、强制文件行数 → 800 行单文件桌面 GUI 被强制拆分为 5 个文件

**AP-17 轻量即正义：** AI 调研时以"不够轻量"为由删除 2-3 个有价值方案 → 用户选择空间被压缩

**AP-21 不可变教条：** 性能敏感代码也被强制不可变 → 性能下降

**AP-22 TDD 教条：** 原型也被强制 TDD → 开发效率下降

### 8.6 阶段 4 的 v3.2 决策树

```
Q: 这次编码应该多严？
A:
  ├─ 关键路径（认证/支付/数据）→ 完整 TDD + 不可变 + 业务分层
  ├─ 业务核心 → 推荐 TDD + 不可变
  ├─ 业务普通 → 软性建议（不强求）
  └─ 原型/演示/UI → 极简（手动测试）
```

### 8.7 v3.2 阶段 4 核心判断

```markdown
Q: 编码规范应该多严？
A: 取决于 3 个问题：
  1. 是否关键路径？（认证/支付 → 严格；UI/原型 → 宽松）
  2. 是否性能敏感？（大数据/Canvas → 允许原地修改）
  3. 是否长期项目？（库/SDK → 严格；一次性脚本 → 宽松）
```

> **v3.2 哲学转变：** 规范是参考书，不是宪法。开发者判断 > 死规则。

# AI Agent 配置文件模板（v3.2 · 极简化 + 项目类型适配）

> **v3.2 关键变化：** 移除 v3.1 的"≤ 150 行硬卡"和"4 段式"强制结构。本模板是**参考**，可按项目需要扩展。
> **使用建议：** 复制到项目根目录作为 `AGENTS.md`，根据**项目类型**（Web/桌面/Mobile/API/CLI）选择对应章节展开。
> **核心哲学：** 内容质量 > 字数控制；功能优先 > 字面合规。

---

## 🎯 快速选择：根据项目类型加载

| 项目类型 | 加载模板 | 关键决策点 |
|---------|---------|----------|
| 🌐 **Web 前端 / 全栈** | `templates/agents-web.md` | 状态管理、SSR/CSR、表单 |
| 🖥️ **桌面应用** | `templates/agents-desktop.md` | Electron vs Tauri、IPC 安全、离线存储 |
| 📱 **移动端 App** | `templates/agents-mobile.md` | 跨平台方案、原生模块、离线同步 |
| 🔌 **API 服务** | `templates/agents-api.md` | 框架选型、ORM、认证、限流 |
| ⚙️ **CLI 工具** | `templates/agents-cli.md` | 命令分发、配置层、错误处理 |

> **v3.2 核心理念：** 不同项目类型有不同的最佳实践，AI 必须**先识别项目类型**再决定规范应用强度。

---

## 通用模板（所有项目类型的基础结构）

```markdown
# {项目名称} — AI Agent 工作指南

> **项目类型：** {Web / 桌面 / Mobile / API / CLI}
> **技术栈：** {Next.js 14 + FastAPI + PostgreSQL / Electron + React / RN + Expo / FastAPI / Commander}
> **本文件用途：** AI Agent 快速理解项目，按场景加载对应规范
> **本文件不限制行数**（v3.2 软化），详细内容按需扩展

---

## 1. Project Overview

- **名称：** {项目名称}
- **类型：** {Web / Desktop / Mobile / API / CLI}
- **技术栈：** {详细技术选型}
- **包管理：** {pnpm / uv / npm}
- **部署：** {Docker / Vercel / App Store / PyPI}
- **目标用户：** {描述}

---

## 2. Build & Test Commands

> **v3.2 软化：** 以下命令按项目类型调整，不必全有。

\`\`\`bash
# 安装依赖
{pnpm install / uv sync / flutter pub get}

# 开发服务器
{pnpm dev / uv run python main.py / flutter run}

# 测试（关键路径推荐）
{pnpm test / uv run pytest / flutter test}

# 代码质量（软性建议）
{pnpm lint / uv run ruff check / flutter analyze}

# 类型检查
{pnpm typecheck / uv run mypy / dart analyze}

# 生产构建（agent 会话中谨慎使用）
{pnpm build / uv build / flutter build}
\`\`\`

---

## 3. Key Conventions

> **v3.2 软化：** 这里是项目**特有**的约定，不是通用规范。

### 3.1 安全红线（v3.2 硬性保留 · R1-R5）

- ❌ 禁止硬编码密钥、密码、Token
- ❌ 所有用户输入必须验证和净化（XSS/SQL 注入/路径穿越）
- ❌ API 响应不得泄露 stack trace、内网 IP、DB 结构
- ❌ 数据库操作必须参数化查询
- ❌ 敏感操作必须有审计日志

### 3.2 项目特定约定

- **{项目特有的命名/组织约定}**
- **{项目特有的业务规则}**
- **{项目特有的依赖版本约束}**

---

## 4. 规范应用强度（v3.2 新增 · 按项目类型决定）

> **v3.2 关键：** 不要用"通用规范"去要求所有项目。**按项目类型调整**：

| 规范 | Web/全栈 | 桌面 | Mobile | API | CLI |
|------|---------|------|--------|-----|-----|
| 文件行数限制 | 🟡 软性（业务可 1500 行） | 🟡 软性 | 🟡 软性 | 🟡 软性 | 🟢 不卡 |
| 覆盖率 | 🟡 60% 推荐 | 🟡 关键路径 | 🟡 关键路径 | 🟡 70% 推荐 | 🟢 不要求 |
| 业务逻辑分层 | 🟡 软性 | 🟡 软性 | 🟡 软性 | ✅ 推荐 | 🟢 不要求 |
| TDD 严格度 | 🟡 关键路径 | 🟡 关键路径 | 🟡 关键路径 | 🟡 关键路径 | 🟢 不要求 |
| 不可变性 | 🟡 推荐 | 🟡 推荐 | 🟡 推荐 | 🟡 推荐 | 🟢 不要求 |
| PR 模板 | 🟡 软性 | 🟡 软性 | 🟡 软性 | 🟡 软性 | 🟢 不要求 |
| Assisted-by trailer | 🟡 软性 | 🟡 软性 | 🟡 软性 | 🟡 软性 | 🟢 不要求 |

> **🟡 = 软性建议 · 🟢 = 不要求 · ✅ = 强烈推荐**

---

## 5. 关键决策记录

> **v3.2 软化：** 记录项目级技术决策，不是规范要求。

- **YYYY-MM-DD：** 决定 X，理由 Y
- **YYYY-MM-DD：** 选择 Z 而非 W，因为 ...

---

## 6. 反模式提醒（v3.2 新增）

- 🚫 **AP-16 规范过度严苛：** 不要为了合规而牺牲功能
- 🚫 **AP-17 轻量即正义：** 调研时不要以"不够轻量"为由删方案
- 🚫 **AP-14 Mock 滥用：** 单元测试不要 Mock 3+ 依赖
- 🚫 **AP-9 范围蔓延：** 只做要求做的，不顺手重构无关代码

---

## 7. References（按需链接）

- **项目详细文档：** `docs/`
- **架构决策记录：** `docs/adr/`
- **学习记录：** `.learnings/`
- **AI 规范：** `~/.claude/skills/ai-dev-workflow/SKILL.md`（v3.2 减法重构版）
```

---

## 5 种项目类型模板（按需展开）

### 🌐 Web 前端 / 全栈（`agents-web.md`）

```markdown
## Web 项目特定规范

### 状态管理
- 简单状态：useState / useReducer
- 跨组件：Zustand / Jotai（轻量）
- 复杂应用：Redux Toolkit
- 服务端状态：TanStack Query / SWR

### 表单
- react-hook-form + zod 验证
- 错误信息友好提示

### 样式
- Tailwind / CSS Modules / styled-components（按团队）
- 禁止内联样式（除动态样式）

### 路由
- Next.js App Router（约定优于配置）
- React Router 6+（配置式）

### 数据获取
- 优先 SWR / TanStack Query（缓存、乐观更新）
- axios / fetch 包装一层

### SSR/CSR 决策
- SEO 关键页：SSG/ISR
- 实时数据：CSR
- 大量用户数据：SSR + hydration

### Web 特定安全
- XSS：禁止 dangerouslySetInnerHTML
- CSRF：Token 验证
- CSP：设置 Content-Security-Policy header
```

### 🖥️ 桌面应用（`agents-desktop.md`）

```markdown
## 桌面项目特定规范

### 框架选型
- 体积敏感 → Tauri（Rust 后端，体积小）
- 生态成熟 → Electron（Node.js）
- 跨端一致 → Flet（Python）

### 安全红线（Electron 特有）
- ❌ 禁用 nodeIntegration（必须 contextIsolation）
- ❌ 禁用 enableRemoteModule
- ✅ preload 脚本最小化
- ✅ 所有 IPC 通信用 contextBridge

### 窗口管理
- 单窗口应用：简单 main process
- 多窗口：BrowserWindow pool
- 系统托盘：可选功能

### 离线存储
- 小数据：electron-store / tauri-plugin-store
- 大数据：SQLite (better-sqlite3)
- 同步：自定义 sync service

### 自动更新
- Electron：electron-updater
- Tauri：tauri-plugin-updater
- 版本检查策略

### 打包分发
- Electron：electron-builder
- Tauri：内置打包
- 代码签名（macOS/Windows 必需）
```

### 📱 移动端 App（`agents-mobile.md`）

```markdown
## 移动项目特定规范

### 跨平台方案
- React Native + Expo：JS 生态、迭代快
- Flutter：性能好、UI 一致
- 原生 (Swift/Kotlin)：性能最佳

### 导航
- React Navigation
- Flutter Navigator 2.0
- 路由参数类型化

### 状态管理
- Redux Toolkit / Zustand（RN）
- Riverpod / Bloc（Flutter）
- Provider（Flutter 简单状态）

### 离线同步
- AsyncStorage (RN) / SharedPreferences (Flutter)
- SQLite: react-native-sqlite-storage / sqflite
- 冲突解决：last-write-wins 或 CRDT

### 平台适配
- iOS HIG / Material Design 3
- 状态栏、安全区域、键盘
- 推送：APNs / FCM

### 性能
- 列表虚拟化（FlatList / ListView.builder）
- 图片缓存（FastImage / cached_network_image）
- 避免大列表 setState

### 发布
- App Store / Google Play
- TestFlight / Internal Testing
- 隐私政策、权限说明
```

### 🔌 API 服务（`agents-api.md`）

```markdown
## API 项目特定规范

### 框架选型
- Python：FastAPI（异步、自动文档）
- Node.js：Express / Fastify / Hono
- Go：Gin / Echo / Fiber
- Rust：Axum / Actix

### 路由设计
- RESTful 资源命名
- 版本：/api/v1/...
- 限流：每 IP/用户配额

### 数据验证
- FastAPI：Pydantic
- Express：zod / joi
- Gin：binding tag

### 错误处理
- 统一错误格式：{code, message, details}
- 4xx vs 5xx 区分
- 不泄露 stack trace（生产环境）

### 认证授权
- JWT（无状态）
- OAuth2（第三方登录）
- Session（传统 Web）
- RBAC 角色权限

### 数据库
- ORM：SQLAlchemy / Prisma / GORM
- Migration：Alembic / Prisma Migrate / golang-migrate
- 连接池配置
- 慢查询监控

### 文档
- OpenAPI / Swagger（自动生成）
- Postman 集合（团队共享）
- README 示例

### 部署
- Docker + docker-compose
- K8s（生产）
- Serverless（轻量 API）
- 反向代理：Nginx / Caddy
```

### ⚙️ CLI 工具（`agents-cli.md`）

```markdown
## CLI 项目特定规范

### 框架选型
- Node.js：Commander.js / yargs
- Python：Click / Typer
- Go：Cobra
- Rust：clap

### v3.2 重要：CLI 不必严格分层！
- 单文件 500-1000 行的 CLI 完全可接受
- 业务逻辑与命令可以共存
- 重点是**易用性**和**错误提示**

### 命令组织
- 一个命令一个文件（复杂 CLI）
- 单文件 main.go（简单 CLI）
- 子命令分层：cli / git / cli git commit

### 配置层
1. 命令行参数（最高优先级）
2. 环境变量
3. 配置文件（最低优先级）

### 错误处理
- 友好错误信息：不要 "Error: ENOENT"
- 退出码：0 成功 / 1 一般错误 / 2 参数错误
- 详细日志：--verbose / --debug

### 输出格式
- 默认人类可读（彩色）
- --json 机器可读
- --quiet 静默
- 进度条：长任务用 ora / indicatif

### 分发
- npm / PyPI / Homebrew
- 二进制（Go/Rust）
- 自动更新（可选）

### 安全
- 路径穿越：path.resolve 后检查
- 命令注入：避免 shell=true
- 配置文件权限检查
```

---

## v3.2 vs v3.1 模板变化总结

| 维度 | v3.1 | v3.2 |
|------|------|------|
| 行数限制 | ≤ 150 行硬卡 | 🟡 软性（不限制） |
| 结构 | 4 段式强制 | 灵活，参考即可 |
| 项目类型 | 单一模板 | **5 种差异化模板** |
| 规范应用强度 | 一视同仁 | **按项目类型分级表** |
| 业务分层 | 强制 core/cli | 🟡 软性（CLI 工具豁免） |
| 反模式 | 10 个通用 | **+AP-16/17 项目类型相关** |

---

## v3.5 增量：审查规则块（借鉴 Qoder 风格）

> **v3.5 新增原因：** v3.2 AGENTS.md 模板告诉 AI "怎么开发"，但没告诉 AI "开发完要怎么自检"和"AI Code Review 要查什么"。v3.5 借鉴阿里 Qoder 的 [qoder-action](https://github.com/QoderAI/qoder-action) AGENTS.md 模板，新增 4 条**硬规则**，每条都必须落到证据状态（0.2.7）。

### 必加 4 条审查硬规则

在 AGENTS.md 末尾追加以下块（v3.5 标准）：

```markdown
---

## 审查规则块（v3.5 · AI Code Review 自动检查项）

> **本块用于：** AI Agent / Code Reviewer / pre-commit hook / CI workflow 共同遵守
> **4 条硬规则来源：** 借鉴 Qoder qoder-action + OWASP Top 10 + ai-dev-workflow v3.5
> **违反任一条：阻塞合并**

### R-AUDIT-01：参数化查询（防 SQL 注入）

```typescript
// ❌ 禁止字符串拼接
db.exec(`SELECT * FROM users WHERE id = ${id}`)

// ✅ 必须参数化
db.prepare('SELECT * FROM users WHERE id = ?').get(id)
```

**检测：** `rg "exec\(`.*\\$\\{" --type ts --type py` + `rg "execute\(`.*\\+" --type py`
**关联：** ERR-SEC-02, OWASP A03

### R-AUDIT-02：API 授权检查（防越权）

```typescript
// ❌ 禁止无授权检查的端点
app.get('/api/users/:id', getUserHandler)

// ✅ 必须中间件验证 + 资源所有者检查
app.get('/api/users/:id', authMiddleware, requireOwner, getUserHandler)
```

**检测：** 审查所有 `app.get/post/put/delete` 后是否有 `authMiddleware` / `requireRole` / `requireOwner`
**关联：** ERR-SEC-04, OWASP A01

### R-AUDIT-03：敏感信息处理（防泄露）

```typescript
// ❌ 禁止硬编码 + 禁止明文日志
const apiKey = 'sk-12345'
console.log('Using key:', apiKey)

// ✅ 必须加密存储 + 脱敏日志
import { safeStorage } from 'electron'
const encrypted = safeStorage.encryptString(apiKey)
logger.info('Using key:', maskKey(apiKey))
```

**检测：** `rg "(api[_-]?key|token|password|secret)\\s*[:=]\\s*['\\\"]" --type ts --type py` + `gitleaks detect`
**关联：** ERR-SEC-01, OWASP A02

### R-AUDIT-04：输入验证（防 XSS / 路径穿越）

```typescript
// ❌ 禁止直接使用用户输入
res.send(html`${userInput}`)
fs.readFile(path.join(uploadDir, filename))  // filename 可包含 '../'

// ✅ 必须转义 + 路径归一化
import DOMPurify from 'isomorphic-dompurify'
res.send(DOMPurify.sanitize(html`${userInput}`))
const safePath = path.resolve(uploadDir, filename)
if (!safePath.startsWith(path.resolve(uploadDir))) throw new Error('Path traversal')
```

**检测：** 审查所有 user input 流（HTTP body / query / IPC / file upload）
**关联：** ERR-SEC-04, OWASP A03

### 审查规则执行机制

| 层级 | 谁执行 | 怎么执行 | 失败处理 |
|------|--------|---------|---------|
| **L0 单测** | 开发者 | 写代码时自检 | 必须改 |
| **L1 提交** | pre-commit hook | `scripts/audit.sh` | 阻塞提交 |
| **L2 PR** | AI Code Review | 扫 4 条规则 | 阻塞合并 |
| **L3 CI** | GitHub Actions | 每周全量审计 | 邮件告警 |

### 4 条规则的"证据状态"声明（0.2.7）

每次完成涉及这 4 条规则的代码时，commit message 必须包含：

```text
[AUDIT-Evidence]
- R-AUDIT-01: [Wired] 在 src/services/user.ts:42 用了 prepared statement
- R-AUDIT-02: [Exercised] 跑了越权测试用例，403 验证通过
- R-AUDIT-03: [Present] safeStorage 调用已加，未跑脱敏日志测试
- R-AUDIT-04: [Outcome-supported] 路径穿越测试 + 修，后续 PR 引用
```

**反模式（v3.5 必查）：**
- ❌ "代码改完了"（无证据状态标注）→ 阻塞合并
- ❌ "[Present]" 状态宣称"已修复" → 退回要求补证据
- ❌ R-AUDIT-04 缺失 → 安全审查直接拒绝
- ✅ "[Exercised] 越权测试 403 验证通过 + 截图" → 接受合并
```

### 项目类型与审查规则的关系

| 项目类型 | R-AUDIT-01 SQL | R-AUDIT-02 Auth | R-AUDIT-03 Secret | R-AUDIT-04 Input |
|---------|---------------|----------------|-----------------|-----------------|
| **Web 全栈** | ✅ 必查 | ✅ 必查 | ✅ 必查 | ✅ 必查 |
| **桌面应用** | ✅ 必查 | 🟡 IPC 必查 | ✅ 必查 | ✅ 必查 |
| **Mobile** | 🟡 视情况 | ✅ 必查 | ✅ 必查 | ✅ 必查 |
| **API 服务** | ✅ 必查 | ✅ 必查 | ✅ 必查 | ✅ 必查 |
| **CLI 工具** | ❌ 通常无 DB | 🟡 视情况 | 🟡 视情况 | ✅ 路径必查 |
| **纯库/SDK** | ❌ 通常无 DB | ❌ 通常无 API | ❌ 通常无 secret | 🟡 视情况 |

---

## v3.5 vs v3.2 模板变化总结

| 维度 | v3.2 | v3.5 |
|------|------|------|
| 行数限制 | 🟡 软性（不限制）| 🟡 软性（不限制）|
| 项目类型 | 5 种差异化 | 5 种 + 审查规则块 |
| 审查产出 | 自由格式 | **4 条硬规则 + 证据状态** |
| 安全 | 通用提及 | **R-AUDIT-01/02/03/04 硬规则** |
| 经验沉淀 | 无 | 🟡 经验被复用率指标（0.5.5）|

## v3.6 增量：可执行审计脚本（从文档到工具的闭环）

> **v3.6 新增原因：** v3.5 给了 4 条 R-AUDIT 硬规则和 0.5.5 经验被复用率公式，但**它们都是文档**——没人会每次手动跑。v3.6 提供 2 个可执行脚本（`audit.sh` + `learnings-summary.sh`），挂到 pre-commit / CI 即可机械拒绝。

### scripts/audit.sh · 4 条 R-AUDIT 自动扫描

**用法：**
```bash
# 跑全部
./scripts/audit.sh

# 跑某一条
./scripts/audit.sh --rule 01   # 只查 SQL 注入
./scripts/audit.sh --rule 03   # 只查敏感信息

# 输出 JSON（CI 用）
./scripts/audit.sh --json

# 按严重度过滤
./scripts/audit.sh --severity high
```

**退出码语义：**
| 退出码 | 含义 | 处置 |
|-------|------|------|
| 0 | 全部通过 | 允许合并 |
| 1 | 发现 HIGH 级别 | **阻塞合并**（必须修）|
| 2 | 发现 MEDIUM 级别 | 警告，建议修 |

**挂到 pre-commit（v3.6 推荐）：**

在 `.pre-commit-config.yaml` 追加：

```yaml
repos:
  - repo: local
    hooks:
      - id: r-audit
        name: R-AUDIT-01~04 security scan
        entry: bash scripts/audit.sh
        language: system
        types: [file]
        files: '\.(ts|tsx|js|jsx|py|go)$'
        pass_filenames: false
```

**挂到 GitHub Actions（v3.6 推荐）：**

```yaml
name: R-AUDIT security scan
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run R-AUDIT
        run: bash scripts/audit.sh --json > audit.json || EXIT=$?
      - name: Upload findings
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: audit-findings
          path: audit.json
      - name: Fail on HIGH
        run: test "${EXIT:-0}" -ne 1
```

### scripts/learnings-summary.sh · 经验被复用率自动汇总

**用法：**
```bash
# 手动跑
./scripts/learnings-summary.sh

# 自动写入 index.md
./scripts/learnings-summary.sh --auto-month

# JSON 输出
./scripts/learnings-summary.sh --json
```

**退出码语义：**
| 退出码 | 含义 | 处置 |
|-------|------|------|
| 0 | 健康（腐化率 ≤ 50%）| 正常 |
| 1 | 找不到 .learnings 目录 | 创建目录后重跑 |
| 2 | 腐化率 > 50% | **必须季度回顾** |

**挂到 GitHub Actions（每月 1 号）：**

```yaml
name: Monthly learnings summary
on:
  schedule:
    - cron: '0 0 1 * *'  # 每月 1 号 0 点
jobs:
  summary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run summary
        run: bash scripts/learnings-summary.sh --auto-month
      - name: Commit index
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "actions@github.com"
          git add .learnings/index.md
          git commit -m "chore: monthly learnings summary" || true
          git push
```

### v3.6 vs v3.5 模板变化

| 维度 | v3.5 | v3.6 |
|------|------|------|
| R-AUDIT | 文档说明 | **audit.sh 脚本机械执行** |
| 经验沉淀 | 公式 + 文档 | **learnings-summary.sh 自动汇总** |
| pre-commit | 通用配置 | **+ audit.sh 钩子模板** |
| CI | 通用检查 | **+ audit.sh --json + 退出码 1 阻塞** |

---

> **v3.2 模板哲学：** AGENTS.md 是给 AI Agent 看的**项目地图**，不是产品文档。重点是**让 AI 快速理解项目类型和规范应用强度**，而不是面面俱到。
>
> **v3.5 模板哲学新增：** AGENTS.md 末尾的**审查规则块**是 AI Code Review 的"硬性检查清单"——开发者 + AI 共同遵守，违反阻塞合并。这是从"项目地图"升级为"项目宪法"。

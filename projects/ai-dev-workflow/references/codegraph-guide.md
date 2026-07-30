# CodeGraph 使用教程 — 给 AI Agent 一张代码地图

> 适用版本：v1.1.x+ | 官方文档：https://colbymchenry.github.io/codegraph/
> GitHub：https://github.com/colbymchenry/codegraph | npm：@colbymchenry/codegraph

---

## 一、为什么需要 CodeGraph

### 问题：AI Agent 「盲人摸象」

当你问 AI Agent "auth 中间件怎么验证 JWT？"时，它没有代码地图，只能：

```
grep "JWT" → 200 行结果 → Read auth.ts → Read middleware.ts → grep "verify" → ...
```

1000 个文件的项目，回答一个问题可能烧 15-30 次工具调用。**文件越多，浪费越严重。**

### 方案：提前建图，查图不扫文件

CodeGraph 把代码库预解析成**符号关系图谱**：函数、类、路由、组件是节点，调用关系、导入依赖是边。Agent 不扫文件，直接查图。

**7 个真实开源项目实测（Claude Opus 4.8，v0.9.9）：**

| 项目 | 文件数 | Token 降幅 | 工具调用降幅 | API 费用降幅 |
|------|--------|-----------|-------------|-------------|
| VS Code | ~10,000 | **-64%** | **-81%** | -18% |
| Django | ~3,000 | -47% | -58% | -16% |
| **7 项目中位数** | various | **-47%** | **-58%** | **-16%** |

---

## 二、安装

### 方式一：直接下载（推荐，无需 Node.js）

```powershell
# Windows PowerShell
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
```

自带运行时，无需编译，无需 Node.js。关掉当前终端，开新终端即可使用 `codegraph` 命令。

### 方式二：npm 安装（已有 Node.js 时更轻量）

```bash
npm i -g @colbymchenry/codegraph
```

### 方式三：npx 零安装体验

```bash
npx @colbymchenry/codegraph
```

### 升级

```bash
codegraph upgrade            # 自动检测安装方式并更新
codegraph upgrade --check    # 仅检查是否有新版本
codegraph upgrade 1.2.0      # 指定版本
```

### 卸载

```bash
codegraph uninstall          # 从所有 agent 移除 MCP 配置（.codegraph/ 目录不删）
codegraph uninit             # 删除项目的 .codegraph/ 目录
```

---

## 三、三分钟上手

### Step 1：安装 CLI（上面三选一）

### Step 2：注册到 AI Agent

```bash
codegraph install
```

自动检测并配置 **Claude Code、Cursor、Codex CLI、Gemini CLI、opencode、Hermes Agent、Antigravity、Kiro**。

`install` 只接线不建图——把 MCP 服务器配置写入各 Agent 的设置文件。

### Step 3：初始化项目

```bash
cd your-project
codegraph init
```

`init` = 创建 `.codegraph/` 目录 + 全量索引，一个命令搞定。

### Step 4：无需再同步

Auto-sync 默认开启。文件改动自动增量索引（2 秒防抖），**索引永不落后**。

---

## 四、核心概念

### 知识图谱结构

| 概念 | 说明 | 示例 |
|------|------|------|
| **节点** | 代码符号 | `function createUser`、`class UserService`、`route GET /api/users` |
| **边** | 符号间关系 | `createUser` 调用 `hashPassword`、`UserService` 导入 `Database` |
| **图谱** | 全部节点+边 | 存在 `.codegraph/codegraph.db`（SQLite） |

### 节点类型（10+ 种）

| 类型 | 说明 |
|------|------|
| `function` | 独立函数 |
| `method` | 类方法 |
| `class` | 类 |
| `interface` | 接口 |
| `component` | Vue/React 组件 |
| `route` | 框架路由 |
| `variable` / `constant` | 变量与常量 |
| `import` | 导入依赖 |
| `field` | 类字段 |
| `type_alias` | 类型别名 |
| `enum` / `enum_member` | 枚举及成员 |

### 数据流水线

```
源文件
  │
  ▼
tree-sitter 解析 AST  ← 20+ 语言原生支持
  │
  ▼
SQLite + FTS5 全文搜索  ← .codegraph/codegraph.db
  │
  ▼
MCP Server 暴露工具     ← AI Agent 通过 MCP 协议查图
```

### 动态调度桥接

不是靠名字猜调用关系。识别虚函数、接口实现、依赖注入绑定等动态调度路径——**grep 绝对做不到**。

---

## 五、CLI 命令参考

### 基础命令

| 命令 | 说明 |
|------|------|
| `codegraph init` | 初始化 + 全量索引（一站式） |
| `codegraph index` | 重新全量索引 |
| `codegraph sync` | 增量更新 |
| `codegraph status` | 查看索引统计 |
| `codegraph install` | 接线到 AI Agent |
| `codegraph uninstall` | 断开所有 Agent |
| `codegraph upgrade` | 升级最新版本 |

### 查询命令

| 命令 | 说明 |
|------|------|
| `codegraph query <name>` | 搜索符号（如 `codegraph query UserService`） |
| `codegraph callers <name>` | 谁调用了它 |
| `codegraph callees <name>` | 它调用了谁 |
| `codegraph impact <name>` | 改动它的影响范围 |
| `codegraph trace <A> <B>` | A 到 B 的调用路径 |
| `codegraph context <task>` | 为 AI 任务构建上下文 |
| `codegraph explore <query>` | 多符号探索 |
| `codegraph files` | 文件结构概览 |

### `codegraph affected` — CI 利器

改代码前知道哪些测试会受影响：

```bash
# 看某个文件的改动影响哪些测试
codegraph affected src/auth/login.ts --quiet

# CI 中：只跑受影响的测试
#!/usr/bin/env bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
if [ -n "$AFFECTED" ]; then
  npx vitest run $AFFECTED
fi
```

---

## 六、MCP 工具详解

Agent 注册后可用的 10+ 个 MCP 工具：

| 工具 | 功能 | 适用场景 |
|------|------|---------|
| `codegraph_search` | 符号搜索 | 找某个函数/类定义在哪 |
| `codegraph_context` | 上下文构建 | SubAgent 启动时，一键获取入口点+相关符号+源码 |
| `codegraph_trace` | 调用链追踪 | 从请求入口追踪到目标函数 |
| `codegraph_callers` | 调用者查询 | 修改函数前，看谁在用它 |
| `codegraph_callees` | 被调用者查询 | 理解函数内部依赖 |
| `codegraph_impact` | 影响分析 | 改一动百？先看影响半径 |
| `codegraph_node` | 符号详情 | 查看完整签名、位置、类型 |
| `codegraph_explore` | 多符号探索 | SubAgent 需要全局视角时 |
| `codegraph_files` | 文件结构 | 了解项目目录布局 |
| `codegraph_status` | 索引状态 | 确认图谱是否最新 |

### 工具选用指南

```
想找某个符号的定义     → codegraph_search
想理解一个功能怎么做   → codegraph_context（SubAgent 首选）
想改函数前看影响       → codegraph_callers → codegraph_impact
想追踪请求完整链路     → codegraph_trace
想知道项目有多深       → codegraph_status
```

---

## 七、实战工作流

### 场景一：安全重构 — 改代码前先看影响

```bash
# 1. 看影响半径（深度 3 层）
codegraph impact TokenService --depth 3

# 2. 追踪关键调用路径
codegraph trace RequestHandler TokenService

# 3. 找到需要跑的测试
codegraph affected src/services/token.ts --quiet
```

### 场景二：AI Agent 接入 CI/CD

```yaml
# .github/workflows/ci.yml 中加
- name: CodeGraph affected tests
  run: |
    AFFECTED=$(git diff --name-only origin/main...HEAD | codegraph affected --stdin --quiet)
    if [ -n "$AFFECTED" ]; then
      npm test -- $AFFECTED
    fi
```

只跑受影响的测试，大幅缩短 CI 时间。

### 场景三：新人接手项目

```
codegraph status          # 了解全局：多少符号、多少文件
codegraph files           # 看目录结构
codegraph explore "auth"  # 以 auth 为入口探索模块
```

不用一个文件一个文件读，直接看图理解架构。

### 场景四：修复 Bug

```
用户报：POST /api/order 返回 500

Agent 调用 codegraph_trace("POST /api/order", "error")
       → 框架感知路由 → 找到 Handler → 追踪到出错的函数
       → codegraph_impact("brokenFunction")
       → 确认修复影响范围，安心改
```

---

## 八、支持的语言与框架

### 编程语言（20+）

TypeScript、JavaScript、Python、Go、Rust、Java、C#、PHP、Ruby、
C/C++、Swift、Kotlin、Scala、Dart、Svelte、Vue、Lua/Luau、Liquid、
Pascal/Delphi、Objective-C（部分）

### 框架路由识别（14+）

| 框架 | 识别内容 |
|------|---------|
| Next.js | App Router + Pages Router |
| Express | 显式路由 + Router 链 |
| FastAPI | 装饰器路由 + 依赖注入 |
| Django | URL patterns |
| Flask | @app.route |
| Gin (Go) | 路由注册 |
| Spring Boot | @RequestMapping |
| Laravel | routes/ 文件 |
| Ruby on Rails | config/routes.rb |
| Vue Router | route 定义 |
| React Router | Route 组件 |
| NestJS | @Controller 装饰器 |
| Nuxt | 文件路由 |
| SvelteKit | 文件路由 |

### 跨语言桥接

- **Swift ↔ ObjC**：追踪 bridging header
- **React Native Bridge**：JS 到原生模块的调用链
- **TurboModules**：C++ ↔ JS 异步桥接

---

## 九、自动同步机制

三层保障确保图谱永不落后：

| 层级 | 机制 | 触发条件 |
|------|------|---------|
| **第一层** | 文件监听 + 防抖自动同步 | 保存文件后 2 秒自动触发增量索引 |
| **第二层** | 文件过期提示横幅 | 检测到文件修改但索引未更新时，Agent 窗口顶部黄色提示 |
| **第三层** | 连接时追赶同步 | MCP Server 每次启动检查 `mtime`，自动追赶落后索引 |

**正常情况下用户无需手动执行任何同步命令。**

---

## 十、配置与调优

### .gitignore

`.codegraph/` 目录应加入 `.gitignore`：

```gitignore
# CodeGraph
.codegraph/
```

索引是本地产物，不应提交到版本库。

### 排除目录

`init` 时自动排除 `node_modules`、`dist`、`build`、`.git`，无需手动配置。

如需追加排除：

```bash
codegraph init --ignore generated,third_party
```

### 关闭自动同步

```bash
codegraph sync --off
```

重新开启：

```bash
codegraph sync --on
```

### 性能参考

| 项目规模 | 索引大小 | 首次索引时间 |
|---------|---------|-------------|
| ~100 文件 | ~2 MB | < 1 秒 |
| ~1,000 文件 | ~20 MB | ~5 秒 |
| ~10,000 文件（VS Code 级别） | ~200 MB | ~30 秒 |

增量更新 < 100ms（单文件改动）。

---

## 十一、常见问题

### Q: 数据安全吗？
**100% 本地。** 代码不过网络，图谱存在本地 SQLite 文件。零遥测、零上传。

### Q: 支持哪些 Agent？
Claude Code、Cursor、Codex CLI、Gemini CLI、opencode、Hermes Agent、Antigravity IDE、Kiro。`codegraph install` 自动检测并配置。

### Q: 低于 100 个文件的项目值得用吗？
收益不大。文件少时 Agent  grep + Read 开销本就不高，CodeGraph 的预建图优势体现不出来。

### Q: 更新某个文件后索引需要重建吗？
不需要。增量索引自动触发，只重解析改动的文件（及相关连边），通常 < 100ms。

### Q: 和 IDE 的「查找引用」有什么区别？
- IDE 查找引用：当前语言，当前编辑器，手动触发
- CodeGraph：跨语言（Bridge）、跨框架（路由→Handler）、Agent 可编程调用、可接入 CI

### Q: 能用于 .NET 项目吗？
CodeGraph（@colbymchenry）current 版本侧重 JS/TS/Python/Go 等，C# 支持有限。.NET 专项项目可用 [CodeGraph .NET 版](https://www.nuget.org/packages/CodeGraph/)（Roslyn 驱动）。

---

## 十二、与其他工具对比

| 工具 | 定位 | 优点 | 缺点 |
|------|------|------|------|
| **CodeGraph** | 通用代码图谱 CLI+MCP | 零配置、20+语言、Framework-aware、3 条命令 | C#/Java 支持不如专项工具 |
| Trailmark | 安全分析专用 | 污点传播、攻击面枚举、变异测试 | 重量级、偏安全 |
| GitNexus | 深度结构分析 | 社区检测、Process 流、Blast Radius | 重、非 MCP 原生 |
| Understand-Anything | 可视化+LLM | 交互仪表盘、15 平台 | 重 |
| Code-Graph (FalkorDB) | Neo4j 图数据库方案 | GraphRAG 聊天、Web UI | 需 Docker、仅 Python/Java/C# |

**推荐组合：CodeGraph（日常编码）+ Trailmark（安全审计）**

---

## 十三、快速参考卡

```
# 安装
irm https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex

# 接线到 Agent
codegraph install

# 项目初始化
cd my-project && codegraph init

# 日常查询
codegraph query UserService
codegraph callers createUser
codegraph impact TokenService --depth 3
codegraph trace App login

# 状态
codegraph status

# 升级
codegraph upgrade

# 卸载
codegraph uninstall
```

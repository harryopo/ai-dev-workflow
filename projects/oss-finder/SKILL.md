---
name: oss-finder
description: |
  开源项目搜索工具。跨 GitHub/GitLab/Gitee/npm/PyPI 搜索开源项目，支持 stars/language/topic 等筛选。
  当用户说"搜索开源项目"、"找开源实现"、"有哪些开源"、"开源推荐"、"find open source"、"search repos"时调用。
context: fork
agent: general-purpose
allowed-tools: Read Write Bash Glob Grep AskUserQuestion
---

# OSS Finder — 全网开源项目搜索

**先调研，再搜索。** 当用户提示词模糊时，先进行初步调研，理解用户真实需求，确认后再执行详细搜索。

## 核心原则

> **调研先行，精准搜索。**
>
> **七条铁律：**
> 1. **先理解再搜索** — 模糊提示词必须先调研，不能盲目搜索
> 2. **用户确认后执行** — 调研结果必须让用户确认，避免无意义搜索
> 3. **gh CLI 优先** — GitHub 搜索优先用 `gh search repos`（实时数据、无速率限制），不可用时降级到 REST API
> 4. **用 API 不用爬虫** — 所有平台使用官方 API/CLI，稳定快速不触发反爬
> 5. **GitHub 为主，其他为辅** — GitHub 数据最全，其他平台作为补充
> 6. **国内网络优先** — GitHub 超时时自动降级到 Gitee
> 7. **Token 可选** — 无 Token 也能用，有 Token 速率更高

---

## 工作流程

### 第一步：需求评估

从 `$ARGUMENTS` 中提取用户意图，判断是否需要调研：

**判断标准：**

| 提示词类型 | 示例 | 是否需要调研 |
|------------|------|--------------|
| **模糊/宽泛** | "react"、"python"、"web framework" | ✅ 需要 |
| **具体但缺参数** | "react table 组件" | ✅ 需要（缺 stars/language 等） |
| **完整明确** | "react table 组件 --stars >1000 --language typescript --limit 10" | ❌ 直接搜索 |

**模糊提示词特征：**
- 只有 1-2 个词
- 没有指定平台、语言、Stars 等筛选条件
- 没有明确的使用场景
- 可能有多种理解方式

### 第二步：初步调研（模糊提示词时）

当提示词模糊时，执行以下调研：

#### 2.1 关键词分析

分析用户提示词的可能含义：

```
用户输入："react"

可能的搜索方向：
1. **React 框架本身** — 核心库、官方工具
2. **React 生态** — 状态管理、路由、UI 组件库
3. **React 项目模板** — 脚手架、 starter kits
4. **React 学习资源** — 教程、示例、最佳实践
5. **React Native** — 移动端开发
```

#### 2.2 平台推荐

根据关键词特性推荐最佳平台：

| 关键词特征 | 推荐平台 | 原因 |
|------------|----------|------|
| 通用框架/库 | GitHub | 数据最全，Stars 筛选有效 |
| npm 包名 | npm | 内置评分系统，版本信息全 |
| Python 包名 | PyPI | 包详情丰富 |
| 国内项目 | Gitee | 中文项目多，访问快 |
| 企业/私有 | GitLab | 自建实例支持 |

#### 2.3 筛选条件推荐

根据关键词推荐筛选条件：

```
用户输入："python web framework"

推荐筛选：
- language: python
- topic: web, web-framework
- stars: >1000（主流方案）
- license: mit, apache-2.0（宽松许可证）
```

#### 2.4 生成调研报告

输出调研报告，让用户确认：

```markdown
## 📋 初步调研：{用户提示词}

### 识别的搜索方向

根据您的提示词 "{提示词}"，我识别到以下可能的搜索方向：

1. **方向 A：{描述}**
   - 关键词：{优化后的关键词}
   - 平台：{推荐平台}
   - 预期结果：{项目类型}

2. **方向 B：{描述}**
   - 关键词：{优化后的关键词}
   - 平台：{推荐平台}
   - 预期结果：{项目类型}

### 推荐搜索策略

- **主平台**：{平台}
- **关键词**：{关键词}
- **语言筛选**：{语言}
- **Stars 范围**：{范围}
- **Topic 标签**：{标签}
- **排序方式**：{排序}

### 预期结果

- **项目类型**：{类型}
- **数量估计**：{数量} 个
- **典型项目**：{示例}

---

请确认：
1. 以上哪个搜索方向符合您的需求？
2. 是否需要调整筛选条件？
3. 是否有其他特殊要求？
```

### 第三步：用户确认

使用 AskUserQuestion 让用户选择：

**问题 1：搜索方向**
- 方向 A：{描述}
- 方向 B：{描述}
- 自定义：用户输入自己的方向

**问题 2：筛选条件**
- 使用推荐的筛选条件
- 调整 Stars 范围
- 调整语言/Topic
- 不使用筛选

**问题 3：结果数量**
- 10 个（快速浏览）
- 20 个（标准）
- 50 个（详细）
- 自定义

### 第四步：检查环境和 Token

```bash
python --version

# 检查 gh CLI（GitHub 搜索首选方案）
if command -v gh &> /dev/null; then
  echo "✅ gh CLI 已安装"
  gh auth status 2>&1 | head -5
else
  echo "⚠️  gh CLI 未安装，将使用 REST API（建议安装：https://cli.github.com）"
fi

# 检查 Token（gh CLI 不可用时的降级方案）
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:+已设置}"
echo "GITLAB_TOKEN: ${GITLAB_TOKEN:+已设置}"
echo "GITEE_TOKEN: ${GITEE_TOKEN:+已设置}"
```

**gh CLI 配置（如未安装）：**

```bash
# Windows (winget)
winget install GitHub.cli

# 或 scoop
scoop install gh

# 认证
gh auth login
```

### 第五步：执行搜索

使用 `${CLAUDE_SKILL_DIR}/scripts/search.py` 执行搜索：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/search.py" \
  --query "搜索关键词" \
  --platform github \
  --language python \
  --stars ">1000" \
  --sort stars \
  --limit 20 \
  --format markdown
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词（必填，位置参数） | — |
| `--platform` | 平台：github/gitlab/gitee/npm/pypi/all | github |
| `--language` | 编程语言筛选 | 不限 |
| `--stars` | Stars 筛选，如 ">100"、"100..1000" | 不限 |
| `--topic` | Topic 标签筛选 | 不限 |
| `--license` | 许可证筛选，如 "mit"、"apache-2.0" | 不限 |
| `--created-after` | 创建日期筛选，如 "2024-01-01" | 不限 |
| `--sort` | 排序：stars/forks/updated/relevance | stars |
| `--order` | 排序方向：asc/desc | desc |
| `--limit` | 返回数量（gh CLI 最大 1000） | 20 |
| `--format` | 输出格式：markdown/json/table | markdown |
| `--save` | 保存结果到文件 | 否 |
| `--output` | 自定义输出目录 | output/oss-finder/ |
| `--no-cache` | 禁用缓存，强制实时搜索 | 否 |

**性能特性：**
- **gh CLI 优先** — GitHub 搜索自动使用 gh CLI（实时数据、无速率限制）
- **并发搜索** — `--platform all` 时 4 个平台并行请求，耗时 ~3s（串行需 ~12s）
- **本地缓存** — 相同查询 1 小时内直接返回缓存（缓存目录：`~/.cache/oss-finder/`）
- **自动重试** — 网络错误/5xx 自动重试 3 次（指数退避）
- **结果去重** — 跨平台搜索时自动按 URL 去重

### 第六步：输出结果

**Markdown 格式（默认）：**

```markdown
## 搜索结果：{关键词}

共找到 {N} 个项目（来源：GitHub）

| # | 项目 | Stars | Language | 描述 |
|---|------|-------|----------|------|
| 1 | [facebook/react](https://github.com/facebook/react) | 220k | JavaScript | A declarative, efficient... |
| 2 | [vuejs/vue](https://github.com/vuejs/vue) | 200k | JavaScript | Vue.js is a progressive... |
```

**JSON 格式：**

```json
{
  "query": "react",
  "platform": "github",
  "total": 11004,
  "results": [
    {
      "name": "facebook/react",
      "url": "https://github.com/facebook/react",
      "stars": 220000,
      "forks": 45000,
      "language": "JavaScript",
      "description": "A declarative, efficient...",
      "topics": ["react", "javascript", "frontend"],
      "license": "MIT",
      "updated_at": "2026-06-20T..."
    }
  ]
}
```

---

## 调研示例

### 示例 1：模糊提示词 → 调研 → 确认 → 搜索

**用户输入：** `/oss-finder react`

**调研报告：**

```markdown
## 📋 初步调研：react

### 识别的搜索方向

根据您的提示词 "react"，我识别到以下可能的搜索方向：

1. **方向 A：React 核心库**
   - 关键词：react
   - 平台：GitHub
   - 预期结果：React 框架本身、官方工具

2. **方向 B：React 状态管理**
   - 关键词：react state management
   - 平台：GitHub
   - 预期结果：Redux、MobX、Zustand 等状态管理库

3. **方向 C：React UI 组件库**
   - 关键词：react component library
   - 平台：GitHub
   - 预期结果：Ant Design、Material-UI、Chakra UI 等

4. **方向 D：React 项目模板**
   - 关键词：react starter template
   - 平台：GitHub
   - 预期结果：Create React App、Vite 模板等

### 推荐搜索策略

- **主平台**：GitHub
- **关键词**：react
- **语言筛选**：JavaScript/TypeScript
- **Stars 范围**：>1000（主流方案）
- **Topic 标签**：react, frontend
- **排序方式**：Stars 降序

### 预期结果

- **项目类型**：React 框架、生态库、组件库
- **数量估计**：100+ 个高质量项目
- **典型项目**：facebook/react, redux, ant-design
```

**用户确认后执行：**

```
/oss-finder react --stars ">1000" --language javascript --limit 20
```

### 示例 2：具体提示词 → 直接搜索

**用户输入：** `/oss-finder react table component --stars ">500" --language typescript --limit 10`

**直接执行搜索：**

```
python scripts/search.py "react table component" --stars ">500" --language typescript --limit 10
```

### 示例 3：npm 包搜索

**用户输入：** `/oss-finder date formatter`

**调研报告：**

```markdown
## 📋 初步调研：date formatter

### 识别的搜索方向

根据您的提示词 "date formatter"，我识别到以下可能的搜索方向：

1. **方向 A：JavaScript 日期格式化库**
   - 关键词：date formatter
   - 平台：npm
   - 预期结果：date-fns、dayjs、moment 等

2. **方向 B：Python 日期格式化库**
   - 关键词：python date formatter
   - 平台：PyPI
   - 预期结果：arrow、pendulum、python-dateutil 等

3. **方向 C：通用日期工具库**
   - 关键词：date utility
   - 平台：GitHub
   - 预期结果：跨语言的日期处理工具

### 推荐搜索策略

- **主平台**：npm
- **关键词**：date formatter
- **语言筛选**：JavaScript
- **排序方式**：relevance

### 预期结果

- **项目类型**：日期格式化、解析、工具库
- **数量估计**：50+ 个包
- **典型项目**：date-fns, dayjs, luxon
```

### 示例 4：跨平台并发搜索

**用户输入：** `/oss-finder python web framework --platform all --stars ">1000" --limit 10`

**执行：** 并发搜索 GitHub + GitLab + Gitee + npm，自动去重

```
🔍 并发搜索 4 个平台...
  ✅ github: 5 个结果
  ✅ npm: 5 个结果
  ⚠️  gitlab: 无结果
  ⚠️  gitee: 无结果
  🔄 去重: 10 → 8
```

### 示例 5：搜索 2025 年新项目

**用户输入：** `/oss-finder ai agent --language python --created-after "2025-01-01" --stars ">500" --limit 10`

**执行：** 搜索 2025 年 1 月 1 日后创建的 AI Agent 项目

```
python "${CLAUDE_SKILL_DIR}/scripts/search.py" "ai agent" --language python --created-after "2025-01-01" --stars ">500" --limit 10
```

### 示例 6：表格格式输出（适合终端）

**用户输入：** `/oss-finder react table --format table --limit 5`

**输出：**
```
搜索结果：react table
共找到 5 个项目（来源：github）

  #  项目                               Stars  Language      描述
---  ----------------------------------  ----------  ------------  ----
  1  TanStack/table                      28.1k  TypeScript    Headless UI for building powerful tables
  2  KevinVandy/material-react-table      1.8k  TypeScript    A fully featured Material UI V5 impl...
```

---

## 平台特定说明

### GitHub（默认，数据最全）

**优先使用 gh CLI（实时数据）：**

```bash
gh search repos "react" --stars ">1000" --language javascript --limit 20 --json fullName,stargazersCount,description
```

**gh CLI 优势：**
- 实时数据（REST API 有缓存延迟）
- 无速率限制（使用 Token 配额，search API 30次/分钟）
- 更丰富的筛选参数

**降级方案：REST API**

`https://api.github.com/search/repositories`

**搜索语法：**
- `stars:>1000` — Stars 大于 1000
- `language:python` — Python 语言
- `topic:machine-learning` — 包含 topic
- `license:mit` — MIT 许可证
- `created:>2024-01-01` — 2024 年后创建
- 组合：`stars:>1000 language:python topic:ml`

**Token 配置：**
- 未认证：10 次/分钟（search API）
- 设置 `GITHUB_TOKEN`：30 次/分钟
- gh CLI：使用 `gh auth login` 配置，自动管理 Token

### GitLab（企业/私有项目）

**API：** `https://gitlab.com/api/v4/projects`

**限制：**
- 搜索语法不如 GitHub 丰富
- 不支持 `stars:>N` 范围查询
- `language` 字段经常为 null

**Token 配置：**
- 设置 `GITLAB_TOKEN` 突破速率限制

### Gitee（国内项目补充）

**API：** `https://gitee.com/api/v5/search/repositories`

**特点：**
- 国内访问速度快
- 中文项目多
- 未认证搜索可能返回空结果

**Token 配置：**
- 设置 `GITEE_TOKEN` 获取有效结果

### npm（Node.js 包搜索）

**API：** `https://registry.npmjs.org/-/v1/search`

**特点：**
- 不需要认证
- 内置评分系统（quality/popularity/maintenance）
- 只搜索包，不搜索仓库

### PyPI（Python 包查询）

**API：** `https://pypi.org/pypi/{package}/json`

**限制：**
- **没有搜索 API**，只能按包名精确查询
- 用于获取包详情，不是搜索

---

## 降级策略

当 GitHub 不可用时：

```
GitHub 超时/失败
  ↓
尝试 GitLab.com
  ↓
尝试 Gitee
  ↓
返回部分结果 + 提示
```

---

## 输出目录

搜索结果保存到：
```
output/oss-finder/
├── {query}-{timestamp}.json    # 原始 JSON
├── {query}-{timestamp}.md      # Markdown 报告
└── latest.json                 # 最新结果软链接
```

---

## 禁止行为

- ❌ **禁止跳过调研直接搜索** — 模糊提示词必须先调研
- ❌ **禁止不确认就执行** — 调研结果必须让用户确认
- ❌ **禁止使用爬虫** — 必须使用官方 API
- ❌ **禁止高频请求** — 遵守各平台速率限制
- ❌ **禁止忽略错误** — API 失败必须记录并提示
- ❌ **禁止伪造数据** — 只返回 API 真实数据
- ❌ **禁止硬编码 Token** — Token 从环境变量读取

---

## 参考资料

- GitHub API：`${CLAUDE_SKILL_DIR}/references/github-api.md`
- GitLab API：`${CLAUDE_SKILL_DIR}/references/gitlab-api.md`
- Gitee API：`${CLAUDE_SKILL_DIR}/references/gitee-api.md`
- npm API：`${CLAUDE_SKILL_DIR}/references/npm-api.md`

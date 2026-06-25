# OSS Finder — 全网开源项目搜索工具

**先调研，再搜索。** 当用户提示词模糊时，先进行初步调研，理解用户真实需求，确认后再执行详细搜索。

## 功能特性

- **智能调研** — 模糊提示词先调研，确认后再搜索
- **多平台搜索** — GitHub、GitLab、Gitee、npm、PyPI
- **智能筛选** — 按 Stars、语言、Topic、许可证筛选
- **灵活排序** — 按 Stars、Forks、更新时间排序
- **多种输出** — Markdown 表格、JSON 格式
- **结果保存** — 支持保存到文件
- **Token 可选** — 无 Token 也能用，有 Token 速率更高

## 快速开始

### 智能调研模式（推荐）

当提示词模糊时，Skill 会自动进行调研：

```
# 模糊提示词 → 自动调研 → 用户确认 → 执行搜索
/oss-finder react
/oss-finder python web
/oss-finder date formatter
```

**调研流程：**
1. 分析用户意图，识别搜索方向
2. 推荐平台、筛选条件、排序方式
3. 输出调研报告，让用户确认
4. 用户确认后执行详细搜索

### 直接搜索模式

当提示词明确时，直接执行搜索：

```bash
# 完整参数 → 直接搜索
/oss-finder react table --stars ">1000" --language typescript --limit 10

# 命令行调用
python scripts/search.py "python web framework"
python scripts/search.py "react component library" --topic react --stars ">500"
python scripts/search.py "date formatter" --platform npm
```

### 高级筛选

```bash
# 按 Stars 筛选
python scripts/search.py "machine learning" --stars ">1000" --language python

# 按 Topic 筛选
python scripts/search.py "graphql client" --topic graphql --limit 10

# 按许可证筛选
python scripts/search.py "web framework" --license mit

# 按创建时间筛选（GitHub）
python scripts/search.py "react" --sort updated --limit 5
```

### 输出格式

```bash
# Markdown 表格（默认）
python scripts/search.py "react hooks" --format markdown

# JSON 格式
python scripts/search.py "react hooks" --format json

# 保存到文件
python scripts/search.py "react hooks" --save --output ./results
```

## 支持平台

### GitHub（默认，数据最全）

- **API**: `https://api.github.com/search/repositories`
- **Token**: 设置 `GITHUB_TOKEN` 环境变量
- **速率限制**: 未认证 10 次/分钟，Token 30 次/分钟
- **搜索语法**: 最丰富，支持 stars/language/topic/license/时间等

### GitLab（企业/私有项目）

- **API**: `https://gitlab.com/api/v4/projects`
- **Token**: 设置 `GITLAB_TOKEN` 环境变量
- **速率限制**: 未认证 500 次/10分钟
- **特点**: 无硬性结果上限，适合深度翻页

### Gitee（国内项目补充）

- **API**: `https://gitee.com/api/v5/search/repositories`
- **Token**: 设置 `GITEE_TOKEN` 环境变量
- **速率限制**: 未认证 60 次/小时
- **特点**: 国内访问快，中文项目多

### npm（Node.js 包搜索）

- **API**: `https://registry.npmjs.org/-/v1/search`
- **Token**: 不需要
- **特点**: 内置评分系统（quality/popularity/maintenance）

### PyPI（Python 包查询）

- **API**: `https://pypi.org/pypi/{package}/json`
- **限制**: **没有搜索 API**，只能按包名精确查询
- **用途**: 获取包详情，不是搜索

## Token 配置

### 必须配置（推荐）

**GitHub Token** — 突破速率限制，搜索更稳定：

1. 打开 https://github.com/settings/tokens/new
2. 勾选 `repo` 权限即可
3. 复制生成的 token

```bash
# Windows (Git Bash)
export GITHUB_TOKEN="ghp_xxxx"

# 或写入 ~/.bashrc 永久生效
echo 'export GITHUB_TOKEN="ghp_xxxx"' >> ~/.bashrc
source ~/.bashrc
```

### 可选配置（按需）

| 环境变量 | 用途 | 获取方式 | 免费额度 |
|----------|------|----------|----------|
| `GITHUB_TOKEN` | GitHub 搜索提速 | [GitHub Settings](https://github.com/settings/tokens) | 30 次/分钟（无 Key 仅 10 次） |
| `GITLAB_TOKEN` | GitLab 搜索 | [GitLab Settings](https://gitlab.com/-/profile/personal_access_tokens) | 500 次/10分钟（无 Key 也可用） |
| `GITEE_TOKEN` | Gitee 搜索 | [Gitee Settings](https://gitee.com/profile/personal_access_tokens) | 60 次/小时（无 Key 仅 10 次） |
| `LIBRARIES_IO_KEY` | **PyPI 搜索**（关键） | [libraries.io](https://libraries.io/api) 注册后获取 | 60 次/分钟，免费 |

### PyPI 搜索配置教程

默认 PyPI 只能按包名精确查询。配置 `LIBRARIES_IO_KEY` 后解锁**关键词搜索**能力：

**步骤 1：注册 libraries.io**

1. 打开 https://libraries.io/
2. 点击右上角 Sign Up，用 GitHub 账号登录
3. 登录后打开 https://libraries.io/api 复制你的 API Key

**步骤 2：设置环境变量**

```bash
# Windows (Git Bash)
export LIBRARIES_IO_KEY="your_api_key_here"

# 永久生效
echo 'export LIBRARIES_IO_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**步骤 3：测试**

```bash
# 无 Key：只能精确查询
python scripts/search.py "fastapi" --platform pypi
# → 1 个结果（精确匹配）

# 有 Key：支持关键词搜索
python scripts/search.py "web framework" --platform pypi
# → 多个结果（模糊搜索）
```

### 下载量数据（免费，无需配置）

- **npm 包**：自动获取最近一周下载量
- **PyPI 包**：自动获取最近一月下载量（通过 pypistats.org）

无需任何配置，开箱即用。

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

---

## 输出示例

### Markdown 格式

```markdown
## 搜索结果：python web framework

共找到 8673 个项目（来源：github）

| # | 项目 | Stars | Language | 描述 |
|---|------|-------|----------|------|
| 1 | [fastapi/fastapi](https://github.com/fastapi/fastapi) | 100k | Python | FastAPI framework, high performance, easy to learn, fast to code |
| 2 | [django/django](https://github.com/django/django) | 88k | Python | The Web framework for perfectionists with deadlines. |
| 3 | [pallets/flask](https://github.com/pallets/flask) | 72k | Python | The Python micro framework for building web applications. |
```

### JSON 格式

```json
{
  "query": "python web framework",
  "platform": "github",
  "total": 8673,
  "results": [
    {
      "name": "fastapi/fastapi",
      "url": "https://github.com/fastapi/fastapi",
      "stars": 100000,
      "forks": 15000,
      "language": "Python",
      "description": "FastAPI framework, high performance, easy to learn, fast to code",
      "topics": ["api", "async", "fastapi", "python", "web"],
      "license": "MIT",
      "created_at": "2018-12-08T10:00:00Z",
      "updated_at": "2026-06-20T15:30:00Z",
      "open_issues": 500
    }
  ]
}
```

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

## 开发指南

### 项目结构

```
oss-finder/
├── SKILL.md              # Skill 主文件
├── README.md             # 本文档
├── scripts/
│   └── search.py         # 搜索脚本
├── references/
│   ├── github-api.md     # GitHub API 参考
│   ├── gitlab-api.md     # GitLab API 参考
│   ├── gitee-api.md      # Gitee API 参考
│   └── npm-api.md        # npm API 参考
└── evals/
    └── evals.json        # 评测集
```

### 运行测试

```bash
# 测试帮助信息
python scripts/search.py --help

# 测试 GitHub 搜索
python scripts/search.py "react" --limit 3

# 测试 npm 搜索
python scripts/search.py "lodash" --platform npm --limit 3

# 测试 JSON 输出
python scripts/search.py "vue" --format json --limit 3
```

## 最佳实践

1. **使用 Token** — 突破速率限制，获得更稳定的服务
2. **合理设置 limit** — 避免请求过多数据
3. **使用筛选条件** — 缩小搜索范围，提高相关性
4. **保存结果** — 使用 `--save` 保存到文件，便于后续分析
5. **跨平台搜索** — 使用 `--platform all` 获取更全面的结果

## 常见问题

### Q: 为什么搜索结果为空？

A: 可能原因：
- GitHub API 速率限制（设置 `GITHUB_TOKEN`）
- Gitee 未认证（设置 `GITEE_TOKEN`）
- 搜索关键词太具体

### Q: 如何提高搜索相关性？

A: 建议：
- 使用更具体的关键词
- 添加语言筛选 `--language`
- 添加 Topic 筛选 `--topic`
- 按 Stars 排序 `--sort stars`

### Q: 如何批量下载项目？

A: 搜索结果包含项目 URL，可以使用 git clone：

```bash
# 搜索并保存
python scripts/search.py "react hooks" --save --format json

# 读取 JSON 并克隆
cat output/oss-finder/latest.json | jq -r '.results[].url' | while read url; do
  git clone "$url"
done
```

## 许可证

MIT License

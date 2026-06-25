# Deep Research — 深度调研工具

> 三阶段模型：澄清 → 并行执行 → 报告生成

## 架构

```
┌─────────────────────────────────────────────────────┐
│                    Deep Research                      │
│                                                       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Tavily   │  │   Jina    │  │ SearXNG   │       │
│  │ AI 搜索   │  │ 网页提取  │  │ 元搜索    │       │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘       │
│        │              │              │               │
│        └──────────┬───┴──────────────┘               │
│                   │                                   │
│            ┌──────┴──────┐                           │
│            │  多源聚合    │                           │
│            └──────┬──────┘                           │
│                   │                                   │
│  ┌────────────────┼────────────────┐                 │
│  │         子 Agent 并行            │                 │
│  │  Agent 1  Agent 2  Agent 3  ... │                 │
│  └────────────────┬────────────────┘                 │
│                   │                                   │
│            ┌──────┴──────┐                           │
│            │  报告生成    │                           │
│            └─────────────┘                           │
└─────────────────────────────────────────────────────┘
```

## 整合的工具

| 工具 | 来源 | 用途 | 免费额度 |
|------|------|------|----------|
| **Tavily** | tavily.com | AI 搜索引擎 | 1000 次/月 |
| **Jina Reader** | jina.ai | 网页内容提取 | 20 RPM |
| **SearXNG** | github.com/searxng/searxng | 元搜索引擎 | 完全免费（需自建） |
| **oss-finder** | 本项目 | 开源项目搜索 | 免费 |

## 为什么选这些工具

1. **Tavily** — 专为 AI Agent 设计，返回结构化结果，集成最简单
2. **Jina Reader** — 一个 GET 请求就能把网页转 Markdown，免费可用
3. **SearXNG** — 开源免费，聚合 70+ 搜索引擎，需 Docker 自建
4. **oss-finder** — 本项目开发的 GitHub/npm/PyPI 搜索工具

## 快速开始

### 1. 配置 Tavily（推荐）

```bash
# 注册：https://app.tavily.com
# 获取 API Key 后设置环境变量
export TAVILY_API_KEY=tvly-xxxxx
```

### 2. 配置 Jina（可选）

```bash
# 注册：https://jina.ai
# 基础功能无需 Key，有 Key 额度更高
export JINA_API_KEY=jina_xxxxx
```

### 3. 使用

```bash
# 网页搜索
python scripts/search.py "Python Web 框架对比 2025"

# 多源搜索
python scripts/search.py "React vs Vue" --sources tavily,jina

# 深度搜索
python scripts/search.py "Kubernetes 最佳实践" --depth advanced

# 读取网页内容
python scripts/search.py --read "https://example.com/article"
```

### 4. 深度调研（Claude Code Skill）

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
```

## 输出示例

```markdown
## 搜索结果: Python Web 框架对比 2025

### AI 回答
[Tavily] FastAPI 是 2025 年最流行的 Python Web 框架...

### 来源 (5 个)

| # | 来源 | 内容摘要 |
|---|------|----------|
| 1 | [FastAPI vs Django](https://...) | FastAPI 在性能上优于 Django... |
| 2 | [Python Web 框架排名](https://...) | 2025 年排名：FastAPI, Django, Flask... |

**数据源:** tavily, jina
```

## 目录结构

```
deep-research/
├── SKILL.md           # 主入口（含架构说明）
├── README.md          # 本文件
├── scripts/
│   └── search.py      # 多源搜索引擎
├── references/
│   └── tool-integration.md
└── evals/
    └── evals.json
```

## 许可证

MIT License

---
name: deep-research
version: 2.1.0
description: |
  深度调研工具，多源并发搜索、子 Agent 并行、生成带引用的研究报告。
  当用户说"深度调研"、"deep research"、"帮我研究"、"全面分析"时调用。
context: fork
agent: general-purpose
allowed-tools: Read Write Bash Glob Grep AskUserQuestion Agent
---

# Deep Research — 深度调研工具 v2.0

**三阶段模型：澄清 → 并行执行 → 报告生成。**

---

## 架构说明

### 数据源分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Deep Research 搜索引擎                      │
├─────────────────────────────────────────────────────────────┤
│  免费层（无需配置）                                             │
│  ├── DuckDuckGo    网页搜索，国内可用                          │
│  ├── GitHub CLI    开源项目搜索                                │
│  ├── npm           Node.js 包搜索                             │
│  └── PyPI          Python 包查询                              │
├─────────────────────────────────────────────────────────────┤
│  增强层（需要 API Key）                                        │
│  ├── Tavily        AI 搜索引擎，1000次/月免费                  │
│  ├── Jina Reader   网页内容提取（需 VPN）                      │
│  └── Gitee         国内开源项目（需 Token）                    │
├─────────────────────────────────────────────────────────────┤
│  自建层（需要部署）                                            │
│  └── SearXNG       元搜索引擎聚合                             │
└─────────────────────────────────────────────────────────────┘
```

### 整合的开源工具

| 工具 | 来源 | 用途 | 许可证 | 国内可用 | 需要配置 |
|------|------|------|--------|----------|----------|
| **DuckDuckGo** | [ddgs](https://github.com/deedy5/ddgs) | 网页搜索 | MIT | ✅ | 无需 |
| **Tavily** | [tavily.com](https://tavily.com) | AI 搜索引擎 | 商业 | ✅ | API Key |
| **Jina Reader** | [jina.ai](https://jina.ai) | 网页内容提取 | 商业 | ❌ 需VPN | API Key（可选） |
| **SearXNG** | [github.com/searxng](https://github.com/searxng/searxng) | 元搜索引擎聚合 | AGPL-3.0 | ✅ | 自建实例 |
| **oss-finder** | 本项目 | 开源项目搜索 | MIT | ✅ | 无需 |

### 为什么选这些工具

1. **DuckDuckGo** — 免费、无需 API Key、国内可用、支持文本/新闻搜索
2. **Tavily** — 专为 AI Agent 设计，返回结构化结果，免费额度 1000 次/月
3. **Jina Reader** — 极简 API，擅长网页转 Markdown，但需要 VPN
4. **SearXNG** — 完全免费开源，聚合 70+ 搜索引擎，需自建
5. **oss-finder** — 本项目开发，GitHub/npm/PyPI 项目搜索

### 降级策略

```
用户输入调研主题
      │
      ▼
┌─────────────────┐
│  检测网络环境    │  判断是否能访问国际服务
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  检测 API Key   │  检查 Tavily/Jina 配置
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  自动选择可用数据源                                           │
│                                                              │
│  有 VPN + API Key:                                           │
│    DuckDuckGo + Tavily + Jina + oss-finder                   │
│                                                              │
│  有 API Key（无 VPN）:                                        │
│    DuckDuckGo + Tavily + oss-finder                          │
│                                                              │
│  无 VPN + 无 API Key:                                         │
│    DuckDuckGo + oss-finder（降级方案）                         │
└─────────────────────────────────────────────────────────────┘
```

### 数据流

```
用户输入调研主题
      │
      ▼
┌─────────────────┐
│  阶段一：澄清    │  AskUserQuestion 确认目标/深度/维度
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  阶段二：拆解    │  拆解为 3-5 个子问题
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段三：并行执行（子 Agent）                                  │
│                                                              │
│  Agent 1: DuckDuckGo 搜索 + Tavily 搜索（如果可用）           │
│  Agent 2: oss-finder 搜索开源项目                             │
│  Agent 3: Jina Search 搜索（如果可用，需要 VPN）               │
│  Agent 4: SearXNG 聚合搜索（如果可用，需要自建）               │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  阶段四：综合    │  交叉验证、标注矛盾、生成报告
└─────────────────┘
```

---

## 核心原则

> **先澄清，再拆解，并行执行，综合报告。**
>
> **七条铁律：**
> 1. **澄清优先** — 模糊主题必须先问用户，不能自作主张
> 2. **拆解为王** — 复杂问题拆解为 3-5 个独立子问题
> 3. **并行执行** — 独立子问题必须并行，不要串行等待
> 4. **多源交叉** — 每个子问题至少搜索 2-3 个不同来源
> 5. **引用可追溯** — 报告中每个关键结论必须附带来源链接
> 6. **诚实标注** — 无法验证的信息标注"待确认"
> 7. **降级透明** — 数据源不可用时明确告知用户，推荐配置方案

---

## 工作流程

### 阶段零：环境检测（自动）

**首次使用时自动执行：**

```bash
python "${SKILL_DIR}/scripts/search.py" --check
```

**输出示例：**
```
[检查] 数据源可用性...

[网络环境]
   VPN: [无]
   Google: [不可达]
   Jina: [不可达]
   Tavily: [不可达]

[数据源状态]
   duckduckgo: [可用]
   tavily: [不可用]
   jina: [不可用]
   searxng: [不可用]
```

**根据检测结果推荐配置：**

| 场景 | 推荐操作 |
|------|----------|
| 无 VPN + 无 API Key | 使用 DuckDuckGo（默认）|
| 无 VPN + 有 Tavily Key | 使用 DuckDuckGo + Tavily |
| 有 VPN + 无 API Key | 使用 DuckDuckGo + Jina |
| 有 VPN + 有 API Key | 使用全部数据源 |

### 阶段一：澄清问题（Clarify）

收到调研主题后，使用 AskUserQuestion 确认：

**问题 1：调研目标**
- 技术选型（比较工具/框架/方案）
- 市场分析（行业/竞品/趋势）
- 学术研究（论文/理论/方法）
- 问题诊断（bug/性能/架构）
- 其他

**问题 2：调研深度**
- 快速浏览（5-10 个来源，1-2 分钟）
- 标准调研（15-25 个来源，3-5 分钟）（默认）
- 深度研究（30+ 个来源，8-15 分钟）

**问题 3：关注维度（可多选）**
- 核心功能/特性
- 性能/基准测试
- 社区活跃度/生态
- 优缺点对比
- 实际案例/最佳实践
- 其他（用户自定义）

### 阶段二：并行执行（Execute）

#### 搜索工具选择

根据子问题选择合适的搜索工具：

| 数据类型 | 工具 | 命令 |
|----------|------|------|
| 网页/文章 | DuckDuckGo | `python scripts/search.py "query"` |
| 网页/文章（AI） | Tavily | `python scripts/search.py "query" --sources tavily` |
| 网页内容提取 | Jina Reader | `python scripts/search.py --read URL` |
| 开源项目 | oss-finder | `python ../oss-finder/scripts/search.py "query"` |
| 多源聚合 | 全部 | `python scripts/search.py "query" --sources duckduckgo,tavily,jina` |

#### 子 Agent Prompt

```
你是深度调研的子 Agent，负责调研以下子问题：

**子问题：** {问题描述}
**所属主题：** {调研主题}

**任务：**
1. 使用搜索工具获取信息
2. 阅读并评估来源
3. 提取关键发现（3-5 条）
4. 标注来源可信度

**搜索命令：**
python "${SKILL_DIR}/scripts/search.py" "搜索关键词" --limit 10

**输出：**
- 关键发现（带来源 URL）
- 矛盾点
- 来源可信度
```

### 阶段三：报告生成（Report）

报告结构：

```markdown
# {调研主题}

**调研时间：** YYYY-MM-DD
**调研深度：** 快速/标准/深度
**数据源：** DuckDuckGo, Tavily, oss-finder, ...

---

## 执行摘要
[核心结论]

## 1. {子问题 1}
[分析 + 引用]

## 2. {子问题 2}
[分析 + 引用]

## N. 结论与建议

## 来源列表
| # | 来源 | URL | 可信度 |
|---|------|-----|--------|
```

---

## 搜索引擎配置

### DuckDuckGo（默认，免费）

**无需配置，开箱即用。**

- 安装：`pip install ddgs`
- 国内可用
- 支持文本/新闻搜索
- 无需 API Key

### Tavily（推荐增强）

1. 注册：https://app.tavily.com
2. 获取 API Key
3. 设置环境变量：`export TAVILY_API_KEY=tvly-xxxxx`

免费额度：约 1000 次/月

**优势：**
- 专为 AI Agent 设计
- 返回结构化结果
- 支持 AI 生成回答

### Jina Reader（需要 VPN）

1. 注册：https://jina.ai
2. 获取 API Key（基础功能无需 Key）
3. 设置环境变量：`export JINA_API_KEY=jina_xxxxx`

免费额度：20 RPM（无 Key）/ 更高（有 Key）

**注意：** 国内网络无法直接访问，需要 VPN。

### SearXNG（可选，需自建）

```bash
# Docker 部署
docker run -d -p 8080:8080 searxng/searxng

# 设置环境变量
export SEARXNG_URL=http://localhost:8080
```

**优势：**
- 完全免费开源
- 聚合 70+ 搜索引擎
- 自建可控

---

## 使用示例

### 快速搜索

```bash
# 网页搜索（DuckDuckGo，免费）
python scripts/search.py "Python Web 框架对比 2025"

# 指定数据源
python scripts/search.py "React vs Vue" --sources duckduckgo,tavily

# 深度搜索（Tavily）
python scripts/search.py "Kubernetes 最佳实践" --depth advanced

# 读取网页内容（需要 VPN）
python scripts/search.py --read "https://example.com/article"

# 检查数据源可用性
python scripts/search.py --check
```

### 深度调研

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
/deep-research 大语言模型微调技术
```

### 配置增强功能

```bash
# 1. 安装 DuckDuckGo（默认）
pip install ddgs

# 2. 配置 Tavily（可选，推荐）
export TAVILY_API_KEY=tvly-xxxxx

# 3. 配置 Jina（可选，需要 VPN）
export JINA_API_KEY=jina_xxxxx

# 4. 自建 SearXNG（可选）
docker run -d -p 8080:8080 searxng/searxng
export SEARXNG_URL=http://localhost:8080
```

---

## 禁止行为

- ❌ **禁止跳过澄清** — 模糊主题必须先确认
- ❌ **禁止串行执行** — 独立子问题必须并行
- ❌ **禁止无来源结论** — 每个结论必须有出处
- ❌ **禁止隐藏数据源** — 必须告知用户用了哪些工具
- ❌ **禁止静默降级** — 数据源不可用时必须告知用户

---

## 参考资料

- DuckDuckGo: https://github.com/deedy5/ddgs (MIT)
- Tavily API: https://docs.tavily.com
- Jina Reader: https://jina.ai/reader
- SearXNG: https://docs.searxng.org
- Kimi Deep Research: https://kimi.moonshot.cn/deep-research
- oss-finder: `${SKILL_DIR}/../oss-finder/SKILL.md`

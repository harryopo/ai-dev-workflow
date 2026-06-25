---
name: deep-research
description: |
  深度调研工具，多源并发搜索、子 Agent 并行、生成带引用的研究报告。
  当用户说"深度调研"、"deep research"、"帮我研究"、"全面分析"时调用。
context: fork
agent: general-purpose
allowed-tools: Read Write Bash Glob Grep AskUserQuestion Agent
---

# Deep Research — 深度调研工具

**三阶段模型：澄清 → 并行执行 → 报告生成。**

---

## 架构说明

### 整合的开源工具

| 工具 | 来源 | 用途 | 许可证 |
|------|------|------|--------|
| **Tavily** | tavily.com | AI 搜索引擎（主搜索） | 商业，有免费额度 |
| **Jina Reader** | jina.ai | 网页内容提取 + 搜索 | 商业，有免费额度 |
| **SearXNG** | github.com/searxng/searxng | 元搜索引擎聚合 | AGPL-3.0 |
| **oss-finder** | 本项目 | 开源项目搜索 | MIT |

### 为什么选这些工具

1. **Tavily** — 专为 AI Agent 设计，返回结构化结果，免费额度 1000 次/月
2. **Jina Reader** — 极简 API（一个 GET 请求），免费可用，擅长网页转 Markdown
3. **SearXNG** — 完全免费开源，聚合 70+ 搜索引擎，需自建
4. **oss-finder** — 本项目开发，GitHub/npm/PyPI 项目搜索

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
┌─────────────────────────────────────────────────┐
│  阶段三：并行执行（子 Agent）                      │
│                                                   │
│  Agent 1: Tavily 搜索 + Jina 读取网页             │
│  Agent 2: oss-finder 搜索开源项目                  │
│  Agent 3: Jina Search 搜索 + 内容提取              │
│  Agent 4: SearXNG 聚合搜索（如果可用）             │
└────────┬────────────────────────────────────────┘
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
> 7. **开源透明** — 使用的工具和数据源必须明确告知用户

---

## 工作流程

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
| 网页/文章 | Tavily | `python scripts/search.py "query" --sources tavily` |
| 网页内容提取 | Jina Reader | `python scripts/search.py --read URL` |
| 开源项目 | oss-finder | `python ../oss-finder/scripts/search.py "query"` |
| 多源聚合 | 全部 | `python scripts/search.py "query" --sources tavily,jina,searxng` |

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
**数据源：** Tavily, Jina, oss-finder, ...

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

### Tavily（推荐）

1. 注册：https://app.tavily.com
2. 获取 API Key
3. 设置环境变量：`export TAVILY_API_KEY=tvly-xxxxx`

免费额度：约 1000 次/月

### Jina Reader（可选）

1. 注册：https://jina.ai
2. 获取 API Key（基础功能无需 Key）
3. 设置环境变量：`export JINA_API_KEY=jina_xxxxx`

免费额度：20 RPM（无 Key）/ 更高（有 Key）

**注意：** 国内网络可能无法直接访问 Jina 服务，需要代理或使用其他数据源。

### SearXNG（可选，需自建）

```bash
# Docker 部署
docker run -d -p 8080:8080 searxng/searxng

# 设置环境变量
export SEARXNG_URL=http://localhost:8080
```

---

## 使用示例

### 快速搜索

```bash
# 网页搜索
python scripts/search.py "Python Web 框架对比 2025"

# 指定数据源
python scripts/search.py "React vs Vue" --sources tavily,jina

# 深度搜索
python scripts/search.py "Kubernetes 最佳实践" --depth advanced

# 读取网页内容
python scripts/search.py --read "https://example.com/article"
```

### 深度调研

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
/deep-research 大语言模型微调技术
```

---

## 禁止行为

- ❌ **禁止跳过澄清** — 模糊主题必须先确认
- ❌ **禁止串行执行** — 独立子问题必须并行
- ❌ **禁止无来源结论** — 每个结论必须有出处
- ❌ **禁止隐藏数据源** — 必须告知用户用了哪些工具

---

## 参考资料

- Tavily API: https://docs.tavily.com
- Jina Reader: https://jina.ai/reader
- SearXNG: https://docs.searxng.org
- Kimi Deep Research: https://kimi.moonshot.cn/deep-research
- oss-finder: `${SKILL_DIR}/../oss-finder/SKILL.md`

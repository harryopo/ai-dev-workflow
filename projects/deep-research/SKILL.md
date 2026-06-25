---
name: deep-research
description: |
  深度调研工具，自动拆解问题、并行多源搜索、生成带引用的研究报告。
  当用户说"深度调研"、"deep research"、"帮我研究"、"全面分析"、"调研报告"时调用。
context: fork
agent: general-purpose
allowed-tools: Read Write Bash Glob Grep AskUserQuestion Agent
---

# Deep Research — 深度调研工具

**三阶段模型：澄清 → 并行执行 → 报告生成。**

参考 Kimi Deep Research 的工作流程，整合 oss-finder、agent-reach、crawl4ai 等工具链，通过子 agent 并行实现高效调研。

---

## 核心原则

> **先澄清，再拆解，并行执行，综合报告。**
>
> **六条铁律：**
> 1. **澄清优先** — 模糊主题必须先问用户，不能自作主张
> 2. **拆解为王** — 复杂问题拆解为 3-5 个独立子问题，每个子问题对应一个子 agent
> 3. **并行执行** — 子 agent 之间无依赖关系时必须并行，不要串行等待
> 4. **多源交叉** — 每个子问题至少搜索 2-3 个不同来源，交叉验证
> 5. **引用可追溯** — 报告中每个关键结论必须附带来源链接
> 6. **迭代深入** — 第一轮结果不够深入时，自动发起第二轮搜索

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
- 快速浏览（5-10 个来源，2-3 分钟）
- 标准调研（15-25 个来源，5-8 分钟）（默认）
- 深度研究（30+ 个来源，10-15 分钟）

**问题 3：关注维度（可多选）**
- 核心功能/特性
- 性能/基准测试
- 社区活跃度/生态
- 优缺点对比
- 实际案例/最佳实践
- 其他（用户自定义）

**跳过条件：** 用户输入已足够明确（如"对比 React vs Vue vs Svelte 的性能"）时，可跳过澄清直接执行。

### 阶段二：并行执行（Execute）

#### 2.1 拆解子问题

根据用户确认的调研目标，将主题拆解为 3-5 个子问题：

```
主题：2025 年最值得学习的 Python Web 框架

拆解为：
1. 主流框架最新版本对比（Django/Flask/FastAPI/Starlette）
2. 性能基准测试数据（TechEmpower 等）
3. 社区活跃度和生态成熟度（GitHub/Stack Overflow）
4. 实际项目采用情况和最佳实践
5. 新兴框架值得关注的（Litestar/Robyn/Granian）
```

#### 2.2 确定数据源

根据子问题选择合适的数据源：

| 数据类型 | 工具 | 适用场景 |
|----------|------|----------|
| 开源项目 | oss-finder | GitHub/GitLab/npm/PyPI 搜索 |
| 网页内容 | crawl4ai MCP | 文章/文档/博客深度阅读 |
| 社交讨论 | agent-reach | Twitter/Reddit/B站/小红书 |
| 搜索引擎 | deep-research-pro | 多引擎搜索（中英文） |
| 技术文档 | Agent + WebFetch | 官方文档/README |

#### 2.3 并行调度

每个子问题启动一个独立 Agent，所有 Agent 并行执行：

```
Agent 1: "搜索 Python Web 框架最新版本和特性"
  → oss-finder: django, flask, fastapi, starlette
  → crawl4ai: 各框架官方文档

Agent 2: "搜索 Python Web 框架性能基准测试"
  → WebFetch: TechEmpower Round 22+
  → 搜索: "python web framework benchmark 2025"

Agent 3: "分析社区活跃度和生态"
  → oss-finder: 各框架 GitHub stars/forks/issues
  → agent-reach: Reddit/Twitter 讨论热度

Agent 4: "搜索实际项目采用案例"
  → 搜索: "companies using fastapi" "django vs flask production"
  → crawl4ai: 技术博客/案例分析

Agent 5: "调研新兴框架"
  → oss-finder: "python web framework" stars>500 created>2024-01-01
  → 搜索: "python web framework 2025 new"
```

#### 2.4 进度监控

每个 Agent 完成后输出：
- 搜索的来源数量
- 关键发现摘要（3-5 条）
- 发现的矛盾点/待验证信息

### 阶段三：报告生成（Report）

#### 3.1 综合分析

收集所有 Agent 的结果后：
1. 交叉验证：同一结论有多个来源支持
2. 矛盾处理：标注争议点，给出不同观点
3. 去重合并：相同来源的不同角度合并

#### 3.2 输出结构

```markdown
# {调研主题} — 深度调研报告

**调研时间：** YYYY-MM-DD
**调研深度：** 快速/标准/深度
**来源数量：** N 个独立来源

---

## 执行摘要

[3-5 句话概括核心结论]

---

## 1. {子问题 1}

[分析内容，带行内引用 [1]]

**关键发现：**
- 发现 1 [来源 1]
- 发现 2 [来源 2]

## 2. {子问题 2}

...

## N. 结论与建议

[基于所有发现的综合建议]

---

## 来源列表

| # | 来源 | URL | 关键信息 |
|---|------|-----|----------|
| 1 | 来源名 | URL | 摘要 |
| 2 | ... | ... | ... |

---

## 调研方法

- 搜索引擎：{使用的引擎}
- 数据平台：{使用的平台}
- 搜索策略：{关键词组合}
- 执行时间：{总耗时}
```

#### 3.3 保存与交付

- 保存到 `~/research/{slug}/report.md`
- 保存原始数据到 `~/research/{slug}/sources.json`
- 可选：生成交互式 HTML 报告（参考 super-frontend-design）

---

## 子 Agent Prompt 模板

每个子 Agent 使用以下 prompt 结构：

```
你是一个深度调研子 Agent，负责调研以下子问题：

**子问题：** {子问题描述}
**所属主题：** {调研主题}
**关注维度：** {用户选择的维度}

**任务：**
1. 使用指定的工具搜索相关信息
2. 阅读并评估找到的来源
3. 提取关键发现（3-5 条）
4. 标注来源的可信度（高/中/低）
5. 发现矛盾点时记录下来

**可用工具：**
- oss-finder: 开源项目搜索
- crawl4ai: 网页深度阅读
- WebFetch: 简单网页抓取
- Bash: 执行命令行工具

**输出格式：**
- 关键发现（带来源链接）
- 矛盾点/待验证信息
- 来源可信度评估
```

---

## 工具集成

### oss-finder 集成

用于开源项目搜索：

```bash
python "${SKILL_DIR}/../oss-finder/scripts/search.py" "query" --stars ">1000" --limit 10 --format json
```

### crawl4ai MCP 集成

用于网页深度阅读：

```
使用 crawl4ai MCP 工具抓取 URL 内容
支持 JavaScript 渲染的页面
```

### agent-reach 集成

用于社交媒体搜索：

```bash
# Twitter
agent-reach twitter search "query" --limit 10

# Reddit
agent-reach reddit search "query" --limit 10

# B站
agent-reach bilibili search "query" --limit 10
```

---

## 禁止行为

- ❌ **禁止跳过澄清** — 模糊主题必须先确认
- ❌ **禁止串行执行** — 独立子问题必须并行
- ❌ **禁止无来源结论** — 每个结论必须有出处
- ❌ **禁止单一来源** — 每个子问题至少 2 个来源
- ❌ **禁止忽略矛盾** — 矛盾点必须在报告中标注
- ❌ **禁止伪造引用** — 来源必须真实可访问

---

## 参考资料

- Kimi Deep Research: https://kimi.moonshot.cn/deep-research
- oss-finder: `${SKILL_DIR}/../oss-finder/SKILL.md`
- agent-reach: `~/.claude/skills/agent-reach/SKILL.md`
- crawl4ai: MCP 工具
- super-frontend-design: HTML 报告生成

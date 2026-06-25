# Deep Research — 深度调研工具

> 三阶段模型：澄清 → 并行执行 → 报告生成

## 简介

Deep Research 是一个 Claude Code Skill，参考 Kimi Deep Research 的工作流程，整合 oss-finder、agent-reach、crawl4ai 等工具链，通过子 Agent 并行实现高效调研。

## 核心特性

- **Kimi 三阶段模型** — 澄清问题 → 并行执行 → 报告生成
- **子 Agent 并行** — 3-5 个子 Agent 同时调研不同维度
- **多源交叉验证** — 每个结论至少 2 个独立来源支持
- **工具链整合** — oss-finder + crawl4ai + agent-reach
- **引用可追溯** — 报告中每个关键结论附带来源链接

## 使用方式

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
/deep-research 大语言模型微调技术
```

## 工作流程

### 阶段一：澄清

收到模糊主题时，使用 AskUserQuestion 确认：
- 调研目标（技术选型/市场分析/学术研究/问题诊断）
- 调研深度（快速/标准/深度）
- 关注维度（功能/性能/社区/案例）

### 阶段二：并行执行

1. 拆解为 3-5 个子问题
2. 每个子问题启动一个独立 Agent
3. 所有 Agent 并行执行
4. 每个 Agent 使用指定的工具搜索

### 阶段三：报告生成

1. 收集所有 Agent 结果
2. 交叉验证关键结论
3. 标注矛盾点和争议
4. 生成结构化报告

## 报告结构

```markdown
# {调研主题} — 深度调研报告

## 执行摘要
[核心结论]

## 1. {子问题 1}
[分析 + 引用]

## 2. {子问题 2}
[分析 + 引用]

## N. 结论与建议

## 来源列表
## 调研方法
```

## 数据源

| 数据类型 | 工具 | 适用场景 |
|----------|------|----------|
| 开源项目 | oss-finder | GitHub/npm/PyPI 搜索 |
| 网页内容 | crawl4ai | 文档/博客深度阅读 |
| 社交讨论 | agent-reach | Twitter/Reddit/B站 |
| 搜索引擎 | deep-research-pro | 多引擎搜索 |

## 目录结构

```
deep-research/
├── SKILL.md           # 主入口
├── README.md          # 本文件
├── evals/
│   └── evals.json     # 测试集
└── references/
    └── tool-integration.md  # 工具集成指南
```

## 依赖

- oss-finder（开源项目搜索）
- agent-reach（社交媒体搜索）
- crawl4ai MCP（网页深度阅读）
- Claude Code Agent（子 Agent 并行）

# CHANGELOG — deep-research-ultra

> 本文件**单独**记录 skill 的版本更新历史、更新概览与迁移指南。
> SKILL.md 保持纯净，只含运行必需内容（触发条件/使用说明/工作流/约束）——见开发约束第 10 条。

---

## v6.2.0（2026-09-18）— 开源调研质量门（六维必检）+ 仓库健康扫描

### 背景
AI 开源调研普遍存在「信息失真、适配不足、风险隐形、落地性差」四类核心问题，
尤其在"用开源方案优化自有项目"场景会传导到落地阶段。v6.2 将六类缺陷固化为强制检查。

### 新功能

| 能力块 | 说明 | 模块 |
|--------|------|------|
| 仓库健康扫描器 | 官方 API 事实（star/最近提交/归档/许可证）+ 停更预警 + OSV CVE + 许可证传染性分级（permissive/weak/strong）+ 综合风险标签 | scripts/repo_health.py |
| 六维质量门 | ①事实核实 ②适配性（技术栈对照） ③生态健康 ④合规安全 ⑤落地计划（成本/指标/灰度回滚） ⑥方法论（重优化轻替换、业务优先）——每候选项目强制检查，缺项拦截 | SKILL.md 7.0b |
| 结论风险标签 | 🔴 高风险 / 🟠 中风险 / 🟢 低风险；无官方数据指标标注"未核实" | SKILL.md 7.0b |
| 推荐清单扩展 | 增列 风险标签/许可证/最近提交/适配性/落地成本/量化指标 | SKILL.md 7.0b |

### 使用

```bash
python scripts/repo_health.py "langchain-ai/langchain" --package "pypi:langchain"   # GitHub + OSV CVE
python scripts/repo_health.py "https://gitee.com/oschina/xx" --json                  # Gitee
```

### 变更文件
- 新增：`scripts/repo_health.py`
- 修改：`SKILL.md`（7.0b 六维质量门）、`evals/evals.json`（dr-038）、`tests/test_v6.py`（+5 用例）、`CHANGELOG.md`

---

## v6.1.0（2026-09-18）— 环境配置门 + 开源调研拓宽（Gitee/ModelScope/论文双查）

### 新功能

| 能力块 | 说明 | 模块 |
|--------|------|------|
| 环境配置门（必过 Phase 0） | 按调研场景分级验证环境（minimal/opensource/academic/full），未就绪引导配置，验证通过才启动 | env_check.py + research.py --env-check |
| 国内开源平台引擎 | Gitee 仓库搜索 + 魔搭 ModelScope 模型搜索（免费公开 API 直连，无需 key，国内可用） | engines/platform_engines.py |
| 开源"项目+论文"双查 | 开源路由链自动含 Gitee/ModelScope/oss-finder + arXiv/OpenAlex 论文源 | router.py ENGINE_CHAIN_MAP |
| 开源语料扩张 | STRONG_KEYWORDS/REGEX 补 魔搭/ModelScope/Gitee；覆盖源矩阵含官方文档/skill 目录站/论坛 | router.py + SKILL.md 7.0 |
| 开源真实性硬规则 | 项目 claim 必须关联官方仓库 URL；事实与推断隔离；账本+校验门可溯源 | SKILL.md 7.0 |

### 变更文件

- 新增：`scripts/env_check.py`、`scripts/engines/platform_engines.py`
- 修改：`scripts/research.py`（--env-check/--env-profile/--no-net + 注册新引擎）、`scripts/engines/__init__.py`、`scripts/router.py`（开源链/关键词/正则）、`SKILL.md`（Phase 0 门控 + 7.0 开源工作流）、`CHANGELOG.md`
- 测试：env_check / platform_engines 单测新增

### 环境分级速览

| profile | 必需 | 可选 |
|---------|------|------|
| minimal | Python + 内置引擎 + 网络 | — |
| opensource | Python + 网络（Gitee/ModelScope/arXiv 免费直连） | GITHUB_TOKEN、全局 skill |
| academic | Python + 网络（arXiv/S2/OpenAlex 直连） | UNPAYWALL_EMAIL、GITHUB_TOKEN |
| full | Python + 网络 + MCP（setup-mcp.sh --core） | Tavily/Firecrawl/Crawl4AI/claude/npx |

### 已知限制（v6.1）

- ModelScope 官方公开 API 端点可能随版本更名（实测 `dolphin/models` 曾 404）：引擎作候选端点尝试 + 容错，失败自动降级到 Gitee/oss-finder/tavily 等（不阻断调研）
- Gitee/ModelScope API 对网络延迟敏感：国内正常直连；超时时引擎返回 None 并走降级链
- `agent-reach` 等社区 skill 为可选增强，缺失时 --env-check 仅告警不阻断

---

## v6.0.0（2026-09-18）— 子 Agent 并行编排 + 深度调研专家团 + 证据账本与分级

**升级依据**：2025-2026 深度调研方法论联网调研（12 个前沿模式 + Top 12 开源方案），结论见 [references/v6-research-notes.md](references/v6-research-notes.md)。

### 新功能

| 能力块 | 说明 | 模块 |
|--------|------|------|
| 子 Agent 并行编排 | Lead 规划 → 并行 spawn 子 Agent（独立上下文）→ 结果落盘 → 归并（Phase 2.5） | SKILL.md 工作流 + ledger.py |
| 深度调研专家团 | 多视角提问（域专家/怀疑者/实践者/记者/成本）+ 红蓝对抗 + 审稿人修订闭环（Phase 3.5） | plan.py + panel.py |
| 证据账本 | claim→source 可溯源、多子 Agent 并发写、merge 去重、status/export | ledger.py |
| 来源 Tier 分级 | Tier 1-4 域名判定，CRAAP 集成加权（Tier1 +0.1 / Tier4 -0.15） | tier.py + score.py |
| 发布前校验门 | 引用一致性/覆盖率/必需章节/低质源占比/摘要长度 | validate_report.py |
| effort 分级 + breadth 旋钮 | `--effort quick\|standard\|deep\|exhaustive` / `--breadth N` | research.py |
| 计划确认门 | `--plan-only` 输出待确认清单 → 用户批准后才执行（Phase 1.5） | research.py cmd_plan_only |
| 证据充分性停止 | 独立来源 ≥2 且 verified ≥1，否则 supplementing（EDR 不提前停止） | reflect.py |
| 报告增强 | 元信息行（effort/breadth/专家团/校验）+ 附录 D Tier 分布 + 账本摘要表 | report.py |
| 多视角注入 | 每个子问题默认挂 3 对抗视角，`--perspectives 0` 关闭 | plan.py |

### 变更文件

- 新增：`scripts/tier.py`、`scripts/ledger.py`、`scripts/panel.py`、`scripts/validate_report.py`、`scripts/tests/test_v6.py`、`references/v6-research-notes.md`
- 修改：`SKILL.md`（v6.0）、`scripts/{plan,reflect,score,report,research}.py`、`evals/evals.json`（+5 样本）、`README.md`
- 测试：pytest 96 → **124 passed**（新增 28 用例）

---

## v5.2.0（2026-08-08）— GitHub 深度搜索 + 国内内容源 + 推荐度评分

- **GitHub 深度搜索**：分桶搜索（4 桶按 star）+ 低星挖掘 + 依赖图反向挖掘 + awesome 列表挖掘（不漏项目）+ GitHub Code Search API（`GITHUB_TOKEN` 可选，有 5000/h 无 60/h）
- **国内内容源**：百度 SERP / 搜狗微信 / 搜狗知乎 / 百度学术（curl_cffi TLS 伪装 + UA 轮换，无需配置）
- **推荐度评分系统**：8 维 GitHub 评分 + 5 维论文评分 + 意图识别权重调整 + 分组排序（旗舰/主流/小众）+ 4 级推荐 + SVG 雷达图
- 引擎数：24 → **30**
- 相关调研归档：`references/GitHub深度搜索技巧调研.md`、`references/调研报告格式最佳实践调研.md`、`references/国内大厂深度研究方案调研-v3.md`、`references/深度研究开源项目调研-v3.md`、`references/国内智能体平台与调研专家团调研.md`

---

## v5.1.0（2026-08-08）— 学术全文 + 引用图谱 + 浏览器自动化 + 反爬升级

- **学术全文**：arXiv PDF/HTML/LaTeX 下载（`ArxivFulltextEngine`）+ Unpaywall DOI→OA PDF（需 `UNPAYWALL_EMAIL`）+ Semantic Scholar 引用图谱（引用意图 + influential citations）
- **浏览器自动化**：Crawl4AI Docker（`CRAWL4AI_URL`/`CRAWL4AI_API_TOKEN`）+ LayeredCrawler 四级爬取策略（curl_cffi → Firecrawl → Crawl4AI → Camoufox）
- **反爬虫升级**：curl_cffi TLS/JA3 指纹伪装（`impersonate="chrome124"`，未装自动降级 urllib）
- **问题链状态机**：6 状态（pending→searching→verified/conflict/supplementing→completed，秘塔问题链）
- **多信号停止**：覆盖率阈值 / 边际收益递减（Δ<0.05 且 ≥0.6）/ 无高优先级空白（Kimi 式）
- 引擎数：22 → **24**

---

## v5.0.0（2026-08-xx）— 智能路由 + 学术直连

- **智能路由**：三级级联 Rule（关键词正则，<1ms）→ Semantic（向量相似度，可选 sentence-transformers）→ LLM（可选回调）；9 类查询类型；每引擎独立 CircuitBreaker（CLOSED→OPEN→HALF_OPEN）
- **学术直连引擎**：OpenAlex（474M+）/ Semantic Scholar（200M+）/ PubMed（36M+），无需 MCP 直连
- 引擎数：20 → **22**

---

## v4.0.0（2026-07-30）— 四阶段范式 + 四层数据源重构

- 重构为 **Plan-Execute-Synthesize-Reflect 四阶段范式**
- 引入**四层数据源架构**：MCP 服务器 → 全局 Skill → Claude 内置 → 降级引擎
- 新增 MECE 问题树拆解（`scripts/plan.py`）、CRAAP 五维评分、交叉验证（≥2 独立来源）、反思循环 Drill-down、HTML 报告（Mermaid 时间线）、MCP 一键配置（`setup-mcp.sh --core`）、LRU 缓存（TTL 1h）、SearchEngine 抽象基类、MCP/Skill 引擎封装
- 弃用：Brave/Ecosia/Startpage/360/神马/Yahoo/Qwant/Google/Wolfram、Jina Reader（改用 defuddle/Firecrawl）、HTML regex 解析
- 修正 v3 文档与代码不一致（宣称 16 引擎实际 13 个）
- 引擎数：13 → **20**

---

## v3.2.0（2026-07-xx）

- 16 个搜索引擎 + 中英文自动切换（后被 v4.0 四层架构取代）

---

## 迁移指南

### v3 → v4

1. 配置 MCP：`bash scripts/setup-mcp.sh --core`
2. `--sources baidu,bing,duckduckgo` 等 v3 引擎名自动映射到 Layer 4 降级引擎（提示降级模式）
3. 缓存目录 `~/.cache/deep-research/` 兼容

### v4 → v5

1. `--auto-route` / `--route` 启用智能路由
2.（可选）`UNPAYWALL_EMAIL` 启用学术全文、`GITHUB_TOKEN` 增强 GitHub 深度搜索
3. 全部 v4 参数（`--sources`/`--format`/`--depth`/`--reflect-rounds`）保持兼容

### v5 → v6（增量扩展，全部向后兼容）

```bash
# 计划确认门：生成计划 + 待确认清单（effort/breadth/专家团建议）
python "${SKILL_DIR}/scripts/research.py" "<主题>" --plan-only --effort deep --breadth 8 --perspectives "domain_expert,skeptic,practitioner"

# 子 Agent 编排 + 证据账本落盘（每个子 Agent 用自己的 --ledger 目录）
python "${SKILL_DIR}/scripts/research.py" "子主题A" --ledger .research/session/ledger --perspectives domain_expert

# 账本管理 / 专家团评审 / Tier 分级 / 发布前校验
python "${SKILL_DIR}/scripts/ledger.py" status --session .research/session/ledger
python "${SKILL_DIR}/scripts/panel.py" review-outline --input outline.md --roles domain_expert,skeptic,practitioner
python "${SKILL_DIR}/scripts/tier.py" "https://www.gov.cn/x"
python "${SKILL_DIR}/scripts/validate_report.py" --report report.md --ledger .research/session/ledger
```

注意：`--effort` 与 `--depth` 同时给出时以 `--effort` 为准；`--breadth N` 显式覆盖并行子 Agent 数。

---

## 版本号规范

- 主版本（X）：架构级变更（四阶段/四层/多 Agent 编排）
- 次版本（Y）：能力级新增（引擎/方法论/工具）
- 修订（Z）：修复与微调
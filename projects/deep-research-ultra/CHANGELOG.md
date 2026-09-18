# CHANGELOG — deep-research-ultra

> 本文件**单独**记录 skill 的版本更新历史、更新概览与迁移指南。
> SKILL.md 保持纯净，只含运行必需内容（触发条件/使用说明/工作流/约束）——见开发约束第 10 条。

---

## v6.5.0（2026-09-18）— 执行模型纠偏 + 引擎真实性自检（实跑失败驱动修复）

### 背景（真实故障现场）
用户实跑"logo/品牌 VIS 开源方案调研"时 skill 报"调用失败、结果只剩开头一句"。取会话日志
（`~/.qoder/logs/.../segments/*.jsonl`）定位到：

```
turn.finished turn_id=skill-deep-research-ultra data={"reason":"max_turns","num_turns":10}
```

**根因是架构级不匹配，不是网络或prompt问题**：

1. `context: fork` 下 skill 作为子 Agent 运行，只有 **10 turn** 预算；四阶段工作流需要
   25-40 次工具调用 → 第 10 轮刚发完最后一批搜索就被掐断，报告从未生成，主 Agent 只拿到
   它的开场叙述（"只返回开头一句"的真相）。
2. 那 10 个 turn 里 **7 个耗在探索性空转**（`ls` skill 目录、读目标项目 package.json/
   tailwind/Icon.tsx、跑 `--help`），因为第 1 个动作 `--env-check` 就在 Windows GBK 控制台
   `UnicodeEncodeError` 崩了，Agent 只能自行摸索绕过。
3. fork 内 `AskUserQuestion` 不可用（Phase 1 澄清门依赖它）、嵌套 `Agent` 派发不可靠
   （Phase 2.5 依赖它）——fork 与本 skill 的编排定位从设计上冲突。

### 架构变更

| 变更 | 说明 |
|------|------|
| 移除 `context: fork` / `agent:` | Lead 改为当前主 Agent 内联执行；上下文隔离交由 Phase 2.5 的子 Agent 承担检索扇出（Lead 只读汇总与账本状态） |
| 新增 Phase 6 交付契约 | 报告一律落盘 `.research/<session>/report.md`，最终回复固定 ≤25 行短摘要（路径+一句话结论+要点+质量+未决）；快撑不住时先落盘再说话 |
| 新增「零、执行模型与冷启动」 | 说明为何不 fork + 前三个动作硬约束（禁止探索 skill 自身/禁止代码考古/首 turn 并行跑完 Phase 0） |
| Phase 0 加 `--probe` 门 | 环境门之外必须做引擎功能自检，全灭则不开工 |

### P0 修复：Windows 控制台崩溃
- 新增 `scripts/console.py:force_utf8()`，7 个 CLI 入口（research/ledger/panel/tier/
  validate_report/repo_health/env_check）在 main 前强制 UTF-8，不再需要调用方设
  `PYTHONIOENCODING`；回归测试断言"不崩 + 中文以 UTF-8 落管道"
- 顺带修掉 `--list`/`--mcp-check`/`--plan-only`/HTML 页脚里硬编码的 `v4.0` banner，
  版本号改为从 SKILL.md frontmatter 单源读取（`skill_version()`）

### P0 修复：引擎"假可用"
| 问题（实测） | 修复 |
|------|------|
| Gitee v5 搜索端点匿名请求恒返回 `[]`（带无效 token 才回 401），`--list` 却标 ✅ | `GiteeEngine.requires_config=True` + `GITEE_TOKEN`，无 token 直接判不可用；请求带 `access_token` |
| ModelScope 关键词搜索端点（dolphin/models）已 404，恒 0 结果 | 收缩为**模型卡详情查询**（`/api/v1/models/{Path}/{Name}` 实测 200），不再声明 `search` 能力；文档同步 |
| 裸数组空响应被折叠成 `None`，"0 结果"与"引擎坏了"混为一谈 | 契约分流：`None`=不可用，`[]`=0 结果 |
| `--env-check` 只探测域名可达，socket 通就算 ✅ | 新增 `scripts/probe.py` + `research.py --probe`：按引擎定制探针查询，输出 ✅N条/⚠️0结果/❌原因/⏭跳过 四级判定，≥1 个 ✅ 才放行 |
| 搜索 0 结果时统一甩锅"所有引擎都不可用，请运行 --mcp-check" | cmd_search 分别列出「已调通但 0 结果」与「未取到数据」的引擎名，并指向 `--probe` |
| 引擎返回 None 后没人知道为什么（arXiv 实为 HTTP 406） | `engines/fallback.py` 记录 `LAST_HTTP_ERROR`，`--probe` 直接印出 `HTTP 406`/`缺少配置: X` |

### P1 修复
- **相关性过滤**：新增 `research.py:filter_by_relevance()` + `--min-relevance`（**默认 50**）。
  此前中文查询"向量数据库 开源"经 OpenAlex 带回土地覆盖/图像质量论文，因总分把权威/时效
  与相关性混加权而得 60-68 全部放行。策略：高相关结果够数才丢弃，不够数保留并显式告警
  （避免跨语言查询被误杀成空报告）。
  阈值按实测标定：`"vector database open source license"` 的 6 条垃圾结果（Open Babel/
  Bioconductor/OQMD/Astropy/OsiriX）relevance 落在 45-55 之间，30 全放行、45 只报 2 条、
  50 起告警；而 `"retrieval augmented generation survey"` 的 6 条真相关结果在 50 下零误报。
  另测 `title_and_abstract.search:` 过滤虽更严但仍混入"疟疾媒介/视网膜血管"，故不改查询构造，
  改由告警把问题暴露给 Lead
- **MECE 维度兜底**：`plan.py` 未命中主题模板时回退 `['综合']` → deep 也只生成 1 个子问题，
  breadth=8 的并行编排整体落空（实测）。改为 `GENERIC_DIMENSIONS` 5 维骨架兜底，并在
  SKILL.md 明确"问题树由 Lead 拆，`--plan-only` 必须带 `--dimensions`"
- 显式 `--sources` 点名的引擎即使未声明 `search` 能力也会被调用（否则文档里的
  `--sources modelscope` 详情查询是空头支票；已实测可用）

### 文档纠偏
- README：`30 引擎`→`32 数据源`、`124 用例`→`176 用例`、`v6.0`→`v6.5`、evals 场景数 37→38
- **14 份 references 调研文档从安装目录回收进版本库**（`GitHub深度搜索技巧调研.md`、
  `intelligent-routing-research.md`、`optimization-plan-v5.md`、`大厂方法论落地调研-v2.md`、
  `论文全文与引用图谱调研-v2.md`、`浏览器自动化与反爬虫调研-v2.md`、
  `调研报告格式最佳实践调研.md`、`国内大厂深度研究方案调研-v3.md`、
  `深度研究开源项目调研-v3.md`、`国内智能体平台与调研专家团调研.md`、
  `anti-bot-research-2026.md`、`大厂深度研究方法论调研报告.md`、
  `开源深度研究项目调研报告.md`、`科研论文检索方案调研报告.md`）。
  它们此前只存在于 `~/.agents/skills/deep-research-ultra/references/`，
  研仓库里的 `references/` 缺这 14 份 → SKILL.md §17 的链接在版本库视角下全是死链
- 新增 3 条防漂移断言（`test_v6.py::TestDocConsistency`）：SKILL.md 不得回退到 fork 执行、
  引用的 references 必须真实存在、CLI banner 版本单一来源于 SKILL.md frontmatter
- §15 代码结构补齐 console/probe/similarity/repo_health/platform_engines 与 3 个新测试文件
- 引擎数口径统一为「32 个数据源：28 个可搜索，15 个支持 --probe」
- `.gitignore` 增加 `.research/`（Phase 6 产物目录约定）
- requirements.txt 去掉过时的 v5.0 标注

### 测试

146 → **176 passed**（+30：GBK 控制台冒烟 4、probe 判定 9、平台引擎真实性契约 3、
arXiv 端点与诊断透出 3、plan 维度兜底 3、相关性过滤 4、文档一致性守护 3、其余为契约修正）

### 已知限制（如实记录）
- **arXiv 直连不稳定**：部分查询（`transformer`、`all:"vector database"` 等宽/零命中查询）
  被服务端判 `HTTP 406`，规则未见官方文档说明，冷却 45-180s 仍复现。学术调研主力请用
  `openalex` / `semantic-scholar`；`--probe` 会把该失败如实标为 ❌ 并附 406 原因
- **Gitee 需 `GITEE_TOKEN`**（v6.1 宣传的"免费公开 API 无需 key"不成立）
- **ModelScope 不再参与关键词搜索**，只按精确 model id 取模型卡（许可证/下载量，供六维门取证）
- 移除 fork 后调研在主 Agent 展开，长报告会占用更多主上下文——用子 Agent 扇出 +
  文件化交付控制在 Phase 6 的短摘要内

---


## v6.4.0（2026-09-18）— 语义级 claim 聚类（解决 v6.3 遗留的两处语义盲区）

### 背景
v6.3 审查遗留两项架构级盲区：① 独立来源按 URL 并集计数 → 同一通稿跨站转载被当作 N 个独立来源，sufficient 虚高；② claim 聚类靠字面词集 Jaccard → 近义改写漏聚（"主流 LLM 架构" vs "主流大模型架构"）、数值矛盾（10x vs 2x）被判相似并入组而未标注。

### 新功能

| 能力 | 说明 | 模块 |
|------|------|------|
| 转载指纹去重 | 标题归一化（去站名/转载/栏目冗余词）→ 同指纹多来源只算 1 个独立来源；dedupe 时组内优先保留官方域 | scripts/similarity.py（新） |
| 语义化聚类 | 判据双通道：字符 n-gram 相似度 OR 核心 token（汉字 2-gram+英文词）重叠 ≥2 → 覆盖近义改写 | similarity.group_by_similarity |
| 数值矛盾检测 | 提取数值（倍/x/%/万/亿等），同单位差异 >20% 且同主题 → 判矛盾，入 Contradiction（带差异比） | similarity.numeric_conflict + verify._detect_numeric_contradictions |
| 全链路接线 | ledger.status 新增 effective_sources（指纹去重独立数）；sufficient/insufficient 判定改用有效独立数；validate_report 校验 2b 同步对齐 | ledger.py / validate_report.py |

### 变更文件

- 新增：`scripts/similarity.py`（纯标准库，中文/英文混合文本可用，一次全部测试）
- 修改：`scripts/verify.py`（聚合替换 + 数值矛盾补充）、`scripts/ledger.py`（effective_sources + 判据）、`scripts/validate_report.py`（2b 对齐）、`tests/test_v6.py`（+6 用例）、`SKILL.md`（version）、`CHANGELOG.md`

### 测试

140 → **146 passed**（+6：转载判定/有效独立数/近义聚类/数值冲突/verify 集成二项）

### 端到端验证

- 3 站转载 + 1 独立原文 → effective_sources=2、sufficient=True（转载被合并，不再虚高）
- 纯 2 站转载（无独立）→ effective_sources=1、sufficient=False、insufficient_claim_ids 命中

---

## v6.3.0（2026-09-18）— 真实性验证链重建（审查驱动修复）

### 背景
三维审查（代码/架构/内容）评分 62/100，发现 6 项 P0：verified 语义污染、Gitee 引擎契约错误、反思循环读空账本、矛盾检测死代码、六维门无实现、引用校验弱契约。本次系统性修复并强化真实性机制。

### P0 修复（真实性核心）

| 问题 | 修复 |
|------|------|
| verified 语义污染：搜索结果未经交叉验证直接落盘 `status='verified'`，账本覆盖率虚高 | `ledger.add_claim` 默认/非法 status 改 `pending`；`research.py` 落盘按交叉验证结果分流（verified/conflict/pending），confidence 分级 0.8/0.3/0.4 |
| 反思循环读空账本（落盘在反思之后） | 落盘前移到交叉验证后、反思循环前；缓存命中也落盘（此前 `--ledger` 二跑命中缓存导致账本为空） |
| verify.py contradicted 死代码：从已过滤列表回找矛盾 claim 恒空 | 先收集后过滤；矛盾 claim 计入 total_claims，verification_rate 不再虚高 |
| GiteeEngine 必然崩溃（API 实测返回裸数组，代码按 dict 取 items） | 兼容 list/dict 两种契约 |
| 六维质量门无实现 | validate_report 新增校验 6：报告含仓库链接时检查六维要素齐备（缺维拦截） |
| 引用校验只查数字范围 | 新增引用反查：编号 N 的来源 URL/标题须出现在报告中；extract_citations 排除 `[N]:` 定义行 |

### P1 修复

- **sufficient 判据 claim 级化**：每条 verified claim 独立来源 ≥2（旧 topic 级 URL 并集判据可被多条单源 claim 虚假满足）；输出 insufficient_claim_ids
- **断路器接线**：cmd_search 搜索循环内 record_success/failure + OPEN 跳过（此前状态恒 CLOSED）
- **[N] 强契约**：export_json 注入稳定 `primary_index` 编号，报告与校验门共用
- **`--depth extreme` 静默降级**：DEPTH_PRESETS 补 extreme 条目（12 子问题/8 源/20-40 分钟）
- **reflect off-by-one**：`--reflect-rounds 3` 实际只跑 2 轮 → 修为完整 3 轮
- **缓存 key 缺参**：补 ledger/effort/breadth/perspectives/reflect_rounds
- **cmd_search 计划生成不透传参数**：补 perspectives/goal/dimensions/time_range
- **ModelScope 运算符优先级**：path 为空时 Name 被整组丢弃 → 显式分支
- **repo_health**：LGPL-or-later 误判 strong → 归一化后缀比对；OSV severity 截断 CVSS 向量 → 修正
- **env_check**：oss-finder 移入可选；网络探测全部可选化（单点不通不阻断，走降级链）
- **validate_report CLI**：`_opt` 尾参 IndexError 容错；"每 topic ≥1 verified" warning→issue

### 内容修正（SKILL.md）

- 引擎数 30 → **32**（含 Layer2 12→14）；CRAAP 标度 0-20 → 0-100（与实现一致）
- 引用不存在的函数名修正：cross_validate→CrossVerifier.verify、score_with_craap→CraapScorer.score、build_issue_tree→PlanGenerator.generate_plan
- 子 Agent 模板 status verified→pending + 「verified 只能由 Lead 交叉验证赋予」语义框
- Phase 2.5 补并发写安全约定（子 Agent 分片文件 + merge，不直写共享 jsonl）
- Phase 5 校验门表格补 3 项 v6.3 校验（引用反查/独立来源强度/六维要素）

### 测试

96 → **140 passed**（+5 v6.3 用例：落盘分流/引用反查/六维缺失/primary_index 稳定/默认 pending；修正 test_should_stop_max_rounds 适配 off-by-one 修复）

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
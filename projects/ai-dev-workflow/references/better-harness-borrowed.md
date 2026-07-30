# Better Harness 借鉴笔记（v3.4 内部沉淀）

> **文档定位：** 本文件不是给 Skill 用户看的，是 v3.4 升级过程的内部研究沉淀，记录 Better Harness 哪些思想被借鉴、哪些不照搬、为什么。
> **调研日期：** 2026-07-30
> **调研对象：** 阿里 Qoder 2026-07-28 开源的 [Better Harness](https://github.com/QoderAI/better-harness)（MIT 协议，825 stars / 57 forks at 2026-07-30）
> **v3.4 升级负责人：** AI 开发顾问
> **关联 Skill 版本：** ai-dev-workflow v3.4

---

## 0. 一句话结论

> Better Harness 的 4 大范式（Configured ≠ Exercised / 4 级证据状态 / Task Episode 评估单位 / Finding 四要素）解决了"清单驱动"vs"证据驱动"的根本性差距——v3.3 绿门全禁只回答"跑什么"，Better Harness 补足了"跑没跑通"。

---

## 1. Better Harness 调研笔记

### 1.1 基本信息

| 维度 | 信息 |
|------|------|
| 名称 | Better Harness |
| 仓库 | https://github.com/QoderAI/better-harness |
| 协议 | MIT |
| 发布时间 | 2026-07-28 |
| Stars | 825 / Forks 57（2026-07-30 查询） |
| 适配平台 | Claude Code / Codex / Qoder / Cursor / Qwen Code |
| 评估规模 | 30 个 GitHub 真实项目首轮评测 |
| 自身评分 | Qoder 用它审自己仓库 → 58 分（说明早期阶段，需要持续完善） |
| 主仓库结构 | `.agents/skills/` + `.claude-plugin/` + `.codex-plugin/` + `.cursor-plugin/` + `references/` + `models/` + `skills/better-harness/` + `templates/` + `case-studies/` |
| 关键文档 | `models/agent-work-loop.md`（812 行，5 维度评估模型的权威定义）|

### 1.2 5 维度 × 3 检查 = 15 个稳定 ID

| 维度 | 3 个检查 | 含义 |
|------|---------|------|
| **Task Understanding**（任务理解）| goal-understanding / relevant-context / scope-boundary | agent 是否理解目标、应用相关上下文、保持范围 |
| **Controlled Execution**（可控执行）| instruction-led-start / supported-operation / permission-boundary | 是否走支持路径、保持权限边界 |
| **Change Validation**（变更验证）| relevant-check / failure-repair / validate-again | 验证是否相关、失败诊断与修复、修复后重验 |
| **Reliable Delivery**（可靠交付）| acceptance-evidence / high-risk-approval / rollback-recovery | 真实交付边界、风险审批、回滚恢复 |
| **Learning Capture**（经验沉淀）| lifecycle-repeat-detection / loop-engineering / later-validation | 重复机会检测、循环工程、纵向验证 |

### 1.3 4 级证据状态

| 状态 | 含义 | 分数上限 |
|------|------|---------|
| **Present** | 机制/文件/配置存在 | 74 |
| **Wired** | 任务/事件能触达 | 84 |
| **Exercised** | 在某个具体任务/事件中实际使用并留结果 | 94 |
| **Outcome-supported** | 在后续可比任务中验证有效 | 100 |
| Missing | 确认缺失 | 59（封顶）|
| Unobserved | 观察边界外（不算失败）| 59（封顶）|
| Not applicable | 不适用 | 59（封顶）|

**关键设计：** "**Configured ≠ Exercised**"——配置存在不等于真的在工作。`Present` 与 `Exercised` 之间差 `Wired` 一档；`Exercised` 与 `Outcome-supported` 之间差"后续可比任务验证"。

### 1.4 Finding 四要素范式

每条 Finding 必须包含：
1. **Evidence**（可追溯证据）— 文件:行 / 命令输出 / 截图
2. **Impact**（用户影响）— 量化"不修的后果"
3. **Smallest repair boundary**（最小修复边界）— 文件/owner
4. **Validation route**（验证方式）— 修复后机械验收

### 1.5 评估单位：Task Episode

> 一个用户目标 + 一个验收边界 = 一个 Task Episode。**所有 Finding 必须挂到具体的 Task Episode 上**，不能挂在仓库或会话上。

**与"仓库/会话"评估的区别：**
- 仓库评估 = 静态资产盘点（"项目里有测试"）
- 会话评估 = 时间序列统计（"这次会话跑了 3 次 lint"）
- Task Episode 评估 = 任务级行为证明（"用户报 Token 用量页空白，AI 改了 5 个文件，跑了端到端测试，确认页面上有 5 条数据"）

### 1.6 三类证据采集

| 证据类型 | 含义 | 来源 |
|---------|------|------|
| **Session Evidence** | 任务会话记录 | ~/.claude/、~/.codex/ 等 |
| **Project Harness** | 项目静态资产 | AGENTS.md / Skills / MCP / Hooks / Memory / Tests / CI |
| **Agent Customize** | Agent 定制参数 | 命令前缀、插件、Custom Agents |

---

## 2. v3.3 现状 vs Better Harness 差距分析

### 2.1 我们 v3.3 强项（Better Harness 没有的）

| v3.3 内容 | Better Harness 对应物 |
|---------|-------------------|
| **5 条 L0 红线**（不可违反）| 无（Better Harness 走"评分制"）|
| **12 条 L1 强约束**（按场景适配）| 无（Better Harness 走"评估模型"）|
| **绿门全禁三层金字塔**（L1/L2/L3）| 部分对应（Change Validation 维度）|
| **6 阶段开发流程** | 无（Better Harness 只做"评估"不做"开发"）|
| **neat vs 循环工程分工** | 无 |
| **65 个评测场景** | 无（Better Harness 跑真实项目做证据评估）|

### 2.2 我们的差距（Better Harness 补足的）

| 差距 | Better Harness 解决方案 | 我们的 v3.4 借鉴 |
|------|---------------------|--------------|
| **清单驱动** vs **证据驱动**：我们只说"必跑" | 4 级证据状态，强制落到证据 | 0.2.7 节：4 级证据状态 |
| **项目级评估** vs **任务级评估**：我们的门禁是项目级 | Task Episode 评估单位 | 0.3 节：5 维 15 问任务级复盘 |
| **Finding 无四要素**：我们的审查报告只写"问题+建议" | 强制 Evidence/Impact/Repair/Validation | 0.3.4 节：审查时强制 Finding 四要素 |
| **AP-18 审计盲信无解药**：只说"必须 Read+Glob"但没说"如何判定" | 证据状态分类 | AP-21 借证据哲学，AP-22 借评估单位 |

### 2.3 借鉴 vs 不照搬

| 项 | Better Harness 做法 | v3.4 处理 | 理由 |
|----|------------------|----------|------|
| 跑插件/CLI | 需 Qoder 桌面或 Marketplace | **不照搬** | 我们做的是 skill 规范文档，不是插件 |
| 30 个真实项目基准 | 用了 | **不照搬** | 我们用 70 个 eval 场景替代 |
| 5 维度命名 | 完全沿用（Task Understanding 等英文）| **借鉴思想** | 改为"任务级 5 维复盘"，避免与 Better Harness 商标冲突；保留英文作为索引 |
| 7 个证据状态 | Present/Wired/Exercised/Outcome-supported/Missing/Unobserved/N/A | **借鉴 4 状态** | 合并 Missing/Unobserved/N/A 为"待定"；简化认知负担 |
| 35-100 分制 | 用 | **不照搬** | v3.3 已明确"不评分"，保留 L0 红线 + L1 强约束两级 |
| 200 份 Spec 累积 | 用 | **不照搬** | v3.4 加入"任务级 spec 自检"思想但不做 Spec 库 |
| Finding 评分系数 | 用 | **不照搬** | 我们只看 4 要素是否齐全，不打分 |
| qoder-action GitHub Action | 提供 | **不照搬** | 与 v3.3 保持一致：跨项目通用规范，不绑定 Qoder 平台 |

---

## 3. v3.4 借鉴落地清单

### 3.1 SKILL.md 新增内容

| 位置 | 内容 | 行数（估算）|
|------|------|----------|
| 头部 | v3.4 版本说明 + 4 个核心变化 | ~13 行 |
| 0.2.7 节 | 证据驱动范式（4 级证据状态 + 6 场景 + 绿门映射）| ~55 行 |
| 0.3 节 | 任务级 5 维复盘（15 问 + 执行规则 + 与绿门关系 + Finding 四要素）| ~68 行 |
| AP 表 | AP-21/22/23 三个新反模式 | +3 行 |

### 3.2 references 详细文档

| 文档 | 定位 | 状态 |
|------|------|------|
| `better-harness-borrowed.md`（本文档）| v3.4 升级内部沉淀，给后续维护者看 | ✅ 已创建 |
| `green-gate-mechanism.md` | 绿门全禁三层金字塔详细说明 | v3.3 已创建 |
| `neat-vs-loop.md` | neat vs 循环工程分工详细说明 | v3.3 已创建 |

### 3.3 evals.json 是否新增？

用户明确选择**不加**新 eval（借鉴范围 0.2.7/0.3/AP-21~23，**未选 eval-066~070**）。AP-21/22/23 在 v3.5 或后续版本可补 eval 验证。

---

## 4. v3.4 vs v3.3 价值差异

| 维度 | v3.3 | v3.4 |
|------|------|------|
| **核心哲学** | 规则驱动 + 清单驱动 | 规则驱动 + **证据驱动** |
| **评估粒度** | 项目级 | 项目级 + **任务级** |
| **审查产出** | "问题+建议" | "Evidence + Impact + Repair + Validation" |
| **AI 自我声明** | "我加了 X 配置" | "我加了 X 配置，处于 [Wired] 状态，[未跑验证]" |
| **源头预防能力** | 弱（清单易跳过）| 强（任务级 15 问 + 4 级证据）|

---

## 5. 待跟进（v3.5+ 候选）

1. **新增 eval-066~070**：5 个评测场景验证 0.2.7/0.3/AP-21~23 行为
2. **借鉴 Better Harness 的"lifecycle-repeat-detection"**：在 LEARNINGS.md 中自动检测"是否重复犯过的错"
3. **借鉴 Better Harness 的"loop-engineering"**：在 0.5 节新增"循环工程"专章，明确"哪些重复工作应转 Skill/Hook"
4. **借鉴 Better Harness 的"纵向验证"（later-validation）**：建立跨任务的"经验被复用率"指标
5. **借鉴 qoder-action 的 AGENTS.md 模板**：在 templates/AGENTS.md 加入"审查规则块"，让用户能直接复用 Qoder 的审查规范模板

---

## 6. 参考链接

- [Better Harness 仓库](https://github.com/QoderAI/better-harness)
- [Better Harness 中文博客（Phodal）](https://m.sohu.com/a/1055911786_385076/)
- [agent-work-loop.md 评估模型定义](https://github.com/QoderAI/better-harness/blob/main/models/agent-work-loop.md)
- [Qoder 企业版发布](http://m.toutiao.com/group/7661829953100546579/)
- [qoder-action GitHub Action](https://github.com/QoderAI/qoder-action)
- [Harness Engineering by Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)

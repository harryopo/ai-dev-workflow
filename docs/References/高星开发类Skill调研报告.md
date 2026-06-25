# 高星开发类 Skill 调研报告

> 调研时间：2026-06-24
> 覆盖范围：代码编译审查、工程文件管理、开发监督等相关的高星 Agent Skills

---

## 一、开发类 Skill 全景概览

当前 Agent Skills 生态已极度繁荣：
- **Anthropic 官方 skills 仓库**：153K+ Stars
- **SkillsMP 市场**：96,000+ 个 Skills
- **antigravity-awesome-skills**：41K+ Stars，1,600+ 个 Skills
- **兼容平台**：Claude Code、Codex CLI、Gemini CLI、Cursor、Windsurf、GitHub Copilot 等 14+ 平台

---

## 二、高星开发类 Skill 推荐 (分级)

### 🏆 殿堂级 (100K+ Stars)

| # | 项目 | Stars | 核心定位 | 安装 |
|---|------|-------|---------|------|
| 1 | **everything-claude-code** | ~99.9K | 28个专业子Agent、119个Skills、60个斜杠命令、34条规则、20+Hooks、14个MCP服务器 | `npx skills install everything-claude-code` |
| 2 | **mattpocock/skills** | ~140K | TypeScript 大佬的工程纪律技能包：/grill-me（需求对齐）、/tdd（TDD循环）、/diagnose（调试）、/improve-codebase-architecture（架构审查） | `npx skills@latest add mattpocock/skills` |
| 3 | **cc-switch** | ~105K | 跨平台 AI 编程助手增强工具，一键切换 API 节点、Skills 统一管理 | git clone 后配置 |

### 🥈 高效必备 (10K-50K Stars)

| # | 项目 | Stars | 核心定位 | 安装 |
|---|------|-------|---------|------|
| 4 | **obra/superpowers** | ~29K | 完整软件开发方法论框架：Brainstorming→Plan→TDD→Code Review→Finish | `npx skills add obra/superpowers` |
| 5 | **pbakaus/impeccable** | ~10K | 前端设计审计与润色：/audit、/arrange、/typeset、/polish | git clone 后使用 |
| 6 | **OthmanAdi/planning-with-files** | ~17.7K | 持久化任务管理，Manus 风格，跨会话保存进度 | git clone |

### 🥉 专业领域 (4K-10K Stars)

| # | 项目 | Stars | 核心定位 | 安装 |
|---|------|-------|---------|------|
| 7 | **trailofbits/skills** | ~4.1K | Trail of Bits 安全审计专家，40+ 安全审核插件 | `/plugin marketplace add trailofbits/skills` |
| 8 | **Lum1104/Understand-Anything** | ~7.2K | 代码知识图谱生成，交互式 Web 仪表盘 | git clone |
| 9 | **SawyerHood/dev-browser** | ~5.1K | 给 Claude 装浏览器，测试已部署功能 | git clone |
| 10 | **context7 (intellectronica)** | ~5K | 实时文档检索，避免 API 幻觉 | `npx skills add intellectronica/agent-skills --skill context7` |

---

## 三、按功能分类详解

### 3.1 代码编译/审查类 (Code Review & Compilation)

#### TRAE-code-review (已内置)
Claude Code 内置的代码审查 Skill，支持多维度审查。

#### c-review (Trail of Bits)
- **Stars**: 4.1K (parent repo)
- 专业的 C/C++ 安全审查，覆盖内存破坏、整数溢出、竞态条件等
- 支持并行工作线程和 SARIF 输出

#### codeql (Trail of Bits)
- CodeQL 静态分析套件
- 支持安全扫描、数据扩展模型、SARIF 处理

#### semgrep (Trail of Bits)
- 多语言静态分析，支持并行子代理执行
- 支持"run all"和"important only"两种模式

#### code-review (Claude Code 内置)
- `/review` 和 `/ultra review` 命令
- 审查 bug、边界条件、设计问题

#### frontend-code-review (社区)
- 流行度评分：126.3K
- 前端代码审查，tsx/ts/js 检查清单

#### github-code-review (社区)
- 流行度评分：48.2K
- 多智能体协同评估的 GitHub 代码审查

### 3.2 工程文件/架构类 (Engineering Files & Architecture)

#### mattpocock/skills — 工程纪律套装
| Skill | 功能 |
|-------|------|
| `/grill-me` / `/grill-with-docs` | 需求深度对齐，写代码前确保理解一致 |
| `/tdd` | 强制红-绿-重构 TDD 循环 |
| `/diagnose` | 系统性调试四步法：重现→最小化→假设→验证 |
| `/improve-codebase-architecture` | 识别模块深度不足，生成 before/after 报告 |
| `/to-prd` / `/to-issues` | PRD 撰写与 Issue 拆分 |
| `/triage` | Issue 状态机管理 |
| `/handoff` | 上下文交接，防止跨会话信息丢失 |
| `/setup-matt-pocock-skills` | 一次性项目初始化 |

#### obra/superpowers — 7 步开发方法论
| 步骤 | Skill | 功能 |
|------|-------|------|
| 1 | Brainstorming | 苏格拉底式提问深化需求 |
| 2 | Git Worktrees | 自动创建隔离分支 |
| 3 | Writing Plans | 分解为 2-5 分钟小任务 |
| 4 | Subagent-Driven Dev | 子代理执行 + 两阶段审查 |
| 5 | Test-Driven Dev | 强制红-绿-重构 |
| 6 | Code Review | 任务间隙自动审查 |
| 7 | Finish Branch | 验证测试 + 合并/保留/丢弃 |

### 3.3 开发监督类 (Development Supervision)

#### everything-claude-code — 全栈开发监督
- **28 个专业子 Agent**：code-reviewer、security-reviewer、tdd-guide、语言特定审查等
- **20+ Hooks**：PreToolUse、PostToolUse、SessionStart、SessionEnd
- **60 Slash Commands**：`/tdd`、`/plan`、`/e2e`、`/learn`
- **AgentShield 安全机制**：隔离执行环境
- NanoClaw v2 引擎：模型路由 + Skill 热加载

#### Trail of Bits 安全审计系列
- **audit-context-building**: 细粒度代码分析上下文构建
- **audit-prep-assistant**: 基于 Trail of Bits 清单的审计准备
- **differential-review**: 安全聚焦的差异审查
- **fp-check**: 误报验证系统
- **code-maturity-assessor**: 9 维度代码成熟度评估
- **spec-to-code-compliance**: 规范到代码的一致性检查

#### 质量与测试监督
- **write-tests** (claudeskills.info)：自动测试生成，并行子代理编写
- **fix-tests**：失败测试自动修复
- **review-pr / review-local-changes**：PR 审查 / 本地变更审查
- **property-based-testing**：基于属性的测试指导
- **mutation-testing**：变异测试配置与优化

---

## 四、安装方式速查

| 来源 | 安装命令 |
|------|---------|
| **mattpocock/skills** | `npx skills@latest add mattpocock/skills` |
| **Anthropic 官方** | `npx skills add anthropics/skills` |
| **Trail of Bits** | `/plugin marketplace add trailofbits/skills` |
| **Superpowers** | `npx skills add obra/superpowers` |
| **Awesome Skills** | `npx skills add sickn33/antigravity-awesome-skills` |
| **Everything Claude Code** | `npx skills install everything-claude-code` |
| **Context7** | `npx skills add intellectronica/agent-skills --skill context7` |
| **Impeccable** | `git clone https://github.com/pbakaus/impeccable` |

---

## 五、推荐组合方案

### 🎯 通用开发组合（全栈）
```
mattpocock/skills        # 工程纪律 + 需求对齐 + TDD + 调试
obra/superpowers         # 完整开发方法论框架
context7                 # 实时文档检索
```

### 🛡️ 安全优先组合（安全审计/区块链）
```
trailofbits/skills       # 40+ 安全审计插件
semgrep + codeql         # 静态分析
fp-check                 # 误报验证
```

### 🎨 前端专注组合
```
pbakaus/impeccable       # 设计审计
frontend-design          # 前端设计
frontend-code-review     # 前端代码审查
```

### 🏗️ 工程管理组合
```
mattpocock/skills        # 工程纪律
everything-claude-code   # 全栈监督
planning-with-files      # 持久化项目管理
understand-anything      # 代码知识图谱
```

---

## 六、已安装的 Trail of Bits 安全技能

当前本地已有（`d:\ai\claude code\skill开发\.agents\skills\`）大量 Trail of Bits 安全技能，包括：

- **c-review**: C/C++ 安全审查
- **codeql**: CodeQL 静态分析
- **semgrep / semgrep-rule-creator**: 半格分析 & 规则创作
- **differential-review**: 差异安全审查
- **fp-check**: 误报验证
- **variant-analysis**: 变体分析（找相似漏洞）
- **constant-time-analysis**: 常量时间分析（时序攻击检测）
- **trailmark**: 代码图分析
- **supply-chain-risk-auditor**: 供应链风险审计
- **mutation-testing / property-based-testing**: 变异测试 & 属性测试
- 及多个智能合约安全扫描器

---

## 七、调研总结

### 核心发现
1. **最值得装的开发类 Skill 是 mattpocock/skills**（140K Stars），它直接解决 AI 编码的四大失败模式
2. **开发方法论框架 obra/superpowers**（29K Stars）是完整开发生命周期管理的标杆
3. **安全审计方面 Trail of Bits** 是权威，40+ 插件覆盖全面
4. 已安装的 Trail of Bits 技能已相当全面，可在此基础上补充工程开发方法论类的 Skill

### 建议下一步
1. 安装 mattpocock/skills 作为工程纪律基础
2. 安装 obra/superpowers 作为开发方法论框架
3. 安装 context7 解决 API 文档实时查询问题
4. 评估是否需要 everything-claude-code（功能最全但较重）

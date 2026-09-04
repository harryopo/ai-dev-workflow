---
name: skill-workspace
version: 5.4.0
description: |
  Skill 全生命周期工作台 v5.4.0。当用户提到"skill工作台"、"管理skill"、"搜索skill"、
  "下载skill"、"优化skill"、"部署skill"、"合并skill"、"MCP整合"、"工作流蒸馏"、
  "开发记忆"、"清洗skill"、"清理源码"、"释放磁盘"、"删掉下载的源码"时触发。
  开发和审查功能由子技能处理。
  面向所有 Agent（Claude Code、TRAE、Codex CLI、Cursor、Windsurf、Gemini CLI、ChatGPT 等），
  一站式完成 Skill 的搜索、下载、安全审查、开发生成、MCP整合、优化改进、质量测评、
  多平台部署、合并整合、更新卸载、工作流蒸馏、开发记忆、发布清洗与源码工作区磁盘回收。
  支持 Skills-for-Skills 范式（用 Skill 审计/创建 Skill）。
argument-hint: "[子命令] [参数]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob Grep Bash WebFetch
---

# Skill 全生命周期工作台

一站式 Skill 管理平台，覆盖 Skill 从发现到退役的完整生命周期，支持 MCP 协议整合、多平台部署、工作流蒸馏与开发记忆管理。

## 核心原则

> **先检查环境，深入理解需求，全网搜索最佳方案，MCP与Skill互补架构，分阶段开发，循环审查，完整交付。**
>
> **用户在做任何有关 Skill 的事情时，都需要用 LLM 的能力进行对话提问，确保方案正确、方向越发清晰。**
>
> **架构原则：MCP 连外部工具，Skill 管内部知识 — 二者互补而非替代。**
>
> **记忆原则：开发记忆沉淀到 .dev-memory.md，不污染主文档；发布前自动清洗，确保产物纯净。**
>
> **编排者哲学：大型 Skill 应调度其他 Skill/MCP 作为子流程，而非重复造轮子。SKILL.md 只含路由表和调度逻辑，子流程独立封装在 subskills/，实现薄入口、低 Token 消耗、高可维护性。**
>
> **防递归硬约束：子 Agent prompt 中禁止出现父 Skill 的触发词，避免无限循环。**

## 评估体系

本工作台统一使用 **Darwin 9 维度评估体系**（基于 SkillLens 论文实证验证），满分 100 分。

**详细评分标准：** `${SKILL_DIR}/references/darwin-rubric.md`

**评级标准：** A（90-100 强烈推荐）/ B（75-89 值得一试）/ C（60-74 仍需改进）/ D（<60 建议重写）

---

## 子命令路由

| 子命令 | 说明 | 处理方式 |
|--------|------|----------|
| **开发** | 从零创建新 Skill（含需求深挖、全网搜索、方案推送、分阶段开发） | 加载 dev 子技能 |
| **合并** | 将多个相关 Skill 整合为一个更强大的 Skill | 本文件处理（流程七） |
| **审查** | Darwin 9 维度质量评分（100 分制） | 加载 review 子技能 |
| **搜索** | 在线搜索可用 Skill | 本文件处理 |
| **下载** | 从 URL/名称/GitHub 安装 Skill | 本文件处理 |
| **安全审查** | 对 Skill 做安全扫描（含语义-行为一致性检测） | 本文件处理 |
| **MCP整合** | 将 MCP Server 包装为 Skill 或 Skill 与 MCP 协同配置 | 本文件处理（流程八） |
| **工作流蒸馏** | 将一整套工作流蒸馏成大型 Skill（含知识库、代码、模板） | 本文件处理（流程九引导到 references/workflow-distillation.md） |
| **优化** | 改进现有 Skill 质量 | 本文件处理 |
| **部署** | 安装到全局目录（支持多平台），自动触发清洗检查 | 本文件处理 |
| **管理** | 更新、卸载、列表 | 本文件处理 |
| **开发记忆** | 沉淀开发记忆到 .dev-memory.md，或执行发布前清洗 | 本文件处理（流程十） |
| **清理源码** | 释放分析用 git 下载的第三方源码，回收磁盘 | 本文件处理（流程十一） |

**路由规则：**
1. 用户说"开发xxx skill" → 加载 `subskills/dev/SKILL.md`
2. 用户说"审查skill" / "skill评分" → 加载 `subskills/review/SKILL.md`
3. 用户说"合并skill" / "整合skill" → 在本文件中执行流程七
4. 用户说"MCP整合" / "包装MCP为Skill" / "Skill与MCP协同" → 在本文件中执行流程八
5. 用户说"工作流蒸馏" / "蒸馏工作流" / "把工作流做成skill" → 引导到 `references/workflow-distillation.md`
6. 用户说"开发记忆" / "沉淀记忆" / "清洗skill" / "准备发布" → 在本文件中执行流程十
7. 用户说"正式部署" / "部署到全局" / "开源" / "发布" → 先执行流程十清洗检查，再执行流程五部署，**部署验证通过后自动执行流程十一**
8. 用户说"清理源码" / "释放磁盘" / "删掉下载的源码" / "清理下载缓存" → 在本文件中执行流程十一
9. 其他子命令 → 在本文件中处理

**子技能加载：**
```
开发 → Read ${SKILL_DIR}/subskills/dev/SKILL.md
审查 → Read ${SKILL_DIR}/subskills/review/SKILL.md
```

---

## 流程零：环境检查

**目标：** 在任何操作开始之前，确保执行环境正常、依赖完整、网络通畅、权限充足。

**原则：** 先检查，后执行。缺失依赖自动提示并提供安装方案。**先问清环境，再动手检查。**

**详细指南：** `${SKILL_DIR}/references/workflow-details.md`（环境检查详细步骤）
**环境检查参考：** `${SKILL_DIR}/references/environment-check.md`

### 执行流程

```
第零步：环境问话 — 了解用户环境与偏好
  ↓
第一步：检查基础依赖是否安装（curl/git/python/node/npm）
  ↓
第二步：检查搜索增强 Skill 是否已安装（deep-research-pro/multi-search-engine）
  ↓
第三步：检查网络是否通畅（GitHub/SkillsMP/npm registry）
  ↓
生成环境检查报告 → 有缺失？→ 询问用户是否自动安装
```

### 环境问话（必问）

1. **操作系统与 Agent** — 确定依赖安装命令和全局 skills 路径
2. **网络环境** — 决定是否启用降级策略和镜像源
3. **已安装的搜索增强 Skill** — 判断搜索能力范围
4. **操作偏好** — 确定自动安装策略

**问话原则：** 根据用户回答动态调整后续问题，不假设用户环境。

**生成环境检查报告** → 保存到 `./artifacts/env/env-check-{date}.md`

---

## 流程一：搜索 Skill

**目标：** 在线查找用户需要的 Skill，避免重复造轮子。

**详细策略：** `${SKILL_DIR}/references/search-strategy.md`
**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（搜索详细步骤）

### 搜索前问话（必问）

1. **使用场景** — 个人项目 / 团队协作 / 企业生产 / 学习研究
2. **技术栈偏好** — Python / Node.js / Rust / Go / 无所谓
3. **功能优先级** — 核心功能完整 / 易用性 / 性能 / 安全性 / 文档完善 / 社区活跃
4. **集成方式** — 直接安装使用 / 改造后使用 / 参考实现自己写 / 仅作调研

### 搜索源（按优先级）

| Tier | 来源 | 命令 |
|------|------|------|
| 1 | SkillsMP | `curl -s "https://skillsmp.com/api/v1/skills/search?q={关键词}&limit=10&sortBy=stars"` |
| 2 | Skills.sh | `npx skills find {关键词}` |
| 3 | CocoLoop | `curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"` |
| 4 | GitHub | `curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"` |
| 5 | clawhub | `npx clawhub@latest search {关键词}` |
| 6 | 深度搜索 | deep-research-pro / multi-search-engine |

**GitHub 国内访问降级策略：** 直连 → 镜像站 → GitHub API → 代理 → 降级到 Tier 1-3

**搜索后：** 展示结果列表 → 询问用户是否安装 → 生成搜索结果报告 → `./artifacts/search/search-results-{date}-{keyword}.md`

---

## 流程二：下载/安装 Skill

**目标：** 从各种来源安全安装 Skill。

**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（安装详细步骤）

### 安装前问话（必问）

1. **安装位置** — 全局目录（~/.skills/）/ 当前工作区（./）/ 项目级（.skills/）
2. **版本选择** — 最新稳定版 / 最新开发版 / 指定版本 / 不在意
3. **安装后操作** — 立即测试 / 仅安装 / 安装并部署到其他 Agent

### 安装流程

1. **环境检查** — 调用流程零检查基础依赖
2. **获取 Skill 内容** — URL/名称/GitHub，国内走降级策略
   - ⚠️ git clone 必须落到 `.cache/sources/{时间戳}-{仓库名}/` 并写 `.skill-workspace-source` 标记，**禁止散落**
   - 优先 `curl` 只取 SKILL.md；确需全量分析才 clone，且加 `--depth 1`
3. **安全审查**（强制）— 评级 >= B → 继续；评级 <= C → 询问用户
4. **安装到工作区** — `cp -r {skill目录}/ ~/.skills/{skill名}/`
5. **确认安装结果**
6. **释放源码工作区**（如执行过 clone）— `release` + `auto`，详见 `${SKILL_DIR}/references/source-lifecycle.md`
7. **生成安装报告** → `./artifacts/install/install-report-{date}-{skill-name}.md`

---

## 流程三：安全审查

**目标：** 对 Skill 进行安全扫描，识别风险。基于 SkillProbe 研究成果，包含语义-行为一致性检测和组合攻击风险评估。

**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（安全审查详细步骤）

### 审查前问话（必问）

1. **审查重点** — 敏感数据泄露 / 危险命令执行 / 网络访问 / 权限范围 / 语义-行为一致性 / 组合攻击风险 / 全部检查
2. **风险容忍度** — 严格（任何 WARNING 都拒绝）/ 标准（仅 BLOCK 拒绝）/ 宽松（仅提示不拒绝）
3. **使用环境** — 个人开发机 / 团队共享 / 企业生产 / 沙盒环境
4. **已知问题** — 无 / 有（请描述）/ 不确定
5. **是否涉及MCP** — 是（需额外MCP安全检查）/ 否 / 不确定

### 审查协议（6 步，基于 SkillProbe 2026 研究）

1. **元数据检查** — name/version/description/author，验证来源可信度
2. **权限范围分析** — Read(Low)/Write(Medium)/Network(High)/Bash(Critical)，检查最小权限原则
3. **内容扫描** — BLOCK(敏感路径/危险命令/base64混淆) / WARNING(宽泛通配符/sudo/提示注入) / INFO(缺少元数据)
4. **语义-行为一致性检测**
   - description 描述的功能与实际指令是否一致
   - 示例输入输出与描述是否匹配
   - 是否存在"描述说做A实际做B"的欺骗性描述
   - 触发词边界是否清晰，是否会误触发相邻场景
5. **Typosquat 检测** — 单字符交换/同形异义字符/多余连字符/近似重名
6. **组合攻击风险评估**
   - Skill 权限组合风险（如 Write + Network = 数据泄露风险）
   - 与已安装 Skill/MCP 的交互风险
   - 链式调用风险（Skill A 调用 Skill B 调用 MCP）

**高危组合检测矩阵：**
| 权限1 | 权限2 | 风险等级 | 说明 |
|-------|-------|----------|------|
| Write | Network | 🔴 Critical | 可能读取敏感文件并外传 |
| Bash | Network | 🔴 Critical | 可能执行远程代码/反弹shell |
| Bash | Write | 🟡 High | 可能写入恶意脚本并执行 |
| Read | Network | 🟡 High | 可能读取敏感文件并外传 |

**输出：** 安全评级（SAFE/WARNING/DANGER/BLOCK）→ `./artifacts/reviews/security-review-{date}-{skill-name}.md`

---

## 流程四：优化 Skill

**目标：** 改进现有 Skill 的质量，解决具体问题。

**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（优化详细步骤）
**棘轮机制：** `${SKILL_DIR}/references/ratchet-mechanism.md`
**多评委评估：** `${SKILL_DIR}/references/multi-judge.md`

### 优化前问话（必问）

1. **优化目标** — 触发精准度 / 指令明确性 / 输出质量 / 性能 / 安全性 / 易用性
2. **具体问题** — 开放式问题，让用户描述具体问题
3. **优化优先级** — 最严重 / 最容易解决 / 影响最大 / 全部解决
4. **优化约束** — 不能改变触发词 / 不能增加文件大小 / 无约束
5. **验收标准** — Darwin 评分提升 / 用户实际测试 / evals 通过 / 多评委审查

### 优化流程

1. **诊断** — 先用「审查」流程找出问题
2. **制定方案** — 按优先级排列改进项
3. **执行改进** — description不准→改触发词；workflow有漏洞→补步骤；输出不合格→改格式
4. **验证** — 用同一个 case 跑一遍，确认改善
5. **回归** — 用 evals 重跑，确保没引入新问题
6. **生成优化报告** → `./artifacts/optimize/optimize-report-{date}-{skill-name}.md`

**棘轮机制：** 分数只能上升，退步自动回滚，连续 2 轮 Δ<2 分自动停止，文件大小 <= 原始 x 1.5

**多评委评估：** 每轮启动至少 2 个独立评委，评委不复用，至少 2 个共识才有效

---

## 流程五：部署

**目标：** 将本地测试通过的 Skill 安装到全局目录，支持多平台部署。

**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（部署详细步骤）
**Agent 中立指南：** `${SKILL_DIR}/references/agent-neutral-guide.md`

### 部署前问话（必问）

1. **目标 Agent** — Claude Code / TRAE / Codex CLI / Cursor / Windsurf / Gemini CLI / 通用（~/.skills/）/ 多平台同时部署
2. **部署范围** — 仅 SKILL.md / 完整 skill 包 / 完整包 + 子技能
3. **已有版本处理** — 覆盖（备份旧版）/ 覆盖（不备份）/ 跳过 / 询问后决定
4. **部署后验证** — 仅检查文件存在 / 运行 evals / 实际任务测试
5. **MCP 配置同步** — 是否需要同步配置 MCP Servers（如Skill依赖MCP工具）

### 全局目录路径（多平台支持）

| 平台 | 全局目录 | 说明 |
|------|----------|------|
| Claude Code | `.agents/skills/` 或 `~/.claude/skills/` | Claude Code 的全局 skills 目录 |
| TRAE | `.trae/skills/` | TRAE 的全局 skills 目录 |
| Codex CLI | `~/.codex/skills/` | OpenAI Codex CLI 目录 |
| Cursor | `~/.cursor/skills/` | Cursor IDE 目录 |
| Windsurf | `~/.codeium/windsurf/skills/` | Windsurf IDE 目录 |
| Gemini CLI | `~/.gemini/skills/` | Google Gemini CLI 目录 |
| 通用 | `~/.skills/` | 跨 Agent 通用目录 |

### MCP 配置路径（如需要）

| 平台 | MCP 配置文件位置 |
|------|------------------|
| Claude Code | `~/.claude.json` 或项目级 `.mcp.json` |
| TRAE | `.trae/mcp.json` |
| Cursor | `~/.cursor/mcp.json` |
| 通用 | `~/.mcp/config.json` |

### 部署流程

1. **环境检查** — 调用流程零，确保目标目录可写
2. **确认来源** — 工作区中的哪个 skill 目录
3. **检查是否通过测评** — 建议先走「审查」流程
4. **检查MCP依赖** — 如Skill依赖MCP工具，确认MCP Server已配置
5. **部署到 Claude 全局目录**
   ```powershell
   # Windows PowerShell
   if (!(Test-Path ".agents\skills")) { New-Item -ItemType Directory -Path ".agents\skills" -Force }
   Copy-Item -Path "projects\{skill名}" -Destination ".agents\skills\{skill名}" -Recurse -Force
   ```
6. **部署到 TRAE 全局目录**
   ```powershell
   if (!(Test-Path ".trae\skills")) { New-Item -ItemType Directory -Path ".trae\skills" -Force }
   Copy-Item -Path "projects\{skill名}" -Destination ".trae\skills\{skill名}" -Recurse -Force
   ```
7. **部署到其他平台（按需）**
   ```powershell
   # Codex CLI
   $codexPath = "$env:USERPROFILE\.codex\skills"
   if (!(Test-Path $codexPath)) { New-Item -ItemType Directory -Path $codexPath -Force }
   Copy-Item -Path "projects\{skill名}" -Destination "$codexPath\{skill名}" -Recurse -Force
   ```
8. **验证部署**
   ```powershell
   ls .agents\skills\{skill名}\
   ls .trae\skills\{skill名}\
   ```
9. **同步MCP配置（如需要）** — 检查并更新对应平台的MCP配置文件
10. **释放源码工作区（自动执行）** — 步骤 8 验证通过后立即执行，无需询问用户
    ```bash
    bash "${SKILL_DIR}/scripts/source-cleanup.sh" release "{工作区名}"
    bash "${SKILL_DIR}/scripts/source-cleanup.sh" auto
    ```
    ```powershell
    powershell -ExecutionPolicy Bypass -File "${SKILL_DIR}\scripts\source-cleanup.ps1" auto
    ```
    - 只清理 `.cache/sources/` 下带标记的第三方源码，**不碰 `projects/{skill名}/` 源文件**
    - 两段式：先移入 `.trash`（可 `restore`），7 天冷静期后才真正删除
    - 必须向用户报告：释放了哪些、释放多少空间、如何回滚

    详见 `${SKILL_DIR}/references/source-lifecycle.md`

**⚠️ 永远用 `cp`/`Copy-Item`，不用 `mv`，保留源文件。**

**⚠️ 区分两个「源」：** `projects/{skill名}/` = Skill 源文件（**永不删除**，回滚依据）；`.cache/sources/` = 分析用下载的第三方源码（部署后释放）。

**⚠️ 如果 Copy-Item 被路径安全策略阻止，使用 robocopy 作为替代方案。**

**⚠️ Windows 路径注意：使用 `$env:USERPROFILE` 而非 `~`，或使用完整路径。**

**生成部署报告** → `./artifacts/deploy/deploy-report-{date}-{skill-name}.md`

---

## 流程六：管理

**目标：** 管理已安装的 Skill。

**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（管理详细步骤）

### 管理前问话（必问）

1. **操作类型** — 列出已安装 / 更新单个 / 批量更新 / 检查更新 / 卸载 / 查看详情
2. **操作范围** — 全局 / 项目级 / 全部
3. **操作确认**（危险操作）— 确认执行 / 取消 / 先查看影响范围

### 管理操作

- **列出：** `ls ~/.skills/`
- **单个更新：** 查询最新版本 → 比较 → 备份旧版 → 下载新版 → 安全审查 → 安装
- **批量更新：** `npx skills update`
- **检查更新：** `npx skills check`
- **卸载：** 确认存在 → 询问用户确认 → 删除目录 → 清理配置

**生成管理操作报告** → `./artifacts/manage/manage-report-{date}-{operation}.md`

---

## 流程七：合并 Skill

**目标：** 将多个相关 Skill 整合为一个更强大、更完整的 Skill。

**详细指南：** `${SKILL_DIR}/references/merge-workflow.md`
**详细步骤：** `${SKILL_DIR}/references/workflow-details.md`（合并详细步骤）

### 合并流程

```
第一步：深度分析原 Skill
  ↓ 生成深度分析报告 → ./artifacts/analysis/deep-analysis-{date}-{skill-names}.md
第二步：审查原 Skill
  ↓ 调用 review 子技能，对每个原 Skill 进行 Darwin 9 维度打分
第三步：理解原 Skill
  ↓ 核心价值、用户场景、使用频率、依赖关系
第四步：询问用户
  ↓ 保留优点、解决痛点、新增需求、优先级、使用场景、用户群体、成功标准
第五步：网上调研
  ↓ 使用 multi-search-engine 搜索最佳实践、踩坑经验、竞品分析
  ↓ 生成调研报告 → ./artifacts/research/research-report-{date}-{topic}.md
第六步：综合优化
  ↓ 设计合并方案
  ↓ 生成合并方案 → ./artifacts/merge/merge-proposal-{date}-{skill-names}.md
第七步：正常工作流
  ↓ 按标准流程分阶段开发合并后的 Skill
第八步：用户确认
  → 每个阶段完成后都需要用户确认
```

### 合并确认清单

每个阶段完成后都需用户确认：深度分析结果准确、审查结果准确、理解正确、需求完整、调研结果可用、合并方案满意、最终成果符合预期。

---

## 流程八：MCP整合

**目标：** 实现 MCP Server 与 Skill 的互补整合 — MCP 连外部工具，Skill 管内部知识。支持两种模式：将 MCP Server 包装为 Skill，或为现有 Skill 配置 MCP 工具依赖。

**架构原则：**
- **MCP (Model Context Protocol)**：标准化外部工具连接（API、数据库、文件系统、浏览器等）
- **Skill**：封装领域知识、工作流程、最佳实践
- **互补而非替代**：MCP提供工具能力，Skill提供决策逻辑和流程编排

### MCP整合前问话（必问）

1. **整合模式** — 将MCP包装为Skill / 为现有Skill添加MCP依赖 / 配置MCP Gateway / 调研MCP生态
2. **MCP来源** — 已有MCP Server配置 / 需要搜索MCP Server / 需要从零开发MCP Server
3. **目标平台** — Claude Code / TRAE / Cursor / 多平台
4. **安全要求** — 沙箱执行 / 权限最小化 / 网络白名单 / 无特殊要求

### MCP整合流程

```
第一步：MCP生态调研
  ↓ 搜索官方MCP Servers、社区MCP、awesome-mcp列表
  ↓ 评估MCP Server质量、安全性、维护状态
第二步：确认整合模式
  ↓ 模式A：MCP包装为Skill（MCP提供工具，Skill提供工作流）
  ↓ 模式B：Skill + MCP协同（Skill调用MCP工具完成任务）
  ↓ 模式C：MCP Gateway配置（企业级统一MCP入口）
第三步：安全审查（增强版）
  ↓ MCP Server权限分析
  ↓ 语义-行为一致性检测（description描述与实际工具是否匹配）
  ↓ 组合攻击风险评估（MCP+Skill组合风险）
第四步：生成整合方案
  ↓ SKILL.md（含MCP工具调用指引）
  ↓ MCP配置片段（.mcp.json）
  ↓ 使用示例和边界条件
第五步：本地测试
  ↓ 验证MCP连接
  ↓ 测试Skill调用MCP工具
  ↓ 审查评分
第六步：部署配置
  ↓ 部署Skill到全局目录
  ↓ 更新对应平台的MCP配置文件
第七步：生成整合报告
  → ./artifacts/mcp/mcp-integration-{date}-{name}.md
```

### MCP包装为Skill模板

当将MCP Server包装为Skill时，SKILL.md需包含：

```markdown
## MCP工具依赖

本Skill依赖以下MCP Server提供工具能力：

| MCP Server | 工具集 | 用途 |
|------------|--------|------|
| {mcp-server-name} | {tool1, tool2} | {用途说明} |

**MCP配置示例（.mcp.json）：**
```json
{
  "mcpServers": {
    "{server-name}": {
      "command": "{启动命令}",
      "args": ["{参数}"]
    }
  }
}
```
```

### 增强安全审查（MCP相关）

除标准安全审查外，MCP整合需额外检查：

1. **语义-行为一致性检测**
   - MCP工具description描述是否与实际功能一致
   - Skill中对MCP工具的说明是否准确
   - 是否存在"描述说做A实际做B"的不一致

2. **权限过度请求检测**
   - MCP Server请求的权限是否超出其功能需要
   - Skill是否过度调用MCP工具

3. **组合攻击风险评估**
   - Skill + MCP组合是否产生新的风险路径
   - 例如：Skill（文件写入）+ MCP（网络访问）= 数据泄露风险

4. **MCP Server来源验证**
   - 是否来自可信来源（官方、知名社区）
   - 最后更新时间、Star数、维护状态
   - 是否有已知漏洞

---

## 流程九：工作流蒸馏

**目标：** 将一整套工作流程蒸馏成一个大型 Skill（含知识库、代码、模板）。适用于复杂业务流程、多阶段工作流、领域专家经验沉淀。

**详细指南：** `${SKILL_DIR}/references/workflow-distillation.md`

### 蒸馏前问话（必问）

1. **工作流类型** — 业务流程 / 技术流程 / 决策流程 / 创作流程 / 多阶段复合流程
2. **复杂度评估** — 阶段数（3-5/6-10/10+）/ 决策点数量 / 异常路径数量
3. **知识库规模** — 小（<10个文件）/ 中（10-50个）/ 大（50+个）
4. **代码量预期** — 纯指令（无脚本）/ 少量脚本（1-5个）/ 大量脚本（10+个）
5. **目标用户** — 新手引导型 / 专家工具型 / 通用型
6. **使用频率** — 高频日常 / 中频周用 / 低频偶用

### 蒸馏流程

```
第一步：工作流分析
  ↓ 识别阶段、输入输出、决策点、异常处理
  ↓ 评估复杂度，决定是否需要三层加载架构
第二步：架构设计（推荐三层加载）
  ├── 第一层：SKILL.md 薄入口（≤200行，理想≤80行）
  ├── 第二层：references/ 按需加载知识库
  └── 第三层：subskills/ + scripts/ + templates/ 工具资产
第三步：内容蒸馏
  ├── 将工作流各阶段拆分到 references/phase-*.md
  ├── 决策树抽象到 references/decision-trees.md
  ├── 确定性逻辑封装到 scripts/*.py
  └── 可复用产出物放入 templates/
第四步：Token优化
  ├── 薄入口只保留路由信息和决策树
  ├── references/ 文件控制在 200-500 行
  └── 使用 ${CLAUDE_SKILL_DIR} 变量引用资源
第五步：评测集构建
  ├── 核心样本（覆盖主流程）
  ├── 边界样本（决策点、异常路径）
  └── 大型样本（端到端完整流程）
第六步：审查与沉淀
  ↓ Darwin 9维度审查
  ↓ 改进记忆沉淀到 .dev-memory.md（流程十）
```

### 三层加载架构（推荐）

```
your-workflow-skill/
├── SKILL.md                    # 薄入口（≤200行）
├── references/                 # 知识库（按需加载）
│   ├── workflow-overview.md    # 完整流程定义
│   ├── phase-1-xxx.md          # 分阶段详情
│   ├── decision-trees.md       # 决策树集合
│   └── error-handling.md       # 错误处理
├── subskills/                  # 子流程拆分
├── scripts/                    # 确定性逻辑脚本
├── templates/                  # 可复用模板
└── evals/evals.json            # 评测集
```

### 适用判断

| 工作流特征 | 推荐架构 | 蒸馏策略 |
|------------|----------|----------|
| 单文件可容纳（<500行） | 单 SKILL.md | 直接编写，无需拆分 |
| 多阶段、有决策树 | 三层加载 | references/ 拆分阶段 |
| 大量确定性逻辑 | SKILL.md + scripts/ | 逻辑脚本化 |
| 多个独立子流程 | SKILL.md + subskills/ | 子流程独立封装 |
| 知识库密集型 | 薄入口 + references/ | 知识库按需加载 |

**产物：** 蒸馏报告 → `./artifacts/distillation/distillation-{date}-{workflow-name}.md`

**关键约束：**
- SKILL.md 主文档 ≤ 500 行（官方建议），超过 30KB 后 AI 任务理解能力显著下降
- references/ 单文件控制在 200-500 行，按需加载
- 使用 `${CLAUDE_SKILL_DIR}` 变量引用资源，避免硬编码路径
- 工作流蒸馏完成后，必须按流程十沉淀开发记忆

---

## 流程十：开发记忆与发布清洗

**目标：** 防止开发记忆污染主 SKILL.md，确保发布产物纯净。开发期记忆沉淀到 `.dev-memory.md`，发布/开源前自动清洗。

**详细指南：** `${SKILL_DIR}/references/dev-memory-guide.md`

### 核心机制

```
开发期：每次优化/合并/MCP整合后
  ↓ 识别变更（What/Why/Before/After/Verification）
  ↓ 生成记忆记录
  ↓ 追加到 .dev-memory.md（不写入主SKILL.md）
  ↓ 确认主文档未被污染

发布期：用户说"正式部署"/"开源"/"发布"等关键词
  ↓ 检测 .dev-memory.md 是否存在
  ↓ 扫描主文档污染（更新概要/版本标记/TODO/决策记录）
  ↓ 清除污染，归档到 .dev-memory.md
  ↓ 验证功能完整性（evals通过率≥80%）
  ↓ 生成清洗报告 → ./artifacts/cleanup/cleanup-{date}-{name}.md
  ↓ 执行部署（流程五）
```

### 记忆沉淀触发时机

| 时机 | 必须沉淀 | 沉淀内容 |
|------|----------|----------|
| Skill优化后（流程四） | ✅ | 改进概要、验证结果 |
| Skill合并后（流程七） | ✅ | 合并方案、关键决策 |
| MCP整合后（流程八） | ✅ | 整合方案、安全审查 |
| 工作流蒸馏后（流程九） | ✅ | 蒸馏方案、架构决策 |
| Bug修复后 | ✅ | 修复内容、根因分析 |
| 触发词调整后 | ✅ | 调整前后对比 |
| 审查发现新问题 | ✅ | 问题与方案 |

### 清洗触发词

LLM 识别以下关键词时，必须主动询问是否执行清洗：

| 类别 | 触发词 |
|------|--------|
| **部署类** | "正式部署"、"部署到全局"、"部署到生产"、"部署到线上" |
| **开源类** | "开源"、"发布到 GitHub"、"上传到社区"、"公开" |
| **发布类** | "打包发布"、"发布新版本"、"release"、"publish" |
| **分享类** | "分享给他人"、"给别人用"、"团队共享" |

### 清洗检查清单

清洗完成后必须验证：

- [ ] SKILL.md 中无"更新概要"、"变更日志"、"版本说明"章节
- [ ] SKILL.md 中无 "vX.Y 新增"、"vX.Y 修改" 等版本标记
- [ ] SKILL.md 中无 TODO、FIXME、HACK 等开发注释
- [ ] SKILL.md 中无"为什么选择 X" 等决策记录
- [ ] subskills/*/SKILL.md 同上检查通过
- [ ] references/*.md 同上检查通过（正式参考文档除外）
- [ ] .dev-memory.md 保留在本地，未随包发布
- [ ] 功能完整性测试通过（evals 通过率 ≥ 80%）
- [ ] 清洗报告已生成

### 反模式（禁止行为）

| 反模式 | 表现 | 正确做法 |
|--------|------|----------|
| 主文档写更新日志 | SKILL.md 末尾追加 "## 更新历史" | 写入 .dev-memory.md |
| 主文档写决策记录 | SKILL.md 中记录 "为什么选择 A" | 写入 .dev-memory.md |
| 主文档写 TODO | SKILL.md 中包含 "- [ ] 待办" | 写入 .dev-memory.md |
| 版本标记污染 | SKILL.md 中标注 "(v5.2 新增)" | 移除版本标记，写入 .dev-memory.md |
| 不清洗就发布 | 直接部署包含开发记忆的 Skill | 先清洗，再部署 |
| 清洗后丢失记忆 | 清洗时直接删除 .dev-memory.md | 清洗只清除主文档污染，保留 .dev-memory.md |

### 与其他流程的协同

| 流程 | 记忆机制 | 清洗机制 |
|------|----------|----------|
| 流程四：优化 | ✅ 优化后必须沉淀 | — |
| 流程五：部署 | — | ✅ 部署前必须清洗 |
| 流程七：合并 | ✅ 合并后必须沉淀 | ✅ 合并产物发布前必须清洗 |
| 流程八：MCP整合 | ✅ 整合后必须沉淀 | — |
| 流程九：工作流蒸馏 | ✅ 蒸馏后必须沉淀 | — |
| **流程十：开发记忆与发布清洗** | ✅ 核心流程 | ✅ 核心流程 |
| **流程十一：源码工作区回收** | — | 独立流程，清理磁盘 |

---

## 流程十一：源码工作区回收

**目标：** 释放「搜索 / 开发 / 审查 / 合并」过程中 git clone 下来的第三方源码，安全回收磁盘空间。

**详细指南：** `${SKILL_DIR}/references/source-lifecycle.md`
**清理工具：** `${SKILL_DIR}/scripts/source-cleanup.sh` 与 `.ps1`

### 触发时机

| 时机 | 触发方式 | 说明 |
|------|----------|------|
| **A. 部署验证通过后** | **自动**，无需询问 | 最高优先级。Skill 已进全局，源码副本即冗余 |
| B. 审查报告产出后 | 先询问用户 | 用户可能要基于报告追问源码细节 |
| C. 合并 / 蒸馏完成后 | 询问后执行 | 源 Skill 已被合并进新 Skill |
| D. 用户显式要求 | 展示清单 → 确认 | "清理源码" / "释放磁盘" / "删掉下载的源码" |

**流程五部署的第 10 步会自动调用本流程**，用户无需手动触发。

### 执行步骤

1. **查看占用**
   ```bash
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" list
   ```
2. **标记可释放**
   ```bash
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" release "{工作区名}"
   ```
3. **回收（移入 .trash，可恢复）**
   ```bash
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" auto
   ```
4. **报告用户** — 释放了哪些、释放多少空间、回滚命令

### 安全红线

1. 只清理 `.cache/sources/` 下**带标记文件** `.skill-workspace-source` 的目录
2. 用户自己的目录（无标记）**只报告、绝不删除**
3. 两段式回收：先 `stage` 移入 `.trash`，7 天冷静期后 `purge` 才真删
4. **绝不删除** `projects/{skill名}/` 源文件 —— 那是回滚依据
5. 拒绝 `..`、绝对路径、符号链接逃逸；非交互环境必须显式 `--yes`

### 回滚

```bash
bash "${SKILL_DIR}/scripts/source-cleanup.sh" restore "{staged-name}"
```

---

## 上下文管理

**详细指南：** `${SKILL_DIR}/references/context-management.md`

### 核心原则

- **主动规划优先** — 任何任务开始前，先生成明确的执行计划
- **阶段性记忆** — 将长任务分解为阶段，每个阶段独立保存关键信息
- **智能压缩** — 当上下文过长时，自动压缩而非丢失信息
- **可追溯性** — 任何决策和完成状态都应有据可查

### 压缩触发条件

- 对话轮次 > 20 轮
- 估算 token 数 > 80% 上下文窗口
- 用户明确要求"继续"或"下一步"时检查

### 压缩公式

```
压缩后上下文 = 
  最近 5 轮完整对话 +
  所有阶段记忆摘要（每个阶段 <= 200 字）+
  当前任务计划 +
  待完成任务列表 +
  关键决策索引
```

---

## 输入规范

### 必需输入

- **子命令**：开发/合并/审查/搜索/下载/安全审查/MCP整合/优化/部署/管理
- **参数**：skill 名称、URL、GitHub 仓库、MCP Server 地址等（根据子命令而定）

### 可选输入

- **搜索关键词**：搜索时使用
- **安装位置**：全局/工作区/项目级
- **目标 Agent**：部署时使用
- **MCP配置**：MCP整合时使用

### 缺材料时

- 子命令不明确 → 展示子命令列表，询问用户
- 参数不完整 → 通过问话补充
- 网络不可用 → 降级到本地操作

---

## 参考资料

**本工作台：**
- 工作流程详细指南：`${SKILL_DIR}/references/workflow-details.md`
- Darwin 评估体系：`${SKILL_DIR}/references/darwin-rubric.md`
- 棘轮机制：`${SKILL_DIR}/references/ratchet-mechanism.md`
- 多评委评估：`${SKILL_DIR}/references/multi-judge.md`
- 反例黑名单：`${SKILL_DIR}/references/anti-patterns.md`
- Agent 中立指南：`${SKILL_DIR}/references/agent-neutral-guide.md`
- MCP整合指南：`${SKILL_DIR}/references/mcp-integration.md`
- 其他参考：`${SKILL_DIR}/references/` 目录下的 requirements.md、search-strategy.md、proposal-template.md、optimize.md、deploy.md、merge-workflow.md、context-management.md、environment-check.md、artifacts.md

**子技能：**
- 开发子技能：`${SKILL_DIR}/subskills/dev/SKILL.md`
- 审查子技能：`${SKILL_DIR}/subskills/review/SKILL.md`

**全局技能（如已安装）：** find-skills、skill-creation-guide、skill-vetter、cocoloop、deep-research-pro、multi-search-engine、mcp-builder

---

## 注意事项

### 必须遵守
- 执行前先做环境检查（流程零）
- **每个流程开始前必须通过 LLM 对话问话明确用户意图**
- **每个流程完成后必须生成对应的产物 md 文件**
- 全网搜索，不要自己造轮子
- 分阶段开发，每个阶段都审查打分
- 永远用 cp 不用 mv
- 优化时采用棘轮机制，评估时采用多评委独立审查
- **安全审查必须包含语义-行为一致性检测和组合风险评估**
- **MCP整合遵循"MCP连外部工具，Skill管内部知识"的架构原则**
- 多平台部署时注意各平台路径差异，Windows使用`$env:USERPROFILE`而非`~`

### 禁止行为
- 跳过环境检查、问话、产物生成直接执行
- 跳过需求深挖、全网搜索、审查打分直接交付
- 跳过安全审查直接部署
- 未测试就部署到全局
- 覆盖用户未确认的文件、静默执行危险操作
- 合并时假设用户意图而不确认
- **MCP与Skill职责混淆** — 不要把外部工具连接逻辑硬编码在Skill里，应使用MCP
- **忽略组合攻击风险** — 单个权限看似安全，但组合起来可能有风险
- 反例黑名单 AP-01 到 AP-08（详见 `${SKILL_DIR}/references/anti-patterns.md`）

---

## Gotchas

### G1: 评分体系必须统一
- 所有评分必须使用 Darwin 9 维度 100 分制
- 不要混用 120 分制或其他评分体系
- 如果发现旧的 120 分制引用，立即修正为 Darwin 体系

### G2: 问话不能跳过
- 每个流程开始前必须通过 LLM 对话问话明确用户意图
- 用户说"直接做"时，至少确认一次关键参数
- 问话不是形式，是真的要理解用户需求

### G3: 产物必须生成
- 每个流程完成后必须生成对应的产物 md 文件
- 产物是可追溯性的基础，不能省略
- 如果用户说"不用生成"，仍然生成但标记为"用户跳过确认"

### G4: 安全审查是强制的
- 下载/安装 Skill 前必须做安全审查
- 安全评级为 BLOCK 时必须停止，不能继续
- 不要因为"看起来没问题"就跳过安全审查
- **v5.2新增：必须检查语义-行为一致性和组合攻击风险**

### G5: 棘轮机制不可违反
- 优化时分数只能上升，退步必须回滚
- 连续 2 轮 Δ < 2 分时自动停止
- 文件大小不能超过原始的 150%

### G6: 多评委必须独立
- 评委之间必须隔离，互不干扰
- 评委不能复用，下一轮必须重新 spawn
- 至少 2 个评委共识才有效

### G7: MCP与Skill职责边界
- 外部工具连接（API、数据库、浏览器）→ 使用 MCP
- 领域知识、工作流程、最佳实践 → 使用 Skill
- 不要在Skill里硬编码MCP服务器启动逻辑
- Skill依赖MCP时，必须在SKILL.md中明确说明依赖和配置方法

### G8: Windows路径差异
- Windows PowerShell中`~`可能不被正确解析
- 使用`$env:USERPROFILE`替代`~`
- 创建目录前先检查是否存在，使用`New-Item -ItemType Directory -Force`
- Copy-Item失败时，尝试使用robocopy作为替代

### G9: 语义-行为不一致是高危信号
- 如果Skill描述说"只读取文件"但实际请求Write权限 → BLOCK
- 如果示例展示安全操作但正文包含危险命令 → 仔细审查
- description的功能描述必须与实际工作流严格一致

---

## 失败处理

| 失败类型 | 表现 | 修复动作 |
|----------|------|----------|
| 环境检查失败 | 依赖缺失、网络不通 | 提示安装依赖、配置网络 |
| 搜索无结果 | 所有搜索源都无结果 | 建议走开发流程 |
| 安全审查 BLOCK | 发现高风险内容 | 停止安装，提示风险 |
| 优化评分下降 | 本轮评分 < 上轮 | 自动回滚到上一版本 |
| 评委分歧过大 | 分差 > 2 分 | 启动第 3 个评委仲裁 |
| 子 Agent 不可用 | 权限不足、环境限制 | 切换干跑模式，标注 DRY_RUN |

**连续失败 3 次应停下来问用户，不要无限重试。**

---

## 弱模型验收

用更便宜的模型测试此 Skill，验证：
- 能否正确路由到子命令
- 能否按 Darwin 9 维度逐项打分
- 能否正确执行多评委流程
- 输出格式是否一致
- 是否遗漏关键检查项
- 反例黑名单检查是否完整

如果弱模型也能稳定输出合格结果，说明流程规则足够明确。

---

## 退役/合并条件

以下情况考虑退役或合并：
- 模型原生能力已经覆盖该场景
- 维护成本超过收益
- 流程已经过时
- 和新 Skill 大量重叠
- 子技能已独立成熟，可脱离主入口

**退役不是失败。** Skill 太多互相打架，Agent 反而更难做对。

---

## 示例

### 搜索并安装
```
用户: 帮我找个代码格式化的 skill
→ 环境检查 → 搜索流程 → 展示结果 → 用户选择 → 安全审查 → 安装
```

### 从零开发
```
用户: 帮我开发一个代码审查 skill
→ 环境检查 → 需求深挖 → 全网搜索 → 方案推送 → 分阶段开发 → 完整交付
```

### 审查评分
```
用户: 帮我审查一下这个 skill 的质量
→ 加载 review 子技能 → 安全审查 → Darwin 9 维度评分 → 输出报告
```

### 优化现有
```
用户: 这个 skill 触发不太准，帮我优化
→ 诊断（审查）→ 找出问题 → 改 description → 棘轮验证 → 多评委评估
```

### 合并 Skill
```
用户: 把这几个 skill 合并成一个
→ 环境检查 → 审查原 Skill → 理解原 Skill → 询问用户 → 网上调研 → 综合优化 → 分阶段开发 → 用户确认
```

### MCP整合
```
用户: 帮我把这个MCP Server包装成Skill
→ 环境检查 → MCP生态调研 → 确认整合模式 → 增强安全审查 → 生成SKILL.md+MCP配置 → 本地测试 → 部署配置

用户: 这个Skill需要调用浏览器工具，帮我整合MCP
→ 环境检查 → 搜索浏览器MCP Server → 安全审查 → 更新SKILL.md添加MCP依赖 → 配置.mcp.json → 测试验证
```

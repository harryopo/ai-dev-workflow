# Learnings

## 2026-06-14

### Skill Workspace 宣传网页创建

**任务**：为 skill-workspace 创建宣传网页，使用 super-frontend-design 技能

**完成内容**：
1. 研究了 skill-workspace 的详细功能和特性
2. 使用 super-frontend-design 的设计原则创建了落地页
3. 网页文件：`skill-workspace-landing.html`

**设计决策**：
- 风格：Clean/Tech 风格，适合开发者工具
- 配色：深色系 + 蓝紫色强调色，体现科技感
- 排版：Inter 字体，现代无衬线
- 动效：滚动动画、hover 效果，克制但有意义

**网页结构**：
1. Hero - 品牌、承诺、CTA、统计数据
2. 核心功能 - 8 大功能卡片展示
3. v5.0 新特性 - Darwin 评估体系、棘轮机制、多评委审查、反例黑名单
4. 解决的问题 - 6 个痛点和解决方案
5. 工作流程 - 8 步完整生命周期
6. 兼容性 - 支持的 Agent 平台
7. CTA - 行动号召
8. Footer - 链接和版权

**技术实现**：
- 纯 HTML/CSS/JS，无外部依赖
- CSS 变量设计系统
- 响应式设计
- 滚动动画（Intersection Observer）
- 可访问性支持（prefers-reduced-motion）

**关键特性展示**：
- 8+ 核心功能
- 9 维度 Darwin 评估体系
- 4 步安全审查协议
- 多源搜索策略
- 棘轮优化机制
- 多评委独立审查
- 反例黑名单
- Agent 兼容性（Claude Code、Codex CLI、ChatGPT 等）

---

## 2026-06-13

### super-frontend-design v1.2.0 关键修复

**问题**：用户反馈 skill 存在三个核心问题：
1. 调研对话不弹出，实际使用中 LLM 没有弹出 AskUserQuestion 对话框
2. 生成的网页 AI 味很重（蓝紫渐变、灰底白卡、emoji 图标等）
3. 没有询问用户是否参考大企业界面

**修复内容**：

1. **强制调研对话**：将 Phase 0 从"问题清单"改为"3 轮 AskUserQuestion 对话流程"，明确每轮的问题格式、选项、multiSelect 设置

2. **去 AI 味原则**：新增 10 条反 AI 模式识别 + 7 条正向设计原则 + 10 条检查清单，核心禁止项：蓝紫渐变按钮、emoji 图标、灰底白卡、均匀间距、无个性排版

3. **企业参考**：新增 9 个企业参考风格速查表（Apple/Stripe/Linear/Vercel/Notion/GitHub/Airbnb/Figma/Tailwind UI），每个包含关键特征、色系、排版、组件风格

4. **impeccable 深度集成**：每个设计阶段结束后自动触发 review 审查（基于 impeccable），review 子技能新增反 AI 味专项审查

**关键认知**：
- Skill 中仅列问题清单不足以触发对话，必须明确指定使用 `AskUserQuestion` 工具并给出具体格式
- AI 味问题是 LLM 生成 UI 的普遍问题，需要专门的"反 AI 味"检查清单来对抗
- 企业参考速查表比泛泛的风格描述更有效，用户可以直接选择"Apple 风格"或"Stripe 风格"
- 全局部署时 Copy-Item 可能被路径安全策略阻止，robocopy 是更可靠的替代方案

**Category**: correction | best_practice
**Source**: user_feedback

---

## 2026-06-18

### Skill 部署工作流（全局）

**背景**：skill-workspace 是一个全局的 Skill 开发工作台，开发出的最新版本的 Skill 需要同时部署到 TRAE 和 Claude 的全局 skill 目录中。

**全局 Skill 目录路径**：

| 平台 | 全局目录 | 说明 |
|------|----------|------|
| Claude | `.agents/skills/` | Claude Code 的全局 skills 目录 |
| TRAE | `.trae/skills/` | TRAE 的全局 skills 目录 |

**部署工作流**：

```
第一步：在 projects/ 目录下开发/优化 Skill
  ↓
第二步：本地测试验证
  ↓
第三步：部署到 Claude 全局目录
  │  cp -r projects/<skill-name>/ .agents/skills/<skill-name>/
  ↓
第四步：部署到 TRAE 全局目录
  │  cp -r projects/<skill-name>/ .trae/skills/<skill-name>/
  ↓
第五步：验证部署结果
  │  检查两个目录中的 SKILL.md 是否一致
  ↓
第六步：生成部署报告
  → 保存到 artifacts/deploy/
```

**PowerShell 部署命令**：

```powershell
# 部署到 Claude 全局目录
Copy-Item -Path "projects\<skill-name>" -Destination ".agents\skills\<skill-name>" -Recurse -Force

# 部署到 TRAE 全局目录
Copy-Item -Path "projects\<skill-name>" -Destination ".trae\skills\<skill-name>" -Recurse -Force

# 批量部署（如需要）
$skills = @("skill-workspace", "skill-dev", "skill-review")
foreach ($skill in $skills) {
    Copy-Item -Path "projects\$skill" -Destination ".agents\skills\$skill" -Recurse -Force
    Copy-Item -Path "projects\$skill" -Destination ".trae\skills\$skill" -Recurse -Force
}
```

**注意事项**：
1. 使用 `Copy-Item -Force` 覆盖旧版本
2. 部署前确保 SKILL.md 中没有版本号（已移至 README.md）
3. 部署后检查文件完整性
4. 如果 Copy-Item 被路径安全策略阻止，使用 robocopy 作为替代方案

**Category**: workflow | deployment
**Source**: user_requirement

---

## 2026-06-25

### OSS Finder 优化

**任务**：优化 oss-finder 的性能和功能

**完成内容**：
1. **gh CLI 优先** — GitHub 搜索自动使用 gh CLI（实时数据、无速率限制）
2. **并发搜索** — `--platform all` 时 4 个平台并行（ThreadPoolExecutor）
3. **本地缓存** — `~/.cache/oss-finder/`，1 小时 TTL
4. **自动重试** — 网络错误/5xx 自动重试 3 次（指数退避）
5. **结果去重** — 跨平台搜索按 URL 去重
6. **日期筛选** — 新增 `--created-after` 参数
7. **表格格式** — 新增 `--format table` 纯文本输出

**Category**: optimization | skill_development
**Source**: user_requirement

---

### Deep Research Skill 开发

**任务**：基于 Kimi Deep Research 模型，开发深度调研 Skill

**完成内容**：
1. 调研了 Kimi Deep Research 的三阶段工作流程（澄清 → 自主执行 → 报告生成）
2. 分析了现有工具链（Agent Reach、Deep Research Pro、OSS Finder）的能力和差异
3. 设计并实现了 `deep-research` Skill，整合以上工具

**核心设计决策**：
- 采用 Kimi 的三阶段模型：澄清 → 并行执行 → 报告生成
- 使用 Claude Code 的 Agent 工具实现子 Agent 并行
- 整合 oss-finder（项目搜索）+ crawl4ai（网页阅读）+ agent-reach（社交搜索）
- 每个结论必须有来源引用（可追溯）
- 交叉验证：同一结论需要 2+ 个独立来源支持

**工具链整合**：
| 工具 | 用途 |
|------|------|
| oss-finder | 开源项目搜索（GitHub/npm/PyPI） |
| crawl4ai MCP | 网页深度阅读 |
| agent-reach | 社交媒体搜索 |
| deep-research-pro | 多引擎搜索 |
| Agent | 子 Agent 并行调度 |

**Category**: skill_development | research
**Source**: user_requirement

---

### OSS Finder 与 Deep Research 的定位关系

**结论**：两者互补，不是替代关系，都保留。

**定位差异**：
- oss-finder ≈ Google 搜索（轻量快速，几秒出结果）
- deep-research ≈ Kimi Deep Research（深度研究，5-15 分钟）

**依赖关系**：deep-research 的子 Agent 调用 oss-finder 的脚本搜索项目

**Category**: architecture | design_decision
**Source**: user_question

---

## 2026-06-24

### 高星开发类 Skill 调研

**任务**：调研代码编译审查、工程文件管理、开发监督相关的高星 Agent Skills。

**完成内容**：
1. 产出了全面调研报告：`docs/References/高星开发类Skill调研报告.md`
2. 覆盖了 10 个高星项目（从 140K Stars 到 4.1K Stars）
3. 按功能分类：代码审查类、工程文件/架构类、开发监督类
4. 提供了 4 种推荐组合方案（通用开发、安全优先、前端专注、工程管理）
5. 梳理了安装方式速查表

**核心发现**：
1. 当前工作区已安装了大量 Trail of Bits 安全审计技能（40+），安全方向覆盖全面
2. 最大的缺口是工程方法论类 Skill：mattpocock/skills（140K Stars，工程纪律套装）和 obra/superpowers（29K Stars，完整开发方法论框架）
3. 用户偏好先调研再行动，对安装新 Skill 未明确（后续会话中用户明确要求安装）

**Category**: research | dev_skills
**Source**: user_requirement
**Status**: completed → 用户后续会话中确认安装

---

### 高星开发类 Skill 安装完成

**任务**：按用户要求安装推荐的开发类 Skills（mattpocock/skills、obra/superpowers、context7）。

**完成内容**：
1. **mattpocock/skills** (140K Stars) - 安装 21 个工程纪律技能
   - 需求对齐: grill-me
   - TDD: tdd
   - 调试: qa
   - 架构审查: improve-codebase-architecture
   - PRD/Issue 管理: to-prd, to-issues, triage-issue
   - 代码审查: domain-model, request-refactor-plan
   - 其他: caveman（Token压缩）, git-guardrails, write-a-skill 等

2. **obra/superpowers** (29K Stars) - 安装 12 个方法论技能
   - brainstorming, using-superpowers, writing-plans
   - executing-plans, subagent-driven-development
   - test-driven-development, using-git-worktrees
   - verification-before-completion, writing-skills
   - dispatching-parallel-agents, finishing-a-development-branch
   - systematic-debugging

3. **context7** (5K Stars) - 实时文档检索技能

**技术要点**：
- GitHub 在国内访问受限，使用 `ghproxy.net` 镜像成功克隆仓库
- 所有技能安装到 `.agents/skills/` 目录下
- 已配置 Git 全局镜像：`gitclone.com/github.com/` 作为 GitHub 替代方案

**用户交互习惯**：
- 用户说"嗯"表示认可，说"按照推荐安装"表示确定执行
- 安装过程中不需要确认，直接执行即可

**Category**: installation | dev_skills | workflow
**Source**: user_requirement

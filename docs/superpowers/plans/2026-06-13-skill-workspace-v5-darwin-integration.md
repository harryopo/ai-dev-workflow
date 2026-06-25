# Skill Workspace v5.0 - Darwin Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 darwin-skill 的核心功能集成到 skill-workspace，并将所有 Claude 相关内容修改为通用 Agent 规范

**Architecture:** 
- 集成 darwin-skill 的 9 维度评估体系、棘轮机制、多评委独立审查
- 集成反例黑名单和可视化结果卡片
- 将所有 Claude-specific 内容改为 Agent-neutral 规范
- 部署到通用 Agent Skill 目录（~/.skills/）

**Tech Stack:** Claude Code Skill 规范、Markdown、JSON、Git

---

## 文件结构

```
skill-workspace/
├── SKILL.md                              # 主入口（v5.0，Agent-neutral）
├── references/
│   ├── darwin-rubric.md                  # 新增：9 维度评估体系
│   ├── ratchet-mechanism.md              # 新增：棘轮机制
│   ├── multi-judge.md                    # 新增：多评委独立审查
│   ├── anti-patterns.md                  # 新增：反例黑名单
│   ├── result-card-template.md           # 新增：可视化结果卡片
│   ├── agent-neutral-guide.md            # 新增：Agent 中立指南
│   ├── requirements.md                   # 更新：Agent-neutral
│   ├── search-strategy.md               # 更新：Agent-neutral
│   ├── proposal-template.md             # 更新：Agent-neutral
│   ├── merge-workflow.md                # 更新：Agent-neutral
│   ├── context-management.md            # 更新：Agent-neutral
│   ├── environment-check.md             # 更新：Agent-neutral
│   ├── optimize.md                       # 更新：集成 Darwin 优化流程
│   └── deploy.md                         # 更新：通用 Agent 部署
├── evals/
│   └── evals.json                        # 更新：v5.0 评测集
├── templates/
│   └── result-card.html                  # 新增：可视化结果卡片模板
└── subskills/
    ├── dev/
    │   └── SKILL.md                      # 更新：Agent-neutral + Darwin 集成
    └── review/
        └── SKILL.md                      # 更新：9 维度评估 + 多评委
```

---

## Task 1: 创建 Darwin 9 维度评估体系参考文档

**Files:**
- Create: `skill-workspace/references/darwin-rubric.md`

- [ ] **Step 1: 创建 9 维度评估体系文档**

```markdown
# Darwin 9 维度评估体系

## 概述

基于微软 SkillLens (arXiv 2605.23899) 论文的实证验证，9 维度 rubric 药方达到 73.8% 准确率。

## 评分维度

### 结构维度（维度 1-7，静态分析）

| 维度 | 名称 | 权重 | 说明 |
|------|------|------|------|
| 1 | 结构完整性 | 10% | SKILL.md 格式、frontmatter、目录结构 |
| 2 | 指令具体性 | 12% | 步骤明确、参数具体、无模糊词 |
| 3 | 失败模式编码 | 12% | 显式编码已知失败路径，不是简单"别犯错"式叮嘱 |
| 4 | 可执行具体性 | 12% | 禁用"建议/可以考虑/根据情况/灵活把握/视情况而定"等模糊措辞 |
| 5 | 边界条件 | 10% | 输入验证、异常处理、边界情况 |
| 6 | 用户确认点 | 8% | 关键决策处有检查点 |
| 7 | 高风险行动黑名单 | 8% | rm / git reset --hard / force push 等破坏性操作必须明文列禁 |

### 效果维度（维度 8，实测验证）

| 维度 | 名称 | 权重 | 说明 |
|------|------|------|------|
| 8 | 实测表现 | 23% | 通过测试 prompt 验证实际输出质量 |

### Meta-Skill 维度（维度 9，反例黑名单）

| 维度 | 名称 | 权重 | 说明 |
|------|------|------|------|
| 9 | 反例黑名单检查 | 5% | 检查是否包含已知反模式 |

## 总分计算

总分 = Σ(维度得分 × 权重)，满分 100 分

## 评级标准

| 总分范围 | 评级 | 说明 |
|----------|------|------|
| 90-100 | A | 强烈推荐 |
| 80-89 | B | 值得一试 |
| 70-79 | C | 仍需改进 |
| <70 | D | 建议重写 |

## 使用方式

评估 skill 时，按维度 1-9 逐项打分，计算加权总分。
```

- [ ] **Step 2: 验证文件创建**

```bash
Get-Content skill-workspace/references/darwin-rubric.md | Select-Object -First 50
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/darwin-rubric.md
git commit -m "feat: add Darwin 9-dimension rubric"
```

---

## Task 2: 创建棘轮机制参考文档

**Files:**
- Create: `skill-workspace/references/ratchet-mechanism.md`

- [ ] **Step 1: 创建棘轮机制文档**

```markdown
# 棘轮机制

## 概述

分数只能上升。每一轮要么改进 Skill，要么干净地回滚。不会随时间积累局部退化。

## 核心规则

1. **只保留改进** - 新总分 > 旧总分 → 保留
2. **自动回滚退步** - 新总分 ≤ 旧总分 → git revert
3. **可追溯链** - 用 git revert 而非 git reset --hard

## 实现流程

```
for each skill:
  round = 0
  while round < MAX_ROUNDS (默认3):
    round += 1

    # Step 1: 诊断
    找出得分最低的维度

    # Step 2: 提出改进方案
    针对最低维度，生成1个具体改进方案

    # Step 3: 执行改进
    编辑 SKILL.md
    git add + commit

    # Step 4: 重新评估
    spawn 独立子 agent 重新打分

    # Step 5: 决策
    if 新总分 > 旧总分:
      status = "keep"
      # 触顶信号：连续2轮 Δ < 2 分 → break
      if last_delta < 2.0 and this_delta < 2.0:
        break
    else:
      status = "revert"
      git revert HEAD
      break
```

## 触顶信号

连续 2 轮 Δ < 2 分 → 自动停止，避免过度调整

## 文件大小约束

优化后 SKILL.md 不应超过原始大小的 150%
```

- [ ] **Step 2: 验证文件创建**

```bash
Get-Content skill-workspace/references/ratchet-mechanism.md | Select-Object -First 50
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/ratchet-mechanism.md
git commit -m "feat: add ratchet mechanism"
```

---

## Task 3: 创建多评委独立审查参考文档

**Files:**
- Create: `skill-workspace/references/multi-judge.md`

- [ ] **Step 1: 创建多评委独立审查文档**

```markdown
# 多评委独立审查

## 概述

基于 SkillLens 论文实证：LLM 自评准确率仅 46.4%。必须使用独立评委避免偏差。

## 核心规则

1. **每轮启动 2 个独立评委** - 不同的子 agent
2. **评委不复用** - 下一轮启动全新评委，避免锚定效应
3. **至少 2 个 judge 共识才信** - 单个评委结果不可靠

## 实现流程

```
# 评分时
spawn 子 agent 1: 读取 SKILL.md，按 9 维度打分
spawn 子 agent 2: 读取 SKILL.md，按 9 维度打分

# 汇总
if 两个评委分数差异 > 10:
  spawn 子 agent 3: 作为 tie-breaker
  final_score = median(三个分数)
else:
  final_score = average(两个分数)

# 下一轮
重新 spawn 2 个新的子 agent（不复用上一轮的评委）
```

## 干跑模式

如果子 agent 不可用（超时、环境限制），维度 8 用干跑验证打分，标注 `dry_run`。

## 干跑比例控制

干跑比例 > 30% 自动告警，维度 8 实测维度形同虚设。
```

- [ ] **Step 2: 验证文件创建**

```bash
Get-Content skill-workspace/references/multi-judge.md | Select-Object -First 50
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/multi-judge.md
git commit -m "feat: add multi-judge review"
```

---

## Task 4: 创建反例黑名单参考文档

**Files:**
- Create: `skill-workspace/references/anti-patterns.md`

- [ ] **Step 1: 创建反例黑名单文档**

```markdown
# 反例黑名单

## 概述

来自 darwin-skill 实战经验和 SkillLens 论文的反模式，每条都是真实踩过的坑。

## 反例清单

| # | 反模式 | 为什么不要做 | 替代做法 |
|---|--------|--------------|----------|
| 1 | **同 context 自评自改** | LLM 自评准确率仅 46.4% | 必须 spawn 独立子 agent 评分 |
| 2 | **`git reset --hard` 当回滚** | 会丢工作树未提交改动 | 用 `git revert HEAD` |
| 3 | **为凑分增冗余** | 触顶后继续硬改往往是加废话 | 触顶信号 → break，见好就收 |
| 4 | **跳过 test-prompts 直接评分** | 没有 test-prompts 的效果维度是凭空打分 | 强制设计 2-3 prompts |
| 5 | **轮内改多个维度** | 多变量同时变，分数升降无法归因 | 每轮 1 个维度 |
| 6 | **dry_run 比例 > 30%** | 效果维度形同虚设 | 强制至少 1 个真实 full_test |
| 7 | **静默跳过异常** | 破坏 ratchet 完整性 | 异常必须先告知用户再处理 |
| 8 | **忽视维度相关性单独优化** | dim2/3/4 是相关簇 | 找最低维度时同时看相关簇 |

## 检查时机

每轮 Phase 2 改动前对照本表一次。任一反模式命中 → 改方案重写。
```

- [ ] **Step 2: 验证文件创建**

```bash
Get-Content skill-workspace/references/anti-patterns.md | Select-Object -First 50
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/anti-patterns.md
git commit -m "feat: add anti-patterns blacklist"
```

---

## Task 5: 创建 Agent 中立指南

**Files:**
- Create: `skill-workspace/references/agent-neutral-guide.md`

- [ ] **Step 1: 创建 Agent 中立指南文档**

```markdown
# Agent 中立指南

## 概述

Skill 必须能在 Claude Code、Codex CLI、ChatGPT、Cursor、OpenClaw、Trae 等任何支持 SKILL.md 的 Agent 中正常运行。

## 部署路径

| Agent | 全局 Skill 目录 |
|-------|-----------------|
| Claude Code | ~/.claude/skills/ |
| Codex CLI | ~/.codex/skills/ |
| ChatGPT | ~/.chatgpt/skills/ |
| Cursor | ~/.cursor/skills/ |
| OpenClaw | ~/.openclaw/skills/ |
| Trae | ~/.trae-cn/skills/ |
| 通用 | ~/.skills/ |

## 替换规则

### 必须替换

| 原内容 | 替换为 |
|--------|--------|
| `~/.claude/skills/` | `{全局skills目录}/` |
| Claude Code | Agent |
| claude -p | {agent-cli} -p |
| Claude Code Skill 规范 | Agent Skill 规范 |
| CLAUDE.md | AGENTS.md 或 README.md |

### 保留原样

- 具体的命令示例（如 curl、git）
- 技术实现细节
- 评估标准和流程

## 部署命令模板

```bash
# 通用部署命令
cp -r skill-workspace/ ~/.skills/skill-workspace/

# 或根据 Agent 选择路径
# Claude Code: ~/.claude/skills/
# Codex CLI:   ~/.codex/skills/
# Trae:        ~/.trae-cn/skills/
```

## 测试命令模板

```bash
# 通用测试命令
{agent-cli} -p "使用 skill-workspace 搜索 xxx"

# Claude Code
claude -p "使用 skill-workspace 搜索 xxx"

# Codex CLI
codex "使用 skill-workspace 搜索 xxx"
```
```

- [ ] **Step 2: 验证文件创建**

```bash
Get-Content skill-workspace/references/agent-neutral-guide.md | Select-Object -First 50
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/agent-neutral-guide.md
git commit -m "feat: add agent-neutral guide"
```

---

## Task 6: 更新审查子技能 - 集成 9 维度评估

**Files:**
- Modify: `skill-workspace/subskills/review/SKILL.md`

- [ ] **Step 1: 读取现有审查子技能**

```bash
Get-Content skill-workspace/subskills/review/SKILL.md | Select-Object -First 100
```

- [ ] **Step 2: 更新审查子技能**

集成 Darwin 9 维度评估体系，替换现有的 10 维度评分：

1. 更新 frontmatter，版本改为 v5.0
2. 替换 10 维度评分为 9 维度评估体系
3. 集成多评委独立审查机制
4. 更新评分标准和输出格式

- [ ] **Step 3: 验证更新**

```bash
Get-Content skill-workspace/subskills/review/SKILL.md | Select-Object -First 50
```

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/subskills/review/SKILL.md
git commit -m "feat: integrate Darwin 9-dimension rubric into review subskill"
```

---

## Task 7: 更新优化流程 - 集成棘轮机制

**Files:**
- Modify: `skill-workspace/references/optimize.md`

- [ ] **Step 1: 读取现有优化流程**

```bash
Get-Content skill-workspace/references/optimize.md
```

- [ ] **Step 2: 更新优化流程**

集成 Darwin 的棘轮机制和优化循环：

1. 添加棘轮机制说明
2. 添加触顶信号检测
3. 添加反例黑名单检查
4. 更新优化流程为 5 阶段

- [ ] **Step 3: 验证更新**

```bash
Get-Content skill-workspace/references/optimize.md | Select-Object -First 50
```

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/references/optimize.md
git commit -m "feat: integrate ratchet mechanism into optimize workflow"
```

---

## Task 8: 更新主技能 - Agent 中立 + Darwin 集成

**Files:**
- Modify: `skill-workspace/SKILL.md`

- [ ] **Step 1: 读取现有主技能**

```bash
Get-Content skill-workspace/SKILL.md | Select-Object -First 100
```

- [ ] **Step 2: 更新主技能**

1. 版本更新为 v5.0
2. 所有 Claude 相关内容改为 Agent 中立
3. 集成 Darwin 评估体系引用
4. 更新部署路径为通用路径
5. 更新参考资料列表

- [ ] **Step 3: 验证更新**

```bash
Get-Content skill-workspace/SKILL.md | Select-Object -First 50
```

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/SKILL.md
git commit -m "feat: update main skill to v5.0 with agent-neutral and Darwin integration"
```

---

## Task 9: 更新开发子技能 - Agent 中立

**Files:**
- Modify: `skill-workspace/subskills/dev/SKILL.md`

- [ ] **Step 1: 读取现有开发子技能**

```bash
Get-Content skill-workspace/subskills/dev/SKILL.md | Select-Object -First 100
```

- [ ] **Step 2: 更新开发子技能**

1. 版本更新为 v5.0
2. 所有 Claude 相关内容改为 Agent 中立
3. 更新部署路径为通用路径
4. 更新测试命令为通用格式

- [ ] **Step 3: 验证更新**

```bash
Get-Content skill-workspace/subskills/dev/SKILL.md | Select-Object -First 50
```

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/subskills/dev/SKILL.md
git commit -m "feat: update dev subskill to agent-neutral"
```

---

## Task 10: 更新所有 references 文件 - Agent 中立

**Files:**
- Modify: `skill-workspace/references/requirements.md`
- Modify: `skill-workspace/references/search-strategy.md`
- Modify: `skill-workspace/references/proposal-template.md`
- Modify: `skill-workspace/references/merge-workflow.md`
- Modify: `skill-workspace/references/context-management.md`
- Modify: `skill-workspace/references/environment-check.md`
- Modify: `skill-workspace/references/deploy.md`

- [ ] **Step 1: 批量更新 references 文件**

将所有 Claude 相关内容改为 Agent 中立：
- ~/.claude/skills/ → {全局skills目录}/
- Claude Code → Agent
- claude -p → {agent-cli} -p

- [ ] **Step 2: 验证更新**

```bash
Select-String -Path "skill-workspace/references/*.md" -Pattern "claude" -CaseSensitive
```

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/
git commit -m "feat: update all references to agent-neutral"
```

---

## Task 11: 更新评测集

**Files:**
- Modify: `skill-workspace/evals/evals.json`

- [ ] **Step 1: 读取现有评测集**

```bash
Get-Content skill-workspace/evals/evals.json
```

- [ ] **Step 2: 更新评测集**

添加 v5.0 评测用例：
1. Darwin 9 维度评估评测用例
2. 棘轮机制评测用例
3. 多评委独立审查评测用例
4. Agent 中立部署评测用例

- [ ] **Step 3: 验证更新**

```bash
Get-Content skill-workspace/evals/evals.json | ConvertFrom-Json | Select-Object -ExpandProperty evals | Measure-Object
```

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/evals/evals.json
git commit -m "feat: update evals for v5.0"
```

---

## Task 12: 更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 读取现有 README**

```bash
Get-Content README.md | Select-Object -First 100
```

- [ ] **Step 2: 更新 README**

1. 版本更新为 v5.0
2. 添加 Darwin 集成功能说明
3. 更新部署路径为通用路径
4. 更新版本信息

- [ ] **Step 3: 验证更新**

```bash
Get-Content README.md | Select-Object -First 50
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README for v5.0"
```

---

## Task 13: 最终验证

- [ ] **Step 1: 验证文件完整性**

```bash
Get-ChildItem -Path skill-workspace -Recurse -Filter "*.md" | Measure-Object
```

- [ ] **Step 2: 验证无 Claude 特定内容**

```bash
Select-String -Path "skill-workspace/**/*.md" -Pattern "~/.claude/skills" -CaseSensitive
```

- [ ] **Step 3: 验证 Darwin 集成**

```bash
Test-Path "skill-workspace/references/darwin-rubric.md"
Test-Path "skill-workspace/references/ratchet-mechanism.md"
Test-Path "skill-workspace/references/multi-judge.md"
Test-Path "skill-workspace/references/anti-patterns.md"
```

- [ ] **Step 4: 验证 Agent 中立指南**

```bash
Test-Path "skill-workspace/references/agent-neutral-guide.md"
```

---

## Task 14: 部署到通用 Agent Skill 目录

- [ ] **Step 1: 部署到通用目录**

```bash
Copy-Item -Path "skill-workspace" -Destination "$env:USERPROFILE/.skills/skill-workspace" -Recurse -Force
```

- [ ] **Step 2: 验证部署**

```bash
Test-Path "$env:USERPROFILE/.skills/skill-workspace/SKILL.md"
```

---

## 任务依赖

```
Phase 1 (Task 1/2/3/4/5 并行)
    ↓
Phase 2 (Task 6/7 并行，依赖 Phase 1)
    ↓
Phase 3 (Task 8/9/10 并行，依赖 Phase 2)
    ↓
Phase 4 (Task 11/12 并行，依赖 Phase 3)
    ↓
Phase 5 (Task 13，依赖 Phase 4)
    ↓
Phase 6 (Task 14，依赖 Phase 5)
```

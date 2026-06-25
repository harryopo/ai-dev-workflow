# Skill Workspace v5.1 - 工作产物管理实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 所有调研分析、全文搜集、方案推送等工作流都必须生成 md 文件，以便引用、参考、优化和追溯

**Architecture:** 在 skill-workspace 中新增"工作产物管理"模块，定义产物类型、命名规范、存放位置和生成规则

**Tech Stack:** Markdown, SKILL.md 规范

---

## 已完成的更改

### Task 1: 创建工作产物管理规范

**Files:**
- Create: `d:/ai/claude code/skill开发/skill-workspace/references/artifacts.md`

**状态：** ✅ 已完成

**更改内容：**
- 定义了 8 种产物类型（搜索结果报告、深度分析报告、调研报告、方案文档、合并方案、审查报告、优化报告、环境检查报告）
- 定义了产物目录结构（`./artifacts/`）
- 定义了产物生成规则（必须生成、自动创建目录、命名规范、产物引用、产物更新）
- 提供了 4 种产物模板（搜索结果报告、深度分析报告、调研报告、方案文档）

---

### Task 2: 更新 SKILL.md - 添加工作产物管理章节

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/SKILL.md`

**状态：** ✅ 已完成

**更改内容：**
- 在"上下文管理"章节前新增"工作产物管理（v5.1 新增）"章节
- 添加了产物类型表、产物目录结构、必须生成产物的流程、产物生成规则、产物使用流程
- 更新了参考资料，添加了 `artifacts.md` 的引用
- 更新了版本历史，添加了 v5.1.0

---

### Task 3: 更新流程一（搜索 Skill）- 添加搜索结果报告生成

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/SKILL.md`

**状态：** ✅ 已完成

**更改内容：**
- 在"搜索后"部分添加了"生成搜索结果报告"的要求
- 添加了搜索结果报告模板

---

### Task 4: 更新流程七（合并 Skill）- 添加深度分析报告、调研报告和合并方案生成

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/SKILL.md`

**状态：** ✅ 已完成

**更改内容：**
- 在第一步（深度分析原 Skill）添加了"生成深度分析报告"的要求
- 在第五步（网上调研）添加了"生成调研报告"的要求
- 在第六步（综合优化）添加了"生成合并方案"的要求

---

### Task 5: 更新 subskills/dev/SKILL.md - 添加产物生成要求

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/subskills/dev/SKILL.md`

**状态：** ✅ 已完成

**更改内容：**
- 在"搜索完成后必须暂停"部分添加了"生成调研报告"的要求
- 在"方案展示后必须暂停"部分添加了"生成方案文档"的要求
- 在合并流程中添加了深度分析报告、调研报告和合并方案的产物要求

---

### Task 6: 更新 references/merge-workflow.md - 添加产物引用

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/references/merge-workflow.md`

**状态：** ✅ 已完成

**更改内容：**
- 在第一步（深度分析原 Skill）添加了产物说明
- 在第五步（网上调研）添加了产物说明
- 在第六步（综合优化）添加了产物说明

---

### Task 7: 更新 README.md - 添加工作产物管理说明

**Files:**
- Modify: `d:/ai/claude code/skill开发/skill-workspace/README.md`

**状态：** ✅ 已完成

**更改内容：**
- 在核心价值表中添加了"调研结果无法追溯"的痛点和解决方案
- 更新了目录结构，添加了 `artifacts.md` 文件
- 添加了工作产物目录结构说明
- 更新了版本历史，添加了 v5.1.0

---

## 产物类型汇总

| 产物类型 | 生成时机 | 文件命名 | 存放位置 |
|----------|----------|----------|----------|
| 搜索结果报告 | 搜索 Skill 完成后 | `search-results-{date}-{keyword}.md` | `./artifacts/search/` |
| 深度分析报告 | 深度分析原 Skill 完成后 | `deep-analysis-{date}-{skill-names}.md` | `./artifacts/analysis/` |
| 调研报告 | 全网调研完成后 | `research-report-{date}-{topic}.md` | `./artifacts/research/` |
| 方案文档 | 方案推送完成后 | `proposal-{date}-{feature}.md` | `./artifacts/proposals/` |
| 合并方案 | 合并方案设计完成后 | `merge-proposal-{date}-{skill-names}.md` | `./artifacts/merge/` |
| 审查报告 | 审查评分完成后 | `review-report-{date}-{skill-name}.md` | `./artifacts/reviews/` |
| 优化报告 | 优化完成后 | `optimize-report-{date}-{skill-name}.md` | `./artifacts/optimize/` |
| 环境检查报告 | 环境检查完成后 | `env-check-{date}.md` | `./artifacts/env/` |

---

## 必须生成产物的流程

1. **搜索 Skill**（流程一）→ 搜索结果报告
2. **深度分析原 Skill**（流程七第一步）→ 深度分析报告
3. **网上调研**（流程七第五步）→ 调研报告
4. **合并方案设计**（流程七第六步）→ 合并方案
5. **全网深度搜索**（dev 子技能第一阶段）→ 调研报告
6. **方案推送**（dev 子技能第二阶段）→ 方案文档

---

## 产物使用流程

```
第一步：执行工作流（搜索/分析/调研/方案）
  ↓
第二步：生成产物 md 文件
  ↓
第三步：展示产物摘要给用户
  ↓
第四步：用户确认产物内容
  ↓
第五步：保存产物到 artifacts/ 目录
  ↓
第六步：后续流程引用产物
```

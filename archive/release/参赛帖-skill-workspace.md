# Skill 全生命周期工作台 — Trae SOLO Skill 大赛参赛帖

***

## 一、作品简介

**Skill 全生命周期工作台** 是一个覆盖 Skill 从发现到退役的完整管理平台。它将 Skill 的搜索、开发、审查、部署等分散功能整合为统一入口，通过子技能架构实现模块化管理。

**核心亮点：**
- 🌐 **5 层搜索源覆盖**：SkillsMP (1.5M+) → Skills.sh → CocoLoop → GitHub → clawhub
- 🔒 **4 步安全审查协议**：元数据→权限→内容→Typosquat 检测
- 📊 **10 维度评分系统**：120 分制，A/B/C/D 四级评定
- 🧩 **子技能架构**：主入口 + 独立子技能包，按需加载
- 🔧 **整合 4 个全局技能**：find-skills、skill-creation-guide、skill-vetter、cocoloop

***

## 二、适用场景与用例

### 场景 1：搜索并安装 Skill

```
用户: 帮我找个代码格式化的 skill

流程:
1. 搜索 — 调用 SkillsMP API（1.5M+ skills，面向所有 Agent）
2. 展示结果 — 列表显示，询问用户选择
3. 安全审查 — 4 步协议自动扫描
4. 安装 — 复制到工作区或全局
```

### 场景 2：开发新 Skill

```
用户: 帮我开发一个代码格式化 skill

流程:
1. 前置判断 — 这个任务值得 Skill 化吗？
2. 搜索已有 — 先搜 SkillsMP/CocoLoop/GitHub，避免重复造轮子
3. 三条路径 — 找现成的 / 改造现成的 / 从零写
4. 生成 SKILL.md — 使用 init_skill.py 或手动创建
5. 本地测试 — 验收清单 7 项全部通过
6. 打包部署 — 使用 package_skill.py 或 cp 到全局
```

### 场景 3：审查 Skill 质量

```
用户: 审查一下这个 skill 的质量

流程:
1. 安全审查 — 4 步协议：元数据→权限→内容→Typosquat
2. 10 维度评分 — A 组规范性（80分）+ B 组实用性（40分）
3. 生成报告 — 评分表格 + 亮点 + 问题与建议
4. 综合评级 — A/B/C/D
```

### 场景 4：优化现有 Skill

```
用户: 这个 skill 触发不太准，帮我优化

流程:
1. 诊断 — 用审查流程找出问题
2. 方案 — 按优先级排列改进项
3. 改进 — 改 description，补正例/反例
4. 验证 — 用同一个 case 跑一遍
5. 回归 — 用 evals 重跑
```

***

## 三、开发过程

### 3.1 需求分析

我观察到当前 Skill 生态存在以下痛点：

1. **搜索碎片化**：不同平台（SkillsMP、Skills.sh、CocoLoop、GitHub）各自独立，用户需要逐个搜索
2. **开发门槛高**：新手不知道如何写符合规范的 SKILL.md
3. **质量参差不齐**：没有统一的审查标准和评分系统
4. **安全隐患**：下载的 Skill 可能包含恶意代码
5. **部署易出错**：手动复制容易丢失文件或覆盖源文件

### 3.2 设计思路

**架构选择：主入口 + 子技能**

最初考虑过三个独立 Skill，但发现：
- 用户要装 3 个，维护成本高
- 触发词容易冲突（"开发skill" 同时触发多个）
- 缺乏统一的搜索和管理入口

最终选择"主入口 + 子技能"架构：
- 主入口处理搜索、下载、安全审查、优化、部署、管理
- 子技能处理开发和审查（这两个功能最复杂，需要独立的 references 和 evals）
- 子技能可独立部署，也可由主入口路由调用

**搜索策略：多源覆盖 + 降级机制**

搜索是 Skill 生态的核心。我设计了 5 层搜索源：
1. SkillsMP API — 覆盖面最广（1.5M+ skills）
2. npx skills find — Skills.sh 生态
3. CocoLoop API — 国内社区
4. GitHub API — 开源仓库
5. clawhub CLI — 兜底方案

每层失败后自动降级到下一层，确保尽可能找到结果。

**安全审查：整合 skill-vetter 的 4 步协议**

安全是 Skill 管理的重中之重。我整合了 skill-vetter 的 4 步审查协议：
1. 元数据检查 — 防止 typosquatting
2. 权限范围分析 — 识别过度权限
3. 内容扫描 — 检测敏感路径、危险命令、base64 混淆
4. Typosquat 检测 — 防止名称欺骗

### 3.3 开发过程

1. **Day 1**：创建 skill-workspace 主入口，实现搜索和下载功能
2. **Day 2**：创建 dev 子技能，实现 Skill 开发流程
3. **Day 3**：创建 review 子技能，实现 10 维度评分系统
4. **Day 4**：整合 find-skills、skill-creation-guide、skill-vetter、cocoloop
5. **Day 5**：优化搜索功能，添加 SkillsMP API 支持
6. **Day 6**：完善文档和测试用例

***

## 四、使用方法

### 4.1 安装

```bash
# 从工作区复制到全局目录
# 路径因 Agent 而异：
#   Claude Code: ~/.claude/skills/
#   Codex CLI:   ~/.codex/skills/
#   通用:        ~/.skills/
cp -r skill-workspace/ {全局skills目录}/skill-workspace/
```

### 4.2 基本使用

```bash
# 搜索 Skill
/skill-workspace 搜索 代码格式化

# 开发 Skill
/skill-workspace 开发 代码审查 skill

# 审查 Skill
/skill-workspace 审查 skill-dev

# 部署 Skill
/skill-workspace 部署 my-skill
```

### 4.3 单独使用子技能

```bash
# 只部署开发子技能
# 路径因 Agent 而异：
#   Claude Code: ~/.claude/skills/
#   Codex CLI:   ~/.codex/skills/
#   通用:        ~/.skills/
cp -r skill-workspace/subskills/dev/ {全局skills目录}/skill-dev/

# 只部署审查子技能
cp -r skill-workspace/subskills/review/ {全局skills目录}/skill-review/
```

***

## 五、演示效果

### 5.1 搜索演示

```
用户: 帮我找个代码格式化的 skill

📋 搜索结果（来源：SkillsMP）:
  1. code-formatter (⭐ 15.5k stars)
     📝 支持多语言的代码格式化工具
     🔗 https://github.com/xxx/xxx
  2. prettier-skill (⭐ 8.2k stars)
     📝 基于 Prettier 的格式化 Skill
     🔗 https://github.com/xxx/xxx

是否安装？[1/2/取消]
```

### 5.2 安全审查演示

```
安全审查报告
============
Skill: code-formatter
安全评级: SAFE
风险标记: 0
建议: install

详细发现:
- 元数据: ✅ 正常
- 权限: ✅ 最小权限（Read, Write, Edit）
- 内容: ✅ 无风险
- Typosquat: ✅ 无
```

### 5.3 10 维度评分演示

```
Skill 质量审查报告
==================
Skill: code-formatter

A 组：规范性（80 分）
  A1. 触发: 18/20 ✅
  A2. 结构: 14/15 ✅
  A3. 上下文: 13/15 ✅
  A4. 安全性: 9/10 ✅
  A5. 可维护性: 9/10 ✅
  A6. 测试: 8/10 ✅

B 组：实用性（40 分）
  B1. 实用性: 9/10 ✅
  B2. 完成度: 8/10 ✅
  B3. 易用性: 8/10 ✅
  B4. 创新性: 9/10 ✅

总分: 105/120
综合评级: B（值得一试）
```

***

## 六、相关链接

### 代码仓库

- GitHub: [待填写]

### 依赖的全局技能

| 技能 | 说明 | 来源 |
|------|------|------|
| find-skills | Skills.sh 生态搜索 | Anthropic |
| skill-creation-guide | Anthropic 官方创建指南 | Anthropic |
| skill-vetter | 安全审查协议 | 社区 |
| cocoloop | CocoLoop Skill 管理器 | CocoLoop |

### 参考资源

- [Agent Skill 规范](https://docs.anthropic.com/claude-code/skills) — 适用于所有支持 SKILL.md 的 Agent
- [Skills.sh — Agent Skills 生态](https://skills.sh) — `npx skills find`
- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com) — 1.5M+ skills，兼容所有 Agent
- [CocoLoop Skill 市场](https://cocoloop.com)

***

## 七、总结

**Skill 全生命周期工作台** 解决了 Skill 生态中的核心痛点：

1. **搜索碎片化** → 5 层搜索源覆盖，自动降级
2. **开发门槛高** → 引导式开发流程，整合 Anthropic 官方工具
3. **质量参差不齐** → 10 维度评分系统，120 分制
4. **安全隐患** → 4 步安全审查协议，Typosquat 检测
5. **部署易出错** → 标准化部署流程，永远用 cp 不用 mv

**面向所有 Agent**：搜索功能不限于 Claude，兼容 Codex CLI、ChatGPT 等所有使用 SKILL.md 格式的 Agent。

**可扩展性**：子技能架构允许独立开发和部署，未来可以轻松添加新的子技能（如 skill-optimizer、skill-benchmark 等）。

***

*参赛者：[你的名字]*
*参赛时间：2026-06-09*
*作品版本：v2.3.0*

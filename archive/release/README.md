# Skill 全生命周期工作台

> 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

一站式完成 Skill 的 **搜索 → 下载 → 安全审查 → 开发 → 优化 → 测评 → 部署 → 管理**。

## 🚀 快速安装

```bash
# 解压 skill 包
unzip skill-workspace.skill -d skill-workspace-install

# 运行安装脚本
cd skill-workspace-install
./install-skill-workspace.sh
```

## 📁 目录结构

```
skill-workspace/
├── SKILL.md                              # 主入口（382 行）
├── references/
│   ├── optimize.md                       # 优化方法论
│   └── deploy.md                         # 部署指南
├── evals/
│   └── evals.json                        # 主技能评测集（9 条）
│
└── subskills/
    ├── dev/                              # 开发子技能（完整包）
    │   ├── SKILL.md                      # 开发流程（553 行）
    │   ├── references/
    │   │   ├── official-spec.md          # 官方规范
    │   │   ├── template.md              # 模板文件
    │   │   ├── example.md               # 示例文件
    │   │   └── methodology.md           # 实战方法论
    │   └── evals/
    │       └── evals.json               # 开发评测集（6 条）
    │
    └── review/                           # 审查子技能（完整包）
        ├── SKILL.md                      # 审查流程（406 行）
        ├── references/
        │   ├── official-spec.md          # 官方规范
        │   ├── scoring-criteria.md      # 10 维度评分标准
        │   └── security.md              # 安全审查规则
        └── evals/
            ├── evals.json               # 审查评测集（5 条）
            └── test-cases.json          # 测试用例
```

## 🔧 使用方式

### 统一入口

```
/skill-workspace 开发 代码格式化     → 加载 dev 子技能
/skill-workspace 审查 my-skill       → 加载 review 子技能
/skill-workspace 搜索 代码格式化     → 在线搜索 skill
/skill-workspace 下载 pdf-processor  → 下载安装 skill
/skill-workspace 优化 my-skill       → 改进现有 skill
/skill-workspace 部署 my-skill       → 安装到全局
/skill-workspace 管理                → 列出/更新/卸载
```

### 自然语言触发

```
"帮我开发一个代码审查 skill"        → 自动走开发流程
"审查一下这个 skill 的质量"         → 自动走审查流程
"帮我找个代码格式化的 skill"        → 自动走搜索流程
```

### 不同 Agent 的使用方式

```bash
# Claude Code
claude -p "使用 skill-workspace 搜索 代码格式化"

# Codex CLI
codex "使用 skill-workspace 搜索 代码格式化"

# 其他 Agent
# 请使用对应的 CLI 调用
```

## 🔍 核心功能

### 1. 搜索 Skill（5 层搜索源）

| 优先级 | 来源 | 说明 |
|--------|------|------|
| Tier 1 | **SkillsMP** (skillsmp.com) | 1.5M+ skills，兼容所有 Agent |
| Tier 2 | **npx skills find** | Skills.sh 生态 |
| Tier 3 | CocoLoop API | Skill 聚合市场 |
| Tier 4 | GitHub 搜索 | 搜索包含 SKILL.md 的仓库 |
| Tier 5 | clawhub CLI | 命令行搜索工具（兜底） |

### 2. 开发 Skill（3 条路径）

- **路径 A**：找现成的 → 去 SkillsMP/CocoLoop/GitHub 搜索
- **路径 B**：改造现成的 → 保留核心结构，改 7 个点
- **路径 C**：从零写 → 走完整流程

### 3. 审查 Skill（10 维度评分）

- **A 组：规范性**（80 分）— 触发、结构、上下文、安全性、可维护性、测试
- **B 组：实用性**（40 分）— 实用性、完成度、易用性、创新性

### 4. 安全审查（4 步协议）

1. 元数据检查 — 防止 typosquatting
2. 权限范围分析 — 识别过度权限
3. 内容扫描 — 检测敏感路径、危险命令
4. Typosquat 检测 — 防止名称欺骗

## 📊 版本信息

- 版本：v2.3.0
- 日期：2026-06-09
- 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

## 🔗 相关链接

- [Agent Skill 规范](https://docs.anthropic.com/claude-code/skills)
- [Skills.sh — Agent Skills 生态](https://skills.sh)
- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com)

## 📄 许可证

MIT License

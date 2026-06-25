# Skill 全生命周期工作台 - 打包说明

## 📦 包文件

- `skill-workspace.skill` — 打包后的 skill 文件（50KB）
- `install-skill-workspace.sh` — 安装脚本

## 🚀 安装方法

### 方法 1：使用安装脚本（推荐）

```bash
# 解压 skill 包
unzip skill-workspace.skill -d skill-workspace-install

# 进入目录
cd skill-workspace-install

# 运行安装脚本
./install-skill-workspace.sh
```

### 方法 2：手动安装

```bash
# 解压 skill 包
unzip skill-workspace.skill -d skill-workspace-install

# 复制到全局 skills 目录
# Claude Code:
cp -r skill-workspace-install/skill-workspace ~/.claude/skills/

# Codex CLI:
cp -r skill-workspace-install/skill-workspace ~/.codex/skills/

# 通用:
cp -r skill-workspace-install/skill-workspace ~/.skills/
```

## 📋 包内容

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

## 🔧 使用方法

### 搜索 Skill

```bash
# Claude Code
claude -p "使用 skill-workspace 搜索 代码格式化"

# Codex CLI
codex "使用 skill-workspace 搜索 代码格式化"
```

### 开发 Skill

```bash
# Claude Code
claude -p "使用 skill-workspace 开发 代码审查 skill"

# Codex CLI
codex "使用 skill-workspace 开发 代码审查 skill"
```

### 审查 Skill

```bash
# Claude Code
claude -p "使用 skill-workspace 审查 skill-dev"

# Codex CLI
codex "使用 skill-workspace 审查 skill-dev"
```

## 📊 版本信息

- 版本：v2.3.0
- 日期：2026-06-09
- 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

## 🔗 相关链接

- [Agent Skill 规范](https://docs.anthropic.com/claude-code/skills)
- [Skills.sh — Agent Skills 生态](https://skills.sh)
- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com)

## 📝 许可证

MIT License

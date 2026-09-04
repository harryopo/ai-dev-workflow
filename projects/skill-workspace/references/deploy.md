# Skill 部署指南

> 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

## 部署位置

不同 Agent 的全局 skills 目录：

| Agent | 全局路径 | 项目路径 |
|-------|----------|----------|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| Codex CLI | `~/.codex/skills/<name>/` | `.codex/skills/<name>/` |
| ChatGPT 等 | `~/.openai/skills/<name>/` | `.openai/skills/<name>/` |
| 通用 | `~/.skills/<name>/` | `.skills/<name>/` |

**本指南使用 `{全局skills目录}` 作为占位符，请替换为你的 Agent 对应的路径。**

## 部署流程

### 前提条件
- 本地测试通过
- 建议先走「测评」流程，评级 ≥ C

### 部署步骤

1. **确认来源**
   ```bash
   # 检查当前目录中的 skill 目录
   ls ./{skill名}/
   ```

2. **复制到全局**
   ```bash
   # ⚠️ 永远用 cp，不用 mv
   cp -r ./{skill名}/ {全局skills目录}/{skill名}/
   ```

3. **验证部署**
   ```bash
   # 检查文件
   ls {全局skills目录}/{skill名}/

   # 确认 SKILL.md 存在
   cat {全局skills目录}/{skill名}/SKILL.md | head -5
   ```

4. **测试全局可用**
   ```bash
   # 使用你的 Agent CLI 测试
   # Claude Code: claude -p "使用 {name} 完成 XXX 任务"
   # Codex CLI:   codex "使用 {name} 完成 XXX 任务"
   # ChatGPT 等: {agent-cli} -p "使用 {name} 完成 XXX 任务"
   ```

5. **释放源码工作区**（验证通过后自动执行）

   Skill 已部署到全局，此过程中 git clone 下来的第三方源码即成冗余，应当释放：

   ```bash
   # Bash / Git Bash
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" release "{工作区名}"
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" auto
   ```

   ```powershell
   # Windows PowerShell
   powershell -ExecutionPolicy Bypass -File "${SKILL_DIR}\scripts\source-cleanup.ps1" auto
   ```

   - 只处理 `.cache/sources/` 下带标记文件的目录
   - 先移入 `.trash`（可 `restore` 恢复），7 天冷静期后才真正删除
   - 执行后向用户报告释放清单与回滚方式

   详见 `${SKILL_DIR}/references/source-lifecycle.md`。

## 版本管理建议

- **工作区** = 源码仓库（开发、测试、迭代）
- **全局目录** = 部署位置（生产环境）
- 修改时先改工作区，测试通过后再部署
- 保留工作区副本，方便回滚

## 更新已部署的 Skill

1. 在工作区修改并测试
2. 用 cp 覆盖全局目录
3. 验证更新生效

## 回滚

如果部署后发现问题：
```bash
# 从工作区重新部署旧版本
cp -r ./{skill名}/ {全局skills目录}/{skill名}/
```

## AGENTS.md 一主多适配策略（v5.3.1新增）

> **核心思想：维护一份源 Skill，通过 AGENTS.md 适配多个 Agent 平台的差异。**

### 背景与问题

跨平台部署 Skill 时面临的核心问题：

| 差异点 | Claude Code | Codex CLI | Cursor | TRAE |
|--------|-------------|-----------|--------|------|
| 全局目录 | `~/.claude/skills/` | `~/.codex/skills/` | `~/.cursor/skills/` | `.trae/skills/` |
| 配置文件 | `.claude.json` | `.codex/config.json` | `.cursor/mcp.json` | `.trae/mcp.json` |
| SKILL.md 限制 | ≤30KB 软建议 | **8KB 硬截断** | 类似 Claude | 类似 Claude |
| 触发机制 | description 匹配 | description 匹配 | description 匹配 | description 匹配 |
| MCP 配置 | `.mcp.json` | `.codex/mcp.json` | `.cursor/mcp.json` | `.trae/mcp.json` |

**痛点：** 同一个 Skill 想要在多个 Agent 平台运行，过去需要分别维护多个副本，导致版本不同步、修改遗漏。

### AGENTS.md 一主多适配方案

**方案：** 维护一份源 Skill（"一主"），在每个部署目标放置 AGENTS.md 适配文件（"多适配"），通过软链接或部署脚本同步。

**目录结构：**

```
workspace/                       # 工作区（"一主"）
└── projects/my-skill/           # 源 Skill
    ├── SKILL.md                 # 主入口（按最严格约束设计：≤8KB）
    ├── references/
    ├── subskills/
    ├── scripts/
    └── AGENTS.md                # 多平台适配清单

# 部署目标（"多适配"）
.claude/skills/my-skill/         # Claude Code 部署
├── [源 Skill 的软链接或副本]
└── AGENTS.md                    # Claude Code 特定配置

.trae/skills/my-skill/           # TRAE 部署
├── [源 Skill 的软链接或副本]
└── AGENTS.md                    # TRAE 特定配置
```

### AGENTS.md 模板

```markdown
# Agent 适配清单 — {skill-name}

## 目标 Agent
- **主 Agent：** Claude Code
- **兼容 Agent：** Codex CLI / Cursor / TRAE / Windsurf / Gemini CLI

## 平台特定配置

### Claude Code
- 全局路径：`~/.claude/skills/{name}/`
- MCP 配置：`~/.claude.json` 或项目级 `.mcp.json`
- 触发机制：description 自动匹配
- 限制：SKILL.md ≤30KB（软建议），description ≤1536 字符

### Codex CLI
- 全局路径：`~/.codex/skills/{name}/`
- MCP 配置：`~/.codex/config.json`
- 触发机制：description 自动匹配
- **限制：SKILL.md 正文 ≤8KB（硬截断）**

### TRAE
- 全局路径：`.trae/skills/{name}/`
- MCP 配置：`.trae/mcp.json`
- 触发机制：description 自动匹配 + Skill 工具调用
- 限制：类似 Claude Code

### Cursor
- 全局路径：`~/.cursor/skills/{name}/`
- MCP 配置：`~/.cursor/mcp.json`
- 触发机制：description 自动匹配

## 跨平台兼容性检查

- [ ] SKILL.md 正文 ≤ 8 KB（Codex 硬截断线）
- [ ] SKILL.md 行数 ≤ 500 行（Claude 甜区）
- [ ] 使用 `${CLAUDE_SKILL_DIR}` 变量引用资源（非硬编码路径）
- [ ] description ≤ 1024 字符（Agent Skills 规范）
- [ ] 无二进制文件
- [ ] 无平台特定命令（如 Windows 路径用 `$env:USERPROFILE`）
- [ ] scripts/ 兼容多平台（Python/Node.js 优先，避免 shell 专属语法）

## 部署命令

### Windows PowerShell（多平台一次性部署）
```powershell
$skillName = "{skill-name}"
$sourcePath = "projects\$skillName"

# Claude Code
$claudePath = ".agents\skills\$skillName"
if (!(Test-Path $claudePath)) { New-Item -ItemType Directory -Path $claudePath -Force }
Copy-Item -Path $sourcePath\* -Destination $claudePath -Recurse -Force

# TRAE
$traePath = ".trae\skills\$skillName"
if (!(Test-Path $traePath)) { New-Item -ItemType Directory -Path $traePath -Force }
Copy-Item -Path $sourcePath\* -Destination $traePath -Recurse -Force

# Codex CLI
$codexPath = "$env:USERPROFILE\.codex\skills\$skillName"
if (!(Test-Path $codexPath)) { New-Item -ItemType Directory -Path $codexPath -Force }
Copy-Item -Path $sourcePath\* -Destination $codexPath -Recurse -Force
```

### macOS/Linux Bash（多平台一次性部署）
```bash
SKILL_NAME="{skill-name}"
SOURCE_PATH="projects/$SKILL_NAME"

# Claude Code
mkdir -p ~/.claude/skills/$SKILL_NAME
cp -r $SOURCE_PATH/* ~/.claude/skills/$SKILL_NAME/

# Codex CLI
mkdir -p ~/.codex/skills/$SKILL_NAME
cp -r $SOURCE_PATH/* ~/.codex/skills/$SKILL_NAME/

# 通用
mkdir -p ~/.skills/$SKILL_NAME
cp -r $SOURCE_PATH/* ~/.skills/$SKILL_NAME/
```

## 设计原则

1. **按最严格约束设计** — SKILL.md 正文 ≤ 8 KB（Codex 截断线），确保跨平台可移植
2. **平台差异最小化** — 使用 `${CLAUDE_SKILL_DIR}` 变量，避免硬编码路径
3. **scripts/ 跨平台** — Python/Node.js 优先，shell 脚本提供 .sh 和 .ps1 双版本
4. **AGENTS.md 跟随部署** — 每个部署目标都有 AGENTS.md，记录该平台的特定配置
5. **单一数据源** — 工作区是唯一源，部署目标是副本，禁止反向修改
```

### 软链接策略（推荐用于 Unix/macOS）

```bash
# macOS/Linux：使用软链接，修改源即同步所有部署
ln -s $(pwd)/projects/my-skill ~/.claude/skills/my-skill
ln -s $(pwd)/projects/my-skill ~/.codex/skills/my-skill
ln -s $(pwd)/projects/my-skill ~/.cursor/skills/my-skill
```

**Windows 注意：** Windows 需要管理员权限或开发者模式才能创建软链接。推荐使用 `mklink /D`：

```powershell
# Windows 开发者模式启用后
cmd /c mklink /D .agents\skills\my-skill projects\my-skill
```

### 一主多适配的版本同步

**原则：** 工作区是"一主"，部署目标是"多适配"，版本必须同步。

**同步检查脚本：**

```bash
#!/bin/bash
# sync-check.sh — 检查工作区与部署版本的同步状态
SKILL_NAME="my-skill"
SOURCE_HASH=$(find projects/$SKILL_NAME -type f -exec md5sum {} \; | sort | md5sum)

for target in ~/.claude/skills/$SKILL_NAME ~/.codex/skills/$SKILL_NAME ~/.cursor/skills/$SKILL_NAME; do
  if [ -d "$target" ]; then
    TARGET_HASH=$(find $target -type f -exec md5sum {} \; | sort | md5sum)
    if [ "$SOURCE_HASH" = "$TARGET_HASH" ]; then
      echo "✅ $target — 同步"
    else
      echo "❌ $target — 不同步，需要重新部署"
    fi
  fi
done
```

## ⚠️ 重要规则

- **永远用 `cp`，不用 `mv`** — 保留源文件
- **部署前先测试** — 不要直接推到全局
- **保留工作区副本** — 方便回滚和迭代
- **按最严格约束设计** — 跨平台 Skill 必须按 Codex 8KB 截断线设计 SKILL.md
- **AGENTS.md 跟随部署** — 每个部署目标都应有 AGENTS.md 记录平台特定配置
- **部署后释放下载源码** — `projects/{skill名}/` 是源文件**永不删除**；要清理的是分析阶段 git clone 到 `.cache/sources/` 的第三方源码，两者不可混淆

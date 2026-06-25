# Claude Code Skill 开发工作台

> 面向 Claude Code、Codex CLI、OpenCode 等所有 Agent 的 Skill 研发与孵化空间。

## 🚀 包含的 Skill

| Skill | 定位 | 状态 |
|-------|------|------|
| **[oss-finder](projects/oss-finder/)** | 全网开源项目搜索（GitHub/GitLab/Gitee/npm/PyPI） | ✅ 稳定 |
| **[deep-research](projects/deep-research/)** | 深度调研工具（Kimi 三阶段模型 + 子 Agent 并行） | ✅ 稳定 |
| **[skill-workspace](projects/skill-workspace/)** | Skill 开发统一入口（8 个子命令） | ✅ 稳定 |
| **[super-frontend-design](projects/super-frontend-design/)** | 前端设计 Skill（反 AI 味设计） | ✅ 稳定 |
| **[token-optimizer](projects/token-optimizer/)** | Token 优化工具 | ✅ 稳定 |
| **[site-cloner](projects/site-cloner/)** | 网站克隆工具 | ✅ 稳定 |
| **[idea-to-dev](projects/idea-to-dev/)** | 从想法到开发的转化工具 | ✅ 稳定 |
| **[skill-dev](projects/skill-dev/)** | Skill 开发助手 | 🔧 开发中 |
| **[skill-review](projects/skill-review/)** | Skill 质量审查 | 🔧 开发中 |

## 📦 快速安装

### 方式一：克隆整个仓库

```bash
git clone https://github.com/YOUR_USERNAME/skill-workbench.git
cd skill-workbench
```

然后将需要的 Skill 复制到 Claude Code 的 skills 目录：

```bash
# Windows
cp -r projects/oss-finder ~/.claude/skills/
cp -r projects/deep-research ~/.claude/skills/

# macOS/Linux
cp -r projects/oss-finder ~/.claude/skills/
cp -r projects/deep-research ~/.claude/skills/
```

### 方式二：单独安装某个 Skill

```bash
# 安装 oss-finder
git clone https://github.com/YOUR_USERNAME/skill-workbench.git /tmp/skill-workbench
cp -r /tmp/skill-workbench/projects/oss-finder ~/.claude/skills/
rm -rf /tmp/skill-workbench
```

## 🛠️ 使用示例

### oss-finder — 快速搜索开源项目

```
/oss-finder react table --stars ">1000" --language typescript
/oss-finder python web framework --platform all --limit 10
/oss-finder ai agent --created-after "2025-01-01" --stars ">500"
```

### deep-research — 深度调研

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
/deep-research 大语言模型微调技术
```

## 📁 目录结构

```
skill-workbench/
├── projects/                    # 在研 Skill 项目
│   ├── oss-finder/             # 全网开源项目搜索
│   ├── deep-research/          # 深度调研工具
│   ├── skill-workspace/        # 统一入口 skill
│   └── ...
├── docs/                        # 文档和参考资料
├── archive/                     # 归档和发布产物
├── .learnings/                  # 学习日志
└── CLAUDE.md                    # 工作台规范
```

## 🔧 开发环境

- **平台**：Windows 11
- **工具**：Git、Python、Node.js
- **Agent**：Claude Code、Trae

## 📄 许可证

MIT License

---

## 目录规范

```
d:\ai\claude code\skill开发/
├── projects/          # 在研 Skill 项目（唯一合法位置）
│   ├── skill-workspace/
│   ├── token-optimizer/
│   └── ...
├── docs/              # 核心知识文档与参考资料
│   ├── 知识库-Skill开发核心知识.md
│   ├── 快速参考卡.md
│   ├── codegraphcontext-skills.md
│   ├── darwin-skill-SKILL.md
│   └── 参考资料/
├── archive/           # 历史/临时/归档文件
│   ├── release/       # 发布产物唯一保留位置
│   ├── skill-workspace-v2.3.0.zip
│   ├── skill-workspace-landing.html
│   └── darwin-skill-temp.md
├── .agents/skills/    # 已安装的 Agent Skill（保持不动）
├── .learnings/        # 实时学习日志（super-memory 工作流）
├── .trae/             # Trae IDE 相关配置与规格
├── CLAUDE.md          # 项目级硬规则与工作约定
├── README.md          # 本文件
└── skills-lock.json   # Skill 锁定清单
```

---

## 使用方式

### 1. 新建在研 Skill

所有新 Skill **必须**创建在 `projects/` 下，且每个项目至少包含：

- `SKILL.md` — 主入口与使用说明
- `evals/evals.json` — 评测集

示例：

```bash
cd projects
mkdir my-new-skill
cd my-new-skill
# 创建 SKILL.md 与 evals/evals.json
```

### 2. 查阅知识文档

Skill 开发相关知识统一存放于 `docs/`，包括：

- `知识库-Skill开发核心知识.md` — Skill 开发核心概念与流程
- `快速参考卡.md` — 常用命令与速查表
- `codegraphcontext-skills.md` — 代码图上下文相关 Skill 说明
- `darwin-skill-SKILL.md` — Darwin 质量进化系统说明
- `参考资料/` — 开发指南、提示词模板、SKILL.md 模板

### 3. 归档发布产物

发布后的 Skill 包、安装脚本、历史版本等只保留在 `archive/release/`。根目录禁止堆放临时或重复文件。

### 4. 整理与同步

当需要整理工作台时，使用 `super-memory` 的 `neat` 子命令执行洁癖级审查：

- 合并重复文档
- 修正过期信息
- 删除废弃文件
- 同步 `CLAUDE.md` 与 `docs/`

---

## 工作约定（摘要）

完整约定见 [`CLAUDE.md`](./CLAUDE.md)。核心要点：

1. **所有在研 Skill 必须位于 `projects/`**。
2. **每个 Skill 项目必须包含 `SKILL.md` 与 `evals/evals.json`**。
3. **发布产物只保留在 `archive/release/`**。
4. **根目录禁止存放临时或重复文件**。
5. **`.agents/skills/` 保持不动**，作为已安装 Skill 的专用目录。

---

## 相关入口

- 在研项目：`projects/`
- 知识文档：`docs/`
- 归档产物：`archive/`
- 工作约定：`CLAUDE.md`
- 实时学习：`.learnings/`

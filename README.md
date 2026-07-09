# AI 开发全流程规范 (AI Development Process Steward)

> **版本 v3.0** — 让 AI Agent 严格按标准化六阶段流程开发，确保每一行代码都符合经过验证的最佳实践。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0-blue.svg)]()

## 是什么

一个系统级 Skill，为 AI 编码 Agent 提供完整的开发规范和工作流管控。不是写代码的工具，而是确保代码质量、安全和可维护性的**守门人**。

## 核心能力

| 模块 | 说明 |
|------|------|
| 🔷 六阶段门禁流水线 | 需求→架构→脚手架→编码→质量门禁→知识沉淀 |
| 🔷 15条硬性规则 | 5🔴安全 + 5🟡质量 + 5🟢规范，违反安全规则即阻塞 |
| 🔷 Slash 命令 | `/spec` `/plan` `/scaffold` `/build` `/build auto` `/review` `/ship` |
| 🔷 需求审讯协议 | 一次一问+附带猜测+信心指数+信号词检测 |
| 🔷 /build auto 自主模式 | 一次批准后完全自主执行，每任务独立commit |
| 🔷 Doubt-Driven Development | 5步对抗性审查循环，消除确认偏见 |
| 🔷 L1-L5 自治级别 | 从代码补全到高度自治的完整定位 |
| 🔷 10大反模式清单 | 流程/认知/质量三维反模式 + Red Flags |
| 🔷 4层AI Code Review | Quick AI → Auto Checks → Deep AI → Human |
| 🔷 Sub-agent编排 | 并行文件所有权+冲突避免+API契约 |
| 🔷 知识沉淀 | .learnings/ → patterns/ → CLAUDE.md |
| 🔷 5种项目模板 | Fullstack/React/FastAPI/Express/Taro |
| 🔷 工程化模板 | Pre-commit + CI/CD + Docker Compose |

## 快速开始

### 安装

将整个目录复制到你的 Agent Skills 目录：

```bash
# Claude Code
cp -r ai-dev-workflow/ ~/.agents/skills/ai-dev-workflow/

# TRAE
cp -r ai-dev-workflow/ ~/.trae/skills/ai-dev-workflow/
```

### 使用

在 AI 对话框中输入以下任一触发词：

- "启动标准化开发流程"
- "我要开发一个新项目"
- "初始化项目"
- `/spec` `/plan` `/build` `/build auto` `/review` `/ship`

## 目录结构

```
ai-dev-workflow/
├── SKILL.md                     # 主入口 (622行, 14节)
├── evals/
│   └── evals.json              # 20条评测用例
├── references/
│   ├── phase-1-requirements.md
│   ├── phase-2-architecture.md
│   ├── phase-3-scaffolding.md
│   ├── phase-4-coding.md
│   ├── phase-5-quality-gates.md
│   ├── phase-6-knowledge.md
│   ├── architecture.md          # 5种项目类型模板
│   ├── environment-setup.md     # 完整环境配置
│   ├── anti-patterns.md         # 10大反模式详解
│   └── autonomy-levels.md       # L1-L5自治级别
└── templates/
    ├── AGENTS.md                # AI Agent通用入口
    ├── CLAUDE.md                # Claude Code专属配置
    ├── ownership.yaml           # Sub-agent文件域
    ├── .pre-commit-config.yaml  # Pre-commit hooks
    ├── github-actions-ci.yml    # CI/CD流水线
    ├── docker-compose.dev.yml   # 开发环境编排
    └── project-scaffold/        # 项目脚手架
```

## 升级历程

- **v3.0** — 合并 addyosmani/agent-skills + SwarmAI反模式 + ClaudeX最佳实践
- **v2.1** — 负向触发条件、错误回退机制、补齐模板
- **v2.0** — 自包含重写，移除外部依赖
- **v1.0** — 基于6份调研报告构建

## 环境要求

| 工具 | 最低版本 |
|------|---------|
| Git | 2.40+ |
| Node.js + pnpm | Node 20 LTS / pnpm 9+ |
| Python + uv | Python 3.12+ / uv 0.4+ |
| Docker | 26+ |

> 完整环境配置指南见 [references/environment-setup.md](references/environment-setup.md)

## 灵感来源

本 Skill 合并吸收了以下项目的最佳实践：

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — interview-me, /build auto, Doubt-Driven
- SwarmAI 避坑指南 — 反模式清单, 自治级别
- ClaudeX / OpenSpec — Spec驱动, Agent编排
- agentskills.io — SKILL.md 标准规范

## 许可

MIT License
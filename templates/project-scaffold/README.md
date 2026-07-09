# 项目脚手架模板目录

本目录存放可复用的项目脚手架模板。当用户说"用 FastAPI 模板初始化项目"时，AI 应从此目录加载对应模板。

## 模板清单

| 模板 | 状态 | 说明 |
|------|------|------|
| fullstack-monorepo/ | 待创建 | Turborepo + Next.js + FastAPI |
| frontend-react/ | 待创建 | Vite + React + TypeScript |
| backend-fastapi/ | 待创建 | FastAPI + SQLAlchemy + Alembic |
| backend-express/ | 待创建 | Express + TypeScript + Prisma |
| mini-app-taro/ | 待创建 | Taro + React 跨端小程序 |
| cli-python/ | 待创建 | Python Click/Typer CLI |

## 模板文件规范

每个模板目录应包含：

```
{template-name}/
├── README.md              # 模板说明和使用方法
├── scaffold.sh            # 一键初始化脚本（可选）
└── files/                  # 模板文件（保持原项目的目录结构）
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── src/
    │   └── ...
    ├── tests/
    ├── package.json        # 或 pyproject.toml
    └── .gitignore
```

## 当前实现策略

由于项目脚手架模板需要根据具体项目需求动态生成，当前采用以下策略：

1. **轻量模板** — 不预置完整的静态模板，而是通过 AI 按需生成
2. **参考架构文档** — 详细的目录树模板见 `references/phase-2-architecture.md`
3. **配置文件模板** — AGENTS.md、CLAUDE.md、ownership.yaml 的模板在 `templates/` 目录下

## 使用方式

当用户请求初始化项目时，AI 应：

1. 读取 `references/phase-2-architecture.md` 获取目录结构
2. 读取 `templates/AGENTS.md` 和 `templates/CLAUDE.md` 获取配置文件模板
3. 根据用户的技术栈选择，动态生成项目骨架
4. 替换模板中的占位符（如 {项目名称}、{技术栈}）
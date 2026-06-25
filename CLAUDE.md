# Skill 开发根工作台 — 工作约定

> 本文件面向所有在此目录工作的 AI Agent，是硬性规则，不是历史叙事。
> 违反以下约定会导致目录混乱、文件重复、新人无法上手。

---

## 1. 在研 Skill 项目位置

- **所有在研 Skill 必须位于 `projects/` 目录下**。
- 根目录禁止直接创建新的 Skill 项目目录。
- 发现一个 Skill 目录不在 `projects/` 下 → 必须移动到 `projects/`。

---

## 2. Skill 项目最小结构

每个 `projects/<skill-name>/` 必须包含：

```
projects/<skill-name>/
├── SKILL.md              # 主入口：触发条件、使用说明、约束
└── evals/
    └── evals.json        # 评测集：核心样本 + 边界样本
```

可选但推荐：

- `references/` — 规范、指南、案例
- `templates/` — 可复用模板
- `scripts/` — 辅助脚本
- `subskills/` — 子技能（如 dev / review / test）

---

## 3. 发布产物归档

- **发布产物只保留在 `archive/release/`**。
- 根目录禁止出现与 `archive/release/` 内容重复的文件。
- 旧版本压缩包、安装脚本、发布说明等一律移入 `archive/` 或 `archive/release/`。

---

## 4. 文档与知识沉淀

- Skill 开发核心知识、参考卡、规范说明统一放入 `docs/`。
- `docs/参考资料/` 用于存放模板、提示词、开发指南等辅助资料。
- 不要把临时笔记、废弃草稿堆在根目录。

---

## 5. 根目录禁止项

根目录 **不允许** 出现以下内容：

- 临时文件或草稿（如 `*-temp.md`、`*.zip`、`-landing.html`）
- 重复的安装脚本或发布包
- 直接存放的在研 Skill 项目目录
- 缓存目录（`__pycache__`、`.pytest_cache` 等，发现即删）

---

## 6. `.agents/skills/` 保持不动

- `.agents/skills/` 是已安装 Agent Skill 的专用目录。
- **不要移动、删除或修改该目录下的内容**，除非任务明确授权。
- 在整理报告中标记为「未处理项」。

---

## 7. 缓存清理

执行整理任务时，必须扫描并删除：

- 所有 `__pycache__` 目录
- 所有 `.pytest_cache` 目录

---

## 8. 整理后必须输出报告

每次执行整理后，必须生成包含以下内容的报告：

- 移动的文件/目录清单
- 删除的文件/目录清单
- 新增/修改的文件清单
- 未处理项及原因
- 最终目录树结构

---

## 9. 跨会话记忆

- 重要决策、踩坑记录、学习点应通过 `super-memory` 工作流归档。
- 实时记录写入 `.learnings/`。
- 阶段性整理使用 `super-memory neat`。
- 成熟规则提升写入本 `CLAUDE.md`。

# 记忆文档探测（intake 用）

接手时**不假设**记忆文件在 `.ai/HANDOFF.md`——命名与位置千变万化（本机 40 项目实测）。先探、再按角色分类、再读。

## 一、探测清单（按实测命中率排序）

**Tier 1 — 容器目录**（先 `ls` 这些，存在即列）：

`.ai/`（含其子目录 `context/`、`knowledge/`、`tasks/`） · `.learnings/`（实测 14+ 项目命中，比 `.ai/` 更高频） · `memory/` · `.memory/` · `.workbuddy/memory/` · `.claude/memory/` · `.codex-memory/` · `docs/handoff/` 与 `docs/handoffs/` · `docs/wiki/` 与 `docs/repowiki/`

**Tier 1 — 文件名**（不分大小写，扫工作区 maxdepth 4）：

`HANDOFF*` `HANDOVER*` `*交接*` `*记忆*` `MEMORY.md` `LEARNINGS.md` `ERRORS.md` `FEATURE_REQUESTS.md` `PROGRESS*` `TASKS.md` `VERIFICATION.md` `PROJECT_BRIEF.md` `AGENTS.md` `CLAUDE.md`

**Tier 2 — 常用但项目特化**：

`ARCHITECTURE.md` `DECISIONS.md` `MAP.md` `SECURITY.md` `INDEX.md` `known_issues.md` `coding_standards.md` `dev-state.md` `DEV-JOURNAL.md` `ROADMAP.md` `00-目标与进度.md` `踩坑记录.md` `项目进度*` `SESSION_*.md` `handoff-notes.md` `current-state.md` `project-map.md` kiro 风格 `project_*.md`/`user_profile.md`/`feedback_*.md`

**Tier 3 — 日期/编号变体**（用正则，别漏）：

`*-YYYYMMDD.md`（交接文档-20260911） · `*-YYYY-MM-DD.md`（交接总账-2026-09-25） · `*_YYYY-MM-DD_主题.md`（SESSION_2026-06-22_…） · `YYYY-MM-DD.md`（纯日期日记） · `vYYYY-MM-DD` / `*_V2.md`

**排除清单**（防误报，实测踩过）：

- `src/`、`tests/` 下的同名文件（`handoff_manager.py`、`profile-handoff.ts` 是代码不是记忆）
- `node_modules/`、`.git/`、`dist/`、`build/`、`venv/`
- 第三方/参考目录整棵（一个 opensource-reference 含 150+ 个 AGENTS.md）

参考命令：

```bash
# Tier1 容器快速探测
for d in .ai .learnings memory .memory .codex-memory docs/handoff docs/handoffs docs/wiki; do
  [ -d "$d" ] && echo "DIR  $d"
done
# 文件名探测（排除噪声目录）
find . -maxdepth 4 \( -iname "*handoff*" -o -iname "*handover*" -o -iname "*交接*" -o -iname "*记忆*" \
  -o -iname "MEMORY.md" -o -iname "PROGRESS*" -o -iname "TASKS.md" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/src/*" -not -path "*/tests/*" \
  -not -path "*/opensource-reference/*" 2>/dev/null
```

## 二、角色分类（不看文件名死认，读首 30 行判）

| 角色 | 判定线索（文件名 ∥ 内容特征） | 读取优先级 |
|---|---|---|
| 交接 | HANDOFF/HANDOVER/交接* ∥ 有进度、断点、下一步、交接口吻 | 1 |
| 进度 | PROGRESS/进度*/dev-state ∥ 时间线、完成度、日常站会式记录 | 2 |
| 概览 | PROJECT_BRIEF/README/项目记忆 ∥ 一页纸定位与总览 | 3 |
| 架构 | ARCHITECTURE/MAP ∥ 分层图、模块说明、目录地图 | 4 |
| 决策 | DECISIONS ∥ 编号决策、备选对比、权衡 | 5 |
| 任务 | TASKS/TODO/项目进度表 ∥ 勾选框、优先级、看板 | 6 |
| 规范 | coding_standards/context/*/AGENTS.md/CLAUDE.md ∥ 规则与禁令 | 7 |
| 踩坑 | known_issues/LEARNINGS/踩坑记录 ∥ 问题-根因-解法 | 8 |

一个文件可能同时是"进度+交接"（多数中文交接文档如此）→ 按最高优先角色读一次即可，别重复读。

## 三、整理两模式（仅当散落/重叠时启用）

触发判据：同一职能 ≥2 份（如 `.ai/HANDOFF.md` 与 `docs/交接文档.md` 并存）、跨容器散落（一部分 `.ai/` 一部分 `docs/`）、或命名混乱到无法判断新旧。

**模式 1：索引归位（默认，零风险）**——不动任何原文件，立/刷新一个入口索引（`.ai/HANDOFF.md` §6 或项目既有索引文件），逐条给：角色 → 路径 → 置信度 → 是否最新。唯一动作是写索引。

**模式 2：物理归并（须用户确认）**——产出整理方案表（# / 文件 / 现状 / 建议动作 / 目标位置），用户确认后执行：

- 纯移动：`mv` 到标准位置，登记新旧路径；随后 grep 全库清理指向旧路径的引用
- 内容合并：合并进目标文件；被合并掉的源文件 `mv` 进 `.tmp/neat-quarantine/<日期>/`（不 `rm`）
- 确认门与执行规范完全复用 `../../references/delete-review-template.md`（四选项 + 隔离 + 摘要登记）

**禁止**：未经确认移动/合并任何记忆文档；把第三方目录里的 AGENTS.md 当本项目记忆处理。

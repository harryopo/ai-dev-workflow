# agent-memory

> **接手必读**：本文件是项目入口。任何 AI（或人）打开本目录，从这里开始。
> 最后更新：2026-10-24 · 分支：`agent-memory`（工作区仓库 `D:\ai\claude code\skill开发`）

## §0 当前快照

- **目标**：把 super-memory（已发布的记忆管理 skill，[github.com/harryopo/super-memory](https://github.com/harryopo/super-memory)）三轮 dogfood 验证过的记忆能力，转化为**后续开发 agent 时可直接拿来用的记忆模块参考资产**——框架、算法、注意事项手册、（远期）论文与竞赛作品。
- **状态**：M0 已完成（方案书 v2 + 调研索引 + 三期路线图）。**M1（core/ 六模块）未开始**——这是下一个动手项。
- **下一步动作**：① 读 `方案书.md`（项目宪法）→ ② 读 `ROADMAP.md` 找到当前期 → ③ M1 详细设计 → 批准后动工。
- **相关文件**：`方案书.md` · `ROADMAP.md` · `docs/research/README.md`（调研索引）· 上游 skill：`../super-memory/`
- **关键上下文**：
  - 工作分支是 `agent-memory`，**不要在 master 上开发本项目**（master 走 super-memory 线）
  - 工作区有 Mimosa 门禁：commit 可能被 `deep-research-ultra/` 存量高危连带拦截——被拦就把变更暂存好，请用户终端直提（已验证的正解）
  - super-memory 是活项目（已发布、用户在用）：格式/schema 变更需两线同步

## 这是什么项目（30 秒版）

用户（harryopo，单人开发者）做了大量 AI 辅助开发，踩过"AI 会话失忆、交接靠翻聊天记录、记忆文档散落漂移"的痛。他先做了 super-memory skill（纯 Markdown、六子命令、18/18 评测实跑、三轮真实项目 dogfood），验证了**记忆生命周期方法论**有效。但 skill 是"给 LLM 的说明书"——执行依赖模型自觉。

本项目的目的：**把这套已验证方法论沉淀为可复用资产**，用户后续开发任何 agent 需要记忆模块时，直接 `import` / 参考 / 抄设计——而不是每次从零想。定位是**参考资产优先**（拿来顺手的程度衡量完成度），跨宿主 MCP 插件化是认可但后置的次线。

## 目录结构

```
agent-memory/
├── README.md            ← 你在读的这个（入口）
├── 方案书.md            ← 项目宪法：目的/资产/形态/铁律/论文与竞赛计划/决策记录
├── ROADMAP.md           ← 三期路线：长远（论文/基础设施）/ 中长远（手册/基准/竞赛）/ 近（core 框架）
├── docs/
│   └── research/        ← 调研索引：论文/系统/基准/竞赛，全部带链接与要点
├── core/                ← 【M1 待建】六模块核心库
└── mcp/                 ← 【次线·暂缓】
```

## 阅读顺序

第一次接手：`README.md`（本文件）→ `方案书.md` → `ROADMAP.md` → 需要外部背景时查 `docs/research/README.md`。
只找某条调研：直接 `docs/research/README.md`。
只看干什么活：`ROADMAP.md` 当前期。

## 禁区

- 禁止在 master 分支上开发本项目内容
- 禁止引入数据库/服务/向量库进 core（Markdown 唯一权威，纯标准库起步——见方案书铁律）
- 禁止把 super-memory 改造成依赖本项目（它是独立活项目，只做格式契约耦合）
- 禁止绕过 Mimosa 门禁（被拦→暂存→用户终端直提）

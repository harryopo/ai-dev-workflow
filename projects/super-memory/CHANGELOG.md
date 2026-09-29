# Changelog

本项目遵循"改动即记录"。版本号只在本文件演进，不写进 SKILL.md。

## 2.0.0 — 2026-09-29

按 Darwin 评分与 PluginEval 反模式清单做的结构重做。开发期副本位于 `projects/super-memory/`，未部署到安装位。

### 修（会导致空跑或误判的）

- **记忆路径**：删除全部硬编码 `~/.claude/projects/<project>/memory/`。该路径在本机不存在（实测 `.claude/projects` 无此目录），导致 save 的第一步读到空、neat 的盘点跳过全部记忆，却仍输出"同步完成"。改为三段寻址：项目规则文件 → 宿主目录探测 → 项目根 `memory/` 兜底并声明。见 `references/memory-addressing.md`。
- **两级记忆分流**：新增用户级 vs 项目级判据（"换一个项目这条还成立吗"）与 type→scope 映射表，此前完全缺失。
- **条目格式贴宿主**：save 不再自创 `## 标题 / **Date** / **Category**` 结构，改为先读目标目录现有条目、照其 frontmatter 与索引行格式写。
- **与宿主自动记忆共存**：写入前先在索引 grep 关键字，命中已有条目则 Edit 而非新建。
- **promote 的筛选命令全部失效**：原三条 grep（`Status: resolved`、`category: best_practice`、`Recurrence-Count: [3-9]`）与 capture 的落盘格式不匹配——capture 写的是 `**Status**: resolved`（星号在冒号前）、类别在标题行。实测在符合格式的样本上命中 0，即"重复三次就推广"的主链路一次都触发不了。改为 `Status\**:`、`^## \[ID\]` 双形态匹配，并把 Recurrence 阈值改成 `([3-9]|[1-9][0-9])` 以覆盖两位数。
- **0 命中必须如实报出**：所有扫描命令加 `|| echo "无命中"`，并规定须分辨"确实没有"与"路径/格式没对上"，禁止把空结果当检查通过。
- **`${SKILL_DIR}` 路径变量**：四条子技能加载路径原依赖该变量，它不是 Agent Skills 标准字段、装成 plugin 时不展开。改为相对技能目录的裸相对路径，子技能引用父级资源用 `../../references/…`。
- **子技能 frontmatter 空转**：`subskills/*/SKILL.md` 的 `context` / `agent` / `allowed-tools` 不会被宿主解析（注册表只有 `super-memory` 一条），原 neat 用这些字段声明工具、结果 AskUserQuestion 从未授权。已移除这些字段，工具授权统一收在父级，并在每个子文件顶部注明"本文件是引用文档，不是独立 skill"。
- **`context: fork` 移除**：fork 上下文只给 10 个 turn，不足以跑完 neat 的六步或 save 的多目录写入。
- **删除改隔离**：neat 原"删除优于保留"+ 唯一兜底是"在摘要里保留关键信息"，摘要不是备份，删了回不来。改为一律 `mv` 到 `.tmp/neat-quarantine/<日期>/` 保留原相对路径，并在禁止清单中明令禁止对记忆/docs/规则文件用 `rm`。
- **`.learnings/` 三代格式并存**：真实数据里同时存在日期叙事、一条一文件（`LRN-*-<slug>.md`）、聚合文件三种形态，聚合文件中合规范式条目数为 0。现定义唯一权威格式；历史文件不重写不迁移，扫描命令改为同时认三代。
- **`.learnings/` 归属未定**：跨项目时该写哪个工作区没规则，现明确"改了哪个项目写哪个项目"。
- **ID 规则去掉随机**：原"XXX 为顺序号或随机 3 字符"——随机码无法被 See Also 引用。改为 `TYPE-YYYYMMDD-NNN`，NNN 由命令算出当天同类型条数 +1。
- **Resolution 字段两边对不上**：promote 写 `**Status**`/`**Promoted**`，capture 定义 `- **Resolved**`/`- **Commit/PR**`。统一为一套骨架。
- **self-improving-agent 双触发**：该 skill 仍在安装位且触发条件与 capture 几乎逐条重复，"三合一消除了冲突"只完成了 2/3。现声明 `.learnings/` 格式权威归 capture，写入前先 grep 去重，并把父级触发词中与之重叠的项移除。

### 修（合规与体积）

- 删除 SKILL.md 的「版本历史」章节，移入本文件（项目根 `CLAUDE.md` §10 禁止）。
- frontmatter description 去掉工作流概述与「合并来源」；此前 description 摘要了流程，agent 会照 description 执行而跳过正文。
- frontmatter 的 `version` 与版本历史表不一致（`1.0.0` vs 表内 v1.1.0），现统一由本文件承载。
- 新增「不触发 / 反例」：全包此前 0 处反例说明。
- neat 正文 16.4KB → 8KB 级：删除审查报告模板、变更摘要模板、变更影响矩阵抽到 `references/`。
- 新增 `evals/evals.json`（项目 `CLAUDE.md` §2 要求的最小结构）。

### 未做

- capture / neat / promote 的三个子命令未做实跑验证；evals 为规格，尚未执行过任何一条。
- 未部署到 `~/.agents/skills/`（需明确授权后 `git archive` 重导出）。

## 1.1.0 — 2026-06-15

neat 子命令增加"删除审查与确认"安全门（第 2.5 步），删除前须生成审查报告并经用户确认。

## 1.0.0 — 2026-06-15

初始版本，合并 save-memory、neat-freak、self-improving-agent 为 4 子命令统一入口。

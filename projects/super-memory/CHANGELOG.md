# Changelog

本项目遵循"改动即记录"。版本号以 SKILL.md frontmatter 的 `version` 为权威，与本文件最新小节、`evals/evals.json` 的 `version` 三处同步演进（verify.py 校验一致）。

## 2.3.0 — 2026-10-03

开源机制移植第二批（任务 4–6，见 `references/v2.2.0-实施计划.md`）：记忆体检并入 neat、hooks 自动触发、README。

### 新增

- **记忆体检并入 neat**（来源 Letta /doctor）：neat 第一步新增 1b——按 `references/memory-doctor.md` 四项机械检查逐项跑（索引断链 / 重复条目 / 非法置信度码 / 超龄未验证），自检清单同步加一条。处置路由表区分"直修（死链索引行、非法码）"与"需第 2.5 步确认（重复合并涉隔离）"与"只提示不动文件（超龄）"。neat 原反例表压缩为指针（与主入口去重），为正文让出体积。
- **hooks-setup.md**（来源 claude-mem 生命周期映射）：SessionStart 读交接 / PreCompact 压缩前抢救 / Stop 收尾提醒三时机配置片段（Claude Code 形态，其他宿主按文档映射）；可选安装件，不装不影响 skill 本体；写明与 claude-mem 类插件的共写边界。
- **README.md**：定位、五子命令表、安装命令、寻址三步、与宿主记忆/self-improving-agent/claude-mem 的共存规则、评测跑法与版本权威说明。

### 实测

- evals 新增 `core-doctor-findings` 并实跑 PASS：四项检查全部检出注入病灶；处置合规（死链直修、[X] 修为 [已失效]+原因、重复 UPDATE 合并+隔离走模拟确认门、超龄只提示）。**执行中自纠一处**：合并后首轮终检仍报 ci-use-pnpm 断链——"合并必须同步清索引"的动作漏了半步，终检命令按设计抓到，清理后复检 0（该教训已体现在用例记录中）。用例总数 14 → 15，状态全 pass。

### 未做

- hooks 片段未在真实宿主上配置触发过（规格与示例已给，属可选件）。

## 2.2.0 — 2026-10-03

开源机制移植第一批（任务 1–3，见 `references/v2.2.0-实施计划.md`）：mem0 巩固协议、A-Mem 互链、Graphiti 双时间戳。全部零外部依赖，纯提示词层。

### 新增

- **巩固四操作**（来源 mem0）：`knowledge-tiers.md` 新增权威节——写入长期库前 grep 相似旧条目后四选一并写明判定：ADD 新建 / UPDATE 改旧条目保留原 ID / **SUPERSEDE**（对应 DELETE，按"只降级不删除"铁律改造：旧条目标 `[已失效]`+原因+替代指针留档）/ NOOP 等价不写。接入 handoff A3 与 promote 第 5 步（2b）。
- **Related 互链**（来源 A-Mem Zettelkasten）：长期库条目格式加 `**Related**` 必填字段（确无写"无"）；入库前必须检索相关旧条目双向互链；旧条目因互链小幅补充只加一行登记日期，不算改写历史。
- **双时间戳**（来源 Graphiti bi-temporal）：条目格式加 `**生效**`（事实在现实中的起点）与 `**记录**`（写入/最近改写日），语义区分写入规范。
- agent 记忆库条目 frontmatter 增加可选 `last_verified`；超 90 天未验证的条目 neat 盘点时列出"建议重验或降级"，不代判不删除（`knowledge-tiers.md` 有效性维护）。

### 实测

- evals 新增 3 例并全部实跑 PASS：`core-consolidate-supersede`（SUPERSEDE 留痕，未 ADD 平行条目、未删除）、`core-related-linking`（双向互链 + 双时间戳语义正确 + 旧条目只补一行）、`edge-stale-memory-prompt`（超龄列出提示，未代判未删除）。用例总数 11 → 14，状态全 pass。
- verify.py 新增静态检查：v2.2.0 格式字段（生效/记录/Related）、巩固四操作四词、last_verified 超龄规则在规范中齐备；黄金样本同步含新字段。

### 未做

- hooks 自动触发、记忆体检并入 neat、README 与部署（任务 4–6，见 2.3.0）。

## 2.1.1 — 2026-10-03

实测复核驱动的修复版：handoff A5 的统计命令对自家模板格式全部报 0——v2.0.0 修过的"promote 筛选命令失效"同类问题，在 v2.1.0 新写的 handoff 里复发。

### 修

- **handoff A5 统计命令失效**：原 `grep -cE "^\[[VWQRF]\]"` 要求置信度码在行首，但 HANDOFF 模板条目是 `` - `[V]` … ``（bullet + 反引号）格式、长期库条目置信度在字段行中部（`**置信度**：[V]`），合规写入后两条统计命令实测报 0。按 skill 自身"0 命中必须分辨格式没对上"的规则，会诱导 agent 把写对的条目改错。改为匹配任意位置的 `\[[VWQRF]\]`，并在 A5 增加显式规则：统计正则必须同时认句首、bullet 后反引号内、字段行中部三种位置，改任一边必须用另一边格式的黄金样本实测命中。
- **A5 `$(find …)` 命令替换健壮性**：目录不存在时 grep 落到读 stdin（交互终端会挂起），文件名含空格会分词。改为 `grep -rcE … .ai/knowledge/ 2>/dev/null | awk -F: 求和`，空目录/缺失目录稳定输出 0。
- **verify.py ★ 检查不断言**：原注释预期 7 处、实测 8 处（模板第 3 行"标 ★ 的六节"多计一个），脚本只打印不判失败。改为只统计 `^## ★` 节标题（必须 = 6）并单独检查图例存在。
- **verify.py 假阳性**：CHANGELOG 的历史描述触发"宿主硬编码/花括号变量"各 1 处，每次跑都要人工排除。违规扫描不再含 CHANGELOG。
- **版本归属矛盾**：本文件头部原写"版本号只在本文件演进，不写进 SKILL.md"，与 frontmatter `version` 及 verify.py 的版本一致性校验冲突，见头部新表述。

### 新增

- verify.py 新增"A5 统计命令 vs 黄金样本"检查：从 handoff SKILL.md 代码块提取实际 grep 正则，对 HANDOFF 模板格式与长期库字段格式两个黄金样本各断言命中——直接防止"命令与格式脱节"这类问题复发。
- evals 新增 3 个用例：`core-capture-dedup-and-id`（查重 + ID 命令 + 脱敏）、`core-promote-threshold`（扫描 → 决策清单 → 归属 → 回写）、`edge-save-no-new-facts`（纯代码改动不进记忆库），补齐 capture / promote / save 三条此前零覆盖链路；用例总数 8 → 11。
- 删除审查模板补隔离目录风险说明：`.gitignore` 的 `*.tmp` 覆盖 `.tmp/`，隔离文件在版本库之外，恢复依赖磁盘存活，摘要登记必须足以凭记录重建。

### 实测（2026-10-03 同日补充）

- **evals 11/11 全部实跑通过**。方式：每例在 /tmp 沙箱建独立 fixture，按 skill 规则真实执行流程、逐项核对 expect 与 fail 条件。core 五例（寻址两级分流/洁癖同步/交接写入/捕获查重/规则推广）全过；boundary 两例（删除隔离/交接读取端 vs 代码核验）全过；edge 四例（0 命中诚实/不触发/mtime 在制品/无新事实不造假）全过。handoff-write 用例对真实产出跑 A5 统计：十节 10、置信度行 4、长期库 1——同产出用旧正则实测报 0，修复在真实流程内验证生效。
- **模拟项声明**：boundary-delete-quarantine 的 AskUserQuestion 确认门以模拟用户选择（①全部确认）执行，其余步骤真实；宿主探测类用例 HOME 指向沙箱假 home，避免污染真实记忆库。
- **环境发现（Windows）**：Write 工具落盘 CRLF，`grep | tr | while read` 提取文件名时 \r 混入产生断链假阳性（tr -d '\r' 后消解）——正属 skill"0/错命中必须分辨路径格式"场景，记为 Windows 使用注意事项，v2.2.0 可考虑在扫描命令处统一 tr -d '\r'。

### 未做
- v2.2.0 开源机制移植计划见 `references/v2.2.0-实施计划.md`（mem0 四操作巩固 / A-Mem 互链 / Graphiti 双时间戳 / Letta 体检 / hooks 自动触发）。
- 仍未部署到安装位（需用户明确授权后 `git archive` 重导出）。

新增第 5 个子命令 handoff（会话交接与经验沉淀），并划清五个知识落点的归属。

### 新增

- `subskills/handoff/SKILL.md`：中期交接记忆 `.ai/HANDOFF.md` 与长期项目记忆 `.ai/knowledge/` 的写入端与读取端。写入端覆盖会话结束、关键断点暂停、阻塞、全局决策、典型问题解决六类触发；读取端按 HANDOFF → knowledge → 架构文档 → 代码 的优先级接手，并要求产出「交接文档 vs 实际代码」差异表。
- `references/handoff-template.md`：十节结构，其中会话概览、已完成、进行中与断点、下一步行动、运行与验证、操作禁区标为必需节。断点项固定七件事（含文件+函数/行号位置）。
- `references/knowledge-tiers.md`：短期/中期/长期三层尺度表 + 五处落点归属权威表（`.learnings/` 暂存、`HANDOFF.md` 交接、`.ai/knowledge/` 项目长期、agent 记忆库跨项目偏好、规则文件硬规则）+ 单向升档路径 + 长期库条目格式与有效性维护（时效标记、定期校验、失效保留归档）。
- 置信度字母码 `[V]` `[W]` `[Q]` `[R]` `[F]`，句首必带；配套核验命令与"未跑验证不得标 `[V]`"约束。
- 主入口路由表、里程碑流程（capture → handoff → save → neat → promote）、不触发表、禁止清单同步更新；`handoff` 与 `save` 的分工写明（跟仓库走 vs 跟人走）。
- capture 的出口拆成两条：跨模块通用 → 升档 `.ai/knowledge/`；必须每次看到的硬规则 → promote。
- promote 的目标文件表新增 `.ai/knowledge/` 分类行与"先判归属再动手"的示例对比。
- neat 的盘点范围纳入 `.ai/`，自检新增必需节齐全/历史记录未被改写/`[V]` 已核验三项。

### 规范与既有实践的对照（决定落地方式时实测）

- 置信度原方案里"进行中"与"有风险"共用同一个警告符号，机械校验无法区分，改为五个互不重复的字母码。
- 本机真实项目对照：`虚拟人智能体开发/.ai/` 是扁平 8 个 md + `context/`；`tdsf-terminal-agent-clone/.ai/knowledge/` 只建了 3/5 个分类；`FDE/HANDOFF.md` 为自定义 8 节 110 行。因此长期库骨架改为按需创建、已存在的 HANDOFF 只做缺失节对齐不重排。

### 未做

- handoff 的写入端与读取端均未实跑；evals 新增用例仍是待执行规格。
- 未部署到安装位。

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

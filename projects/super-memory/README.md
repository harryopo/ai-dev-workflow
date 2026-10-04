# super-memory

记忆与知识管理工作台：把错误/学习/纠正结构化记到 `.learnings/`，把会话成果归档到 agent 记忆库，里程碑时对文档与记忆做洁癖同步，把成熟学习提炼为项目规则。纯 Markdown 文件驱动，**无外部服务、无向量库**，检索靠 grep + frontmatter + 索引。

## 五个子命令

| 子命令 | 什么时候走 |
|---|---|
| capture | 错误 / 用户纠正 / 知识过时 / 更好做法 → 写 `.learnings/` |
| handoff | 会话交接（写 `.ai/HANDOFF.md`）或接手项目（读取端核验）；顺带把已验证通用内容升档 `.ai/knowledge/` |
| save | 会话结束，把跨会话偏好与事实归档 agent 记忆库并更新索引 |
| neat | 里程碑：尺寸体检 → 盘点 → 变更矩阵 → 删除审查 → 修改 → 自检 → 摘要 |
| promote | 反复出现的学习提炼成规则写进项目规则文件 |

里程碑完整流程：`capture → handoff → save → neat → promote`。触发词与反例见 `SKILL.md`。

## 安装

```bash
# 从本仓库导出（在仓库根目录执行）
git archive HEAD projects/super-memory | mkdir -p ~/.agents/skills/super-memory
git archive HEAD projects/super-memory | tar -x --strip-components=2 -C ~/.agents/skills/super-memory
```

安装位按宿主而定：`~/.agents/skills/`（Claude Code 等）、`~/.zcode/skills/` 或项目 `.agents/skills/`。装完跑 `python scripts/verify.py` 应全绿。

## 写记忆前：寻址

本 skill 不假设宿主。写入前按三步定位（`references/memory-addressing.md`）：项目规则文件的记忆章节 → 宿主目录探测（`~/.qoder/…`、`~/.claude/…`）→ 兜底项目根 `memory/`。格式照现存条目抄，不自创。

## 与其他机制的共存

- **宿主自动记忆**（Claude Code memory tool 等）：写前先 grep 索引，命中同主题就 Edit 不新建（`ADD/UPDATE/SUPERSEDE/NOOP` 四操作，见 `references/knowledge-tiers.md`）。
- **self-improving-agent**：`.learnings/` 格式权威归本 skill 的 capture；写入前 grep 去重，不重复记录同一事件。
- **claude-mem 等自动记忆插件**：可共存，但插件不得写 `.ai/` 与 `.learnings/`（这两处格式与历史由本 skill 排他管理）。

## 可选增强

- **hooks 自动触发**：会话开始读交接、压缩前抢救、结束提醒归档——配置片段见 `references/hooks-setup.md`，不装也能用。

## 评测

`evals/evals.json` 为可执行规格：每例在沙箱建 fixture、按 skill 规则真实走流程、逐项核对 expect 与 fail。2026-10-03 已 15/15 实跑通过。跑法：为每例建独立 fixture 项目（宿主探测类用例把 `HOME` 指向沙箱假 home），执行后把 `status` 回写为 `pass`。

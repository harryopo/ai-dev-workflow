# 记忆寻址（memory-addressing）

四个子命令写记忆前共用本文件。**目标不是记住某个路径，而是每次现场确定"这个 agent 的记忆在哪、长什么样"。**

## 一、优先级：规则文件 > 宿主探测 > 兜底

### 1. 规则文件（最高优先）

在当前工作区根目录按序找，读到哪个算哪个：

`AGENTS.md` → `CLAUDE.md` → `QODER.md` → `GEMINI.md` → `.cursor/rules/` → `.github/copilot-instructions.md`

在文件里搜"记忆 / memory / learnings"章节。只要它规定了目录或格式，**照它写**，本文件后面的表全部作废。

例：某仓库 `CLAUDE.md` 写了"重要决策通过 super-memory 归档、实时记录写 `.learnings/`、成熟规则写回本文件"——那就按这三条走，别再猜宿主。

### 2. 宿主探测

规则文件没写，用命令实测，别凭印象：

```bash
# 打印实际存在的记忆位，探测结果要出现在给用户的输出里
for p in \
  ~/.qoder/memory \
  ~/.qoder/projects/*/memory \
  ~/.claude/memory ~/.claude/projects \
  ~/memory ~/AGENTS.md; do
  [ -d "$p" ] && echo "DIR  $p"
  [ -f "$p" ] && echo "FILE $p"
done
```

已知形态（仅作为探测的候选，不是结论）：

| 宿主 | 用户级（跨项目） | 项目级（单项目） |
|---|---|---|
| Qoder | `~/.qoder/memory/` | `~/.qoder/projects/<slug>/memory/` |
| Claude Code | `~/.claude/memory/`（若存在） | `~/.claude/projects/<slug>/memory/` |
| Codex CLI | `~/AGENTS.md` | 项目根 `AGENTS.md` |
| 无托管记忆 | — | 项目根 `memory/` |

`<slug>` 生成规则：工作区绝对路径，把盘符冒号、`\`、`/` 和空格统一换成 `-`。
例：`D:\ai\claude code\skill开发` → `D--ai-claude-code-skill--`。
**别手算，用现有目录对：** `ls ~/.qoder/projects/` 里找得到就用它，找不到再按规则新建。

### 3. 兜底

一个都没探测到 → 用项目根 `memory/` + `memory/MEMORY.md` 索引，并在变更摘要中写明"未找到宿主记忆位"。

## 二、两级分流：这条该进用户级还是项目级

只问一句：**换一个项目，这条还成立吗？**

| 类型 | 成立范围 | 去处 |
|---|---|---|
| 用户角色、技术背景、长期偏好 | 所有项目 | 用户级 |
| 协作习惯（怎么汇报、怎么确认、什么时候该停下来） | 所有项目 | 用户级 |
| 只在本项目成立的事实、决策、约束、进度 | 单项目 | 项目级 |
| 本项目专属的外部资源（看板、文档站、部署地址） | 单项目 | 项目级 |
| 某工具的通用用法、和具体项目无关 | 所有项目 | 用户级 |

判不准就**放项目级**——项目级写错了下次还能捞，用户级污染了会跟着所有项目。

## 三、格式：贴现存条目，不要自创

1. 列出目标目录的现有条目，读 1–2 个。
2. 照抄它的字段结构。多数 agent 记忆库形如：

```markdown
---
name: <与文件名一致的 kebab-case>
description: <一行，将来靠它判断相关性，写具体>
metadata:
  type: user | project | feedback | reference
---

<正文。事实本身 + Why + How to apply>
```

3. 更新索引（`MEMORY.md`），每个条目一行：

```markdown
- [标题](文件名.md) — 一行钩子
```

索引只放指针，不放正文。

## 四、和宿主自动记忆机制共存

宿主本身可能在写同一批目录。写前必做：

```bash
grep -rin "<本条关键字>" <目标目录>/MEMORY.md <目标目录>/*.md
```

- 命中 → 编辑已有条目（改内容 + 必要时改 description），**不新建**。
- 未命中 → 新建条目 + 追加索引行。
- 两边同时改过同一条 → 以磁盘当前内容为准做合并，别用记忆里的旧版覆盖。

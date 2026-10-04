# 发布前清洗清单

> 目的：发布包里只留 Agent 运行必需的内容。开发期产物、升级纪要、版本标记一律不进包。

## 为什么必须清洗

| 不清洗的后果 | 说明 |
|---|---|
| 上下文浪费 | description 之外，正文和 resources 都在被调用时读入；纪要类文本是纯噪音 |
| 误导 Agent | 升级纪要里的旧结论会被当成现状，触发错误的判断 |
| 磁盘占用 | `.research/`、`artifacts/`、`__pycache__/` 动辄几百 KB 到几 MB |
| 维护负担 | 同一份知识散在主文档和纪要里，改一处必漏另一处 |

## 清洗项

### 1. 删除开发期目录

整目录删，不保留：

```
.research/          # 门禁日志、调研脚本、commit 记录
artifacts/          # 优化报告、清洗报告等过程产物
__pycache__/        # Python 缓存
.dev-memory.md      # 开发记忆，留工作区，不进包
*.bak*  *~          # 编辑器与备份残留
index.html          # 落地页，Agent 不读
CHANGELOG.md        # 版本历史，见下方"版本信息归位"
```

`.dev-memory.md` 的内容不要丢——它记录了"为什么这么改"，是后续维护的依据。移到工作区（`{工作区}/.dev-memory/{skill名}.md`）。

### 2. 剥离 frontmatter 版本字段

删除 `version:` 行。版本靠 git 历史追溯，不靠 frontmatter——写死在 frontmatter 里只会造成"文档说 5.4、代码是 5.3"的漂移。

```yaml
# 清洗前
name: my-skill
version: 5.4.0
description: |
  我的 Skill v5.4.0。当用户提到...

# 清洗后
name: my-skill
description: |
  我的 Skill。当用户提到...
```

### 3. 剥离正文版本字眼

| 类型 | 清洗前 | 清洗后 |
|---|---|---|
| 标题后缀 | `## Gotchas 指引（v5.3.1新增）` | `## Gotchas 指引` |
| 行内标注 | `**产物** — 调研报告（v5.1 新增）` | `**产物** — 调研报告` |
| 文件头注 | `> v5.4 新增。解决 X 问题。` | `> 解决 X 问题。` |

**不要动这两类**：
- 外部依赖的版本号（如"基于 SkillLens 论文 v2.0"）——那是客观事实
- 讲解反模式的示例文本（如反模式表里的 `"v5.2 新增"`）——那是教学用例

### 4. 去重

同一份知识只留一处。正文里若整段复述了 `references/` 的内容，压缩成 1-2 行摘要 + 指向 references 的路径。

### 5. 路径写法

资源引用用相对技能目录的裸相对路径（`references/xxx.md`），不要用宿主私有变量——`CLAUDE_SKILL_DIR` 只在 Claude Code 展开，装成 plugin 时失效。

## 执行

优先跑脚本（清单的可执行版本）：

```bash
bash "{技能目录}/scripts/release-clean.sh" "{工作区路径}/{skill名}"
```

```powershell
powershell -ExecutionPolicy Bypass -File "{技能目录}\scripts\release-clean.ps1" "{工作区路径}\{skill名}"
```

脚本只做删除与剥离，不改业务内容。清洗后向用户报告删了哪些文件、剥离了哪些位置。

## 清洗后自查

- [ ] 目录里只剩 SKILL.md + references/ + scripts/ + evals/（按需）
- [ ] frontmatter 无 `version:` 字段
- [ ] 正文无自身版本字眼（教学示例除外）
- [ ] 资源引用均为相对路径
- [ ] SKILL.md 行数 ≤ 500（Codex 8KB 硬截断线更严）
- [ ] description 前 250 字符含触发条件
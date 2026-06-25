# Skill 开发核心知识库

> 整合自：SKILL-开发指南、skill开发提示词模板、skill模板-SKILL.md、快速参考卡、skill-official-spec 记忆、skill-dev 元技能
> 最后更新：2026-05-29

---

## 一、Skill 本质：目录结构，不是单文件

```
my-skill/
├── SKILL.md          # 必须——核心指令（≤500行）
├── references/       # 可选——按需加载，被引用时才读取
├── assets/           # 可选——模板、图片
├── scripts/          # 可选——可执行脚本
├── examples/         # 可选——好结果、坏结果、边界样例
└── evals/            # 可选——最小评测集
```

**核心设计意图：** `references/` 是按需加载的。塞进 SKILL.md 正文会每次调用都注入上下文，白白烧 token。放 references/ 里只在 Claude 主动引用时才读取。

---

## 二、三层渐进式加载机制

| 层级 | 何时加载 | 上下文占用 |
|------|---------|-----------|
| Level 1：元数据 | 会话启动时 | name + description，~100 tokens/skill |
| Level 2：SKILL.md 正文 | 被调用时 | 全文注入 |
| Level 3：目录资源 | 正文引用时 | 仅读取的文件 |

**核心理解：** description 始终在上下文里（占路由空间），正文和目录资源只在调用时才加载。

---

## 三、Frontmatter 完整字段（官方 12 字段）

所有字段都是可选的，强烈建议写 `description`。

### 第一组：标识（告诉系统你是谁）

```yaml
name: my-skill              # /slash-command 名称
                            # 全小写+数字+连字符，≤64 字符
                            # 省略时用目录名
                            # 禁止包含 XML 标签、"anthropic"、"claude"

description: |              # ≤1024 字符（列表中截断为 250 字符）
  做什么 + 什么时候触发

argument-hint: "[参数]"     # 自动补全时的提示
```

### 第二组：触发控制（决定谁能让 Skill 运行）

```yaml
disable-model-invocation: false  # true = 只能用户手动 /name 触发
                                  # description 不进入上下文
                                  # Claude 不知道此 Skill 存在
                                  # 默认：false

user-invocable: true              # false = 用户看不到此 Skill
                                  # 只有 Claude 能调用
                                  # 默认：true

paths: "*.md, src/**/*.ts"        # 只在处理匹配文件时才自动激活
                                  # 逗号分隔或 YAML 列表
```

### 调用控制矩阵

| 配置 | 用户可调用 | Claude 可自动调用 | description 在上下文 |
|------|-----------|------------------|-------------------|
| 默认（都不设） | ✅ | ✅ | ✅ |
| `disable-model-invocation: true` | ✅ | ❌ | ❌ |
| `user-invocable: false` | ❌ | ✅ | ✅ |

**隐藏用法：** `user-invocable: false` 可以写一个用户完全看不到的 Skill，让 Claude 在后台自动调用（隐形工作流）。

### 第三组：执行模式（Skill 在哪跑）——实战价值最高

```yaml
context: fork              # fork = 独立子 Agent，省略 = 当前会话（inline）

agent: "general-purpose"   # context: fork 时使用的子 Agent 类型
                           # 内置：Explore | Plan | general-purpose
                           # 或 .claude/agents/ 中的自定义 Agent name

allowed-tools: Read Write Edit Glob Grep  # Skill 激活时免询问的工具

model: sonnet              # 覆盖会话模型（可选）

effort: medium             # 覆盖会话 effort：low | medium | high | max（可选）
```

### 第四组：生命周期与其他

```yaml
hooks:                     # Skill 级钩子
  PostToolUse:             # 支持：PreToolUse | PostToolUse | UserPromptSubmit | Stop
    - matcher: "Write"
      hooks:
        - type: command
          command: "echo 'done'"

shell: bash                # Shell 预处理使用的 shell：bash | powershell
```

---

## 四、context: fork vs inline：选错等于白写

| | fork 模式 | inline 模式（默认） |
|--|----------|-------------------|
| 对话历史 | 不继承 | 继承完整历史 |
| 上下文消耗 | 独立窗口，不占主对话 | 占用主对话 token |
| 执行 Agent | 由 `agent` 字段指定 | 当前会话 |
| 适用场景 | 独立任务 | 需要对话上下文 |

### 判断法则

**如果指令本身就包含了完成任务所需的全部信息，用 fork；如果指令依赖对话上下文来理解，用 inline。**

- 复杂任务（代码审查、批量重构、全项目搜索）→ **必须 fork**（上下文生存策略）
- 需要对话历史（"帮我把刚才讨论的那个功能写出来"）→ **必须 inline**

---

## 五、Description 写作规范（最被低估的设计）

### 预算限制

- 所有 Skill 的 description 共享上下文预算：默认 = 上下文窗口的 1%，fallback 为 8000 字符
- 每个 Skill 的 description 在列表中截断为 250 字符

### 写 description 的原则

**前 250 个字符必须说清楚两件事：**
1. 这个 Skill 干什么
2. 什么时候该用它

**写 description 不是在写简介，是在写路由规则。** Claude 根据这段文字决定要不要自动调用你的 Skill。

### 写之前先回答三个问题

1. 用户真实会怎么提出这个需求？ — 用他们的话，不是你的抽象
2. 哪些相邻需求不应该触发？ — 明确边界，避免误触发
3. 加载这个 Skill 后，Agent 应该产出什么类型的结果？ — 预期产出要清晰

### 示例对比

```yaml
# ❌ 错误：无触发词，不知道什么时候用
description: 一个帮助写代码的工具

# ❌ 错误：像口号，不像路由触发器
description: 让你的代码更优雅、更高效、更安全

# ❌ 错误：超过 250 字符才说重点
description: 这个 Skill 是一个非常强大的代码审查工具，它可以帮助你...

# ✅ 正确：做什么 + 触发词 + 产出
description: |
  代码审查工具。当用户提到"代码审查"、"review"、
  "检查代码"时触发。审查质量、安全性、性能，输出审查报告。
```

### 精简策略

- 用动词开头：当用户提到...时触发
- 别写废话：去掉"这个 Skill 可以帮助你..."之类的客套
- 核心信息必须在前 250 字符内
- **改 description 必须同步补正例和反例评测，验证路由是否真的改善**

---

## 六、字符串替换变量

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 用户调用时传入的所有参数 |
| `$ARGUMENTS[N]` / `$N` | 按索引访问第 N 个参数（0 开始） |
| `${CLAUDE_SKILL_DIR}` | SKILL.md 所在目录的绝对路径 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |

**注意：** 如果正文中不包含 `$ARGUMENTS` 变量，参数自动追加为 `ARGUMENTS: <value>`

---

## 七、Shell 预处理（动态上下文注入）

正文支持 `` !`<command>` `` 语法。在发送给 Claude **之前**执行 shell 命令，输出替换占位符。

```markdown
当前 Git 状态：!`git status --short`
当前分支：!`git branch --show-current`
```

多行命令：
````markdown
```!
find . -name "*.md" -newer /tmp/last_check | head -20
```
````

**这个功能让 Skill 从"静态指令"变成了"动态工作流"。**

---

## 八、存放位置（按优先级高→低）

| 优先级 | 路径 | 范围 |
|--------|------|------|
| 1 | Managed settings | 组织内所有用户 |
| 2 | `~/.claude/skills/<name>/SKILL.md` | 用户全局 |
| 3 | `.claude/skills/<name>/SKILL.md` | 当前项目 |
| 4 | `<plugin>/skills/<name>/SKILL.md` | Plugin 作用域 |

- 同名 Skill，高优先级覆盖低优先级
- 嵌套目录的 `.claude/skills/` 也会被自动发现（支持 monorepo）

---

## 九、正文结构模板

```markdown
# Skill 标题

简要说明这个 skill 是做什么的。

## 触发条件

### 精确匹配
- 关键词1、关键词2、关键词3

### 模糊匹配
- 任务属于 XXX 领域

### 不触发条件
- 任务与 XXX 无关
- 更简单的工具可以处理

## 核心原则

> **一句话总结核心理念。**

## 工作流程

### 第一步：接收输入
1. 使用 $ARGUMENTS 获取参数
2. 解析用户输入
3. 确认理解

### 第二步：核心处理
1. 读取参考资料：${CLAUDE_SKILL_DIR}/references/xxx.md
2. 执行核心逻辑
3. 生成结果

### 第三步：输出结果
1. 格式化输出
2. 保存到指定位置
3. 展示给用户

## 输出规范

### 输出格式
- 格式类型：Markdown / JSON / 其他

### 输出位置
- 目录：D:\path\to\output\
- 文件名格式：{前缀}_{YYYYMMDD}.{扩展名}

### 输出模板
​```markdown
# {标题} - {日期}
## 任务描述
{用户需求}
## 执行结果
{具体内容}
## 总结
{要点回顾}
​```

## 参考资料

- 文件1：${CLAUDE_SKILL_DIR}/references/file1.md - {说明}

## 输入规范

### 必需输入
- {输入1}：{说明，从哪来，什么格式}

### 可选输入
- {输入3}：{说明，缺省时怎么处理}

### 缺材料时
- 追问用户 / 使用默认值 / 停止并说明原因（三选一）

## 注意事项

### 必须遵守
- 规则1：{详细说明}

### 禁止行为
- 禁止1：{详细说明}

## 示例

### 输入示例
{用户输入内容}

### 期望输出
{期望的输出内容}

### 反例：不该触发的情况
{看起来相似但不该走这个 Skill 的场景}

## 失败处理

| 失败类型 | 表现 | 修复动作 |
|----------|------|----------|
| 触发错误 | 该触发没触发 / 不该触发却触发了 | 改 description，补正例/反例 |
| 步骤遗漏 | 跳过关键步骤 | 补 workflow，加检查点 |
| 输出不合格 | 格式错、内容缺 | 补 examples，明确输出契约 |
| 工具误用 | 用错工具或参数 | 补 gotchas，脚本化稳定动作 |

**连续失败 3 次应停下来问用户，不要无限重试。**

## Gotchas

### G1: 看起来像但不该触发
- {具体场景和判断依据}

### G2: 容易误用的工具
- {具体注意事项}

### G3: 连续失败时停止
- {停止条件}
```

---

## 十、开发工作流（完整 5 步）

### 第一步：前置判断 — 是否值得 Skill 化

1. 这个任务重复出现过几次？ — 至少 3 次才值得
2. Agent 每次是否稳定犯同一类错？ — 不稳定犯错说明边界不清
3. 先跑 baseline — 拿 3-5 个真实 case 让 Agent 在没有 Skill 的情况下跑一遍

**如果任务不值得 Skill 化，直接告诉用户，不要硬写。**

### 第二步：三条路径选择

| 路径 | 适用场景 | 第一步 |
|------|----------|--------|
| **A. 找现成的** | 常见场景 | 去 skills.sh 或社区搜索 |
| **B. 改造现成的** | 方向接近但不完全匹配 | 保留核心结构，改 description/workflow/输出格式 |
| **C. 从零写** | 没有合适 Skill | 走完整流程 |

**先 A，再 B，最后 C。** 能复用就别从空白页开始。

### 第三步：生成 SKILL.md

按模板生成，确保：
- description 前 250 字符包含触发词
- 正文 ≤500 行
- 参考资料放 references/
- 使用 ${CLAUDE_SKILL_DIR} 引用
- 复杂任务用 context: fork

### 第四步：本地测试

```bash
# 在项目目录测试
claude -p "使用 <name> 完成 XXX 任务"
```

**验收清单（7 项全部通过才算合格）：**
- [ ] 用户换一种常见说法时，description 仍能触发
- [ ] 缺少必要输入时，Skill 知道该追问、假设还是停止
- [ ] 每个步骤都有明确动作，而不只是原则性描述
- [ ] 输出格式固定，能被人或下一个流程继续使用
- [ ] 至少有 3 个标准样例、2 个边界样例、1 个反例
- [ ] 关键 CLI 或脚本调用有参数示例和失败处理
- [ ] 停止条件明确：缺资料、权限失败、高风险动作时有处理路径

**创建 Evals 评测集：**
- 核心样本 5-10 个（用户最常提交的任务）
- 边界样本 3-5 个（空输入、资料不全、格式混乱）
- 已知坑 3-5 个（之前误触发、乱用工具的案例）

### 第五步：部署到全局

```bash
# 复制到全局目录（永远用 cp，不用 mv！）
cp -r <项目根目录>/<skill-name>/ ~/.claude/skills/<skill-name>/

# 验证
ls ~/.claude/skills/<skill-name>/
claude -p "使用 <name> 完成 XXX 任务"
```

---

## 十一、脚本化稳定动作

判断标准：
```
参数固定 + 每次都执行 → 脚本化（放 scripts/）
参数变化 + 需要判断 → 写进 workflow
偶尔执行 + 简单命令 → 写在 workflow 里即可
```

适合脚本化的动作：
- 每次都执行且参数固定（如读取文档目录、校验 JSON 格式）
- 涉及多步组合操作（如先 fetch → 判断结构 → 精读）
- 需要精确参数、人容易记错的命令

---

## 十二、Gotchas 飞轮：把失败变成边界

在 SKILL.md 中添加 `## Gotchas` 部分，记录真实失败案例：

```markdown
## Gotchas

### G1: 看起来像但不该触发
- 用户说"帮我看看这段代码"可能是问功能，不是审查
- 判断依据：是否提到"质量"、"安全"、"性能"等关键词

### G2: 容易误用的工具
- 不要用 Write 直接覆盖用户文件，先用 Edit 做 diff

### G3: 连续失败时停止
- 如果连续 3 次输出不符合格式要求，停下来问用户
```

---

## 十三、迭代与演进

### 泛化与特化时机

- **从特化开始** — 先覆盖一个具体场景，用真实 case 验证
- **泛化条件** — 同一条规则在 3+ 个不同 case 里重复出现时，再泛化
- **特化信号** — 泛化后误触发率上升，或不同场景输出格式差异太大

### 什么时候该退役

- 模型原生能力已经覆盖该场景
- 维护成本超过收益
- 流程已经过时
- 和新 Skill 大量重叠

**退役不是失败。** Skill 太多互相打架，Agent 反而更难做对。

### 个人 Skill vs 团队 Skill

| 维度 | 个人 Skill | 团队 Skill |
|------|-----------|-----------|
| 触发词 | 个人习惯用语 | 团队通用术语 |
| 输出格式 | 个人偏好 | 团队模板/规范 |
| 停止条件 | 个人判断 | 团队风险边界 |
| 示例 | 个人 case | 团队真实 case |
| 维护 | 一个人改 | 需要 review 机制 |

### 弱模型验收

如果更便宜、更弱的模型也能按流程产出稳定结果，说明 Skill 真的把经验写进了流程。如果跑偏，说明约束还不够明确。

---

## 十四、常见错误速查

| 问题 | 原因 | 解决 |
|------|------|------|
| Skill 未触发 | description 缺少关键词 | 前 250 字符包含触发词 |
| 上下文爆炸 | 正文太长或未用 fork | 正文 ≤500 行，复杂任务用 fork |
| 无法自动调用 | 设置了 disable-model-invocation | 改为 false 或删除该字段 |
| 用户看不到 | 设置了 user-invocable: false | 改为 true 或删除该字段 |
| 路径错误 | 使用了相对路径 | 用 ${CLAUDE_SKILL_DIR} 变量 |

---

## 十五、速记口诀

```
目录不是文件，
描述决定路由，
fork 保护上下文，
引用按需加载。
```

---

## 十六、内置 Skill 参考

| Skill | 功能 |
|-------|------|
| `/batch <instruction>` | 通过 git worktree 编排大规模并行代码修改 |
| `/claude-api` | 加载项目语言的 Claude API 参考 |
| `/debug [description]` | 启用 debug 日志排查问题 |
| `/loop [interval] <prompt>` | 按间隔重复执行 prompt |
| `/simplify [focus]` | 审查改动文件的复用性、质量、效率 |

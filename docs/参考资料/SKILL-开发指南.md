# Claude Code Skill 官方规范开发指南

> 基于 Claude Code 官方文档 (code.claude.com/docs/en/skills)
> 最后更新：2026-05-27

---

## 一、Skill 本质：是一个目录，不是一个文件

```
my-skill/
├── SKILL.md          # 必须——核心指令
├── references/       # 可选——参考资料，被引用时才加载
├── assets/           # 可选——模板、图片等
└── scripts/          # 可选——可执行脚本
```

**关键设计意图：** `references/` 目录是按需加载的。把参考资料塞进 SKILL.md 正文会每次调用都注入上下文，白白烧 token。放在 references/ 里只在 Claude 主动引用时才读取。

**官方建议：** 正文控制在 500 行以内（约 1500-2000 词），参考资料外挂。

---

## 二、三层渐进式加载机制

| 层级 | 何时加载 | 上下文占用 |
|------|---------|-----------|
| Level 1：元数据 | 会话启动时 | name + description，~100 tokens/skill |
| Level 2：SKILL.md 正文 | 被调用时 | 全文注入 |
| Level 3：目录资源 | 正文引用时 | 仅读取的文件 |

**核心理解：** description 始终在上下文里（占路由空间），正文和目录资源只在调用时才加载。

---

## 三、Description：你 Skill 的名片（最被低估的设计）

### 预算限制

```
所有 Skill 的 description 共享上下文预算：
- 默认 = 上下文窗口的 1%，fallback 为 8000 字符
- 每个 Skill 的 description 在列表中截断为 250 字符
- 环境变量 SLASH_COMMAND_TOOL_CHAR_BUDGET 可调整
```

### 写 description 的原则

**前 250 个字符必须说清楚两件事：**
1. 这个 Skill 干什么
2. 什么时候该用它

**写 description 不是在写简介，是在写路由规则。** Claude 根据这段文字决定要不要自动调用你的 Skill。

### 示例对比

```yaml
# ❌ 错误写法
description: 一个帮助写代码的工具

# ✅ 正确写法
description: |
  根据功能需求生成完整的 React 组件代码。当用户提到"创建组件"、
  "写个页面"、"新增功能模块"时触发。
```

### 精简策略

- 用动词开头：当用户提到...时触发
- 别写废话：去掉"这个 Skill 可以帮助你..."之类的客套
- 核心信息必须在前 250 字符内

---

## 四、Frontmatter 完整字段（官方 12 字段）

**所有字段都是可选的。** 强烈建议写 `description`。

### 第一组：标识（告诉系统你是谁）

```yaml
name: my-skill              # 也是 /slash-command 的名称
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

**隐藏用法：** `user-invocable: false` 可以写一个用户完全看不到的 Skill，让 Claude 在后台自动调用，比如自动格式化输出、自动检查文件结构。这是一种"隐形工作流"的设计思路。

### 第三组：执行模式（Skill 在哪跑）——实战价值最高

```yaml
context: fork              # fork = 独立子 Agent，省略 = 当前会话（inline）

agent: "general-purpose"   # context: fork 时使用的子 Agent 类型
                           # 内置：Explore | Plan | general-purpose
                           # 或 .claude/agents/ 中的自定义 Agent name
                           # 默认：general-purpose

allowed-tools: Read Write Edit Glob Grep  # Skill 激活时免询问的工具

model: sonnet              # 覆盖会话模型

effort: medium             # 覆盖会话 effort：low | medium | high | max
```

### 第四组：生命周期与其他

```yaml
hooks:                     # Skill 级钩子，与全局/Agent 级钩子隔离
  PostToolUse:             # 支持：PreToolUse | PostToolUse | UserPromptSubmit | Stop
    - matcher: "Write"
      hooks:
        - type: command
          command: "echo 'done'"

shell: bash                # Shell 预处理命令使用的 shell：bash | powershell
                           # powershell 需要 CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

---

## 五、context: fork vs inline：选错等于白写

| | fork 模式 | inline 模式（默认） |
|--|----------|-------------------|
| 对话历史 | 不继承 | 继承完整历史 |
| 上下文消耗 | 独立窗口，不占主对话 | 占用主对话 token |
| 执行 Agent | 由 `agent` 字段指定 | 当前会话 |
| 适用场景 | 独立任务 | 需要对话上下文 |

### 什么时候必须用 fork？

当你写了一个复杂的 Skill——比如代码审查、批量重构、全项目搜索——这些任务本身就会消耗大量 token。如果跑在 inline 模式，你主对话的上下文会被严重挤占。

**fork 模式不是可选功能，是上下文窗口的生存策略。**

### 什么时候必须用 inline？

当 Skill 需要你之前的对话信息——比如"帮我把刚才讨论的那个功能写出来"——这种情况 fork 模式拿不到对话历史，根本没法工作。

### 简单判断法则

**如果指令本身就包含了完成任务所需的全部信息，用 fork；如果指令依赖对话上下文来理解，用 inline。**

---

## 六、字符串替换变量

正文中以下变量会被运行时自动替换：

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 用户调用时传入的所有参数 |
| `$ARGUMENTS[N]` | 按索引访问第 N 个参数（0 开始） |
| `$N` | `$ARGUMENTS[N]` 的简写。`$0` = 第一个参数 |
| `${CLAUDE_SKILL_DIR}` | SKILL.md 所在目录的绝对路径 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |

**注意：** 如果正文中不包含 `$ARGUMENTS` 变量，参数自动追加为 `ARGUMENTS: <value>`

---

## 七、Shell 预处理（动态上下文注入）

正文支持 `` !`<command>` `` 语法。在发送给 Claude **之前**执行 shell 命令，输出替换占位符。

### 单行命令

```markdown
当前 Git 状态：
!`git status --short`
```

### 多行命令

````markdown
```!
find . -name "*.md" -newer /tmp/last_check | head -20
```
````

### 应用场景

- 自动读取 package.json 判断项目技术栈
- 检查最近修改的文件列表
- 获取当前分支名和未提交改动

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
- Plugin Skill 使用 `plugin-name:skill-name` 命名空间，不冲突
- `.claude/commands/` 旧文件仍有效，同名时 Skill 优先
- 嵌套目录的 `.claude/skills/` 也会被自动发现（支持 monorepo）

---

## 九、权限控制

三种方式限制 Claude 对 Skill 的访问：

| 方式 | 效果 |
|------|------|
| `/permissions` 中添加 `Skill` 到 deny | 禁用所有 Skill |
| `Skill(commit)` 精确匹配 / `Skill(deploy *)` 前缀匹配 | 允许/禁用特定 Skill |
| frontmatter `disable-model-invocation: true` | 从 Claude 上下文完全移除 |

`allowed-tools` 在 Skill 激活时授予免询问权限，但会话级权限设置仍然是基线。

---

## 十、分发方式

| 方式 | 路径 |
|------|------|
| 项目 Skill | 提交 `.claude/skills/` 到版本控制 |
| Plugin | 在 plugin 中创建 `skills/` 目录 |
| 企业 | 通过 managed settings 部署 |

---

## 十一、内置 Skill

Claude Code 自带以下 Skill：

| Skill | 功能 |
|-------|------|
| `/batch <instruction>` | 通过 git worktree 编排大规模并行代码修改 |
| `/claude-api` | 加载你项目语言的 Claude API 参考 |
| `/debug [description]` | 启用 debug 日志排查问题 |
| `/loop [interval] <prompt>` | 按间隔重复执行 prompt |
| `/simplify [focus]` | 审查改动文件的复用性、质量、效率 |

---

## 十二、最佳实践清单

### Description 写作

- [ ] 前 250 字符包含核心触发条件
- [ ] 用动词开头：当用户提到...时触发
- [ ] 去掉客套话和废话
- [ ] 明确说明触发词

### 正文结构

- [ ] 控制在 500 行以内
- [ ] 参考资料放 `references/` 目录
- [ ] 引用目录内文件用 `${CLAUDE_SKILL_DIR}/references/xxx.md`
- [ ] references 保持一层深度，避免嵌套引用链

### 执行模式选择

- [ ] 独立任务用 `context: fork`
- [ ] 需要对话上下文用 inline（默认）
- [ ] 复杂任务指定合适的 `agent` 类型

### 触发控制

- [ ] 需要用户手动触发时设置 `disable-model-invocation: true`
- [ ] 后台自动调用设置 `user-invocable: false`
- [ ] 限定文件范围使用 `paths`

---

## 十三、实战示例

### 示例 1：基础 Skill（inline 模式）

```yaml
---
name: commit
description: 提交暂存的更改，生成规范的 commit message。当用户提到"提交"、"commit"时触发。
allowed-tools: Bash
---

Review staged changes with `git diff --cached`, then create a concise
commit message following conventional commits format. Run `git commit`
with the message. If nothing is staged, check `git status` and suggest
what to stage.
```

### 示例 2：复杂 Skill（fork 模式）

```yaml
---
name: code-review
description: |
  代码审查工具。当用户提到"代码审查"、"review"、"检查代码"时触发。
  审查代码质量、安全性、性能，提供改进建议。
context: fork
agent: general-purpose
allowed-tools: Read Glob Grep
model: sonnet
effort: high
---

你是一个代码审查专家。请按以下步骤审查代码：

1. 使用 Glob 找到相关文件
2. 使用 Read 读取代码内容
3. 使用 Grep 搜索潜在问题
4. 生成审查报告

审查维度：
- 代码质量：可读性、可维护性
- 安全性：输入验证、SQL注入、XSS
- 性能：算法复杂度、资源管理

输出格式：Markdown 报告，包含问题、严重程度、改进建议。
```

### 示例 3：隐形 Skill（用户不可调用）

```yaml
---
name: auto-format
description: 自动格式化输出。当 Claude 生成代码时自动触发。
user-invocable: false
disable-model-invocation: false
allowed-tools: Read Write
---

检查 Claude 生成的代码是否符合项目规范：
1. 读取项目的 .editorconfig 或 .prettierrc
2. 检查代码格式是否符合规范
3. 如不符合，自动修正
```

### 示例 4：动态 Skill（Shell 预处理）

```yaml
---
name: project-status
description: 显示项目当前状态。当用户提到"项目状态"、"当前情况"时触发。
---

# 项目状态报告

当前 Git 分支：!`git branch --show-current`
未提交更改：!`git status --short | wc -l` 个文件

最近提交：
!`git log --oneline -5`

package.json 版本：!`node -p "require('./package.json').version"`
```

---

## 十四、常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| Skill 未触发 | description 缺少关键词 | 前 250 字符包含触发词 |
| 上下文爆炸 | 正文太长或未用 fork | 正文 ≤500 行，复杂任务用 fork |
| 无法自动调用 | 设置了 disable-model-invocation | 改为 false 或删除该字段 |
| 用户看不到 | 设置了 user-invocable: false | 改为 true 或删除该字段 |
| 路径错误 | 使用了相对路径 | 用 ${CLAUDE_SKILL_DIR} 变量 |

---

## 十五、核心要点总结

```
description 的前 250 个字符，决定 Claude 会不会用你的 Skill。
context: fork 不是选项，是生存策略。
写 Skill 不是在写指令，是在设计一个 AI 的工作流。
```

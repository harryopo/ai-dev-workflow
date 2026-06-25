# Skill 开发提示词模板（官方规范版）

当你需要开发一个新的 Claude Code skill 时，可以使用以下提示词模板：

---

## 模板 1：从零开始开发 Skill（推荐）

```
我需要开发一个 Claude Code skill，用于 [描述主要功能]。

请按照官方规范帮我生成完整的 SKILL.md 文件：

1. Frontmatter 配置：
   - name：skill 名称（全小写+连字符）
   - description：前 250 字符必须包含触发条件
   - context：是否需要 fork（复杂任务用 fork）
   - agent：子 Agent 类型（Explore/Plan/general-purpose）
   - allowed-tools：免询问的工具列表

2. 正文内容：
   - 触发条件（精确匹配、模糊匹配、不触发条件）
   - 工作流程（至少3个步骤）
   - 输出规范（格式、位置、模板）
   - 参考资料（使用 ${CLAUDE_SKILL_DIR} 变量）
   - 注意事项和限制条件

3. 要求：
   - 触发词要包含：[列出关键词]
   - 输出格式：[Markdown/JSON/其他]
   - 输出位置：[指定目录]
   - 特殊要求：[如有]

请确保：
- description 前 250 字符包含核心触发条件
- 正文控制在 500 行以内
- 参考资料放 references/ 目录，用 ${CLAUDE_SKILL_DIR} 引用
- 复杂任务使用 context: fork
```

---

## 模板 2：优化现有 Skill

```
我有一个现有的 skill，请帮我按照官方规范优化：

```yaml
[粘贴现有 SKILL.md 内容]
```

请优化以下方面：

1. Description 优化：
   - 前 250 字符包含触发条件
   - 去掉废话和客套
   - 用动词开头

2. Frontmatter 优化：
   - 添加缺失的字段
   - 优化 context 选择（fork vs inline）
   - 配置 allowed-tools

3. 正文优化：
   - 精简到 500 行以内
   - 参考资料移到 references/ 目录
   - 使用 ${CLAUDE_SKILL_DIR} 变量

4. 触发条件优化：
   - 明确触发词
   - 添加不触发条件
```

---

## 模板 3：批量生成 Skill

```
我需要为以下场景开发多个 skill：

场景1：[描述]
场景2：[描述]
场景3：[描述]

请为每个场景生成符合官方规范的 SKILL.md：

要求：
- 命名规范：[前缀/后缀]
- 统一风格：[输出格式]
- 共享资源：放在 references/ 目录
- description 前 250 字符包含触发词
- 复杂任务使用 context: fork
```

---

## 模板 4：教学型 Skill

```
我需要开发一个教学型 skill，用于教用户 [学习主题]。

教学要求：
1. 不只展示结果，还要解释原因
2. 提供示例和反例
3. 包含常见错误和避免方法
4. 提供练习题和答案

触发条件：
- 当用户询问 [相关问题] 时
- 当用户需要学习 [相关主题] 时

输出格式：
- 知识点讲解
- 示例代码
- 练习题
- 参考资料

请按照官方规范生成 SKILL.md，确保：
- description 包含触发词
- 正文 ≤500 行
- 参考资料放 references/
- 使用 ${CLAUDE_SKILL_DIR} 引用
```

---

## 模板 5：自动化工具 Skill

```
我需要开发一个自动化 skill，用于自动执行 [任务描述]。

自动化需求：
1. 接收输入：[输入类型]
2. 自动处理：[处理步骤]
3. 输出结果：[输出格式]

技术要求：
- 使用工具：[Read/Write/Bash/其他]
- 依赖环境：[环境要求]
- 错误处理：[异常情况]

触发条件：
- 当用户需要执行 [任务] 时
- 当用户输入 [关键词] 时

请按照官方规范生成 SKILL.md：
- 使用 context: fork（独立任务）
- 配置 allowed-tools
- 使用 Shell 预处理（如需要）
- 参考资料放 references/
```

---

## 模板 6：隐形 Skill（用户不可调用）

```
我需要开发一个隐形 skill，让 Claude 在后台自动调用。

功能描述：[描述功能]

触发条件：
- 当 Claude [执行某操作] 时自动触发
- 不需要用户手动调用

请按照官方规范生成 SKILL.md：
- user-invocable: false（用户看不到）
- disable-model-invocation: false（Claude 可自动调用）
- 正文简洁明了
```

---

## 模板 7：动态 Skill（Shell 预处理）

```
我需要开发一个动态 skill，使用 Shell 预处理获取实时信息。

功能描述：[描述功能]

需要获取的动态信息：
- Git 状态：!`git status --short`
- 当前分支：!`git branch --show-current`
- 最近提交：!`git log --oneline -5`
- 其他：[自定义命令]

输出格式：[Markdown/其他]

请按照官方规范生成 SKILL.md：
- 使用 !`command` 语法
- 正文简洁
- 触发词明确
```

---

## 使用说明

1. **选择模板**：根据你的需求选择合适的模板
2. **填写内容**：替换 `[占位符]` 为实际内容
3. **生成 SKILL.md**：让 Claude 根据模板生成完整的 SKILL.md
4. **保存位置**：`~/.claude/skills/你的skill名/SKILL.md`
5. **测试验证**：使用 `claude -p` 测试触发条件
6. **迭代优化**：根据测试结果优化 skill

---

## 示例：使用模板 1 开发 Skill

### 用户输入：
```
我需要开发一个 Claude Code skill，用于自动生成数据库 ER 图。

请按照官方规范帮我生成完整的 SKILL.md 文件：

1. Frontmatter 配置：
   - name：skill 名称（全小写+连字符）
   - description：前 250 字符必须包含触发条件
   - context：是否需要 fork（复杂任务用 fork）
   - agent：子 Agent 类型（Explore/Plan/general-purpose）
   - allowed-tools：免询问的工具列表

2. 正文内容：
   - 触发条件（精确匹配、模糊匹配、不触发条件）
   - 工作流程（至少3个步骤）
   - 输出规范（格式、位置、模板）
   - 参考资料（使用 ${CLAUDE_SKILL_DIR} 变量）
   - 注意事项和限制条件

3. 要求：
   - 触发词要包含：ER图、数据库图、表关系、数据库设计
   - 输出格式：Markdown + Draw.io 文件
   - 输出位置：D:\ai\claude code\skill开发\ER图\
   - 特殊要求：支持从 SQL 文件生成

请确保：
- description 前 250 字符包含核心触发条件
- 正文控制在 500 行以内
- 参考资料放 references/ 目录，用 ${CLAUDE_SKILL_DIR} 引用
- 复杂任务使用 context: fork
```

### Claude 输出：
完整的 SKILL.md 文件，包含符合官方规范的 frontmatter 和正文。

---

**提示：** 这些模板基于 Claude Code 官方规范，确保生成的 skill 符合最佳实践。

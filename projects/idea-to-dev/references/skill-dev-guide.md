# Claude Code Skill 开发指南

## 什么是 Skill？

Skill 是 Claude Code 的扩展能力包，通过 SKILL.md 文件定义，让 AI Agent 具备特定领域的工作能力。

## 目录结构

```
skill名/
├── SKILL.md              # 技能主文件（必须）
├── templates/            # 代码模板（可选）
├── references/           # 参考资料（可选）
├── examples/             # 示例代码（可选）
└── scripts/              # 辅助脚本（可选）
```

## SKILL.md 文件结构

```markdown
---
name: skill-name
description: |
  技能描述。触发词1、触发词2、触发词3。
argument-hint: "[参数说明]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Bash
---

# 技能名称

## 核心理念
[一句话说明这个技能做什么]

## 工作流程

### 第一步：[步骤名称]
[步骤说明]

### 第二步：[步骤名称]
[步骤说明]

## 注意事项
[使用注意事项]
```

## Frontmatter 字段说明

| 字段 | 必须 | 说明 |
|------|------|------|
| `name` | 是 | 技能名称，使用kebab-case |
| `description` | 是 | 描述 + 触发词，决定何时激活 |
| `argument-hint` | 否 | 参数提示 |
| `context` | 否 | `fork`（独立上下文）或 `main`（继承主上下文） |
| `agent` | 否 | `general-purpose`、`search`、`computer-teacher` 等 |
| `allowed-tools` | 否 | 允许使用的工具列表 |

## 安装位置

- **Claude Code**: `~/.claude/skills/`
- **Trae IDE**: `~/.trae-cn/skills/`

## 测试方法

```bash
# Claude Code
claude -p "使用 skill-name 完成 XXX"

# 或在对话中直接说触发词
"帮我用 skill-name 做 XXX"
```

## 最佳实践

1. **description 要精确**：包含足够的触发词，但不要过于宽泛
2. **工作流要完整**：从输入到输出的完整流程
3. **模板要可直接用**：复制后只需修改少量内容
4. **参考要精简**：只放必要的参考资料，避免过大
5. **示例要典型**：覆盖最常见用例

## 常见错误

- description 太宽泛导致误触发
- 工作流缺少错误处理
- 模板代码缺少注释
- 没有测试就部署

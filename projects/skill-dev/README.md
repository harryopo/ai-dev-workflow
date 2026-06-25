# Skill 开发助手

这是一个用于开发其他 Skill 的 Skill（元技能）。

## 功能

帮助用户快速开发符合 Claude Code 官方规范的 Skill，自动生成 SKILL.md 文件。

## 触发条件

当用户提到以下关键词时触发：
- 开发skill、创建skill、新建skill
- 写个skill、帮我做个skill
- 做一个skill、开发一个skill

## 使用方法

### 方法 1：直接调用

```bash
claude /skill-dev
```

### 方法 2：自然语言触发

```
帮我开发一个代码格式化 skill
```

```
创建一个数据库查询 skill
```

```
我想做一个自动测试的 skill
```

## 工作流程

1. **需求分析**：通过对话了解用户需求
2. **生成 SKILL.md**：根据官方规范生成完整文件
3. **保存和测试**：保存到正确位置并提供测试命令

## 输出

- 符合官方规范的 SKILL.md 文件
- 包含完整的 frontmatter 配置
- 包含触发条件、工作流程、输出规范
- 提供测试命令

## 参考资料

- `references/official-spec.md`：Claude Code 官方规范
- `references/template.md`：Skill 模板
- `references/example.md`：完整示例

## 目录结构

```
skill-dev/
├── SKILL.md              # 核心指令
├── README.md             # 本文件
└── references/           # 参考资料
    ├── official-spec.md  # 官方规范
    ├── template.md       # 模板文件
    └── example.md        # 完整示例
```

## 安装

将整个 `skill-dev` 目录复制到：

```
~/.claude/skills/skill-dev/
```

或

```
.claude/skills/skill-dev/
```

## 测试

```bash
claude -p "使用 skill-dev 开发一个代码格式化 skill"
```

# MCP 集成指南

> 本 Skill 是 Agent 内运行的设计 Skill，可通过配置以下 MCP Server 增强能力。
> 所有 MCP Server 都是可选的 — 本 Skill 在不配置任何 MCP 的情况下也可独立运行。

---

## 推荐 MCP Server

### 1. 21st.dev Magic MCP — 组件灵感搜索 + shadcn 组件生成

**用途**：在 design 阶段搜索 21st.dev 上数千个经过审核的高质量 UI 组件，生成 shadcn/compatible 组件代码。

**安装**：

```bash
# 方式 1：CLI 一键安装
npx @21st-dev/cli@latest install cursor --api-key <your-key>

# 方式 2：手动配置
# 在 ~/.cursor/mcp.json（或对应 IDE 的 MCP 配置）中添加：
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest", "API_KEY=\"your-api-key\""]
    }
  }
}
```

**API Key 获取**：https://21st.dev/magic/console

**在 Skill 中的使用**：
- design 阶段：输入 `/ui create a modern data table with sorting and pagination`
- 生成结果会包含 21st.dev 的组件设计知识
- GitHub: https://github.com/21st-dev/magic-mcp

---

### 2. Figma MCP — 设计稿上下文读取

**用途**：如果有 Figma 设计稿，直接读取设计上下文、CSS Token、组件结构，大幅减少 research 阶段的手动对话轮次。

**安装**：

```bash
# Figma MCP 是 Figma 官方提供的远程 MCP Server
# 需要 Figma 访问 Token 和文件 URL
# 配置参考：https://www.figma.com/mcp
```

**在 Skill 中的使用**：
- research 阶段：读取 Figma 设计稿 → 自动填充 DESIGN.md 的 Color / Typography / Spacing 等 section
- design 阶段：参考设计稿的 Token 生成代码
- review 阶段：对比 Figma 设计稿验证还原度

---

### 3. ShadCN MCP — shadcn/ui 组件生成

**用途**：在 design 阶段直接生成 shadcn/ui 兼容的组件代码。

**安装**：

```bash
# shadcn MCP 配置
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn", "mcp"]
    }
  }
}
```

**在 Skill 中的使用**：
- design 阶段：生成基础组件（Button、Card、Input 等）后，Agent 在此基础上应用 DESIGN.md 的定制样式

---

### 4. Open Design MCP — 150+ 设计系统访问

**用途**：如果已安装 Open Design 桌面应用，可直接访问其 150+ 品牌设计系统和 261 个插件。

**安装**：

```bash
# 先安装 Open Design 桌面应用
# https://open-design.ai/
# 然后安装 MCP 到 Agent
od mcp install claude    # Claude Code
od mcp install cursor    # Cursor
od mcp install trae      # Trae
```

**在 Skill 中的使用**：
- research 阶段：浏览 150+ 设计系统寻找参考
- design 阶段：注入匹配的 DESIGN.md 到上下文

---

## MCP 与 Skill 阶段对应表

| Skill 阶段 | 推荐 MCP | 效果 |
|:---:|------|------|
| research | Figma MCP + Open Design MCP | 自动读取设计稿 + 浏览设计系统库 |
| creative | — | 创意阶段不依赖 MCP |
| theme | — | 依赖 DESIGN.md |
| design | 21st.dev Magic MCP + ShadCN MCP | 组件灵感 + 代码生成 |
| review | Figma MCP | 设计稿对比验证 |

---

## 不使用 MCP 时的回退

本 Skill 的核心价值在于**调研驱动的设计方法论**和**去 AI 味规则**，不依赖任何 MCP Server。

不配置任何 MCP 时：
- 搜索设计参考 → 走 SKILL.md 的 14 个设计作品平台 WebSearch 流程
- 组件生成 → Agent 直接编码（已有 50+ 风格 / 161 色板 / 99 UX 准则）
- 设计对比 → review 子技能的 15 维度 + 8 项设计灵魂追溯

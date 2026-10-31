# MCP 与可调用通道总表

> 本 Skill 是 Agent 内运行的设计 Skill，增强能力分两类：**MCP Server**（下表）与**旁路工具**（§6 本机脚本通道）。
> 所有增强都是可选的 — 本 Skill 在不配置任何 MCP 的情况下也可独立运行。
> **验证状态列**（诚实纪律）：只有实测通过的条目才可标"已验证"；"未验证"= 只有安装说明、未在本机跑通过——引用其能力表述时须带此状态，不得当作已确认可用。

---

## 推荐 MCP Server

| # | MCP | 用途 | 验证状态 |
|---|-----|------|---------|
| 1 | **21st.dev Magic** | 组件灵感搜索 + shadcn 兼容组件生成（**可直接把组件装进代码库**，回流映射首选） | 未验证 |
| 2 | **Figma MCP** | 设计稿上下文/Token/截图读取，research 减轮次、review 验还原度 | 未验证 |
| 3 | **ShadCN MCP** | shadcn/ui 兼容组件代码生成 | 未验证 |
| 4 | **Open Design MCP** | 150+ 设计系统与 261 插件访问 | 未验证 |

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

**完整消费流程**（并入自本机 figma skill，三步）：
1. `get_design_context`：按 Figma 文件 URL/节点取设计上下文（结构化 Token/布局）
2. `get_screenshot`：取节点截图做视觉对照
3. `assets` 端点：取切图素材
排障与 setup 细节见本机 figma skill（`C:\Users\Administrator\.zcode\skills\figma\`）。

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
- 搜索设计参考 → `references/inspiration-sources.md` 双层地图（agent 检索层 + 用户浏览目录）+ §0 动态搜索优先
- 组件生成 → Agent 直接编码（50+ 风格 / 161 色板口径 / 99 UX 准则；组件库见 component-block-catalog.md 决策树）
- 设计对比 → review 子技能的灵魂追溯 + 19 维度审查

---

## 6. 旁路工具（本机脚本通道，非 MCP）

| 工具 | 所在 | 能力 | 进入条件 |
|------|------|------|---------|
| **Seedream 生图** | byted-seedream-image-generate skill（CLI 脚本 `seedream_image_generate`） | design 阶段生成 hero 配图/产品示意图/插画；提示词模板与纪律见 `references/media-craft.md` §4 | 需 `ARK_API_KEY` 等环境变量；未配置 = 通道关闭，回退"无图设计"，**禁占位 CDN 顶替** |
| **site-cloner 整站抓取** | site-cloner skill（SingleFile/Playwright 工具链） | 用户给整站 URL → 抓全站 → 喂 research「现有风格审计模式」/任意网站 Token 提取 | 工具链已装即可；只抓公开页面 |
| **web-artifacts-builder 打包** | web-artifacts-builder skill（bundle-artifact.sh） | React+shadcn 多组件 artifact 打包单 HTML——sfd 产出的可选输出通道 | 与 sfd 产出形态匹配时选用 |

## 7. 开源 skill 生态（发现新 skill 的入口）

- **ComposioHQ/awesome-claude-skills**（github.com/ComposioHQ/awesome-claude-skills）：社区精选清单
- **alirezarezvani/claude-skills**（380+ skills 聚合）
- **GitHub topic `ai-skills`**：持续更新的聚合页
- 用法：定期浏览发现新的设计类 skill → 对照本 skill 查缺补漏（v2.14.0/v2.15.0 的机制即部分源自对 impeccable 等本机 skill 的普查）

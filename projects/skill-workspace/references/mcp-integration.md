# MCP整合指南

本文档详细说明如何实现 MCP (Model Context Protocol) 与 Skill 的互补整合。

---

## 架构原则

### 核心分工

| 组件 | 职责 | 不应该做 |
|------|------|----------|
| **MCP Server** | 外部工具连接（API、数据库、浏览器、文件系统） | 不包含工作流逻辑、领域知识、决策判断 |
| **Skill** | 领域知识、工作流程、最佳实践、决策逻辑 | 不硬编码外部工具连接细节、不直接实现工具协议 |

### 互补模式

1. **MCP包装为Skill**：MCP提供工具能力，Skill提供使用这些工具的工作流
   - 示例：browser MCP + web-scraping Skill
   - MCP提供点击、输入、截图工具，Skill提供爬取流程、反爬策略、数据提取逻辑

2. **Skill调用MCP**：现有Skill增强，通过MCP获得外部工具能力
   - 示例：code-review Skill + github MCP
   - Skill已有审查逻辑，通过MCP获得读取PR、评论等能力

3. **MCP Gateway（企业级）**：统一MCP入口，Skill通过Gateway访问工具
   - 统一权限控制、审计日志、速率限制

---

## MCP Server来源

### Tier 1: 官方MCP Servers
- GitHub: `modelcontextprotocol/servers` 仓库
- 包含：filesystem、github、git、postgres、browser-use、fetch、memory等

### Tier 2: 社区MCP
- awesome-mcp-servers列表
- npm: `@modelcontextprotocol/*` 包
- GitHub搜索：`mcp-server` topic

### Tier 3: 自定义MCP
- 使用mcp-builder Skill从零开发
- 使用FastMCP（Python）或MCP SDK（TypeScript）

---

## 整合流程详细步骤

### 第一步：MCP生态调研

**搜索命令：**
```bash
# 搜索官方MCP servers
curl -s "https://api.github.com/repos/modelcontextprotocol/servers/contents/src"

# 搜索npm MCP包
npm search @modelcontextprotocol

# GitHub搜索
curl -s "https://api.github.com/search/repositories?q=mcp-server+topic:mcp&sort=stars"
```

**评估维度：**
| 维度 | 检查项 |
|------|--------|
| 可信度 | 官方/知名社区/个人开发者 |
| 维护状态 | 最后更新时间、open issues数量 |
| 安全性 | 是否有安全审计、权限模型 |
| 文档 | 是否有清晰文档、示例 |
| Star数 | 社区认可度 |

### 第二步：确认整合模式

**模式A：MCP包装为Skill**
适用场景：已有成熟MCP Server，需要为其提供使用指南和工作流

SKILL.md模板：
```markdown
---
name: {skill-name}
description: |
  {功能描述}。当用户提到{触发词}时触发。
  依赖 {mcp-server} MCP提供工具能力。
---

# {Skill名称}

{功能说明}

## MCP工具依赖

本Skill依赖以下MCP Server：

| MCP Server | 工具 | 用途 |
|------------|------|------|
| {server} | {tool1, tool2} | {用途} |

**MCP配置：**
```json
{
  "mcpServers": {
    "{server-name}": {
      "command": "{command}",
      "args": ["{args}"]
    }
  }
}
```

## 工作流程

1. 第一步：...（调用MCP工具）
2. 第二步：...（处理结果）
```

**模式B：Skill + MCP协同**
适用场景：现有Skill需要增加外部工具能力

在SKILL.md中添加：
```markdown
## 可选MCP增强

如果配置了 {mcp-server} MCP，本Skill可以：
- {增强功能1}
- {增强功能2}

**无MCP时降级方案：** {说明如何在没有MCP时工作}
```

### 第三步：增强安全审查

除标准安全审查外，MCP整合需检查：

1. **语义-行为一致性**
   ```
   检查清单：
   - [ ] MCP工具描述与实际功能一致
   - [ ] Skill中对MCP工具的说明准确
   - [ ] 没有"描述说只读实际需要写"的情况
   ```

2. **权限最小化**
   ```
   检查清单：
   - [ ] MCP只请求必要的权限
   - [ ] Skill不滥用MCP工具
   - [ ] 文件系统MCP有路径限制
   ```

3. **组合风险**
   ```
   高危组合：
   - filesystem(write) + fetch/network → 数据泄露
   - bash/execute + fetch → 远程代码执行
   - 任何两个高权限MCP同时存在 → 仔细审查
   ```

### 第四步：本地测试

**测试检查清单：**
- [ ] MCP Server能正常启动
- [ ] Agent能发现MCP工具
- [ ] Skill能正确调用MCP工具
- [ ] 异常情况处理（MCP不可用、超时、错误）
- [ ] 降级方案工作正常（如有）

### 第五步：部署配置

**各平台MCP配置位置：**

| 平台 | 配置位置 | 说明 |
|------|----------|------|
| Claude Code | `~/.claude.json` 或项目 `.mcp.json` | 全局/项目级 |
| TRAE | `.trae/mcp.json` | 项目级 |
| Cursor | `~/.cursor/mcp.json` | 全局 |
| 通用 | `~/.mcp/config.json` | 通用 |

**配置示例：**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

## MCP整合报告模板

```markdown
# MCP整合报告

**整合时间：** {date}
**Skill名称：** {skill-name}
**MCP Server：** {mcp-server}
**整合模式：** 模式A/模式B/模式C

## MCP调研结果

| 维度 | 评估 |
|------|------|
| 来源 | {官方/社区/自定义} |
| Stars | {数量} |
| 最后更新 | {日期} |
| 安全评级 | {SAFE/WARNING/DANGER/BLOCK} |

## 安全审查结果

- [ ] 语义-行为一致性通过
- [ ] 权限最小化验证通过
- [ ] 组合风险评估通过
- [ ] 无高危组合

## 配置文件

### MCP配置
```json
{配置内容}
```

### SKILL.md更新部分
{关键变更摘要}

## 测试结果

- [ ] MCP连接成功
- [ ] 工具调用正常
- [ ] 降级方案工作
- [ ] 审查评分达标

## 下一步

- [ ] 部署到目标平台
- [ ] 更新MCP配置
- [ ] 用户验收
```

---

## 常见MCP Servers参考

| MCP Server | 包名 | 用途 | 权限要求 |
|------------|------|------|----------|
| filesystem | `@modelcontextprotocol/server-filesystem` | 文件系统操作 | Read/Write（指定目录） |
| github | `@modelcontextprotocol/server-github` | GitHub操作 | Network（API调用） |
| postgres | `@modelcontextprotocol/server-postgres` | PostgreSQL数据库 | Network（数据库连接） |
| browser-use | `@modelcontextprotocol/server-browseruse` | 浏览器自动化 | Network + 本地执行 |
| fetch | `@modelcontextprotocol/server-fetch` | HTTP请求 | Network |
| memory | `@modelcontextprotocol/server-memory` | 知识图谱记忆 | Local文件读写 |
| brave-search | `@modelcontextprotocol/server-brave-search` | 网页搜索 | Network |
| google-drive | `@modelcontextprotocol/server-gdrive` | Google Drive | Network + OAuth |

---

## 反模式（避免）

❌ **反模式1：在Skill里硬编码MCP启动命令**
- 正确：让用户在平台配置中添加MCP，Skill只说明依赖
- 错误：Skill中包含`npx @modelcontextprotocol/server-xxx`

❌ **反模式2：Skill与特定MCP强耦合无降级**
- 正确：提供MCP增强功能，同时说明无MCP时的降级方案
- 错误：没有MCP就完全无法使用

❌ **反模式3：忽略组合攻击风险**
- 正确：评估Skill + MCP的组合权限风险
- 错误：只单独审查Skill和MCP，不看组合

❌ **反模式4：请求过多权限**
- 正确：文件系统MCP只允许访问必要目录
- 错误：filesystem MCP允许访问整个`/`或`C:\`

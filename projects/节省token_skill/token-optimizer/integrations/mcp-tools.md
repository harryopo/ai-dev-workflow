# MCP 工具集成

## 核心 MCP 工具

| 工具 | 用途 | 降级方案 |
|------|------|----------|
| sequential-thinking | 深度思考和推理链 | TodoWrite 分步规划 |
| mcp-shrimp-task-manager | 任务分解与依赖管理 | TodoWrite 任务列表 |
| context7 | 第三方库文档查询 | WebSearch + GitHub |
| interactive-feedback | 结构化用户交互 | 文本结构化反馈 |
| filesystem | 文件系统操作 | 原生文件操作 |

## 容错机制

### 自动重试
- 网络超时等临时故障，自动重试 3 次
- 指数退避：1s → 2s → 4s

### 降级矩阵
```
MCP 工具故障 → 检查降级方案 → 使用替代工具 → 通知用户
```

### 通知示例
```
⚠️ MCP 工具降级通知
【故障工具】：sequential-thinking
【降级方案】：TodoWrite 分步规划
【功能影响】：无法进行思维链验证，分析深度降低
【需要注意】：请额外关注任务依赖关系和边界条件
```

## 集成示例

### Sequential Thinking
```python
# 使用 Sequential Thinking 进行深度思考
result = mcp.sequential_thinking.think(
    thought="分析问题...",
    thought_number=1,
    total_thoughts=5
)
```

### Context7
```python
# 使用 Context7 查询库文档
docs = mcp.context7.get_docs(
    library="react",
    query="useEffect hook"
)
```

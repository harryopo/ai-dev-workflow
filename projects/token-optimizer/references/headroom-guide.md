# Headroom 使用指南

## 简介

Headroom 是一个专为 AI Agent 设计的可逆上下文压缩层，通过结构感知引擎在不丢失信息前提下最高节省 95% Token。

## 安装

```bash
# Python
pip install "headroom-ai[all]"

# Node / TypeScript
npm install headroom-ai
```

## 使用模式

### 1. Library 模式

直接在代码中调用压缩函数：

```python
from headroom import compress

# 压缩文本
compressed = compress(your_text)

# 压缩消息列表
messages = [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
compressed_messages = compress(messages)
```

### 2. Proxy 模式

启动代理服务器，零代码更改：

```bash
headroom proxy --port 8787
```

然后将 API 请求发送到 `http://localhost:8787`。

### 3. Agent Wrap 模式

包装现有的 AI Agent：

```bash
# Claude Code
headroom wrap claude

# Codex
headroom wrap codex

# Cursor
headroom wrap cursor
```

### 4. MCP Server 模式

作为 MCP 服务器运行：

```bash
headroom mcp install
```

## 压缩算法

### SmartCrusher (JSON)

专门用于压缩 JSON 数据：
- 数组字典压缩
- 嵌套对象压缩
- 混合类型压缩

### CodeCompressor (代码)

AST 感知的代码压缩：
- Python
- JavaScript/TypeScript
- Go
- Rust
- Java
- C++

### Kompress-base (文本)

通用文本压缩模型：
- 基于 HuggingFace 的压缩模型
- 训练于 Agent 追踪数据
- 保持语义完整性

## 可逆压缩 (CCR)

Headroom 支持可逆压缩（Content Compression and Retrieval）：

1. 原始数据存储在本地
2. LLM 接收压缩后的内容
3. LLM 可通过 `headroom_retrieve` 工具检索原始内容

## 性能数据

| 工作负载 | 压缩前 | 压缩后 | 节省比例 |
|----------|--------|--------|----------|
| 代码搜索 (100 结果) | 17,765 | 1,408 | 92% |
| SRE 故障排查 | 65,694 | 5,118 | 92% |
| GitHub Issue 分类 | 54,174 | 14,761 | 73% |
| 代码库探索 | 78,502 | 41,254 | 47% |

## 配置选项

```python
from headroom import compress

# 指定模型
result = compress(text, model="kompress-base")

# 自定义配置
result = compress(text, config={
    "max_tokens": 1000,
    "preserve_structure": True,
    "reversible": True
})
```

## 集成示例

### 与 Anthropic SDK 集成

```python
from anthropic import Anthropic
from headroom import withHeadroom

# 创建带 Headroom 的客户端
client = withHeadroom(Anthropic())

# 正常使用，自动压缩
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "..."}]
)
```

### 与 OpenAI SDK 集成

```python
from openai import OpenAI
from headroom import withHeadroom

client = withHeadroom(OpenAI())
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "..."}]
)
```

## 最佳实践

1. **选择合适的模式**
   - 开发测试：Library 模式
   - 生产环境：Proxy 模式
   - 多 Agent：MCP Server 模式

2. **监控压缩效果**
   - 使用 `headroom perf` 查看性能
   - 定期检查压缩比例

3. **保持可逆性**
   - 启用 CCR 以保留原始数据
   - 定期备份压缩历史

## 常见问题

### Q: 压缩会影响答案质量吗？
A: 不会。Headroom 使用结构感知压缩，保持语义完整性。基准测试显示答案准确率保持不变。

### Q: 支持哪些 Agent？
A: 支持 Claude Code、Codex、Cursor、Aider、Copilot CLI 等。

### Q: 数据安全吗？
A: 是的。Headroom 在本地运行，数据不会上传到任何服务器。

### Q: 如何查看压缩效果？
A: 使用 `headroom perf` 命令查看实时压缩统计。

## 更多资源

- GitHub: https://github.com/chopratejas/headroom
- 文档: https://headroom-docs.vercel.app/docs
- Discord: https://discord.gg/yRmaUNpsPJ

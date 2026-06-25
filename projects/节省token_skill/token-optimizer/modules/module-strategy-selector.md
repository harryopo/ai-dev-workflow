# Module: Strategy Selector

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 1: Strategy Selector

## 8 种优化策略决策树

### 策略 1: 全量记忆
- 场景：短对话（<10轮），信息完整性要求高
- 节省：0%（无节省）
- 实现：保留所有对话历史

### 策略 2: 滑动窗口
- 场景：短对话，信息完整性要求低
- 节省：极高（固定窗口）
- 实现：只保留最近 N 轮对话

### 策略 3: 摘要压缩
- 场景：长对话（>20轮），信息密度低
- 节省：70-90%
- 实现：定期让 LLM 压缩旧对话为摘要

### 策略 4: 向量检索(RAG)
- 场景：需要长期记忆，语义检索
- 节省：高（topK）
- 实现：向量化存储 + 相似度检索

### 策略 5: 分层混合记忆
- 场景：长对话，信息密度高
- 节省：高
- 实现：短期窗口 + 中期摘要 + 长期向量

### 策略 6: 状态变量提取
- 场景：任务型对话（订票/表单）
- 节省：极高（近乎0）
- 实现：提取结构化状态变量

### 策略 7: 工具/函数调用
- 场景：Agent 场景
- 节省：极高
- 实现：让模型自主管理记忆工具

### 策略 8: CLI 代理压缩
- 场景：CLI 输出优化
- 节省：60-90%
- 实现：RTK 代理压缩命令输出

## 场景匹配算法

```python
def select_strategy(scenario):
    if scenario.turns < 10:
        if scenario.integrity == "high":
            return "全量记忆"
        else:
            return "滑动窗口"
    elif scenario.turns > 20:
        if scenario.density == "high":
            return "分层混合记忆"
        elif scenario.need_long_term:
            return "向量检索(RAG)"
        else:
            return "摘要压缩"
    elif scenario.type == "task":
        return "状态变量提取"
    elif scenario.type == "agent":
        return "工具/函数调用"
    elif scenario.has_cli_output:
        return "CLI 代理压缩"
    else:
        return "摘要压缩"  # 默认
```

## 输出格式

```
Token 优化策略推荐
═══════════════════════════════════════
场景：[场景描述]
推荐策略：[策略名称]
预计节省：[X]%
实施步骤：
1. [步骤1]
2. [步骤2]
═══════════════════════════════════════
```

## 与现有模块的映射

| 策略 | 对应模块 | 模块编号 |
|------|----------|----------|
| 全量记忆 | Module 1 (Audit) | 1 |
| 滑动窗口 | Module 3 (Compression) | 3 |
| 摘要压缩 | Module 3 (Compression) | 3 |
| 向量检索 | 新增（待开发） | - |
| 分层混合 | Module 4 (Canvas) | 4 |
| 状态变量 | Module 1 (Audit) | 1 |
| 工具调用 | Module 7 (Retry) | 7 |
| CLI 压缩 | 新增（待开发） | - |

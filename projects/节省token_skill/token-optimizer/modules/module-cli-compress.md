# Module: CLI Compress

> Part of Token Optimizer V2 Five-Layer Architecture
> Layer 2: Optimization Modules

## 四种压缩策略

### 策略 1: 智能过滤
- 适用场景：测试输出
- 压缩率：90%
- 实现方式：
  - 100 个 PASSED → "100 个测试全部通过"
  - 保留失败测试的完整信息

### 策略 2: 分组聚合
- 适用场景：git log, ls, grep
- 压缩率：80%
- 实现方式：
  - git log 50 条 → "最近 50 次提交摘要"
  - ls 100 个文件 → "100 个文件，按类型分组"

### 策略 3: 智能截断
- 适用场景：错误堆栈
- 压缩率：70%
- 实现方式：
  - 只保留前 5 行错误信息
  - 保留文件路径和行号

### 策略 4: 去重处理
- 适用场景：重复信息
- 压缩率：60%
- 实现方式：
  - 相同信息只保留一份
  - 用引用替代重复内容

## RTK 集成

### 安装
```bash
# macOS
brew install rtk

# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh

# 初始化（Claude Code）
rtk init -g
```

### 配置
```toml
# ~/.config/rtk/config.toml
[commands]
exclude = ["vim", "nano", "less"]

[tee]
enabled = true  # 失败时保存完整原始输出
```

### 常用命令
```bash
# 查看统计
rtk gain --project

# 分析最耗 Token 的命令
rtk discover

# 查看过滤掉的完整信息
rtk tee show

# 绕过 RTK 执行原始命令
/usr/bin/git status
```

## 压缩策略选择

| 命令类型 | 推荐策略 | 预计节省 |
|----------|----------|----------|
| cargo test / pytest | 智能过滤 | 90% |
| git add/commit/push | 分组聚合 | 92% |
| ls / grep / git log | 分组聚合 | 80% |
| npm install / pip install | 智能截断 | 85% |
| 错误堆栈 | 智能截断 | 70% |
| 重复输出 | 去重处理 | 60% |

## 监控与调优

### 查看压缩效果
```bash
rtk gain --project
```

输出示例：
```
Project: my-project
Commands processed: 13
Input tokens: 18.2k
Output tokens: 5.9k
Tokens saved: 12.4k
Savings: 67.8%
```

### 调优建议
1. 如果压缩过度导致 AI 重新执行命令 → 调整压缩阈值
2. 如果关键信息被过滤 → 将该命令加入排除列表
3. 定期运行 `rtk discover` 分析优化空间

# RTK 集成指南

## 概述
RTK (Rust Token Killer) 是一个 CLI 代理，在命令行输出到达 LLM 之前做智能压缩和过滤。

## 安装与配置

### 安装
```bash
# macOS
brew install rtk

# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh

# Windows (via cargo)
cargo install --git https://github.com/rtk-ai/rtk
```

### 初始化
```bash
# Claude Code
rtk init -g

# Codex
rtk init -g --codex

# Gemini CLI
rtk init -g --gemini

# Cursor
rtk init --agent cursor
```

### 配置文件
```bash
rtk config --create
# 编辑 ~/.config/rtk/config.toml
```

## 使用方式

### 自动 Hook
RTK 初始化后会自动 hook 常用命令：
- git, ls, grep, find
- npm, pip, cargo, maven
- pytest, jest, cargo test

### 手动包装
```bash
rtk git status
rtk mvn test
rtk npm install
```

### 绕过 RTK
```bash
/usr/bin/git status
```

## 监控与调试

### 查看统计
```bash
rtk gain --project
rtk gain --global
```

### 分析优化空间
```bash
rtk discover
```

### 查看过滤信息
```bash
rtk tee show
```

## 最佳实践

1. **保持默认配置**：除非有特殊需求，不要修改压缩阈值
2. **定期检查统计**：每周运行 `rtk gain --project` 查看节省效果
3. **调试时绕过**：遇到问题时用完整路径执行原始命令
4. **保留失败输出**：开启 `tee.enabled = true` 以便调试

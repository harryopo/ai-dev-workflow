# Token 优化模板文件

## 1. .claudeignore 模板

### 通用模板
```gitignore
# 依赖目录
node_modules/
.next/
dist/
build/
vendor/
venv/
__pycache__/
.venv/
env/

# 构建产物
*.log
*.lock
coverage/
.env*
*.pyc
*.pyo
*.class
*.o
*.so
*.dylib

# IDE 配置
.idea/
.vscode/
*.swp
*.swo
*~

# 大型数据文件
*.csv
*.json
*.xml
*.sql
*.db
*.sqlite

# 文档和图片（如果不需要）
*.pdf
*.doc
*.docx
*.xls
*.xlsx
*.ppt
*.pptx
*.png
*.jpg
*.jpeg
*.gif
*.svg
*.ico

# 测试和临时文件
tmp/
temp/
.cache/
.nyc_output/
```

### Python 项目模板
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Logs
*.log

# Environment
.env
.env.local
.env.*.local
```

### Node.js 项目模板
```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Build
build/
dist/
.next/
out/

# Testing
coverage/
.nyc_output/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 2. CLAUDE.md 模板

### 通用模板
```markdown
# CLAUDE.md

## Rules
- 规则 1: [简短描述]
- 规则 2: [简短描述]
- 规则 3: [简短描述]
- 规则 4: [简短描述]
- 规则 5: [简短描述]

## Key Files
- [文件描述]: path/to/file1.md
- [文件描述]: path/to/file2.md
- [文件描述]: path/to/file3.md

## Quick Reference
- [常用命令或配置]
```

### Python 项目模板
```markdown
# CLAUDE.md

## Rules
- 使用 Python 3.8+ 语法
- 遵循 PEP 8 代码规范
- 为每个函数编写类型注解
- 使用 pytest 编写测试
- 提交前运行 `black` 格式化

## Key Files
- 主入口: src/main.py
- 配置: config/settings.py
- 测试: tests/

## Quick Reference
- 运行测试: `pytest`
- 格式化: `black .`
- 类型检查: `mypy src/`
```

### TypeScript 项目模板
```markdown
# CLAUDE.md

## Rules
- 使用 TypeScript 严格模式
- 遵循 ESLint 规则
- 为每个函数编写类型定义
- 使用 Jest 编写测试
- 提交前运行 `npm run lint`

## Key Files
- 入口: src/index.ts
- 类型定义: src/types/
- 测试: src/__tests__/

## Quick Reference
- 运行测试: `npm test`
- 检查类型: `npm run typecheck`
- 构建: `npm run build`
```

## 3. 优化报告模板

### 简单报告模板
```markdown
# Token 优化报告

## 当前状态
- CLAUDE.md 大小: [X] tokens
- 会话平均长度: [X] 条消息
- 主要消耗来源: [来源列表]

## 优化建议

### 高优先级
1. [建议 1]: 预期节省 [X]%
2. [建议 2]: 预期节省 [X]%

### 中优先级
3. [建议 3]: 预期节省 [X]%
4. [建议 4]: 预期节省 [X]%

### 低优先级
5. [建议 5]: 预期节省 [X]%

## 实施步骤
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

## 预期效果
- Token 消耗降低: [X]%
- 月度成本节省: $[X]（估算）
```

### 详细报告模板
```markdown
# Token 优化详细报告 - [日期]

## 1. 执行摘要

**主要发现：**
- [发现 1]
- [发现 2]
- [发现 3]

**总体优化潜力：** [X]%

## 2. 当前状态分析

### 2.1 配置文件
- CLAUDE.md 大小: [X] tokens（建议 500 以内）
- .claudeignore 状态: [已配置/未配置]
- MCP 服务器: [X] 个（[Y] 个活跃）

### 2.2 使用模式
- 平均会话长度: [X] 条消息
- 主要工具调用: [工具列表]
- 模型使用分布: [百分比]

### 2.3 成本分析
- 日均 Token 消耗: [X]
- 月度成本: $[X]
- 主要消耗来源: [来源及占比]

## 3. 优化建议

### 3.1 高优先级（预期节省 [X]%）

#### 建议 1: [建议标题]
**问题：** [问题描述]
**方案：** [解决方案]
**实施：** [具体步骤]
**验证：** [验证方法]

#### 建议 2: [建议标题]
**问题：** [问题描述]
**方案：** [解决方案]
**实施：** [具体步骤]
**验证：** [验证方法]

### 3.2 中优先级（预期节省 [X]%）

#### 建议 3: [建议标题]
**问题：** [问题描述]
**方案：** [解决方案]
**实施：** [具体步骤]
**验证：** [验证方法]

#### 建议 4: [建议标题]
**问题：** [问题描述]
**方案：** [解决方案]
**实施：** [具体步骤]
**验证：** [验证方法]

### 3.3 低优先级（预期节省 [X]%）

#### 建议 5: [建议标题]
**问题：** [问题描述]
**方案：** [解决方案]
**实施：** [具体步骤]
**验证：** [验证方法]

## 4. 配置文件

### 4.1 .claudeignore
```gitignore
[生成的忽略规则]
```

### 4.2 CLAUDE.md 优化建议
```markdown
[优化后的 CLAUDE.md 内容]
```

## 5. 实施计划

### 阶段 1: 立即实施（1-2 天）
1. [任务 1]
2. [任务 2]
3. [任务 3]

### 阶段 2: 短期优化（1 周）
1. [任务 4]
2. [任务 5]
3. [任务 6]

### 阶段 3: 长期改进（1 个月）
1. [任务 7]
2. [任务 8]
3. [任务 9]

## 6. 预期效果

### 6.1 Token 节省
- 初级优化: 降低 [X]%
- 中级优化: 降低 [X]%
- 高级优化: 降低 [X]%
- **总体优化: 降低 [X]%**

### 6.2 成本节省
- 月度成本节省: $[X]（估算）
- 年度成本节省: $[X]（估算）

### 6.3 效率提升
- 响应速度提升: [X]%
- 任务完成质量: [提升/保持]

## 7. 监控和维护

### 7.1 监控指标
- Token 消耗量（每周检查）
- 响应时间（持续监控）
- 任务完成质量（用户反馈）

### 7.2 定期审查
- 每周: 检查 token 使用情况
- 每月: 分析优化效果
- 每季度: 调整优化策略

## 8. 附录

### 8.1 参考资料
- [参考资料 1]
- [参考资料 2]
- [参考资料 3]

### 8.2 工具和命令
- `/usage`: 查看当前会话 token 用量
- `/cost`: 查看预估费用
- `/compact`: 压缩对话
- `/clear`: 清除对话

### 8.3 常见问题
- Q: [问题 1]
- A: [答案 1]
- Q: [问题 2]
- A: [答案 2]
```

## 4. 会话管理脚本

### 会话开始检查脚本
```bash
#!/bin/bash
# session-check.sh

echo "=== 会话开始检查 ==="

# 检查 CLAUDE.md 大小
if [ -f "CLAUDE.md" ]; then
    lines=$(wc -l < CLAUDE.md)
    echo "CLAUDE.md: $lines 行"
    if [ $lines -gt 50 ]; then
        echo "⚠️  CLAUDE.md 过长，建议压缩至 50 行以内"
    fi
else
    echo "ℹ️  未找到 CLAUDE.md"
fi

# 检查 .claudeignore
if [ -f ".claudeignore" ]; then
    echo "✅ .claudeignore 已配置"
else
    echo "⚠️  未找到 .claudeignore，建议创建"
fi

# 检查 MCP 配置
if [ -f ".mcp.json" ]; then
    servers=$(grep -c '"name"' .mcp.json 2>/dev/null || echo "0")
    echo "MCP 服务器: $servers 个"
fi

echo "=== 检查完成 ==="
```

### Token 监控脚本
```bash
#!/bin/bash
# token-monitor.sh

echo "=== Token 使用监控 ==="

# 这里可以集成 Claude API 调用来获取实际使用情况
# 示例：检查日志文件中的 token 使用

if [ -f "usage.log" ]; then
    echo "最近使用记录:"
    tail -10 usage.log
else
    echo "未找到使用日志"
fi

echo ""
echo "建议使用以下命令查看实时使用情况:"
echo "  /usage - 查看当前会话 token 用量"
echo "  /cost  - 查看预估费用"
```

## 5. 优化检查清单

### 设置层检查清单
- [ ] 创建 .claudeignore 文件
- [ ] 压缩 CLAUDE.md 至 500 token 以内
- [ ] 断开未使用的 MCP 服务器
- [ ] 禁用未使用的插件
- [ ] 考虑安装 context-mode

### 会话习惯检查清单
- [ ] 每个聊天只讨论一个主题
- [ ] 正确使用 /clear 和 /compact
- [ ] 针对特定文件而非整个仓库
- [ ] 用脚本获取数据而非让 Claude 读取
- [ ] 用 CLI 替代 MCP 进行精准读取
- [ ] 根据任务复杂度切换模型
- [ ] 限制 Extended Thinking（简单任务）
- [ ] 按需加载 Skills
- [ ] 使用子代理处理高上下文任务

### 监控检查清单
- [ ] 设置 token 使用基线
- [ ] 定期检查使用情况
- [ ] 分析优化效果
- [ ] 调整优化策略

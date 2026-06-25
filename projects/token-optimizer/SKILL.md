---
name: token-optimizer
description: |
  Token优化工具，自动压缩上下文、统计token使用、生成可视化报告。
  当用户提到"节省token"、"token优化"、"token太多"、"压缩上下文"、
  "token报告"时触发。使用headroom进行智能压缩，节省60-95% Token。
argument-hint: "[analyze|compress|report|config]"
context: fork
agent: general-purpose
allowed-tools: Read Write Bash
---

# Token Optimizer

自动优化AI Agent的Token使用，节省60-95%成本。

## 触发条件

### 精确匹配
- 节省token、token优化、token太多
- 压缩上下文、上下文压缩
- token报告、token统计
- 优化成本、降低成本

### 模糊匹配
- 对话太长，需要压缩
- Token消耗过大
- 想看token使用情况
- 优化AI使用成本

### 不触发条件
- 简单的token计数（不需要压缩）
- 与token无关的任务

## 核心原则

> **智能压缩，可视化报告，持续优化。**

## 依赖检查

首次使用前，检查并安装依赖：

```bash
pip install "headroom-ai[all]"
```

## 工作流程

### 第一步：接收输入

使用 $ARGUMENTS 获取参数：
- `analyze` - 分析当前token使用情况
- `compress` - 压缩当前上下文
- `report` - 生成token使用报告
- `config` - 查看/修改配置

### 第二步：执行操作

#### analyze 模式
1. 统计当前对话的token数量
2. 识别可以压缩的内容
3. 预估压缩后的节省量

#### compress 模式
1. 调用 headroom 压缩上下文
2. 记录压缩前后的token数量
3. 保存压缩历史

#### report 模式
1. 读取历史记录
2. 生成可视化报告
3. 计算总节省金额

#### config 模式
1. 显示当前配置
2. 允许修改参数

### 第三步：输出结果

根据操作类型，输出相应的结果和报告。

## 输出规范

### 压缩报告格式

```markdown
# Token 压缩报告

## 压缩统计
- 压缩前：{before} tokens
- 压缩后：{after} tokens
- 节省：{saved} tokens ({percentage}%)

## 压缩详情
- JSON压缩：{json_saved} tokens
- 代码压缩：{code_saved} tokens
- 文本压缩：{text_saved} tokens

## 成本节省
- 预估节省：${cost_saved}

## 时间戳
- 压缩时间：{timestamp}
```

### 统计报告格式

```markdown
# Token 使用统计报告

## 总体统计
- 总Token使用：{total_tokens}
- 总压缩节省：{total_saved}
- 节省比例：{percentage}%
- 预估节省成本：${total_cost_saved}

## 使用趋势
- 今日使用：{today_tokens}
- 本周使用：{week_tokens}
- 本月使用：{month_tokens}

## 压缩历史
| 时间 | 压缩前 | 压缩后 | 节省 |
|------|--------|--------|------|
| ... | ... | ... | ... |

## 优化建议
1. {suggestion_1}
2. {suggestion_2}
3. {suggestion_3}
```

## 参考资料

- headroom使用指南：${CLAUDE_SKILL_DIR}/references/headroom-guide.md
- 优化技巧：${CLAUDE_SKILL_DIR}/references/optimization-tips.md

## 输入规范

### 必需输入
- 无（使用默认配置）

### 可选输入
- `mode`：操作模式（analyze/compress/report/config）
- `threshold`：压缩阈值（token数量）
- `output`：报告输出格式

### 缺材料时
- 使用默认配置
- 自动检测当前上下文

## 注意事项

### 必须遵守
- 本地运行，数据不上传
- 保持可逆压缩，原始数据可恢复
- 定期清理过期的历史记录

### 禁止行为
- 不要删除原始数据
- 不要在压缩时丢失关键信息
- 不要自动上传任何数据

## 示例

### 示例1：分析token使用
```
用户：帮我分析一下当前的token使用情况
→ 执行 analyze 模式
→ 输出token统计和优化建议
```

### 示例2：压缩上下文
```
用户：对话太长了，帮我压缩一下
→ 执行 compress 模式
→ 输出压缩报告
```

### 示例3：生成报告
```
用户：我想看看这个月的token使用报告
→ 执行 report 模式
→ 输出详细的统计报告
```

### 反例：不该触发的情况
```
用户：帮我写一个token验证函数
→ 不触发（与token优化无关）
```

## 失败处理

| 失败类型 | 表现 | 修复动作 |
|----------|------|----------|
| 依赖缺失 | headroom未安装 | 自动安装依赖 |
| 压缩失败 | 压缩过程出错 | 回退到原始内容 |
| 报告生成失败 | 无法生成报告 | 显示原始统计 |
| 配置错误 | 配置文件损坏 | 重置为默认配置 |

## Gotchas

### G1: 压缩阈值设置
- 默认阈值：5000 tokens
- 过低会导致频繁压缩
- 过高会导致压缩不及时

### G2: 可逆压缩
- headroom支持可逆压缩（CCR）
- 原始数据存储在本地
- LLM可按需检索原始内容

### G3: 多算法选择
- SmartCrusher：JSON数据压缩
- CodeCompressor：代码压缩
- Kompress-base：通用文本压缩
- 自动根据内容类型选择最佳算法

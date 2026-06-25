# 工作产物管理规范

## 概述

所有调研分析、全文搜集、方案推送等工作流都必须生成 md 文件，以便：
- **引用** — 后续流程可直接引用前序产物
- **参考** — 用户和 Agent 可直观查看调研结果
- **优化** — 基于产物进行迭代优化
- **追溯** — 确保执行过程可追溯、可复现

## 产物类型

| 产物类型 | 生成时机 | 文件命名 | 存放位置 |
|----------|----------|----------|----------|
| 搜索结果报告 | 搜索 Skill 完成后 | `search-results-{date}-{keyword}.md` | `./artifacts/search/` |
| 深度分析报告 | 深度分析原 Skill 完成后 | `deep-analysis-{date}-{skill-names}.md` | `./artifacts/analysis/` |
| 调研报告 | 全网调研完成后 | `research-report-{date}-{topic}.md` | `./artifacts/research/` |
| 方案文档 | 方案推送完成后 | `proposal-{date}-{feature}.md` | `./artifacts/proposals/` |
| 合并方案 | 合并方案设计完成后 | `merge-proposal-{date}-{skill-names}.md` | `./artifacts/merge/` |
| 审查报告 | 审查评分完成后 | `review-report-{date}-{skill-name}.md` | `./artifacts/reviews/` |
| 安全审查报告 | 安全审查完成后 | `security-review-{date}-{skill-name}.md` | `./artifacts/reviews/` |
| 优化报告 | 优化完成后 | `optimize-report-{date}-{skill-name}.md` | `./artifacts/optimize/` |
| 安装报告 | 安装完成后 | `install-report-{date}-{skill-name}.md` | `./artifacts/install/` |
| 部署报告 | 部署完成后 | `deploy-report-{date}-{skill-name}.md` | `./artifacts/deploy/` |
| 环境检查报告 | 环境检查完成后 | `env-check-{date}.md` | `./artifacts/env/` |
| 管理操作报告 | 管理操作完成后 | `manage-report-{date}-{operation}.md` | `./artifacts/manage/` |

## 产物目录结构

```
./artifacts/
├── search/              # 搜索结果报告
│   └── search-results-2026-06-13-code-format.md
├── analysis/            # 深度分析报告
│   └── deep-analysis-2026-06-13-skill-a-skill-b.md
├── research/            # 调研报告
│   └── research-report-2026-06-13-code-review-best-practices.md
├── proposals/           # 方案文档
│   └── proposal-2026-06-13-code-formatter-skill.md
├── merge/               # 合并方案
│   └── merge-proposal-2026-06-13-skill-a-skill-b.md
├── reviews/             # 审查报告（含安全审查）
│   ├── review-report-2026-06-13-code-review.md
│   └── security-review-2026-06-13-code-review.md
├── optimize/            # 优化报告
│   └── optimize-report-2026-06-13-code-review.md
├── install/             # 安装报告
│   └── install-report-2026-06-13-code-formatter.md
├── deploy/              # 部署报告
│   └── deploy-report-2026-06-13-code-formatter.md
├── manage/              # 管理操作报告
│   └── manage-report-2026-06-13-uninstall.md
└── env/                 # 环境检查报告
    └── env-check-2026-06-13.md
```

## 产物生成规则

### 规则 1：必须生成

以下流程**必须**生成 md 文件：
- 环境检查（流程零）→ 环境检查报告
- 搜索 Skill（流程一）→ 搜索结果报告
- 安装 Skill（流程二）→ 安装报告
- 安全审查（流程三）→ 安全审查报告
- 优化 Skill（流程四）→ 优化报告
- 部署 Skill（流程五）→ 部署报告
- 管理 Skill（流程六）→ 管理操作报告
- 全网深度搜索（dev 子技能第一阶段）→ 调研报告
- 方案推送（dev 子技能第二阶段）→ 方案文档
- 深度分析原 Skill（流程七第一步）→ 深度分析报告
- 网上调研（流程七第五步 / dev 子技能合并流程第五步）→ 调研报告
- 合并方案设计（流程七第六步 / dev 子技能合并流程第六步）→ 合并方案
- 审查评分（review 子技能）→ 审查报告

### 规则 2：自动创建目录

生成产物前，自动创建目录（如果不存在）：
```bash
mkdir -p ./artifacts/search/
mkdir -p ./artifacts/analysis/
mkdir -p ./artifacts/research/
mkdir -p ./artifacts/proposals/
mkdir -p ./artifacts/merge/
mkdir -p ./artifacts/reviews/
mkdir -p ./artifacts/optimize/
mkdir -p ./artifacts/install/
mkdir -p ./artifacts/deploy/
mkdir -p ./artifacts/manage/
mkdir -p ./artifacts/env/
```

### 规则 3：命名规范

文件名格式：`{类型}-{date}-{关键词}.md`
- `{类型}` — 产物类型（search-results, deep-analysis, research-report, proposal, merge-proposal, review-report, optimize-report, env-check）
- `{date}` — 日期，格式 YYYY-MM-DD
- `{关键词}` — 简短描述，用连字符分隔

示例：
- `search-results-2026-06-13-code-format.md`
- `deep-analysis-2026-06-13-skill-workspace-skill-dev.md`
- `research-report-2026-06-13-code-review-best-practices.md`

### 规则 4：产物引用

后续流程引用前序产物时，使用相对路径：
```markdown
**参考资料：**
- 搜索结果：`./artifacts/search/search-results-2026-06-13-code-format.md`
- 调研报告：`./artifacts/research/research-report-2026-06-13-code-review-best-practices.md`
```

### 规则 5：产物更新

如果同一主题的产物已存在，询问用户：
- 覆盖旧产物
- 保留旧产物，生成新版本（文件名加版本号）
- 合并新旧产物

## 产物模板

### 搜索结果报告模板

```markdown
# 搜索结果报告

**搜索时间：** {date}
**搜索关键词：** {keyword}
**搜索源：** {sources}

## 搜索结果

### 结果 1: {name}
- **来源：** {source}
- **Stars：** {stars}
- **描述：** {description}
- **链接：** {url}

### 结果 2: {name}
...

## 搜索统计

| 来源 | 结果数 | 耗时 |
|------|--------|------|
| SkillsMP | {count} | {time} |
| Skills.sh | {count} | {time} |
| GitHub | {count} | {time} |

## 推荐

基于搜索结果，推荐以下方案：
1. {recommendation 1}
2. {recommendation 2}

## 下一步

- [ ] 用户选择方案
- [ ] 安全审查
- [ ] 安装/开发
```

### 深度分析报告模板

```markdown
# 深度分析报告

**分析时间：** {date}
**分析对象：** {skill names}

## 一、功能清单

### {skill A}

#### 核心功能
1. {function 1}
2. {function 2}

#### 辅助功能
1. {function 1}
2. {function 2}

#### 边界功能
1. {scenario 1} — 不应该触发
2. {scenario 2} — 不应该触发

#### 缺失功能
1. {function 1} — 可能需要
2. {function 2} — 可能需要

### {skill B}
...

## 二、架构设计

| 维度 | {skill A} | {skill B} |
|------|-----------|-----------|
| 触发条件 | {conditions} | {conditions} |
| 工作流程 | {workflow} | {workflow} |
| 输出规范 | {output} | {output} |
| 子技能 | {subskills} | {subskills} |

## 三、提示词质量

| 维度 | {skill A} | {skill B} |
|------|-----------|-----------|
| 触发词精准度 | {score} | {score} |
| 指令明确性 | {score} | {score} |
| 输出格式规范 | {score} | {score} |
| 边界条件说明 | {score} | {score} |
| 示例完整性 | {score} | {score} |

## 四、子技能调用工程

| 维度 | {skill A} | {skill B} |
|------|-----------|-----------|
| 调用方式 | {method} | {method} |
| 参数传递 | {params} | {params} |
| 结果整合 | {integration} | {integration} |
| 错误处理 | {error handling} | {error handling} |
| 降级策略 | {fallback} | {fallback} |

## 五、优化空间

| 维度 | {skill A} | {skill B} |
|------|-----------|-----------|
| 性能优化 | {suggestion} | {suggestion} |
| 准确性优化 | {suggestion} | {suggestion} |
| 易用性优化 | {suggestion} | {suggestion} |
| 可维护性优化 | {suggestion} | {suggestion} |
| 可扩展性优化 | {suggestion} | {suggestion} |

## 六、总结

### 优点汇总
- {skill A}: {advantages}
- {skill B}: {advantages}

### 缺点汇总
- {skill A}: {disadvantages}
- {skill B}: {disadvantages}

### 优化建议
1. {suggestion 1}
2. {suggestion 2}
```

### 调研报告模板

```markdown
# 调研报告

**调研时间：** {date}
**调研主题：** {topic}
**调研来源：** {sources}

## 一、调研背景

{background description}

## 二、调研结果

### 2.1 解决方案

#### 方案 1: {name}
- **来源：** {source}
- **描述：** {description}
- **优点：** {advantages}
- **缺点：** {disadvantages}
- **推荐度：** {rating}

#### 方案 2: {name}
...

### 2.2 最佳实践

1. **{practice 1}**
   - 来源：{source}
   - 说明：{description}
   - 适用场景：{scenario}

2. **{practice 2}**
   ...

### 2.3 踩坑经验

1. **{pitfall 1}**
   - 来源：{source}
   - 问题：{problem}
   - 解决方案：{solution}
   - 预防措施：{prevention}

2. **{pitfall 2}**
   ...

### 2.4 竞品分析

| 竞品 | 优点 | 缺点 | 差异化 |
|------|------|------|--------|
| {competitor 1} | {advantages} | {disadvantages} | {differentiation} |
| {competitor 2} | {advantages} | {disadvantages} | {differentiation} |

### 2.5 用户反馈

1. **{feedback 1}**
   - 来源：{source}
   - 内容：{content}
   - 建议：{suggestion}

2. **{feedback 2}**
   ...

## 三、总结

### 关键发现
1. {finding 1}
2. {finding 2}

### 推荐方案
{recommendation}

### 下一步行动
1. {action 1}
2. {action 2}
```

### 方案文档模板

```markdown
# 方案文档

**创建时间：** {date}
**功能名称：** {feature}
**方案类型：** {推荐方案 / 备选方案}

## 一、方案概述

{overview description}

## 二、技术方案

### 2.1 技术栈
- {tech 1}
- {tech 2}

### 2.2 架构设计
{architecture description}

### 2.3 核心逻辑
{core logic description}

## 三、实现步骤

### 步骤 1: {step name}
{step description}

### 步骤 2: {step name}
{step description}

## 四、对比分析

| 维度 | 本方案 | 备选方案 1 | 备选方案 2 |
|------|--------|------------|------------|
| 技术栈 | {tech} | {tech} | {tech} |
| 优点 | {advantages} | {advantages} | {advantages} |
| 缺点 | {disadvantages} | {disadvantages} | {disadvantages} |
| 预估时间 | {time} | {time} | {time} |
| 难度 | {difficulty} | {difficulty} | {difficulty} |
| 推荐度 | {rating} | {rating} | {rating} |

## 五、风险评估

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| {risk 1} | {probability} | {impact} | {mitigation} |
| {risk 2} | {probability} | {impact} | {mitigation} |

## 六、确认清单

- [ ] 方案可行
- [ ] 技术栈合适
- [ ] 风险可控
- [ ] 可以开始开发
```

## 产物使用流程

```
第一步：执行工作流（搜索/分析/调研/方案）
  ↓
第二步：生成产物 md 文件
  ↓
第三步：展示产物摘要给用户
  ↓
第四步：用户确认产物内容
  ↓
第五步：保存产物到 artifacts/ 目录
  ↓
第六步：后续流程引用产物
```

## 产物引用示例

### 在合并流程中引用搜索结果

```markdown
## 调研结果

**参考资料：**
- 搜索结果：`./artifacts/search/search-results-2026-06-13-code-format.md`
- 深度分析：`./artifacts/analysis/deep-analysis-2026-06-13-skill-a-skill-b.md`

基于搜索结果和深度分析，我们发现：
1. {finding 1}
2. {finding 2}
```

### 在开发流程中引用调研报告

```markdown
## 方案推送

**参考资料：**
- 调研报告：`./artifacts/research/research-report-2026-06-13-code-review-best-practices.md`

基于调研结果，推荐以下方案：
1. {recommendation 1}
2. {recommendation 2}
```

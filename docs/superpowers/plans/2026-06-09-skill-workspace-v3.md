# Skill Workspace v3.0 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 skill-workspace 升级到 v3.0，实现全新的开发流程（需求深挖 → 全网搜索 → 方案推送 → 分阶段开发 → 完整交付），复用现有所有功能。

**Architecture:** 采用方案 A+B 融合设计，架构层用全新流程，实现层复用现有功能。每个阶段都是独立模块，可单独使用。

**Tech Stack:** Claude Code Skill 规范、Markdown、JSON

---

## 文件结构

```
skill-workspace/
├── SKILL.md                    # 主入口（重写）
├── references/
│   ├── optimize.md             # 优化方法论（保留）
│   ├── deploy.md               # 部署指南（保留）
│   ├── requirements.md         # 需求深挖指南（新增）
│   ├── search-strategy.md      # 搜索策略指南（新增）
│   └── proposal-template.md    # 方案推送模板（新增）
├── evals/
│   └── evals.json              # 主技能评测集（更新）
└── subskills/
    ├── dev/                    # 开发子技能（重写）
    │   ├── SKILL.md            # 开发流程
    │   ├── references/
    │   │   ├── official-spec.md
    │   │   ├── template.md
    │   │   ├── example.md
    │   │   └── methodology.md
    │   └── evals/
    │       └── evals.json
    └── review/                 # 审查子技能（保留）
        ├── SKILL.md
        ├── references/
        │   ├── official-spec.md
        │   ├── scoring-criteria.md
        │   └── security.md
        └── evals/
            ├── evals.json
            └── test-cases.json
```

---

## Task 1: 创建需求深挖指南

**Files:**
- Create: `skill-workspace/references/requirements.md`

- [ ] **Step 1: 创建需求深挖指南文件**

```markdown
# 需求深挖指南

## 概述

需求深挖是 Skill 开发的第一步，目标是深入理解用户的真实痛点和需求，而不是只问几个表面问题。

## 痛点挖掘（5-8 个问题）

### 问题清单

1. **这个任务你重复做过几次？**
   - 选项：1次 / 2-5次 / 6-10次 / 10次以上
   - 目的：判断是否值得 Skill 化（至少 3 次才值得）

2. **每次做的时候最痛苦的是什么？**
   - 开放式问题
   - 目的：找到核心痛点

3. **你理想中的解决方案是什么样的？**
   - 开放式问题
   - 目的：理解用户期望

4. **有没有类似的工具？哪里不满意？**
   - 开放式问题
   - 目的：了解竞品，找到差异化

5. **你的使用场景是什么？**
   - 选项：个人 / 团队 / 企业
   - 目的：确定功能范围

6. **有没有特殊要求？**
   - 开放式问题
   - 目的：识别约束条件

7. **你希望达到什么效果？**
   - 开放式问题
   - 目的：明确成功标准

8. **有没有时间/预算限制？**
   - 开放式问题
   - 目的：评估可行性

### 提问策略

- **一次只问一个问题** - 不要一次问多个问题，让用户专注于一个问题
- **优先使用多选题** - 比开放式问题更容易回答
- **根据回答调整后续问题** - 如果用户已经回答了某个问题，跳过
- **追问细节** - 如果回答模糊，追问具体细节

## 用户场景分析

### 分析维度

1. **使用频率**
   - 每天：需要高效、稳定
   - 每周：需要易用、可定制
   - 每月：需要简单、快速
   - 偶尔：需要直观、有引导

2. **skill 水平**
   - 新手：需要详细引导、示例
   - 中级：需要灵活配置、高级功能
   - 高级：需要最大控制、可扩展

3. **偏好**
   - 简单：最少功能，快速上手
   - 功能全：完整功能，满足所有需求
   - 创新：新技术栈，前沿方案

4. **场景**
   - 个人：个人偏好，快速迭代
   - 团队：团队规范，协作友好
   - 企业：企业标准，安全合规

### 输出：用户画像

```markdown
# 用户画像

## 基本信息
- 使用频率：[频率]
- skill 水平：[水平]
- 偏好：[偏好]
- 场景：[场景]

## 需求分析
- 核心痛点：[痛点]
- 期望效果：[效果]
- 约束条件：[约束]

## 推荐方案
- 方案类型：[轻量级/功能全/创新]
- 技术栈：[技术栈]
- 预估时间：[时间]
```

## 需求确认

### 确认内容

1. **功能需求清单**
   - 列出所有功能需求
   - 标注优先级（必须/应该/可以）
   - 标注复杂度（简单/中等/复杂）

2. **非功能需求**
   - 性能：响应时间、并发量
   - 安全：数据安全、权限控制
   - 易用性：学习成本、操作步骤

3. **约束条件**
   - 时间：截止日期
   - 预算：资源限制
   - 技术栈：技术限制

### 打分标准

| 维度 | 满分 | 检查项 |
|------|------|--------|
| 需求完整性 | 30 | 功能需求是否完整、非功能需求是否明确 |
| 需求清晰度 | 30 | 需求描述是否清晰、无歧义 |
| 需求可行性 | 20 | 需求是否可行、是否在技术范围内 |
| 需求一致性 | 20 | 需求之间是否一致、无矛盾 |
| **总分** | **100** | |

**通过标准：** ≥ 80 分

### 输出格式

```markdown
# 需求文档

## 功能需求

### 必须功能
1. [功能 1]
2. [功能 2]

### 应该功能
1. [功能 3]
2. [功能 4]

### 可以功能
1. [功能 5]
2. [功能 6]

## 非功能需求

### 性能
- [性能要求]

### 安全
- [安全要求]

### 易用性
- [易用性要求]

## 约束条件

### 时间
- [时间约束]

### 预算
- [预算约束]

### 技术栈
- [技术栈约束]

## 审查结果

| 维度 | 得分 | 满分 | 评级 |
|------|------|------|------|
| 需求完整性 | [分] | 30 | [评级] |
| 需求清晰度 | [分] | 30 | [评级] |
| 需求可行性 | [分] | 20 | [评级] |
| 需求一致性 | [分] | 20 | [评级] |
| **总分** | **[分]** | **100** | **[评级]** |

**审查结论：** [通过/不通过]
```
```

- [ ] **Step 2: 验证文件创建**

```bash
cat skill-workspace/references/requirements.md | head -50
```

Expected: 看到完整的需求深挖指南内容

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/requirements.md
git commit -m "feat: add requirements deep-dive guide"
```

---

## Task 2: 创建搜索策略指南

**Files:**
- Create: `skill-workspace/references/search-strategy.md`

- [ ] **Step 1: 创建搜索策略指南文件**

```markdown
# 搜索策略指南

## 概述

全网搜索是 Skill 开发的第二步，目标是全方位搜索，不遗漏任何有价值的信息源。

## 5 层搜索源

### Tier 1: SkillsMP (skillsmp.com)

**说明：** 1.5M+ skills，兼容所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

**搜索命令：**
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q={关键词}&limit=10&sortBy=stars"
```

**参数：**
- `q`: 搜索关键词
- `limit`: 返回数量（默认 10）
- `sortBy`: 排序方式（stars/downloads/updated）
- `category`: 分类过滤
- `occupation`: 职业过滤
- `page`: 分页

**返回字段：**
- `name`: skill 名称
- `description`: 描述
- `stars`: 星数
- `downloads`: 下载量
- `github_url`: GitHub 链接
- `author`: 作者
- `version`: 版本

### Tier 2: Skills.sh 生态

**说明：** Agent Skills 的包管理器

**搜索命令：**
```bash
npx skills find {关键词}
```

**其他命令：**
```bash
# 安装 skill
bash /path/to/skill/scripts/install-skill.sh <owner/repo@skill-name>

# 检查更新
npx skills check

# 批量更新
npx skills update
```

### Tier 3: CocoLoop API

**说明：** Skill 聚合市场

**搜索命令：**
```bash
curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"
```

**参数：**
- `keyword`: 搜索关键词
- `page`: 页码
- `page_size`: 每页数量
- `sort`: 排序方式（downloads/stars/updated）

### Tier 4: GitHub 搜索

**说明：** 搜索包含 SKILL.md 的仓库

**搜索命令：**
```bash
curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"
```

**参数：**
- `q`: 搜索关键词 + filename:SKILL.md
- `sort`: 排序方式（stars/forks/updated）
- `per_page`: 每页数量

### Tier 5: 技术博客/社区

**说明：** 搜索最佳实践、踩坑经验

**搜索关键词组合：**
- "{关键词} skill 最佳实践"
- "{关键词} agent skill 开发"
- "{关键词} claude code skill"
- "{关键词} SKILL.md 示例"

**搜索来源：**
- GitHub Issues/Discussions
- Stack Overflow
- 知乎
- 掘金
- CSDN

## 搜索策略

### 并行搜索

同时搜索 5 个源，提高效率：

```
┌─────────────────────────────────────────────────────────────┐
│                    并行搜索流程                              │
├─────────────────────────────────────────────────────────────┤
│  1. 启动 5 个搜索任务                                        │
│     ├── Task 1: SkillsMP 搜索                                │
│     ├── Task 2: Skills.sh 搜索                               │
│     ├── Task 3: CocoLoop 搜索                                │
│     ├── Task 4: GitHub 搜索                                  │
│     └── Task 5: 技术博客/社区搜索                            │
│                                                             │
│  2. 等待所有任务完成                                         │
│                                                             │
│  3. 合并结果                                                 │
│     ├── 去重                                                 │
│     ├── 排序                                                 │
│     └── 分析                                                 │
└─────────────────────────────────────────────────────────────┘
```

### 智能排序

按相关度、下载量、评分综合排序：

**排序算法：**
```
score = (relevance * 0.4) + (downloads * 0.3) + (stars * 0.3)
```

- `relevance`: 相关度（0-100）
- `downloads`: 下载量（归一化到 0-100）
- `stars`: 星数（归一化到 0-100）

### 深度分析

分析每个结果的优缺点：

**分析维度：**
- 功能完整度
- 技术栈
- 代码质量
- 社区活跃度
- 文档质量

## 结果对比分析

### 对比维度

1. **功能完整度**
   - 实现了哪些功能
   - 缺少哪些功能
   - 功能是否符合需求

2. **技术栈**
   - 使用了哪些技术
   - 技术是否先进
   - 技术是否稳定

3. **代码质量**
   - 代码是否规范
   - 是否有测试
   - 是否有文档

4. **社区活跃度**
   - 最近更新时间
   - Issue 数量
   - PR 数量

5. **文档质量**
   - 是否有 README
   - 是否有示例
   - 是否有 API 文档

### 输出格式

```markdown
📋 搜索结果汇总（来源：5 个源）

## 搜索统计

- SkillsMP: [数量] 个结果
- Skills.sh: [数量] 个结果
- CocoLoop: [数量] 个结果
- GitHub: [数量] 个结果
- 技术博客: [数量] 个结果

## 结果列表

### 1. skill-name (⭐ 15.5k stars, 📥 50k+ downloads)

**来源：** SkillsMP
**描述：** [描述文本]
**GitHub：** https://github.com/xxx/xxx
**作者：** [作者]
**版本：** [版本]
**最近更新：** [日期]

**优点：**
- [优点 1]
- [优点 2]
- [优点 3]

**缺点：**
- [缺点 1]
- [缺点 2]
- [缺点 3]

**推荐度：** ⭐⭐⭐⭐⭐

### 2. ...

## 技术方案对比

| 方案 | 技术栈 | 功能完整度 | 代码质量 | 社区活跃度 | 推荐度 |
|------|--------|------------|----------|------------|--------|
| 方案 1 | [技术栈] | [评分] | [评分] | [评分] | ⭐⭐⭐⭐⭐ |
| 方案 2 | [技术栈] | [评分] | [评分] | [评分] | ⭐⭐⭐⭐ |
| 方案 3 | [技术栈] | [评分] | [评分] | [评分] | ⭐⭐⭐ |
```

## 下载参考实现

### 下载策略

1. **用户选择要下载的参考实现**
   - 展示搜索结果列表
   - 让用户选择要下载的实现

2. **下载到本地工作区**
   ```bash
   # 克隆仓库
   git clone https://github.com/xxx/xxx.git

   # 或下载 SKILL.md
   curl -o SKILL.md https://raw.githubusercontent.com/xxx/xxx/main/SKILL.md
   ```

3. **安全审查**
   - 调用安全审查流程（4 步协议）
   - 评级 ≥ B → 继续
   - 评级 ≤ C → 询问用户是否继续

### 安全审查协议

**第 1 步：元数据检查**
- [ ] name 匹配预期名称（无拼写欺骗）
- [ ] description 清晰且与实际行为一致
- [ ] version 遵循 semver（可选但建议）

**第 2 步：权限范围分析**

| 权限 | 风险 | 说明 |
|------|------|------|
| Read | 🟢 Low | 几乎总是合理 |
| Write | 🟡 Medium | 必须说明写入哪些文件 |
| Bash | 🔴 Critical | 必须说明执行哪些命令 |
| network | 🔴 Critical | 必须说明访问哪些端点 |

**危险组合：** `network` + `shell` 同时出现 → 数据泄露风险，必须 BLOCK。

**第 3 步：内容安全扫描**

🔴 **Critical（直接 BLOCK）：**
- 引用 `~/.ssh`、`~/.aws`、`~/.env` 等敏感路径
- 使用 `curl`、`wget`、`nc`、`bash -i` 等网络/反弹命令
- `base64` 混淆内容
- 禁用安全机制的指令
- 未知或可疑 URL

🟡 **Warning（需要人工审查）：**
- `/**/*` 等宽泛通配符
- `sudo` 使用
- 潜在的提示注入

ℹ️ **Info（建议改进）：**
- 缺少 description/version

**第 4 步：Typosquat 检测**

检查以下情况：
- 单字符替换（如 `skil1-review`）
- 同形字符（l/1, O/0, a/а）
- 多余连字符（`skill--review`）
- 与已安装 skill 重名或近似

**输出格式：**

```
安全审查报告
============
Skill: {name}
安全评级: SAFE / WARNING / DANGER / BLOCK
风险标记: {数量}
建议: install / sandbox first / do not install

详细发现:
- 元数据: ✅ 正常 / ⚠️ 问题描述
- 权限: ✅ 最小权限 / ⚠️ 过度权限
- 内容: ✅ 无风险 / ⚠️ 风险项列表
- Typosquat: ✅ 无 / ⚠️ 可疑命名
```
```

- [ ] **Step 2: 验证文件创建**

```bash
cat skill-workspace/references/search-strategy.md | head -50
```

Expected: 看到完整的搜索策略指南内容

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/search-strategy.md
git commit -m "feat: add search strategy guide"
```

---

## Task 3: 创建方案推送模板

**Files:**
- Create: `skill-workspace/references/proposal-template.md`

- [ ] **Step 1: 创建方案推送模板文件**

```markdown
# 方案推送模板

## 概述

方案推送是 Skill 开发的第三步，目标是主推一个方案，附带 2-3 个备选，让用户选择。

## 推荐方案生成

### 生成要求

1. **基于搜索结果和用户需求**
   - 分析搜索结果
   - 结合用户需求
   - 选择最佳匹配的方案

2. **详细说明实现思路**
   - 列出实现步骤
   - 说明每个步骤的具体内容
   - 预估每个步骤的时间

3. **预估开发时间和难度**
   - 总时间估算
   - 难度评估（1-5 星）
   - 风险评估

### 输出格式

```markdown
## 🎯 推荐方案：[方案名称]

**推荐理由：** [一句话说明为什么推荐]

**实现思路：**
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**技术栈：** [技术栈列表]
**预估时间：** [时间]
**难度：** ⭐⭐⭐⭐⭐
**风险：** [低/中/高]
```

## 备选方案生成

### 备选方案类型

1. **备选方案 1：轻量级**
   - 适用场景：快速验证想法
   - 特点：实现快，简单
   - 缺点：功能有限
   - 预估时间：较短

2. **备选方案 2：功能最全**
   - 适用场景：需要完整功能
   - 特点：功能全面
   - 缺点：开发时间长
   - 预估时间：较长

3. **备选方案 3：创新方案**
   - 适用场景：想尝试新技术
   - 特点：技术先进
   - 缺点：风险较高
   - 预估时间：不确定

### 输出格式

```markdown
## 🔄 备选方案

### 备选方案 1：轻量级
**适用场景：** 快速验证想法
**优点：** 实现快，简单
**缺点：** 功能有限
**预估时间：** [时间]

### 备选方案 2：功能最全
**适用场景：** 需要完整功能
**优点：** 功能全面
**缺点：** 开发时间长
**预估时间：** [时间]

### 备选方案 3：创新方案
**适用场景：** 想尝试新技术
**优点：** 技术先进
**缺点：** 风险较高
**预估时间：** [时间]
```

## 方案对比

### 对比维度

1. **技术栈**
   - 使用了哪些技术
   - 技术是否先进
   - 技术是否稳定

2. **优点**
   - 实现了哪些功能
   - 有哪些优势

3. **缺点**
   - 缺少哪些功能
   - 有哪些劣势

4. **预估时间**
   - 开发时间估算
   - 测试时间估算
   - 部署时间估算

5. **难度**
   - 技术难度（1-5 星）
   - 实现难度（1-5 星）
   - 测试难度（1-5 星）

6. **推荐度**
   - 综合评分（1-5 星）
   - 推荐理由

### 输出格式

```markdown
## 📊 方案对比

| 方案 | 技术栈 | 优点 | 缺点 | 预估时间 | 难度 | 推荐度 |
|------|--------|------|------|----------|------|--------|
| 推荐方案 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 备选 1 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 备选 2 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 备选 3 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
```

## 用户选择

### 选择方式

```markdown
## 🤔 请选择

请选择一个方案，或者告诉我你的想法：
1. 使用推荐方案
2. 使用备选方案 1
3. 使用备选方案 2
4. 使用备选方案 3
5. 自定义方案（告诉我你的想法）
```

### 选择后处理

1. **用户选择推荐方案**
   - 确认方案细节
   - 开始开发

2. **用户选择备选方案**
   - 确认方案细节
   - 开始开发

3. **用户选择自定义方案**
   - 了解用户想法
   - 调整方案
   - 确认后开始开发

## 完整输出模板

```markdown
# 📋 Skill 开发方案推荐

## 🎯 推荐方案：[方案名称]

**推荐理由：** [一句话说明为什么推荐]

**实现思路：**
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**技术栈：** [技术栈列表]
**预估时间：** [时间]
**难度：** ⭐⭐⭐⭐⭐
**风险：** [低/中/高]

---

## 🔄 备选方案

### 备选方案 1：轻量级
**适用场景：** 快速验证想法
**优点：** 实现快，简单
**缺点：** 功能有限
**预估时间：** [时间]

### 备选方案 2：功能最全
**适用场景：** 需要完整功能
**优点：** 功能全面
**缺点：** 开发时间长
**预估时间：** [时间]

### 备选方案 3：创新方案
**适用场景：** 想尝试新技术
**优点：** 技术先进
**缺点：** 风险较高
**预估时间：** [时间]

---

## 📊 方案对比

| 方案 | 技术栈 | 优点 | 缺点 | 预估时间 | 难度 | 推荐度 |
|------|--------|------|------|----------|------|--------|
| 推荐方案 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 备选 1 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 备选 2 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 备选 3 | [技术栈] | [优点] | [缺点] | [时间] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🤔 请选择

请选择一个方案，或者告诉我你的想法：
1. 使用推荐方案
2. 使用备选方案 1
3. 使用备选方案 2
4. 使用备选方案 3
5. 自定义方案（告诉我你的想法）
```
```

- [ ] **Step 2: 验证文件创建**

```bash
cat skill-workspace/references/proposal-template.md | head -50
```

Expected: 看到完整的方案推送模板内容

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/proposal-template.md
git commit -m "feat: add proposal template"
```

---

## Task 4: 重写开发子技能 SKILL.md

**Files:**
- Modify: `skill-workspace/subskills/dev/SKILL.md`

- [ ] **Step 1: 读取现有开发子技能 SKILL.md**

```bash
cat skill-workspace/subskills/dev/SKILL.md
```

- [ ] **Step 2: 重写开发子技能 SKILL.md**

基于设计文档，重写开发子技能，集成新流程：

```markdown
---
name: skill-dev
description: |
  Skill 开发助手。当用户提到"开发skill"、"创建skill"、"新建skill"、
  "写个skill"、"帮我做个skill"时触发。引导用户完成符合官方规范的
  Skill 开发，自动生成 SKILL.md 文件。由 skill-workspace 主入口路由调用。
argument-hint: "[skill功能描述]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob Bash WebFetch
---

# Skill 开发助手（v3.0）

你是一个 Skill 开发专家，精通 Agent Skill 规范（适用于 Claude Code、Codex CLI、ChatGPT 等所有支持 SKILL.md 的 Agent）。你的目标是帮助用户开发高质量的 Skill。

## 核心原则

> **深入理解需求，全网搜索最佳方案，分阶段开发，循环审查，完整交付。**

## 完整流程

```
┌─────────────────────────────────────────────────────────────┐
│           Skill 开发完整流程（v3.0）                         │
├─────────────────────────────────────────────────────────────┤
│  第一阶段：需求深挖                                          │
│  ├── 痛点挖掘（5-8 个问题）                                  │
│  ├── 用户场景分析                                            │
│  ├── 需求确认（打分 ≥ 80 分才通过）                          │
│  └── 集成：可选搜索类似 skill                                │
├─────────────────────────────────────────────────────────────┤
│  第二阶段：全网搜索                                          │
│  ├── 5 层搜索源并行搜索                                      │
│  ├── 结果对比分析                                            │
│  ├── 技术方案汇总                                            │
│  ├── 下载参考实现                                            │
│  └── 安全审查                                                │
├─────────────────────────────────────────────────────────────┤
│  第三阶段：方案推送                                          │
│  ├── 主推方案（最佳匹配）                                    │
│  ├── 备选方案 1（轻量级）                                    │
│  ├── 备选方案 2（功能最全）                                  │
│  ├── 备选方案 3（创新方案）                                  │
│  └── 用户选择后继续                                          │
├─────────────────────────────────────────────────────────────┤
│  第四阶段：分阶段开发 + 循环审查                             │
│  ├── 4.1 需求确认 → 审查打分 → 循环返工                      │
│  ├── 4.2 方案确认 → 审查打分 → 循环返工                      │
│  ├── 4.3 代码实现 → 审查打分 → 循环返工                      │
│  └── 4.4 测试验证 → 审查打分 → 循环返工                      │
├─────────────────────────────────────────────────────────────┤
│  第五阶段：完整交付                                          │
│  ├── 最终审查（10 维度综合评分）                             │
│  ├── 生成完整 SKILL.md                                       │
│  ├── 生成评测集                                              │
│  ├── 安全审查                                                │
│  ├── 部署指南                                                │
│  ├── 优化建议                                                │
│  └── 版本管理                                                │
└─────────────────────────────────────────────────────────────┘
```

## 第一阶段：需求深挖

**目标：** 深入理解用户的真实痛点和需求

**参考资料：** `${CLAUDE_SKILL_DIR}/../references/requirements.md`

### 痛点挖掘（5-8 个问题）

**问题清单：**

1. 这个任务你重复做过几次？
2. 每次做的时候最痛苦的是什么？
3. 你理想中的解决方案是什么样的？
4. 有没有类似的工具？哪里不满意？
5. 你的使用场景是什么？
6. 有没有特殊要求？
7. 你希望达到什么效果？
8. 有没有时间/预算限制？

**提问策略：**
- 一次只问一个问题
- 优先使用多选题
- 根据回答调整后续问题

### 用户场景分析

**分析维度：**
- 使用频率（每天/每周/每月/偶尔）
- skill 水平（新手/中级/高级）
- 偏好（简单/功能全/创新）
- 场景（个人/团队/企业）

**输出：** 用户画像文档

### 需求确认

**确认内容：**
- 功能需求清单
- 非功能需求（性能、安全、易用性）
- 约束条件（时间、预算、技术栈）

**打分标准：**
- 需求完整性：30 分
- 需求清晰度：30 分
- 需求可行性：20 分
- 需求一致性：20 分
- **总分 100 分，≥ 80 分通过**

## 第二阶段：全网搜索

**目标：** 全方位搜索，不遗漏任何有价值的信息源

**参考资料：** `${CLAUDE_SKILL_DIR}/../references/search-strategy.md`

### 5 层搜索源并行搜索

**搜索源：**

| 优先级 | 来源 | 说明 |
|--------|------|------|
| Tier 1 | SkillsMP (skillsmp.com) | 1.5M+ skills，兼容所有 Agent |
| Tier 2 | Skills.sh 生态 | npx skills find |
| Tier 3 | CocoLoop API | Skill 聚合市场 |
| Tier 4 | GitHub 搜索 | 搜索包含 SKILL.md 的仓库 |
| Tier 5 | 技术博客/社区 | 最佳实践、踩坑经验 |

**搜索策略：**
- 并行搜索，提高效率
- 智能排序（相关度、下载量、评分综合排序）
- 深度分析（优缺点、可复用部分）

### 结果对比分析

**对比维度：**
- 功能完整度
- 技术栈
- 代码质量
- 社区活跃度
- 文档质量

### 下载参考实现

**下载策略：**
- 用户选择要下载的参考实现
- 下载到本地工作区
- 安全审查（4 步协议）

### 安全审查

**审查协议（4 步）：**
1. 元数据检查
2. 权限范围分析
3. 内容扫描
4. Typosquat 检测

**输出：**
```
安全评级：SAFE / WARNING / DANGER / BLOCK
风险标记：{数量}
建议：install / sandbox first / do not install
```

## 第三阶段：方案推送

**目标：** 主推一个方案，附带 2-3 个备选，让用户选择

**参考资料：** `${CLAUDE_SKILL_DIR}/../references/proposal-template.md`

### 生成推荐方案

**推荐方案要求：**
- 基于搜索结果和用户需求
- 选择最佳匹配的方案
- 详细说明实现思路
- 预估开发时间和难度

### 生成备选方案

**备选方案类型：**
- 备选方案 1：轻量级（快速实现）
- 备选方案 2：功能最全（完整实现）
- 备选方案 3：创新方案（新技术栈）

### 方案对比

**对比维度：**
- 技术栈
- 优点
- 缺点
- 预估时间
- 难度
- 推荐度

### 用户选择

**选择方式：**
1. 使用推荐方案
2. 使用备选方案 1
3. 使用备选方案 2
4. 使用备选方案 3
5. 自定义方案

## 第四阶段：分阶段开发 + 循环审查

**目标：** 每个阶段都审查打分，分数低就返工，直到达标才进入下一阶段

### 阶段 4.1：需求确认

**流程：**
1. 生成需求文档
2. 审查打分（复用 review 子技能）
3. 分数 ≥ 80 → 进入下一阶段
4. 分数 < 80 → 返工（复用优化功能）→ 重新审查

### 阶段 4.2：方案确认

**流程：**
1. 生成技术方案文档
2. 审查打分
3. 分数 ≥ 80 → 进入下一阶段
4. 分数 < 80 → 返工 → 重新审查

### 阶段 4.3：代码实现

**流程：**
1. 生成 SKILL.md（复用 dev 子技能）
2. 安全审查（复用安全审查功能）
3. 审查打分
4. 分数 ≥ 80 → 进入下一阶段
5. 分数 < 80 → 返工 → 重新审查

### 阶段 4.4：测试验证

**流程：**
1. 生成评测集
2. 运行测试
3. 审查打分
4. 分数 ≥ 80 → 进入下一阶段
5. 分数 < 80 → 返工 → 重新审查

### 循环返工机制

**返工流程：**
1. 分析扣分项
2. 生成改进建议
3. 自动修复（如果可以）
4. 重新审查

**循环控制：**
- 最多返工 3 次
- 3 次后仍不达标 → 询问用户
- 用户可以：继续返工 / 降低标准 / 手动修改

### 审查标准（10 维度）

| 维度 | 满分 | 检查项 |
|------|------|--------|
| A1. 触发 | 20 | description 前 250 字符含触发词 |
| A2. 结构 | 15 | 目录结构完整、正文 ≤500 行 |
| A3. 上下文 | 15 | fork/inline 选择正确 |
| A4. 安全性 | 10 | 无敏感信息泄露 |
| A5. 可维护性 | 10 | 模块化、有版本管理 |
| A6. 测试 | 10 | 有 evals、有验收清单 |
| B1. 实用性 | 10 | 问题真实存在 |
| B2. 完成度 | 10 | 功能完整、流程无遗漏 |
| B3. 易用性 | 10 | 触发简单、参数易懂 |
| B4. 创新性 | 10 | 有独特设计 |
| **总分** | **120** | |

## 第五阶段：完整交付

**目标：** 生成完整 skill 包，节省用户调试步骤

### 最终审查

**审查内容：**
- 调用 review 子技能
- 10 维度综合评分
- 生成审查报告
- 分数 ≥ 90 → 通过

### 生成完整 SKILL.md

**内容要求：**
- 整合所有阶段的成果
- 生成符合官方规范的 SKILL.md
- 包含：触发条件、工作流程、输出规范、参考资料
- 包含：示例、反例、失败处理、Gotchas

### 生成评测集

**评测集要求：**
- 核心样本 5-10 个
- 边界样本 3-5 个
- 已知坑 3-5 个
- 生成 evals.json

### 安全审查

**审查协议（4 步）：**
1. 元数据检查
2. 权限范围分析
3. 内容扫描
4. Typosquat 检测

### 部署指南

**指南内容：**
- 本地测试命令
- 验收清单（7 项）
- 部署到全局目录
- 版本管理建议

### 优化建议

**建议内容：**
- 分析可优化点
- 提供优化方案
- 生成优化报告

### 版本管理

**管理内容：**
- 版本号管理
- 变更日志
- 发布流程

## 输出规范

### 输出格式
- 格式类型：Markdown
- 编码：UTF-8

### 输出位置
- SKILL.md：用户指定的项目目录
- 评测集：同目录下的 evals/evals.json

### 输出模板

```markdown
# {Skill 名称}

{简要说明}

## 触发条件

### 精确匹配
- {关键词1}、{关键词2}、{关键词3}

### 模糊匹配
- {场景描述}

### 不触发条件
- {排除场景}

## 核心原则

> {一句话总结}

## 工作流程

### 第一步：{步骤名称}
{详细说明}

### 第二步：{步骤名称}
{详细说明}

## 输出规范

### 输出格式
- {格式说明}

### 输出模板
​```markdown
{模板内容}
​```

## 参考资料

- {文件}：${CLAUDE_SKILL_DIR}/references/{file}.md

## 注意事项

### 必须遵守
- {规则}

### 禁止行为
- {禁止}

## 示例

### 输入示例
{示例}

### 期望输出
{输出}

### 反例
{反例}

## 失败处理

| 失败类型 | 表现 | 修复动作 |
|----------|------|----------|
| 触发错误 | 该触发没触发 / 不该触发却触发了 | 改 description，补正例/反例 |
| 步骤遗漏 | 跳过关键步骤 | 补 workflow，加检查点 |
| 输出不合格 | 格式错、内容缺 | 补 examples，明确输出契约 |
| 工具误用 | 用错工具或参数 | 补 gotchas，脚本化稳定动作 |

**连续失败 3 次应停下来问用户，不要无限重试。**

## Gotchas

### G1: 看起来像但不该触发
- {具体场景和判断依据}

### G2: 容易误用的工具
- {具体注意事项}

### G3: 连续失败时停止
- {停止条件}
```

## 参考资料

- 需求深挖指南：`${CLAUDE_SKILL_DIR}/../references/requirements.md`
- 搜索策略指南：`${CLAUDE_SKILL_DIR}/../references/search-strategy.md`
- 方案推送模板：`${CLAUDE_SKILL_DIR}/../references/proposal-template.md`
- 官方规范：`${CLAUDE_SKILL_DIR}/references/official-spec.md`
- 模板文件：`${CLAUDE_SKILL_DIR}/references/template.md`
- 示例文件：`${CLAUDE_SKILL_DIR}/references/example.md`
- 实战方法论：`${CLAUDE_SKILL_DIR}/references/methodology.md`
- 评测集：`${CLAUDE_SKILL_DIR}/evals/evals.json`

## 注意事项

### 必须遵守
- 深入理解需求，不要只问几个表面问题
- 全网搜索，不要自己造轮子
- 分阶段开发，每个阶段都审查打分
- 循环返工，分数低就返工，直到达标
- 完整交付，生成完整 skill 包

### 禁止行为
- 不要跳过需求深挖直接开发
- 不要跳过全网搜索直接开发
- 不要跳过审查打分直接交付
- 不要跳过安全审查直接部署

## 常见问题处理

### Q: 用户不知道怎么描述需求
**A:** 通过痛点挖掘问题引导：
- "这个任务你重复做过几次？"
- "每次做的时候最痛苦的是什么？"
- "你理想中的解决方案是什么样的？"

### Q: 搜索结果太多怎么办
**A:** 按相关度、下载量、评分综合排序，只展示前 10 个结果

### Q: 搜索结果太少怎么办
**A:** 扩大搜索范围，使用更多关键词组合

### Q: 审查打分一直不达标怎么办
**A:** 最多返工 3 次，3 次后询问用户：继续返工 / 降低标准 / 手动修改

### Q: 用户选择自定义方案怎么办
**A:** 了解用户想法，调整方案，确认后开始开发
```

- [ ] **Step 3: 验证文件创建**

```bash
head -100 skill-workspace/subskills/dev/SKILL.md
wc -l skill-workspace/subskills/dev/SKILL.md
```

Expected: 看到完整的开发子技能内容，约 500-600 行

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/subskills/dev/SKILL.md
git commit -m "feat: rewrite dev subskill with v3.0 flow"
```

---

## Task 5: 重写主技能 SKILL.md

**Files:**
- Modify: `skill-workspace/SKILL.md`

- [ ] **Step 1: 读取现有主技能 SKILL.md**

```bash
cat skill-workspace/SKILL.md
```

- [ ] **Step 2: 重写主技能 SKILL.md**

基于设计文档，重写主技能，集成新流程：

```markdown
---
name: skill-workspace
description: |
  Skill 全生命周期工作台。当用户提到"skill工作台"、"管理skill"、"搜索skill"、
  "下载skill"、"优化skill"、"部署skill"时触发。开发和审查功能由子技能处理。
  面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等），一站式完成 Skill 的
  搜索、下载、安全审查、开发生成、优化改进、质量测评、部署上线、更新卸载。
argument-hint: "[子命令] [参数]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob Grep Bash WebFetch
---

# Skill 全生命周期工作台（v3.0）

一站式 Skill 管理平台，覆盖 Skill 从发现到退役的完整生命周期。

## 核心原则

> **深入理解需求，全网搜索最佳方案，分阶段开发，循环审查，完整交付。**

## 子命令路由

| 子命令 | 说明 | 处理方式 |
|--------|------|----------|
| **开发** | 从零创建新 Skill | 加载 dev 子技能 |
| **审查** | 10 维度质量评分 | 加载 review 子技能 |
| **搜索** | 在线搜索可用 Skill | 本文件处理 |
| **下载** | 从 URL/名称/GitHub 安装 Skill | 本文件处理 |
| **安全审查** | 对 Skill 做安全扫描 | 本文件处理 |
| **优化** | 改进现有 Skill 质量 | 本文件处理 |
| **部署** | 安装到全局目录 | 本文件处理 |
| **管理** | 更新、卸载、列表 | 本文件处理 |

**路由规则：**
1. 用户说"开发xxx skill" → 加载 `subskills/dev/SKILL.md`
2. 用户说"审查skill" / "skill评分" → 加载 `subskills/review/SKILL.md`
3. 其他子命令 → 在本文件中处理

## 子技能加载

当路由到子技能时，使用 `Read` 工具加载对应的 SKILL.md：

```
开发 → Read ${CLAUDE_SKILL_DIR}/subskills/dev/SKILL.md
审查 → Read ${CLAUDE_SKILL_DIR}/subskills/review/SKILL.md
```

子技能是完整的包，有自己的 references 和 evals，可独立使用。

---

## 流程一：搜索 Skill

**目标：** 在线查找用户需要的 Skill（面向所有 Agent，不限于 Claude），避免重复造轮子。

**搜索源（按优先级）：**

**Tier 1：Skill 聚合市场（最优先）**

SkillsMP (skillsmp.com) — 1.5M+ skills，兼容所有 Agent（Claude Code、Codex CLI、ChatGPT 等）：
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q={关键词}&limit=10&sortBy=stars"
```
- 支持匿名访问（有每日速率限制）
- 可用参数：`category`（分类）、`occupation`（职业）、`page`、`limit`
- 返回：skill 名称、描述、GitHub 链接、stars

**Tier 2：Skills.sh 生态（CLI 工具）**
```bash
npx skills find {关键词}
```
- Skills.sh 是开源 Agent Skills 生态的包管理器
- 支持交互式搜索和关键词搜索
- 安装命令：`bash /path/to/skill/scripts/install-skill.sh <owner/repo@skill-name>`
- 检查更新：`npx skills check`
- 批量更新：`npx skills update`

**Tier 3：CocoLoop API**
```bash
curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"
```

**Tier 4：GitHub 搜索**
```bash
curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"
```

**Tier 5：clawhub CLI（兜底）**
```bash
npx clawhub@latest search {关键词}
```

**搜索策略：**

```
第一步：SkillsMP API 搜索（覆盖面最广）
  ↓ 无结果或超时
第二步：npx skills find（Skills.sh 生态）
  ↓ 无结果或超时
第三步：CocoLoop API 搜索
  ↓ 无结果或超时
第四步：GitHub API 搜索
  ↓ 无结果或超时
第五步：clawhub CLI 搜索
  ↓ 无结果
第六步：提示用户手动搜索或走「开发」流程
```

**输出格式：**
```
📋 搜索结果（来源：SkillsMP）:
  1. skill-name (⭐ 15.5k stars)
     📝 描述文本
     🔗 GitHub: https://github.com/xxx/xxx
  2. ...
```

**搜索后：**
- 展示结果列表，询问用户是否安装
- 如果都没找到 → 建议用户走「开发」流程

---

## 流程二：下载/安装 Skill

**目标：** 从各种来源安全安装 Skill。

**支持的来源：**

| 来源 | 格式 | 处理方式 |
|------|------|----------|
| URL | `https://.../*.skill` | 直接下载 |
| 名称 | `skill-name` | 搜索 → 确认 → 安装 |
| GitHub | `owner/repo` | 克隆 → 检查 → 安装 |

**安装流程：**

1. **获取 Skill 内容**
   - URL → curl 下载
   - 名称 → 按搜索流程找到后下载
   - GitHub → git clone 或 curl 下载 SKILL.md

2. **安全审查**（强制）
   - 调用「安全审查」流程
   - 评级 ≥ B → 继续
   - 评级 ≤ C → 询问用户是否继续

3. **安装到工作区**
   ```bash
   # 安装到当前工作区（开发模式）
   cp -r {skill目录}/ "./{skill名}/"

   # 或安装到全局（使用模式）
   # 路径因 Agent 而异：
   #   Claude Code: ~/.claude/skills/{skill名}/
   #   Codex CLI:   ~/.codex/skills/{skill名}/
   #   通用:        ~/.skills/{skill名}/
   cp -r {skill目录}/ {全局skills目录}/{skill名}/
   ```

4. **确认安装结果**

---

## 流程三：安全审查

**目标：** 对 Skill 进行安全扫描，识别风险。整合 skill-vetter 的 4 步审查协议。

**审查协议（4 步）：**

### 第 1 步：元数据检查
- [ ] `name` 与预期 skill 名称匹配（无 typosquatting）
- [ ] `version` 遵循语义化版本号
- [ ] `description` 清晰且与实际行为一致
- [ ] `author` 可识别

### 第 2 步：权限范围分析

| 权限 | 风险等级 | 说明 |
|------|----------|------|
| Read | Low | 几乎总是合法的 |
| Write | Medium | 必须说明写入哪些文件 |
| Network | High | 必须说明访问哪些端点 |
| Shell/Bash | Critical | 必须说明执行哪些命令 |

**⚠️ 危险组合：** `network` + `shell` 同时出现 → 可能导致数据泄露

### 第 3 步：内容扫描

**🔴 BLOCK（阻止安装）：**
- 引用 `~/.ssh`、`~/.aws`、`~/.env` 等敏感路径
- 使用 `curl`、`wget`、`nc`、`bash -i` 等命令
- `base64` 混淆内容
- 禁用安全机制
- 未知或可疑 URL

**⚠️ WARNING（需要审查）：**
- `/**/*` 等宽泛通配符
- `sudo` 使用
- 潜在的提示注入

**ℹ️ INFO（信息）：**
- 缺少 description/version/author

### 第 4 步：Typosquat 检测
- 检查单字符交换（如 `skil` vs `skill`）
- 检查同形异义字符（如 `l/1`、`O/0`）
- 检查多余连字符（如 `skill--name`）

**输出格式：**
```
安全审查报告
============
Skill: {name}
安全评级: SAFE / WARNING / DANGER / BLOCK
风险标记: {数量}
建议: install / sandbox first / do not install

详细发现:
- 元数据: ✅ 正常 / ⚠️ 问题描述
- 权限: ✅ 最小权限 / ⚠️ 过度权限
- 内容: ✅ 无风险 / ⚠️ 风险项列表
- Typosquat: ✅ 无 / ⚠️ 可疑命名
```

**参考：** 如果 skill-vetter 已安装，可参考其详细审查协议

---

## 流程四：优化 Skill

**目标：** 改进现有 Skill 的质量，解决具体问题。

**优化触发信号：**
- 用户说"这个 skill 不好用"
- 测评发现的问题需要修复
- 用户想增加新功能或改进行为

**优化流程：**

1. **诊断** — 先用「审查」流程找出问题
2. **制定方案** — 按优先级排列改进项
3. **执行改进**
   - description 不准 → 改触发词，补正例/反例
   - workflow 有漏洞 → 补步骤，加检查点
   - 输出不合格 → 改格式，补样例
   - 误触发 → 收窄触发条件
4. **验证** — 用同一个 case 跑一遍，确认改善
5. **回归** — 用 evals 重跑，确保没引入新问题

---

## 流程五：部署

**目标：** 将本地测试通过的 Skill 安装到全局目录。

**部署流程：**

1. **确认来源** — 工作区中的哪个 skill 目录
2. **检查是否通过测评** — 建议先走「审查」流程
3. **复制到全局**
   ```bash
   # 路径因 Agent 而异：
   #   Claude Code: ~/.claude/skills/
   #   Codex CLI:   ~/.codex/skills/
   #   通用:        ~/.skills/
   cp -r "./{skill名}/" {全局skills目录}/{skill名}/
   ```
4. **验证部署**
   ```bash
   ls {全局skills目录}/{skill名}/
   ```
5. **测试全局可用** — 使用 Agent CLI 测试，如：
   - Claude Code: `claude -p "使用 {name} 完成 XXX"`
   - Codex CLI: `codex "使用 {name} 完成 XXX"`

**⚠️ 永远用 `cp`，不用 `mv`，保留源文件。**

---

## 流程六：管理

**目标：** 管理已安装的 Skill。

### 列出已安装 Skill
```bash
# 路径因 Agent 而异：
#   Claude Code: ~/.claude/skills/
#   Codex CLI:   ~/.codex/skills/
#   通用:        ~/.skills/
ls {全局skills目录}/
ls ./
```

### 更新 Skill

**单个更新：**
1. 查询最新版本（SkillsMP API、CocoLoop API 或 GitHub）
2. 比较本地版本与远程版本
3. 有更新 → 备份旧版 → 下载新版 → 安全审查 → 安装

**批量更新（如 find-skills 已安装）：**
```bash
npx skills update
```
- 检查所有已安装 skills 的更新
- 自动更新到最新版本

**检查更新：**
```bash
npx skills check
```

### 卸载 Skill
1. 确认 skill 存在
2. 询问用户确认
3. 删除 skill 目录
4. 清理相关配置

---

## 参考资料

**本工作台：**
- 需求深挖指南：`${CLAUDE_SKILL_DIR}/references/requirements.md`
- 搜索策略指南：`${CLAUDE_SKILL_DIR}/references/search-strategy.md`
- 方案推送模板：`${CLAUDE_SKILL_DIR}/references/proposal-template.md`
- 优化方法：`${CLAUDE_SKILL_DIR}/references/optimize.md`
- 部署指南：`${CLAUDE_SKILL_DIR}/references/deploy.md`

**子技能：**
- 开发子技能：`${CLAUDE_SKILL_DIR}/subskills/dev/SKILL.md`
- 审查子技能：`${CLAUDE_SKILL_DIR}/subskills/review/SKILL.md`

**全局技能（如已安装）：**
- find-skills — Skills.sh 生态搜索
- skill-creation-guide — Anthropic 官方创建指南（含 init_skill.py、package_skill.py）
- skill-vetter — 安全审查协议
- cocoloop — CocoLoop Skill 管理器

**注意：** 全局技能的安装路径因 Agent 而异：
- Claude Code: `~/.claude/skills/`
- Codex CLI: `~/.codex/skills/`
- 通用: `~/.skills/`

## 注意事项

### 必须遵守
- 深入理解需求，不要只问几个表面问题
- 全网搜索，不要自己造轮子
- 分阶段开发，每个阶段都审查打分
- 循环返工，分数低就返工，直到达标
- 完整交付，生成完整 skill 包
- 下载前必须做安全审查
- 部署前建议做质量测评
- 永远用 cp 不用 mv
- 用 AskUserQuestion 与用户交互

### 禁止行为
- 跳过需求深挖直接开发
- 跳过全网搜索直接开发
- 跳过审查打分直接交付
- 跳过安全审查直接部署
- 未测试就部署到全局
- 覆盖用户未确认的文件
- 静默执行危险操作

## 示例

### 搜索并安装
```
用户: 帮我找个代码格式化的 skill
→ 搜索流程 → 展示结果 → 用户选择 → 安全审查 → 安装
```

### 从零开发（v3.0 流程）
```
用户: 帮我开发一个代码审查 skill
→ 需求深挖 → 全网搜索 → 方案推送 → 分阶段开发 → 完整交付
```

### 审查评分
```
用户: 帮我审查一下这个 skill 的质量
→ 加载 review 子技能 → 安全审查 → 10 维度评分 → 输出报告
```

### 优化现有
```
用户: 这个 skill 触发不太准，帮我优化
→ 诊断（审查）→ 找出问题 → 改 description → 验证
```
```

- [ ] **Step 3: 验证文件创建**

```bash
head -100 skill-workspace/SKILL.md
wc -l skill-workspace/SKILL.md
```

Expected: 看到完整的主技能内容，约 400-500 行

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/SKILL.md
git commit -m "feat: rewrite main skill with v3.0 flow"
```

---

## Task 6: 更新评测集

**Files:**
- Modify: `skill-workspace/evals/evals.json`

- [ ] **Step 1: 读取现有评测集**

```bash
cat skill-workspace/evals/evals.json
```

- [ ] **Step 2: 更新评测集**

添加新流程的评测用例：

```json
{
  "skill_name": "skill-workspace",
  "version": "3.0.0",
  "evals": [
    {
      "id": 1,
      "prompt": "帮我开发一个代码格式化 skill",
      "expected_output": "完整的 SKILL.md 文件，包含触发条件、工作流程、输出规范、参考资料、示例、反例、失败处理、Gotchas",
      "assertions": [
        { "id": "a1", "text": "通过需求深挖理解用户痛点" },
        { "id": "a2", "text": "通过全网搜索找到最佳方案" },
        { "id": "a3", "text": "通过方案推送让用户选择" },
        { "id": "a4", "text": "通过分阶段开发确保质量" },
        { "id": "a5", "text": "通过循环审查确保达标" },
        { "id": "a6", "text": "通过完整交付生成完整 skill 包" }
      ]
    },
    {
      "id": 2,
      "prompt": "帮我审查一下这个 skill 的质量",
      "expected_output": "审查报告，包含 10 维度评分、亮点、问题与建议、综合评级",
      "assertions": [
        { "id": "a1", "text": "安全审查通过" },
        { "id": "a2", "text": "10 维度评分完整" },
        { "id": "a3", "text": "审查报告格式正确" }
      ]
    },
    {
      "id": 3,
      "prompt": "帮我找个代码格式化的 skill",
      "expected_output": "搜索结果列表，包含 skill 名称、描述、GitHub 链接、stars",
      "assertions": [
        { "id": "a1", "text": "搜索结果来自多个源" },
        { "id": "a2", "text": "搜索结果按相关度排序" },
        { "id": "a3", "text": "搜索结果格式正确" }
      ]
    },
    {
      "id": 4,
      "prompt": "帮我优化这个 skill",
      "expected_output": "优化报告，包含问题诊断、改进方案、验证结果",
      "assertions": [
        { "id": "a1", "text": "问题诊断准确" },
        { "id": "a2", "text": "改进方案可行" },
        { "id": "a3", "text": "验证结果通过" }
      ]
    },
    {
      "id": 5,
      "prompt": "帮我部署这个 skill",
      "expected_output": "部署指南，包含本地测试命令、验收清单、部署命令、版本管理建议",
      "assertions": [
        { "id": "a1", "text": "本地测试命令正确" },
        { "id": "a2", "text": "验收清单完整" },
        { "id": "a3", "text": "部署命令正确" }
      ]
    },
    {
      "id": 6,
      "prompt": "帮我管理已安装的 skill",
      "expected_output": "已安装 skill 列表，包含名称、版本、状态",
      "assertions": [
        { "id": "a1", "text": "列表完整" },
        { "id": "a2", "text": "信息准确" }
      ]
    },
    {
      "id": 7,
      "prompt": "帮我开发一个代码审查 skill，要求支持多种语言",
      "expected_output": "完整的 SKILL.md 文件，支持多种语言的代码审查",
      "assertions": [
        { "id": "a1", "text": "需求深挖理解多语言需求" },
        { "id": "a2", "text": "全网搜索找到多语言方案" },
        { "id": "a3", "text": "方案推送包含多语言选项" },
        { "id": "a4", "text": "分阶段开发确保多语言支持" },
        { "id": "a5", "text": "循环审查确保多语言质量" },
        { "id": "a6", "text": "完整交付生成多语言 skill 包" }
      ]
    },
    {
      "id": 8,
      "prompt": "帮我开发一个代码审查 skill，要求支持安全审查",
      "expected_output": "完整的 SKILL.md 文件，支持安全审查功能",
      "assertions": [
        { "id": "a1", "text": "需求深挖理解安全审查需求" },
        { "id": "a2", "text": "全网搜索找到安全审查方案" },
        { "id": "a3", "text": "方案推送包含安全审查选项" },
        { "id": "a4", "text": "分阶段开发确保安全审查功能" },
        { "id": "a5", "text": "循环审查确保安全审查质量" },
        { "id": "a6", "text": "完整交付生成安全审查 skill 包" }
      ]
    },
    {
      "id": 9,
      "prompt": "帮我开发一个代码审查 skill，要求支持性能分析",
      "expected_output": "完整的 SKILL.md 文件，支持性能分析功能",
      "assertions": [
        { "id": "a1", "text": "需求深挖理解性能分析需求" },
        { "id": "a2", "text": "全网搜索找到性能分析方案" },
        { "id": "a3", "text": "方案推送包含性能分析选项" },
        { "id": "a4", "text": "分阶段开发确保性能分析功能" },
        { "id": "a5", "text": "循环审查确保性能分析质量" },
        { "id": "a6", "text": "完整交付生成性能分析 skill 包" }
      ]
    }
  ]
}
```

- [ ] **Step 3: 验证文件更新**

```bash
cat skill-workspace/evals/evals.json | jq .
```

Expected: 看到更新后的评测集，包含 9 个评测用例

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/evals/evals.json
git commit -m "feat: update evals for v3.0 flow"
```

---

## Task 7: 更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 读取现有 README.md**

```bash
cat README.md
```

- [ ] **Step 2: 更新 README.md**

更新目录结构和使用说明：

```markdown
# Skill 全生命周期工作台（v3.0）

> 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

一站式完成 Skill 的 **需求深挖 → 全网搜索 → 方案推送 → 分阶段开发 → 完整交付**。

## 🚀 快速安装

```bash
# 解压 skill 包
unzip skill-workspace.skill -d skill-workspace-install

# 运行安装脚本
cd skill-workspace-install
./install-skill-workspace.sh
```

## 📁 目录结构

```
skill-workspace/
├── SKILL.md                              # 主入口（v3.0）
├── references/
│   ├── requirements.md                   # 需求深挖指南（新增）
│   ├── search-strategy.md                # 搜索策略指南（新增）
│   ├── proposal-template.md              # 方案推送模板（新增）
│   ├── optimize.md                       # 优化方法论
│   └── deploy.md                         # 部署指南
├── evals/
│   └── evals.json                        # 主技能评测集（9 条）
│
└── subskills/
    ├── dev/                              # 开发子技能（v3.0）
    │   ├── SKILL.md                      # 开发流程（553 行）
    │   ├── references/
    │   │   ├── official-spec.md          # 官方规范
    │   │   ├── template.md              # 模板文件
    │   │   ├── example.md               # 示例文件
    │   │   └── methodology.md           # 实战方法论
    │   └── evals/
    │       └── evals.json               # 开发评测集（6 条）
    │
    └── review/                           # 审查子技能（完整包）
        ├── SKILL.md                      # 审查流程（406 行）
        ├── references/
        │   ├── official-spec.md          # 官方规范
        │   ├── scoring-criteria.md      # 10 维度评分标准
        │   └── security.md              # 安全审查规则
        └── evals/
            ├── evals.json               # 审查评测集（5 条）
            └── test-cases.json          # 测试用例
```

## 🔧 使用方式

### 统一入口

```
/skill-workspace 开发 代码格式化     → 加载 dev 子技能（v3.0 流程）
/skill-workspace 审查 my-skill       → 加载 review 子技能
/skill-workspace 搜索 代码格式化     → 在线搜索 skill
/skill-workspace 下载 pdf-processor  → 下载安装 skill
/skill-workspace 优化 my-skill       → 改进现有 skill
/skill-workspace 部署 my-skill       → 安装到全局
/skill-workspace 管理                → 列出/更新/卸载
```

### 自然语言触发

```
"帮我开发一个代码审查 skill"        → 自动走 v3.0 开发流程
"审查一下这个 skill 的质量"         → 自动走审查流程
"帮我找个代码格式化的 skill"        → 自动走搜索流程
```

### 不同 Agent 的使用方式

```bash
# Claude Code
claude -p "使用 skill-workspace 搜索 代码格式化"

# Codex CLI
codex "使用 skill-workspace 搜索 代码格式化"

# 其他 Agent
# 请使用对应的 CLI 调用
```

## 🔍 核心功能（v3.0）

### 1. 需求深挖（新增）

- **痛点挖掘** — 5-8 个问题深入理解用户痛点
- **用户场景分析** — 分析使用频率、skill 水平、偏好、场景
- **需求确认** — 打分 ≥ 80 分才通过

### 2. 全网搜索（增强）

| 优先级 | 来源 | 说明 |
|--------|------|------|
| Tier 1 | **SkillsMP** (skillsmp.com) | 1.5M+ skills，兼容所有 Agent |
| Tier 2 | **npx skills find** | Skills.sh 生态 |
| Tier 3 | CocoLoop API | Skill 聚合市场 |
| Tier 4 | GitHub 搜索 | 搜索包含 SKILL.md 的仓库 |
| Tier 5 | clawhub CLI | 命令行搜索工具（兜底） |

### 3. 方案推送（新增）

- **主推方案** — 最佳匹配的方案
- **备选方案 1** — 轻量级（快速实现）
- **备选方案 2** — 功能最全（完整实现）
- **备选方案 3** — 创新方案（新技术栈）

### 4. 分阶段开发 + 循环审查（新增）

- **阶段 4.1：需求确认** → 审查打分 → 循环返工
- **阶段 4.2：方案确认** → 审查打分 → 循环返工
- **阶段 4.3：代码实现** → 审查打分 → 循环返工
- **阶段 4.4：测试验证** → 审查打分 → 循环返工

### 5. 完整交付（增强）

- **最终审查** — 10 维度综合评分
- **生成完整 SKILL.md** — 符合官方规范
- **生成评测集** — 核心样本 + 边界样本 + 已知坑
- **安全审查** — 4 步协议
- **部署指南** — 本地测试 + 验收清单 + 部署命令
- **优化建议** — 分析可优化点
- **版本管理** — 版本号 + 变更日志 + 发布流程

### 6. 安全审查（保留）

- **元数据检查** — 防止 typosquatting
- **权限范围分析** — 识别过度权限
- **内容扫描** — 检测敏感路径、危险命令
- **Typosquat 检测** — 防止名称欺骗

### 7. 开发 Skill（3 条路径）

- **路径 A**：找现成的 → 去 SkillsMP/CocoLoop/GitHub 搜索
- **路径 B**：改造现成的 → 保留核心结构，改 7 个点
- **路径 C**：从零写 → 走 v3.0 完整流程

### 8. 审查 Skill（10 维度评分）

- **A 组：规范性**（80 分）— 触发、结构、上下文、安全性、可维护性、测试
- **B 组：实用性**（40 分）— 实用性、完成度、易用性、创新性

## 📊 版本信息

- 版本：v3.0.0
- 日期：2026-06-09
- 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

## 🔗 相关链接

- [Agent Skill 规范](https://docs.anthropic.com/claude-code/skills)
- [Skills.sh — Agent Skills 生态](https://skills.sh)
- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com)

## 📄 许可证

MIT License
```

- [ ] **Step 3: 验证文件更新**

```bash
cat README.md | head -100
```

Expected: 看到更新后的 README，包含 v3.0 功能说明

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README for v3.0"
```

---

## Task 8: 最终验证

- [ ] **Step 1: 验证完整目录结构**

```bash
cd "D:/ai/claude code/skill开发"
find skill-workspace -type f | sort
```

Expected: 看到完整的文件列表

- [ ] **Step 2: 验证所有 SKILL.md 文件**

```bash
# 主技能
head -20 skill-workspace/SKILL.md

# 开发子技能
head -20 skill-workspace/subskills/dev/SKILL.md

# 审查子技能
head -20 skill-workspace/subskills/review/SKILL.md
```

Expected: 每个文件都有正确的 frontmatter

- [ ] **Step 3: 验证 references 完整性**

```bash
ls -la skill-workspace/references/
```

Expected: 看到 5 个 reference 文件（requirements.md、search-strategy.md、proposal-template.md、optimize.md、deploy.md）

- [ ] **Step 4: 验证 evals 完整性**

```bash
cat skill-workspace/evals/evals.json | jq .
```

Expected: 看到 9 个评测用例

- [ ] **Step 5: 最终 Commit**

```bash
git add -A
git commit -m "feat: complete skill-workspace v3.0 upgrade"
```

---

## 完成

实施计划完成。所有任务执行完毕后，skill-workspace 将升级到 v3.0：

1. **需求深挖** — 深入理解用户痛点
2. **全网搜索** — 5 层搜索源并行搜索
3. **方案推送** — 主推方案 + 2-3 个备选
4. **分阶段开发** — 每个阶段都审查打分
5. **循环审查** — 分数低就返工，直到达标
6. **完整交付** — 生成完整 skill 包

**下一步：** 选择执行方式：
1. **Subagent-Driven（推荐）** - 每个 Task 一个子代理，任务间审查
2. **Inline Execution** - 在当前会话中执行，批量处理

# Skill Workspace 集成实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 skill-workspace、skill-dev、skill-review 集成为一个完整的 Skill 开发工作台，每个子技能是独立完整的包，可单独使用。

**Architecture:** 采用"主入口 + 独立子技能包"架构。skill-workspace 作为统一入口，通过子命令路由到 dev/review 子技能。每个子技能保持完整的 references 和 evals，可独立部署。

**Tech Stack:** Claude Code Skill 规范、Markdown、JSON

---

## 文件结构

```
skill-workspace/
├── SKILL.md                    # 主入口：路由到子技能
├── README.md                   # 使用说明
├── subskills/
│   ├── dev/                    # 开发子技能（完整包）
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── official-spec.md
│   │   │   ├── template.md
│   │   │   ├── example.md
│   │   │   └── methodology.md
│   │   └── evals/
│   │       └── evals.json
│   └── review/                 # 审查子技能（完整包）
│       ├── SKILL.md
│       ├── references/
│       │   ├── official-spec.md
│       │   ├── scoring-criteria.md
│       │   └── security.md
│       └── evals/
│           ├── evals.json
│           └── test-cases.json
├── references/                 # 共享参考资料
│   ├── optimize.md
│   └── deploy.md
└── evals/
    └── evals.json              # 主技能评测集
```

---

## Task 1: 创建目录结构

**Files:**
- Create: `skill-workspace/subskills/dev/references/`
- Create: `skill-workspace/subskills/dev/evals/`
- Create: `skill-workspace/subskills/review/references/`
- Create: `skill-workspace/subskills/review/evals/`

- [ ] **Step 1: 创建子技能目录结构**

```bash
cd "D:/ai/claude code/skill开发"
mkdir -p skill-workspace/subskills/dev/references
mkdir -p skill-workspace/subskills/dev/evals
mkdir -p skill-workspace/subskills/review/references
mkdir -p skill-workspace/subskills/review/evals
```

- [ ] **Step 2: 验证目录创建**

```bash
find skill-workspace/subskills -type d | sort
```

Expected: 看到完整的目录结构

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/subskills/
git commit -m "feat: create subskills directory structure with references and evals"
```

---

## Task 2: 迁移开发子技能的 references

**Files:**
- Copy: `skill-dev/references/official-spec.md` → `skill-workspace/subskills/dev/references/`
- Copy: `skill-dev/references/template.md` → `skill-workspace/subskills/dev/references/`
- Copy: `skill-dev/references/example.md` → `skill-workspace/subskills/dev/references/`
- Copy: `skill-dev/references/methodology.md` → `skill-workspace/subskills/dev/references/`

- [ ] **Step 1: 复制所有开发参考资料**

```bash
cd "D:/ai/claude code/skill开发"
cp skill-dev/references/official-spec.md skill-workspace/subskills/dev/references/
cp skill-dev/references/template.md skill-workspace/subskills/dev/references/
cp skill-dev/references/example.md skill-workspace/subskills/dev/references/
cp skill-dev/references/methodology.md skill-workspace/subskills/dev/references/
```

- [ ] **Step 2: 验证文件复制**

```bash
ls -la skill-workspace/subskills/dev/references/
wc -l skill-workspace/subskills/dev/references/*.md
```

Expected: 4 个 .md 文件，每个都有内容

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/subskills/dev/references/
git commit -m "feat: migrate dev references to subskill package"
```

---

## Task 3: 迁移审查子技能的 references

**Files:**
- Copy: `skill-review/references/official-spec.md` → `skill-workspace/subskills/review/references/`
- Copy: `skill-review/references/scoring-criteria.md` → `skill-workspace/subskills/review/references/`
- Copy: `skill-workspace/references/security.md` → `skill-workspace/subskills/review/references/`

- [ ] **Step 1: 复制所有审查参考资料**

```bash
cd "D:/ai/claude code/skill开发"
cp skill-review/references/official-spec.md skill-workspace/subskills/review/references/
cp skill-review/references/scoring-criteria.md skill-workspace/subskills/review/references/
cp skill-workspace/references/security.md skill-workspace/subskills/review/references/
```

- [ ] **Step 2: 验证文件复制**

```bash
ls -la skill-workspace/subskills/review/references/
wc -l skill-workspace/subskills/review/references/*.md
```

Expected: 3 个 .md 文件，每个都有内容

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/subskills/review/references/
git commit -m "feat: migrate review references to subskill package"
```

---

## Task 4: 迁移 evals 文件

**Files:**
- Copy: `skill-dev/evals/evals.json` → `skill-workspace/subskills/dev/evals/`
- Copy: `skill-review/evals/evals.json` → `skill-workspace/subskills/review/evals/`
- Copy: `skill-review/evals/test-cases.json` → `skill-workspace/subskills/review/evals/`

- [ ] **Step 1: 复制所有 evals 文件**

```bash
cd "D:/ai/claude code/skill开发"
cp skill-dev/evals/evals.json skill-workspace/subskills/dev/evals/
cp skill-review/evals/evals.json skill-workspace/subskills/review/evals/
cp skill-review/evals/test-cases.json skill-workspace/subskills/review/evals/
```

- [ ] **Step 2: 验证文件复制**

```bash
ls -la skill-workspace/subskills/dev/evals/
ls -la skill-workspace/subskills/review/evals/
cat skill-workspace/subskills/dev/evals/evals.json | jq .
cat skill-workspace/subskills/review/evals/evals.json | jq .
```

Expected: JSON 文件格式正确

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/subskills/dev/evals/ skill-workspace/subskills/review/evals/
git commit -m "feat: migrate evals to subskill packages"
```

---

## Task 5: 创建开发子技能 SKILL.md

**Files:**
- Create: `skill-workspace/subskills/dev/SKILL.md`

- [ ] **Step 1: 读取现有 skill-dev/SKILL.md**

```bash
cat skill-dev/SKILL.md
```

- [ ] **Step 2: 创建开发子技能 SKILL.md**

基于 skill-dev 内容，创建子技能版本。关键修改：
- 保留完整的开发流程和所有细节
- 更新 references 路径为 `${CLAUDE_SKILL_DIR}/references/`
- 添加 evals 引用

```markdown
---
name: skill-dev
description: |
  Skill 开发助手。当用户提到"开发skill"、"创建skill"、"新建skill"、
  "写个skill"、"帮我做个skill"时触发。引导用户完成符合官方规范的
  Skill 开发，自动生成 SKILL.md 文件。
argument-hint: "[skill功能描述]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob
---

# Skill 开发助手

你是一个 Skill 开发专家，精通 Claude Code 官方规范。你的目标是帮助用户开发高质量的 Skill。

## 核心原则

> **一次到位，符合规范。** 生成的 SKILL.md 必须符合官方规范，不需要二次修改。

## 前置判断：是否值得 Skill 化

在开始开发前，先帮用户判断任务是否值得 Skill 化：

1. **问用户：这个任务重复出现过几次？** — 至少 3 次才值得
2. **问用户：Agent 每次是否稳定犯同一类错？** — 不稳定犯错说明边界不清
3. **建议用户先跑 baseline** — 拿 3-5 个真实 case 让 Agent 在没有 Skill 的情况下跑一遍，观察是否稳定暴露问题

**如果任务不值得 Skill 化，直接告诉用户，不要硬写。**

## 三条路径选择

根据用户情况选择不同路径：

| 路径 | 适用场景 | 第一步 |
|------|----------|--------|
| **A. 找现成的** | 常见场景（代码审查、文档整理等） | 去 skills.sh 或社区搜索 |
| **B. 改造现成的** | 找到方向接近但不完全匹配的 Skill | 保留核心结构，改 description、workflow、输出格式 |
| **C. 从零写** | 没有合适 Skill，或强依赖内部系统/私有流程 | 走下面的完整流程 |

**先 A，再 B，最后 C。** 能复用就别从空白页开始。

### 路径 A：找到现成 Skill 后怎么判断值不值得用

不要看到安装量高就直接装。至少检查这 7 项：

1. **元数据** — description 不能像口号，要说清楚"用户说什么时该触发"
2. **触发条件** — 哪些必须用、哪些不要用？不能只写"当用户需要时使用"
3. **输入规范** — 需要哪些材料？缺材料怎么办？
4. **工作流程** — 先做什么后做什么？不能只有原则没有动作
5. **输出契约** — 交付物长什么样？不能没有格式也没有示例
6. **失败处理** — 什么情况下要停、重试或问人？
7. **示例和评测** — 怎么知道它做得对？

### 路径 B：改造现有 Skill 的改造点

1. **description** — 加上用户自己常用的说法、关键词、触发场景
2. **触发条件和反例** — 确认不会和其他 Skill 冲突
3. **输入规范** — 加上特有的来源（内部系统链接、特定格式）
4. **workflow** — 加上必须的检查点（如安全审查、术语一致性）
5. **输出格式** — 改成用户模板（标题结构、标签、归档规则）
6. **停止条件** — 加上风险动作边界（如不自动发布、不自动修改权限）
7. **示例** — 换成真实 case

### 路径特殊：从真实协作沉淀 Skill

当用户已经跑通了一次完整任务，想把它沉淀成 Skill：

1. **复盘对话** — 找出反复纠正过的地方：哪些必须确认、哪些不能自动做、哪些输出不合格
2. **提炼结构** — 触发条件、输入要求、固定步骤、失败处理、验收标准
3. **沉淀 SKILL.md** — 长资料放 references/，稳定动作做成 scripts/
4. **弱模型验证** — 让较弱模型按 Skill 执行同类任务，看是否稳定

## 工作流程

### 第一步：需求分析

通过对话了解用户需求：

1. **功能定位**
   - 这个 Skill 做什么？
   - 解决什么问题？
   - 目标用户是谁？

2. **触发设计**
   - 用户会用什么词触发？
   - 有哪些同义词/近义词？
   - 什么情况下不应该触发？

3. **执行模式**
   - 是否需要对话历史？→ inline
   - 是否是独立任务？→ fork
   - 是否需要特定 Agent？→ Explore/Plan/general-purpose

4. **输出规范**
   - 输出格式？（Markdown/JSON/代码/其他）
   - 输出位置？（指定目录）
   - 是否需要模板？

5. **参考资料**
   - 需要哪些参考资料？
   - 是否有配置文件？
   - 是否有示例代码？

**关键判断：**

```
如果指令本身就包含了完成任务所需的全部信息 → fork
如果指令依赖对话上下文来理解 → inline
```

### 第二步：生成 SKILL.md

根据需求生成符合官方规范的 SKILL.md。

**参考资料：**
- 官方规范：`${CLAUDE_SKILL_DIR}/references/official-spec.md`
- 模板文件：`${CLAUDE_SKILL_DIR}/references/template.md`
- 示例文件：`${CLAUDE_SKILL_DIR}/references/example.md`
- 实战方法论：`${CLAUDE_SKILL_DIR}/references/methodology.md`

### 第三步：保存到本地项目目录

1. **保存位置（本地开发）**
   - 当前项目：`<项目根目录>/<skill-name>/SKILL.md`
   - 不要直接保存到全局目录

2. **创建目录结构**
   ```
   <项目根目录>/<skill-name>/
   ├── SKILL.md          # 核心说明书
   ├── references/       # 参考资料，按需加载
   ├── scripts/          # 脚本化动作
   ├── examples/         # 好结果、坏结果、边界样例
   └── evals/            # 最小评测集
   ```

3. **告知用户**
   - 已保存到本地项目目录
   - 需要测试通过后才能部署到全局

### 第四步：本地测试

1. **提供测试命令**
   ```bash
   # 在项目目录测试
   claude -p "使用 <name> 完成 XXX 任务"
   ```

2. **验收清单**（7 项全部通过才算合格）
   - [ ] 用户换一种常见说法时，description 仍能触发
   - [ ] 缺少必要输入时，Skill 知道该追问、假设还是停止
   - [ ] 每个步骤都有明确动作，而不只是原则性描述
   - [ ] 输出格式固定，能被人或下一个流程继续使用
   - [ ] 至少有 3 个标准样例、2 个边界样例、1 个反例
   - [ ] 关键 CLI 或脚本调用有参数示例和失败处理
   - [ ] 停止条件明确：缺资料、权限失败、高风险动作时有处理路径

3. **创建 Evals 评测集**
   ```json
   {
     "skill_name": "<skill-name>",
     "evals": [
       {
         "id": 1,
         "prompt": "用户的真实任务描述",
         "expected_output": "期望 Agent 最终交付什么",
         "assertions": [
           { "id": "a1", "text": "可检查的细项" }
         ]
       }
     ]
   }
   ```
   - 核心样本 5-10 个（用户最常提交的任务）
   - 边界样本 3-5 个（空输入、资料不全、格式混乱）
   - 已知坑 3-5 个（之前误触发、乱用工具的案例）

4. **迭代优化**
   - 根据测试结果修改 SKILL.md
   - 每次修改后用 evals 重跑，确保没有引入新问题
   - 重复测试直到满意

### 第五步：部署到全局

**前提：** 本地测试通过后才执行此步骤。

1. **部署命令**
   ```bash
   # 复制到全局目录
   cp -r <项目根目录>/<skill-name>/ ~/.claude/skills/<skill-name>/
   ```

2. **验证部署**
   ```bash
   # 验证文件已复制
   ls ~/.claude/skills/<skill-name>/

   # 测试全局可用
   claude -p "使用 <name> 完成 XXX 任务"
   ```

3. **版本管理建议**
   - 本地项目目录作为源码仓库
   - 全局目录作为部署位置
   - 修改时先改本地，测试通过后再部署

## 输出规范

### 输出格式
- 格式类型：Markdown
- 编码：UTF-8

### 输出模板

```markdown
# {Skill 名称}

{简要说明}

## 触发条件

### 精确匹配
- {关键词1}、{关键词2}

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
```

## 参考资料

- 官方规范：`${CLAUDE_SKILL_DIR}/references/official-spec.md`
- 模板文件：`${CLAUDE_SKILL_DIR}/references/template.md`
- 示例文件：`${CLAUDE_SKILL_DIR}/references/example.md`
- 实战方法论：`${CLAUDE_SKILL_DIR}/references/methodology.md`
- 评测集：`${CLAUDE_SKILL_DIR}/evals/evals.json`

## 常见问题处理

### Q: 用户不知道怎么描述需求
**A:** 通过提问引导：
- "你希望这个 Skill 做什么？"
- "用户会用什么词来触发？"
- "输出应该是什么格式？"

### Q: 不确定用 fork 还是 inline
**A:** 判断法则：
- 指令自带全部信息 → fork
- 依赖对话上下文 → inline
- 默认推荐 fork（上下文生存策略）

### Q: 参考资料太多怎么办
**A:** 正文 ≤500 行，长资料放 references/，用 ${CLAUDE_SKILL_DIR} 引用

### Q: 怎么判断 Skill 是否成熟
**A:** 用弱模型验收。如果更便宜、更弱的模型也能按流程产出稳定结果，说明 Skill 真的把经验写进了流程。

## 注意事项

- 生成的 SKILL.md 必须符合官方规范
- description 前 250 字符必须包含触发词
- 正文控制在 500 行以内
- 参考资料放 references/ 目录
- 使用 ${CLAUDE_SKILL_DIR} 引用文件路径

## Gotchas

### G1: 看起来像但不该触发
- 用户说"帮我看看这段代码"可能是问功能，不是开发 Skill
- 判断依据：是否明确说要做一个"新 Skill"

### G2: 容易误用的工具
- 不要用 Write 直接覆盖用户文件，先用 Edit 做 diff

### G3: 连续失败时停止
- 如果连续 3 次输出不符合格式要求，停下来问用户
```

- [ ] **Step 3: 验证文件创建**

```bash
head -50 skill-workspace/subskills/dev/SKILL.md
wc -l skill-workspace/subskills/dev/SKILL.md
```

Expected: 看到完整的开发子技能内容，约 300-400 行

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/subskills/dev/SKILL.md
git commit -m "feat: create dev subskill SKILL.md"
```

---

## Task 6: 创建审查子技能 SKILL.md

**Files:**
- Create: `skill-workspace/subskills/review/SKILL.md`

- [ ] **Step 1: 读取现有 skill-review/SKILL.md**

```bash
cat skill-review/SKILL.md
```

- [ ] **Step 2: 创建审查子技能 SKILL.md**

基于 skill-review 内容，创建子技能版本。关键修改：
- 保留完整的审查流程和所有细节
- 更新 references 路径为 `${CLAUDE_SKILL_DIR}/references/`
- 添加 evals 引用

```markdown
---
name: skill-review
description: |
  Skill 审查评分工具。当用户提到"审查skill"、"review skill"、"skill评分"、
  "检查skill质量"时触发。对 Skill 进行 10 维度质量审查，输出评分报告。
argument-hint: "[skill名称或目录路径]"
context: fork
agent: general-purpose
allowed-tools: Read Glob Grep
---

# Skill 审查评分工具

你是 Skill 质量审查专家，精通 Claude Code 官方规范。你的目标是对 Skill 进行全面审查并给出评分报告。

## 核心原则

> **安全第一，客观公正。** 先做安全审查，再做质量评分。审查的目的是帮助改进 Skill，不是挑刺。

## 触发条件

> 触发词已在 description 中定义，此处不重复。

### 模糊匹配
- 任务涉及 Skill 质量改进
- 需要 Skill 规范性检查
- 用户想要 Skill 优化建议

### 不触发条件
- 用户只是询问 Skill 功能（不需要审查）
- 开发新 Skill（应该用 /skill-dev）
- 用户明确表示不需要审查

## 工作流程

### 第一步：安全审查（Security Vetting）

在质量评分前，先做安全审查。发现安全问题直接标记为 BLOCK，不进入评分。

**参考资料：** `${CLAUDE_SKILL_DIR}/references/security.md`

#### 1.1 元数据检查
- [ ] `name` 匹配预期名称（无拼写欺骗）
- [ ] `description` 清晰且与实际行为一致
- [ ] `version` 遵循 semver（可选但建议）

#### 1.2 权限范围分析

| 权限 | 风险 | 说明 |
|------|------|------|
| Read | 🟢 Low | 几乎总是合理 |
| Write | 🟡 Medium | 必须说明写入哪些文件 |
| Bash | 🔴 Critical | 必须说明执行哪些命令 |
| network | 🔴 Critical | 必须说明访问哪些端点 |

**危险组合：** `network` + `shell` 同时出现 → 数据泄露风险，必须 BLOCK。

#### 1.3 内容安全扫描

**🔴 Critical（直接 BLOCK）：**
- 引用 `~/.ssh`、`~/.aws`、`~/.env` 等敏感路径
- 使用 `curl`、`wget`、`nc`、`bash -i` 等网络/反弹命令
- `base64` 混淆内容
- 禁用安全机制的指令
- 未知或可疑 URL

**🟡 Warning（需要人工审查）：**
- `/**/*` 等宽泛通配符
- `sudo` 使用
- 潜在的提示注入

**ℹ️ Info（建议改进）：**
- 缺少 description/version

#### 1.4 拼写欺骗检测

检查以下情况：
- 单字符替换（如 `skil1-review`）
- 同形字符（l/1, O/0, a/а）
- 多余连字符（`skill--review`）
- 与已安装 skill 重名或近似

#### 1.5 安全审查结论

```
安全评级：SAFE / WARNING / DANGER / BLOCK
风险标记：{数量}
建议：install / sandbox first / do not install
```

**如果评级为 BLOCK → 停止，不进入质量评分。**
**如果评级为 WARNING → 继续评分，但在报告中标注安全风险。**

---

### 第二步：定位 Skill

1. **获取路径**
   - 使用 $ARGUMENTS 获取参数
   - 如果参数是目录路径 → 直接使用
   - 如果参数是 skill 名称 → 在以下位置搜索：
     - `~/.claude/skills/<name>/`
     - `.claude/skills/<name>/`
     - 当前工作区目录下的子目录

2. **确认文件存在**
   - 检查 SKILL.md 是否存在
   - 检查目录结构（references/、scripts/、examples/、evals/）

3. **读取内容**
   - 使用 Read 读取 SKILL.md 全文
   - 使用 Glob 列出目录下所有文件
   - 如果有 references/，读取引用的文件列表

### 第三步：10 维度质量评分

**参考资料：** `${CLAUDE_SKILL_DIR}/references/scoring-criteria.md`

#### A 组：规范性审查（6 维度，共 80 分）

| 维度 | 满分 | 检查项 | 优(≥90%) | 良(75-89%) | 中(60-74%) | 差(<60%) |
|------|------|--------|----------|------------|------------|----------|
| A1. 触发 | 20 | description 前250字符含触发词、覆盖常用说法、有不触发条件、不误触发 | 18-20 | 14-17 | 10-13 | 0-9 |
| A2. 结构 | 15 | 目录结构完整、正文≤500行、references/ 按需加载、用 ${CLAUDE_SKILL_DIR} 引用 | 13-15 | 10-12 | 7-9 | 0-6 |
| A3. 上下文 | 15 | fork/inline 选择正确、三层加载合理、消耗可控 | 13-15 | 10-12 | 7-9 | 0-6 |
| A4. 安全性 | 10 | 无敏感信息泄露、无命令注入、最小权限、有危险警告 | 9-10 | 7-8 | 4-6 | 0-3 |
| A5. 可维护性 | 10 | 模块化、有版本管理、有退役条件、个人/团队明确 | 9-10 | 7-8 | 4-6 | 0-3 |
| A6. 测试 | 10 | 有 evals、有边界样例和反例、有验收清单、有弱模型验收 | 9-10 | 7-8 | 4-6 | 0-3 |

#### B 组：实用性打分（4 维度，共 40 分）

| 维度 | 满分 | 检查项 | 优(≥90%) | 良(75-89%) | 中(60-74%) | 差(<60%) |
|------|------|--------|----------|------------|------------|----------|
| B1. 实用性 | 10 | 问题真实存在、有明确场景、比手动高效 | 9-10 | 7-8 | 4-6 | 0-3 |
| B2. 完成度 | 10 | 功能完整、流程无遗漏、输出规范明确、错误处理完善 | 9-10 | 7-8 | 4-6 | 0-3 |
| B3. 易用性 | 10 | 触发简单、参数易懂、输出易读、错误提示友好 | 9-10 | 7-8 | 4-6 | 0-3 |
| B4. 创新性 | 10 | 有独特设计、有创新方案、值得借鉴 | 9-10 | 7-8 | 4-6 | 0-3 |

### 第四步：生成审查报告

按以下格式输出到终端：

```markdown
# Skill 审查报告 — {skill名称}

**审查时间：** {日期}
**Skill 路径：** {路径}
**Skill 版本：** {版本或"未标注"}

---

## 安全审查

```
安全评级：{SAFE / WARNING / DANGER / BLOCK}
风险标记：{数量}
权限范围：{Read / Write / Bash / network}
建议：{install / sandbox first / do not install}
```

{如有安全风险，在此列出具体问题}

---

## 质量评分概览

| 维度 | 得分 | 满分 | 评级 |
|------|------|------|------|
| A1. 触发 | {分} | 20 | {优/良/中/差} |
| A2. 结构 | {分} | 15 | {优/良/中/差} |
| A3. 上下文 | {分} | 15 | {优/良/中/差} |
| A4. 安全性 | {分} | 10 | {优/良/中/差} |
| A5. 可维护性 | {分} | 10 | {优/良/中/差} |
| A6. 测试 | {分} | 10 | {优/良/中/差} |
| B1. 实用性 | {分} | 10 | {优/良/中/差} |
| B2. 完成度 | {分} | 10 | {优/良/中/差} |
| B3. 易用性 | {分} | 10 | {优/良/中/差} |
| B4. 创新性 | {分} | 10 | {优/良/中/差} |
| **总分** | **{分}** | **120** | **{评级}** |

**综合评级：** {强烈推荐/值得一试/仍需改进}

---

## 亮点

1. {亮点1}
2. {亮点2}
3. {亮点3}

## 问题与建议

### 问题 1: {问题标题}
- **维度：** {A1-A6 或 B1-B4}
- **严重程度：** 高/中/低

**问题描述：**
{详细描述}

**改进建议：**
{具体方法}

### 问题 2: {问题标题}
...

---

## 审查统计

| 统计项 | 数值 |
|--------|------|
| 问题总数 | {数量} |
| 高严重度 | {数量} |
| 中严重度 | {数量} |
| 低严重度 | {数量} |

## 总结

{一段话总结审查结论，给出整体评价和优先改进建议}
```

### 测评报告模板

当用户需要对外发布测评（如博客、社区分享）时，使用以下模板：

```markdown
# {skill名称} 测评报告

---

## 测评结论

**{强烈推荐/值得一试/仍需改进}。** {一句话总结核心感受，点明最大亮点和最大短板。}

---

## 测评过程

### 使用路径

​```
{入口路径，如：Claude Code → /skill-review 示例-代码审查skill}
​```

或自然语言触发：
​```
{触发方式，如：帮我审查一下这个 skill 的质量}
​```

### 使用效果（前后对比）

| 维度 | {操作}前 | {操作}后 |
|------|----------|----------|
| {维度1} | {之前状态} | {之后状态} |
| {维度2} | {之前状态} | {之后状态} |
| {维度3} | {之前状态} | {之后状态} |

**实际测试：** {描述一次真实测试的输入和输出}

---

## 测评发现

### 亮点

1. **{亮点1标题}** — {一句话说明}
2. **{亮点2标题}** — {一句话说明}
3. **{亮点3标题}** — {一句话说明}

### 改进建议

| 问题 | 建议 |
|------|------|
| {问题1} | {建议1} |
| {问题2} | {建议2} |
| {问题3} | {建议3} |

---

## 综合打分（5 分制）

| 维度 | 评分 | 说明 |
|------|------|------|
| 实用性 | ⭐⭐⭐⭐⭐ | {说明} |
| 完成度 | ⭐⭐⭐⭐⭐ | {说明} |
| 易用性 | ⭐⭐⭐⭐⭐ | {说明} |
| 创新性 | ⭐⭐⭐⭐⭐ | {说明} |
| **综合** | **⭐⭐⭐⭐⭐** | **{评级}** |

---

**一句话总结：** {最终评价，给潜在用户一个明确建议}
```

## 输入规范

### 必需输入
- **Skill 路径或名称**：从 $ARGUMENTS 获取
  - 目录路径（如 `./my-skill/`）→ 直接使用
  - Skill 名称（如 `code-review`）→ 按优先级搜索：工作区子目录 → `.claude/skills/` → `~/.claude/skills/`

### 可选输入
- 无额外参数时，审查完整 SKILL.md 及其目录结构

### 缺材料时
- 路径不存在 → 停止并提示"Skill 目录不存在，请检查路径"
- SKILL.md 缺失 → 停止并提示"目录下未找到 SKILL.md"
- 内容为空 → 停止并提示"SKILL.md 内容为空，无法审查"

## 参考资料

- 官方规范：`${CLAUDE_SKILL_DIR}/references/official-spec.md`
- 评分标准：`${CLAUDE_SKILL_DIR}/references/scoring-criteria.md`
- 安全检查：`${CLAUDE_SKILL_DIR}/references/security.md`
- 评测集：`${CLAUDE_SKILL_DIR}/evals/evals.json`

## 注意事项

### 必须遵守
- 客观公正：基于事实和规范，不带个人偏好
- 具体明确：指出具体行号和代码
- 建设性：提供改进建议，不只是批评
- 对照规范：每条建议必须引用官方规范或知识库条目

### 禁止行为
- 人身攻击
- 模糊的批评（如"这个 skill 不好"）
- 忽略上下文（不考虑 skill 的设计意图）
- 无依据打分（每个分数必须有对应检查项支撑）

## 示例

### 输入示例
```
/skill-review code-review
```

### 期望输出
审查报告，包含 10 维度评分、亮点、问题与建议、综合评级。

### 反例：不该触发的情况
- 用户说"帮我开发一个 skill" → 应该用 /skill-dev，不是审查
- 用户说"这个 skill 怎么用" → 询问功能，不是审查
- 用户说"帮我看看这段代码" → 代码审查，不是 skill 审查

## 失败处理

| 失败类型 | 修复动作 |
|----------|----------|
| 路径错误 | 提示检查路径，列出已知 skill |
| 文件缺失 | 提示目录结构不完整 |
| 解析失败 | 标记为结构问题，继续审查正文 |
| 评分争议 | 提供检查项依据，允许用户调整 |

**连续失败 3 次应停下来问用户。**

## Gotchas

### G1: 看起来像但不该触发
- 用户说"帮我看看这个 skill"可能是在问功能，不是要审查
- 判断依据：是否提到"质量"、"评分"、"规范"等关键词

### G2: 评分必须有依据
- 不能凭感觉打分，每个分数必须对应具体检查项
- 如果某个维度无法判断，标记为"未评估"而非随意给分

### G3: 参考资料可能不存在
- references/ 目录下的文件可能缺失
- 缺失时跳过该维度的深度检查，但要在报告中标注

## 弱模型验收

用更便宜的模型（如 haiku）测试此 Skill，验证：
- 能否正确解析 frontmatter
- 能否按 10 维度逐项打分
- 输出格式是否一致
- 是否遗漏关键检查项

如果弱模型也能稳定输出合格报告，说明评分规则足够明确。
```

- [ ] **Step 3: 验证文件创建**

```bash
head -50 skill-workspace/subskills/review/SKILL.md
wc -l skill-workspace/subskills/review/SKILL.md
```

Expected: 看到完整的审查子技能内容，约 300-400 行

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/subskills/review/SKILL.md
git commit -m "feat: create review subskill SKILL.md"
```

---

## Task 7: 重写主技能 SKILL.md

**Files:**
- Modify: `skill-workspace/SKILL.md`

- [ ] **Step 1: 读取现有 skill-workspace/SKILL.md**

```bash
cat skill-workspace/SKILL.md
```

- [ ] **Step 2: 重写主技能 SKILL.md**

创建新的主入口，整合所有子命令和子技能路由：

```markdown
---
name: skill-workspace
description: |
  Skill 全生命周期工作台。当用户提到"开发skill"、"创建skill"、"审查skill"、
  "review skill"、"skill评分"、"搜索skill"、"下载skill"、"优化skill"、
  "部署skill"、"管理skill"时触发。一站式完成 Skill 的搜索、下载、安全审查、
  开发生成、优化改进、质量测评、部署上线、更新卸载。
argument-hint: "[子命令] [参数]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob Grep Bash WebFetch
---

# Skill 全生命周期工作台

一站式 Skill 管理平台，覆盖 Skill 从发现到退役的完整生命周期。

## 核心原则

> **先搜再写，不造轮子。** 开发前必须搜索，下载前必做安全审查。

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

**目标：** 在线查找用户需要的 Skill，避免重复造轮子。

**搜索优先级：**

1. **CocoLoop API**（最优先）
   ```bash
   curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"
   ```

2. **GitHub 搜索**（API 失败时）
   ```bash
   curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"
   ```

3. **clawhub 搜索**（兜底）
   ```bash
   npx clawhub@latest search {关键词}
   ```

**输出格式：**
```
📋 搜索结果:
  1. skill-name (⭐ 下载量/星数)
     📝 描述文本
     👤 作者 | v1.0.0
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
   cp -r {skill目录}/ ~/.claude/skills/{skill名}/
   ```

4. **确认安装结果**

---

## 流程三：安全审查

**目标：** 对 Skill 进行安全扫描，识别风险。

**快速检查清单：**

1. **元数据检查**
   - [ ] name 无拼写欺骗
   - [ ] description 与实际行为一致

2. **权限分析**
   - [ ] Read/Write/Bash/network 权限是否合理
   - [ ] 有无危险组合（network + shell）

3. **内容扫描**
   - 🔴 BLOCK：引用敏感路径、使用 curl/wget/nc、base64 混淆
   - 🟡 WARNING：宽泛通配符、sudo 使用
   - ℹ️ INFO：缺少 description/version

**输出：**
```
安全评级：SAFE / WARNING / DANGER / BLOCK
风险标记：{数量}
建议：install / sandbox first / do not install
```

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
   cp -r "./{skill名}/" ~/.claude/skills/{skill名}/
   ```
4. **验证部署**
   ```bash
   ls ~/.claude/skills/{skill名}/
   ```
5. **测试全局可用** — `claude -p "使用 {name} 完成 XXX"`

**⚠️ 永远用 `cp`，不用 `mv`，保留源文件。**

---

## 流程六：管理

**目标：** 管理已安装的 Skill。

### 列出已安装 Skill
```bash
ls ~/.claude/skills/
ls ./
```

### 更新 Skill
1. 查询最新版本（CocoLoop API 或 GitHub）
2. 比较本地版本与远程版本
3. 有更新 → 备份旧版 → 下载新版 → 安全审查 → 安装

### 卸载 Skill
1. 确认 skill 存在
2. 询问用户确认
3. 删除 skill 目录
4. 清理相关配置

---

## 参考资料

- 开发规范：`${CLAUDE_SKILL_DIR}/references/optimize.md`
- 部署指南：`${CLAUDE_SKILL_DIR}/references/deploy.md`

## 注意事项

### 必须遵守
- 下载前必须做安全审查
- 部署前建议做质量测评
- 永远用 cp 不用 mv
- 用 AskUserQuestion 与用户交互

### 禁止行为
- 跳过安全审查直接安装
- 未测试就部署到全局
- 覆盖用户未确认的文件
- 静默执行危险操作

## 示例

### 搜索并安装
```
用户: 帮我找个代码格式化的 skill
→ 搜索流程 → 展示结果 → 用户选择 → 安全审查 → 安装
```

### 从零开发
```
用户: 帮我开发一个代码审查 skill
→ 加载 dev 子技能 → 需求分析 → 生成 SKILL.md → 测试
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

- [ ] **Step 3: 验证主技能**

```bash
head -50 skill-workspace/SKILL.md
wc -l skill-workspace/SKILL.md
```

Expected: 看到整合后的主技能内容，约 200-300 行

- [ ] **Step 4: Commit**

```bash
git add skill-workspace/SKILL.md
git commit -m "feat: rewrite main skill with subskill routing"
```

---

## Task 8: 清理共享 references 目录

**Files:**
- Remove: `skill-workspace/references/dev.md`（已迁移到 subskills/dev/references/）
- Remove: `skill-workspace/references/review.md`（已迁移到 subskills/review/references/）
- Remove: `skill-workspace/references/security.md`（已迁移到 subskills/review/references/）
- Remove: `skill-workspace/references/official-spec.md`（已迁移到子技能）
- Keep: `skill-workspace/references/optimize.md`（共享）
- Keep: `skill-workspace/references/deploy.md`（共享）

- [ ] **Step 1: 删除已迁移的 references**

```bash
cd "D:/ai/claude code/skill开发"
rm -f skill-workspace/references/dev.md
rm -f skill-workspace/references/review.md
rm -f skill-workspace/references/security.md
rm -f skill-workspace/references/official-spec.md
```

- [ ] **Step 2: 验证 references 目录**

```bash
ls -la skill-workspace/references/
```

Expected: 只剩下 optimize.md 和 deploy.md

- [ ] **Step 3: Commit**

```bash
git add skill-workspace/references/
git commit -m "refactor: clean up shared references, keep only optimize and deploy"
```

---

## Task 9: 更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 读取现有 README.md**

```bash
cat README.md
```

- [ ] **Step 2: 更新 README.md**

更新目录结构和使用说明：

```markdown
# Skill 全生命周期工作台

一站式完成 Skill 的 **搜索 → 下载 → 安全审查 → 开发 → 优化 → 测评 → 部署 → 管理**。

## 目录结构

```
skill-workspace/
├── SKILL.md                    # 主入口：路由到子技能
├── README.md                   # 使用说明
├── subskills/
│   ├── dev/                    # 开发子技能（完整包）
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── official-spec.md
│   │   │   ├── template.md
│   │   │   ├── example.md
│   │   │   └── methodology.md
│   │   └── evals/
│   │       └── evals.json
│   └── review/                 # 审查子技能（完整包）
│       ├── SKILL.md
│       ├── references/
│       │   ├── official-spec.md
│       │   ├── scoring-criteria.md
│       │   └── security.md
│       └── evals/
│           ├── evals.json
│           └── test-cases.json
├── references/                 # 共享参考资料
│   ├── optimize.md
│   └── deploy.md
└── evals/
    └── evals.json              # 主技能评测集
```

## 使用方式

### 统一入口

```
/skill-workspace 开发 代码格式化     → 加载 dev 子技能
/skill-workspace 审查 my-skill       → 加载 review 子技能
/skill-workspace 搜索 代码格式化     → 在线搜索 skill
/skill-workspace 下载 pdf-processor  → 下载安装 skill
/skill-workspace 优化 my-skill       → 改进现有 skill
/skill-workspace 部署 my-skill       → 安装到全局
/skill-workspace 管理                → 列出/更新/卸载
```

### 也可以自然语言触发

```
"帮我开发一个代码审查 skill"        → 自动走开发流程
"审查一下这个 skill 的质量"         → 自动走审查流程
"帮我找个代码格式化的 skill"        → 自动走搜索流程
```

## 子技能

### 开发子技能 (dev)

帮助用户开发符合官方规范的 Skill。核心功能：
- 前置判断：是否值得 Skill 化
- 三条路径：找现成的 / 改造现成的 / 从零写
- 完整开发流程：需求分析 → 生成 SKILL.md → 测试 → 部署

**参考资料：**
- 官方规范：`subskills/dev/references/official-spec.md`
- 模板文件：`subskills/dev/references/template.md`
- 示例文件：`subskills/dev/references/example.md`
- 实战方法论：`subskills/dev/references/methodology.md`

### 审查子技能 (review)

对 Skill 进行 10 维度质量审查。核心功能：
- 安全审查：元数据检查、权限分析、内容扫描
- 质量评分：A 组规范性（80 分）+ B 组实用性（40 分）
- 审查报告：评分表格 + 亮点 + 问题与建议

**参考资料：**
- 官方规范：`subskills/review/references/official-spec.md`
- 评分标准：`subskills/review/references/scoring-criteria.md`
- 安全检查：`subskills/review/references/security.md`

## 完整工作流

```
需求 → 搜索 → 找到？ → 安全审查 → 下载 → 优化 → 测评 → 部署
         ↓ 没找到
       开发 → 测评 → 部署
```

## 参考资料

- 优化方法：`references/optimize.md`
- 部署指南：`references/deploy.md`
```

- [ ] **Step 3: 验证 README**

```bash
cat README.md
```

Expected: 看到更新后的目录结构和使用说明

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README with new structure"
```

---

## Task 10: 最终验证

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

- [ ] **Step 3: 验证子技能 references 完整性**

```bash
# 开发子技能
ls -la skill-workspace/subskills/dev/references/
wc -l skill-workspace/subskills/dev/references/*.md

# 审查子技能
ls -la skill-workspace/subskills/review/references/
wc -l skill-workspace/subskills/review/references/*.md
```

Expected: 每个子技能都有完整的 references

- [ ] **Step 4: 验证子技能 evals 完整性**

```bash
# 开发子技能
ls -la skill-workspace/subskills/dev/evals/
cat skill-workspace/subskills/dev/evals/evals.json | jq .

# 审查子技能
ls -la skill-workspace/subskills/review/evals/
cat skill-workspace/subskills/review/evals/evals.json | jq .
```

Expected: 每个子技能都有 evals 文件

- [ ] **Step 5: 最终 Commit**

```bash
git add -A
git commit -m "feat: complete skill-workspace integration with full subskill packages"
```

---

## 完成

实施计划完成。所有任务执行完毕后，skill-workspace 将成为一个完整的 Skill 开发工作台：

1. **主技能** - 统一入口，路由到子技能
2. **开发子技能** - 完整的包，有自己的 references 和 evals
3. **审查子技能** - 完整的包，有自己的 references 和 evals
4. **共享参考资料** - optimize.md 和 deploy.md

每个子技能都是**独立完整的包**，可单独部署到 `~/.claude/skills/`。

**下一步：** 选择执行方式：
1. **Subagent-Driven（推荐）** - 每个 Task 一个子代理，任务间审查
2. **Inline Execution** - 在当前会话中执行，批量处理

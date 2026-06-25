---
name: super-frontend-design
version: 2.1.0
description: |
  前端设计全流程工作台。从灵感到交付一站式完成。集成需求调研、生成艺术、UI/UX设计、主题系统、设计审查五大模块。
  v2.0.0: 精确反AI规则集(14条) · 结构化DESIGN.md(9-section) · Typography硬规则 · Block分类目录(18类型) · 动效扩展(Aceternity+Inspira) · MCP集成指南 · 5框架Prompt模板 · 品牌人格扩展(8→14)
  v2.1.0: 企业设计系统参考目录(60+国际品牌+17中国品牌·VoltAgent/awesome-design-md+alexpate/awesome-design-systems集成)
  **此 Skill 为子代理型 Skill，必须通过 Task 工具调用（subagent_type: skill_agent_super-frontend-design），不能直接使用 Skill 工具。**
  触发词：设计、UI、UX、前端、落地页、海报、艺术、品牌、主题、优化界面、视觉、组件、dashboard、
  landing page、生成艺术、算法艺术、p5.js、创意设计、配色、字体、审查UI、设计评分、搜索设计参考、后端页面设计。
  子命令：research（需求调研+全网搜索）、creative（生成艺术+海报）、design（UI/UX设计）、theme（主题+品牌）、review（基于impeccable的设计审查）。
  工作流：research → creative → theme → design → review
  每个阶段结束后自动触发 review（impeccable）审查，形成质量闭环。
  **区别于其他前端 Skill：** 本 Skill 提供完整五阶段工作流，强调「先调研再设计」「去AI味」「设计灵魂（品牌人格+情绪板）」。
  当你需要「从零完整设计一个前端项目（含需求调研+视觉方向+主题+代码+审查）」→ 用本 Skill；
  当你只需要「快速设计一个单页面」→ 用 frontend-design；
  当你需要「从零构建完整项目（含PRD文档）」→ 用 web-dev；
  当你只需要「查询设计数据（色板/字体/风格）」→ 用 ui-ux-pro-max。
context: fork
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# Super Frontend Design — 前端设计全流程工作台

## 0. 调用方式

> ⚠️ **重要：本 Skill 是子代理型 Skill，不能直接通过 Skill 工具调用！**

### 正确调用方式

必须通过 **Task 工具** 启动：

```
subagent_type: skill_agent_super-frontend-design
```

### 调用示例

当用户说「帮我设计一个 landing page」时，Agent 应执行：

```
Task(
  subagent_type="skill_agent_super-frontend-design",
  query="用户需要设计一个 landing page...",
  description="前端设计"
)
```

### 如果误用 Skill 工具调用

会收到错误提示：`"Skill 'super-frontend-design' runs as a sub-agent task and should be invoked via the Task tool, not the Skill tool."`。此时应改用 Task 工具重新调用。

### 何时使用本 Skill vs 其他前端 Skill

| 场景 | 推荐 Skill | 原因 |
|------|-----------|------|
| 从零完整设计前端项目（含调研+方向+主题+代码+审查） | **super-frontend-design**（本 Skill） | 唯一提供完整五阶段工作流的 Skill，强调「先调研再设计」「去AI味」「设计灵魂」 |
| 快速设计一个单页面/组件 | `frontend-design` | 更轻量，不需要完整调研和审查流程 |
| 从零构建完整项目（含 PRD 技术文档） | `web-dev` | 强调项目规划文档，输出结构化工程方案 |
| 查询设计数据（色板/字体/风格/UX准则） | `ui-ux-pro-max` | 设计数据库查询，不需要完整设计流程 |
| 审查现有设计 | 直接用本 Skill 的 `review` 子命令 | 不需要完整工作流，只走审查通道 |
| 生成算法艺术作品/海报 | 直接用本 Skill 的 `creative` 子命令 | 不需要完整工作流，只走创意通道 |

### 适用场景（正例 ✅）

- "帮我设计一个 SaaS 产品官网"
- "从零开始设计一个后台管理系统"
- "帮我做一个完整的品牌落地页，要有调研、视觉方向、设计实现"
- "我有个产品想法，帮我从头设计它的前端界面"
- "帮我设计 dashboard，我想先看看竞品参考"

### 不适用场景（反例 ❌）

- "给这个按钮换个颜色" → 直接用代码修改，不需要设计 Skill
- "帮我查一下有什么好看的配色方案" → 用 `ui-ux-pro-max` 查数据
- "写一个 React 组件的代码" → 直接编码，不需要设计流程
- "审查一下这个页面的可访问性" → 可直接用本 Skill 的 review 子命令，但不需要完整五阶段
- "有没有好看的字体搭配推荐" → 用 `ui-ux-pro-max` 查询

---

## 1. 概述

### 定位

前端设计全流程工作台——从灵感到交付一站式完成。将分散的设计能力整合为一条完整工作流，确保设计方向一致、视觉系统统一、输出质量可控。

**核心改进**：在设计执行前强制进行需求调研，避免"开盲盒"式设计；集成全网搜索能力，突破内置框架限制；搜索结果经过综合优化，融合多源参考优点。

### 合并来源

本 Skill 由以下 10 个原有 Skill 合并而成：

| 原 Skill | 核心能力 | 归入模块 |
|----------|----------|----------|
| creative-art | 生成艺术、p5.js 交互式作品 | creative |
| canvas-design | 博物馆级海报、PDF/PNG 静态输出 | creative |
| algorithmic-art | 算法艺术、flow field、粒子系统 | creative |
| frontend-design | 高设计质量前端界面 | design |
| frontend-skill | 落地页、视觉方向、构图动效 | design |
| frontend-ui | 综合前端设计智能 | design |
| ui-ux-pro-max | 50+ 风格、161 色板、57 字体对、99 UX 准则 | design + theme |
| brand-guidelines | 品牌色彩、排版规范 | theme |
| theme-factory | 10 预设主题、主题工具包 | theme |
| impeccable | 设计审查、优化、打磨（14 维度） | review |
| web-design-guidelines | Web Interface Guidelines 合规性审查 | review |

### 核心理念

**方向先行、需求驱动、跨领域借鉴、审查闭环**

- **方向先行**：先确定视觉方向再执行，避免"安全平均"的 UI
- **需求驱动**：设计前必须完成需求调研，明确目标、受众、功能、交互、风格偏好，拒绝"开盲盒"
- **跨领域借鉴**：设计灵感不限于 UI 领域，从建筑、时尚、工业设计、自然、电影、音乐等领域获取灵感
- **审查闭环**：每个环节可触发审查，形成质量闭环

---

## 2. 子命令路由

| 子命令 | 触发词 | 加载路径 | 核心功能 |
|--------|--------|----------|----------|
| research | 需求调研、设计参考、搜索灵感、后端页面、找参考、设计方向 | 主入口直接处理 | 需求调研对话 + 全网搜索设计参考 + 参考解构优化 |
| creative | 生成艺术、海报、p5.js、算法艺术、视觉设计、flow field、粒子系统 | subskills/creative/SKILL.md | 哲学宣言→视觉表达，p5.js 交互式 + PDF/PNG 静态 |
| design | 设计页面、UI、组件、landing page、dashboard、app、前端 | subskills/design/SKILL.md | 方向选择→视觉系统→构图→动效→代码实现 |
| theme | 配色、字体、主题、品牌色、dark mode、调色板 | subskills/theme/SKILL.md | 10 预设主题 + 自定义 + 品牌规范，Design Token 输出 |
| review | 审查UI、设计评分、优化界面、UX检查、可访问性 | subskills/review/SKILL.md | 可访问性 + 一致性 + 性能 + 视觉质量审查 |

### 路由规则

根据用户输入的关键词自动路由到对应子命令：

- 用户提到 **"需求调研" / "设计参考" / "搜索灵感" / "找参考" / "后端页面" / "设计方向"** → `research`
- 用户提到 **"生成艺术" / "算法艺术" / "p5.js" / "交互" / "粒子" / "flow field"** → `creative`
- 用户提到 **"海报" / "设计" / "PDF" / "PNG" / "海报设计" / "视觉设计"** 且不涉及网页 UI → `creative`
- 用户提到 **"设计页面" / "UI" / "组件" / "landing page" / "dashboard" / "app"** → `design`（如未明确需求，先触发 `research` 需求调研）
- 用户提到 **"配色" / "字体" / "主题" / "品牌色" / "dark mode" / "调色板"** → `theme`
- 用户提到 **"审查UI" / "设计评分" / "优化界面" / "UX检查"** → `review`
- 用户未明确指定 → **先触发 `research` 需求调研**，通过对话明确需求后再路由

### 路由 Fallback 机制

路由失败或不确定时的降级策略（按优先级）：

| Fallback 层级 | 条件 | 行为 |
|:---:|---|---|
| **L1 · 用户确认** | 无法确定意图 | 使用 AskUserQuestion 询问用户意图，给出 2-3 个最可能的路由选项 |
| **L2 · 安全降级** | 用户模糊回答（"都行"/"随便"） | 自动路由到 `research`，通过需求调研对话澄清 |
| **L3 · 默认工作流** | 完全无法判断（极少数情况） | 启动完整五阶段工作流 `research → creative → theme → design → review`，每个阶段结束时让用户确认是否继续 |
| **L4 · 优雅退出** | 子代理执行失败或超时 | 输出已完成的阶段成果 + 未完成阶段的待办清单 + 「请重新调用 Task 工具继续」提示 |

### 路由决策树

```
用户输入
  ├── 明确关键词匹配 → 直接路由到对应子命令
  ├── 部分匹配（如只说"设计"但无上下文） → L1: 询问用户意图
  │     ├── 用户明确选择 → 路由到指定子命令
  │     └── 用户模糊回答 → L2: 降级到 research
  ├── 无关键词匹配 → L1: 询问用户意图
  │     ├── 用户明确选择 → 路由到指定子命令
  │     └── 用户模糊回答 → L2: 降级到 research
  └── 完全无法判断 → L3: 启动完整工作流
```

### 路由冲突解决

当用户输入匹配多个子命令时（如"帮我设计一个配色的主题页面"同时匹配 design/theme），按以下优先级：

1. **优先选择最具体的子命令**（theme > design，因为用户明确提到"配色"）
2. 如仍冲突 → 询问用户确认
3. 如用户选择完整流程 → 按工作流顺序串联执行

---

## 3. 工作流模式

### 完整工作流（新项目）

当用户需要从零开始设计一个完整的前端项目时，按以下顺序执行：

```
research（需求调研+参考搜索）→ creative（灵感探索）→ theme（确定主题/配色）→ design（设计实现）→ review（审查优化）
```

**详细流程：**

0. **research 阶段**：需求调研对话 + 全网搜索设计参考（Phase 0，不可跳过）
   - 输入：用户的初步需求描述（可能模糊、不完整）
   - 调研内容：见下方「Phase 0 需求调研」章节
   - 搜索内容：当内置参考不足时，全网搜索设计灵感和最佳实践
   - 输出：结构化需求简报（Design Brief）+ 设计参考集合
   - **→ 完成后触发 review 检查：Design Brief 是否完整？企业参考是否合理？**

1. **creative 阶段**：探索视觉方向，生成灵感草图或交互原型
   - 输入：需求简报 + 设计参考集合
   - 输出：视觉方向 + 设计哲学宣言
   - **→ 完成后触发 review 检查：视觉方向是否与需求简报一致？是否有 AI 味？**

2. **theme 阶段**：基于视觉方向确定主题系统
   - 输入：creative 阶段的视觉方向 + 需求简报中的品牌/风格偏好
   - 输出：Design Token 系统（CSS 变量完整定义）
   - **→ 完成后触发 review 检查：Token 是否完整？对比度是否达标？**

3. **design 阶段**：基于主题系统实现前端代码
   - 输入：Design Token 系统 + 需求简报中的功能需求 + 设计参考集合 + 视觉论文
   - 输出：可运行的前端代码（HTML/CSS/JS 或框架代码）
   - **→ 完成后触发 review 检查：反 AI 味检查清单是否全部通过？设计灵魂是否体现？**

4. **review 阶段**：最终设计审查，输出改进建议
   - 输入：前端代码 + Design Token 系统 + 需求简报 + 视觉论文
   - 输出：审查报告 + 具体改进建议
   - **→ 基于 impeccable 的 15 维度审查，包含去 AI 味专项检查 + 设计灵魂追溯检查**

### 快速通道（单一任务）

当用户只需要某个模块的能力时，直接路由到对应子命令，无需走完整五阶段流程：

- 只需要搜索设计参考 → `research`（不启动完整工作流）
- 只需要生成艺术作品 → `creative`
- 只需要调整配色/主题 → `theme`
- 只需要审查现有设计 → `review`

> ⚠️ **快速通道 ≠ 跳过调研**。路由到 `design` 子命令时，如当前会话中没有已完成的有效 Design Brief，仍必须先完成至少 **最小化调研**（设计类型 + 页面场景 + 核心目标），禁止用全局画像/历史偏好替代。

**所谓「需求已经很明确」的判断标准（全部满足才可跳过完整调研）：**
1. 用户在本**当前会话**中已经通过 AskUserQuestion 完成过一轮调研
2. 用户明确说"就用刚才调研的结果，再做一个类似页面"
3. 设计类型/场景未发生变化（如两次都是后台管理页面）

**不满足以上任一条件 → 必须启动调研对话。**

### 子命令串联

当用户需要完整流程时，按顺序执行子命令，每个子命令的输出作为下一个的输入：

| 阶段 | 输入 | 输出 |
|------|------|------|
| research | 用户初步需求（可能模糊） | 需求简报 + 设计参考集合 |
| creative | 需求简报 + 设计参考 | 视觉方向 + 设计哲学 |
| theme | 视觉方向 + 品牌/风格偏好 | Design Token 系统（CSS 变量） |
| design | Design Token + 功能需求 + 设计参考 | 可运行的前端代码 |
| review | 前端代码 + Design Token + 需求简报 | 审查报告 + 改进建议 |

---

## 3.5. Phase 0 需求调研（research 子命令）

### 目标

在任何设计执行前，通过 **AskUserQuestion 工具** 进行结构化对话，明确用户的真实需求，避免"开盲盒"式设计。

### 核心要求（铁律）

> ⚠️ **以下为硬性规则，违反即视为 Skill 执行失败：**

**铁律 1**：每次新设计任务，必须使用 AskUserQuestion 工具与用户进行交互式对话，**不允许跳过此步骤**。
**铁律 2**：**绝对禁止**自己假设用户需求，**绝对禁止**用以下任何来源替代本次调研对话：
  - ❌ 用户的全局画像（user profile）
  - ❌ 用户的历史偏好记录（past preferences / global memory / ontology）
  - ❌ 用户在其他会话中表达过的风格喜好
  - ❌ 用户在其他项目中使用过的配色方案
  - ❌ 任何跨会话持久化的用户数据
**铁律 3**：即使用户说"和上次一样"，也必须至少重新确认**设计类型/场景**和**当前项目的具体需求**，因为同一用户对不同项目（后台 vs 前台 vs 落地页 vs App）的设计需求截然不同。
**铁律 4**：调研对话中必须首先询问**设计场景**（后台管理 / 宣传落地页 / 移动端 App / 数据 Dashboard 等），不同场景对应相反的配色策略、字体选择、动效需求、组件密度。

### 对话执行流程

调研对话分为 **3 轮**，每轮使用 AskUserQuestion 工具提出 2-4 个问题：

---

#### 第 1 轮：设计类型 + 企业参考

**必须提出的问题（使用 AskUserQuestion）：**

**问题 1 — 设计类型与目标：**
```
header: "设计类型"
question: "这个设计是面向什么场景的？"
options:
  - "产品官网 / Landing Page" → 品牌展示、转化率优先
  - "后台管理系统 / Dashboard" → 数据密集、操作效率优先
  - "移动端 App 界面" → 触摸交互、移动优先
  - "营销活动页 / H5" → 视觉冲击、转化导向
  - "内部工具 / 企业应用" → 功能优先、效率导向
  - "其他（请描述）"
multiSelect: false
```

**问题 2 — 企业参考风格：**
```
header: "企业参考"
question: "有没有喜欢的大企业产品界面风格？没有的话我可以根据你的场景推荐。"
options:
  - "Apple 风格" → 极致简洁、大留白、SF字体感、毛玻璃效果
  - "Stripe 风格" → 渐变色彩、精致微交互、开发者友好
  - "Linear 风格" → 暗色为主、极简线条、键盘快捷键感
  - "Vercel 风格" → 几何感、黑白对比、科技极简
  - "Notion 风格" → 轻量干净、功能即设计、emoji点缀
  - "GitHub 风格" → 开发者审美、深色主题、等宽字体
  - "Airbnb 风格" → 温暖友好、大图排版、圆角柔和
  - "Figma 风格" → 设计工具感、暗色界面、高对比工具栏
  - "Tailwind UI 风格" → 实用主义、组件化、高可读性
  - "不需要参考，自由发挥"
multiSelect: false
```

**问题 3 — 目标受众（可选，但建议问）：**
```
header: "目标受众"
question: "主要面向什么用户群体？"
options:
  - "开发者 / 技术人群"
  - "企业客户 / B2B"
  - "普通消费者 / C端"
  - "内部员工"
  - "不限"
multiSelect: true
```

**第 1 轮结束后，根据用户选择的企业参考，自动加载对应的设计特征，在 Design Brief 中记录。**

---

#### 第 2 轮：风格 + 配色 + 暗色模式

**问题 4 — 风格偏好：**
```
header: "风格偏好"
question: "偏好什么视觉风格？"
options:
  - "极简主义" → 大量留白、克制的色彩、精准排版
  - "科技 / 未来感" → 深色背景、霓虹点缀、几何线条
  - "活泼 / 趣味" → 圆润形状、明亮色彩、微交互
  - "专业 / 商务" → 稳重配色、清晰层次、正式感
  - "温暖 / 有机" → 暖色调、自然曲线、亲和力
  - "奢华 / 高端" → 暗色+金色、精致细节、优雅过渡
  - "不确定，推荐一个"
multiSelect: false
```

**问题 5 — 暗色模式：**
```
header: "暗色模式"
question: "是否需要暗色模式？"
options:
  - "需要（同时支持亮色和暗色）"
  - "只要暗色模式"
  - "只要亮色模式"
  - "不确定"
multiSelect: false
```

---

#### 第 3 轮：技术栈 + 响应式 + 交互

**问题 6 — 技术栈：**
```
header: "技术栈"
question: "使用什么技术栈实现？"
options:
  - "纯 HTML/CSS/JS（无框架）"
  - "React + Tailwind CSS"
  - "Vue + Tailwind CSS"
  - "React + shadcn/ui"
  - "不需要代码，只要设计稿/描述"
  - "其他（请描述）"
multiSelect: false
```

**问题 7 — 响应式需求：**
```
header: "响应式"
question: "需要适配哪些设备？"
options:
  - "桌面端为主"
  - "移动端为主"
  - "桌面 + 平板 + 手机全适配"
  - "不确定"
multiSelect: false
```

**问题 8 — 交互复杂度：**
```
header: "交互需求"
question: "需要什么程度的交互？"
options:
  - "纯静态展示" → 只需好看的界面
  - "基础交互" → 表单、按钮、导航
  - "中等交互" → 搜索、筛选、Tab切换、模态框
  - "复杂交互" → 拖拽、实时数据、富文本编辑
  - "完整应用" → 路由、状态管理、API对接
multiSelect: false
```

---

#### 第 4 轮：品牌人格 + 情绪板 + 设计禁忌（决定设计灵魂）

**问题 9 — 品牌人格（最重要）：**
```
header: "品牌人格"
question: "如果这个品牌/产品是一个人，TA 是什么性格？"
options:
  - "极客工程师" → 技术硬核、等宽字体、暗色、代码感、工具优先
  - "优雅艺术家" → 精致细节、衬线字体、大量留白、材质感、慢节奏
  - "活力创业者" → 明亮色彩、圆润形状、大标题、行动导向、快速感
  - "权威专家" → 稳重配色、紧凑排版、数据密集、专业术语、可信感
  - "温暖朋友" → 暖色调、友好圆角、手写感、轻松文案、亲和力
  - "叛逆先锋" → 粗野主义、高对比、打破规则、实验性、冲击力
  - "极简主义者" → 黑白为主、极致留白、单一字体、克制、安静
  - "不确定，由你推荐"
multiSelect: false
```

**问题 10 — 情绪板（用 3 个词）：**
```
header: "情绪板"
question: "用 3 个词描述你想要的设计感觉？"
options:
  - "不，我想自己描述" → 用户输入 3 个词
  - "科技感 + 未来感 + 冷静"
  - "温暖 + 有机 + 自然"
  - "大胆 + 冲击 + 力量"
  - "优雅 + 精致 + 安静"
  - " playful + 趣味 + 轻松"
  - "粗野 +  raw + 真实"
  - "复古 + 怀旧 + 温暖"
  - "不确定"
multiSelect: false
```

**问题 11 — 设计禁忌（绝对不能出现）：**
```
header: "设计禁忌"
question: "有什么绝对不能出现在设计中的元素？"
options:
  - "不，没有禁忌" → 无限制
  - "绝对不能有蓝紫渐变" → 禁止蓝紫渐变
  - "绝对不能有emoji图标" → 禁止emoji作为图标
  - "绝对不能有灰底白卡" → 禁止灰色背景+白色卡片
  - "绝对不能有圆角卡片堆砌" → 禁止卡片网格布局
  - "绝对不能有居中大标题Hero" → 禁止标准Hero模板
  - "绝对不能有玻璃拟态" → 禁止毛玻璃效果
  - "绝对不能有新拟态" → 禁止neumorphism
  - "我想自定义禁忌" → 用户输入
multiSelect: true
```

**问题 12 — 竞品拆解（关键）：**
```
header: "竞品拆解"
question: "有没有竞品/参考网站，你特别喜欢它的哪一点？"
options:
  - "不，没有具体参考" → 无参考
  - "喜欢它的配色方案" → 提取配色方向
  - "喜欢它的排版方式" → 提取排版方向
  - "喜欢它的动效" → 提取动效方向
  - "喜欢它的整体氛围" → 提取氛围方向
  - "我可以提供链接" → 用户发送链接，进行解构分析
  - "我想上传截图" → 用户上传截图
multiSelect: true
```

---

### 对话执行规则

1. **每次使用 AskUserQuestion 工具**，最多 4 个问题，优先第 1-2 轮
2. **用户回答后**，根据回答内容追问或进入下一轮
3. **如果用户跳过某个问题**，使用默认值（记录在 Design Brief 中标记为"默认假设"）
4. **如果用户说"随便"、"都行"、"你推荐"** → 基于设计类型自动推荐最佳方案
5. **每轮对话结束后**，简要总结用户的选择，确认理解无误
6. **第 4 轮（品牌人格）不可跳过**：这是决定设计灵魂的关键轮次，必须收集至少品牌人格和情绪板

### 快捷模式（严格限制）

以下情况允许精简调研，但**永远不能完全跳过**：

| 情况 | 最少必须询问 | 禁止行为 |
|------|-------------|---------|
| 用户说"需求很清楚，直接开始" | 至少第 1 轮（设计类型 + 企业参考） + 第 4 轮（品牌人格） | 禁止从全局画像/历史偏好中提取答案 |
| 用户说"和上次一样" | 至少确认「设计类型是否相同」+「有没有新的特殊需求」 | 禁止假设场景不变 |
| 同一会话内连续第二个任务 | 可跳过第 1-3 轮，但第 4 轮（品牌人格+情绪板+设计禁忌）**必须重新确认** | 同一个用户做后台和做落地页的品牌人格可能完全不同 |

**任何精简模式下**：
- 所有未询问的维度必须在 Design Brief 中标记为 `[默认假设]`
- 在执行前向用户展示所有默认假设并请求确认
- 绝对禁止从用户的全局画像、历史记忆、ontology 等任何持久化数据中提取设计偏好来填充答案

### 调研输出：Design Brief（需求简报）

完成调研后，输出结构化的需求简报：

```markdown
# Design Brief — {项目名称}

## 基本信息
- 设计类型：{官网/后台/App/落地页/内部工具}
- 核心目标：{一句话描述}
- 目标受众：{用户画像}

## 企业参考
- 参考风格：{Apple/Stripe/Linear/Vercel/Notion/...}
- 参考特征：{对应的设计特征描述}
- 参考原因：{为什么选择这个参考}

## 功能需求
- 核心页面/区块：{列表}
- 关键功能：{列表}
- 数据来源：{API/静态/用户输入}

## 交互需求
- 交互类型：{展示/表单/实时/拖拽/完整应用}
- 动效需求：{微交互/页面转场/加载动画/无}
- 响应式：{桌面/平板/手机/全适配}

## 风格系统
- 视觉风格：{极简/科技/活泼/专业/...}
- 暗色模式：{需要/不需要/仅暗色}
- 品牌色：{色值或描述}
- 排除风格：{不要什么}

## 设计灵魂（第4轮产出）
- 品牌人格：{极客工程师/优雅艺术家/活力创业者/权威专家/温暖朋友/叛逆先锋/极简主义者/创意总监/数据驱动/奢华高端/环保自然/游戏品牌/教育品牌/金融科技}
- 情绪板：{3个关键词}
- 设计禁忌：{绝对不能出现的元素列表}
- 竞品拆解：{喜欢的竞品 + 具体喜欢的点 + 提取的方向}
- 文案调性：{专业/轻松/幽默/温暖/权威/简洁}

## 技术约束
- 技术栈：{React/Vue/HTML/Flutter/...}
- 性能要求：{描述}
- 国际化：{需要/不需要}
```

### DESIGN.md 产出（v2.0 格式）

research 阶段对话全部完成后，**必须**生成 `output/design-system.md` 文件，严格遵循 [references/design-system-template.md](references/design-system-template.md) 的 9-section 格式：

```
output/
└── design-system.md   # 9-section 结构化设计系统文件
```

**填充规则**：

| Section | 数据来源 |
|---------|---------|
| 1. 视觉主题与氛围 | research 第 4 轮"品牌人格 + 情绪板" |
| 2. 配色 | research 第 2 轮"暗色模式" + 第 4 轮"竞品颜色提取" |
| 3. 排版 | research 第 2 轮字体偏好 + creative 视觉论文的 typography-distance |
| 4. 间距 | creative 视觉论文 layout-direction 推导 |
| 5. 布局与构图 | research 第 1 轮"设计类型" + 第 3 轮"响应式" |
| 6. 组件 | creative 视觉论文 material-direction 推导 |
| 7. 动效与交互 | research 第 3 轮"交互复杂度" |
| 8. 语调与品牌 | research 第 4 轮"品牌人格" |
| 9. 禁止模式 | research 第 4 轮"设计禁忌" + anti-ai-slop.md |

**硬约束**：
- 所有颜色值必须为真实 hex 值（6 位或 3 位），不允许 #REPLACE_ME
- 所有 CSS 变量必须包裹在 `:root {}` 块
- 暗色模式必须使用 `[data-theme="dark"]` 覆盖模式
- 必须包含 `Font labels for catalog extraction:` 块
- 每个交互组件必须包含 `:focus-visible` 样式

pass-data.yaml 更新为：

```yaml
design-system: output/design-system.md
```

---

### 大企业参考风格速查

> v2.1.0：完整的 60+ 全球品牌设计系统目录见 [references/corporate-design-systems.md](references/corporate-design-systems.md)

当用户在 research 对话中提到具体品牌时，Agent 应：

1. **查目录**：在 `corporate-design-systems.md` 中找到对应品牌
2. **下载 DESIGN.md**：若品牌在 VoltAgent/awesome-design-md 中（60+ 品牌），通过 `https://getdesign.md/{brand-slug}/design-md` 下载完整的 9-section DESIGN.md
3. **提取 Token**：从 DESIGN.md 中提取色板/字体/间距/圆角等核心参数
4. **映射品牌人格**：将品牌设计特征映射到本 Skill 的 14 种品牌人格之一
5. **注入对话**：在 research 第 4 轮（品牌人格）中引用提取的参考信息

**快速速查（常用企业）：**

| 企业 | 关键特征 | 品牌人格 | DESIGN.md |
|------|----------|:---:|:---:|
| **Apple** | 极致留白、SF Pro 字体、银灰+蓝、动效克制 | 极简主义者 | ✅ |
| **Google** | Material Design、卡片隐喻、多彩 accent | 活力创业者 | 📄 官方文档 |
| **Stripe** | 紫色渐变、weight-300 排版、极简留白 | 优雅艺术家 | ✅ |
| **IBM** | Carbon DS、结构化蓝、企业网格 | 权威专家 | ✅ |
| **Microsoft** | Fluent UI、光感深度、Acrylic 材质 | 权威专家 | 📄 官方文档 |
| **Airbnb** | 暖珊瑚 accent、大圆角、摄影驱动 | 温暖朋友 | ✅ |
| **Figma** | 多彩活力、趣味但专业 | 创意总监 | ✅ |
| **Nike** | 黑白 UI、大写 Futura、全幅摄影 | 叛逆先锋 | ✅ |
| **Ferrari** | 黑白明暗、红极简点缀 | 奢华高端 | ✅ |
| **百度** | 蓝+白+红、搜索基因、卡片信息流 | 数据驱动 | — |
| **小米** | 扁平多彩、大圆角、活力橙、MiSans | 温暖朋友 | — |
| **华为** | HarmonyOS、空间感/光影/生命力 | 极简主义者 | — |
| **阿里/Ant Design** | 企业级中后台、确定性/意义/生长 | 权威专家 | 📄 官方文档 |
| **腾讯/TDesign** | 包容/多元/进化/连接 | 权威专家 | 📄 官方文档 |
| **字节/Arco Design** | 年轻化、简洁高效 | 活力创业者 | 📄 官方文档 |

> 完整目录（60+ 国际品牌 + 17 个中国品牌）见 `references/corporate-design-systems.md`

### 全网搜索设计参考

> ⚠️ **搜索目标：找设计作品/界面截图/组件模板，不是找文章/博客/教程。**

#### 搜索源分类

##### ✅ 设计作品平台（必须优先搜索 — 能找到真实的 UI 截图和组件）

| 来源 | 搜索方式 | 能找到什么 |
|------|----------|-----------|
| Dribbble | `site:dribbble.com {关键词}` | UI 截图、按钮样式、卡片设计、配色方案 |
| Behance | `site:behance.net {关键词}` | 完整项目案例、品牌设计系统 |
| Awwwards | `site:awwwards.com {关键词}` | 获奖网站、前沿布局 |
| Mobbin | `site:mobbin.com {关键词}` | 真实 App 截图、移动端 UI 模式 |
| CollectUI | `site:collectui.com {关键词}` | 按组件分类的 UI 截图（登录页/404/设置页等） |
| Pageflows | `site:pageflows.com {关键词}` | 用户流程截图、交互模式 |
| Refero | `site:refero.design {关键词}` | 真实 Web App 截图 |
| Godly | `site:godly.website {关键词}` | 精选高设计质量网站 |
| Siteinspire | `site:siteinspire.com {关键词}` | 按风格分类的设计参考 |
| Landingfolio | `site:landingfolio.com {关键词}` | 落地页截图 |
| CSS Design Awards | `site:cssdesignawards.com {关键词}` | CSS 技术实现案例 |
| Uigarage | `site:uigarage.net {关键词}` | 按日更新的 UI 设计截图 |
| CallToInspiration | `site:calltoinspiration.com {关键词}` | UI 组件细节截图 |
| Httpster | `site:httpster.net {关键词}` | 当代网站设计参考 |

##### ❌ 科技博客/文章网站（绝对禁止搜索 — 只能看到理论文章，找不到实际 UI 模板）

| 禁止搜索 | 原因 |
|----------|------|
| `site:medium.com` | 博客文章，没有 UI 截图 |
| `site:smashingmagazine.com` | 设计理论文章 |
| `site:dev.to` | 开发者博客，不是设计作品 |
| `site:css-tricks.com` | CSS 教程，不是实际 UI |
| `site:freecodecamp.org` | 编程文章 |
| `site:uxdesign.cc` | UX 理论博客 |
| `site:blog.logrocket.com` | 技术文章 |
| `site:ui.dev` | 教程文章 |
| `site:web.dev` | 性能/SEO 文章，不是 UI 设计 |
| 任何其他博客/文章/教学类网站 | 我们找的是设计作品，不是文章 |

#### 搜索后强制步骤

> ⚠️ **搜索只是第一步，必须执行以下步骤才能提取到可用素材：**

```
Step A: 关键词搜索
  ├── 从 Design Brief 提取关键词（产品类型 + 页面类型 + 风格）
  ├── 用 site:设计作品平台 限定搜索
  └── 同时搜索 3-5 个设计作品平台

Step B: 打开搜索结果（WebFetch）      ← 🆕 不可跳过
  ├── 对每个搜索结果，用 WebFetch 打开具体页面
  ├── 目标：看到真实的 UI 截图、组件样式、配色方案
  └── 不看：纯文字文章、博客帖子、教程

Step C: 提取具体设计资产               ← 🆕 不可跳过
  ├── 按钮样式：截图中的按钮颜色/圆角/阴影/悬停效果
  ├── 卡片设计：卡片圆角/阴影/内边距/边框
  ├── 表单布局：标签位置/输入框样式/错误状态
  ├── 表格风格：表头颜色/行交替色/边框/分页器
  ├── 导航模式：侧边栏/顶栏/标签页/面包屑
  ├── 配色提取：主色/强调色/背景色/文字色的 hex 值
  ├── 字体识别：标题字体/正文字体/字号层级
  └── 间距节奏：section 间距/card padding/元素间距

Step D: 解构分析（4 步流程，见下方）
```

#### 搜索关键词构建模板

```
{产品类型} + {页面类型} + {具体组件} + {年份}

✅ 正确示例（能找到具体 UI）：
- "admin dashboard table filter card" → site:dribbble.com
- "backend form validation input style" → site:collectui.com
- "data table pagination checkbox dark" → site:mobbin.com
- "login page clean modern 2024" → site:awwwards.com
- "SaaS pricing card comparison" → site:dribbble.com
- "settings page sidebar navigation" → site:pageflows.com

❌ 错误示例（只能找到文章）：
- "admin dashboard best practices" → 会搜到博客文章
- "how to design a backend panel" → 会搜到教程
- "UI design principles 2024" → 会搜到理论文章
- "what is good dashboard design" → 纯理论
```

#### 搜索策略

```
第一步：从 Design Brief 提取关键词
  ↓ 如 "后台管理后台 数据表格 dashboard 深色"
第二步：构建面向设计平台的搜索查询
  ↓ 格式：{具体组件描述} + site:{设计作品平台}
  ↓ 示例："data table filter dark" site:dribbble.com
第三步：多源并行搜索（3-5 个设计作品平台）
  ↓ 每个平台用略微不同的关键词
第四步：WebFetch 打开 3-5 个最佳结果    ← 🆕 关键步骤
  ↓ 打开实际页面，查看 UI 截图和细节
第五步：提取具体设计资产             ← 🆕 关键步骤
  ↓ 按钮样式/卡片布局/配色 hex 值/字体/间距
第六步：解构优化（见下方）

### 参考解构与综合优化（4 步流程）

网上搜集的设计参考通常不够完美，需要经过解构、分析、融合、优化四步处理：

**Step 1: 解构（Deconstruct）**
- 拆解参考设计的组成元素：布局结构、色彩方案、排版层次、组件模式、交互方式、间距节奏
- 标注优秀元素和不足之处
- 提取可复用的设计模式

**Step 2: 分析（Analyze）**
- 分析参考设计的优点：什么让它看起来好？
- 分析参考设计的缺点：什么让它看起来差？
- 识别设计模式背后的原理：为什么这样布局？为什么用这个颜色？
- 评估与用户需求的匹配度

**Step 3: 融合（Synthesize）**
- 从多个参考中提取各自的优点
- 融合内置设计系统（色板、字体、Token）保持一致性
- 跨领域借鉴：从建筑、时尚、工业设计等领域获取灵感
- 组合成新的设计方案，而非照搬任何一个参考

**Step 4: 优化（Optimize）**
- 应用 Design Token 系统统一视觉语言
- 检查可访问性底线（对比度、触摸目标、键盘导航）
- 优化性能（图片、字体、动画）
- 确保响应式适配
- 对照反模式检查

**优化原则：**
- 参考是起点，不是终点——从参考中学习，但不复制
- 多源融合优于单一照搬——综合 3 个参考的优点 > 照搬 1 个参考
- 内置系统优先——Design Token、色板、字体对等内置资源优先使用
- 质量底线不可妥协——即使参考本身质量不高，优化后的输出必须达标

### 跨领域设计借鉴

设计思考不应局限于 UI 领域，以下领域可提供丰富的设计灵感：

| 领域 | 借鉴内容 | 应用场景 |
|------|----------|----------|
| 建筑 | 空间层次、结构韵律、光影对比 | 页面布局、视觉层次 |
| 时尚 | 色彩搭配、材质质感、比例关系 | 配色方案、视觉风格 |
| 工业设计 | 人机交互、功能美学、材料语言 | 组件设计、交互模式 |
| 自然 | 有机曲线、渐变色彩、生长模式 | 视觉元素、动效设计 |
| 电影 | 镜头语言、色彩分级、叙事节奏 | 页面转场、视觉叙事 |
| 音乐 | 节奏感、层次感、和谐与对比 | 动效节奏、信息层次 |
| 平面设计 | 排版规则、网格系统、留白艺术 | 排版布局、视觉平衡 |
| 游戏 | 沉浸感、进度反馈、成就系统 | 用户引导、反馈机制 |
| 书法 | 笔触韵律、空间张力、气韵生动 | 品牌标识、标题设计 |
| 摄影 | 构图法则、景深关系、色彩温度 | 图片处理、视觉焦点 |

---

## 4. 通用设计原则（所有子命令共享）

### 方向先行

- 先确定视觉方向再执行，避免"安全平均"的 UI
- 可能的方向包括但不限于：
  - **极简**：少即是多，大量留白，精准排版
  - **编辑**：杂志式排版，强层次感，大胆字体
  - **工业**：功能优先，网格系统，机械感
  - **奢华**：精致细节，金色点缀，优雅过渡
  - **趣味**：圆润形状，明亮色彩，微交互
  - **几何**：形状驱动，数学美感，对称/不对称
  - **复古未来**：怀旧与未来碰撞，霓虹+金属
  - **有机**：自然曲线，流动形态，生物感
  - **极繁**：丰富层次，密集信息，视觉盛宴
- 选择一个方向并坚持执行，不要混合多个方向

### Design Token 系统

所有设计决策通过 Design Token 表达，确保跨模块一致性：

**三层架构：**

```
原始 Token（Primitive）     →  语义 Token（Semantic）     →  组件 Token（Component）
--color-blue-500: #3b82f6     --color-primary: var(...)     --button-bg: var(--color-primary)
--font-size-16: 1rem          --font-body: var(...)         --card-title: var(--font-heading-md)
--space-4: 1rem               --space-inline: var(...)      --input-padding: var(--space-inline)
```

**命名规范：**

- 语义化命名：`--color-danger` 而非 `--color-red-500`
- 分层命名：`--{category}-{property}-{variant}`
- 暗色模式通过语义 Token 自动适配，不需要单独定义暗色值

**必须输出的 Token 类别：**

| 类别 | 示例 |
|------|------|
| 颜色 | --color-primary, --color-surface, --color-on-surface |
| 排版 | --font-heading-lg, --font-body-md, --font-mono |
| 间距 | --space-xs, --space-sm, --space-md, --space-lg |
| 圆角 | --radius-sm, --radius-md, --radius-full |
| 阴影 | --shadow-sm, --shadow-md, --shadow-lg |
| 动效 | --duration-fast, --duration-normal, --ease-default |

### 可访问性底线

所有设计必须满足以下最低标准：

| 指标 | 要求 |
|------|------|
| 对比度（正文） | ≥ 4.5:1 |
| 对比度（大文本） | ≥ 3:1 |
| 触摸目标 | 最小 44×44pt |
| 键盘导航 | 完整支持，可见焦点环 |
| 颜色信息 | 不只靠颜色传达信息，需配合图标/文字 |
| 屏幕阅读器 | 语义化 HTML，ARIA 标签 |
| 动效 | 尊重 prefers-reduced-motion |

### 反模式（所有模块禁止）

以下模式在所有子命令中均被禁止：

- ❌ **通用 SaaS 卡片网格**作为第一印象——缺乏个性，千篇一律
- ❌ **随机强调色无系统**——没有 Design Token 约束的随意配色
- ❌ **占位符感排版**——默认字体、默认行高、默认间距
- ❌ **仅为装饰的动效**——没有功能目的的动画
- ❌ **混合风格随意组合**——极简 + 极繁 + 工业随意混搭

### 去 AI 味设计原则

完整的反 AI 模式规则集见 [references/anti-ai-slop.md](references/anti-ai-slop.md)（14 条精确规则，含具体 hex 值）。

核心要求：
- AI 默认色（#6366f1 / #4f46e5 / #8b5cf6 等）绝对禁止
- 两色渐变 Hero 绝对禁止
- emoji 作为功能图标绝对禁止
- h1/h2 必须使用 `var(--font-display)`
- 圆角卡片 + 彩色左边框组合绝对禁止
- 假指标（"10× faster"）绝对禁止
- 填充文案（lorem ipsum）绝对禁止
- 标准 Hero→Features→Pricing→FAQ→CTA 序列必须打破
- 装饰性 blob/wave SVG 背景禁止
- 完美对称布局禁止

**审查规则全表** 见 `references/anti-ai-slop.md`，design 阶段执行前必须加载此文件。

---

## 5. 子技能加载机制

当路由到子命令时，使用 Read 工具加载对应的 SKILL.md 文件，获取该模块的完整工作流和详细指令：

```
creative → Read ${SKILL_DIR}/subskills/creative/SKILL.md
design   → Read ${SKILL_DIR}/subskills/design/SKILL.md
theme    → Read ${SKILL_DIR}/subskills/theme/SKILL.md
review   → Read ${SKILL_DIR}/subskills/review/SKILL.md
```

**加载流程：**

1. 根据路由规则确定子命令
2. 使用 Read 工具加载对应子技能的 SKILL.md
3. 按照子技能的工作流执行任务
4. 如需串联，将输出传递给下一个子技能

**注意：** `${SKILL_DIR}` 为本 Skill 的安装目录，即 `super-frontend-design/`。

---

## 6. 参考资料索引

本 Skill 包含丰富的参考资料，供各子命令使用：

| 文件 | 内容 | 使用场景 |
|------|------|----------|
| references/palettes.md | 161 色板数据 | theme 子命令 |
| references/font-pairings.md | 57 字体对数据 | theme 子命令 |
| references/ux-guidelines.md | 99 条 UX 准则 | design / review 子命令 |
| references/styles-catalog.md | 50+ 风格目录 | design 子命令 |
| references/chart-types.md | 25 图表类型 | design 子命令 |
| references/design-tokens.md | Design Token 规范 | theme / design 子命令 |
| templates/viewer.html | p5.js 交互模板 | creative 子命令 |
| templates/generator_template.js | p5.js 最佳实践 | creative 子命令 |
| canvas-fonts/ | 字体资源（TTF + OFL 授权） | creative 子命令 |
| themes/ | 10 个预设主题数据 | theme 子命令 |
| scripts/search.py | CLI 搜索工具 | design 子命令 |

**预设主题列表：**

| 主题 | 文件 | 风格 |
|------|------|------|
| Arctic Frost | themes/arctic-frost.md | 冷冽冬季，清晰专业 |
| Botanical Garden | themes/botanical-garden.md | 自然有机，清新生机 |
| Desert Rose | themes/desert-rose.md | 暖色沙漠，温暖优雅 |
| Forest Canopy | themes/forest-canopy.md | 深林绿意，沉稳内敛 |
| Golden Hour | themes/golden-hour.md | 黄金时刻，温暖活力 |
| Midnight Galaxy | themes/midnight-galaxy.md | 深空星夜，神秘科技 |
| Modern Minimalist | themes/modern-minimalist.md | 现代极简，黑白灰调 |
| Ocean Depths | themes/ocean-depths.md | 深海蓝调，沉稳专业 |
| Sunset Boulevard | themes/sunset-boulevard.md | 日落暖调，活力浪漫 |
| Tech Innovation | themes/tech-innovation.md | 科技创新，未来感 |

---

## 7. 跨子命令输出一致性规范

各子技能在独立运行时设计哲学差异大（creative 强调大胆创意 vs design 强调可运行代码 vs theme 强调 Token 系统），为避免输出风格割裂，必须遵守以下跨模块一致性规范。

### 7.1 统一术语表

所有子命令必须使用统一的术语，禁止各自定义：

| 术语 | 统一定义 | 来源 |
|------|----------|------|
| 品牌人格 | 设计灵魂的14种人格类型 | SKILL.md §3.5 第4轮 + references/brand-personality-expanded.md |
| 情绪板 | 3个关键词描述设计感觉 | SKILL.md §3.5 第4轮 |
| 视觉论文 | creative 阶段产出的5个方向决策 | subskills/creative/SKILL.md |
| Design Token | 三层架构的 CSS 变量系统 | SKILL.md §4 |
| 去AI味 | 14条精确反AI规则（含七宗罪+软规则+抛光规则） | references/anti-ai-slop.md |
| 设计禁忌 | 用户指定的绝对不能出现的元素 | SKILL.md §3.5 第4轮 + references/anti-ai-slop.md §9 |

### 7.2 阶段间传递格式

子命令串联时，输出必须包含传递给下一阶段的结构化数据块：

```
---pass-to-next---
brand-personality: {品牌人格类型}
mood-board: [{词1}, {词2}, {词3}]
design-taboos: [{禁忌1}, {禁忌2}, ...]
visual-thesis:
  color-direction: {配色方向}
  typography-direction: {排版方向}
  layout-direction: {布局方向}
  material-direction: {材质方向}
  motion-direction: {动效方向}
---end-pass---
```

**责任划分：**
- `research` 产出 → 品牌人格 + 情绪板 + 设计禁忌（来自第4轮调研）
- `creative` 产出 → 视觉论文（5个方向决策）
- `theme` 消费 → 品牌人格 + 视觉论文，产出 Design Token
- `design` 消费 → Design Token + 品牌人格 + 视觉论文 + 设计禁忌，产出可运行代码
- `review` 消费 → 代码 + Design Token + 品牌人格 + 视觉论文 + 情绪板 + 设计禁忌，产出审查报告

### 7.3 统一输出模板

各阶段输出文件命名规范：

```
output/
├── 01-design-brief.md          # research 产出
├── 02-visual-thesis.md          # creative 产出
├── 03-design-tokens.css         # theme 产出
├── 04-implementation/           # design 产出（HTML/CSS/JS 或框架代码）
├── 05-review-report.md          # review 产出
└── pass-data.yaml               # 阶段传递数据
```

### 7.4 代码输出风格约束

`design` 子命令输出的前端代码必须满足：

| 约束 | 说明 |
|------|------|
| 使用语义化 Design Token | `var(--color-primary)` 而非 `#3b82f6` |
| 输出可独立运行 | 单个 HTML 文件或完整项目目录结构 |
| 包含注释标注设计决策来源 | `/* 品牌人格: 极客工程师 → 等宽字体 */` |
| 引用视觉论文 | 代码头部注释包含视觉论文链接 |
| 不包含 template 脚手架代码 | 禁止 create-react-app 等模板噪声 |

### 7.5 跨模块冲突解决

当子命令之间产出冲突时（如 theme 的预设配色与 creative 的视觉方向不符）：

| 冲突类型 | 解决优先级 | 示例 |
|----------|:---:|------|
| 视觉论文 vs 预设主题 | **视觉论文优先** | creative 指定"暖橙为主色" → theme 不能选"Arctic Frost"（冷蓝） |
| 用户明确偏好 vs 自动推荐 | **用户偏好优先** | 用户选择"Apple 风格" → 所有子命令必须遵循 Apple 设计特征 |
| 可访问性 vs 视觉表达 | **可访问性优先** | 文字对比度不达标 → 必须调整配色，即使偏离视觉论文 |
| 设计禁忌 vs 任何产出 | **设计禁忌一票否决** | 用户说"禁用蓝紫渐变" → 绝对不能出现，即使视觉论文指定 |

---

## 8. 注意事项

### 必须遵守

- ✅ **先调研再设计**：设计前必须使用 AskUserQuestion 工具完成需求调研（Phase 0），明确目标、受众、功能、交互、风格偏好
- ✅ **先路由再执行**：不要跳过子命令加载，必须先确定路由并加载对应 SKILL.md
- ✅ **保持 Design Token 一致性**：跨子命令共享同一套 Design Token 系统
- ✅ **每个阶段结束自动触发 review 审查**：调用 subskills/review/SKILL.md（基于 impeccable），形成质量闭环
- ✅ **遵循各子命令的完整工作流**：不要省略步骤，每个步骤都有其目的
- ✅ **输出可运行的代码**：design 子命令输出的代码必须可直接运行
- ✅ **语义化 Token**：所有颜色、间距、字体使用语义化命名
- ✅ **全网搜索结果必须经过解构优化**：不可直接照搬搜索结果，必须经过解构→分析→融合→优化四步流程
- ✅ **跨领域借鉴**：设计思考不局限于 UI 领域，主动从建筑、时尚、工业设计等领域获取灵感
- ✅ **去 AI 味**：所有设计输出必须经过反 AI 味检查清单，禁止蓝紫渐变、emoji 图标、均匀间距等 AI 味特征开端

### 禁止行为

- ❌ **跳过需求调研直接设计**：信息不完整时必须先完成 Phase 0 调研，必须弹出 AskUserQuestion 对话
- ❌ **用全局画像/历史偏好替代调研**：绝对禁止从用户全局画像（user profile）、历史记忆（global memory）、ontology、跨会话持久化数据中提取设计偏好来跳过或填充调研答案。每次设计任务的场景和要求都不同
- ❌ **跳过子命令直接执行**：必须先加载子技能再执行
- ❌ **混合多个方向随意组合**：选择一个方向并坚持
- ❌ **使用原始 hex 值而非语义 Token**：`color: #3b82f6` → `color: var(--color-primary)`
- ❌ **忽略可访问性底线**：对比度、触摸目标、键盘导航不可妥协
- ❌ **省略子命令中的任何步骤**：每个步骤都是质量保证的一部分
- ❌ **输出占位符内容**：所有内容必须是真实、完整、可用的
- ❌ **直接照搬搜索结果**：全网搜索的参考必须经过解构优化，不可原样复制
- ❌ **输出 AI 味设计**：禁止蓝紫渐变按钮、emoji 图标、灰底白卡、均匀间距、无个性排版

---

## 9. 快速参考

### 常见场景路由

| 用户说 | 路由到 | 说明 |
|--------|--------|------|
| "帮我做个生成艺术作品" | creative | p5.js 交互式 |
| "设计一张海报" | creative | PDF/PNG 静态输出 |
| "做一个 landing page" | research → design | 先调研再设计 |
| "设计一个 dashboard" | research → design | 先调研再设计 |
| "设计一个后端管理页面" | research → design | 先搜索参考再设计 |
| "帮我选个配色方案" | theme | 色板 + Design Token |
| "适配 dark mode" | theme | 暗色模式主题 |
| "审查一下我的 UI" | review | 设计质量审查 |
| "从零开始设计一个网站" | 完整工作流 | research → creative → theme → design → review |
| "搜索一下后台管理的设计灵感" | research | 全网搜索 + 解构优化 |
| "优化一下界面" | review | 审查 + 改进建议 |

### 子命令速查

```
research  →  需求调研、全网搜索、参考解构、Design Brief 输出
creative  →  灵感探索、生成艺术、海报设计、视觉表达
theme     →  配色方案、字体搭配、主题系统、品牌规范
design    →  页面设计、组件开发、UI实现、代码输出
review    →  设计审查、质量评分、可访问性检查、改进建议
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.1.0 | 2026-06-22 | 企业设计系统参考目录：1) 集成 VoltAgent/awesome-design-md（68K+ stars，60+ 品牌可下载 DESIGN.md）；2) 集成 alexpate/awesome-design-systems（200+ 设计系统目录）；3) 新增 17 个中国企业设计系统分析（百度/小米/华为/阿里/腾讯/字节/京东/美团等）；4) 大企业参考速查表升级为 5 步流程（查目录→下载 DESIGN.md→提取 Token→映射人格→注入对话） |
| v2.0.0 | 2026-06-22 | v2.0 大版本：1) 精确反AI规则集(10→14条，含具体hex值和Grep检测)；2) 结构化 DESIGN.md(自由格式→9-section)；3) Typography硬规则(8项Grep检测，ALL CAPS tracking≥0.06em)；4) Block分类目录(18类型+场景匹配)；5) 动效方向扩展(Aceternity+Inspira 19种特效)；6) MCP集成指南(4服务器)；7) 5框架Prompt模板(React/Vue/RN/HTML/Flutter)；8) 品牌人格扩展(8→14)；9) 子技能版本统一+8项修复 |
| v1.8.0 | 2026-06-21 | 搜索策略大修：1) 搜索源从 9 个扩展到 14 个设计作品平台（新增 Mobbin/Pageflows/Refero/Godly/Siteinspire/CallToInspiration/Httpster）；2) 新增科技博客禁令（10 个禁止搜索的博客/教程网站）；3) 新增「搜索后强制步骤」：WebFetch → 提取设计资产（按钮/卡片/表单/表格/导航/配色/字体/间距 8 类）；4) 新增搜索关键词正例/反例模板；5) research 搜索标记为主动触发而非 fallback；6) design 子技能 Part 12 同步更新 |
| v1.7.0 | 2026-06-21 | 二次排查修复 4 项高危/中危问题：1) design Part 1「设计工作流」从自填改为从 Design Brief 提取（禁止自行推理/套用默认值）；2) creative/theme/review 三个子技能新增 §0 调研守卫 + 全局画像禁令；3) design「App UI」从强制默认 Linear 改为根据 7 种品牌人格自适应选择基调；4) review 新增 §0「设计灵魂追溯」8 项 Design Brief 对照检查 + 设计灵魂评分（A+/A/B/C） |
| v1.6.0 | 2026-06-21 | 修复调研被跳过问题：1) P0 新增「铁律」4条（绝对禁止用全局画像/历史偏好/ontology替代调研、每次必须询问设计场景、禁止跨会话复用偏好）；2) P1 收窄快捷通道（移除「需求明确可跳过research」、新增3条严格跳过标准、路由到design前必须最小化调研）；3) P2 design子技能新增§0「执行前置条件」调研守卫（无Design Brief拒绝执行+全局画像禁令+返回消息模板）；4) P3 快捷模式改为严格限制表（3种情况各有最少询问项+禁止行为）；5) 禁止行为新增「用全局画像替代调研」禁令 |
| v1.5.0 | 2026-06-21 | 审查报告驱动修复：1) P0 新增「0. 调用方式」章节，明确子代理调用方法 + 误用降级提示；2) P1 新增与 frontend-design/web-dev/ui-ux-pro-max 的对比表 + 正例/反例触发条件；3) P2 新增路由 Fallback 机制（L1用户确认→L2安全降级→L3默认工作流→L4优雅退出）+ 路由决策树 + 路由冲突解决；4) P3 新增调用示例和「何时使用本 Skill」场景表；5) P4 新增「7. 跨子命令输出一致性规范」包括统一术语表、阶段传递格式、输出模板、代码风格约束、跨模块冲突解决 |
| v1.4.0 | 2026-06-13 | 根治"设计不好看"问题：1) 调研增加第4轮（品牌人格+情绪板+设计禁忌+竞品拆解）+ 4个深度问题；2) creative子技能增加「视觉论文」输出（5个方向决策）；3) theme子技能增加反安全默认约束（禁止从预设复制、字体必须有个性）；4) design子技能增加8条执行级约束（视觉论文引用、非对称布局、模板检测、品牌人格体现、情绪板验证、字体个性、输出质量门限）；5) review子技能增加设计灵魂追溯检查（品牌人格/情绪板/视觉论文/设计禁忌）；6) 阶段间增加视觉论文传递机制 |
| v1.3.0 | 2026-06-13 | 补全遗漏的 web-design-guidelines 技能（并入 review 子技能，新增第 15 个审查维度）；review 子技能版本升至 v1.2.0；合并来源从 10 个更新为 11 个 |
| v1.2.0 | 2026-06-13 | 修复调研对话不弹出的问题（强制使用 AskUserQuestion 3轮对话）；新增 9 个企业参考风格选项（Apple/Stripe/Linear/Vercel/Notion/GitHub/Airbnb/Figma/Tailwind UI）；新增去 AI 味设计原则（10 条反 AI 模式 + 7 条正向原则 + 10 条检查清单）；深度集成 impeccable（每个阶段结束后自动触发审查）；review 子技能新增反 AI 味专项审查 |
| v1.1.0 | 2026-06-13 | 新增 Phase 0 需求调研流程；新增 research 子命令（需求调研+全网搜索+参考解构优化）；新增跨领域设计借鉴原则；工作流从 4 阶段扩展为 5 阶段；design 子技能集成全网搜索和参考优化 |
| v1.0.0 | 2026-06-13 | 初始版本，合并 10 个前端设计 skill |

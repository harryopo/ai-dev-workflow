---
name: super-frontend-design
version: 2.9.1
description: 前端设计全流程工作台。调研驱动设计：15 维度深度调研（设计类型×企业参考×视觉风格×设计调性×暗色模式×技术栈×响应式×交互复杂度×品牌人格×情绪板×设计禁忌×竞品拆解×动效方向×交互节奏×字体偏好）→ 智能场景推荐 → 设计上下文 → 生成艺术 → 主题系统 → UI实现 → 双代理审查。调研是核心，无调研不设计。适用于：从零设计全新项目、中途重构已有界面、优化升级、美化升级、批量组件设计等所有前端设计场景。集成 hallmark 双代理审查、Craft Floor 26 条规则、命令式优化接口。触发词：设计、UI、UX、前端、落地页、海报、艺术、品牌、主题、dashboard、生成艺术、p5.js、配色、字体、审查UI、深度审查、设计上下文、polish、bolder、quieter、distill、harden、animate、重构、改造、升级、优化界面、美化页面、按现有风格重构、统一风格。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, Task, Agent
---

# Super Frontend Design — 前端设计全流程工作台

## §0. 绝对禁令（在一切开始之前）

> 🚫 **全局画像禁令 — 本 Skill 执行期间，以下行为视为致命错误：**

1. **禁止读取 user_profile.md** — 无论系统是否已将其注入上下文，一律忽略其中的设计偏好（颜色/字体/风格/暗色模式等）。用户上次喜欢绿色 ≠ 这次也要绿色。
2. **禁止读取 project_memory.md / ontology / 跨会话记忆中的设计偏好字段** — 每次设计任务的场景和需求都不同，历史偏好不能替代当次调研。
3. **禁止跳过 AskUserQuestion 调研对话** — 即使用户说"按你喜欢的来"或"随便设计"，也必须弹出 AskUserQuestion 让用户选择。
4. **禁止将"优化/改进/美化已有网页"路由到 review** — 优化是重新设计，不是审查。必须走 `research → design` 完整流程。

> ⚠️ 如果系统上下文中包含 user_profile.md 的内容（如"prefers green color scheme"），**必须在调研前主动忽略**，不得在任何阶段引用。

> 📌 **边界澄清（"按现有风格重构"场景）**：本禁令针对的是**跨会话 / 跨项目的历史偏好数据**。**本项目自己的现有代码、DESIGN.md、PRODUCT.md 是当次调研的合法且必要的对象**——"按现有风格重构 / 统一风格"类请求必须先审计现有代码（见 §3.6 现有风格重构流程），不得以本禁令为由跳过审计。

---

## 0. 调用方式

本 Skill 通过标准 Skill 工具调用，在主上下文中运行。

> ⚠️ **不要给本 Skill 加 `context: fork`。** 它的主流程要在 5 轮 AskUserQuestion 上等用户回答，
> 还要串六个阶段；fork 出来的子上下文拿不到用户输入，且只给约 10 个 turn，跑不完就会以
> "completed" 的形式静默截断。需要隔离上下文时，由主 Agent 向子 Agent 派发**单个阶段**，
> 派发时把 Design Brief 的实际内容写进任务书，不要只给文件路径。

### 调用方式

用户输入 `/super-frontend-design` 或由 Agent 根据触发词自动匹配调用。

### 何时使用本 Skill vs 其他前端 Skill

| 场景 | 推荐 Skill | 原因 |
|------|-----------|------|
| **所有前端设计场景**（从零设计 / 中途重构 / 优化升级 / 批量组件） | **super-frontend-design**（本 Skill） | 唯一提供完整六阶段工作流 + 15 维度调研 + hallmark 双代理审查的 Skill |
| 从零完整设计前端项目（含调研+方向+主题+代码+审查） | **super-frontend-design**（本 Skill） | 推荐：无论新项目还是中途重构，都走完整工作流 |
| 查询设计数据（色板/字体/风格/UX准则） | `ui-ux-pro-max` | 设计数据库查询，不需要完整设计流程 |
| 审查现有设计（快速） | 直接用本 Skill 的 `review` 子命令 | 不需要完整工作流，只走审查通道 |
| 深度审查现有设计（上线前） | 直接用本 Skill 的 `critique` 子命令 | 双代理评估 + 26条探测器规则 |
| 优化设计（打磨/增强/精简） | 直接用本 Skill 的 `refine` 子命令 | 命令式优化接口 |
| 添加动效 | 直接用本 Skill 的 `animate` 子命令 | 动效设计与实现 |
| 生成算法艺术作品/海报 | 直接用本 Skill 的 `creative` 子命令 | 不需要完整工作流，只走创意通道 |

### 适用场景（正例 ✅）

- "帮我设计一个 SaaS 产品官网"
- "从零开始设计一个后台管理系统"
- "帮我做一个完整的品牌落地页，要有调研、视觉方向、设计实现"
- "我有个产品想法，帮我从头设计它的前端界面"
- "帮我设计 dashboard，我想先看看竞品参考"
- "重构我的现有前端，换一套全新的设计风格"
- "把后台管理页面全部升级，改用新的设计系统"
- "优化这个页面的 UI，提升视觉品质"
- "把移动端 App 的界面重新设计一遍"
- "给产品页面加一套完整的动效系统"

### 不适用场景（反例 ❌）

- "给这个按钮换个颜色" → 直接用代码修改，不需要设计 Skill
- "帮我查一下有什么好看的配色方案" → 用 `ui-ux-pro-max` 查数据
- "写一个 React 组件的代码" → 直接编码，不需要设计流程
- "审查一下这个页面的可访问性" → 可直接用本 Skill 的 review 子命令，但不需要完整六阶段
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
| impeccable | 双代理审查、Craft Floor 探测器规则、设计上下文系统 | review + critique + design-context |
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
| research | 需求调研、设计参考、搜索灵感、后端页面、找参考、设计方向 | subskills/research/SKILL.md | 需求调研对话 + 全网搜索设计参考 + 参考解构优化 |
| design-context | 设计上下文、初始化项目、teach、PRODUCT.md、DESIGN.md、访客意图、shape | subskills/design-context/SKILL.md | 项目级设计上下文管理、设计Token提取、访客意图分类、设计brief生成 |
| creative | 生成艺术、海报、p5.js、算法艺术、视觉设计、flow field、粒子系统 | subskills/creative/SKILL.md | 哲学宣言→视觉表达，p5.js 交互式 + PDF/PNG 静态 |
| design | 设计页面、UI、组件、landing page、dashboard、app、前端、桌面应用、Electron、Tauri、PySide6、SwiftUI | **必须先加载 subskills/research/SKILL.md 完成调研**，再加载 subskills/design-context/SKILL.md 获取上下文，最后加载 subskills/design/SKILL.md 执行设计 | ⚠️ 无 Design Brief 拒绝执行。支持网页/移动端/桌面端（Electron/Tauri/PySide6/SwiftUI）全场景 |
| theme | 配色、字体、主题、品牌色、dark mode、调色板、跨平台 Token 输出 | subskills/theme/SKILL.md | 10 预设主题 + 自定义 + 品牌规范，Design Token 输出（CSS/SwiftUI/Compose/WinUI 3/Tailwind v4） |
| review | 审查UI、设计评分、优化界面、UX检查、可访问性 | subskills/review/SKILL.md | 快速审查：19维度质量检查 + 56条Slop Test反AI味（其中可静态判定的部分由 `slop_scan.py` 执行，判定表见 `rules/slop-table.json`，其余人工核对） |
| critique | 深度审查、critique、双代理审查、探测器规则、上线前检查 | subskills/critique/SKILL.md | 深度审查：双代理评估（Assessment A + B）+ 26条Craft Floor探测器规则 |
| refine | polish、bolder、quieter、distill、harden、优化设计、打磨界面 | subskills/refine/SKILL.md | 命令式设计优化：上线前打磨/增强视觉/降低噪音/精简内容/性能加固 |
| animate | animate、动效、动画、ScrollTrigger、GSAP、桌面动效、Electron动画、SwiftUI动效 | subskills/animate/SKILL.md | 动效调研前置 → GSAP vs Motion 选择 → 时间线编排；支持网页（GSAP）和桌面（系统原生） |

### 路由规则

> ⚠️ **铁律：任何路由到 `design` 的请求，必须先执行 `research` 调研对话（AskUserQuestion），产出 Design Brief 后才能进入 design 子技能。违反此规则视为 Skill 执行失败。**

根据用户输入的关键词自动路由到对应子命令：

- 用户提到 **"需求调研" / "设计参考" / "搜索灵感" / "找参考" / "后端页面" / "设计方向"** → `research`
- 用户提到 **"生成艺术" / "算法艺术" / "p5.js" / "交互" / "粒子" / "flow field"** → `creative`
- 用户提到 **"海报" / "设计" / "PDF" / "PNG" / "海报设计" / "视觉设计"** 且不涉及网页 UI → `creative`
- 用户提到 **"设计页面" / "UI" / "组件" / "landing page" / "dashboard" / "app"** → **`research`（调研）→ `design-context`（初始化上下文）→ `design`（设计）**，必须先完成调研和上下文初始化
- 用户提到 **"配色" / "字体" / "主题" / "品牌色" / "dark mode" / "调色板"** → `theme`
- 用户提到 **"审查UI" / "设计评分" / "UX检查"** → `review`
- 用户提到 **"深度审查" / "critique" / "双代理审查" / "探测器规则"** → `critique`
- 用户提到 **"polish" / "bolder" / "quieter" / "distill" / "harden"** → `refine`
- 用户提到 **"animate" / "动效" / "动画"** → `animate`
- 用户提到 **"优化" / "改进" / "美化" / "重新设计" / "改造" / "升级" / "重构"** 已有网页 → 先分风格意图，再定流程：
  - **要求保持现有风格**（"按现有风格""统一一下风格""别换风格""保持现在的风格"）→ 走 **§3.6 现有风格重构流程**（现状审计 → 统一设计稿 → ⛔ 用户确认 → 按稿重构）
  - **要换新风格或未指定** → **`research`（调研）→ `design-context`（初始化上下文）→ `design`（重新设计）**
  - 两者都不是 review！优化/重构是重新设计任务，必须先调研
- 用户未明确指定 → **先触发 `research` 需求调研**，通过对话明确需求后再路由

> ⚠️ **"优化/改进/美化"路由铁律**：当用户说"优化这个网页""改进这个界面""美化这个页面"时，**绝对禁止路由到 review**。review 只是审查现有设计的缺陷，不会重新调研用户想要什么风格。必须走 `research → design` 完整流程，让用户通过 AskUserQuestion 选择新的设计方向。
>
> 若用户明确要求**保持现有风格**，"重新调研"的对象是**现有代码库**（走 §3.6 审计流程），同样必须调研、同样禁止跳过。

### 路由 Fallback 机制

路由失败或不确定时的降级策略（按优先级）：

| Fallback 层级 | 条件 | 行为 |
|:---:|---|---|
| **L1 · 用户确认** | 无法确定意图 | 使用 AskUserQuestion 询问用户意图，给出 2-3 个最可能的路由选项 |
| **L2 · 安全降级** | 用户模糊回答（"都行"/"随便"） | 自动路由到 `research`，通过需求调研对话澄清 |
| **L3 · 默认工作流** | 完全无法判断（极少数情况） | 启动完整六阶段工作流 `research → design-context → creative → theme → design → review`，每个阶段结束时让用户确认是否继续 |
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

当用户需要设计前端项目时（**无论是从零开始还是中途重构/优化**），按以下顺序执行：

> ⚠️ **铁律**：本 Skill 的唯一使命是「调研驱动设计」。任何前端设计任务（新建 / 重构 / 优化 / 升级）都必须先经过 research 调研，不允许跳过调研直接设计。

```
research（需求调研+参考搜索）→ design-context（设计上下文初始化）→ creative（灵感探索）→ theme（确定主题/配色）→ design（设计实现）→ review（快速审查）或 critique（深度审查）
```

命令式优化流程（设计后）：
```
/polish → /bolder → /quieter → /distill → /harden → /animate
```

**详细流程：**

0. **research 阶段（核心·不可跳过）**：15 维度深度调研对话 + 全网搜索设计参考（Phase 0，铁律）
   - 调研维度：设计类型 × 企业参考 × 视觉风格 × 设计调性 × 暗色模式 × 技术栈 × 响应式 × 交互复杂度 × 品牌人格 × 情绪板 × 设计禁忌 × 竞品拆解 × **动效方向** × **交互节奏** × **字体风格**
   - 智能场景推荐：基于设计类型自动推荐动效方案（见 animate 子技能 §0.3）
   - 搜索内容：当内置参考不足时，全网搜索设计灵感和最佳实践
   - 输出：结构化需求简报（Design Brief）+ 15 维度调研结果 + 设计参考集合

1. **design-context 阶段**：初始化项目级设计上下文
   - 输入：Design Brief + 设计参考集合
   - 输出：PRODUCT.md + DESIGN.md（项目级设计上下文持久化）
   - 访客意图分类：Persuade/Operate/Read/Experience
   - **→ 完成后触发 review 检查：设计上下文是否完整？访客意图是否明确？**

2. **creative 阶段**：探索视觉方向，生成灵感草图或交互原型
   - 输入：Design Brief + 设计上下文（PRODUCT.md + DESIGN.md）
   - 输出：视觉方向 + 设计哲学宣言
   - **→ 完成后触发 review 检查：视觉方向是否与需求简报一致？是否有 AI 味？**

3. **theme 阶段**：基于视觉方向确定主题系统
   - 输入：creative 阶段的视觉方向 + 设计上下文中的品牌/风格偏好
   - 输出：Design Token 系统（CSS 变量完整定义）
   - **→ 完成后触发 review 检查：Token 是否完整？对比度是否达标？**

4. **design 阶段**：基于主题系统实现前端代码
   - 输入：Design Token 系统 + Design Brief + 设计上下文 + 功能需求 + 设计参考集合 + 视觉论文
   - 输出：可运行的前端代码（HTML/CSS/JS 或框架代码）
   - **→ 完成后触发 review 检查：反 AI 味检查清单是否全部通过？设计灵魂是否体现？**

5. **review/critique 阶段**：设计质量审查
   - **review（快速审查）**：19维度质量检查 + 56条Slop Test反AI味（其中可静态判定的部分由 `slop_scan.py` 执行，判定表见 `rules/slop-table.json`，其余按 review §2.18 人工核对）
   - **critique（深度审查）**：双代理评估（Assessment A + B）+ 26条Craft Floor探测器规则
   - 输入：前端代码 + Design Token 系统 + Design Brief + 设计上下文 + 视觉论文
   - 输出：审查报告 + 具体改进建议
   - **→ 基于 impeccable 的双代理评估，包含去 AI 味专项检查 + 设计灵魂追溯检查**

### 快速通道（单一任务）

当用户只需要某个模块的能力时，直接路由到对应子命令，无需走完整六阶段流程：

- 只需要搜索设计参考 → `research`（不启动完整工作流）
- 只需要生成艺术作品 → `creative`
- 只需要调整配色/主题 → `theme`
- 只需要审查现有设计 → `review`
- 只需要深度审查现有设计 → `critique`
- 只需要优化设计 → `refine`
- 只需要添加动效 → `animate`
- **需要设计页面/UI → `research` → `design-context` → `design`（必须先调研，无例外）**

> ⚠️ **`design` 没有快速通道。** 任何涉及页面/UI 设计的请求，必须先经过 `research` 子技能的 AskUserQuestion 调研对话，再经过 `design-context` 子技能初始化设计上下文，产出 Design Brief + PRODUCT.md + DESIGN.md 后才能进入 design。这是铁律，不存在"需求已经很明确"的例外。
>
> 「按现有风格重构 / 统一风格」走 §3.6 现有风格重构流程——审计现状与设计稿确认同样不可跳过。

**唯一允许跳过完整 5 轮调研的情况（仍需至少 1 轮确认）：**
1. 用户在本**当前会话**中已经通过 AskUserQuestion 完成过一轮调研
2. 用户明确说"就用刚才调研的结果，再做一个类似页面"
3. 设计类型/场景未发生变化（如两次都是后台管理页面）
4. 设计上下文文件（PRODUCT.md + DESIGN.md）已存在

**不满足以上全部条件 → 必须启动完整调研对话。**

### 子命令串联

当用户需要完整流程时，按顺序执行子命令，每个子命令的输出作为下一个的输入：

| 阶段 | 输入 | 输出 | 前置条件 |
|------|------|------|----------|
| research | 用户初步需求（可能模糊） | 需求简报（Design Brief）+ 设计参考集合 | 无 |
| creative | 需求简报 + 设计参考 | 视觉方向 + 设计哲学 | 无 |
| theme | 视觉方向 + 品牌/风格偏好 | Design Token 系统（CSS 变量） | 无 |
| **design** | **Design Brief** + Design Token + 功能需求 + 设计参考 | 可运行的前端代码 | **⚠️ 必须有 Design Brief，否则拒绝执行** |
| review | 前端代码 + Design Token + 需求简报 | 审查报告 + 改进建议 | 无 |

> ⚠️ **design 阶段的硬性前置条件：**
> 1. 必须存在有效的 Design Brief（由 research 阶段产出）
> 2. 必须存在设计上下文文件（PRODUCT.md + DESIGN.md，由 design-context 阶段生成）
> 3. Design Brief 必须包含 `品牌人格` 和 `情绪板` 字段
> 4. 不满足 → 拒绝执行 design，强制回退到 research → design-context
> 5. **不存在"需求明确可跳过调研"的例外**

---

## 3.5. Phase 0 需求调研（research 子命令）

> 完整调研流程、5 轮对话问题、Design Brief 模板、搜索策略、参考解构优化、企业参考速查 → 见 [subskills/research/SKILL.md](subskills/research/SKILL.md)

**调研铁律摘要**：
1. 每次新设计任务必须通过 AskUserQuestion 进行 5 轮对话（共 15 维度），不允许跳过
2. 绝对禁止用全局画像/历史偏好/跨会话数据替代调研
3. 第 4 轮（品牌人格+情绪板+设计禁忌）和第 5 轮（动效方向+交互节奏+字体风格）**均不可跳过**
4. 快捷模式仍需至少第 1 轮 + 第 4 轮 + 第 5 轮
5. animate 子技能执行前必须从 Design Brief 读取动效配置，缺失则必须询问用户
6. **按现有风格重构**（保持 / 统一现有风格）走 **§3.6 现有风格重构流程**——调研对象是现有代码库，审计与统一方案确认不可跳过
7. **参考不默认全套**：第 1 轮先问参考维度与反参考；参考处理受「参考距离分级」约束（Operate 结构借鉴 / C 端原理解构、外观原创）——见 research 子技能

**调研输出**：Design Brief（需求简报）+ `output/design-system.md`（9-section 结构化设计系统文件）

---

## 3.6 现有风格重构流程（按现有风格 / 统一风格）

> **适用**：用户要求"按现有风格重构""统一一下这个项目的风格""重构但别换风格"——风格基准已经存在（散落在现有代码里）。
> **不适用**：用户要换新风格（走 §3 完整工作流）。
> ⚠️ 这是与完整工作流并列的第二条重通道：调研对象从"用户想象"变为**现有代码库**，并多一道**设计稿确认硬门**。

```
research（现有风格审计：扫描现有代码 + 门禁测量 → 风格画像 + 不一致点清单 → 用户确认统一方案）
  → design-context（生成统一设计稿 DESIGN.md）
    → ⛔ 用户确认设计稿（硬门：确认前禁止改实现代码）
      → design（按稿重构）
        → review/critique（照常）
          → 六道门禁（照常）
            → 询问是否固化风格（保存 DESIGN.md/PRODUCT.md 到项目根）
```

**与完整工作流的差异**：

| 阶段 | 完整工作流 | 现有风格重构 |
|------|-----------|-------------|
| research | 5 轮 15 维度问卷 | **现有风格审计模式**（见 research 子技能）：扫描代码 + 门禁测量 → 风格画像 + 不一致点清单 → 用户确认统一方案；品牌人格 / 情绪板从现有证据推导后确认 |
| creative | 视觉论文探索 | 跳过——不做新方向探索，视觉论文以统一设计稿为准 |
| theme | 从视觉论文推导 Token | 跳过——统一设计稿已含 Token 系统 |
| design-context | 初始化上下文 | 生成 / 更新 DESIGN.md 作为**统一设计稿**，呈现用户确认 |
| design | 按 Design Brief 设计 | **按稿重构**：逐页对齐设计稿，改动对照「不一致点清单」 |
| 完成 | 交付 | 交付 + **询问是否固化风格**（用户同意 → 写入项目根，后续设计以它为准） |

**执行要点**：

1. 只说"重构"未提风格意图 → 调研第一步先问「保持现有风格统一收敛 / 换一套新风格」，据答案分流
2. 审计先拿证据：扫描结果与门禁 findings 都要附文件:行号，禁止目测编造不一致点
3. 设计稿确认是硬门：即使用户说"直接改不用看了"，也必须先呈现设计稿（DESIGN.md 汇总 + 可选样例页）并请求明确确认
4. 重构中途发现新不一致点 → 回统一方案补确认，不带病施工
5. 固化询问不可省略：完成后明确问"是否把这套风格保存为项目设计规范"；保存后该项目所有后续设计 / 优化请求以它为准

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
design-context → Read ${SKILL_DIR}/subskills/design-context/SKILL.md
research       → Read ${SKILL_DIR}/subskills/research/SKILL.md
creative       → Read ${SKILL_DIR}/subskills/creative/SKILL.md
design         → Read ${SKILL_DIR}/subskills/design/SKILL.md
theme          → Read ${SKILL_DIR}/subskills/theme/SKILL.md
review         → Read ${SKILL_DIR}/subskills/review/SKILL.md
critique       → Read ${SKILL_DIR}/subskills/critique/SKILL.md
refine         → Read ${SKILL_DIR}/subskills/refine/SKILL.md
animate        → Read ${SKILL_DIR}/subskills/animate/SKILL.md
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
| references/macrostructures.md | 21 种 Macrostructure 路由 | design 子命令 |
| references/themes.md | 20 种命名主题风格（hallmark） | design / theme 子命令 |
| references/custom-theme.md | 自定义主题生成流程 | theme 子命令 |
| references/corporate-design-systems.md | 60+ 品牌 DESIGN.md 参考 | research / design 子命令 |
| references/mcp-integration.md | 推荐 MCP Server 配置指南 | 可选增强配置 |
| references/component-block-catalog.md | Cult UI / Magic UI 组件库 | design 子命令 |
| references/gsap-animation-guide.md | GSAP 动效最佳实践 | design / animate 子命令 |
| references/anti-ai-slop.md | 14 条精确反 AI 味规则 | design / review 子命令 |
| references/saturated-lanes.md | 饱和风格赛道清单（防"参考驱动像"的第二层同质化） | review / critique 子命令 |
| references/typography.md | Typography 硬规则（字体/字重/行高禁令） | review 子命令 §2.16 |
| references/premium-design-rules.md | 16 条数值化高级感规范 | design 子命令 |
| references/css-modern-features.md | CSS 2025-2026 新特性 | design 子命令 |
| references/brand-personality-expanded.md | 14 种品牌人格类型详解 | research / design 子命令 |
| references/design-system-template.md | DESIGN.md 输出模板 | design-context 子命令 |
| references/slop-test.md | hallmark 56 条 Slop Test 规则 | review 子命令 |
| references/desktop-patterns.md | 桌面应用设计模式库 | design 子命令（Electron/Tauri/PySide6/SwiftUI） |
| references/professional-software.md | 专业软件设计模式（Figma/VSCode/Notion/Linear/Trae/DaVinci/Blender/Warp） | design 子命令（效率工具/专业软件） |
| references/admin-enterprise-patterns.md | B端/企业软件设计模式库（数据表格/表单/权限/布局模板） | design 子命令（管理后台/ERP/内部工具） |
| references/token-mapping.md | 跨平台 Design Token 映射 | design 子命令（跨平台输出） |
| references/motion-patterns.md | 桌面端动效方案库 | animate 子命令（桌面应用） |
| templates/viewer.html | p5.js 交互模板 | creative 子命令 |
| templates/generator_template.js | p5.js 最佳实践 | creative 子命令 |
| templates/prompt-templates/react-tailwind.md | React + Tailwind 组件 Prompt 模板 | design 子命令（React 栈） |
| templates/prompt-templates/vue-nuxt.md | Vue 3 + Nuxt + Tailwind Prompt 模板 | design 子命令（Vue 栈） |
| templates/prompt-templates/html-css.md | 纯 HTML/CSS 组件 Prompt 模板 | design 子命令（无框架栈） |
| templates/prompt-templates/react-native.md | React Native + NativeWind Prompt 模板 | design 子命令（移动 RN 栈） |
| templates/prompt-templates/flutter.md | Flutter Prompt 模板 | design 子命令（Flutter 栈） |
| canvas-fonts/ | 字体资源（TTF + OFL 授权） | creative 子命令 |
| themes/ | 10 个预设主题数据 | theme 子命令 |
| references/design-systems/tdesign.md | TDesign 风格设计系统预设（9-section） | design-context / theme 子命令 |
| references/design-systems/ant-design.md | Ant Design 风格设计系统预设（9-section） | design-context / theme 子命令 |
| references/design-systems/material-3.md | Material 3 风格设计系统预设（9-section） | design-context / theme 子命令 |
| references/design-systems/shadcn-style.md | shadcn 风格设计系统预设（9-section） | design-context / theme 子命令 |
| scripts/search.py | CLI 搜索工具 | design 子命令 |
| scripts/audit_integrity.py | 结构自检门禁：断链/孤儿资源/数字对账/政策数字对账/围栏配对 | 交付前自检 |
| scripts/slop_scan.py | 静态反 AI 味门禁：30 条规则扫 html/css，退出码 0/1/2；`--only 规则号` 可单点复检 | review / critique |
| scripts/render_probe.py | 渲染量测门禁：对比度/横向滚动/触摸目标/焦点/alt/label（Playwright 离线）；`--apca` 加量 APCA 感知对比度 Lc | review / critique |
| scripts/apca_contrast.mjs | APCA Lc 计算器（colorjs.io，stdin 收前景/背景，算不出给 null 不猜） | render_probe --apca |
| scripts/token_lint.py | Token 门禁：未定义引用、死 token、与 DESIGN.md 契约双向对账（纯标准库） | design / review |
| scripts/visual_diff.py | 参考图对账：截图、逐像素差异、白屏与内容密度兜底（Playwright + Pillow） | review（有参考图时） |
| scripts/structure_lint.mjs | 结构层门禁：stylelint 真解析 CSS + html-validate 真校验标记（需项目本地 `.sfd-tools`，无全局安装） | design / review |
| rules/gates.json | 六道门禁清单（脚本路径、触发时机、是否可选），audit_integrity 用它反查文档一致性 | 交付前自检 |
| rules/stylelint.config.json | 结构层的 CSS 规则表（颜色/字体必须走 var()，属性名/函数/单位真校验） | structure_lint |
| rules/html-validate.config.json | 结构层的标记规则表（recommended + WCAG 项，关掉排版风格类规则） | structure_lint |
| templates/sfd-tools/package.json | 结构层依赖清单（6 个包，全 MIT）：复制到仓库根 `.sfd-tools` 后 `npm install --ignore-scripts` | 换机器时装结构层 |
| rules/slop-table.json | slop_scan 的判定表（规则即数据，阈值可溯源到条文） | review / critique |
| rules/policy.json | 政策数字的唯一真值源（字体上限、强调色面积、对比度阈值…），文档与门禁双向对账 | 交付前自检 |
| tests/slop_red.html | 反向夹具：每条规则必须被触发 | 门禁自测 |
| tests/slop_clean.html | 正向夹具：不得报任何硬判定 | 门禁自测 |
| tests/token_clean.css | Token 正向夹具 | 门禁自测 |
| tests/token_red.html | Token 反向夹具（同行声明、缺失 token、死 token） | 门禁自测 |
| tests/design_contract.md | DESIGN.md 契约对账夹具 | 门禁自测 |
| tests/test_slop_scan.py | slop_scan 契约测试（8 项），证明扫描器真能变红 | 交付前自检 |
| tests/test_token_lint.py | token_lint 契约测试（12 项）：误判回归 + 契约对账 + 空扫描/拼错参数必须拒跑 | 交付前自检 |
| tests/test_visual_diff.py | visual_diff 契约测试（13 项）：白屏兜底、尺寸不符未比对面积、UTF-8 输出 | 交付前自检 |
| tests/test_render_probe.py | render_probe 契约测试（10 项）：真浏览器量对比度/横向滚动/alt + APCA 参考值锚定；无 Playwright 时退出 2，不许"没量到"当成通过 | 交付前自检 |
| tests/test_structure_lint.py | structure_lint 契约测试（9 项）：var() 不误判、硬编码色必抓、配错规则名/指错 --tools 都 exit 2 | 交付前自检 |
| tests/test_audit_gate_red.py | 往副本注入 12 类缺陷 + 1 项参数拼写拒跑（共 13 项），证明结构门禁会红、参数拼错会拒跑 | 交付前自检 |

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
| 反参考 | 用户明确要避开的方向/品牌/感觉，写入 Design Brief 全程生效 | SKILL.md §3.5 第1轮 |
| 参考距离分级 | 场景决定参考可走多深：Operate 结构借鉴 / Persuade·Experience 原理解构 / Read 结构为主 | subskills/research/SKILL.md |

### 7.2 阶段间传递格式

子命令串联时，输出必须包含传递给下一阶段的结构化数据块：

```
---pass-to-next---
brand-personality: {品牌人格类型}
mood-board: [{词1}, {词2}, {词3}]
mood-board-derivation: {色相策略 / 字体气质 / 材质 / 动效性格}
anti-references: [{要避开1}, {要避开2}, ...]
reference-distance: {结构借鉴 | 原理解构 | 显式复制}
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
- `research` 产出 → 品牌人格 + 情绪板（含推导）+ 设计禁忌 + 反参考 + 参考距离等级（第 1 轮与第 4 轮调研）
- `design-context` 产出 → PRODUCT.md + DESIGN.md（设计上下文持久化）
- `creative` 产出 → 视觉论文（5个方向决策）
- `theme` 消费 → 品牌人格 + 视觉论文，产出 Design Token
- `design` 消费 → Design Token + 品牌人格 + 视觉论文 + 设计禁忌 + 设计上下文，产出可运行代码
- `review/critique` 消费 → 代码 + Design Token + 品牌人格 + 视觉论文 + 情绪板 + 设计禁忌 + 设计上下文，产出审查报告

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

- ✅ **⚠️ 先调研再设计（铁律）**：路由到 `design` 时，必须先加载 `subskills/research/SKILL.md`，通过 AskUserQuestion 完成至少 1 轮调研对话，再加载 `subskills/design-context/SKILL.md` 初始化设计上下文，产出 Design Brief + PRODUCT.md + DESIGN.md 后才能进入 design 子技能。**无 Design Brief 和设计上下文 = 拒绝执行 design。** 不存在"需求明确可跳过"的例外。
- ✅ **先路由再执行**：不要跳过子命令加载，必须先确定路由并加载对应 SKILL.md
- ✅ **保持 Design Token 一致性**：跨子命令共享同一套 Design Token 系统
- ✅ **每个阶段结束自动触发 review 审查**：调用 subskills/review/SKILL.md（基于 impeccable），形成质量闭环
- ✅ **遵循各子命令的完整工作流**：不要省略步骤，每个步骤都有其目的
- ✅ **输出可运行的代码**：design 子命令输出的代码必须可直接运行
- ✅ **交付前跑六道门禁**（清单见 `rules/gates.json`，改哪条都要同步这里）：改过本 Skill 的任何文件 → `python ${SKILL_DIR}/scripts/audit_integrity.py`；产出了 UI 代码 → `slop_scan.py <产物路径>`（静态反 AI 味）、`token_lint.py <产物>`（Token 与 DESIGN.md 对账）、`render_probe.py <产物.html>`（对比度/横向滚动/焦点/alt，Playwright 离线）、`node ${SKILL_DIR}/scripts/structure_lint.mjs <产物>`（stylelint + html-validate 真解析，需项目本地 `.sfd-tools`：`cp -r ${SKILL_DIR}/templates/sfd-tools <仓库根>/.sfd-tools && cd <仓库根>/.sfd-tools && npm install --ignore-scripts`；没装时退出码 2 并说明，不许当成通过），`render_probe.py --apca` 还会用 colorjs.io 量 APCA 感知对比度（Lc 阈值只认 `rules/policy.json`），有参考图时再跑 `visual_diff.py check <产物.html> --reference 参考图.png`。任一退出码非 0 视为未完成，不得声称已修好；退出码 2 表示根本没扫到东西或参数拼错，同样不算通过。改过门禁脚本本身还要跑 `tests/` 下的契约测试与 `test_audit_gate_red.py`
- ✅ **语义化 Token**：所有颜色、间距、字体使用语义化命名，并用 `token_lint.py` 证明没有未定义引用与死 Token
- ✅ **全网搜索结果必须经过解构优化**：不可直接照搬搜索结果，必须经过解构→分析→融合→优化四步流程
- ✅ **跨领域借鉴**：设计思考不局限于 UI 领域，主动从建筑、时尚、工业设计等领域获取灵感
- ✅ **去 AI 味**：所有设计输出必须经过反 AI 味检查清单，禁止蓝紫渐变、emoji 图标、均匀间距等 AI 味特征开端
- ✅ **项目设计规范优先**：项目根存在 DESIGN.md / PRODUCT.md 时，涉及该项目的任何设计 / 优化 / refine / theme / animate 请求，必须先读 DESIGN.md 并以它为风格基准；用户要求偏离既有规范时，明确确认后再执行（见 §3.6）

### 禁止行为

- ❌ **跳过需求调研直接设计**：路由到 `design` 时必须先完成 research 调研，必须弹出 AskUserQuestion 对话。违反此规则视为 Skill 执行失败
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
| "做一个 landing page" | research → design-context → design | 先调研再初始化上下文再设计 |
| "设计一个 dashboard" | research → design-context → design | 先调研再初始化上下文再设计 |
| "设计一个后端管理页面" | research → design-context → design | 先搜索参考再初始化上下文再设计 |
| "帮我选个配色方案" | theme | 色板 + Design Token |
| "适配 dark mode" | theme | 暗色模式主题 |
| "审查一下我的 UI" | review | 快速设计质量审查 |
| "深度审查我的设计" | critique | 双代理深度审查 + 探测器规则 |
| "初始化设计上下文" | design-context | 创建 PRODUCT.md + DESIGN.md |
| "polish 一下这个页面" | refine | 上线前最终打磨 |
| "bolder 一点" | refine | 增强视觉冲击力 |
| "quieter 一点" | refine | 降低视觉噪音 |
| "distill 一下内容" | refine | 精简冗余内容 |
| "harden 一下性能" | refine | 性能与错误处理加固 |
| "添加动效" | animate | 动效设计与实现 |
| "从零开始设计一个网站" | 完整工作流 | research → design-context → creative → theme → design → review/critique |
| "搜索一下后台管理的设计灵感" | research | 全网搜索 + 解构优化 |
| "优化一下界面" | research（重新调研）→ design-context → design；**保持现有风格时**走 §3.6 审计流程 | ⚠️ 优化=重新设计，不是审查！必须先重新调研（尤其动效/字体/交互节奏可能已变） |
| "按现有风格重构" / "统一一下风格" | **§3.6 现有风格重构流程** | 风格基准已存在：先审计后统一，设计稿确认再动手 |

### 子命令速查

```
| research     | subskills/research/SKILL.md          | 需求调研、全网搜索、参考解构、Design Brief 输出 |
| design-context | subskills/design-context/SKILL.md  | 设计上下文初始化、PRODUCT.md/DESIGN.md 生成、访客意图分类 |
| creative     | subskills/creative/SKILL.md          | 灵感探索、生成艺术、海报设计、视觉表达 |
| theme        | subskills/theme/SKILL.md             | 配色方案、字体搭配、主题系统、品牌规范 |
| design       | subskills/design/SKILL.md            | 页面设计、组件开发、UI实现、代码输出 |
| review       | subskills/review/SKILL.md            | 快速审查、质量评分、可访问性检查、改进建议 |
| critique     | subskills/critique/SKILL.md          | 深度审查、双代理评估、探测器规则、上线前检查 |
| refine       | subskills/refine/SKILL.md            | 命令式优化（polish/bolder/quieter/distill/harden） |
| animate      | subskills/animate/SKILL.md           | 动效设计、Motion/GSAP 选择、时序编排、缓动曲线 |
```

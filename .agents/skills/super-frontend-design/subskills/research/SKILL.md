---
name: super-frontend-design:research
version: 2.7.0
description: |
  需求调研与参考解构模块。通过 5 轮 AskUserQuestion 结构化对话明确设计需求（品牌人格、情绪板、设计禁忌），
  全网搜索设计作品平台提取真实UI资产，解构竞品并生成 Design Brief。
  由 super-frontend-design 主入口路由调用。
  合并来源：research + web-search + 任意网站Token提取
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# Research — 需求调研 + 全网搜索

## 目标

在任何设计执行前，通过 **AskUserQuestion 工具** 进行结构化对话，明确用户的真实需求，避免"开盲盒"式设计。

## 核心要求（铁律）

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

> 📌 **重构场景的合法替代**：用户要求"按现有风格重构 / 统一风格"时，走下方「现有风格审计模式」——同样必须用 AskUserQuestion 与用户确认（统一方案），但调研对象是**现有代码库**而非从零询问 5 轮问卷。铁律 2 禁止的仍是跨会话 / 跨项目的历史偏好数据；**本项目现有代码、DESIGN.md、PRODUCT.md 是合法且必要的审计对象**。

## 对话执行流程

调研对话分为 **5 轮**，每轮使用 AskUserQuestion 工具提出 2-4 个问题：

---

### 第 1 轮：设计类型 + 企业参考

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

### 第 2 轮：风格 + 配色 + 暗色模式

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

### 第 3 轮：技术栈 + 响应式 + 交互

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

### 第 4 轮：品牌人格 + 情绪板 + 设计禁忌（决定设计灵魂）

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
  - "playful + 趣味 + 轻松"
  - "粗野 + raw + 真实"
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

### 第 5 轮：动效与粒子效果 + 交互节奏感 + 字体偏好（决定体验灵魂）

> ⚠️ **本轮是调研的核心环节之一**。动效和粒子效果不是事后添加的装饰，而是设计决策的一部分，必须在调研阶段明确方向。不同场景对应完全不同的动效策略：

**场景 × 动效推荐映射（供 AI 参考，不直接展示给用户）：**

| 设计场景 | 推荐动效方向 | 粒子效果 | 交互节奏 |
|----------|-------------|---------|---------|
| 产品官网 / Landing Page | 滚动驱动（ScrollTrigger）+ 入场 reveal + 数字计数 | 可选低密度背景粒子 | 中等偏慢，强调仪式感 |
| 后台管理系统 | 无或极简 fade/slide，状态切换过渡 | ❌ 禁止 | 快，追求效率感 |
| 移动端 App | 手势驱动微交互 + 页面转场 | 视场景定 | 快，流畅响应 |
| 数据 Dashboard | 图表渐进绘制 + 数字步进 | ❌ 禁止 | 快，信息优先 |
| 品牌展示页 / 作品集 | 沉浸式 3D / WebGL / 视差层叠 | 可选创意粒子 | 慢，强调氛围感 |
| 电商 / 营销落地页 | 弹性入场 + hover 反馈 + CTA 突出 | 可选少量装饰 | 中，引导转化 |
| 教育 / 内容平台 | 温和 fade + 进度指示 | ❌ 禁止 | 中偏慢，舒适阅读 |
| 金融科技 | 无动效或极简数据过渡 | ❌ 禁止 | 快，专业克制 |
| 游戏品牌 / 娱乐 | 粒子系统 + shader 效果 + 霓虹 glow | ✅ 强烈推荐 | 快，能量感 |
| 工具 / SaaS 产品 | 功能性动效（loading、success state） | ❌ 禁止 | 快，实用优先 |

---

**问题 13 — 动效与粒子效果：**
```
header: "动效与粒子效果"
question: "你希望这个设计有多少动效和粒子效果？"
options:
  - "无动效，纯静态" → 适合后台、Dashboard、金融科技，追求效率和专业感
  - "少量微交互" → 仅 hover/focus 状态反馈，简单 fade/slide 入场
  - "中等动效" → 滚动驱动动画（ScrollTrigger）、数字计数、渐入揭示
  - "丰富动效" → 复杂时间轴编排、SplitText 文字动画、视差层叠
  - "需要粒子效果 / WebGL" → 粒子背景、Shader 效果、3D 沉浸体验
  - "不确定，按场景推荐"
multiSelect: false
```

**问题 14 — 交互节奏感：**
```
header: "交互节奏感"
question: "用户在这个页面上的操作节奏应该是怎样的？"
options:
  - "快速高效" → 操作反馈迅速，动效短促（150-300ms），追求生产力
  - "流畅自然" → 标准交互节奏（300-500ms），平衡美观与效率
  - "沉浸体验" → 动效舒缓（500-1000ms），强调视觉叙事和品牌氛围
  - "活力动感" → 动效富有弹性和能量感（spring 物理效果）
  - "不确定，按场景推荐"
multiSelect: false
```

**问题 15 — 字体风格偏好：**
```
header: "字体风格"
question: "你偏好什么样的字体风格？"
options:
  - "无衬线现代" → Inter, SF Pro, Roboto, Helvetica — 干净、专业、通用
  - "衬线优雅" → Playfair Display, Lora, Georgia — 精致、文艺、高端感
  - "等宽极客" → JetBrains Mono, Fira Code, Geist Mono — 技术感、代码感
  - "混搭组合" → 衬线标题 + 无衬线正文（杂志感）
  - "有趣个性" → 圆润/手写/实验性字体（如 Quicksand, Nunito）
  - "不确定，按场景推荐"
multiSelect: false
```

---

## 对话执行规则

1. **每次使用 AskUserQuestion 工具**，最多 4 个问题，优先第 1-3 轮
2. **用户回答后**，根据回答内容追问或进入下一轮
3. **如果用户跳过某个问题**，使用默认值（记录在 Design Brief 中标记为"默认假设"）
4. **如果用户说"随便"、"都行"、"你推荐"** → 基于设计类型自动推荐最佳方案
5. **每轮对话结束后**，简要总结用户的选择，确认理解无误
6. **第 4 轮（品牌人格）和第 5 轮（动效/交互/字体）不可跳过**：第 4 轮决定设计灵魂，第 5 轮决定体验品质

## 快捷模式（严格限制）

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

## 现有风格审计模式（按现有风格 / 统一风格重构专用）

> **触发**：用户要求"按现有风格重构""统一一下风格""保持现有风格"等——风格基准已经存在，调研对象是**现有代码库**，不是用户的想象。这是 5 轮问卷在重构场景的**替代模式**（并列，不是精简版）。
>
> **为什么独立成模式**："按现有风格"意味着答案写在代码里——调研要做的是**审计现状、找出不一致、与用户确认统一方案**；从零问"想参考哪家产品""什么风格"全部问错方向。

### Step 1 扫描与门禁测量（先拿证据，再开口）

扫描现有代码库的设计用法：
- CSS 变量（:root 定义）与样式文件中的实际用法（同一角色的裸值 / var() 混用情况）
- 设计系统文件（design-system.md、tokens.json、项目根 DESIGN.md）
- 框架配置（tailwind.config.js、theme.config.ts、components.json 等）
- 组件 / 页面文件中的硬编码值抽查（重点：同一角色出现多个值的场景）

对现有代码跑门禁测量（findings 即机器证据）：
- `python scripts/token_lint.py <现有代码路径>` —— 未定义引用 / 死 Token / 与 DESIGN.md 契约对账
- `python scripts/slop_scan.py <现有代码目录> --only font-size-step-count,radius-value-count,bare-hex-outside-root` —— 字号 / 圆角 / 裸色档位收敛度

产出**风格画像**：主色 / 背景 / 文字 / 字体 / 圆角 / 间距的现状提取（提取维度参照「任意网站品牌Token提取流程」Step 2，对象换成自有代码）。

### Step 2 不一致点清单

汇总三类证据，每条附文件:行号：

| 来源 | 示例 |
|------|------|
| 门禁 findings | `radius-value-count：6 档圆角（3/6/10/12/16/999px）@ src/styles/` |
| 目测核对 | 主色 3 个值：#0F766E ×24 / #10B981 ×7 / #059669 ×3 → 建议统一 #0F766E |
| 用户已知痛点 | "颜色太乱" → 归并到具体条目再确认 |

### Step 3 统一方案确认（AskUserQuestion）

- 逐项确认：保留哪个值 / 统一到哪个 / 哪些要改 / 是否借机调整（如换主色）
- 品牌人格 / 情绪板 / 设计禁忌：**从现有证据推导**（色彩 / 字体 / 密度 → 人格映射，参照「任意网站品牌Token提取流程」Step 3），请用户确认或修正——不从零询问
- 用户说"随便"时给推荐并请确认，不省略此步

### Step 4 输出与移交

- Design Brief（追加标记 `refactor-mode: style-audit`）+ 风格画像 + 统一方案
- 移交 `design-context`：按其 §7.1 提取机制生成统一设计稿（DESIGN.md）→ 用户确认（硬门）→ 进入 design（见主 SKILL.md §3.6）

## 调研输出：Design Brief（需求简报）

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
- 动效需求：{无动效/微交互/中等动效/丰富动效/粒子效果}
- 动效强度：{快/标准/慢/弹性质感}
- 交互节奏：{快速高效/流畅自然/沉浸体验/活力动感}
- 粒子/WebGL：{不需要/可选/强烈推荐}
- 响应式：{桌面/平板/手机/全适配}

## 风格系统
- 视觉风格：{极简/科技/活泼/专业/...}
- 暗色模式：{需要/不需要/仅暗色}
- 品牌色：{色值或描述}
- 字体风格：{无衬线现代/衬线优雅/等宽极客/混搭组合/有趣个性}
- 排除风格：{不要什么}

## 设计灵魂（第 4-5 轮产出）
- 品牌人格：{极客工程师/优雅艺术家/活力创业者/权威专家/温暖朋友/叛逆先锋/极简主义者/创意总监/数据驱动/奢华高端/环保自然/游戏品牌/教育品牌/金融科技}
- 情绪板：{3个关键词}
- 设计禁忌：{绝对不能出现的元素列表}
- 竞品拆解：{喜欢的竞品 + 具体喜欢的点 + 提取的方向}
- 文案调性：{专业/轻松/幽默/温暖/权威/简洁}
- 动效方向：{无动效/微交互/中等动效/丰富动效/粒子效果}
- 动效强度：{快速高效/流畅自然/沉浸体验/活力动感}
- 字体风格：{无衬线现代/衬线优雅/等宽极客/混搭组合/有趣个性}
- 场景推荐：{基于设计类型自动推荐的动效/粒子/节奏方案}

## 技术约束
- 技术栈：{React/Vue/HTML/Flutter/...}
- 性能要求：{描述}
- 国际化：{需要/不需要}
```

## DESIGN.md 产出（v2.0 格式）

research 阶段对话全部完成后，**必须**生成 `output/design-system.md` 文件，严格遵循 [references/design-system-template.md](../../references/design-system-template.md) 的 9-section 格式：

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

## 大企业参考风格速查

> v2.1.0：完整的 60+ 全球品牌设计系统目录见 [references/corporate-design-systems.md](../../references/corporate-design-systems.md)

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

## 任意网站品牌Token提取流程

当用户提供任意网站URL（如"参考 https://example.com 的风格"）且该网站不在 corporate-design-systems.md 预置目录中时：

### Step 1: 获取网站内容
- 使用 WebFetch 获取目标网站HTML
- 若WebFetch内容不全，用Grep搜索内联样式和CSS链接

### Step 2: 提取关键Design Token
- **主色**: 提取导航栏背景、CTA按钮颜色、品牌logo颜色
- **背景色**: 提取body/background颜色
- **文字色**: 提取正文文字颜色、标题文字颜色
- **字体**: 从font-family提取（标题字体 + 正文字体）
- **圆角**: 从border-radius提取按钮/卡片的圆角值
- **阴影**: 从box-shadow提取阴影特征（无阴影/轻微/厚重）
- **间距感**: 观察section padding判断留白密度

### Step 3: 推导品牌人格
基于提取的Token推导品牌人格：
- 大留白 + 轻字重 + 小圆角 → 极简主义者
- 深色背景 + 单一亮色accent → 极客工程师
- 暖色 + 大圆角 + 柔和阴影 → 温暖朋友
- 衬线字体 + 金色/金属色 + 精致间距 → 奢华高端
- 高对比 + 粗边框 + 非对称 → 叛逆先锋

### Step 4: 用户确认
展示提取结果给用户确认：
"从 {url} 提取到设计Token：
- 主色: #xxxxx
- 背景: #xxxxx
- 字体: Xxx
- 圆角: {px}
- 品牌人格推导: {类型}
是否使用此风格？[确认 / 调整]"

### Step 5: 注入DESIGN.md
用户确认后，将提取的Token注入output/design-system.md的对应Section。

## hallmark Study Verb — 任意网站Macrostructure+Theme提取

> hallmark的Study Verb核心能力：从任意参考网站提取其使用的Macrostructure和Theme，生成可复用的`portable design.md`。

当用户提供参考网站URL且需要分析其结构特征时使用此流程：

### Step 1: 获取网站内容
- 使用 WebFetch 获取目标网站首页HTML
- 分析页面结构：导航位置、Hero布局、section序列、Bento/卡片使用、CTA位置、图片布局

### Step 2: 识别Macrostructure
加载 `references/macrostructures.md`，根据页面结构匹配最接近的Macrostructure：

| 识别信号 | 对应Macrostructure |
|---------|-------------------|
| 全幅标题+大CTA+极简 | 01-Punchy / 05-Symmetric |
| 标题→特性→Bento→CTA序列 | 02-Storytelling / 10-Showcase |
| 全屏图片+文字叠加 | 08-Editorial / 15-Cinematic |
| 暗色+数据密集布局 | 12-Data-Dense / 16-Command |
| 画廊式多图布局 | 09-Gallery / 20-Experimental |
| 标准居中Hero+卡片网格 | 03-Human / 04-Modern |

### Step 3: 识别Theme
加载 `references/themes.md`，根据配色/字体/氛围匹配最接近的Theme：

| 视觉信号 | 对应Theme |
|---------|----------|
| 黑底白字+单一accent色 | Luxurious / Dark Confidence |
| 彩色渐变+大胆排版 | Bold / Electric Energy |
| 极简黑白+大量留白 | Minimal / Refined Classic |
| 暖色调+圆润形状 | Warm / Human Optimistic |
| 冷色调+几何形状 | Futuristic / Confident Tech |

### Step 4: 输出Portable Design.md
生成`output/portable-design.md`，格式如下：

```markdown
## Portable Design — {参考网站名称}

### Macrostructure: {编号}-{名称}
- 结构描述: {简要描述}
- 适用场景: {哪些场景适合}
- 结构骨架: {各section的顺序和职责}

### Theme: {主题名称}
- 配色方向: {主色/背景/文字色}
- 字体组合: {标题/正文}
- 氛围: {关键词}

### 可复用设计决策
1. {决策1}
2. {决策2}
3. {决策3}

### 不推荐复制的部分
- {需要避免的元素}
```

### Step 5: 注入Design Brief
将portable-design.md的关键信息注入到research的Design Brief中，供design子技能使用。

## 全网搜索设计参考

> ⚠️ **搜索目标：找设计作品/界面截图/组件模板，不是找文章/博客/教程。**

### 搜索源分类

#### ✅ 设计作品平台（必须优先搜索 — 能找到真实的 UI 截图和组件）

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
| Cult UI | `site:cult-ui.com {关键词}` | 高级动效组件、金属/玻璃材质按钮、Apple设备mockup |
| Motion Examples | `site:motion.dev/examples {关键词}` | Motion库动画示例、spring物理动画、scroll动画 |

#### ❌ 科技博客/文章网站（绝对禁止搜索 — 只能看到理论文章，找不到实际 UI 模板）

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

### 搜索后强制步骤

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

### 搜索关键词构建模板

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

### 搜索策略

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
```

## 参考解构与综合优化（4 步流程）

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

## 跨领域设计借鉴

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

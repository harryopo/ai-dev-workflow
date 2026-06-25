---
name: design
version: 2.1.0
description: |
  UI/UX设计模块。综合设计智能，包含50+风格、161调色板、57字体配对、99 UX准则、25图表类型、10技术栈、shadcn/ui组件管理。
  由 super-frontend-design 主入口路由调用。
  合并来源：frontend-design + frontend-skill + frontend-ui + ui-ux-pro-max + web-design-guidelines + shadcn/ui
  v1.1.0: 集成全网搜索设计参考、参考解构与综合优化、跨领域设计借鉴
  v1.2.0: 新增调研守卫 — 无 Design Brief 时禁止执行，强制回退到 research 阶段
  v2.0.0: Block类型匹配(18种) + 5框架Prompt模板集成; v2.1.0: 企业设计系统参考目录集成
context: fork
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Design — UI/UX 综合设计智能

## 0. 执行前置条件（调研守卫）

> ⚠️ **在执行任何设计工作前，必须通过以下检查：**

### 必须满足（二选一）

| 条件 | 检查方式 |
|------|---------|
| **A. 主工作流传入 Design Brief** | 检查 `pass-data.yaml` 或父代理传递的 Design Brief 是否存在且包含 `brand-personality` 和 `mood-board` 字段 |
| **B. 本 Skill 独立调用时完成最小化调研** | 若独立调用（非主工作流串联），必须先执行最小化调研后再设计 |

### 不满足条件时的行为

**如果 A 和 B 都不满足 → 必须拒绝执行设计，并返回主入口要求先完成 research 阶段。**

返回消息模板：
```
⚠️ 缺少 Design Brief，无法开始设计。

请先完成需求调研（research 阶段），我需要知道：
1. 设计类型：后台管理系统 / 宣传落地页 / Dashboard / App 界面？
2. 目标受众：开发者 / 企业客户 / 普通消费者？
3. 视觉风格偏好：极简 / 科技 / 活泼 / 专业？

这些信息来自本次任务的具体需求，不能用历史偏好替代。
```

### 全局画像禁令

**绝对禁止**从以下来源自动填充设计参数：
- ❌ 用户全局画像（user profile）
- ❌ 历史偏好记忆（global memory / ontology）
- ❌ 其他会话的风格选择
- ❌ 其他项目的配色方案

每次设计任务的场景、受众、目标都不同，不可复用历史数据。

---

## Part 1: 艺术方向与高级设计

### 核心原则：选择方向并坚持

目标：交付感觉刻意、高级、当代的界面。默认追求获奖级构图——一个大创意、强视觉、精简文案、严谨间距、少量令人难忘的动效。

### 设计工作流（从 Design Brief 提取，禁止自填）

> ⚠️ 以下 5 点必须从 Design Brief（或 pass-data.yaml）中**提取答案**，禁止自行判断或猜测。如果 Design Brief 中某字段缺失，必须向上游（research 阶段）请求补充，而非自行填充。

**必须从 Design Brief 中读取：**

1. **目的** → 读取 Design Brief「基本信息·核心目标」字段
2. **受众** → 读取 Design Brief「基本信息·目标受众」字段
3. **情感基调** → 读取 Design Brief「设计灵魂·品牌人格」字段（14 种之一）
4. **视觉方向** → 读取 Design Brief「风格系统·视觉风格」字段 + creative 子技能的视觉论文
5. **一个用户应记住的事** → 从情绪板 3 个关键词中提炼

**禁止行为：**
- ❌ 自己推理"这个场景应该用什么风格"
- ❌ 从全局画像/历史记录推断用户偏好
- ❌ 跳过 Design Brief 直接套用内置默认值

### Block 类型匹配（v2.0）

> 加载 `references/component-block-catalog.md`，根据 Design Brief 的场景描述自动匹配需要的 Block 类型。

**匹配规则**：

| 用户场景关键词 | 自动匹配的 Block |
|--------------|-----------------|
| "落地页" / "官网" / "landing page" | Hero + Features + CTA + Footer |
| "SaaS" / "定价页" | Hero + Features + Pricing + CTA |
| "后台" / "管理系统" / "admin" | Navigation + Data Tables + Forms + Cards |
| "Dashboard" / "仪表盘" | Navigation + Cards + Data Tables |
| "App" / "移动端" | Navigation + Cards + Forms |
| "博客" / "内容" | Hero + Blog Sections + Cards |
| "联系" / "表单" | Hero + Contact Sections |

**执行流程**：
1. 从 DESIGN.md §1 读取"设计类型"字段
2. 在 component-block-catalog.md 中查找匹配的 Block 列表
3. 对每个 Block 生成一张设计卡（参考 §7 Prompt 模板体系）
4. 设计卡输出到 `output/01-component-cards/`

### 工作模型（从上游输入组装，禁止自行创作）

在构建之前，从上游阶段结果中组装三个文档：

- **视觉论文 (visual thesis)** → 从 `pass-data.yaml` 的 `visual-thesis` 字段组装（creative 子技能产出）
- **内容计划 (content plan)** → 从 Design Brief「功能需求」字段组装，不自行决定需要什么区块
- **交互论文 (interaction thesis)** → 从 Design Brief「交互需求·动效需求」字段 + 品牌人格推导，非自行创意

每个区块获得一个职责、一个主导视觉想法、一个主要收获或行动。

### 美丽默认值

- 从构图开始，而非组件
- 偏好全出血 hero 或全画布视觉锚点
- 让品牌或产品名称成为最响亮的文字
- 保持文案短到几秒内可扫描
- 在添加装饰之前，先使用留白、对齐、缩放、裁剪和对比
- 限制系统：最多两种字体，默认一种强调色
- 默认无卡片布局。使用区块、列、分隔线、列表和媒体块
- 将第一视口视为海报，而非文档

### 落地页规则

默认序列：

1. **Hero**：品牌或产品、承诺、CTA、一个主导视觉
2. **Support**：一个具体功能、优惠或证明点
3. **Detail**：氛围、工作流、产品深度或故事
4. **Final CTA**：转化、开始、访问或联系

**Hero 规则：**

- 只有一个构图
- 全出血图片或主导视觉平面
- 规范全出血规则：在品牌落地页上，hero 本身必须边到边运行，没有继承的页面沟槽、框架容器或共享 max-width；只约束内部文本/行动列
- 品牌第一、标题第二、正文第三、CTA 第四
- 默认不要 hero 卡片、统计条、logo 云、药丸汤或浮动仪表板
- 桌面标题保持约 2-3 行，移动端一目了然
- 保持文本列窄并锚定到图像的平静区域
- 图像上的所有文字必须保持强对比度和清晰的点击目标

**视口预算：**

- 如果第一屏包含 sticky/fixed 头部，该头部计入 hero。组合的 header + hero 内容必须在常见桌面和移动尺寸的初始视口内
- 使用 `100vh`/`100svh` hero 时，减去持久 UI chrome（`calc(100svh - header-height)`）或叠加 header 而非在正常流中堆叠

**检验：** 如果移除图片后第一视口仍然有效，图片太弱。如果隐藏导航后品牌消失，层级太弱。

### App UI 风格（根据品牌人格自适应，禁止硬编码）

> ⚠️ App UI 风格必须从 Design Brief 的品牌人格推导，**禁止**所有场景都默认使用 Linear 风格。

根据品牌人格选择 App UI 基调：

| 品牌人格 | App UI 基调 | 特征 |
|----------|-----------|------|
| 极客工程师 | **Linear 风格克制** | 暗色为主、极简线条、等宽字体、Command+K 感、功能即设计 |
| 优雅艺术家 | **精雕细琢** | 圆角柔和的卡片、精致阴影层次、衬线字体点缀、艺术感微交互 |
| 活力创业者 | **明亮大胆** | 强品牌色、大圆角、弹性动效、积极向上的氛围 |
| 权威专家 | **紧凑专业** | 数据密集、清晰表格、稳重配色、功能优先 |
| 温暖朋友 | **友好柔和** | 暖色调、圆润形状、亲和力文案、手写感元素 |
| 叛逆先锋 | **粗野实验** | 不对称布局、高对比、打破常规、原始感 |
| 极简主义者 | **Ultra-minimal** | 黑白为主、几乎无装饰、极致留白、单一字体 |
| 创意总监 | **实验大胆** | 撞色拼接、非传统布局、Split Screen、大字体混搭 |
| 数据驱动 | **数据至上** | Dashboard 风格、KPI Cards、Chart Grid、冷色调数据色板 |
| 奢华高端 | **极致奢华** | 大幅 Hero、Serif 标题、黑白金配色、戏剧性排版 |
| 环保自然 | **自然有机** | 大地色调、有机形状卡片、柔和过渡、自然图片 |
| 游戏品牌 | **沉浸电竞** | 暗色沉浸、霓虹 Glow、粒子效果、排行榜 |
| 教育品牌 | **清晰友好** | 明亮安全色、大字体、进度指示器、可访问性优先 |
| 金融科技 | **可靠精确** | 深蓝+深绿、数据表格、金额格式化、稳重配色 |

**未指定品牌人格时**：不允许假设默认值，必须向上游请求品牌人格。

**通用 App UI 组织原则（所有风格共享）：**

围绕以下元素组织：
- 主要工作区
- 导航
- 次要上下文或检查器
- 一个清晰的强调色用于行动或状态

**避免（所有风格）：**
- dashboard-card 马赛克
- 每个区域上的粗边框
- 常规产品 UI 背后的装饰渐变
- 多个竞争的强调色
- 不改善扫描的装饰性图标

如果面板可以在不丢失含义的情况下变为普通布局，移除卡片处理。

### 图像规则

图像必须做叙事工作：

- 为品牌、场地、编辑页面和生活方式产品使用至少一张强有力、真实的图像
- 偏好场景摄影而非抽象渐变或假 3D 对象
- 选择或裁剪具有稳定色调区域的图像用于文字
- 不使用带有嵌入式标牌、logo 或与 UI 争夺的排版杂乱的图像
- 不生成带有内置 UI 框、分割、卡片或面板的图像
- 如果需要多个时刻，使用多张图片，而非一张拼贴

第一视口需要真实的视觉锚点。装饰性纹理不够。

### 文案原则

- 用产品语言写作，而非设计评论
- 让标题承载含义
- 支持文案通常应是一句短句
- 削减区块间的重复
- 不在 UI 中包含提示语言或设计评论
- 给每个区块一个职责：解释、证明、深化或转化

**如果删除 30% 的文案能改善页面，继续删除。**

### 产品 UI 的实用文案

当工作是仪表板、应用界面、管理工具或操作工作区时，默认使用实用文案而非营销文案：

- 优先方向、状态和行动，而非承诺、情绪或品牌声音
- 从工作表面本身开始：KPI、图表、过滤器、表格、状态或任务上下文。除非用户明确要求，否则不要引入 hero 区块
- 区块标题应说明区域是什么或用户可以在那里做什么
  - 好："Selected KPIs"、"Plan status"、"Search metrics"、"Top segments"、"Last sync"
  - 避免：渴望型 hero 行、隐喻、活动风格语言和执行摘要横幅
- 支持文本应在一句话中解释范围、行为、新鲜度或决策价值
- 如果一句话可以出现在首页 hero 或广告中，重写它直到听起来像产品 UI
- 如果一个区块不能帮助某人操作、监控或决策，移除它
- **试金石检查**：如果操作员只扫描标题、标签和数字，他们能立即理解页面吗？

### 动效（艺术方向）

使用动效创造存在感和层级，而非噪音。

为视觉主导的工作交付至少 2-3 个有意动效：

- hero 中的一个入场序列
- 一个滚动链接、sticky 或深度效果
- 一个 hover、reveal 或布局过渡，增强可操作性

偏好 Framer Motion（当可用时）用于：

- 区块 reveal
- 共享布局过渡
- 滚动链接的 opacity、translate 或 scale 变化
- sticky 叙事
- 推进叙事的轮播，而非仅填充空间
- 菜单、抽屉和模态存在效果

**动效规则：**

- 在快速录屏中可注意到
- 在移动端流畅
- 快速且克制
- 在整个页面上一致
- 如果仅装饰性则移除

### 反模式

- 默认无卡片
- 默认无 hero 卡片
- 当简报要求全出血时，无框式或居中列 hero
- 每个区块不超过一个主导想法
- 没有区块需要许多小型 UI 设备来解释自己
- 在品牌页面上，标题不应压过品牌
- 无填充文案
- 除非文本位于平静、统一的一侧，否则无分屏 hero
- 除非产品已有强系统，否则不超过两种字体
- 不超过一种强调色

**拒绝这些失败：**

- 通用 SaaS 卡片网格作为第一印象
- 美丽图像但品牌存在感弱
- 强标题但无明确行动
- 文本背后繁忙的图像
- 重复相同情绪声明的区块
- 无叙事目的的轮播
- 由堆叠卡片而非布局构成的 App UI

### Litmus 检查

- 品牌或产品在第一屏是否无可误认？
- 是否有一个强视觉锚点？
- 仅通过扫描标题能否理解页面？
- 每个区块是否只有一个职责？
- 卡片是否真的必要？
- 动效是否改善了层级或氛围？
- 如果移除所有装饰性阴影，设计是否仍然感觉高级？

---

## Part 2: 风格与设计系统

### 风格选择规则

风格选择优先级表（按产品类型匹配）：

| 优先级 | 规则 | 说明 |
|--------|------|------|
| 1 | `style-match` | 风格匹配产品类型（使用 `--design-system` 获取推荐） |
| 2 | `consistency` | 所有页面使用相同风格 |
| 3 | `no-emoji-icons` | 使用 SVG 图标（Heroicons、Lucide），不用 emoji |
| 4 | `color-palette-from-product` | 从产品/行业选择调色板（搜索 `--domain color`） |
| 5 | `effects-match-style` | 阴影、模糊、圆角与所选风格对齐（glass/flat/clay 等） |
| 6 | `platform-adaptive` | 尊重平台习惯（iOS HIG vs Material）：导航、控件、排版、动效 |
| 7 | `state-clarity` | hover/pressed/disabled 状态视觉上区分但保持风格一致（Material state layers） |
| 8 | `elevation-consistent` | 卡片、sheet、模态使用一致的 elevation/shadow 刻度；避免随机阴影值 |
| 9 | `dark-mode-pairing` | 同时设计 light/dark 变体以保持品牌、对比度和风格一致 |
| 10 | `icon-style-consistent` | 整个产品使用一个图标集/视觉语言（笔画宽度、圆角半径） |
| 11 | `system-controls` | 偏好原生/系统控件而非完全自定义；仅在品牌需要时自定义（Apple HIG） |
| 12 | `blur-purpose` | 使用模糊表示背景消除（模态、sheet），而非装饰（Apple HIG） |
| 13 | `primary-action` | 每个屏幕应只有一个主要 CTA；次要行动视觉上从属（Apple HIG） |

### 可用风格列表（50+）

| # | 风格名称 | 关键特征 | 适用产品类型 |
|---|----------|----------|-------------|
| 1 | Minimalism | 大量留白、极少元素、功能优先 | SaaS、工具、文档 |
| 2 | Brutalism | 粗犷排版、高对比、原始网格 | 创意机构、艺术、Zine |
| 3 | Glassmorphism | 毛玻璃效果、半透明层、模糊背景 | 科技、金融、现代App |
| 4 | Neumorphism | 柔和凸起/凹陷、同色阴影 | 设置面板、计算器、控制 |
| 5 | Claymorphism | 膨胀圆角、柔和阴影、黏土质感 | 儿童、教育、趣味产品 |
| 6 | Skeuomorphism | 拟真材质、物理隐喻 | 音乐、阅读、奢侈品 |
| 7 | Flat Design 2.0 | 简洁色块、微妙层次、无装饰 | 企业、后台、通用 |
| 8 | Bento Grid | 网格卡片、不等比区块、信息密度 | 产品展示、功能概览 |
| 9 | Dark Mode First | 深色基底、霓虹强调、低亮度 | 开发者工具、游戏、媒体 |
| 10 | Responsive | 流体布局、弹性网格、自适应 | 所有通用 |
| 11 | Editorial/Magazine | 大标题、分栏、衬线字体 | 新闻、博客、出版 |
| 12 | Retro-Futuristic | 复古配色+未来元素、扫描线 | 游戏、音乐、创意 |
| 13 | Organic/Natural | 柔和曲线、自然色、不规则形状 | 健康、食品、环保 |
| 14 | Luxury/Refined | 金色点缀、衬线字体、大量留白 | 奢侈品、高端服务 |
| 15 | Playful/Toy-like | 圆角、鲜艳色、弹跳动效 | 儿童、游戏、社交 |
| 16 | Art Deco/Geometric | 几何图案、对称、金属色 | 酒店、时尚、活动 |
| 17 | Soft/Pastel | 柔和色调、圆角、轻阴影 | 婴儿、美容、冥想 |
| 18 | Industrial/Utilitarian | 单色、等宽字体、功能至上 | 工程、物流、数据 |
| 19 | Cyberpunk | 霓虹色、暗色基底、故障效果 | 游戏、加密、夜生活 |
| 20 | Swiss Design | 网格系统、无衬线、红黑 | 设计机构、建筑 |
| 21 | Vaporwave | 粉紫渐变、希腊雕塑、网格 | 音乐、艺术、亚文化 |
| 22 | Material Design | Material组件、elevation、ripple | Android、通用移动 |
| 23 | Apple HIG | SF字体、模糊、原生控件 | iOS、macOS应用 |
| 24 | Metro/Flat | 方块磁贴、纯色、无圆角 | 信息展示、仪表板 |
| 25 | Gradient Mesh | 多色渐变、流体形状、3D感 | 科技、创意、SaaS |
| 26 | Monochrome | 单色系、纹理变化、层次 | 摄影、作品集、时尚 |
| 27 | Maximalism | 丰富装饰、多层叠加、密集 | 创意、艺术、活动 |
| 28 | Neo-Brutalism | 粗边框、硬阴影、亮色 | 创业、个人品牌 |
| 29 | Aurora/Northern Lights | 流动渐变、深色背景、光效 | 科技、SaaS、创意 |
| 30 | Morphism | 介于flat和skeuo之间、微妙深度 | 通用、现代App |
| 31 | Isometric | 等轴测图、3D感、无透视 | 信息图、技术、教育 |
| 32 | Hand-drawn/Sketch | 手绘线条、不规则、温暖 | 教育、创意、笔记 |
| 33 | Typographic | 排版驱动、极少图像、字体艺术 | 出版、文化、品牌 |
| 34 | Cinematic | 全视口图像、慢过渡、叙事 | 电影、品牌、故事 |
| 35 | Corporate | 保守配色、结构化、专业 | 企业、金融、法律 |
| 36 | Startup/Modern | 渐变CTA、插图、活力 | 创业、科技、SaaS |
| 37 | E-commerce | 产品焦点、信任信号、转化 | 购物、零售、市场 |
| 38 | Dashboard/Data | 数据密度、图表、过滤器 | 分析、管理、监控 |
| 39 | Portfolio | 作品展示、个性表达、简约 | 设计师、摄影师、开发者 |
| 40 | Blog/Content | 阅读优先、排版舒适、导航 | 博客、杂志、新闻 |
| 41 | Mobile-first | 触摸友好、底部导航、紧凑 | 移动App、PWA |
| 42 | Print-inspired | 印刷质感、分栏、衬线 | 出版、文化、编辑 |
| 43 | Neon/Glow | 发光效果、暗色基底、高对比 | 夜生活、游戏、音乐 |
| 44 | Terrazzo/Pattern | 碎片图案、纹理、色块 | 室内、时尚、生活方式 |
| 45 | Duotone | 双色调、高对比、艺术 | 摄影、音乐、创意 |
| 46 | Frutiger Aero | 光泽、气泡、自然+科技 | 2000s风格、怀旧 |
| 47 | Y2K | 金属色、3D、未来感 | 时尚、音乐、Z世代 |
| 48 | Clean/Tech | 极简、等宽、功能 | 开发者、API、文档 |
| 49 | Whimsical | 异想天开、插画、趣味 | 儿童、教育、创意 |
| 50 | Professional | 克制、信任、权威 | 法律、医疗、金融 |
| 51 | Immersive | 全屏体验、3D、交互 | 游戏、品牌体验、展示 |
| 52 | Accessible-first | 高对比、大触控、屏幕阅读器 | 政府、医疗、通用 |

---

## Part 3: 色彩调色板（161 调色板）

### 色彩规则

| 规则 | 说明 |
|------|------|
| `color-semantic` | 定义语义色彩 token（primary、secondary、error、surface、on-surface），不在组件中使用原始 hex（Material color system） |
| `color-dark-mode` | 暗色模式使用去饱和/更浅色调变体，而非反转颜色；单独测试对比度（HIG, MD） |
| `color-accessible-pairs` | 前景/背景对必须满足 4.5:1 (AA) 或 7:1 (AAA)；使用工具验证（WCAG, MD） |
| `color-not-decorative-only` | 功能色（错误红、成功绿）必须包含图标/文本；避免仅色彩含义（HIG, MD） |
| `contrast-readability` | 浅色背景上使用深色文本（如 slate-900 on white） |

### 按产品类型的调色板类别

| 类别 | 产品类型 | 典型色系 | 调色板数量 |
|------|----------|----------|-----------|
| 科技/SaaS | SaaS、开发者工具、API | 蓝紫系、深色系、冷灰 | 25+ |
| 金融/企业 | 银行、保险、企业 | 深蓝、金色、灰绿 | 15+ |
| 健康/医疗 | 医疗、健身、心理健康 | 绿色系、蓝白、柔和 | 12+ |
| 教育/学习 | 在线课程、LMS、儿童 | 暖色、蓝橙、活泼 | 12+ |
| 电商/零售 | 购物、市场、品牌 | 红橙、信任蓝、活力 | 15+ |
| 创意/设计 | 作品集、机构、艺术 | 紫粉、渐变、大胆 | 15+ |
| 食品/餐饮 | 餐厅、外卖、食谱 | 暖橙、绿棕、食欲色 | 10+ |
| 旅行/酒店 | 酒店、航空、旅游 | 天蓝、沙金、自然 | 10+ |
| 社交/通讯 | 聊天、社区、约会 | 活力色、渐变、年轻 | 12+ |
| 媒体/娱乐 | 音乐、视频、游戏 | 霓虹、暗色、大胆 | 10+ |
| 房产/家居 | 地产、装修、家具 | 暖色、木色、中性 | 8+ |
| 法律/政府 | 政府、法律、合规 | 庄重蓝、灰、红 | 5+ |
| 通用/中性 | 通用、博客、文档 | 灰白、黑白、单色 | 12+ |

### 色彩语义系统

```
--color-primary        → 主要行动、品牌色
--color-secondary      → 次要行动、辅助
--color-accent         → 强调、注意
--color-destructive    → 危险、删除、错误
--color-success        → 成功、完成、确认
--color-warning        → 警告、注意
--color-info           → 信息、提示
--color-background     → 页面背景
--color-foreground     → 主文本
--color-muted          → 次要文本、禁用
--color-border         → 边框、分隔
--color-card           → 卡片背景
--color-popover        → 弹出层背景
--color-ring           → 焦点环
--color-input          → 输入框边框
--color-surface        → 表面（HIG/MD）
--color-on-surface     → 表面上的文本
```

### 暗色模式对比规则

- 暗色模式使用去饱和/更浅色调变体，而非反转颜色
- 单独测试暗色模式对比度（不假设亮色对比自动适用）
- `color-scheme: dark` 在 `<html>` 上（修复滚动条、输入框）
- `<meta name="theme-color">` 匹配页面背景
- 原生 `<select>`：显式 `background-color` 和 `color`（Windows 暗色模式）
- 设计 light/dark 变体时保持品牌、对比度和风格一致

---

## Part 4: 排版与字体配对（57 配对）

### 排版规则

| 规则 | 说明 |
|------|------|
| `line-height` | 正文使用 1.5-1.75 行高 |
| `line-length` | 限制每行 65-75 字符 |
| `font-pairing` | 匹配标题/正文字体个性 |
| `font-scale` | 一致的字号刻度（如 12 14 16 18 24 32） |
| `text-styles-system` | 使用平台排版系统：iOS 11 Dynamic Type / Material 5 type roles（display、headline、title、body、label）（HIG, MD） |
| `weight-hierarchy` | 用 font-weight 强化层级：粗体标题（600-700）、常规正文（400）、中等标签（500）（MD） |
| `truncation-strategy` | 偏好换行而非截断；截断时使用省略号并通过 tooltip/展开提供完整文本（Apple HIG） |
| `letter-spacing` | 尊重平台默认 letter-spacing；避免正文紧排（HIG, MD） |
| `number-tabular` | 数据列、价格和计时器使用 tabular/等宽数字以防止布局偏移 |
| `whitespace-balance` | 有意使用留白分组相关项和分隔区块；避免视觉杂乱（Apple HIG） |

### 字体配对类别表

| 类别 | 标题字体 | 正文字体 | 适用风格 |
|------|----------|----------|----------|
| 经典衬线 | Playfair Display / Crimson Pro / Lora | Source Sans 3 / Instrument Sans | Editorial、Luxury、出版 |
| 现代无衬线 | Outfit / Work Sans / Instrument Sans | DM Sans / Inter / IBM Plex Sans | SaaS、科技、企业 |
| 等宽技术 | JetBrains Mono / Geist Mono / IBM Plex Mono | IBM Plex Sans / Inter / Work Sans | 开发者工具、API文档 |
| 几何展示 | Poiret One / Italiana / Gloock | Outfit / Work Sans / Jura | 时尚、品牌、创意 |
| 圆润友好 | Nunito / Quicksand / Baloo 2 | Nunito Sans / Source Sans 3 | 儿童、教育、社交 |
| 工业力量 | Big Shoulders / Oswald / Anton | Barlow / IBM Plex Sans | 工业、物流、数据 |
| 复古怀旧 | Erica One / Boldonse / Nothing You Could Do | Crimson Pro / Lora / Libre Baskerville | 复古、音乐、艺术 |
| 未来科技 | Tektur / Smooch Sans / Red Hat Mono | Jura / Outfit / Work Sans | 科技、游戏、加密 |
| 极简主义 | National Park / Arsenal SC / Instrument Serif | Instrument Sans / Work Sans | 极简、建筑、设计 |
| 像素复古 | Silkscreen / Pixelify Sans / Press Start 2P | DM Mono / IBM Plex Mono | 游戏、像素风、怀旧 |
| 装饰艺术 | Young Serif / Bricolage Grotesque / Playfair | Outfit / Work Sans / DM Sans | 奢侈、酒店、时尚 |
| 中文衬线 | 思源宋体 / Noto Serif SC | 思源黑体 / Noto Sans SC | 中文出版、文化、教育 |
| 中文无衬线 | 钉钉进步体 / HarmonyOS Sans | 思源黑体 / Noto Sans SC | 中文科技、企业、SaaS |
| 日文混合 | Noto Sans JP / Zen Kaku Gothic | Noto Serif JP / Zen Old Mincho | 日文内容、文化 |
| 韩文混合 | Pretendard / Noto Sans KR | Noto Serif KR | 韩文内容、科技 |

### 排版系统规则

- 正文最小 16px（避免 iOS 自动缩放）
- 移动端每行 35-60 字符；桌面端 60-75 字符
- 使用 `text-wrap: balance` 或 `text-pretty` 在标题上（防止孤行）
- `font-variant-numeric: tabular-nums` 用于数字列/比较
- `…` 而非 `...`（省略号字符）
- 弯引号 `"` `"` 而非直引号
- 不间断空格：`10&nbsp;MB`、`⌘&nbsp;K`、品牌名
- 加载状态以 `…` 结尾：`"Loading…"`、`"Saving…"`

---

## Part 5: UX 准则（99 规则）

### 1. 可访问性（CRITICAL）

| ID | 规则 | 说明 |
|----|------|------|
| `color-contrast` | 最小 4.5:1 对比度 | 普通文本（大文本 3:1）；Material Design |
| `focus-states` | 可见焦点环 | 交互元素上 2-4px；Apple HIG, MD |
| `alt-text` | 描述性 alt 文本 | 有意义的图像 |
| `aria-labels` | aria-label | 仅图标按钮；原生使用 accessibilityLabel（Apple HIG） |
| `keyboard-nav` | Tab 顺序匹配视觉顺序 | 完整键盘支持（Apple HIG） |
| `form-labels` | 使用 label with for 属性 | |
| `skip-links` | 跳到主内容 | 键盘用户 |
| `heading-hierarchy` | 顺序 h1→h6 | 不跳级 |
| `color-not-only` | 不仅通过颜色传达信息 | 添加图标/文本 |
| `dynamic-type` | 支持系统文本缩放 | 避免文本增长时截断（Apple Dynamic Type, MD） |
| `reduced-motion` | 尊重 prefers-reduced-motion | 请求时减少/禁用动画（Apple Reduced Motion API, MD） |
| `voiceover-sr` | 有意义的 accessibilityLabel/accessibilityHint | VoiceOver/屏幕阅读器的逻辑阅读顺序（Apple HIG, MD） |
| `escape-routes` | 模态和多步流程中提供取消/返回 | Apple HIG |
| `keyboard-shortcuts` | 保留系统和 a11y 快捷键 | 为拖放提供键盘替代（Apple HIG） |

**额外规则（Web Design Guidelines）：**

- 仅图标按钮需要 `aria-label`
- 表单控件需要 `<label>` 或 `aria-label`
- 交互元素需要键盘处理器（`onKeyDown`/`onKeyUp`）
- `<button>` 用于行动，`<a>`/`<Link>` 用于导航（不是 `<div onClick>`）
- 图像需要 `alt`（装饰性则 `alt=""`）
- 装饰性图标需要 `aria-hidden="true"`
- 异步更新（toast、验证）需要 `aria-live="polite"`
- 在 ARIA 之前使用语义 HTML（`<button>`、`<a>`、`<label>`、`<table>`）
- 标题层次 `<h1>`–`<h6>`；包含跳转到主内容的链接
- 标题锚点上使用 `scroll-margin-top`

### 2. 触摸与交互（CRITICAL）

| ID | 规则 | 说明 |
|----|------|------|
| `touch-target-size` | 最小 44×44pt (Apple) / 48×48dp (Material) | 需要时扩展点击区域超出视觉边界 |
| `touch-spacing` | 触摸目标间最小 8px/8dp 间距 | Apple HIG, MD |
| `hover-vs-tap` | 使用 click/tap 作为主要交互 | 不单独依赖 hover |
| `loading-buttons` | 异步操作期间禁用按钮 | 显示 spinner 或进度 |
| `error-feedback` | 问题附近清晰错误消息 | |
| `cursor-pointer` | 可点击元素添加 cursor-pointer | Web |
| `gesture-conflicts` | 避免主内容上水平滑动 | 偏好垂直滚动 |
| `tap-delay` | 使用 touch-action: manipulation 减少 300ms 延迟 | Web |
| `standard-gestures` | 一致使用平台标准手势 | 不重新定义（如 swipe-back、pinch-zoom）（Apple HIG） |
| `system-gestures` | 不阻止系统手势 | Control Center、返回滑动等（Apple HIG） |
| `press-feedback` | 按压时视觉反馈 | ripple/highlight；MD state layers |
| `haptic-feedback` | 确认和重要行动使用触觉反馈 | 避免过度使用（Apple HIG） |
| `gesture-alternative` | 不依赖仅手势交互 | 始终为关键行动提供可见控件 |
| `safe-area-awareness` | 远离刘海、Dynamic Island、手势条和屏幕边缘放置主要触摸目标 | |
| `no-precision-required` | 避免需要精确点击小图标或薄边缘 | |
| `swipe-clarity` | 滑动操作必须显示清晰提示 | chevron、标签、教程 |
| `drag-threshold` | 开始拖动前使用移动阈值 | 避免意外拖动 |

**额外规则（Web Design Guidelines）：**

- `touch-action: manipulation`（防止双击缩放延迟）
- `-webkit-tap-highlight-color` 有意设置
- `overscroll-behavior: contain` 在模态/抽屉/sheet 中
- 拖动期间：禁用文本选择，拖动元素上 `inert`
- `autoFocus` 谨慎使用——仅桌面，单个主要输入；移动端避免

### 3. 性能（HIGH）

| ID | 规则 | 说明 |
|----|------|------|
| `image-optimization` | 使用 WebP/AVIF、响应式图像（srcset/sizes） | 懒加载非关键资产 |
| `image-dimension` | 声明 width/height 或使用 aspect-ratio | 防止布局偏移（Core Web Vitals: CLS） |
| `font-loading` | 使用 font-display: swap/optional | 避免不可见文本（FOIT）；预留空间减少布局偏移（MD） |
| `font-preload` | 仅预加载关键字体 | 避免在每个变体上过度使用 preload |
| `critical-css` | 优先首屏 CSS | 内联关键 CSS 或早期加载样式表 |
| `lazy-loading` | 通过 dynamic import / 路由级分割懒加载非 hero 组件 | |
| `bundle-splitting` | 按路由/功能分割代码 | React Suspense / Next.js dynamic 减少 TTI |
| `third-party-scripts` | 第三方脚本 async/defer 加载 | 审计并移除不必要的（MD） |
| `reduce-reflows` | 避免频繁布局读写 | 批量 DOM 读取然后写入 |
| `content-jumping` | 为异步内容预留空间 | 避免布局跳动（Core Web Vitals: CLS） |
| `lazy-load-below-fold` | 首屏下方图像和重型媒体使用 loading="lazy" | |
| `virtualize-lists` | 50+ 项列表虚拟化 | 提高内存效率和滚动性能 |
| `main-thread-budget` | 每帧工作保持在 ~16ms 以内 | 60fps；将重任务移出主线程（HIG, MD） |
| `progressive-loading` | >1s 操作使用骨架屏/shimmer | 而非长时间阻塞 spinner（Apple HIG） |
| `input-latency` | 点击/滚动输入延迟保持在 ~100ms 以内 | Material 响应性标准 |
| `tap-feedback-speed` | 点击后 100ms 内提供视觉反馈 | Apple HIG |
| `debounce-throttle` | 高频事件使用 debounce/throttle | scroll、resize、input |
| `offline-support` | 提供离线状态消息和基本回退 | PWA / 移动 |
| `network-fallback` | 慢网络提供降级模式 | 低分辨率图像、更少动画 |

**额外规则（Web Design Guidelines）：**

- 大列表（>50 项）：虚拟化（`virtua`、`content-visibility: auto`）
- 渲染中无布局读取（`getBoundingClientRect`、`offsetHeight`、`offsetWidth`、`scrollTop`）
- 批量 DOM 读/写；避免交错
- 偏好非受控输入；受控输入每次按键必须廉价
- 为 CDN/资产域添加 `<link rel="preconnect">`
- 关键字体：`<link rel="preload" as="font">` 配合 `font-display: swap`

### 4. 风格选择（HIGH）

见 Part 2 风格选择规则完整列表。

### 5. 布局与响应式（HIGH）

| ID | 规则 | 说明 |
|----|------|------|
| `viewport-meta` | width=device-width initial-scale=1 | 永不禁止缩放 |
| `mobile-first` | 移动优先设计 | 然后扩展到平板和桌面 |
| `breakpoint-consistency` | 使用系统断点 | 如 375 / 768 / 1024 / 1440 |
| `readable-font-size` | 移动端最小 16px 正文 | 避免 iOS 自动缩放 |
| `line-length-control` | 移动端 35-60 字符/行；桌面 60-75 | |
| `horizontal-scroll` | 移动端无水平滚动 | 确保内容适合视口宽度 |
| `spacing-scale` | 使用 4pt/8dp 增量间距系统 | Material Design |
| `touch-density` | 保持组件间距舒适 | 不拥挤，不导致误触 |
| `container-width` | 桌面一致 max-width | max-w-6xl / 7xl |
| `z-index-management` | 定义分层 z-index 刻度 | 如 0 / 10 / 20 / 40 / 100 / 1000 |
| `fixed-element-offset` | 固定导航/底栏必须预留安全内边距 | |
| `scroll-behavior` | 避免干扰主滚动的嵌套滚动区域 | |
| `viewport-units` | 移动端偏好 min-h-dvh 而非 100vh | |
| `orientation-support` | 横屏模式保持可读和可操作 | |
| `content-priority` | 移动端优先显示核心内容 | 折叠或隐藏次要内容 |
| `visual-hierarchy` | 通过大小、间距、对比建立层级 | 而非仅颜色 |

**额外规则（Web Design Guidelines）：**

- 全出血布局需要 `env(safe-area-inset-*)` 处理刘海
- 避免不需要的滚动条：`overflow-x-hidden` 在容器上，修复内容溢出
- Flex/grid 优于 JS 测量进行布局

### 6. 排版与色彩（MEDIUM）

见 Part 3 和 Part 4 完整规则。

### 7. 动画（MEDIUM）

| ID | 规则 | 说明 |
|----|------|------|
| `duration-timing` | 微交互 150-300ms；复杂过渡 ≤400ms | 避免 >500ms（MD） |
| `transform-performance` | 仅使用 transform/opacity | 避免动画 width/height/top/left |
| `loading-states` | 加载超过 300ms 时显示骨架或进度指示器 | |
| `excessive-motion` | 每个视图最多动画 1-2 个关键元素 | |
| `easing` | 进入用 ease-out，退出用 ease-in | UI 过渡避免 linear |
| `motion-meaning` | 每个动画必须表达因果关系 | 不仅是装饰（Apple HIG） |
| `state-transition` | 状态变化应平滑动画 | 而非跳变 |
| `continuity` | 页面/屏幕过渡保持空间连续性 | 共享元素、方向性滑动（Apple HIG） |
| `parallax-subtle` | 谨慎使用视差 | 必须尊重 reduced-motion 且不引起眩晕（Apple HIG） |
| `spring-physics` | 偏好 spring/物理曲线 | 而非 linear 或 cubic-bezier（Apple HIG） |
| `exit-faster-than-enter` | 退出动画短于进入 | 约 60-70% 进入时长（MD motion） |
| `stagger-sequence` | 列表/网格项入场交错 30-50ms | 避免同时出现或太慢的 reveal（MD） |
| `shared-element-transition` | 屏幕间使用共享元素/hero 过渡 | 视觉连续性（MD, HIG） |
| `interruptible` | 动画必须可中断 | 用户点击/手势立即取消进行中的动画（Apple HIG） |
| `no-blocking-animation` | 动画期间永不阻止用户输入 | UI 必须保持可交互（Apple HIG） |
| `fade-crossfade` | 同一容器内内容替换使用 crossfade | MD |
| `scale-feedback` | 可点击卡片/按钮按压时微妙缩放 0.95-1.05 | 释放时恢复（HIG, MD） |
| `gesture-feedback` | 拖动、滑动、捏合必须提供实时视觉响应 | 跟踪手指（MD Motion） |

**额外规则（Web Design Guidelines）：**

- 尊重 `prefers-reduced-motion`（提供减少变体或禁用）
- 仅动画 `transform`/`opacity`（合成器友好）
- 永不 `transition: all`——显式列出属性
- 设置正确的 `transform-origin`
- SVG：在 `<g>` 包装器上变换，配合 `transform-box: fill-box; transform-origin: center`
- 动画可中断——动画中响应用户输入

### 8. 表单与反馈（MEDIUM）

| ID | 规则 | 说明 |
|----|------|------|
| `visible-labels` | 可见标签 | 不是仅占位符 |
| `error-near-field` | 错误消息靠近字段 | 不是仅在顶部 |
| `helper-text` | 辅助文本 | 渐进式披露 |
| `progressive-disclosure` | 渐进式披露 | 不预先压倒 |

**额外规则（Web Design Guidelines）：**

- 输入需要 `autocomplete` 和有意义的 `name`
- 使用正确的 `type`（`email`、`tel`、`url`、`number`）和 `inputmode`
- 永不阻止粘贴（`onPaste` + `preventDefault`）
- 标签可点击（`htmlFor` 或包裹控件）
- 在邮箱、代码、用户名上禁用拼写检查（`spellCheck={false}`）
- 复选框/单选：标签 + 控件共享单个点击目标（无死区）
- 提交按钮保持启用直到请求开始；请求期间 spinner
- 错误内联在字段旁；提交时聚焦第一个错误
- 占位符以 `…` 结尾并显示示例模式
- 非认证字段上 `autocomplete="off"` 避免密码管理器触发
- 未保存更改导航前警告（`beforeunload` 或路由守卫）

### 9. 导航模式（HIGH）

| ID | 规则 | 说明 |
|----|------|------|
| `predictable-back` | 可预测的返回行为 | |
| `bottom-nav` | 底部导航 ≤5 项 | |
| `deep-linking` | 深度链接 | |

**额外规则（Web Design Guidelines）：**

- URL 反映状态——过滤器、标签、分页、展开面板在查询参数中
- 链接使用 `<a>`/`<Link>`（Cmd/Ctrl+点击、中键点击支持）
- 深度链接所有有状态 UI（如果使用 `useState`，考虑通过 nuqs 或类似工具 URL 同步）
- 破坏性操作需要确认模态或撤销窗口——永不立即执行

### 10. 图表与数据（LOW）

| ID | 规则 | 说明 |
|----|------|------|
| `legends` | 图例 | |
| `tooltips` | 工具提示 | |
| `accessible-colors` | 可访问色彩 | 不仅依赖颜色传达含义 |

---

## Part 6: 图表类型（25 类型）

| # | 图表类型 | 适用场景 | 推荐库 |
|---|----------|----------|--------|
| 1 | 折线图 (Line Chart) | 趋势、时间序列 | Recharts, Chart.js, D3 |
| 2 | 柱状图 (Bar Chart) | 比较、排名 | Recharts, Chart.js |
| 3 | 堆叠柱状图 (Stacked Bar) | 组成+比较 | Recharts, Chart.js |
| 4 | 水平柱状图 (Horizontal Bar) | 排名、比较 | Recharts, Chart.js |
| 5 | 面积图 (Area Chart) | 趋势+体量 | Recharts, D3 |
| 6 | 堆叠面积图 (Stacked Area) | 组成趋势 | Recharts, D3 |
| 7 | 饼图 (Pie Chart) | 组成（≤5类） | Recharts, Chart.js |
| 8 | 环形图 (Donut Chart) | 组成+中心指标 | Recharts, Chart.js |
| 9 | 散点图 (Scatter Plot) | 相关性、分布 | Recharts, D3 |
| 10 | 气泡图 (Bubble Chart) | 三维比较 | Recharts, D3 |
| 11 | 雷达图 (Radar Chart) | 多维比较 | Recharts, Chart.js |
| 12 | 热力图 (Heatmap) | 密度、矩阵 | D3, Nivo |
| 13 | 树形图 (Treemap) | 层级+大小 | D3, Recharts |
| 14 | 桑基图 (Sankey Diagram) | 流量、转移 | D3 |
| 15 | 漏斗图 (Funnel Chart) | 转化流程 | Chart.js, 自定义 |
| 16 | 甘特图 (Gantt Chart) | 时间线、项目 | 自定义, D3 |
| 17 | 箱线图 (Box Plot) | 统计分布 | D3, Plotly |
| 18 | 小提琴图 (Violin Plot) | 密度+分布 | D3, Plotly |
| 19 | 瀑布图 (Waterfall Chart) | 增减变化 | 自定义, Plotly |
| 20 | 子弹图 (Bullet Chart) | 目标vs实际 | D3, 自定义 |
| 21 | 旭日图 (Sunburst) | 层级+组成 | D3 |
| 22 | 和弦图 (Chord Diagram) | 关系、流量 | D3 |
| 23 | 力导向图 (Force-Directed) | 网络关系 | D3 |
| 24 | 地图 (Choropleth) | 地理数据 | D3, Mapbox, Leaflet |
| 25 | 仪表盘 (Gauge Chart) | KPI、进度 | Recharts, 自定义 |

---

## Part 7: 技术栈（10 栈）

### 1. React / Next.js

- **框架**：Next.js 15+ (App Router), React 19
- **样式**：Tailwind CSS v4, CSS Modules
- **组件**：shadcn/ui, Radix UI
- **状态**：useState → lifted state → Context → URL state → React Query/SWR → Zustand
- **动效**：Framer Motion, CSS transitions
- **图表**：Recharts, Visx
- **关键模式**：Server Components, Suspense boundaries, streaming

### 2. Vue / Nuxt

- **框架**：Nuxt 3+, Vue 3 (Composition API)
- **样式**：Tailwind CSS, UnoCSS
- **组件**：Radix Vue, Headless UI
- **状态**：ref/reactive → Pinia
- **动效**：Vue transitions, @vueuse/motion
- **图表**：Vue-chartjs, Unovis

### 3. Svelte / SvelteKit

- **框架**：SvelteKit, Svelte 5
- **样式**：Tailwind CSS, CSS scoped
- **组件**：shadcn-svelte, Melt UI
- **状态**：Svelte stores, runes
- **动效**：Svelte transitions, svelte/motion
- **图表**：LayerCake

### 4. Flutter

- **框架**：Flutter 3.x, Dart
- **样式**：ThemeData, Material 3
- **组件**：Material, Cupertino
- **状态**：Provider, Riverpod, Bloc
- **动效**：AnimationController, Hero transitions
- **图表**：fl_chart, syncfusion

### 5. React Native

- **框架**：React Native, Expo
- **样式**：StyleSheet, NativeWind
- **组件**：React Native Paper, Tamagui
- **状态**：Zustand, React Query
- **动效**：Reanimated, Gesture Handler
- **图表**：react-native-chart-kit, Victory Native

### 6. SwiftUI

- **框架**：SwiftUI, iOS 17+
- **样式**：ViewModifier, ShapeStyle
- **组件**：原生 SwiftUI 组件
- **状态**：@State, @Observable, @Environment
- **动效**：withAnimation, matchedGeometryEffect
- **图表**：Swift Charts

### 7. Tailwind CSS

- **v4 关键变化**：`@theme` 替代 tailwind.config.js, `@import "tailwindcss"`, OKLCH 颜色
- **设计 token**：`--color-*`, `--font-*`, `--radius-*`, `--shadow-*`
- **3 层 token 架构**：Base（原始值）→ Semantic（意图）→ Component（组件特定）
- **暗色模式**：`@custom-variant dark`, `color-scheme: dark`
- **关键工具**：`cn()` 合并类, `@utility` 自定义, `@custom-variant` 自定义变体

### 8. shadcn/ui

详见 Part 8。

### 9. HTML/CSS

- **语义 HTML5**：`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- **CSS Grid/Flexbox**：现代布局
- **CSS Custom Properties**：设计 token
- **Container Queries**：组件级响应式
- **CSS Layers**：`@layer` 管理样式优先级

### 10. Material Design

- **Material 3**：Dynamic Color, color roles, elevation tones
- **组件**：Material Web, MDC-Web
- **排版**：Material Type Scale（display, headline, title, body, label）
- **动效**：Motion system（container transform, shared axis, fade through, fade）
- **状态层**：hover, focus, pressed, dragged, state layers

---

## Part 8: shadcn/ui 组件

### 原则

- **复制即拥有 (Copy-and-own)**：组件在你的代码库中，不是 npm 包
- **基于 Radix UI 原语**：可访问性内置
- **Tailwind CSS 样式**：实用优先，零运行时
- **TypeScript 优先**：完整类型安全
- **组合模式**：复合组件而非配置

### 关键样式规则

- 使用 `cn()` 工具合并类（`clsx` + `tailwind-merge`）
- 主题通过 CSS 自定义属性，OKLCH 格式
- 新 `Field` 组件替代旧的 `Form/FormField` 模式，表单库无关
- 使用 `npx shadcn@latest add` 安装组件到 `components/ui/`
- 读取项目的 `components.json` 获取配置

### 表单与输入

- 使用 `Field` 组件进行字段布局（标签、输入、描述、错误）
- 输入需要 `autocomplete` 和有意义的 `name`
- 使用正确的 `type`（`email`、`tel`、`url`、`number`）和 `inputmode`
- 永不阻止粘贴
- 标签可点击（`htmlFor` 或包裹控件）
- 在邮箱、代码、用户名上禁用拼写检查
- 复选框/单选：标签 + 控件共享单个点击目标
- 提交按钮保持启用直到请求开始；请求期间 spinner
- 错误内联在字段旁；提交时聚焦第一个错误
- 占位符以 `…` 结尾并显示示例模式

### 组件组合

偏好组合而非配置：

```tsx
// 好：组合模式
<Card>
  <CardHeader>
    <CardTitle>标题</CardTitle>
    <CardDescription>描述</CardDescription>
  </CardHeader>
  <CardContent>内容</CardContent>
  <CardFooter>操作</CardFooter>
</Card>

// 避免：过度配置
<Card
  title="标题"
  description="描述"
  content="内容"
  footer="操作"
/>
```

### 图标

- 使用一个图标集保持一致（Lucide React 推荐）
- 图标按钮需要 `aria-label`
- 装饰性图标需要 `aria-hidden="true"`
- 图标风格与整体设计一致（笔画宽度、圆角）

### 覆盖层组件

- Dialog/Modal：焦点陷阱、ESC 关闭、`overscroll-behavior: contain`
- Sheet/Drawer：边缘滑动、`overscroll-behavior: contain`
- Popover：点击外部关闭、焦点管理
- Tooltip：延迟显示、可访问性
- Command Palette：键盘导航、搜索

### 组件选择参考

| 需求 | 推荐组件 |
|------|----------|
| 按钮 | Button (variant: default/destructive/outline/secondary/ghost/link) |
| 卡片 | Card + CardHeader/CardTitle/CardDescription/CardContent/CardFooter |
| 对话框 | Dialog + DialogTrigger/DialogContent/DialogHeader/DialogFooter |
| 表单字段 | Field + FieldLabel/FieldInput/FieldDescription/FieldError |
| 数据表格 | Table + TableHeader/TableBody/TableRow/TableHead/TableCell |
| 输入 | Input, Textarea, Select, Checkbox, RadioGroup, Switch, Slider |
| 导航 | NavigationMenu, Tabs, Breadcrumb, Menubar |
| 反馈 | Alert, Toast (Sonner), Progress, Skeleton |
| 覆盖层 | Dialog, Sheet, Popover, Tooltip, HoverCard |
| 数据展示 | Badge, Avatar, Separator, ScrollArea, Accordion |
| 命令面板 | Command + CommandInput/CommandList/CommandItem/CommandGroup |

### 主题与定制

- **CSS 变量**：`--background`, `--foreground`, `--primary`, `--secondary`, `--accent`, `--destructive`, `--muted`, `--border`, `--ring`, `--card`, `--popover`
- **OKLCH 格式**：使用 `oklch()` 定义颜色以获得更广色域
- **圆角**：`--radius` 控制全局圆角
- **暗色模式**：`.dark` 类切换，CSS 变量覆盖
- **预设**：`--preset` 切换设计风格
- **Tailwind v3 vs v4**：v4 使用 `@theme` 替代 `tailwind.config.js`

### 关键项目上下文字段

当 shadcn/ui skill 激活时，读取 `components.json` 获取：

- `style`：设计风格（default/new-york）
- `tailwind`：Tailwind 配置和版本
- `aliases`：组件和工具路径别名
- `iconLibrary`：图标库选择
- `baseLib`：基础库（radix/base）

### 快速参考

```bash
# 初始化
npx shadcn@latest init

# 添加组件
npx shadcn@latest add button card dialog form

# 搜索组件
npx shadcn@latest search

# 查看组件文档
npx shadcn@latest docs [component]

# 查看项目信息
npx shadcn@latest info --json

# 差异比较
npx shadcn@latest diff [component]
```

---

## Part 9: Web 设计审查

### 工作方式

1. 获取最新指南
2. 读取指定文件
3. 对照所有规则检查
4. 以简洁的 `file:line` 格式输出发现

### 指南来源

获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 获取最新规则。获取的内容包含所有规则和输出格式说明。

### 使用方法

当用户提供文件或模式参数时：

1. 从源 URL 获取指南
2. 读取指定文件
3. 应用获取指南中的所有规则
4. 使用指南中指定的格式输出发现

**审查覆盖领域：**

- 可访问性（图标按钮 aria-label、表单标签、键盘处理、语义 HTML）
- 焦点状态（focus-visible、outline 替代）
- 表单（autocomplete、type、粘贴、标签、错误内联）
- 动画（reduced-motion、transform/opacity、transition 属性列表）
- 排版（省略号、弯引号、不间断空格、tabular-nums）
- 内容处理（长内容、空状态、flex min-w-0）
- 图像（尺寸、懒加载、优先级）
- 性能（虚拟化、布局读取、批量 DOM）
- 导航与状态（URL 同步、链接语义、深度链接、破坏性确认）
- 触摸与交互（touch-action、overscroll-behavior、drag）
- 安全区域与布局（safe-area-inset、overflow）
- 暗色模式与主题（color-scheme、theme-color、原生控件）
- 本地化（Intl.*、语言检测、translate="no"）
- 水合安全（value+onChange、日期时间守卫）
- Hover 与交互状态
- 内容与文案（主动语态、Title Case、数字、具体标签）

### 反模式（标记这些）

- `user-scalable=no` 或 `maximum-scale=1` 禁用缩放
- `onPaste` 配合 `preventDefault`
- `transition: all`
- `outline-none` 无 focus-visible 替代
- 内联 `onClick` 导航无 `<a>`
- `<div>` 或 `<span>` 带点击处理（应为 `<button>`）
- 图像无尺寸
- 大数组 `.map()` 无虚拟化
- 表单输入无标签
- 图标按钮无 `aria-label`
- 硬编码日期/数字格式（使用 `Intl.*`）
- `autoFocus` 无明确理由

---

## Part 10: CLI 搜索工具

### 前置条件

确保项目已初始化 shadcn/ui：

```bash
npx shadcn@latest init
```

### 生成设计系统（REQUIRED）

在开始任何 UI 工作之前，生成设计系统：

```bash
# 基于产品类型生成推荐
--design-system <product-type>

# 示例
--design-system saas
--design-system e-commerce
--design-system dashboard
```

### 持久化设计系统

将生成的设计系统保存到项目：

```bash
--persist-design-system
```

保存到 `.claude/design-system.json`，后续会话自动加载。

### 域搜索

搜索特定设计域：

```bash
--domain color        # 色彩调色板
--domain typography   # 字体配对
--domain style        # 风格推荐
--domain chart        # 图表类型
--domain product      # 产品类型匹配
--domain ux           # UX 准则
--domain stack        # 技术栈指南
```

### 栈指南

获取特定技术栈的详细指南：

```bash
--stack react         # React/Next.js
--stack vue           # Vue/Nuxt
--stack svelte        # Svelte/SvelteKit
--stack flutter       # Flutter
--stack react-native  # React Native
--stack swiftui       # SwiftUI
--stack tailwind      # Tailwind CSS
--stack shadcn        # shadcn/ui
--stack html          # HTML/CSS
--stack material      # Material Design
```

---

## Part 11: 专业 UI 通用规则

### 图标与视觉元素

- 使用 SVG 图标（Heroicons、Lucide），不用 emoji
- 一个图标集保持一致（笔画宽度、圆角半径）
- 图标按钮需要 `aria-label`
- 装饰性图标需要 `aria-hidden="true"`
- 图标风格与整体设计对齐
- 不用 emoji 作为图标

### 交互（App）

- 每个屏幕一个主要 CTA
- 次要行动视觉上从属
- 破坏性操作需要确认
- 异步操作显示加载状态
- 错误消息靠近问题
- 状态变化平滑动画
- 动画可中断
- 退出动画短于进入动画

### 布局与间距

- 使用 4pt/8dp 增量间距系统
- 一致的 max-width（max-w-6xl / 7xl）
- 分层 z-index 刻度
- 固定元素预留内边距
- 移动端无水平滚动
- Flex/grid 优于 JS 测量
- 全出血布局使用 `env(safe-area-inset-*)`

---

## Part 12: 全网搜索参考与综合优化

### 概述

> ⚠️ **搜索目标是找 UI 截图/组件模板/设计作品，不是找文章/博客/教程。**

当内置 50+ 风格、161 调色板中的参考不足以满足用户的具体需求时（如后端管理页面、特殊行业领域、用户有明确的参考需求），通过全网搜索从设计作品平台获取实际 UI 设计参考，经过 WebFetch → 提取 → 解构 → 分析 → 融合 → 优化流程处理。

### 搜索源分类

#### ✅ 设计作品平台（优先搜索）

| 来源 | 搜索方式 | 能找到什么 |
|------|----------|-----------|
| Dribbble | `site:dribbble.com {关键词}` | UI 截图、按钮样式、卡片设计 |
| Behance | `site:behance.net {关键词}` | 完整项目案例、品牌系统 |
| Awwwards | `site:awwwards.com {关键词}` | 获奖网站、前沿布局 |
| Mobbin | `site:mobbin.com {关键词}` | 真实 App 截图、移动端模式 |
| CollectUI | `site:collectui.com {关键词}` | 按组件分类的 UI 截图 |
| Pageflows | `site:pageflows.com {关键词}` | 用户流程截图 |
| Refero | `site:refero.design {关键词}` | 真实 Web App 截图 |
| Godly | `site:godly.website {关键词}` | 高设计质量网站 |
| Siteinspire | `site:siteinspire.com {关键词}` | 按风格分类参考 |
| Landingfolio | `site:landingfolio.com {关键词}` | 落地页截图 |
| Uigarage | `site:uigarage.net {关键词}` | UI 设计截图 |
| Httpster | `site:httpster.net {关键词}` | 当代网站参考 |

#### ❌ 科技博客/文章网站（绝对禁止）

| 禁止搜索 | 原因 |
|----------|------|
| `site:medium.com` | 博客文章，无 UI 截图 |
| `site:smashingmagazine.com` | 设计理论文章 |
| `site:dev.to` | 开发者博客 |
| `site:css-tricks.com` | CSS 教程 |
| `site:freecodecamp.org` | 编程文章 |
| 任何博客/教程类网站 | 找的是设计作品，不是文章 |

### 搜索后强制步骤

```
Step A: WebSearch
  ↓ 在 3-5 个设计作品平台搜索，用具体组件描述词
Step B: WebFetch（不可跳过）
  ↓ 打开搜索结果中的具体设计作品页面
  ↓ 查看 UI 截图、按钮样式、配色方案
Step C: 提取设计资产（不可跳过）
  ↓ 按钮颜色/圆角/阴影 | 卡片布局/间距 | 表单样式 | 表格风格
  ↓ 配色 hex 值 | 字体组合 | 间距节奏
Step D: 解构分析（4 步）
```

### 搜索关键词构建

```
✅ 正确（能找到具体 UI）：
- "data table pagination dark" site:dribbble.com
- "form validation input group" site:collectui.com
- "settings sidebar navigation" site:pageflows.com
- "auth login clean modern" site:awwwards.com

❌ 错误（只能找到文章）：
- "admin dashboard best practices"
- "how to design backend panel"
- "UI design principles 2024"
```

### 参考解构与综合优化（4 步流程）

#### Step 1: 解构（Deconstruct）

从搜索结果中提取设计元素：

| 元素 | 提取内容 |
|------|----------|
| 布局结构 | 网格系统、内容分区、导航模式 |
| 色彩方案 | 主色、强调色、背景色、文字色 |
| 排版层次 | 字体选择、字号层级、行高、行长 |
| 组件模式 | 按钮样式、卡片设计、表单布局、表格样式 |
| 交互方式 | 悬停效果、过渡动画、加载状态 |
| 间距节奏 | 内边距、外边距、元素间距 |

#### Step 2: 分析（Analyze）

评估参考设计的质量：

- **优点提取**：什么让它看起来好？（布局清晰、配色和谐、层次分明……）
- **缺点识别**：什么让它看起来差？（对比度不足、间距混乱、风格不一致……）
- **原理分析**：为什么这样设计？（视觉引导、信息优先级、用户习惯……）
- **需求匹配**：与用户需求的匹配度如何？

#### Step 3: 融合（Synthesize）

将多个参考的优点融合为新方案：

1. **提取各自优点**：参考 A 的布局 + 参考 B 的配色 + 参考 C 的组件模式
2. **融入内置系统**：使用 references/ 中的色板、字体对、Design Token
3. **跨领域借鉴**：从建筑、时尚、工业设计等领域获取灵感
4. **组合创新**：生成新的设计方案，而非照搬任何一个参考

**融合规则：**
- 内置 Design Token 优先：参考中的颜色/字体替换为内置系统的语义 Token
- 可访问性底线：参考中的低对比度/小触摸目标必须修正
- 一致性保证：融合后的方案必须在视觉语言上保持一致

#### Step 4: 优化（Optimize）

对融合后的方案进行最终优化：

- [ ] 应用 Design Token 系统统一视觉语言
- [ ] 检查可访问性底线（对比度 ≥ 4.5:1、触摸目标 ≥ 44×44pt）
- [ ] 优化性能（图片尺寸、字体加载、动画性能）
- [ ] 确保响应式适配（桌面/平板/手机）
- [ ] 对照反模式检查（通用卡片网格、随机强调色、占位符排版）
- [ ] 确保输出可运行的代码

### 跨领域设计借鉴

设计思考不应局限于 UI 领域：

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

### 输出规范

参考解构优化后的输出必须包含：

```markdown
## 设计参考分析

### 参考来源
1. {来源1} — {URL} — {简要描述}
2. {来源2} — {URL} — {简要描述}
3. {来源3} — {URL} — {简要描述}

### 解构结果
- 布局：{参考了谁的布局，为什么}
- 配色：{参考了谁的配色，如何融入内置系统}
- 组件：{参考了谁的组件模式，做了什么改进}
- 排版：{参考了谁的排版，如何优化}

### 融合方案
- 采用了 {参考A} 的 {优点X}
- 采用了 {参考B} 的 {优点Y}
- 融合了内置 {色板名} 的配色
- 跨领域借鉴了 {领域} 的 {元素}

### 优化改进
- {改进1}：{具体说明}
- {改进2}：{具体说明}
```

---

## Part 13: 工作流摘要

### Step 0: 需求调研与参考搜索（新增）

在开始任何设计工作前，确认以下信息（如主入口 Phase 0 已完成则跳过）：

- [ ] 设计目标明确？
- [ ] 目标受众明确？
- [ ] 功能需求完整？
- [ ] 交互需求明确？
- [ ] 风格偏好确认？
- [ ] 技术约束确认？

**参考搜索：** 当内置 50+ 风格无法满足需求时，触发全网搜索：

| 场景 | 搜索关键词示例 |
|------|---------------|
| 后端管理页面 | `site:dribbble.com admin dashboard UI design 2024` |
| 数据可视化 | `site:behance.net data visualization dashboard` |
| SaaS 产品 | `site:awwwards.com SaaS landing page design` |
| 移动端 App | `site:dribbble.com mobile app UI kit` |
| 电商页面 | `site:pinterest.com e-commerce product page UI` |
| 内部工具 | `site:dribbble.com internal tool admin panel` |

搜索后执行参考解构优化流程（见 Part 13）。

### Step 1: 确定设计方向

- **必须接收输入**：Design Brief 中的「设计灵魂」（品牌人格、情绪板、设计禁忌）和 creative 子技能的「视觉论文」
- **视觉论文对齐**：确认设计方向与视觉论文的 5 个决策方向（配色、排版、布局、材质、动效）一致
- 明确目的、受众、情感基调
- 写下视觉论文、内容计划、交互论文
- 选择风格（参考 Part 2 风格列表）
- **禁忌检查**：确认设计方向没有触碰 Design Brief 中的任何设计禁忌

### Step 2: 生成设计系统

- 使用 `--design-system <product-type>` 生成推荐
- 选择调色板（参考 Part 3）
- 选择字体配对（参考 Part 4）
- 持久化设计系统（`--persist-design-system`）

### Step 3: 应用 UX 准则

- 按优先级 1→10 应用规则（参考 Part 5）
- CRITICAL 规则必须满足
- HIGH 规则应满足
- MEDIUM/LOW 规则推荐满足

### Step 4: 选择技术栈

- 确定目标栈（参考 Part 7）
- 应用栈特定指南
- 安装必要组件（shadcn/ui 等）

### Step 5: 构建与审查（执行级约束）

**代码生成时必须遵守以下约束，违反任何一条必须重写：**

1. **视觉论文引用**：每个主要组件的代码注释中必须引用视觉论文的一个具体决策（如 `/* 配色方向：冷峻，使用深蓝而非蓝紫渐变 */`）
2. **非对称布局优先**：默认使用非对称布局，只有在功能需要时才使用对称
3. **无模板检测**：生成代码后自检——如果代码看起来像"又一个 SaaS 模板"（卡片网格、居中大标题、灰底白卡），必须重写
4. **设计禁忌检查**：对照 Design Brief 中的设计禁忌逐项检查，触碰任何一条必须重写
5. **品牌人格体现**：代码必须能体现品牌人格（如"叛逆先锋"应有打破常规的布局，"优雅艺术家"应有精致的细节）
6. **情绪板验证**：用情绪板的 3 个关键词描述生成的界面，如果描述不匹配，调整设计
7. **字体必须有个性**：不能只用 Inter 或系统默认字体，必须至少有一个有性格的字体（通过 `scripts/search.py fonts` 搜索）
8. **输出质量门限**：生成的代码必须能直接通过 review 子技能的 8/10 分标准（所有维度 ≥ 8 分）

- 遵循艺术方向原则（Part 1）
- 使用 Web 设计审查检查（Part 9）
- 修复所有反模式
- 确保可访问性合规

### Step 6: 交付前检查清单

- [ ] 品牌在第一屏无可误认？
- [ ] 有一个强视觉锚点？
- [ ] 仅扫描标题可理解页面？
- [ ] 每个区块只有一个职责？
- [ ] 卡片真的必要？
- [ ] 动效改善层级或氛围？
- [ ] 移除装饰性阴影后仍感觉高级？
- [ ] 对比度 ≥ 4.5:1？
- [ ] 所有交互元素有焦点状态？
- [ ] 表单有标签和错误反馈？
- [ ] 动画尊重 reduced-motion？
- [ ] 移动端无水平滚动？
- [ ] 图像有尺寸属性？
- [ ] 大列表虚拟化？
- [ ] 暗色模式对比度单独测试？
- [ ] 语义色彩 token 而非原始 hex？
- [ ] URL 反映状态？
- [ ] 破坏性操作有确认？
- [ ] 触摸目标 ≥ 44×44px？

**设计灵魂检查（新增，不可跳过）：**
- [ ] **品牌人格体现**：这个设计看起来像"极客工程师"还是"优雅艺术家"？如果看不出来，重写
- [ ] **情绪板匹配**：用情绪板的 3 个词描述这个界面，是否匹配？
- [ ] **设计禁忌检查**：是否触碰了任何禁忌？（蓝紫渐变/emoji/灰底白卡/卡片堆砌/标准Hero）
- [ ] **模板检测**：这个设计是否像"又一个 SaaS 模板"？如果是，重写
- [ ] **字体个性**：是否至少有一个有性格的字体？不能全是 Inter/系统默认
- [ ] **非对称检查**：布局是否至少有一个非对称元素？不能全是居中对齐/等宽卡片
- [ ] **视觉论文追溯**：代码中的主要决策能否追溯到视觉论文的 5 个方向？
- [ ] 无反模式（见 Part 9）？
- [ ] 需求简报（Design Brief）已确认？
- [ ] 全网搜索参考已解构优化（非直接照搬）？
- [ ] Design Token 系统已应用？
- [ ] 跨领域借鉴已考虑？

# 组件 Block 分类目录

> 基于 Aceternity UI 的 Block 分类体系 + 21st.dev 的组件市场结构
> design 阶段根据用户需求自动匹配对应 Block 类型生成设计卡

---

## Block 类型总览

| Block 类型 | 适用场景 | 参考来源 | 设计要点 |
|-----------|---------|---------|---------|
| **Hero Sections** | 首页首屏 | Aceternity UI (21+) / 21st.dev | 排版冲击 > 图片，禁止渐变背景 |
| **Feature Sections** | 产品特性展示 | Aceternity UI (18+) | 2026 asymmetric Bento Grid，非均匀卡片混合尺寸 |
| **Bento Grids** | 特性聚合展示 | Aceternity UI (6+) / Magic UI / Cult UI | 2026 asymmetric 非对称拼贴：混合 1x1/2x1/1x2/2x2 尺寸，内容密度和内边距必须变化 |
| **CTA Sections** | 行动号召 | Aceternity UI (6+) / 21st.dev | 简洁直接，不超过 2 个 CTA 按钮 |
| **Pricing Cards** | 定价对比 | 21st.dev / shadcn | 最多 3-4 列，高亮推荐列 |
| **Contact Sections** | 联系/表单 | Aceternity UI (4+) | 最少字段，清晰的输入状态 |
| **Blog Sections** | 内容列表 | Aceternity UI (4+) | 图文比例，阅读流导向 |
| **Empty States** | 空数据/首次使用 | Aceternity UI (5+) | 引导 > 空白，有意义的 placeholder |
| **Background Effects** | 页面背景 | Aceternity UI (11+) / Magic UI | 噪点/着色器/波纹/线条，不抢内容 |
| **Shaders** | 着色器背景 | Aceternity UI (3+) | WebGL / Canvas，性能敏感 |
| **Data Tables** | 数据展示 | 21st.dev | 等宽数字、排序、分页、行 hover |
| **Navigation** | 导航栏/侧栏 | 21st.dev | 移动端汉堡菜单，桌面端 sidebar |
| **Forms** | 输入表单 | 21st.dev / shadcn | 验证状态、标签位置、提交反馈 |
| **Cards** | 内容卡片 | Aceternity UI (4+) / 21st.dev | 图片+文字+CTA，信息层级 |
| **Carousels** | 轮播/滑动 | Aceternity UI | Apple 风格极简，非传统 dot 轮播 |
| **Testimonials** | 用户评价墙 | Aceternity UI | 非对称编排，真人感 |
| **Logo Clouds** | 合作品牌展示 | Aceternity UI (6+) | 灰度 logo，不抢视觉 |
| **Footers** | 页脚 | 21st.dev / shadcn | 链接分组，版权行 |

---

## 2026 Asymmetric Bento Grid 规范

### 布局参数

- **Desktop Grid**: `grid-cols-3 md:grid-cols-4 lg:grid-cols-6`
- **Gap**: `gap-4` (16px) 或 `gap-6` (24px)
- **响应式**: 移动端自动降级为 `grid-cols-1` 或 `grid-cols-2`

### 必须混合尺寸（MUST mix sizes）

| 尺寸 | col-span / row-span | 用途 |
|------|-------------------|------|
| 1x1 小卡片 | `col-span-1 row-span-1` | 图标、简短文字、小数据 |
| 2x1 宽卡片 | `col-span-2 row-span-1` | 横向图片、短列表、按钮组 |
| 1x2 高卡片 | `col-span-1 row-span-2` | 纵向图片、引用、用户头像 |
| 2x2 大英雄卡 | `col-span-2 row-span-2` | **至少一个**，主视觉、核心特性、视频预览 |

### 内容密度变化（MUST vary）

- 部分卡片以图片为主（图片占比 ≥ 70%）
- 部分卡片以文字为主（标题 + 描述 + 小图标）
- 部分卡片以数据为主（数字 + 图表 + 标签）
- 避免所有卡片视觉权重相同

### 内边距变化（Padding MUST vary）

- 大卡片/英雄卡: `p-8` (32px)
- 中等卡片: `p-6` (24px)
- 小卡片/密集信息卡: `p-4` (16px)

### ❌ 禁止项

- ❌ 所有卡片都是 `col-span-1`（老式均匀网格）
- ❌ 所有卡片内边距完全相同
- ❌ 所有卡片内容密度一致
- ❌ 缺少 2x2 大英雄卡
- ❌ 机械对称排列（左2x2右四个1x1这种过于规整的布局）

---

## Block 类型 → 场景映射

| 用户描述 | 需要的 Block 类型 |
|---------|-----------------|
| "做个 SaaS 官网" | Hero + Features + Pricing + CTA + Footer |
| "后台管理系统" | Navigation + Data Tables + Forms + Cards |
| "App 落地页" | Hero + Features + Testimonials + CTA + Footer |
| "设计一个 Dashboard" | Navigation + Cards + Data Tables + Charts |
| "产品介绍页" | Hero + Features + Bento Grid + CTA |
| "博客首页" | Hero + Blog Sections + Cards + Footer |
| "联系我们页面" | Hero + Contact Sections + Footer |
| "404 / 空状态" | Empty States + CTA |

---

## 每个 Block 的设计卡格式

```
## Block: {Block 类型名称}

**设计决策来源**：Design Brief §{section} · 品牌人格「{type}」
**参考来源**：Aceternity UI · 21st.dev · {额外参考}

**AI 生成 Prompt**：
生成一个 {框架} {Block 类型} 组件：
- 配色: var(--color-*)
- 布局: {布局描述}
- 字体: var(--font-display) / var(--font-body)
- 动效: {动效描述，使用 Motion (motion/react) 实现}
- 禁止: {反 AI 规则}
```

---

### 19. 2026新特效组件 (Cult UI / Magic UI)

| 组件名 | 来源 | 描述 | 适用场景 |
|--------|------|------|---------|
| Metal Button | Cult UI | 金属质感按钮，有银色/金色渐变高光 | 奢华高端品牌、科技产品CTA |
| Cosmic Button | Cult UI | 宇宙风格按钮，粒子光晕效果 | 科技品牌、AI产品、游戏 |
| Fluted Glass | Cult UI | 竖条纹玻璃效果，高级磨砂质感 | Hero背景、卡片装饰、导航栏 |
| Folded Card | Cult UI | 折叠卡片，模拟纸张折角效果 | 产品展示、功能介绍、作品集 |
| Circuit Board | Cult UI | 电路板纹理背景SVG | 技术产品、API文档、开发者工具 |
| Apple Device Mockups | Cult UI | iPhone/Watch/Keyboard/Display XDR 高保真mockup | App展示、产品screenshot展示 |
| Feature Sticky Section | Cult UI | 粘性特性区块，滚动时内容切换 | 产品功能介绍、长页面特性展示 |
| Collab Avatar | Cult UI | 协作用头像组，头像重叠+计数 | 团队展示、用户头像、社交证明 |
| Shift Card | Cult UI | 悬停时显示详情的卡片 | 作品集、产品卡片、项目列表 |
| Glyph Matrix | Magic UI | 文字矩阵效果，字符随机变换后定格 | Hero标题、数据展示、数字动效 |
| Magnetic Button | Motion | 磁性按钮，鼠标靠近时按钮向鼠标微移5-10px | CTA按钮、重要操作按钮 |
| Spotlight Card | Aceternity | 鼠标跟随径向渐变光晕卡片 | 特性卡片、团队成员卡片、产品展示 |
| Text Reveal | Motion | 滚动时文字逐行从mask中显现 | 大段引言、特性标题、Testimonial |
| Number Counter | Motion | 数字从0滚动到目标值 | 数据展示、统计数字、KPI |
| Ticker/Marquee | Motion | 无限滚动跑马灯 | 客户logo展示、评价滚动、合作伙伴 |

---

### 20. 高级CSS组件（无JS依赖）

| 组件名 | CSS特性 | 描述 |
|--------|---------|------|
| Scroll Progress Bar | Scroll-driven animations | 页面顶部固定进度条，随滚动增长 |
| Fade-up on Scroll | animation-timeline: view() | 元素进入视口时淡入上移 |
| Gradient Border | @property + conic-gradient | 旋转渐变边框 |
| Grid Pattern Background | linear-gradient | 网格线背景 |
| Noise Texture | SVG data URI | 噪点质感叠加层 |
| Glow Orb | radial-gradient + blur | 背景光晕装饰 |

---

## 全局参考索引

| 参考库 | 类型 | 访问方式 |
|--------|------|---------|
| Aceternity UI | React/Tailwind 组件 | https://ui.aceternity.com |
| 21st.dev | React/Tailwind/shadcn 组件市场 | https://21st.dev |
| Magic UI | React/Tailwind 动画组件 | https://magicui.design |
| Cult UI | React/Tailwind 高端特效组件 | https://cult-ui.com |
| Motion (motion/react) | React 动画库（2025年更名后统一使用 Motion） | https://motion.dev |
| shadcn/ui | React 基础组件 | https://ui.shadcn.com |
| Inspira UI | Vue/Nuxt 3D 动画组件 | https://inspira-ui.com |
| TDesign | 企业级组件库（React/Vue/移动端/小程序/Flutter） | https://tdesign.tencent.com |
| Ant Design | 企业级组件库（React；Vue 走社区版） | https://ant.design |
| Element Plus | 企业级组件库（Vue 3） | https://element-plus.org |
| Arco Design | 企业级组件库（React/Vue3） | https://arco.design |

> 企业级组件库的 Token 定制入口、与语义 Token 层的映射方式见 design 子技能 Part 7
> 「国内企业级组件库」小节；B 端模式参考 `references/admin-enterprise-patterns.md`。

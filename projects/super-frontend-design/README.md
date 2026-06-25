# Super Frontend Design — 前端设计全流程工作台

## 简介

**一句话描述：** 集生成艺术、UI/UX设计、主题系统、设计审查于一体的前端设计全流程 Skill，从灵感到交付一站式完成。

**合并来源：** 本 Skill 由以下 11 个前端设计相关 Skill 合并整合而成：
1. `algorithmic-art` — 算法艺术与 p5.js 生成 → creative
2. `creative-art` — 生成艺术与视觉设计 → creative
3. `canvas-design` — Canvas 视觉设计 → creative
4. `frontend-design` — 前端界面设计 → design
5. `frontend-skill` — 高品质前端落地页 → design
6. `frontend-ui` — UI/UX 综合设计智能 → design
7. `ui-ux-pro-max` — UI/UX Pro Max 全栈设计 → design + theme
8. `brand-guidelines` — 品牌色彩、排版规范 → theme
9. `theme-factory` — 10 预设主题、主题工具包 → theme
10. `impeccable` — 前端界面精修与优化（14 维度） → review
11. `web-design-guidelines` — Web 设计规范审查 → review

**核心理念：**
- **Design Token 贯穿** — 从主题定义到代码输出，所有设计决策通过语义化 Token 传递，杜绝原始 hex 值
- **全流程闭环** — research → creative → theme → design → review 五阶段工作流，灵感到审查无缝衔接
- **品质优先** — 博物馆级视觉输出、生产级代码质量、专业级审查标准
- **拒绝平庸** — 反对通用模板、反对卡片网格堆砌、反对千篇一律的 SaaS 风格

---

## 功能模块

### creative — 生成艺术与视觉设计

**功能描述：** 基于算法和哲学驱动的生成艺术创作，支持交互式 p5.js 作品和博物馆级静态海报两种输出模式。

**支持模式：**
- **生成艺术模式** — 输出交互式 HTML 文件，内含 p5.js 种子随机、参数控件、哲学宣言
- **视觉设计模式** — 输出博物馆级 PDF/PNG 海报，90% 视觉 + 10% 文字，使用 canvas-fonts 字体库

**触发词：** 生成艺术、算法艺术、flow field、粒子系统、海报设计、generative art、poster、museum-quality、p5.js

---

### design — UI/UX 综合设计

**功能描述：** 全栈 UI/UX 设计智能，从视觉方向探索到生产级代码输出的完整设计流程。

**包含内容：**
- **50+ 设计风格** — Glassmorphism、Claymorphism、Minimalism、Brutalism、Neumorphism、Bento Grid 等
- **161 调色板** — 精心策划的配色方案，覆盖各行业与情绪
- **57 字体配对** — 标题/正文字体组合，确保排版品质
- **161 产品类型** — Landing Page、Dashboard、SaaS、E-commerce 等场景模板
- **99 UX 准则** — 可访问性、响应式、交互状态等设计规范
- **25 图表类型** — 数据可视化组件库
- **10 技术栈** — React/Next.js、Vue/Nuxt、Svelte/SvelteKit、Flutter、React Native、SwiftUI、Tailwind CSS、shadcn/ui、HTML/CSS、Material Design

**触发词：** UI设计、UX设计、前端开发、组件创建、配色、排版、布局、动画、可访问性、landing page、dashboard、admin panel

---

### theme — 主题与品牌系统

**功能描述：** 基于语义化 Design Token 的主题系统，支持 10 种预设主题和自定义主题生成，确保从品牌定义到代码实现的一致性。

**预设主题数量：** 10 种
- Arctic Frost（极地霜冻）
- Botanical Garden（植物园）
- Desert Rose（沙漠玫瑰）
- Forest Canopy（森林冠层）
- Golden Hour（黄金时刻）
- Midnight Galaxy（午夜银河）
- Modern Minimalist（现代极简）
- Ocean Depths（海洋深处）
- Sunset Boulevard（日落大道）
- Tech Innovation（科技创新）

**触发词：** 主题、配色方案、品牌色、Design Token、暗色模式、light/dark、CSS变量、色彩系统

---

### review — 设计审查

**功能描述：** 多维度设计质量审查，对现有 UI 代码进行专业级评估，输出评分报告和改进建议。

**审查维度数量：** 7 大维度
1. **视觉层次** — 排版、间距、对比度
2. **色彩系统** — Token 使用、对比度合规、色彩和谐
3. **布局与响应式** — 网格系统、断点、流式布局
4. **交互状态** — Hover、Focus、Active、Disabled
5. **可访问性** — ARIA、键盘导航、屏幕阅读器
6. **性能** — 图片优化、字体加载、渲染性能
7. **代码质量** — 语义化 HTML、Token 使用、组件化

**触发词：** 设计审查、UI审查、UX审查、代码审查、设计质量、可访问性审查、review

---

## 工作流

### 完整工作流

```
creative → theme → design → review
  │          │         │         │
  │          │         │         └─ 多维度审查报告 + 改进建议
  │          │         └─ Design Token + 可运行代码
  │          └─ 主题定义 + CSS变量
  └─ 灵感探索 + 哲学宣言
```

1. **creative** — 探索视觉灵感，生成艺术原型，确立设计哲学
2. **theme** — 基于灵感定义主题系统，生成 Design Token
3. **design** — 基于主题进行 UI/UX 设计，输出生产级代码
4. **review** — 审查设计质量，输出评分和改进建议

### 快速通道

各子命令可独立使用：
- 仅需生成艺术 → 直接使用 `creative`
- 仅需 UI 设计 → 直接使用 `design`
- 仅需主题配色 → 直接使用 `theme`
- 仅需设计审查 → 直接使用 `review`

---

## 目录结构

```
super-frontend-design/
├── SKILL.md                    # 主 Skill 入口文件
├── README.md                   # 本文件
├── evals/
│   └── evals.json              # 评测用例（10条）
├── subskills/
│   ├── creative/
│   │   └── SKILL.md            # 生成艺术子命令
│   ├── design/
│   │   └── SKILL.md            # UI/UX 设计子命令
│   ├── review/
│   │   └── SKILL.md            # 设计审查子命令
│   └── theme/
│       └── SKILL.md            # 主题系统子命令
├── templates/
│   ├── generator_template.js   # 海报生成器模板
│   └── viewer.html             # 交互式查看器模板
├── themes/
│   ├── arctic-frost.md         # 极地霜冻主题
│   ├── botanical-garden.md     # 植物园主题
│   ├── desert-rose.md          # 沙漠玫瑰主题
│   ├── forest-canopy.md        # 森林冠层主题
│   ├── golden-hour.md          # 黄金时刻主题
│   ├── midnight-galaxy.md      # 午夜银河主题
│   ├── modern-minimalist.md    # 现代极简主题
│   ├── ocean-depths.md         # 海洋深处主题
│   ├── sunset-boulevard.md     # 日落大道主题
│   └── tech-innovation.md      # 科技创新主题
└── canvas-fonts/               # 博物馆级海报字体库
    ├── ArsenalSC-*.ttf
    ├── BigShoulders-*.ttf
    ├── Boldonse-*.ttf
    ├── BricolageGrotesque-*.ttf
    ├── CrimsonPro-*.ttf
    ├── DMMono-*.ttf
    ├── EricaOne-*.ttf
    ├── GeistMono-*.ttf
    ├── Gloock-*.ttf
    ├── IBMPlexMono-*.ttf
    ├── IBMPlexSerif-*.ttf
    ├── InstrumentSans-*.ttf
    ├── InstrumentSerif-*.ttf
    ├── Italiana-*.ttf
    ├── JetBrainsMono-*.ttf
    ├── Jura-*.ttf
    ├── LibreBaskerville-*.ttf
    ├── Lora-*.ttf
    ├── NationalPark-*.ttf
    ├── NothingYouCouldDo-*.ttf
    ├── Outfit-*.ttf
    ├── PixelifySans-*.ttf
    ├── PoiretOne-*.ttf
    ├── RedHatMono-*.ttf
    ├── Silkscreen-*.ttf
    ├── SmoochSans-*.ttf
    ├── Tektur-*.ttf
    ├── WorkSans-*.ttf
    └── YoungSerif-*.ttf
```

---

## 安装

### 安装到全局 Skill 目录

```bash
cp -r ./super-frontend-design/ ~/.skills/super-frontend-design/
```

### 安装到项目目录

```bash
cp -r ./super-frontend-design/ ./skills/super-frontend-design/
```

---

## 使用示例

### 生成艺术

```
用户: 帮我生成一个有机湍流风格的flow field
→ 路由到 creative 子命令
→ 输出哲学宣言 + 交互式HTML
```

### UI 设计

```
用户: 设计一个SaaS Dashboard
→ 路由到 design 子命令
→ 输出Design Token + 可运行代码
```

### 主题选择

```
用户: 给我配一套科技感的配色
→ 路由到 theme 子命令
→ 输出Design Token CSS变量
```

### 设计审查

```
用户: 审查一下这个页面的UI质量
→ 路由到 review 子命令
→ 输出审查报告 + 改进建议
```

---

## 技术栈支持

| 技术栈 | 框架 | 样式方案 |
|--------|------|----------|
| React | Next.js | Tailwind CSS / CSS Modules |
| Vue | Nuxt | Tailwind CSS / Scoped CSS |
| Svelte | SvelteKit | Tailwind CSS / Scoped CSS |
| Flutter | Dart | ThemeData |
| React Native | Expo | StyleSheet |
| SwiftUI | Swift | SwiftUI Modifiers |
| HTML/CSS | Vanilla | Tailwind CSS / Custom Properties |
| shadcn/ui | React | Tailwind CSS + Radix |
| Material Design | React/Vue | MUI / Vuetify |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-06-13 | 初始版本，合并10个前端设计skill |

---

## 许可证

与原 Skill 保持一致。字体文件遵循各自的 OFL（SIL Open Font License）协议。

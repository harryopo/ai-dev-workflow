# super-frontend-design v2.0.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade super-frontend-design from v1.8.0 to v2.0.0 by integrating learnings from Open Design (anti-slop craft system, 9-section DESIGN.md schema, typography rules), Aceternity UI (block classification), 21st.dev (prompt superiority), Magic UI / Inspira UI (motion/animation), and MCP integration guides.

**Architecture:** 8 phases modifying 5 existing files + creating 11 new reference/template files. Core change: Design Brief (free-form conversation notes) → structured DESIGN.md (Open Design 9-section schema) consumed by all sub-skills. Anti-AI-slop upgraded from 10 vague patterns to 14 precise, checkable rules with hex values. Typography rules codified as hard constraints.

**Tech Stack:** Markdown (SKILL.md, references), YAML (front-matter), CSS variable conventions (DESIGN.md)

---

## File Structure Map

```
projects/super-frontend-design/
├── SKILL.md                          [MODIFY: P1, P2, P8]
├── references/
│   ├── anti-ai-slop.md               [CREATE: P1]
│   ├── typography.md                 [CREATE: P3]
│   ├── design-system-template.md     [CREATE: P2]
│   ├── component-block-catalog.md    [CREATE: P4]
│   ├── mcp-integration.md            [CREATE: P6]
│   ├── brand-personality-expanded.md [CREATE: P8]
│   └── palettes.md                   [existing]
├── subskills/
│   ├── design/
│   │   └── SKILL.md                  [MODIFY: P2, P4, P7]
│   ├── creative/
│   │   └── SKILL.md                  [MODIFY: P5]
│   ├── review/
│   │   └── SKILL.md                  [MODIFY: P1, P3]
│   └── theme/
│       └── SKILL.md                  [no change needed]
├── templates/
│   └── prompt-templates/
│       ├── react-tailwind.md         [CREATE: P7]
│       ├── vue-nuxt.md               [CREATE: P7]
│       ├── react-native.md           [CREATE: P7]
│       ├── html-css.md               [CREATE: P7]
│       └── flutter.md                [CREATE: P7]
└── evals/
    └── evals.json                    [existing]
```

---

### Task 1: P1 — Create `references/anti-ai-slop.md` (14 precise rules)

**Files:**
- Create: `projects/super-frontend-design/references/anti-ai-slop.md`

- [ ] **Step 1: Write the anti-slop reference file**

Create `projects/super-frontend-design/references/anti-ai-slop.md`:

```markdown
# 去 AI 味规则（精确版）

> 基于 Open Design `craft/anti-ai-slop.md`（MIT 许可）精炼
> 合并来源：super-frontend-design v1.x 反 AI 模式 + Open Design Seven Cardinal Sins

---

## 七宗罪（P0 — design 阶段必须通过，review 阶段硬阻止）

### 1. 禁止 AI 默认色

以下 hex 值**绝对禁止**作为主色（accent）或大面积使用：

```
#6366f1  #4f46e5  #4338ca  #3730a3  #8b5cf6  #7c3aed  #a855f7
```

以上是 Tailwind CSS 默认的 indigo/purple/violet 色阶，AI 生成代码的教科书级指纹。
→ 必须使用 Design Brief 导出的 Design Token（`var(--color-primary)`）

### 2. 禁止两色渐变 Hero

以下渐变组合**绝对禁止**出现在 Hero 区域：
- `purple → blue`（#8b5cf6 → #3b82f6）
- `blue → cyan`（#3b82f6 → #06b6d4）
- `indigo → pink`（#6366f1 → #ec4899）
- 任何类似的多色渐变

→ 使用纯色底 + 排版变化，或单色微调

### 3. 禁止以下 emoji 作为功能图标

以下 emoji **绝对禁止**出现在 `<h1>` ~ `<h6>`、`<button>`、`<li>` 或 `class*="icon"` 元素中：

```
✨  🚀  🎯  ⚡  🔥  💡  🎨  🛠️
```

→ 使用 1.6–1.8px 描边的单线 SVG，`stroke="currentColor"`，来自 Lucide / Phosphor / Tabler Icons

### 4. h1/h2 必须用 var(--font-display)

标题元素**绝对禁止**硬编码字体族：
- ❌ `<h1 style="font-family: Inter, system-ui">`
- ❌ `<h1 style="font-family: Roboto, sans-serif">`
- ✅ `<h1 style="font-family: var(--font-display)">`

### 5. 禁止「圆角卡片 + 彩色左边框」

这是"AI dashboard tile"的经典形状：
```
┌──────────────────────────┐
│██  Card Title            │  ← 左边框是彩色 accent
│    Content here...       │
└──────────────────────────┘
```
→ 去掉圆角或去掉左边框，二选一，不可同时存在。

### 6. 禁止假指标

以下文案模式**绝对禁止**：
- "10× 更快" / "3× 更高效" / "99.9% 在线" / "百万级用户"
- 没有数据来源的量化声明
→ 使用真实数据，或标注 `[真实数据待填充]`

### 7. 禁止填充文案

以下内容**绝对禁止**：
- `lorem ipsum` 及任何变体
- "功能一 / 功能二 / 功能三"
- "placeholder text" / "sample content"
- 无意义的占位文字
→ 空着比假的强；空 section 是设计问题，不是文案问题

---

## 软规则（P1 — review 阶段必须警告，可人工裁定）

### 8. 禁止「Hero→Features→Pricing→FAQ→CTA」标准序列

毫无变化的 AI 模板骨架。至少引入一个非标准 section：
- 全幅引用墙（testimonial wall）
- 嵌入式产品演示
- 数据对比（comparison-against-status-quo）
- 横向滚动画廊

### 9. 禁止外部占位图片 CDN

以下域名**禁止**出现在 `<img src="">` 中：
- `unsplash.com` / `images.unsplash.com`
- `placehold.co`
- `placekitten.com`
- `picsum.photos`
→ 使用本地 SVG placeholder 或 Design Brief 指定的图源

### 10. 禁止超过 12 个裸 hex 值出现在 `:root` 之外

裸 hex 值 = 未使用 Design Token。Token 纪律体现在 CSS 变量引用率。
→ 除 `:root` 内的变量定义外，其他 CSS 中裸 hex 值 ≤ 12 个

### 11. `var(--accent)` 在同一屏使用 ≤ 2 次

Accent 色的力量在于稀缺。每屏出现 2 次以上 = 没有主次。

---

## 抛光规则（P2 — review 阶段建议修复，不强制）

### 12. 每个 section 应有 `data-section-id` 属性

便于后续编辑模式定位具体 section。

```html
<section data-section-id="hero">...</section>
<section data-section-id="features">...</section>
```

### 13. 禁止装饰性 blob / wave SVG 背景

无意义的几何形状。

### 14. 禁止完美对称布局

交替紧/松密度读起来是有意的设计：
- 一个紧凑 section → 一个呼吸 section → 一个紧凑 section
- 对称 = AI 默认，不对称 = 人设计的

---

## 如何注入设计灵魂（不复制模板）

目标：**~80% 成熟模式 + ~20% 独特选择**

那 20% 应该放在：

1. **一个大胆的排版选择** — 标题用负 tracking，卡片用非常规字号比
2. **一个有记忆点的微交互** — 按钮按下移动 2px，数字以 150ms 步进计数
3. **一个只有用过产品的人才会放的细节** — 键盘快捷键提示、特定行业术语的 status badge

### 灵魂验证问题

> 如果截屏后一个不参与项目的人能辨认出这是哪个产品的设计 → **有灵魂**
> 如果不能 → **你交付的是模板**
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/anti-ai-slop.md
git commit -m "feat: add anti-ai-slop reference file with 14 precise rules"
```

---

### Task 2: P1 — Update `SKILL.md` anti-slop section to reference new file

**Files:**
- Modify: `projects/super-frontend-design/SKILL.md`

- [ ] **Step 1: Replace the old "去 AI 味设计原则" paragraph with brief + reference**

Find the "### 去 AI 味设计原则" section in SKILL.md and replace it.

Search for this block:
```markdown
### 去 AI 味设计原则

本 Skill 识别并禁止了 10 种 AI 生成设计的标志性模板套路...
```

Replace with:
```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/SKILL.md
git commit -m "feat: link anti-ai-slop reference file in SKILL.md"
```

---

### Task 3: P1 — Update `subskills/review/SKILL.md` to add anti-slop hard checks

**Files:**
- Modify: `projects/super-frontend-design/subskills/review/SKILL.md`

- [ ] **Step 1: Insert anti-slop checklist into review §0 (after "设计灵魂追溯")**

In `subskills/review/SKILL.md`, find the section `### 0. 审查前置：设计灵魂追溯` and after the 8-item 设计灵魂检查 table and before `#### 设计灵魂评分`, insert:

```markdown

### 0.5 去 AI 味硬检查（七宗罪 — 任何一项不通过则审查不通过）

> 加载 `references/anti-ai-slop.md`，逐项检查以下 7 条。任一失败 → 审查 blocked，返回 design 阶段。

| # | 检查项 | 检测方式 | 失败动作 |
|:---:|------|---------|---------|
| 1 | **AI 默认色检测** | Grep 搜索 `#6366f1\|#4f46e5\|#4338ca\|#3730a3\|#8b5cf6\|#7c3aed\|#a855f7` | 🔴 Blocked · 列出所有违规 hex 值所在文件和行号 |
| 2 | **两色渐变 Hero** | Grep 搜索渐变模式 `linear-gradient.*#8b5cf6.*#3b82f6` 等 | 🔴 Blocked · 列出所有渐变组合 |
| 3 | **Emoji 功能图标** | Grep 搜索 emoji 在 h1-h6/button/li/icon class 中 | 🔴 Blocked · 列出所有 emoji 位置 |
| 4 | **h1/h2 硬编码字体** | Grep 搜索 `font-family:\s*(Inter\|Roboto\|system-ui)` 在 h1/h2 范围内 | 🔴 Blocked · 必须改为 var(--font-display) |
| 5 | **圆角卡片+彩色左边框** | 检查 `.card` 或类似元素同时有 border-radius 和 border-left 差异化颜色 | 🔴 Blocked · 二选一移除 |
| 6 | **假指标** | Grep 搜索 "× faster\|× 更\|% uptime\|% 在线\|百万" | 🔴 Blocked · 列出所有假指标 |
| 7 | **填充文案** | Grep 搜索 "lorem ipsum\|功能一\|功能二\|功能三\|placeholder" | 🔴 Blocked · 替换为真实文案或 [待填充] |

### 0.6 软规则检查（P1 — 警告但不会 Block）

| # | 检查项 | 检测方式 |
|:---:|------|---------|
| 8 | **标准序列** | 检查 section 顺序是否为 Hero→Features→Pricing→FAQ→CTA |
| 9 | **占位图片 CDN** | Grep 搜索 `unsplash\|placehold.co\|placekitten\|picsum.photos` |
| 10 | **裸 hex 值** | 统计 `:root` 外的 hex 值是否超 12 个 |
| 11 | **Accent 滥用** | 统计 `var(--accent)` 每屏使用次数是否 >2 |
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/subskills/review/SKILL.md
git commit -m "feat: add anti-slop hard checks (seven cardinal sins) to review sub-skill"
```

---

### Task 4: P2 — Create `references/design-system-template.md` (9-section DESIGN.md)

**Files:**
- Create: `projects/super-frontend-design/references/design-system-template.md`

- [ ] **Step 1: Write the 9-section DESIGN.md template**

Create `projects/super-frontend-design/references/design-system-template.md`:

```markdown
# DESIGN.md 模板 — 9-Section Design System

> 格式遵循 Open Design `DESIGN.md` 约定，可被 Agent / Linter / Renderer 消费
> 所有 CSS 变量必须在 `:root {}` 块内

---

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

<!-- 从 research 第 4 轮对话的"品牌人格 + 情绪板"自动填充 -->

```markdown
**品牌人格**：{极客工程师 / 优雅艺术家 / 活力创业者 / 权威专家 / 温暖朋友 / 叛逆先锋 / 极简主义者}

**情绪板**：{词1}、{词2}、{词3}

**设计意图**：{一句话描述这个设计应该让用户感受到什么}

**不适合的场景**：{这个设计系统明确不适用于什么}

**参考先例**：{用户选择的企业参考风格}
```

## 2. 配色 (Color)

```css
:root {
  /* 主色 */
  --color-primary: #XXXXXX;
  --color-primary-hover: #XXXXXX;
  --color-primary-light: #XXXXXX;

  /* 中性色 */
  --color-bg: #XXXXXX;
  --color-surface: #XXXXXX;
  --color-surface-hover: #XXXXXX;
  --color-border: #XXXXXX;
  --color-divider: #XXXXXX;

  /* 文字色 */
  --color-text: #XXXXXX;
  --color-text-secondary: #XXXXXX;
  --color-text-tertiary: #XXXXXX;

  /* 语义色 */
  --color-success: #XXXXXX;
  --color-warning: #XXXXXX;
  --color-error: #XXXXXX;
  --color-info: #XXXXXX;

  /* 强调色 — 全屏使用不超过 2 次 */
  --color-accent: #XXXXXX;
}

/* 暗色模式覆盖 */
[data-theme="dark"] {
  --color-bg: #XXXXXX;
  --color-surface: #XXXXXX;
  --color-surface-hover: #XXXXXX;
  --color-border: #XXXXXX;
  --color-text: #XXXXXX;
  --color-text-secondary: #XXXXXX;
}
```

**配色决策记录**：
- 主色选择理由：{为什么选这个色}
- 暗色模式策略：{如果启用暗色}

## 3. 排版 (Typography)

```css
:root {
  --font-display: "{Display 字体}", {fallback};
  --font-body: "{Body 字体}", {fallback};
  --font-mono: "{Mono 字体}", ui-monospace, monospace;

  /* 字号阶乘（1.25 乘法比例） */
  --text-display: 56px;
  --text-h1: 36px;
  --text-h2: 28px;
  --text-h3: 22px;
  --text-body: 16px;
  --text-small: 14px;
  --text-caption: 12px;

  /* 字间距 — ALL CAPS 必须有 ≥0.06em tracking */
  --tracking-caps: 0.08em;
  --tracking-display: -0.02em;
}
```

Font labels for catalog extraction:
Display: "{Display 字体}", {fallback}
Body: "{Body 字体}", {fallback}
Mono: "{Mono 字体}", ui-monospace, monospace

**行高规范**：
- Display / H1 (≥32px): `line-height: 1.0–1.2`
- Body (15–18px): `line-height: 1.5–1.6`
- Small (≤14px): `line-height: 1.5`

**字重系统（恰好 3 个 weight）**：
- Read (400): body copy
- Emphasize (500–550): UI text, labels, navigation
- Announce (600): headlines, buttons

## 4. 间距 (Spacing)

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
}
```

**正文最大宽度**：`max-width: 65ch`

## 5. 布局与构图 (Layout & Composition)

```
{左侧导航 + 右侧内容 / 单列垂直滚动 / 多列卡片网格 / 杂志式分栏}

Section 节奏：{紧-松-紧} 交替，禁止全对称。
```

## 6. 组件 (Components)

> 每个组件必须使用 CSS 语义变量。禁止硬编码 #hex 值。

### 按钮 (Button)

```css
.button-primary {
  background: var(--color-primary);
  color: white;
  border-radius: {X}px;
  padding: var(--space-sm) var(--space-lg);
  font-family: var(--font-body);
  font-weight: 600;
  transition: transform 100ms ease-in;
}
.button-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}
.button-primary:active {
  transform: translateY(1px);
}
.button-primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### 卡片 (Card)

```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: {X}px;
  padding: var(--space-lg);
}
```

### 标签 / Badge

```css
.badge {
  font-size: var(--text-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  padding: 2px 8px;
  border-radius: 4px;
}
.badge-success { background: rgba({success-r}, {success-g}, {success-b}, 0.15); color: var(--color-success); }
.badge-warning { background: rgba({warning-r}, {warning-g}, {warning-b}, 0.15); color: var(--color-warning); }
.badge-error   { background: rgba({error-r}, {error-g}, {error-b}, 0.15); color: var(--color-error); }
```

### 表单 (Form)

```css
.form-input {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: {X}px;
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-body);
  font-size: var(--text-body);
}
.form-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 2px rgba({primary-r}, {primary-g}, {primary-b}, 0.2);
}
.form-input.error {
  border-color: var(--color-error);
}
.form-label {
  font-size: var(--text-small);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xs);
}
```

### 数据表格 (Data Table)

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th {
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: var(--text-small);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
  text-align: left;
}
.data-table td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-divider);
  font-family: var(--font-mono);
  font-size: var(--text-small);
}
.data-table tr:hover td {
  background: var(--color-surface-hover);
}
```

## 7. 动效与交互 (Motion & Interaction)

```css
:root {
  --transition-fast: 100ms ease-in;
  --transition-base: 150ms ease-out;
  --transition-slow: 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .button-primary { transition: none; }
}
```

**动效策略**：{无动效 / hover 微过渡 / 页面切换动画 / 粒子特效}

## 8. 语调与品牌 (Voice & Brand)

- **品牌语调**：{专业冷静 / 友好温暖 / 大胆自信 / 极简冷静}
- **微文案风格**：{命令式 / 对话式 / 技术式}
- **产品名称**：{来自用户输入}

## 9. 禁止模式 (Anti-patterns)

> 详见 `references/anti-ai-slop.md`。summary below:

```
1. 禁止 AI 默认色（#6366f1 / #4f46e5 / #8b5cf6 等）
2. 禁止两色渐变 Hero
3. 禁止 emoji 作为功能图标
4. h1/h2 必须使用 var(--font-display)
5. 禁止圆角卡片 + 彩色左边框
6. 禁止假指标
7. 禁止填充文案
8. 禁止标准 Hero→Features→Pricing→FAQ→CTA 序列
9. 禁止外部占位图片 CDN
10. 禁止超过 12 个裸 hex 值在 :root 之外
11. var(--accent) 每屏使用 ≤2 次
12. 禁止装饰性 blob/wave SVG
13. 禁止完美对称布局
14. 每个 section 应有 data-section-id
```

---

## 使用说明

1. research 阶段结束时自动填充此模板的 `{}` 占位符
2. 所有颜色值必须验证 WCAG AA 对比度（≥4.5:1）
3. 暗色模式覆盖值必须不同于 light 模式值
4. 组件 CSS 中不得出现裸 hex 值 — 必须使用 `var(--color-*)`
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/design-system-template.md
git commit -m "feat: add 9-section DESIGN.md template (Open Design compatible)"
```

---

### Task 5: P2 — Update `SKILL.md` research Phase 0 to output DESIGN.md

**Files:**
- Modify: `projects/super-frontend-design/SKILL.md`

- [ ] **Step 1: Add DESIGN.md output instruction to research phase**

In SKILL.md, find the section about research phase outputs (after the 4 rounds of AskUserQuestion). Look for the Design Brief output description. Add the following after "### Design Brief 产出" or similar section:

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/SKILL.md
git commit -m "feat: research phase now outputs 9-section DESIGN.md"
```

---

### Task 6: P3 — Create `references/typography.md`

**Files:**
- Create: `projects/super-frontend-design/references/typography.md`

- [ ] **Step 1: Write the typography reference file**

Create `projects/super-frontend-design/references/typography.md`:

```markdown
# Typography 硬规则

> 基于 Open Design `craft/typography.md`（MIT 许可）精炼
> 这些规则覆盖 DESIGN.md 的排版 section，是 design 和 review 阶段的硬约束

---

## 1. 字号阶（乘法比例 1.2 或 1.25）

| 角色 | 字号范围 | 用途 |
|------|:---:|------|
| Display | 48–72 px | 品牌展示、超级标题 |
| H1 | 32–48 px | 页面标题 |
| H2 | 24–32 px | Section 标题 |
| H3 | 20–24 px | 子标题 |
| Body | 15–18 px | 正文 |
| Small | 13–14 px | UI 标签、辅助文字 |
| Caption | 11–12 px | 脚注、时间戳 |

每页面可见字号 ≤ 6–8 种。

---

## 2. 行高 (Line Height)

| 文字大小 | 行高 | 说明 |
|----------|:---:|------|
| Display / H1 (≥32 px) | `1.0 – 1.2` | 紧凑 |
| Body (15–18 px) | `1.5 – 1.6` | 标准可读 |
| Small (≤14 px) | `1.5` | 最小 |

---

## 3. 字间距 (Letter Spacing) — AI 最大盲区

| 上下文 | 字间距 | 强制性 |
|--------|:---:|:---:|
| Body text (14–18 px) | `0` (默认) | 必须 |
| Small text (11–13 px) | `0.01em – 0.02em` (正值) | 必须 |
| UI 标签和按钮文字 | `0.02em` | 必须 |
| **ALL CAPS** | **`0.06em – 0.1em`** | **绝对必须** |
| Headings 32 px+ | `-0.01em – -0.02em` | 必须 |
| Display 48 px+ | `-0.02em – -0.03em` | 必须 |

**为什么 ALL CAPS 需要 0.06em tracking：**
不带此规则的 ALL CAPS 文字看起来拥挤且业余。这是 AI 生成设计中最可靠的"AI 指纹"之一。
0.06em 下限来自印刷和网页排版实践的收敛值（参考 Bringhurst《The Elements of Typographic Style》§3.2.7）。

---

## 4. 字体配对

- 每个页面最多 **2 个 typeface**（display + body，或一个可变字体多 weight）
- 始终声明系统回退链
- **禁止** `font-family: system-ui` 单独用于标题 — 这是教科书级 AI 默认

```css
/* ✅ 正确 */
h1 { font-family: var(--font-display); }
body { font-family: var(--font-body); }

/* ❌ 错误 — AI 默认 */
h1 { font-family: Inter, system-ui, sans-serif; }
```

---

## 5. 正文最大宽度

```
max-width: 65ch
```

65 字符/行是 web 正文的可读性安全宽度（约 50–75 字符范围）。

---

## 6. 三 Weight 系统

大多数精心设计的 UI 恰好使用 3 个 weight：

| Weight | 数值 | 用途 |
|--------|:---:|------|
| **Read** | 400 / 450 | body copy |
| **Emphasize** | 500 / 550 | UI text, labels, navigation |
| **Announce** | 600 | headlines, buttons |

Weight 700+ 极少需要。如果你的设计用了 Bold on Bold，说明其他地方缺少 weight 纪律。

---

## 7. review 阶段 Typography 检查清单

| # | 检查项 | 检测方式 | 严重度 |
|:---:|------|---------|:---:|
| T1 | ALL CAPS 缺少 letter-spacing ≥ 0.06em | Grep `text-transform:\s*upper` 并检查 letter-spacing | 🔴 High |
| T2 | Display text ≥32px 缺少负 tracking | 检查 ≥32px 的文本元素是否有 letter-spacing 负值 | 🟡 Medium |
| T3 | Body text 行高 < 1.5 | 检查 15–18px 文本的 line-height | 🟡 Medium |
| T4 | Body copy 行宽超 75 字符 | 计算 `max-width` 字符数 | 🟡 Medium |
| T5 | >2 个 typeface 在同一页面 | 统计 `font-family` 声明中的第一字体 | 🟡 Medium |
| T6 | `font-family: system-ui` 在标题元素 | Grep `h[1-6].*font-family.*system-ui` | 🔴 High |
| T7 | Weight 超过 3 个 | 统计 `font-weight` 值种类 | 🟢 Low |
| T8 | `text-align: justify` 在 body copy | Grep `text-align:\s*justify` | 🔴 High |
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/typography.md
git commit -m "feat: add typography hard rules reference file"
```

---

### Task 7: P3 — Update `subskills/review/SKILL.md` with typography checks

**Files:**
- Modify: `projects/super-frontend-design/subskills/review/SKILL.md`

- [ ] **Step 1: Insert typography checklist into review §2 (after anti-slop section)**

In `subskills/review/SKILL.md`, find the review dimensions section and add a new dimension. Look for "### 2. 审查维度" and after the list of dimensions add:

```markdown

### 2.X Typography 硬检查（基于 references/typography.md）

> 加载 `references/typography.md`，逐项检查以下 8 条。

| # | 检查项 | 检测方式 | 不通过 |
|:---:|------|---------|:---:|
| T1 | ALL CAPS letter-spacing | Grep `text-transform:.*upper` 检查是否有 `letter-spacing` | 🔴 |
| T2 | Display tracking | 检查 ≥48px 元素是否有 `letter-spacing: -0.02em` 或更紧 | 🟡 |
| T3 | Body line-height | 检查 15-18px 文本 `line-height` ≥ 1.5 | 🟡 |
| T4 | 行宽 | 检查 body copy `max-width` ≤ 75ch | 🟡 |
| T5 | Typeface 数量 | 统计不同 font-family 第一字体 ≤ 2 | 🟡 |
| T6 | system-ui 标题 | Grep h1-h6 中 `font-family:.*system-ui`（非 var(--font-display)） | 🔴 |
| T7 | Weight 数量 | 统计 font-weight 种类 ≤ 3 | 🟢 |
| T8 | justify | Grep `text-align: justify` | 🔴 |

**检查结果格式**：

```markdown
## Typography 检查报告

| # | 状态 | 位置 | 详情 |
|:---:|:---:|------|------|
| T1 | ✅ PASS | — | ALL CAPS 均含 letter-spacing ≥ 0.06em |
| T2 | ⚠️ FAIL | index.html:45 | `<h1>` 48px 缺少负 tracking |
| ... | ... | ... | ... |
```
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/subskills/review/SKILL.md
git commit -m "feat: add typography hard checks to review sub-skill"
```

---

### Task 8: P4 — Create `references/component-block-catalog.md`

**Files:**
- Create: `projects/super-frontend-design/references/component-block-catalog.md`

- [ ] **Step 1: Write the block catalog**

Create `projects/super-frontend-design/references/component-block-catalog.md`:

```markdown
# 组件 Block 分类目录

> 基于 Aceternity UI 的 Block 分类体系 + 21st.dev 的组件市场结构
> design 阶段根据用户需求自动匹配对应 Block 类型生成设计卡

---

## Block 类型总览

| Block 类型 | 适用场景 | 参考来源 | 设计要点 |
|-----------|---------|---------|---------|
| **Hero Sections** | 首页首屏 | Aceternity UI (21+) / 21st.dev | 排版冲击 > 图片，禁止渐变背景 |
| **Feature Sections** | 产品特性展示 | Aceternity UI (18+) | Bento Grid 或交错布局，非均匀卡片 |
| **Bento Grids** | 特性聚合展示 | Aceternity UI (6+) / Magic UI | 大小卡片拼贴，视觉节奏不重复 |
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
- 动效: {动效描述}
- 禁止: {反 AI 规则}
```

---

## 全局参考索引

| 参考库 | 类型 | 访问方式 |
|--------|------|---------|
| Aceternity UI | React/Tailwind 组件 | https://ui.aceternity.com |
| 21st.dev | React/Tailwind/shadcn 组件市场 | https://21st.dev |
| Magic UI | React/Tailwind 动画组件 | https://magicui.design |
| shadcn/ui | React 基础组件 | https://ui.shadcn.com |
| Inspira UI | Vue/Nuxt 3D 动画组件 | https://inspira-ui.com |
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/component-block-catalog.md
git commit -m "feat: add component block catalog with 18 block types"
```

---

### Task 9: P4 — Update `subskills/design/SKILL.md` Block classification

**Files:**
- Modify: `projects/super-frontend-design/subskills/design/SKILL.md`

- [ ] **Step 1: Add Block-based design workflow**

In `subskills/design/SKILL.md`, after the "### 设计工作流（从 Design Brief 提取，禁止自填）" section, add:

```markdown

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
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/subskills/design/SKILL.md
git commit -m "feat: add block-based design workflow with automatic matching"
```

---

### Task 10: P5 — Update `subskills/creative/SKILL.md` with animation/effect mappings

**Files:**
- Modify: `projects/super-frontend-design/subskills/creative/SKILL.md`

- [ ] **Step 1: Add Aceternity UI + Inspira UI effect mappings**

In `subskills/creative/SKILL.md`, after the visual thesis section (after "### 动效方向"), add:

```markdown

### 动效方向扩展（v2.0 — 整合 Aceternity UI + Inspira UI）

> 以下特效类型来自 Aceternity UI（React/Tailwind）和 Inspira UI（Vue/Nuxt 3D）的实际组件设计模式。仅借鉴设计模式，不复制代码。

#### 着色器特效 (Shader Effects)

| 特效 | 来源 | 适用场景 | 技术特征 |
|------|------|---------|---------|
| Dither Shader | Aceternity UI | Pixel art / 复古风格 | 实时有序抖动 |
| Noise Background | Aceternity UI | 氛围背景 | 动画渐变 + 噪点纹理 |
| Background Beams | Aceternity UI | Hero 背景 | 碰撞爆炸光束 |
| Background Lines | Aceternity UI | Hero 背景 | SVG 波形路径 |
| Ripple Effect | Aceternity UI | 交互反馈 | 点击涟漪网格 |

#### 文字特效 (Text Effects)

| 特效 | 来源 | 适用场景 | 技术特征 |
|------|------|---------|---------|
| Squiggly Text | Aceternity UI | 品牌标题 | SVG turbulence + displacement |
| Encrypted Text | Aceternity UI | 技术产品 | 渐进揭示 + 乱码过渡 |
| Text Flipping Board | Aceternity UI | 数据展示 | 翻转板动画 |
| Canvas Text | Aceternity UI | 创意品牌 | Canvas 绘制彩色线条 |
| Colourful Text | Aceternity UI | 趣味场景 | 多彩滤镜 + 缩放 |
| ASCII Art | Aceternity UI | 极客/终端主题 | 图片 → ASCII 转换 |

#### 3D 交互 (3D Interactions)

| 特效 | 来源 | 适用场景 | 技术特征 |
|------|------|---------|---------|
| 3D Card Effect | Aceternity UI | 卡片展示 | 透视悬浮提升 |
| Macbook Scroll | Aceternity UI | 产品展示 | 图片出屏效果 |
| 3D Globe | Aceternity UI | 全球分布 | 真实地理 globe |
| 3D Scene | Inspira UI | 沉浸式背景 | Three.js 场景 + 物理 |

#### 微交互 (Micro-interactions)

| 特效 | 来源 | 适用场景 | 技术特征 |
|------|------|---------|---------|
| Magnetic Button | Aceternity UI | CTA 按钮 | 光标磁吸 + 弹簧回弹 |
| Card Spotlight | Aceternity UI | 卡片 hover | 光标跟随径向渐变 |
| Gooey Input | Aceternity UI | 搜索框 | SVG 滤镜粘性扩展 |
| Tooltip Card | Aceternity UI | 悬停提示 | 跟随鼠标浮动卡片 |

#### 视觉论文·动效方向扩展

在 creative 阶段输出视觉论文时，动效方向新增以下选项：

| 动效方向 | 关键词 | 对应组件 |
|---------|--------|---------|
| Shader Effects | "着色器"/"噪点"/"光束"/"像素" | Dither + Noise + Beams |
| Text Effects | "文字动效"/"翻转"/"加密" | Squiggly + Encrypted + Flipping |
| 3D Scene | "3D"/"三维"/"Three.js" | 3D Globe + 3D Scene |
| Micro-interaction | "微交互"/"磁吸"/"弹性" | Magnetic + Spotlight + Gooey |

> **约束**：动效选择必须与品牌人格匹配。极客工程师 → Text Effects + Shader；优雅艺术家 → 3D + 微交互；极简主义者 → 仅 hover 过渡；温暖朋友 → 弹性动效。
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/subskills/creative/SKILL.md
git commit -m "feat: add Aceternity UI + Inspira UI effect mappings to creative sub-skill"
```

---

### Task 11: P6 — Create `references/mcp-integration.md`

**Files:**
- Create: `projects/super-frontend-design/references/mcp-integration.md`

- [ ] **Step 1: Write the MCP integration guide**

Create `projects/super-frontend-design/references/mcp-integration.md`:

```markdown
# MCP 集成指南

> 本 Skill 是 Agent 内运行的设计 Skill，可通过配置以下 MCP Server 增强能力。
> 所有 MCP Server 都是可选的 — 本 Skill 在不配置任何 MCP 的情况下也可独立运行。

---

## 推荐 MCP Server

### 1. 21st.dev Magic MCP — 组件灵感搜索 + shadcn 组件生成

**用途**：在 design 阶段搜索 21st.dev 上数千个经过审核的高质量 UI 组件，生成 shadcn/compatible 组件代码。

**安装**：

```bash
# 方式 1：CLI 一键安装
npx @21st-dev/cli@latest install cursor --api-key <your-key>

# 方式 2：手动配置
# 在 ~/.cursor/mcp.json（或对应 IDE 的 MCP 配置）中添加：
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest", "API_KEY=\"your-api-key\""]
    }
  }
}
```

**API Key 获取**：https://21st.dev/magic/console

**在 Skill 中的使用**：
- design 阶段：输入 `/ui create a modern data table with sorting and pagination`
- 生成结果会包含 21st.dev 的组件设计知识
- GitHub: https://github.com/21st-dev/magic-mcp

---

### 2. Figma MCP — 设计稿上下文读取

**用途**：如果有 Figma 设计稿，直接读取设计上下文、CSS Token、组件结构，大幅减少 research 阶段的手动对话轮次。

**安装**：

```bash
# Figma MCP 是 Figma 官方提供的远程 MCP Server
# 需要 Figma 访问 Token 和文件 URL
# 配置参考：https://www.figma.com/mcp
```

**在 Skill 中的使用**：
- research 阶段：读取 Figma 设计稿 → 自动填充 DESIGN.md 的 Color / Typography / Spacing 等 section
- design 阶段：参考设计稿的 Token 生成代码
- review 阶段：对比 Figma 设计稿验证还原度

---

### 3. ShadCN MCP — shadcn/ui 组件生成

**用途**：在 design 阶段直接生成 shadcn/ui 兼容的组件代码。

**安装**：

```bash
# shadcn MCP 配置
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn", "mcp"]
    }
  }
}
```

**在 Skill 中的使用**：
- design 阶段：生成基础组件（Button、Card、Input 等）后，Agent 在此基础上应用 DESIGN.md 的定制样式

---

### 4. Open Design MCP — 150+ 设计系统访问

**用途**：如果已安装 Open Design 桌面应用，可直接访问其 150+ 品牌设计系统和 261 个插件。

**安装**：

```bash
# 先安装 Open Design 桌面应用
# https://open-design.ai/
# 然后安装 MCP 到 Agent
od mcp install claude    # Claude Code
od mcp install cursor    # Cursor
od mcp install trae      # Trae
```

**在 Skill 中的使用**：
- research 阶段：浏览 150+ 设计系统寻找参考
- design 阶段：注入匹配的 DESIGN.md 到上下文

---

## MCP 与 Skill 阶段对应表

| Skill 阶段 | 推荐 MCP | 效果 |
|:---:|------|------|
| research | Figma MCP + Open Design MCP | 自动读取设计稿 + 浏览设计系统库 |
| creative | — | 创意阶段不依赖 MCP |
| theme | — | 依赖 DESIGN.md |
| design | 21st.dev Magic MCP + ShadCN MCP | 组件灵感 + 代码生成 |
| review | Figma MCP | 设计稿对比验证 |

---

## 不使用 MCP 时的回退

本 Skill 的核心价值在于**调研驱动的设计方法论**和**去 AI 味规则**，不依赖任何 MCP Server。

不配置任何 MCP 时：
- 搜索设计参考 → 走 SKILL.md 的 14 个设计作品平台 WebSearch 流程
- 组件生成 → Agent 直接编码（已有 50+ 风格 / 161 色板 / 99 UX 准则）
- 设计对比 → review 子技能的 15 维度 + 8 项设计灵魂追溯
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/mcp-integration.md
git commit -m "feat: add MCP integration guide (4 MCP servers)"
```

---

### Task 12: P7 — Create 5 prompt template files

**Files:**
- Create: `projects/super-frontend-design/templates/prompt-templates/react-tailwind.md`
- Create: `projects/super-frontend-design/templates/prompt-templates/vue-nuxt.md`
- Create: `projects/super-frontend-design/templates/prompt-templates/react-native.md`
- Create: `projects/super-frontend-design/templates/prompt-templates/html-css.md`
- Create: `projects/super-frontend-design/templates/prompt-templates/flutter.md`

- [ ] **Step 1: Create React + Tailwind prompt template**

Create `projects/super-frontend-design/templates/prompt-templates/react-tailwind.md`:

```markdown
# React + Tailwind CSS Prompt 模板

> 在生成组件设计卡时使用以下模板格式。
> `{...}` 为从 DESIGN.md 和视觉论文中动态填充的变量。

---

## Block: {Block 类型}

```
生成一个 React + Tailwind CSS 的 {Block 类型名称} 组件。

**全局约束**：
- 配色: 主色 var(--color-primary) = {hex}，背景 var(--color-bg) = {hex}，表面 var(--color-surface) = {hex}
- 字体: 标题 var(--font-display)，正文 var(--font-body)，等宽 var(--font-mono)
- 暗色模式: {是/否}·{是时使用 [data-theme="dark"] 覆盖}
- 品牌人格: {品牌人格类型} → {对应的设计特征}

**排版约束**：
- ALL CAPS 元素必须有 letter-spacing ≥ 0.08em
- Display 文字 (≥48px) 必须有 letter-spacing: -0.02em
- Body 文字行高 ≥ 1.5
- Body copy max-width: 65ch
- 恰好 3 个 font-weight (400 / 550 / 600)

**动效**：
- {动效描述，来自视觉论文 motion-direction}
- prefers-reduced-motion 必须禁用动效

**禁止**：
- ❌ hex #6366f1 #4f46e5 #4338ca #8b5cf6 #7c3aed
- ❌ 两色渐变 (purple→blue / blue→cyan / indigo→pink)
- ❌ emoji 图标 (✨🚀🎯⚡🔥💡🎨🛠️)
- ❌ 圆角卡片 + 彩色左边框组合
- ❌ 假指标 ("10× faster")
- ❌ 填充文案 (lorem ipsum)
- ❌ 外部占位图片 CDN
- ❌ >12 个裸 hex 值在 :root 之外
- ❌ var(--accent) 在同一屏幕超过 2 次
- ❌ 装饰性 blob/wave SVG 背景
- ❌ 完美对称布局

**参考**：
- Design Brief: output/design-system.md
- 参考源: Aceternity UI · 21st.dev
```

---

## 按钮 (Button) Prompt 模板

```
生成 React + Tailwind CSS 按钮组件：
- 类型: {primary / secondary / ghost / danger}
- 状态: default, hover, active, focus-visible, disabled
- 圆角: {4px / 8px / full}
- 动效: hover 时 translateY(-1px)，active 时 translateY(1px)
- CSS 变量: var(--color-primary) / var(--color-primary-hover)
- focus-visible: outline 2px solid var(--color-primary) + 2px offset
- 字体: var(--font-body), weight 600, letter-spacing 0.02em
- 禁止: 渐变背景、过度阴影、emoji
```

## 卡片 (Card) Prompt 模板

```
生成 React + Tailwind CSS 卡片组件：
- 背景: var(--color-surface)
- 边框: 1px solid var(--color-border)
- 圆角: {8px}
- 间距: padding var(--space-lg)
- hover: 轻微 shadow，非大幅提升
- 禁止: 圆角 + 彩色左边框组合
- 禁止: 毛玻璃背景
```

## 数据表格 (Data Table) Prompt 模板

```
生成 React + Tailwind CSS 数据表格组件：
- 表头: var(--color-surface) 背景，text-transform uppercase + tracking 0.08em
- 行交替: var(--color-bg) / var(--color-surface-hover)
- 数值列: font-family var(--font-mono), text-align right
- 排序: 16px SVG 箭头图标 column header
- Hover: tr:hover td { background: var(--color-surface-hover) }
- 分页: 右下角，简洁数字 + < > 箭头
- 禁止: 卡片包裹、彩色斑马纹、大圆角、阴影
```

## 表单 (Form) Prompt 模板

```
生成 React + Tailwind CSS 表单组件：
- 标签: 上置 label，font-size var(--text-small)，color var(--color-text-secondary)
- 输入框: height 40px，border 1px var(--color-border)，border-radius {4px}
- 聚焦态: border-color var(--color-primary) + box-shadow 0 0 0 2px (primary 20% opacity)
- 错误态: border-color var(--color-error)，下方 error message
- 提交按钮: 右对齐 primary button
- 禁止: 过于夸张的动效、缺少 label、placeholder 作为 label
```

## 导航 (Navigation) Prompt 模板

```
生成 React + Tailwind CSS 导航组件：
- 桌面: 左侧 sidebar（{宽度}px），{暗色/亮色}背景
- 导航项: padding var(--space-sm) var(--space-md)，hover var(--color-surface-hover)
- 激活态: 左边框或背景高亮
- 移动端: 汉堡菜单 → 滑出 sidebar
- 图标: 16-20px SVG，stroke="currentColor"
- 禁止: emoji 图标、过于花哨的动效、多级嵌套（最多 1 层）
```
```

- [ ] **Step 2: Create Vue + Nuxt prompt template**

Create `projects/super-frontend-design/templates/prompt-templates/vue-nuxt.md`:

```markdown
# Vue 3 + Nuxt + Tailwind CSS Prompt 模板

> 与 React 模板共享相同的设计约束（反 AI 规则、Typography 硬规则等），仅框架语法不同。
> 完整约束见 `react-tailwind.md`，这里列 Vue 特有部分。

---

## Block: {Block 类型}

```
生成一个 Vue 3 + Nuxt + Tailwind CSS 的 {Block 类型名称} 组件。

**框架约定**：
- 使用 `<script setup lang="ts">`
- 使用 Composition API
- 响应式数据用 `ref()` / `computed()`
- 组件 props 用 `defineProps<T>()`
- 事件用 `defineEmits<T>()`

**技术栈**：
- Vue 3.4+
- Nuxt 3 (如果涉及路由/SEO)
- Tailwind CSS 3.4+
- @nuxtjs/tailwindcss 模块
- Lucide Vue Next (图标)

**全局约束**：见 react-tailwind.md 全局约束部分（配色/字体/排版/动效/禁止 全部相同）

**Vue 特有禁止**：
- ❌ 不要在 `<style scoped>` 中定义 CSS 变量（应在全局 styles 或 nuxt.config 中）
- ❌ 不要使用 Options API
- ❌ 不要使用 `v-for` key 为 index

**示例结构**：
```vue
<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
  items: Item[]
}

const props = defineProps<Props>()
const active = ref<string | null>(null)
</script>

<template>
  <section data-section-id="{block-slug}">
    <!-- component content -->
  </section>
</template>
```
```

---

## Inspira UI 组件（Vue 3D 专场）

当创意方向涉及 3D/动画时，参考 Inspira UI (https://inspira-ui.com)：

```
生成一个 Vue 3 + Nuxt 的 {3D 组件}：
- 使用 Three.js + GSAP
- 可参考 Inspira UI 的 {组件名} 组件
- 性能：仅在视窗内渲染（IntersectionObserver）
- 资源：按需加载 Three.js 模块
```
```

- [ ] **Step 3: Create React Native prompt template**

Create `projects/super-frontend-design/templates/prompt-templates/react-native.md`:

```markdown
# React Native + NativeWind Prompt 模板

> React Native 移动端组件生成模板。
> 设计约束同 react-tailwind.md，适配移动端布局。

---

## Block: {Block 类型}

```
生成一个 React Native + NativeWind 的 {Block 类型名称} 移动端组件。

**框架约定**：
- React Native 0.73+
- NativeWind 4+ (Tailwind CSS 运行时)
- Expo Router (路由)
- Lucide React Native (图标)
- 使用 `<View>` / `<Text>` / `<ScrollView>` / `<FlatList>`

**移动端适配**：
- 最小触摸目标: 44x44px
- 安全区域: SafeAreaView
- 键盘避让: KeyboardAvoidingView
- 滚动物理: 原生动量

**全局约束**：见 react-tailwind.md（配色/字体/反 AI 规则全相同）

**移动端特有禁止**：
- ❌ hover 效果（移动端无 hover）
- ❌ 桌面端 fixed sidebar
- ❌ 横向滚动（除非显式需要）
- ❌ 过小的文字 (≤11px)

**焦点状态**：
- 使用 AccessibilityInfo + focus 事件
- 所有交互元素有 accessible label
```

---

## 核心组件模板

### 卡片 (移动端)

```
生成 React Native 卡片组件：
- 背景: var(--color-surface)
- 圆角: 12px
- 间距: padding 16px
- 触摸反馈: Pressable + opacity 0.8 onPressIn
- 禁止: 阴影层级 >2
```

### 底部导航 (移动端)

```
生成 React Native 底部 Tab 导航：
- 高度: 56px + safe area bottom
- 背景: var(--color-bg)
- 分隔线: 1px var(--color-border)
- 图标: 24px SVG，激活态 var(--color-primary)，非激活态 var(--color-text-tertiary)
- 标签: 10px caption，激活态 primary
- 禁止: emoji 图标、超过 5 个 tab
```

### 表单 (移动端)

```
生成 React Native 表单组件：
- 标签: 上置，14px，color var(--color-text-secondary)
- 输入框: height 48px，border 1px var(--color-border)，border-radius 8px
- 聚焦: border-color var(--color-primary) + 2px primary 光晕
- 提交: 全宽 48px primary 按钮
- 禁止: placeholder 替代 label
```
```

- [ ] **Step 4: Create HTML/CSS prompt template**

Create `projects/super-frontend-design/templates/prompt-templates/html-css.md`:

```markdown
# 纯 HTML/CSS Prompt 模板

> 零依赖、单文件输出。
> 所有 CSS 变量定义在 `:root {}`，暗色模式用 `[data-theme="dark"]`。

---

## Block: {Block 类型}

```
生成一个纯 HTML/CSS 的 {Block 类型名称}（单文件，零依赖）。

**文件结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{页面标题}</title>
  <style>
    :root { /* DESIGN.md 的所有变量 */ }
    [data-theme="dark"] { /* 暗色覆盖 */ }
    /* 组件样式 — 禁止裸 hex 值 */
  </style>
</head>
<body>
  <!-- 语义化 HTML -->
</body>
</html>
```

**HTML 语义要求**：
- 使用 `<main>` / `<nav>` / `<section>` / `<article>` / `<footer>`
- 每个 section 有 `data-section-id`
- 图片使用 `loading="lazy"` + `alt`
- 表单使用 `<label>` + `<input>` 正确关联

**CSS 要求**：
- 所有颜色使用 CSS 变量
- 响应式：@media (max-width: 768px) 移动端适配
- prefers-reduced-motion: reduce 必须禁用动效
- :focus-visible 必须为所有交互元素定义

**全局约束**：见 react-tailwind.md（反 AI 规则 + Typography 硬规则全相同）

**纯 HTML 特有禁止**：
- ❌ 外部 CSS 文件（全部内联在 `<style>`）
- ❌ 外部字体 CDN（使用系统字体回退）
- ❌ JavaScript 框架引用（纯原生）
- ❌ 不完整的 HTML 结构（必须有 doctype + head + body）
```

---

## 核心组件模板

### 按钮 (纯 HTML)

```html
<button class="btn-primary" type="button">
  按钮文字
</button>

<style>
.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: var(--space-sm) var(--space-lg);
  font-family: var(--font-body);
  font-weight: 600;
  font-size: var(--text-body);
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: transform 100ms ease-in;
}
.btn-primary:hover { background: var(--color-primary-hover); transform: translateY(-1px); }
.btn-primary:active { transform: translateY(1px); }
.btn-primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

### 卡片 (纯 HTML)

```html
<article class="card">
  <h3 class="card-title">卡片标题</h3>
  <p class="card-body">卡片内容...</p>
</article>

<style>
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--space-lg);
}
.card:hover { border-color: var(--color-primary); }
</style>
```

### 表单 (纯 HTML)

```html
<form class="form">
  <label class="form-label" for="name">姓名</label>
  <input class="form-input" type="text" id="name" required>

  <label class="form-label" for="email">邮箱</label>
  <input class="form-input" type="email" id="email" required>

  <button class="btn-primary" type="submit">提交</button>
</form>

<style>
.form-label {
  display: block;
  font-size: var(--text-small);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xs);
}
.form-input {
  width: 100%;
  height: 40px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-body);
  font-size: var(--text-body);
  margin-bottom: var(--space-md);
  box-sizing: border-box;
}
.form-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 2px rgba({primary-r}, {primary-g}, {primary-b}, 0.2);
}
.form-input.error { border-color: var(--color-error); }
</style>
```
```

- [ ] **Step 5: Create Flutter prompt template**

Create `projects/super-frontend-design/templates/prompt-templates/flutter.md`:

```markdown
# Flutter Prompt 模板

> Flutter 移动端/桌面端组件生成模板。
> 设计约束同 react-tailwind.md，适配 Material Design 3 + Design Token。

---

## Block: {Block 类型}

```
生成一个 Flutter (Dart) 的 {Block 类型名称} 组件。

**框架约定**：
- Flutter 3.22+
- Material 3 主题
- Dart 3.4+
- 使用 StatelessWidget / StatefulWidget
- 状态管理: Provider / Riverpod（根据项目）
- 图标: flutter_svg (SVG) 或 Material Icons

**全局约束**：
- 配色: 将 DESIGN.md CSS 变量映射为 Material ColorScheme
- 字体: Google Fonts 匹配 Design Brief 选定字体
- 暗色模式: ThemeData.dark() 对应 [data-theme="dark"]
- 品牌人格: 对应 Material 3 的 style strategy

**排版约束**：
- ALL CAPS 元素 letterSpacing ≥ 0.08em
- Display 文字 (≥48px) letterSpacing: -0.02em
- Body 文字 height 属性 ≥ 1.5
- 恰好 3 个 fontWeight (w400 / w500 / w600)

**动效**：
- {动效描述，来自视觉论文 motion-direction}
- 使用 AnimatedContainer / AnimatedOpacity / AnimationController
- respectsReduceMotion: true

**禁止**：见 react-tailwind.md 全局禁止列表（7 反 AI 规则全相同）
```

---

## 核心组件模板

### Material ColorScheme 映射

```dart
final colorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF{primary-hex}),          // var(--color-primary)
  onPrimary: Colors.white,
  surface: Color(0xFF{surface-hex}),          // var(--color-surface)
  onSurface: Color(0xFF{text-hex}),           // var(--color-text)
  error: Color(0xFF{error-hex}),              // var(--color-error)
  outline: Color(0xFF{border-hex}),           // var(--color-border)
);
```

### 按钮 (Flutter)

```
生成 Flutter 按钮组件：
- 类型: ElevatedButton / OutlinedButton / TextButton
- 圆角: BorderRadius.circular(8)
- elevation: 0（扁平设计）
- padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8)
- textStyle: fontWeight w600, letterSpacing 0.02em
- 动效: onPressed → transform scale(0.98)
- 禁止: elevation > 2
```

### 卡片 (Flutter)

```
生成 Flutter 卡片组件：
- 背景: ColorScheme.surface
- 边框: Border.all(color: ColorScheme.outline, width: 1)
- 圆角: 8px
- 禁止: elevation (使用 border 而非阴影)
- 禁止: 圆角 + 彩色左边框组合
```
```

- [ ] **Step 6: Commit**

```bash
git add projects/super-frontend-design/templates/prompt-templates/
git commit -m "feat: add 5 framework prompt templates (React/Vue/RN/HTML/Flutter)"
```

---

### Task 13: P8 — Create `references/brand-personality-expanded.md`

**Files:**
- Create: `projects/super-frontend-design/references/brand-personality-expanded.md`

- [ ] **Step 1: Write the expanded brand personality reference**

Create `projects/super-frontend-design/references/brand-personality-expanded.md`:

```markdown
# 品牌人格扩展（8 → 14）

> v2.0 将品牌人格从 8 种扩展到 14 种，覆盖更多行业和应用场景。
> 每种人格包含完整的设计映射：颜色偏好、字体倾向、动效选择、组件风格。

---

## 核心品牌人格 (6)

### 1. 极客工程师
| 维度 | 映射 |
|------|------|
| 颜色 | 深色系基底 + 单色 accent（青色 / 绿色），暗色模式首选 |
| 字体 | Display: Geist Mono / JetBrains Mono；Body: Geist Sans |
| 圆角 | 2-4 px（极简） |
| 动效 | 终端打字、渐进揭示、ASCII Art 过渡 |
| 组件 | 代码块、数据表格、终端式搜索 |
| 禁止 | 过度装饰、emoji、圆角 > 4px |

### 2. 优雅艺术家
| 维度 | 映射 |
|------|------|
| 颜色 | 极简 monochrome + 1 种 accent，大量留白 |
| 字体 | Display: Playfair Display / Cormorant Garamond；Body: Inter |
| 圆角 | 0 px（完全直角） |
| 动效 | 极简 — 仅 opacity 过渡，或 3D 沉浸式 |
| 组件 | 大幅排版、全幅图片、Asymmetric Grid |
| 禁止 | 任何视觉杂乱、多余的 divider / border |

### 3. 活力创业者
| 维度 | 映射 |
|------|------|
| 颜色 | Gradient 驱动（单色渐变，非两色），高活力色 |
| 字体 | Display: Switzer / Cabinet Grotesk；Body: Switzer |
| 圆角 | 12-16 px（大胆圆角） |
| 动效 | 弹性动效、磁吸按钮、弹性弹簧 |
| 组件 | Bento Grid、Social Proof、Animated Counter |
| 禁止 | 过于沉稳的灰色、对称布局 |

### 4. 权威专家
| 维度 | 映射 |
|------|------|
| 颜色 | 深蓝 + 灰调，稳重专业 |
| 字体 | Display: DM Serif Display / Newsreader；Body: Source Serif |
| 圆角 | 0-4 px |
| 动效 | 无动效或极简 |
| 组件 | 大量文字内容、引用、数据图表 |
| 禁止 | 活泼配色、弹性动画、emoji |

### 5. 温暖朋友
| 维度 | 映射 |
|------|------|
| 颜色 | 暖色调（蜜色、奶油、焦糖），柔和 accent |
| 字体 | Display: Sniglet / Quicksand；Body: Nunito |
| 圆角 | 16-24 px（最大圆角） |
| 动效 | 弹性、柔和的 spring 动效 |
| 组件 | 插画、圆角头像、温暖色调卡片 |
| 禁止 | 锐利边角、冷色调、硬阴影 |

### 6. 叛逆先锋
| 维度 | 映射 |
|------|------|
| 颜色 | 高对比度黑白 + 弹出 neon accent |
| 字体 | Display: Bebas Neue / Anton；Body: Space Grotesk |
| 圆角 | 混合（部分 0，部分 24） |
| 动效 | Morphing、Glitch、Split Text |
| 组件 | 大幅排版、不对称、Brutalist |
| 禁止 | 对称布局、温和色、圆形 |

---

## 扩展品牌人格 (8)

### 7. 极简主义者
| 维度 | 映射 |
|------|------|
| 颜色 | 单色 + 功能 accent，无渐变 |
| 字体 | Display: Inter；Body: Inter（单字体多 weight） |
| 圆角 | 4 px |
| 动效 | 仅 hover 过渡，无页面动效 |
| 组件 | 网格、列表、直线 |
| 禁止 | 装饰性元素、多于 2 种颜色 |

### 8. 创意总监
| 维度 | 映射 |
|------|------|
| 颜色 | 大胆色彩碰撞、非传统配色 |
| 字体 | Display: Clash Display / Fraunces；Body: Satoshi |
| 圆角 | 12-32 px（超大圆角） |
| 动效 | Morphing、Scroll-driven、Parallax |
| 组件 | Split Screen、Masonry、Text Overlap |
| 禁止 | 传统布局、保守色 |

### 9. 数据驱动
| 维度 | 映射 |
|------|------|
| 颜色 | 冷色数据色板（蓝/绿/灰），强调准确 |
| 字体 | Display: Inter / SF Pro Display；Body: Inter；Mono: JetBrains Mono |
| 圆角 | 2-4 px |
| 动效 | 数字步进计数、图表渐进绘制 |
| 组件 | 数据表格、KPI Cards、Chart Grid |
| 禁止 | 装饰性动效、过于鲜艳的颜色 |

### 10. 奢华高端
| 维度 | 映射 |
|------|------|
| 颜色 | 黑+金 / 黑+白，高对比度 |
| 字体 | Display: Cormorant Garamond / Playfair Display；Body: Lora |
| 圆角 | 0 px |
| 动效 | Parallax 层叠、reveal 动画 |
| 组件 | 大幅 Hero 图片、Serif 标题、金色 accent |
| 禁止 | 圆角、鲜艳色、密集布局 |

### 11. 环保自然
| 维度 | 映射 |
|------|------|
| 颜色 | 大地色调（绿/棕/米色），自然柔和 |
| 字体 | Display: Fraunces / Newsreader；Body: Lora |
| 圆角 | 8-12 px |
| 动效 | 渐变 + 柔和过渡，具象背景 |
| 组件 | 自然图片、有机形状的卡片、可持续指标 |
| 禁止 | 科技感元素、荧光色 |

### 12. 游戏品牌
| 维度 | 映射 |
|------|------|
| 颜色 | 黑+紫+霓虹，深色沉浸 |
| 字体 | Display: Orbitron / Audiowide；Body: Inter |
| 圆角 | 4-8 px |
| 动效 | 粒子系统、Shaders、Glow 效果 |
| 组件 | Full-screen Hero、Video Background、排行榜 |
| 禁止 | 过于商务的色调、Serif 字体 |

### 13. 教育品牌
| 维度 | 映射 |
|------|------|
| 颜色 | 明亮安全色（蓝/橙/绿），可访问性优先 |
| 字体 | Display: Lexend / Atkinson Hyperlegible；Body: Lexend |
| 圆角 | 12-16 px |
| 动效 | 进度条、达成徽章、鼓励性动效 |
| 组件 | 进度指示器、课程卡片、学习路径 |
| 禁止 | 过于复杂的布局、小字体 |

### 14. 金融科技
| 维度 | 映射 |
|------|------|
| 颜色 | 深蓝+深绿+谨慎 accent，可靠感 |
| 字体 | Display: DM Sans / Inter；Body: DM Sans；Mono: JetBrains Mono |
| 圆角 | 4-8 px |
| 动效 | 无动效或数字滚动 |
| 组件 | 数据表格、金额格式化、交易卡片 |
| 禁止 | 过度动效、非标准金额格式 |

---

## 品牌人格 → 设计关键词速查

| 人格 | 关键词 | Accent 策略 | Mono 需求 |
|------|--------|:---:|:---:|
| 极客工程师 | 终端、代码、暗色 | 单色青色 | ✅ 需要 |
| 优雅艺术家 | 留白、Serif、质感 | 金属/黑 | ❌ |
| 活力创业者 | 渐变、弹性、大胆 | 渐变主色 | ❌ |
| 权威专家 | 稳重、Serif、数据 | 深蓝 | 🟡 可选 |
| 温暖朋友 | 暖色调、圆角、插画 | 柔和橙/粉 | ❌ |
| 叛逆先锋 | 黑白、不对称、大字体 | 霓虹 | ❌ |
| 极简主义者 | 单色、网格、无装饰 | 最小 accent | ❌ |
| 创意总监 | 碰撞色、非传统、大胆 | 实验性 | ❌ |
| 数据驱动 | 图表、KPI、冷色 | 蓝/绿 | ✅ 需要 |
| 奢华高端 | Serif、黑白金、戏剧性 | 金色 | ❌ |
| 环保自然 | 大地色、有机形、柔和 | 绿色 | ❌ |
| 游戏品牌 | 霓虹、深色、沉浸 | 紫/霓虹 | ❌ |
| 教育品牌 | 可访问、明亮、安全 | 蓝/橙 | ❌ |
| 金融科技 | 深蓝、可靠、数字准确 | 蓝/绿深色 | ✅ 需要 |
```

- [ ] **Step 2: Commit**

```bash
git add projects/super-frontend-design/references/brand-personality-expanded.md
git commit -m "feat: expand brand personalities from 8 to 14 types"
```

---

## Self-Review

### Correctness
- [ ] All 8 phases have tasks specified (P1–P8)
- [ ] All 16 files listed in File Structure Map have corresponding tasks
- [ ] No SKILL.md YAML invalid — all markdown within spec
- [ ] All CSS variable references use `var(--color-*)` notation
- [ ] All hex values in anti-ai-slop.md match actual Tailwind defaults

### Completeness
- [ ] 11 new files to create (references + templates)
- [ ] 5 existing files to modify (SKILL.md + subskills)
- [ ] 1 version bump (v1.8.0 → v2.0.0) specified
- [ ] All 5 prompt template frameworks covered (React/Vue/RN/HTML/Flutter)
- [ ] MCP integration guide covers 4 servers
- [ ] Brand personality expanded from 8 to 14

### Safety
- [ ] No placeholder/unsafe CSS values
- [ ] No hardcoded credentials in MCP integration guide
- [ ] All external references documented as URLs
- [ ] `prefers-reduced-motion` covered in all templates

### Ambiguity
- [ ] No ambiguous instructions — each Step has exact content to write
- [ ] No "or similar" without concrete fallback
- [ ] All `{...}` template variables have documented data sources

---

## Execution Options

### Option A: Subagent-driven (recommended for speed)
Use `superpowers:subagent-driven-development` skill. The plan's 8 phases are 80% independent — P1 (anti-slop), P2 (DESIGN.md), P3 (typography), P4 (blocks), P5 (creative), P6 (MCP), P7 (prompts), P8 (brand) can run in parallel batches of 3-4 agents.

### Option B: Inline execution
Execute each Task sequentially in the current session. Slower but provides step-by-step visibility.

### Option C: Mixed
Run P1–P4 in parallel via sub-agents, then P5–P8 inline for fine-tuning.

---

**Plan status:** ✅ Complete — Ready for execution
**Next step:** User selects execution option → begin implementation
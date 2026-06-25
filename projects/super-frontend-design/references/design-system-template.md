# DESIGN.md 模板 — 9-Section Design System

> 格式遵循 Open Design `DESIGN.md` 约定，可被 Agent / Linter / Renderer 消费
> 所有 CSS 变量必须在 `:root {}` 块内

---

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

<!-- 从 research 第 4 轮对话的"品牌人格 + 情绪板"自动填充 -->

```markdown
**品牌人格**：{极客工程师 / 优雅艺术家 / 活力创业者 / 权威专家 / 温暖朋友 / 叛逆先锋 / 极简主义者 / 创意总监 / 数据驱动 / 奢华高端 / 环保自然 / 游戏品牌 / 教育品牌 / 金融科技}

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
  --color-background: #XXXXXX;
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
  --color-background: #XXXXXX;
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

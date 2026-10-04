# 纯 HTML/CSS Prompt 模板

> 零依赖、单文件输出，优先使用纯 CSS 原生特性。
> 所有 CSS 变量定义在 `:root {}`，暗色模式用 `[data-theme="dark"]`。
> **v2.4.0 规范**: 严格遵循 references/premium-design-rules.md 的16条规则（含斜体标题禁令/侧边条纹禁令/LCP优化/间距4px纪律）、hallmark 21种Macrostructure路由、hallmark 57条Slop Test检查、GSAP 动效最佳实践（纯 CSS 动效优先，复杂动效用 GSAP）。
> 参考: references/css-modern-features.md（CSS 2025-2026 现代特性指南）

---

## Block: {Block 类型}

```
生成一个纯 HTML/CSS 的 {Block 类型名称}（单文件，零依赖，纯 CSS 实现）。

**文件结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{页面标题}</title>
  <style>
    :root { /* DESIGN.md 的所有变量 + clamp() 流式字号 */ }
    [data-theme="dark"] { /* 暗色覆盖 */ }
    /* 组件样式 — 禁止裸 hex 值，使用 CSS 嵌套 */
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
- 使用 text-wrap: balance/pretty 优化文字排版

**CSS 现代特性优先**（参考 css-modern-features.md）：
- ✅ clamp() 流式排版（字号/间距）
- ✅ Scroll-driven Animations（滚动触发动画，无需 JS）
- ✅ Container Queries（容器查询组件化响应式）
- ✅ :has() 父选择器
- ✅ color-mix() 动态颜色混合
- ✅ backdrop-filter 毛玻璃效果
- ✅ aspect-ratio 宽高比控制
- ✅ light-dark() 自动暗色模式
- ✅ 原生 CSS 嵌套
- ✅ @keyframes + CSS transitions
- ⚠️ Motion JS (`motion`) 仅在复杂交互时可选使用（非必需）

**全局约束**：
- 配色: 主色 var(--color-primary) = {hex}，背景 var(--color-bg) = {hex}，表面 var(--color-surface) = {hex}
- 字体: 标题 var(--font-display)，正文 var(--font-body)，等宽 var(--font-mono)
- 暗色模式: {是/否}·{是时使用 [data-theme="dark"] 覆盖}
- 品牌人格: {品牌人格类型} → {对应的设计特征}

**排版约束**：
- 使用 clamp() 流式字号（参考 css-modern-features.md §1）：
  ```css
  --font-size-display: clamp(2.5rem, 7vw, 5.5rem);
  --font-size-h1: clamp(2rem, 5vw, 3.5rem);
  --font-size-h2: clamp(1.5rem, 4vw, 2.5rem);
  --font-size-h3: clamp(1.25rem, 2.5vw, 1.875rem);
  --font-size-body: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  ```
- 间距也用 clamp(): padding: clamp(3rem, 8vw, 8rem)
- Display/H1 字重: 400 (Regular) 或 500 (Medium)
- H2/H3 字重: 500 (Medium) 或 600 (Semibold)
- Display/H1 (>2.5rem): letter-spacing: -0.02em 到 -0.04em（负tracking）
- H2: letter-spacing: -0.01em
- ALL CAPS 元素: letter-spacing: 0.06em 到 0.1em
- Body 文字行高: 1.6-1.75
- Body copy max-width: 65ch
- 标题: text-wrap: balance; 正文: text-wrap: pretty;
- 恰好 3 个 font-weight (400 / 500 / 600)

**动效**（纯 CSS 优先）：
- {动效描述，来自视觉论文 motion-direction}
- 优先使用 CSS Scroll-driven Animations（animation-timeline: view()）
- 使用 @keyframes + cubic-bezier 缓动
- 使用 CSS transitions 做微交互
- Hover微交互: 150ms, cubic-bezier(0.4, 0, 0.2, 1)
- 过渡动画: 200-300ms
- 入场动画: 400-600ms
- Stagger子元素延迟: 40-80ms
- 离场动画: 200ms, cubic-bezier(0.4, 0, 1, 1)
- 按钮点击: transform: scale(0.97)（active态）
- 卡片hover: transform: translateY(-2px)
- 优先动画 transform 和 opacity（GPU加速）
- 必须支持 prefers-reduced-motion
- @supports (animation-timeline: view()) 优雅降级

**禁止**：
- ❌ Framer Motion 包（纯 CSS 优先，Motion JS 仅复杂场景可选）
- ❌ hex #6366f1 #4f46e5 #4338ca #8b5cf6 #7c3aed
- ❌ AI 经典两色/三色渐变 (purple→blue / blue→cyan / indigo→pink / 蓝→紫→粉)
- ❌ emoji 图标 (✨🚀🎯⚡🔥💡🎨🛠️)
- ❌ 圆角卡片 + 彩色左边框组合
- ❌ 假指标 ("10× faster")
- ❌ 填充文案 (lorem ipsum)
- ❌ 外部占位图片 CDN
- ❌ >12 个裸 hex 值在 :root 之外
- ❌ var(--accent) 在同一屏幕超过 2 次
- ❌ 装饰性 blob/wave SVG 背景
- ❌ 完美对称布局
- ❌ 大标题(H1/Display)使用 font-weight: 700 (Bold) 或更重
- ❌ 全篇使用 font-weight: 900 (Black) 或 800 (Extra Bold)
- ❌ 所有 section 统一使用 padding: 3rem (py-12) 或 4rem（使用 clamp(3rem, 8vw, 8rem)）
- ❌ 直接使用默认厚重 box-shadow（使用自定义柔和多层阴影）
- ❌ 动画时长超过 600ms
- ❌ 对 color/background-color 做动画（用 opacity 或 transform 替代）
- ❌ 无兜底地只写 CSS scroll-driven 动画：`animation-timeline` 目前非 Baseline（MDN 标 Limited availability），必须 `@supports (animation-timeline: view())` 命中才用，未命中时用 IntersectionObserver/rAF 驱动同等效果，禁止让入场动画直接消失
- ❌ 在未做 @supports 判定前，用裸 scroll 事件监听替代滚动动画（有性能问题；但作为降级路径是**允许且必须**的）
- ❌ 外部 CSS 文件（全部内联在 `<style>`）
- ❌ 外部字体 CDN（使用系统字体回退或 base64 嵌入）
- ❌ JavaScript 框架引用（纯原生 JS 仅在必要时使用，且内联）
- ❌ 不完整的 HTML 结构（必须有 doctype + head + body）
- ❌ 互补色渐变（蓝→橙/红→绿）
- ❌ 给正文文字加渐变
- ❌ 超过 3 个色标的渐变

**参考**：
- Design Brief: output/design-system.md
- Premium Rules: references/premium-design-rules.md
- CSS Modern Features: references/css-modern-features.md
```

---

## 核心组件模板

### 按钮 (纯 HTML/CSS)

```html
<button class="btn-primary" type="button">
  按钮文字
</button>

<style>
.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px; /* rounded-lg */
  padding: 10px 24px;
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--font-size-body);
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1),
              background 150ms ease;
}
.btn-primary:hover {
  background: color-mix(in srgb, var(--color-primary) 85%, black);
  transform: translateY(-1px) scale(1.02);
}
.btn-primary:active {
  transform: translateY(1px) scale(0.97);
}
.btn-primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
</style>
```

### 卡片 (纯 HTML/CSS)

```html
<article class="card">
  <h3 class="card-title">卡片标题</h3>
  <p class="card-body">卡片内容...</p>
</article>

<style>
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px; /* rounded-xl */
  padding: 24px;
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 200ms ease,
              border-color 200ms ease;
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
.card:hover {
  border-color: color-mix(in srgb, var(--color-primary) 30%, var(--color-border));
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -2px rgb(0 0 0 / 0.05),
              0 10px 20px -5px rgb(0 0 0 / 0.08);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(32px); }
  to { opacity: 1; transform: translateY(0); }
}

.card-title {
  font-size: var(--font-size-h3);
  font-weight: 500;
  letter-spacing: -0.01em;
  margin: 0 0 12px 0;
}
.card-body {
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}
</style>
```

### 表单 (纯 HTML/CSS)

```html
<form class="form">
  <div class="form-group">
    <label class="form-label" for="name">姓名</label>
    <input class="form-input" type="text" id="name" required>
  </div>

  <div class="form-group">
    <label class="form-label" for="email">邮箱</label>
    <input class="form-input" type="email" id="email" required>
  </div>

  <button class="btn-primary" type="submit">提交</button>
</form>

<style>
.form-group {
  margin-bottom: 20px;
}
.form-label {
  display: block;
  font-size: var(--font-size-caption);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}
.form-input {
  width: 100%;
  height: 40px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px; /* rounded-lg */
  padding: 8px 16px;
  font-family: var(--font-body);
  font-size: var(--font-size-body);
  box-sizing: border-box;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}
.form-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--color-primary) 20%, transparent);
}
.form-group:has(.error-message) .form-input {
  border-color: var(--color-error);
}
.error-message {
  color: var(--color-error);
  font-size: var(--font-size-caption);
  margin-top: 4px;
}
</style>
```

### Section 布局模板（Scroll-driven 动画）

```html
<section class="section" data-section-id="features">
  <div class="container">
    <h2 class="section-title">大标题</h2>
    <p class="section-subtitle">副标题描述</p>
    <div class="section-content">
      <!-- 内容 -->
    </div>
  </div>
</section>

<style>
.section {
  padding-top: clamp(6rem, 12vw, 10rem);
  padding-bottom: clamp(6rem, 12vw, 10rem);
}
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding-left: clamp(1.5rem, 4vw, 2rem);
  padding-right: clamp(1.5rem, 4vw, 2rem);
}
.section-title {
  font-size: var(--font-size-h2);
  font-weight: 500;
  letter-spacing: -0.02em;
  text-wrap: balance;
  max-width: 42rem;
  margin: 0 0 16px 0;
}
.section-subtitle {
  font-size: var(--font-size-body-lg);
  color: var(--color-text-secondary);
  line-height: 1.6;
  max-width: 36rem;
  text-wrap: pretty;
  margin: 0 0 48px 0;
}
</style>
```

### 响应式与无障碍

```css
/* 暗色模式自动切换（可选） */
:root {
  color-scheme: light dark;
  --color-bg: light-dark(#FFFFFF, #0A0A0A);
  --color-text: light-dark(#0A0A0A, #FAFAFA);
}

/* 减少动效模式 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Scroll-driven 动画降级 */
@supports not (animation-timeline: view()) {
  .fade-up {
    animation: fade-up 0.6s cubic-bezier(0.4, 0, 0.2, 1) both;
  }
}
</style>
```

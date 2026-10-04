# CSS 2025-2026 现代特性指南

> 优先使用这些原生CSS特性，减少JS依赖，提升性能和视觉质量。

---

## 1. 流式排版 clamp()

### 用途
一行代码实现响应式字号，不需要媒体查询断点。

### 代码模板
```css
/* 语法: clamp(最小值, 首选值(视口单位), 最大值) */
h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
}

/* 推荐字号阶 */
:root {
  --fs-display: clamp(2.5rem, 7vw, 5.5rem);
  --fs-h1: clamp(2rem, 5vw, 3.5rem);
  --fs-h2: clamp(1.5rem, 4vw, 2.5rem);
  --fs-h3: clamp(1.25rem, 2.5vw, 1.875rem);
  --fs-body: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
}
```

### 间距也可以用clamp
```css
.section {
  padding-top: clamp(3rem, 8vw, 8rem);
  padding-bottom: clamp(3rem, 8vw, 8rem);
}
```

---

## 2. Scroll-driven Animations（滚动驱动动画）

### 用途
不用JS监听scroll事件，纯CSS实现滚动触发动画和视差效果。浏览器支持: Chrome/Edge/Safari 17.4+。

### 元素进入视口时淡入上移
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-up {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 60%;
}
```

### 滚动进度条
```css
@keyframes grow-bar {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-primary);
  transform-origin: left;
  animation: grow-bar linear;
  animation-timeline: scroll(root);
  z-index: 100;
}
```

### 视差背景
```css
@keyframes parallax-slow {
  from { transform: translateY(0); }
  to { transform: translateY(-100px); }
}

.hero-bg {
  animation: parallax-slow linear;
  animation-timeline: scroll(root);
  animation-range: 0 60vh;
}
```

### 图片reveal效果
```css
@keyframes reveal {
  from { clip-path: inset(0 100% 0 0); }
  to { clip-path: inset(0 0 0 0); }
}

.img-reveal {
  animation: reveal 1s cubic-bezier(0.77, 0, 0.175, 1) both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
```

### 注意事项
- 降级: 使用 `@supports (animation-timeline: view())` 包裹
- 不支持的浏览器: 元素默认显示，无动画（优雅降级）
- Motion库(如Motion/react)有useScroll钩子作为JS备选

---

## 3. Container Queries（容器查询）

### 用途
响应式基于组件容器宽度而非视口宽度，真正的组件化响应式。

### 代码模板
```css
/* 定义容器 */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* 基于容器宽度的样式 */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 1.5rem;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }
  .card-image {
    width: 100%;
    aspect-ratio: 16/9;
  }
}
```

### 使用场景
- Bento Grid中不同大小卡片内的布局适配
- 组件在侧边栏(窄)和主内容区(宽)中自动调整
- 列表在不同容器中自动切换grid/flex布局

---

## 4. :has() 选择器（父选择器）

### 用途
根据子元素状态设置父元素样式，实现复杂交互而无需JS。

### 代码模板
```css
/* 表单输入有错误时，整个form group变红 */
.form-group:has(.error-message) {
  border-color: #ef4444;
}

/* 卡片包含图片时调整内边距 */
.card:has(img) {
  padding: 0;
}
.card:has(img) .card-content {
  padding: 1.5rem;
}

/* 导航栏有打开的下拉菜单时增加背景模糊 */
nav:has([aria-expanded="true"]) {
  backdrop-filter: blur(12px);
  background: rgb(255 255 255 / 0.8);
}

/* 图片加载失败时显示占位 */
img:has(+ .img-fallback) {
  display: none;
}
```

---

## 5. text-wrap 文字排版控制

### 用途
自动平衡标题文字换行，避免孤字/孤行。

### 代码模板
```css
/* 标题文字平衡换行，避免一行只有1-2个字 */
h1, h2, h3 {
  text-wrap: balance;
}

/* 正文段落漂亮排版（控制孤行） */
p {
  text-wrap: pretty;
}
```

### 效果对比
- `balance`: 标题两侧文字长度尽量均等
- `pretty`: 段落最后一行至少有2个词，避免孤字
- 浏览器支持: Chrome 114+, Safari 17.4+, Firefox 124+

---

## 6. color-mix() 动态颜色混合

### 用途
在CSS中动态混合颜色，不需要预定义大量色阶。

### 代码模板
```css
.btn-primary {
  background: var(--color-primary);
}
.btn-primary:hover {
  background: color-mix(in srgb, var(--color-primary) 85%, black);
}
.btn-primary:active {
  background: color-mix(in srgb, var(--color-primary) 70%, black);
}

/* 生成同色系变体 */
--color-primary-light: color-mix(in srgb, var(--color-primary) 20%, white);
--color-primary-dark: color-mix(in srgb, var(--color-primary) 80%, black);
--color-primary-glass: color-mix(in srgb, var(--color-primary) 8%, transparent);
```

---

## 7. @property 注册自定义属性

### 用途
让CSS自定义属性支持渐变动画和类型检查。

### 代码模板
```css
@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@keyframes rotate-gradient {
  to { --angle: 360deg; }
}

.gradient-border {
  background: conic-gradient(from var(--angle), #0ea5e9, #8b5cf6, #0ea5e9);
  animation: rotate-gradient 3s linear infinite;
}
```

---

## 8. backdrop-filter 毛玻璃/磨砂效果

### 用途
高级感必备——模糊背景的元素叠加效果。

### 代码模板
```css
/* 毛玻璃导航栏 */
nav {
  background: rgb(255 255 255 / 0.7);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border-bottom: 1px solid rgb(255 255 255 / 0.2);
}

/* 暗色毛玻璃 */
.modal-backdrop {
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(8px);
}

/* Fluted Glass（竖条纹玻璃 - 2026新效果） */
.fluted-glass {
  background: linear-gradient(
    90deg,
    rgb(255 255 255 / 0.1) 0px,
    rgb(255 255 255 / 0.3) 1px,
    transparent 1px,
    transparent 4px
  );
  background-size: 4px 100%;
  backdrop-filter: blur(12px);
}
```

### 性能提示
- `backdrop-filter` 需要GPU合成，避免大面积使用
- 给元素加上 `will-change: backdrop-filter` 或 `transform: translateZ(0)` 提升性能
- 降级: `@supports (backdrop-filter: blur(1px))` 包裹

---

## 9. aspect-ratio 宽高比

### 用途
不需要padding hack就能控制元素宽高比。

### 代码模板
```css
.video-frame { aspect-ratio: 16/9; }
.avatar { aspect-ratio: 1/1; border-radius: 50%; }
.card-image { aspect-ratio: 4/3; object-fit: cover; }
.phone-mockup { aspect-ratio: 9/19.5; }
```

---

## 10. light-dark() 自动暗色模式

### 用途
一行代码实现暗色/亮色自动切换，不需要重复写dark:前缀。

### 代码模板
```css
:root {
  color-scheme: light dark;
  --color-bg: light-dark(#FFFFFF, #0A0A0A);
  --color-text: light-dark(#0A0A0A, #FAFAFA);
  --color-border: light-dark(#E4E4E7, #27272A);
}

@media (prefers-color-scheme: dark) {
  :root {
    /* 仅在需要额外暗色调整时使用 */
  }
}
```

---

## 11. prefers-reduced-motion 无障碍动画

### 用途
尊重用户系统设置，对开启"减少动态效果"的用户禁用非必要动画。

### 代码模板
```css
/* 默认动画 */
.fade-up {
  animation: fade-up 0.5s ease-out both;
}

/* 用户开启"减少动效"时: 禁用装饰性动画 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  /* 保留必要的过渡动画（如菜单展开） */
  .menu {
    transition: opacity 0.15ms;
  }
}
```

---

## 12. CSS嵌套（原生）

### 用途
不需要Sass/Less，原生CSS支持嵌套，代码更简洁。

### 代码模板
```css
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  transition: box-shadow 0.2s, transform 0.2s;

  &:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
  }

  & .card-title {
    font-size: var(--fs-h3);
    font-weight: 600;
    margin-bottom: var(--spacing-2);
  }

  & .card-content {
    color: var(--color-text-secondary);
  }
}
```

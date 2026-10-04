# Vue 3 + Nuxt + Tailwind CSS Prompt 模板

> 在生成组件设计卡时使用以下模板格式。
> `{...}` 为从 DESIGN.md 和视觉论文中动态填充的变量。
> **v2.4.0 规范**: 严格遵循 references/premium-design-rules.md 的16条规则（含斜体标题禁令/侧边条纹禁令/LCP优化/间距4px纪律）、hallmark 21种Macrostructure路由、hallmark 56条Slop Test检查、GSAP 动效最佳实践（Vue 3 中推荐 useGSAP hook）。
> 参考: references/css-modern-features.md（CSS现代特性指南）

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
- Motion (`motion/vue`) — 动画库，替代 Framer Motion
  - import { motion } from "motion/vue"

**全局约束**：
- 配色: 主色 var(--color-primary) = {hex}，背景 var(--color-bg) = {hex}，表面 var(--color-surface) = {hex}
- 字体: 标题 var(--font-display)，正文 var(--font-body)，等宽 var(--font-mono)
- 暗色模式: {是/否}·{是时使用 [data-theme="dark"] 覆盖}
- 品牌人格: {品牌人格类型} → {对应的设计特征}

**排版约束**：
- 使用 clamp() 流式字号（参考 css-modern-features.md §1）：
  - Display: clamp(2.5rem, 7vw, 5.5rem)
  - H1: clamp(2rem, 5vw, 3.5rem)
  - H2: clamp(1.5rem, 4vw, 2.5rem)
  - H3: clamp(1.25rem, 2.5vw, 1.875rem)
- Display/H1 字重: 400 (Regular) 或 500 (Medium)
- H2/H3 字重: 500 (Medium) 或 600 (Semibold)
- Display/H1 (>2.5rem): letter-spacing: -0.02em 到 -0.04em（负tracking）
- H2: letter-spacing: -0.01em
- ALL CAPS 元素: letter-spacing ≥ 0.08em
- Body 文字行高 ≥ 1.5-1.75
- Body copy max-width: 65ch
- 恰好 3 个 font-weight (400 / 500 / 600)

**动效**：
- {动效描述，来自视觉论文 motion-direction}
- 使用 Motion (`motion/vue`) spring 物理动画：
  - 按钮点击: whileTap={{ scale: 0.97 }} transition={{ type: "spring", stiffness: 400, damping: 25 }}
  - 卡片入场: initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ type: "spring", stiffness: 200, damping: 25 }}
  - 模态框: initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ type: "spring", stiffness: 300, damping: 25 }}
- Hover微交互: 150ms, cubic-bezier(0.4, 0, 0.2, 1)
- 过渡动画: 200-300ms, spring(stiffness: 300, damping: 30)
- 入场动画: 400-600ms, spring(stiffness: 200, damping: 25)
- 优先动画 transform 和 opacity（GPU加速）
- prefers-reduced-motion 必须禁用动效

**禁止**：
- ❌ framer-motion 包（使用 motion/vue 替代）
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
- ❌ 大标题(H1/Display)使用 font-bold (700) 或更重
- ❌ 全篇使用 font-black (900) 或 font-extrabold (800)
- ❌ 所有 section 统一使用 py-12 或 py-16（使用 py-24 md:py-32）
- ❌ 直接使用 Tailwind 默认 shadow-md/shadow-lg（使用自定义柔和阴影）
- ❌ 动画时长超过 600ms
- ❌ 对 color/background-color 做动画（用 opacity 或 transform 替代）
- ❌ 在未判定 `@supports (animation-timeline: view())` 的情况下只用 CSS scroll-driven 做滚动动画（该属性尚未 Baseline）；降级路径允许并要求使用 Motion `useScroll` 或 IntersectionObserver
- ❌ 在 `<style scoped>` 中定义 CSS 变量（应在全局 styles 或 nuxt.config 中）
- ❌ 不要使用 Options API
- ❌ 不要使用 `v-for` key 为 index

**参考**：
- Design Brief: output/design-system.md
- Premium Rules: references/premium-design-rules.md
- CSS Modern Features: references/css-modern-features.md
- 参考源: Inspira UI · Aceternity UI · 21st.dev

**示例结构**：
```vue
<script setup lang="ts">
import { ref } from 'vue'
import { motion } from 'motion/vue'

interface Props {
  title: string
  items: Item[]
}

const props = defineProps<Props>()
const active = ref<string | null>(null)
</script>

<template>
  <section data-section-id="{block-slug}">
    <!-- component content with <motion.div> etc. -->
  </section>
</template>
```
```

---

## 按钮 (Button) Prompt 模板

```
生成 Vue 3 + Tailwind CSS 按钮组件：
- 类型: {primary / secondary / ghost / danger}
- 状态: default, hover, active, focus-visible, disabled
- 圆角: rounded-lg (8px)（禁止 rounded-full 除非是icon-only圆形按钮）
- 动效: 使用 Motion spring 动画
  - hover: translateY(-1px) scale(1.02)
  - active/tap: translateY(1px) scale(0.97)
  - transition: { type: "spring", stiffness: 400, damping: 25 }
- CSS 变量: var(--color-primary) / var(--color-primary-hover)（用 color-mix() 生成hover态）
- focus-visible: outline 2px solid var(--color-primary) + 2px offset
- 字体: var(--font-body), weight 500, letter-spacing 0.02em
- 禁止: 渐变背景、过度阴影、emoji、elevation > 0
```

## 卡片 (Card) Prompt 模板

```
生成 Vue 3 + Tailwind CSS 卡片组件：
- 背景: var(--color-surface)
- 边框: 1px solid var(--color-border)
- 圆角: rounded-xl (12px)
- 间距: padding var(--space-lg) (24px)
- hover: 使用 Motion，轻微 translateY(-2px) + 柔和自定义阴影
- 入场动画: initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
- 禁止: 圆角 + 彩色左边框组合
- 禁止: 毛玻璃背景（除非导航/模态）
- 禁止: 默认 Tailwind shadow-md/shadow-lg
```

## 数据表格 (Data Table) Prompt 模板

```
生成 Vue 3 + Tailwind CSS 数据表格组件：
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
生成 Vue 3 + Tailwind CSS 表单组件：
- 标签: 上置 label，font-size var(--text-small)，color var(--color-text-secondary)
- 输入框: height 40px，border 1px var(--color-border)，border-radius rounded-md (6px) 或 rounded-lg (8px)
- 聚焦态: border-color var(--color-primary) + box-shadow 0 0 0 2px (primary 20% opacity)
- 错误态: border-color var(--color-error)，下方 error message
- 提交按钮: 右对齐 primary button
- 禁止: 过于夸张的动效、缺少 label、placeholder 作为 label
```

## 导航 (Navigation) Prompt 模板

```
生成 Vue 3 + Tailwind CSS 导航组件：
- 桌面: 左侧 sidebar（{宽度}px），{暗色/亮色}背景
- 导航项: padding var(--space-sm) var(--space-md)，hover var(--color-surface-hover)
- 激活态: 左边框或背景高亮
- 移动端: 汉堡菜单 → 滑出 sidebar
- 图标: 16-20px SVG，stroke="currentColor"
- 毛玻璃: backdrop-filter: blur(12px) saturate(180%)
- 禁止: emoji 图标、过于花哨的动效、多级嵌套（最多 1 层）
```

---

## Inspira UI 组件（Vue 3D 专场）

当创意方向涉及 3D/动画时，参考 Inspira UI (https://inspira-ui.com)：

```
生成一个 Vue 3 + Nuxt 的 {3D 组件}：
- 使用 Three.js + Motion (motion/vue)
- 可参考 Inspira UI 的 {组件名} 组件
- 性能：仅在视窗内渲染（IntersectionObserver）
- 资源：按需加载 Three.js 模块
- 动画库: Motion 或 GSAP（Nuxt 3 用 @vueuse/core + GSAP；SSR 安全写法见 gsap-animation-guide.md）
  - SSR 安全: GSAP 代码必须在 nuxtServerHandler 或 onMounted 中执行
```

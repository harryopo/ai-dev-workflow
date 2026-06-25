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

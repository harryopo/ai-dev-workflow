# React + Tailwind CSS Prompt 模板

> 在生成组件设计卡时使用以下模板格式。
> `{...}` 为从 DESIGN.md 和视觉论文中动态填充的变量。
> **v2.4.0 规范**: 严格遵循 references/premium-design-rules.md 的16条规则（含斜体标题禁令/侧边条纹禁令/LCP优化/间距4px纪律）、hallmark 21种Macrostructure路由、hallmark 57条Slop Test检查、GSAP 动效最佳实践（动效库选择规则/GSAP性能规范）。

---

## Block: {Block 类型}

```
生成一个 React + Tailwind CSS 的 {Block 类型名称} 组件。

**全局约束**：
- 配色: 主色 var(--color-primary) = {hex}，背景 var(--color-bg)，表面 var(--color-surface)
- 字体: 标题 var(--font-display)，正文 var(--font-body)，等宽 var(--font-mono)
- 暗色模式: {是/否}·{是时使用 [data-theme="dark"] 覆盖}
- 品牌人格: {品牌人格类型} → {对应的设计特征}
- 动画库: Motion (motion/react) 或 GSAP（复杂时间轴/滚动驱动/SVG/文字动画时使用 gsap）
- 动效库选择: 简单入场/退出 → Motion；复杂编排/ScrollTrigger/SplitText → GSAP（详见 references/gsap-animation-guide.md）
- **高级感规范**: 必须遵循 premium-design-rules.md: Section间距≥py-24, 大标题font-weight 400-500(不用bold), 使用clamp()流式字号, 多层阴影非Tailwind默认

**排版约束**：
- 字号使用clamp()流式排版: Display clamp(2.5rem,7vw,5.5rem), H1 clamp(2rem,5vw,3.5rem)
- Display/H1字重: 400(normal)或500(medium)，❌禁止font-bold(700)/extrabold/black
- Display/H1负letter-spacing: -0.02em到-0.04em
- ALL CAPS 元素 letter-spacing ≥ 0.08em
- 正文行高 1.6-1.75, Body copy max-width: 65ch
- 标题使用 text-wrap: balance, 正文 text-wrap: pretty

**动效**：
- 使用 Motion (motion/react)，spring物理动画: stiffness 200-400, damping 25-30
- Stagger子元素延迟: 40-80ms
- Hover: 150ms, 入场: 400-600ms, 离场: 200ms
- 按钮hover scale(1.02), tap scale(0.97); 卡片hover translateY(-2px)+shadow-lift
- 滚动动画：`animation-timeline` 尚未 Baseline（MDN: Limited availability），只在 `@supports (animation-timeline: view())` 命中时使用；否则用 IntersectionObserver 或 Motion useScroll 兜底，不得让入场动画在不支持的浏览器里消失
- prefers-reduced-motion 必须禁用装饰性动效

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
- ❌ Framer Motion包（已更名Motion，用motion/react）
- ❌ Tailwind默认shadow-sm/shadow-md/shadow-lg（用自定义多层阴影）
- ❌ h1/h2/display使用font-bold/extrabold/black（字重≤600）
- ❌ Section统一使用py-12/py-16（必须≥py-24）
- ❌ 所有Bento卡片同一尺寸（必须混合2x1/1x2/2x2）
- ❌ GSAP动画库（除非明确需要复杂时间轴/ScrollTrigger/SplitText，否则用Motion）

**参考**：
- Design Brief: output/design-system.md
- 参考源: Aceternity UI · 21st.dev
- 高级感规范: references/premium-design-rules.md
- CSS现代特性: references/css-modern-features.md
- 组件目录: references/component-block-catalog.md
```

---

## 按钮 (Button) Prompt 模板

```
生成 React + Tailwind CSS 按钮组件：
- 类型: {primary / secondary / ghost / danger}
- 状态: default, hover, active, focus-visible, disabled
- 圆角: rounded-lg (8px)（奢华/活力人格可用rounded-xl，极简/权威用rounded-md）
- 动效: Motion whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
- spring过渡: type: "spring", stiffness: 400, damping: 25
- CSS 变量: var(--color-primary) / color-mix(in srgb, var(--color-primary) 85%, black)
- focus-visible: outline 2px solid var(--color-primary) + 2px offset
- 字体: var(--font-body), weight 500(medium), letter-spacing 0.02em
- hover背景: color-mix(in srgb, var(--color-primary) 85%, black)
- 禁止: 蓝紫渐变背景、emoji、rounded-full按钮
```

## 卡片 (Card) Prompt 模板

```
生成 React + Tailwind CSS 卡片组件：
- 背景: var(--color-surface) (#FAFAFA亮色/#171717暗色)
- 边框: 1px solid var(--color-border)
- 圆角: rounded-xl (12px)
- 阴影: 自定义多层阴影(非Tailwind默认): 0 2px 4px -1px rgb(0 0 0 / 0.05), 0 4px 6px -1px rgb(0 0 0 / 0.03)
- hover阴影提升: 0 4px 6px -2px rgb(0 0 0 / 0.05), 0 10px 20px -5px rgb(0 0 0 / 0.08)
- 间距: padding var(--space-6) (24px)
- hover动效: Motion whileHover={{ y: -2 }} transition={{ type: "spring", stiffness: 300, damping: 25 }}
- 禁止: 彩色左边框、毛玻璃(除非明确要求)、rounded-2xl以上圆角
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
- 输入框: height 40px，border 1px var(--color-border)，border-radius rounded-lg(8px)
- 聚焦态: border-color var(--color-primary) + box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-primary) 15%, transparent)
- 错误态: border-color var(--color-error)，下方 error message
- 提交按钮: 右对齐 primary button, Motion whileTap={{ scale: 0.97 }}
- 禁止: 过于夸张的动效、缺少label、placeholder作为label
```

## 导航 (Navigation) Prompt 模板

```
生成 React + Tailwind CSS 导航组件：
- 桌面: 顶部nav，sticky定位，backdrop-filter: blur(12px) saturate(180%)
- 桌面导航项: padding var(--space-sm) var(--space-md)，hover var(--color-surface-hover)
- 激活态: 文字颜色var(--color-primary)或底部指示线
- 移动端: 汉堡菜单 → 滑出菜单
- 图标: 16-20px SVG，stroke="currentColor"
- 滚动时导航: 可选缩小/增加阴影效果
- 禁止: emoji 图标、过于花哨的动效
```

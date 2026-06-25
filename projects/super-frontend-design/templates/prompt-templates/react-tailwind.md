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

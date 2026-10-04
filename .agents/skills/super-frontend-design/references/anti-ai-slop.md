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

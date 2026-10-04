# Custom Theme — 自定义主题生成流程

> 用于处理超出预设 20 种主题的特殊需求场景。
> 当用户指定品牌色、多属性 vibe、或明确要求 custom 主题时使用。

---

## 1. 触发条件

以下情况使用 custom theme 流程：
- 用户指定了品牌色/品牌规范
- 用户明确要求"custom"或"自定义主题"
- 预设主题无法满足用户需求
- 多属性 vibe 要求（如"科技感+温暖+极简"）

---

## 2. 输入要求

从 Design Brief 或用户输入中提取以下信息：

| 信息项 | 来源 | 示例 |
|--------|------|------|
| 品牌主色 | Brand Guidelines / 用户指定 | `#0F172A` |
| 品牌辅助色 | Brand Guidelines / 用户指定 | `#3B82F6` |
| 品牌字体 | Brand Guidelines / 用户指定 | `'Inter', sans-serif` |
| 品牌人格 | Design Brief · 品牌人格 | "极客工程师" |
| 情绪板 | Design Brief · 情绪板 | ["精密", "信任", "创新"] |

---

## 3. 流程步骤

### Step 1: 验证输入完整性

检查是否所有必需信息都已提供：

```markdown
## Custom Theme 输入验证

| 信息项 | 状态 | 值 |
|--------|:---:|------|
| 品牌主色 | ✅/❌ | [颜色值] |
| 品牌辅助色 | ✅/❌ | [颜色值] |
| 品牌字体 | ✅/❌ | [字体族] |
| 品牌人格 | ✅/❌ | [人格类型] |
| 情绪板 | ✅/❌ | [关键词列表] |
```

**如果任何项缺失 → 询问用户补充**

### Step 2: 生成 Design Token 系统

基于输入生成完整的 CSS 变量系统：

```css
:root {
  /* 品牌色彩系统 */
  --color-primary: [品牌主色];
  --color-primary-hover: [主色 darken(8%)];
  --color-primary-active: [主色 darken(12%)];
  --color-secondary: [品牌辅助色];
  --color-secondary-hover: [辅助色 darken(8%)];

  /* 语义色彩 */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* 中性色彩 */
  --color-surface: #FFFFFF;
  --color-surface-elevated: #F8FAFC;
  --color-on-surface: #0F172A;
  --color-border: #E2E8F0;
  --color-muted: #64748B;

  /* 暗色模式 */
  --color-surface-dark: #0F172A;
  --color-surface-elevated-dark: #1E293B;
  --color-on-surface-dark: #F8FAFC;
  --color-border-dark: #334155;

  /* 字体系统 */
  --font-display: [品牌字体];
  --font-body: [品牌字体];
  --font-mono: 'JetBrains Mono', monospace;

  /* 字号系统 */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  --font-size-5xl: 3rem;

  /* 间距系统（4px 基准） */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;

  /* 圆角系统 */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  /* 阴影系统 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Step 3: 验证色彩对比度

使用 WCAG 2.1 标准验证所有色彩组合：

```markdown
## 色彩对比度验证

| 组合 | 前景 | 背景 | 对比度 | WCAG AA | WCAG AAA |
|------|------|------|:---:|:---:|:---:|
| Primary on White | [颜色] | #FFFFFF | X:1 | ✅/❌ | ✅/❌ |
| White on Primary | #FFFFFF | [颜色] | X:1 | ✅/❌ | ✅/❌ |
| Muted on White | [颜色] | #FFFFFF | X:1 | ✅/❌ | ❌ |
```

**如果不满足 WCAG AA → 调整色彩值**

### Step 4: 输出到 DESIGN.md

将生成的 Token 系统写入 `DESIGN.md`：

```markdown
# Design System

## Colors
[CSS 变量代码块]

## Typography
[字体系统代码块]

## Spacing
[间距系统代码块]

## Radius
[圆角系统代码块]

## Shadow
[阴影系统代码块]

## Brand Personality
[品牌人格]

## Mood Board
[情绪板]
```

### Step 5: 验证一致性

检查生成的主题是否与品牌人格一致：

| 检查项 | 标准 | 结果 |
|--------|------|:---:|
| 色彩符合品牌人格 | 见 brand-personality-expanded.md | ✅/⚠️/❌ |
| 对比度满足 WCAG AA | 所有文本组合 ≥ 4.5:1 | ✅/⚠️/❌ |
| 字体符合品牌调性 | 见 typography.md | ✅/⚠️/❌ |
| 间距系统一致 | 使用 4px 基准 | ✅/⚠️/❌ |

---

## 4. 输出文件

生成后的输出：
- `DESIGN.md` - 完整的 Design Token 系统
- `pass-data.yaml` - 包含 `theme` 字段（值为 "custom"）

---

## 5. 示例

### 示例 1: 科技品牌

**输入：**
- 品牌主色: `#0EA5E9`（天空蓝）
- 品牌辅助色: `#6366F1`（靛蓝）
- 品牌字体: `'Inter', sans-serif`
- 品牌人格: "极客工程师"
- 情绪板: ["精密", "创新", "信任"]

**输出：**
- 生成的 Design Token 系统
- 验证对比度 ≥ 4.5:1
- 记录到 DESIGN.md

### 示例 2: 温暖品牌

**输入：**
- 品牌主色: `#D97706`（琥珀）
- 品牌辅助色: `#059669`（翠绿）
- 品牌字体: `'Lora', serif`
- 品牌人格: "温暖包容"
- 情绪板: ["温暖", "自然", "舒适"]

**输出：**
- 生成的 Design Token 系统
- 验证对比度 ≥ 4.5:1
- 记录到 DESIGN.md

---

## 6. 注意事项

- 尊重用户指定的品牌规范
- 如果用户未指定某些属性，从品牌人格推导
- 确保所有色彩组合满足 WCAG AA
- 输出后通知用户主题已生成，可以继续 design 阶段

# DESIGN.md 预设 — shadcn 风格（现代轻量 / 社区主流）

> 内置设计系统预设，格式遵循 `references/design-system-template.md`（9-section）。
> 用途：design-context init 的 DESIGN.md 种子、theme 子技能 Token 参照。
> **预设不是免调研通行证**：中性灰底色只是种子方向，品牌强调色必须经 research → theme
> 从视觉论文推导。技术栈用 shadcn/ui 时与 design Part 8 专章配合阅读。

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

- **品牌人格**：极客工程师（克制、精确、工具感）
- **情绪板**：克制 · 锐利 · 安静
- **设计意图**：界面退后，内容与数据向前；所有视觉决策可解释
- **适合**：开发者工具、SaaS 控制台、文档站、现代内部工具
- **不适合**：需要强烈品牌情绪的营销页（配合 design 工作流另选方向）
- **参考先例**：Linear、Vercel Dashboard、GitHub（见 professional-software.md）

## 2. 配色 (Color)

```css
:root {
  /* 原始层：shadcn/ui OKLCH 中性系（亮色），暗色成对维护 */
  --background: oklch(0.985 0.002 90);       /* 近白暖灰 */
  --foreground: oklch(0.216 0.006 56);       /* 近黑 */
  --muted: oklch(0.967 0.001 88);
  --muted-foreground: oklch(0.553 0.013 58);
  --border: oklch(0.923 0.003 48);
  --primary: oklch(0.216 0.006 56);          /* 主按钮 = 近黑（品牌色经调研注入） */
  --destructive: oklch(0.577 0.245 27.325);
  --ring: oklch(0.709 0.01 56);              /* 焦点环 */

  /* 语义层（暗色在 .dark / @media (prefers-color-scheme) 成对覆盖） */
  --color-canvas: var(--background);
  --color-text: var(--foreground);
  --color-muted: var(--muted-foreground);
  --color-border: var(--border);
  --color-primary: var(--primary);
  --color-danger: var(--destructive);
}
```

- 主按钮默认近黑——品牌色经调研后替换 `--primary`，不塞渐变
- 层级靠**边线与灰阶**，不靠投影；焦点永远有 `--ring` 描边

## 3. 排版 (Typography)

```css
:root {
  /* display 字体禁用 Inter/Roboto（slop 门禁黑名单）——
     从 canvas-fonts/ 选有性格的显示字体配 Geist/系统 sans 做正文 */
  --font-display: "Bricolage Grotesque", var(--font-body);
  --font-body: "Geist", "Segoe UI", "PingFang SC", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --font-size-sm: 13px;
  --font-size-md: 14px;   /* UI 正文基准 */
  --font-size-lg: 16px;
  --font-size-xl: 20px;
  --font-size-2xl: 28px;
}
```

- 工具感来自字重与间距纪律，不来自大字号：标题 20-28px 到顶
- 数据界面大量使用 mono 字体做数字与代码，但 slot 不超过 typography.md §4 上限

## 4. 间距 (Spacing)

```css
:root {
  --space-xs: 4px; --space-sm: 8px; --space-md: 12px;
  --space-lg: 16px; --space-xl: 24px; --space-2xl: 32px;
  --radius-sm: 0.375rem;  /* 6px：输入框/按钮 */
  --radius-md: 0.5rem;    /* 8px：卡片 */
  --radius-lg: 0.75rem;   /* 12px：对话框 */
  --radius-full: 999px;
}
```

- Tailwind 原生 4px 网格；密度中等偏紧（开发者工具习惯）
- 阴影只有一档可选（subtle shadow-sm），优先用 border 分层

## 5. 布局与构图 (Layout & Composition)

- 常见骨架：可折叠侧栏 + 顶栏（含 Command Palette 入口 ⌘K）+ 内容区
- 数据视图优先表格化，但不复制 Ant 风格的灰底表格——行边线代替网格线
- 空态用极简插画或纯文字 + 快捷操作（键盘提示常驻）

## 6. 组件 (Components)

- **复制即拥有**：组件代码在 `components/ui/`，定制直接改源码，不改运行时主题
- **Dialog/Sheet**：退出路径明确（Esc + 点遮罩 + 显式关闭），焦点圈定在对话框内
- **Toast**：sonner 风格堆叠，动作按钮最多一个
- **表单**：Field 布局（标签+输入+描述+错误同组），校验消息与字段一一对应
- **Command Palette**：全站命令入口，支持模糊搜索与最近使用

## 7. 动效与交互 (Motion & Interaction)

- 150-200ms 的透明度/位移微动效；radix 内建动画即够用，不引重动效库
- 焦点环是交互反馈的主体（键盘可见性是一等公民）
- 骨架屏与内容错位最小化：占位尺寸必须等于真实尺寸
- `prefers-reduced-motion` 全局降级

## 8. 语调与品牌 (Voice & Brand)

- 文案直给、技术准确：说「部署失败：端口 3000 已被占用」不说「出错了」
- 快捷键提示常驻（`⌘K`、`⌘S`），界面即文档
- 数据诚实：加载中显示骨架，失败显示重试，永不编造空值

## 9. 禁止模式 (Anti-patterns)

- 禁止 Inter/Roboto 当 display 字体（slop 门禁 V1 会拦）
- 禁止彩色投影、渐变按钮、玻璃拟态堆叠
- 禁止修改 shadcn 组件语义结构换外观（改样式不改结构）
- 禁止把暗色模式做成亮色反转——两套 Token 成对设计
- 禁止无键盘路径的交互（一切可鼠标必可键盘）

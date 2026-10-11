# DESIGN.md 预设 — Material 3 风格（Google）

> 内置设计系统预设，格式遵循 `references/design-system-template.md`（9-section）。
> 用途：design-context init 的 DESIGN.md 种子、theme 子技能 Token 参照。
> **预设不是免调研通行证**：M3 的灵魂是 Dynamic Color——正式使用必须从品牌种子色
> 生成完整 tonal palette（基线紫 #6750a4 只是默认种子，不是品牌色）。

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

- **品牌人格**：活力创造者（明快、有弹性、色彩驱动）
- **情绪板**：明快 · 弹性 · 有机
- **设计意图**：色彩与形状传达层级，动效表达空间关系
- **适合**：消费级应用、内容社区、工具型移动端、跨端产品
- **不适合**：数据密集的传统中后台（层级系统过重会拖效率）
- **参考先例**：Google 全家桶（Gmail、Google Home）、Android 14+ 原生应用

## 2. 配色 (Color)

```css
:root {
  /* 原始层：M3 baseline tonal palette（种子色 #6750a4 生成，正式项目重生成） */
  --md-primary: #6750a4;         /* Primary 40 */
  --md-on-primary: #ffffff;
  --md-primary-container: #eaddff; /* Primary 90 */
  --md-secondary: #625b71;
  --md-tertiary: #7d5260;
  --md-surface: #fef7ff;
  --md-surface-variant: #e7e0ec;
  --md-on-surface: #1d1b20;
  --md-on-surface-variant: #49454f;
  --md-outline: #79747e;
  --md-error: #b3261e;

  /* 语义层 */
  --color-primary: var(--md-primary);
  --color-danger: var(--md-error);
  --color-text: var(--md-on-surface);
  --color-muted: var(--md-on-surface-variant);
  --color-border: var(--md-outline);
  --color-surface: var(--md-surface);
  --color-canvas: var(--md-surface);
}
```

- 色彩角色化：primary 只给 FAB/主按钮/选中态，大面积氛围用 container 色
- 表面用色调微移（surface tint）表达层级，**不堆投影**——这是 M3 与 M2 的分界线

## 3. 排版 (Typography)

```css
:root {
  --font-body: "Roboto", "Noto Sans SC", system-ui, sans-serif;
  /* M3 type scale（计算后档位，需换算为 rem 落 Token） */
  --font-size-display-lg: 57px;  /* Display：品牌时刻才用 */
  --font-size-headline-md: 28px; /* Headline：页面主标题 */
  --font-size-title-lg: 22px;    /* Title：区块标题 */
  --font-size-body-lg: 16px;     /* Body：正文（移动端基准） */
  --font-size-label-lg: 14px;    /* Label：按钮/标签 */
}
```

- M3 字号阶是官方台阶，禁止自造中间档；同屏可见档位控制在 typography.md 上限内
- 大标题负 tracking（Display/Headline 约 -0.25px~-0.5px），正文零 tracking

## 4. 间距 (Spacing)

```css
:root {
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px;
  /* M3 shape scale：五档圆角 */
  --radius-xs: 4px;  --radius-sm: 8px;  --radius-md: 12px;
  --radius-lg: 16px; --radius-xl: 28px; --radius-full: 999px;
}
```

- 组件与圆角档位一一对应：chip/small 按钮 8px、卡片 12px、FAB/sheet 16-28px
- 触摸目标最小 48dp（M3 标准，高于通用 44pt 底线）

## 5. 布局与构图 (Layout & Composition)

- 栅格遵循 M3 layout：移动端 4 列 / 平板 8 列 / 桌面 12 列，gutter 24px
- 导航自适应：小屏 NavigationBar（底部）、中屏 NavigationRail（侧轨）、大屏 NavigationDrawer
- FAB 是页面唯一主操作的锚点，不放次要操作

## 6. 组件 (Components)

- **按钮四件套**：Filled（主）/ Tonal（次）/ Outlined（边缘场景）/ Text（低强调），一屏一 Filled
- **状态层**：悬停/按压/选中全部用 on-color 8%/12% 透明度叠加，不换底色
- **卡片三种**：Elevated / Filled / Outlined，同屏只用其中两型
- **Snackbar** 用于轻反馈，需要用户行动的用 banner 或对话框
- **Chip** 承担筛选/输入辅助/单选组，别把按钮做成 chip 形状

## 7. 动效与交互 (Motion & Interaction)

- 官方缓动：emphasized `cubic-bezier(0.2, 0, 0, 1)`；时长 200ms（小组件）/ 350-500ms（容器转场）
- 转场表达空间：容器变换（container transform）> 淡入淡出；共享元素跨页过渡
- 触觉反馈是 M3 一部分（移动端勾选态、FAB 按压）
- `prefers-reduced-motion` 下降级为透明度切换

## 8. 语调与品牌 (Voice & Brand)

- 文案友好但不卖萌；空态给插画 + 一句引导 + 主操作按钮
- 数字与单位跟随 locale 规范；日期用相对表达（今天、昨天）
- 错误文案提供出路：「连接已断开，正在重试（第 2 次）」

## 9. 禁止模式 (Anti-patterns)

- 禁止 M2 遗产：硬投影阴影当主层级手段（层级靠 surface tint 与轮廓）
- 禁止绕过 tonal palette 直接引 hex——主题必须由种子色生成
- 禁止把 FAB 当装饰或放次要操作
- 禁止自造字号档位与圆角档位（M3 shape/type scale 是封闭集合）
- 禁止动效超过 500ms 的非容器转场

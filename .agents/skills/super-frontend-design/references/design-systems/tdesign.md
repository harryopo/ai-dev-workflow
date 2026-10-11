# DESIGN.md 预设 — TDesign 风格（腾讯企业级）

> 内置设计系统预设，格式遵循 `references/design-system-template.md`（9-section）。
> 用途：design-context init 时的 DESIGN.md 种子、theme 子技能的 Token 参照、
> design Part 7「国内企业级组件库」的 TDesign 对接基准。
> **预设不是免调研通行证**：品牌色仅是基线种子，正式使用必须经 research → theme
> 从视觉论文推导后再落 Token；技术栈用 TDesign 时，原始层 Token 直接映射 `--td-*` 变量。

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

- **品牌人格**：极客工程师（可靠、克制、系统感）
- **情绪板**：稳固 · 清晰 · 秩序
- **设计意图**：数据密集场景的确定性——界面是工具，不抢内容的戏
- **适合**：管理后台、企业中台、数据平台、SaaS 控制台
- **不适合**：品牌营销页、消费级内容社区（会显得过于严肃）
- **参考先例**：腾讯系产品中后台（腾讯云控制台、企业微信管理端）

## 2. 配色 (Color)

```css
:root {
  /* 原始层：TDesign 官方变量（tdesign-react / tdesign-vue-next 原生） */
  --td-brand-color: #0052d9;
  --td-brand-color-hover: #266fe8;
  --td-brand-color-active: #0048c6;
  --td-success-color: #2ba471;
  --td-warning-color: #e37318;
  --td-error-color: #d54941;
  --td-gray-color-14: #0b0d0f;   /* 文字主色 */
  --td-gray-color-10: #262a2e;   /* 次级文字 */
  --td-gray-color-6: #b4bac1;    /* 边线 */
  --td-gray-color-1: #f3f5f7;    /* 页面底 */

  /* 语义层：产物代码只引用这里 */
  --color-primary: var(--td-brand-color);
  --color-success: var(--td-success-color);
  --color-warning: var(--td-warning-color);
  --color-danger: var(--td-error-color);
  --color-text: var(--td-gray-color-14);
  --color-muted: var(--td-gray-color-10);
  --color-border: var(--td-gray-color-6);
  --color-surface: #ffffff;
  --color-canvas: var(--td-gray-color-1);
}
```

- 强调色使用面积克制：中性色主导界面，品牌色只给主操作与选中态
- 状态色语义固定：成功绿、进行蓝、警示橙、失败红、停用灰，全站不换含义

## 3. 排版 (Typography)

```css
:root {
  --font-body: "PingFang SC", "Microsoft YaHei", "Segoe UI", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", Consolas, ui-monospace, monospace; /* register 用，≤2 处 */
  --font-size-xs: 12px;   /* 辅助说明 */
  --font-size-sm: 14px;   /* 正文主导（B 端标准） */
  --font-size-md: 16px;   /* 小标题 */
  --font-size-lg: 20px;   /* 区块标题 */
  --font-size-xl: 24px;   /* 页面标题 */
}
```

- 正文 14px 主导（B 端纪律，见 admin-enterprise-patterns.md §10），标题克制不加 Display 档
- 数字列一律 tabular-nums；行高正文 1.6、标题 1.3

## 4. 间距 (Spacing)

```css
:root {
  --space-xs: 4px;  --space-sm: 8px;  --space-md: 12px;
  --space-lg: 16px; --space-xl: 24px; --space-2xl: 32px;
  --radius-sm: 3px; --radius-md: 6px; --radius-lg: 9px; --radius-full: 999px;
}
```

- 圆角小而统一（TDesign 基线 3px 起阶），不追大圆角卡片风
- 表格行高两档：紧凑 40px / 标准 48px，密度可切换

## 5. 布局与构图 (Layout & Composition)

- 模式复用优先：列表页 / 详情页 / 仪表盘 / 设置页四模板起步（admin-enterprise §9）
- 侧导航 220px 固定 + 可折叠到 64px 图标态；内容区最大宽 1440px 居中
- 筛选条件进 URL；批量操作贴表格顶部浮现（admin-enterprise §4/§5）

## 6. 组件 (Components)

- **按钮**：主按钮品牌蓝实底、次按钮描边、文字按钮灰色；同一操作区只允许一个主按钮
- **表格**：表头灰底、行悬停浅灰、金额右对齐 tabular-nums、操作列末列固定
- **表单**：标签左置（横排）或上置（纵排）全站统一；失焦即时校验 + 提交全量
- **对话框**：标题 + 内容 + 右下操作对；破坏性操作用红色主按钮并写明后果
- **反馈**：toast 用于动作结果（自动消失），需要留存的进任务中心/站内通知

## 7. 动效与交互 (Motion & Interaction)

- 动效只服务状态反馈：150-250ms、ease-out，禁止入场大动画与滚动叙事
- 悬停反馈统一 0.15s 透明度/底色过渡；展开折叠用高度过渡
- 全站必须提供 `prefers-reduced-motion` 降级

## 8. 语调与品牌 (Voice & Brand)

- 文案短、动词开头、说清结果：「已发货 20 单」而不是「操作成功」
- 空态文案给下一步：「还没有订单，去新建第一笔」
- 错误文案三要素：发生了什么 + 为什么 + 用户能做什么

## 9. 禁止模式 (Anti-patterns)

- 禁止营销页元素混入：Hero 大字、两色渐变、装饰 blob（B 端纪律）
- 禁止把 C 端大字号阶（48px Display）搬进后台
- 禁止绕过 `--td-*` 直接改组件内部类名样式
- 禁止 emoji 当功能图标；图标统一用 TDesign Icons
- 禁止彩色投影卡片堆砌——卡片层级靠边线与底色，不靠影子

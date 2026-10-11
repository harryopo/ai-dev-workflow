# DESIGN.md 预设 — Ant Design 风格（蚂蚁企业级）

> 内置设计系统预设，格式遵循 `references/design-system-template.md`（9-section）。
> 用途：design-context init 的 DESIGN.md 种子、theme 子技能 Token 参照、
> design Part 7「国内企业级组件库」的 Ant Design 对接基准。
> **预设不是免调研通行证**：正式使用必须经 research → theme 从视觉论文推导品牌色。
> 技术栈用 antd 5.x 时，原始层走 ConfigProvider `theme.token`（开 `cssVar: true` 得 `--ant-*`）。

## 1. 视觉主题与氛围 (Visual Theme & Atmosphere)

- **品牌人格**：专业人士（确定性、秩序、即时反馈）
- **情绪板**：确定 · 高效 · 即时
- **设计意图**：用最少的视觉元素承载最重的业务逻辑，反馈永远快人一步
- **适合**：中后台系统、ToB SaaS、数据密集型运营工具
- **不适合**：追求个性化表达的 C 端品牌站
- **参考先例**：蚂蚁系中后台（云凤蝶、阿里云控制台新基调）

## 2. 配色 (Color)

```css
:root {
  /* 原始层：antd 5 官方色板（theme.token 对应项） */
  --ant-color-primary: #1677ff;
  --ant-color-primary-hover: #4096ff;
  --ant-color-primary-active: #0958d9;
  --ant-color-success: #52c41a;
  --ant-color-warning: #faad14;
  --ant-color-error: #ff4d4f;
  --ant-color-text: rgba(0, 0, 0, 0.88);
  --ant-color-text-secondary: rgba(0, 0, 0, 0.65);
  --ant-color-border: #d9d9d9;
  --ant-color-bg-layout: #f5f5f5;

  /* 语义层 */
  --color-primary: var(--ant-color-primary);
  --color-success: var(--ant-color-success);
  --color-warning: var(--ant-color-warning);
  --color-danger: var(--ant-color-error);
  --color-text: var(--ant-color-text);
  --color-muted: var(--ant-color-text-secondary);
  --color-border: var(--ant-color-border);
  --color-surface: #ffffff;
  --color-canvas: var(--ant-color-bg-layout);
}
```

- 主操作蓝只给唯一主路径；面包屑/次级操作全部中性化
- 禁止把 v4 旧蓝 `#1890ff` 硬编码当品牌色——主色必须经 theme.token 注入

## 3. 排版 (Typography)

```css
:root {
  --font-body: -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-size-sm: 12px;
  --font-size-md: 14px;   /* 正文基准（antd 默认） */
  --font-size-lg: 16px;
  --font-size-xl: 20px;   /* 页面标题 */
}
```

- 正文 14px 基准、行高 1.5715（antd 基线）；标题用字重而非字号拉层级
- 状态文字跟随状态色（成功/失败/警示），不再单独加图标重复表达

## 4. 间距 (Spacing)

```css
:root {
  --space-xs: 8px; --space-sm: 12px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 40px;
  --radius-sm: 4px; --radius-md: 6px; --radius-lg: 8px; --radius-full: 999px;
}
```

- antd 5 基线圆角 6px；卡片与输入框同阶，不搞大小圆角混排
- 表单纵向间距 24px 一档到底，字段组之间才升 32px

## 5. 布局与构图 (Layout & Composition)

- 经典中后台骨架：侧边栏（可折叠）+ 顶栏 + 内容卡片区
- 内容用卡片分区，但同屏卡片不超过两层层级；「页头区」统一放标题+主操作
- 模式细节见 `references/admin-enterprise-patterns.md`（表格/筛选/批量/五态）

## 6. 组件 (Components)

- **反馈链完整**：每个写操作有 loading（按钮内联）、成功结果、失败原因三个态
- **表格**：列设置/密度切换交给组件自带能力；金额右对齐；固定操作列
- **表单**：antd Form 校验时机统一 blur + submit；label 宽度对齐（横排）
- **Modal vs Drawer**：编辑上下文用 Drawer 保留列表视野；确认动作用 Modal
- **空状态**：Empty 组件 + 下一步动作按钮，不给裸图标

## 7. 动效与交互 (Motion & Interaction)

- 即时反馈是灵魂：按钮按压态、输入聚焦描边、行悬停，全部 ≤200ms
- Modal/Drawer 进出 250ms ease-out；**不做**视差、滚动叙事、入场大动画
- 波纹效果保留在按钮上（antd 内建），不要手动复制到非按钮元素
- 全站提供 `prefers-reduced-motion` 降级

## 8. 语调与品牌 (Voice & Brand)

- 全局确认文案统一句式：「确定删除这 3 条记录吗？删除后可在回收站恢复。」
- 按钮动词精确：用「发布」「下线」，不用统一的「确定」
- 数字呈现走规范：千分位 + 单位缩写（1.2 万）跟随业务约定

## 9. 禁止模式 (Anti-patterns)

- 禁止硬编码 v4 遗留色（#1890ff）或绕过 theme.token 改样式
- 禁止禁用态输入框当只读展示用（用文本，见 admin-enterprise §6）
- 禁止在 Card 上叠彩色阴影和渐变边框装点
- 禁止把每个操作都做成 Modal 三连——保留页面级编辑视图
- 禁止 emoji 功能图标；图标走 @ant-design/icons

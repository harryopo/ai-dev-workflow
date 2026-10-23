---
name: super-frontend-design:animate
description: |
  动效设计模块。支持 Motion（motion/react）和 GSAP 两种动画库，提供时序编排、缓动曲线设计、
  ScrollTrigger滚动驱动、SplitText文字动画、Flip布局过渡、性能优化、无障碍适配（prefers-reduced-motion）。
  由 super-frontend-design 主入口路由调用。
  合并来源：impeccable (animate) + gsap-animation-guide
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Animate — 动效设计

## 1. 概述

本模块负责设计和管理前端动效，确保动效有意义、性能优异、可访问性好。

**核心能力：**
- Motion（motion/react）简单入场/退出/悬停
- GSAP 复杂时间轴编排、ScrollTrigger、SplitText、Flip
- 时序与缓动曲线设计
- 性能优化（transform/opacity 优先）
- 无障碍适配（prefers-reduced-motion）

---

## 0. 动效调研前置（铁律）

> ⚠️ **在执行任何动效设计前，必须先确认动效需求。禁止假设用户想要动效。**

### Step 0.1: 从 Design Brief 读取动效配置

**必须首先加载并读取以下文件：**
1. `output/design-system.md` 或 `pass-data.yaml`
2. 查找字段：`动效方向`、`动效强度`、`交互节奏`、`粒子/WebGL`

```yaml
# 从 Design Brief 提取的动效配置示例：
动效方向: 中等动效
动效强度: 流畅自然
交互节奏: 300-500ms
粒子/WebGL: 可选
```

### Step 0.2: 如果 Design Brief 中缺少动效信息

**如果 Design Brief 中没有动效相关字段 → 必须使用 AskUserQuestion 询问用户：**

```
header: "动效需求"
question: "这个设计需要什么样的动效？"
options:
  - "无动效，纯静态" → 后台、Dashboard、金融科技
  - "少量微交互" → hover/focus 反馈 + 简单 fade
  - "中等动效" → ScrollTrigger + 数字计数 + 渐入揭示
  - "丰富动效" → 复杂时间轴 + SplitText + 视差
  - "需要粒子/WebGL" → 粒子背景 + Shader + 3D 效果
  - "不确定，按场景推荐"
multiSelect: false
```

### Step 0.3: 场景 × 动效智能推荐

基于设计类型自动推荐动效方案（展示给用户确认）：

| 设计类型 | 推荐动效方案 | 原因 |
|----------|-------------|------|
| 产品官网 / Landing Page | 滚动驱动 + 入场 reveal + 数字计数 | 强调品牌故事，提升转化率 |
| 后台管理系统 | 无或极简 fade | 效率优先，动效干扰操作 |
| 移动端 App | 手势微交互 + 页面转场 | 流畅响应，符合移动习惯 |
| 数据 Dashboard | 图表渐进绘制 + 数字步进 | 数据可读性，避免分散注意力 |
| 品牌展示页 / 作品集 | 沉浸式 3D / WebGL / 视差层叠 | 强调视觉冲击和品牌调性 |
| 电商 / 营销落地页 | 弹性入场 + hover 反馈 + CTA 突出 | 引导转化，营造紧迫感 |
| 教育 / 内容平台 | 温和 fade + 进度指示 | 舒适阅读，减少认知负担 |
| 金融科技 | 无动效或极简数据过渡 | 专业克制，建立信任感 |
| 游戏品牌 / 娱乐 | 粒子系统 + Shader + 霓虹 glow | 能量感，强化沉浸体验 |
| 工具 / SaaS 产品 | 功能性动效（loading、success） | 实用优先，减少干扰 |

**用户确认动效方案后，进入正式动效设计流程。**

---

## 2. 触发条件

以下关键词触发本模块：
- "animate"、"动效"、"动画"
- "微交互"、"hover"、"入场动画"
- "ScrollTrigger"、"GSAP"、"时间轴"
- "SplitText"、"Flip"、"视差"

---

## 3. 动画库选择决策

### 3.1 选择矩阵

| 场景 | 推荐库 | 原因 |
|------|--------|------|
| 简单入场/退出 | Motion | 轻量、声明式、React 原生 |
| 悬停/点击反馈 | Motion | 简单、性能好 |
| 复杂时间轴编排 | GSAP | 精确控制、可嵌套 |
| 滚动驱动动画 | GSAP (ScrollTrigger) | 行业标准 |
| 文字逐字动画 | GSAP (SplitText) | 专业文字动画 |
| 布局过渡动画 | GSAP (Flip) | 自动计算位置变化 |
| SVG 路径动画 | GSAP | 精确路径控制 |
| 纯静态页面 | CSS transitions | 无依赖、性能最优 |

### 3.2 性能考量

| 库 | 体积 | 学习曲线 | 适用场景 |
|----|------|----------|----------|
| Motion | ~15KB | 低 | 简单动效 |
| GSAP | ~25KB（核心） | 中 | 复杂动效 |
| CSS transitions | 0KB | 低 | 静态页面 |

---

## 4. 时序设计

### 4.1 标准时长

| 动效类型 | 时长范围 | 用途 |
|----------|----------|------|
| 微交互（hover/press） | 150-300ms | 状态反馈 |
| 过渡动画（页面切换） | 300-500ms | 场景切换 |
| 复杂动画（onboarding） | ≤1000ms | 引导流程 |
| 滚动动画 | 根据内容 | 视差/视差滚动 |

### 4.2 缓动曲线

**标准缓动曲线：**

| 名称 | CSS 值 | GSAP 值 | 用途 |
|------|--------|---------|------|
| ease-out | cubic-bezier(0.16, 1, 0.3, 1) | Expo.easeOut | 入场动画 |
| ease-in | cubic-bezier(0.55, 0, 1, 0.45) | Expo.easeIn | 离场动画 |
| ease-in-out | cubic-bezier(0.65, 0, 0.35, 1) | Expo.easeInOut | 过渡动画 |
| standard | cubic-bezier(0.2, 0, 0, 1) | Power2.easeOut | 微交互 |
| decelerate | cubic-bezier(0, 0, 0.2, 1) | Power3.easeOut | 滑动反馈 |
| accelerate | cubic-bezier(0.4, 0, 1, 1) | Power3.easeIn | 加速入场 |

**Motion 示例：**
```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
/>
```

**GSAP 示例：**
```javascript
gsap.to(".element", {
  opacity: 1,
  y: 0,
  duration: 0.5,
  ease: "expo.out"
});
```

---

## 5. GSAP 高级特性

### 5.1 ScrollTrigger

滚动驱动动画，用于视差效果和滚动触发动画。

```javascript
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

ScrollTrigger.create({
  trigger: ".section",
  start: "top 80%",
  end: "bottom 20%",
  scrub: true,
  animation: gsap.to(".element", {
    y: -100,
    opacity: 0.5
  })
});
```

### 5.2 SplitText

文字逐字/逐行动画。

```javascript
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const split = new SplitText(".heading", { type: "chars" });
gsap.from(split.chars, {
  opacity: 0,
  y: 50,
  stagger: 0.02,
  duration: 0.5,
  ease: "back.out(1.7)"
});
```

### 5.3 Flip

布局过渡动画，自动计算元素位置变化。

```javascript
import { Flip } from "gsap/Flip";
gsap.registerPlugin(Flip);

const state = Flip.getState(".card");
// 执行布局变化...
Flip.from(state, {
  duration: 0.5,
  ease: "power1.inOut",
  stagger: 0.02
});
```

### 5.4 React 集成

```jsx
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function MyComponent() {
  const scope = useGSAP(() => {
    ScrollTrigger.create({
      trigger: scope.current,
      start: "top 80%"
    });
  }, { scope });

  return <div ref={scope}>{/* ... */}</div>;
}
```

---

## 6. 性能优化

### 6.1 动画属性选择

**优先使用：**
- `transform`（translate, scale, rotate）
- `opacity`

**避免使用：**
- `width`, `height`, `top`, `left`（触发 layout）
- `margin`, `padding`（触发 layout）
- `box-shadow`（触发 paint）

### 6.2 will-change 使用

```css
.animated-element {
  will-change: transform, opacity;
}
```

**注意：** 仅在需要时添加，不要滥用。

### 6.3 减少重绘

```css
/* 避免触发重绘的属性 */
background-color: red; /* paint */
border-radius: 10px;   /* paint */
filter: blur(5px);     /* paint */

/* 只触发合成的属性 */
transform: translateY(-10px); /* composite */
opacity: 0.5;                /* composite */
```

---

## 7. 无障碍适配

### 7.1 prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 7.2 GSAP 无障碍适配

```javascript
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

gsap.to(".element", {
  x: 100,
  duration: prefersReducedMotion ? 0 : 0.5,
  ease: "power2.out"
});
```

---

## 8. 动效设计原则

### 8.1 有意义的动效

每个动效必须有明确的目的：
- 引导用户注意力
- 提供状态反馈
- 展示空间关系
- 增强沉浸感

### 8.2 避免的动效

- 纯装饰性动画（无功能目的）
- 过长的动画（>1000ms）
- 同时动画的元素过多（>5个）
- 快速切换的动画（stuttering）

### 8.3 品牌一致性

动效风格应与品牌人格一致：
- **专业权威**：克制、精准、流畅
- **友好亲切**：柔和、弹性、有温度
- **激进创新**：大胆、快速、有冲击力
- **克制内敛**：轻微、缓慢、低调

---

## 9. 执行流程

### 步骤 1：分析需求

- 确定动效类型（入场/退出/悬停/滚动）
- 确定目标元素
- 确定交互触发方式

### 步骤 2：选择动画库

根据需求矩阵选择 Motion 或 GSAP

### 步骤 3：设计时序

- 确定时长（150-500ms 标准）
- 选择缓动曲线
- 确定延迟（stagger）

### 步骤 4：实现代码

按照目标库的最佳实践实现

### 步骤 5：性能检查

- 确认只使用 transform/opacity
- 检查 will-change 使用
- 验证 prefers-reduced-motion 适配

### 步骤 6：测试

- 在不同设备上测试
- 检查 60fps 流畅度
- 验证无障碍适配

---

## 10. 常见问题

### Q: 如何选择 Motion 还是 GSAP？

**选 Motion：**
- 简单入场/退出动画
- 悬停/点击反馈
- 需要声明式 API
- 项目已使用 React

**选 GSAP：**
- 复杂时间轴编排
- 滚动驱动动画
- 文字逐字动画
- SVG 路径动画
- 需要精确控制

### Q: 如何处理大型列表动画？

- 使用虚拟列表（react-window）
- 分批渲染动画元素
- 使用 requestAnimationFrame
- 限制同时动画元素数量（≤5个）

---

## 11. 桌面应用动效模式

> 加载 `references/motion-patterns.md` 获取完整桌面动效规范。

### 桌面 vs 网页动效差异

| 维度 | 网页动效 | 桌面动效 |
|------|---------|---------|
| 性能预算 | 浏览器限制 | 系统原生资源 |
| 系统整合 | 仅 Web API | 原生窗口/拖放/剪贴板 |
| 用户预期 | 随时可刷新 | 状态持久，动效需尊重历史 |
| 卡顿感知 | 可接受 | 更敏感（用户长期使用） |
| 动效优先级 | 装饰+功能 | 功能>装饰，克制优先 |

### 平台动效规范

| 平台 | 窗口动画 | 面板滑入 | 按钮反馈 | 关键原则 |
|------|---------|---------|---------|---------|
| macOS | Scale+fade 200-300ms | Spring 250-350ms | Scale 100ms | Spring 物理曲线 |
| Windows | Fade+slide 200-300ms | Slide 200-250ms | Raise+color 100-150ms | Acrylic 模糊效果 |
| Linux (GNOME) | Fade+scale 200-250ms | Slide 200-250ms | Scale 100ms | 简洁流畅 |

### 各框架动效方案

| 框架 | 推荐方案 | 时长范围 |
|------|---------|---------|
| Electron | CSS transitions（首选） | 150-300ms |
| Tauri | CSS transitions + 原生窗口动画 | 150-300ms |
| PySide6 | QPropertyAnimation | 150-350ms |
| SwiftUI | withAnimation(.spring()) | 200-400ms |
| WinUI 3 | Implicit animations | 150-300ms |

### 桌面常用动效模式

| 场景 | 方案 | 时长 |
|------|------|------|
| 窗口打开 | Fade in + Scale up | 200-300ms |
| 窗口关闭 | Fade out | 150-200ms |
| 面板折叠 | 宽度过渡（transform） | 200-250ms |
| 列表新增 | Slide in from top | 200ms |
| 列表删除 | Fade out + Shrink | 150ms |
| 模态弹出 | Scale 0.9→1.0 + 遮罩淡入 | 200-300ms |
| Toast 通知 | Slide in/out | 250ms |
| 页面切换 | Slide 左右 | 300ms |
| 按钮点击 | Scale down 0.95→1.0 | 100ms |

### 桌面动效检查清单

- [ ] 窗口动画使用系统原生 API（非 CSS 模拟）
- [ ] 面板折叠使用 transform/width 过渡（非 JS 频繁计算）
- [ ] 所有动效可被用户操作立即中断
- [ ] 尊重 prefers-reduced-motion（macOS/Windows/Linux）
- [ ] 动效时长在 150-500ms 范围内
- [ ] 动效风格符合当前平台规范
- [ ] 低性能设备可降级（减少/禁用动效）

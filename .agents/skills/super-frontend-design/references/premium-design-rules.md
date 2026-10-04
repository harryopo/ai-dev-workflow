# Premium Design Rules — 高级感/大气界面设计规范

> 本文件定义"大气美观/高级感/惊艳"界面的具体数值化规则。
> 所有设计输出必须满足以下规则。review §2.18 自动扫描检查。

---

## 1. 留白规范 (Whitespace)

### 1.1 Section 间距
- 标准 section: `py-24 md:py-32` (96px-128px)
- Hero section: `pt-20 md:pt-32 pb-32 md:pb-48`
- CTA/Footer前最后一个section: `pb-24 md:pb-32`
- ❌ 禁止所有section统一使用 `py-12` 或 `py-16`

### 1.2 内容宽度
- 主容器: `max-w-7xl mx-auto px-6 md:px-8`
- 文字段落最大宽度: `max-w-3xl` (prose宽度)
- 大标题最大宽度: `max-w-4xl`
- ❌ 禁止内容撑满屏幕到边缘

### 1.3 段落间距
- 段落之间: `space-y-6` (24px)
- 标题与正文之间: `mt-4` 或 `mt-6`
- 列表项之间: `space-y-3` (12px)

---

## 2. 排版规范 (Typography Premium)

### 2.1 字号阶（必须使用clamp()流式排版）
```css
--font-size-display: clamp(2.5rem, 7vw, 5.5rem);   /* 40-88px Hero大标题 */
--font-size-h1: clamp(2rem, 5vw, 3.5rem);          /* 32-56px */
--font-size-h2: clamp(1.5rem, 4vw, 2.5rem);        /* 24-40px */
--font-size-h3: clamp(1.25rem, 2.5vw, 1.875rem);   /* 20-30px */
--font-size-body-lg: 1.125rem;                      /* 18px */
--font-size-body: 1rem;                             /* 16px */
--font-size-caption: 0.875rem;                      /* 14px */
```

### 2.2 字重策略
- Display/H1: `font-weight: 400` (Regular) 或 `font-weight: 500` (Medium)
- H2/H3: `font-weight: 500` (Medium) 或 `font-weight: 600` (Semibold)
- Body: `font-weight: 400` (Regular)
- Button labels: `font-weight: 500` (Medium)
- ❌ 禁止大标题使用 `font-weight: 700` (Bold) 或更重
- ❌ 全篇禁止 `font-black (900)` 和 `font-extrabold (800)`

### 2.3 字间距（letter-spacing）
- Display/H1 (>2.5rem): `letter-spacing: -0.02em` 到 `-0.04em`（负tracking）
- H2: `letter-spacing: -0.01em`
- ALL CAPS 文字: `letter-spacing: 0.06em` 到 `0.1em`
- 正文: `letter-spacing: normal`

### 2.4 行高
- Display: `line-height: 1.05` 到 `1.1`（紧凑）
- H1/H2: `line-height: 1.15` 到 `1.25`
- 正文: `line-height: 1.6` 到 `1.75`
- ❌ 禁止所有文字统一使用 `leading-relaxed (1.625)`

---

## 3. 色彩规范 (Premium Color)

### 3.1 中性色板（高级感专用值）
```css
/* 亮色模式 */
--color-background: #FFFFFF;
--color-surface: #FAFAFA;
--color-surface-alt: #F8F8F8;
--color-text-primary: #0A0A0A;
--color-text-secondary: #52525B;
--color-text-tertiary: #71717A;
--color-border: #E4E4E7;
--color-border-subtle: #F4F4F5;

/* 暗色模式 */
--color-background-dark: #0A0A0A;
--color-surface-dark: #171717;
--color-text-primary-dark: #FAFAFA;
--color-text-secondary-dark: #A1A1AA;
--color-border-dark: #27272A;
```

### 3.2 色彩数量限制
- 整个界面主色+强调色不超过 **2种彩色**
- 强调色使用面积 < 5%（CTA按钮/关键数据点/少量装饰）
- ❌ 禁止同时出现3种以上高饱和色彩

### 3.3 渐变规则
- 文字渐变（黑到灰）: `linear-gradient(to bottom, #0A0A0A 0%, #52525B 100%)`
- 同色系渐变: `linear-gradient(135deg, {hue-light}, {hue-dark})`
- 金属质感: `linear-gradient(135deg, #fff 0%, #a3a3a3 50%, #fff 100%)`
- ❌ 禁止不同色相之间的渐变（蓝→紫→粉 绝对禁止）
- ❌ 禁止超过3个色标的渐变
- 渐变仅用于大标题/背景光晕/CTA按钮，不用于正文/普通卡片

---

## 4. 阴影与光影规范 (Shadow & Lighting)

### 4.1 阴影层级
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 2px 4px -1px rgb(0 0 0 / 0.05),
            0 4px 6px -1px rgb(0 0 0 / 0.03);
--shadow-lg: 0 4px 6px -2px rgb(0 0 0 / 0.05),
            0 10px 20px -5px rgb(0 0 0 / 0.08);
--shadow-xl: 0 10px 25px -5px rgb(0 0 0 / 0.08),
            0 20px 50px -12px rgb(0 0 0 / 0.12);
--shadow-glow: 0 0 60px -15px var(--color-accent);
```

### 4.2 阴影原则
- 光从上方来，阴影向下偏移（y-offset 必须为正）
- 多层阴影（外层大而淡，内层小而深）比单阴影更自然
- ❌ 禁止直接使用 Tailwind 默认的 `shadow-md/shadow-lg`（黑色太重）
- ❌ 禁止彩色阴影（除了glow光晕效果）

---

## 5. 圆角规范 (Border Radius)

### 5.1 组件圆角标准
- 按钮 (Button): `rounded-lg` (8px)
- 输入框 (Input): `rounded-md` (6px) 或 `rounded-lg` (8px)
- 卡片 (Card): `rounded-xl` (12px)
- 模态框 (Modal): `rounded-2xl` (16px)
- 标签/徽章 (Badge): `rounded-full`
- 头像 (Avatar): `rounded-full`

### 5.2 品牌人格与圆角映射
| 人格 | 按钮圆角 | 卡片圆角 |
|------|:---:|:---:|
| 极简主义者/权威专家/数据驱动 | rounded-md (6px) | rounded-lg (8px) |
| 优雅艺术家/奢华高端 | rounded-lg (8px) | rounded-xl (12px) |
| 友好向导/教育品牌 | rounded-lg (8px) | rounded-xl (12px) |
| 活力创作者/游戏品牌 | rounded-xl (12px) | rounded-2xl (16px) |

### 5.3 圆角禁忌
- ❌ 按钮禁止 `rounded-full`（除非是icon-only圆形按钮）
- ❌ 卡片禁止 `rounded-2xl` (16px) 以上
- ❌ 一个页面内圆角不统一

---

## 6. 动效规范 (Premium Motion)

### 6.1 动画库
- **首选**: Motion (`motion/react`) — 原Framer Motion，适合简单入场/退出/悬停
- **备选**: CSS transitions + animations（纯静态页面）
- **复杂动效**: GSAP — 复杂时间轴编排、ScrollTrigger 滚动驱动、SplitText 文字动画、Flip 布局过渡时使用
- **禁止**: jQuery动画（过时）

### 6.2 动效时长
| 类型 | 时长 | 缓动 |
|------|:---:|------|
| Hover微交互 | 150ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 过渡动画 | 200-300ms | spring(stiffness: 300, damping: 30) |
| 入场动画 | 400-600ms | spring(stiffness: 200, damping: 25) |
| Stagger子元素延迟 | 40-80ms | 线性stagger |
| 离场动画 | 200ms | `cubic-bezier(0.4, 0, 1, 1)` |

### 6.3 Spring物理动画参数
```tsx
// 按钮点击
whileTap={{ scale: 0.97 }}
transition={{ type: "spring", stiffness: 400, damping: 25 }}

// 卡片入场
initial={{ opacity: 0, y: 20 }}
whileInView={{ opacity: 1, y: 0 }}
transition={{ type: "spring", stiffness: 200, damping: 25 }}

// 模态框
initial={{ opacity: 0, scale: 0.95 }}
animate={{ opacity: 1, scale: 1 }}
transition={{ type: "spring", stiffness: 300, damping: 25 }}
```

### 6.4 Scroll-driven animations（原生CSS）
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(32px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
```

### 6.5 动效禁忌
- ❌ 动画时长超过600ms
- ❌ 同时给5个以上元素stagger动画
- ❌ 对color/background-color做动画（用opacity或transform替代）
- ❌ 不支持`prefers-reduced-motion`
- ❌ 用JS监听scroll事件实现滚动动画

---

## 7. Bento Grid 规范（2026 不对称版）

- 桌面端: `grid-cols-3 md:grid-cols-4 lg:grid-cols-6`
- 间距: `gap-4` (16px) 或 `gap-6` (24px)
- 必须混合尺寸: 1x1 / 2x1 / 1x2 / 2x2（至少一个2x2大卡片）
- 内容密度必须不均匀
- ❌ 禁止所有卡片都是1x1

---

## 8. 文字渐变规范

### 允许模式
- 黑到灰: `linear-gradient(to bottom, #0A0A0A, #52525B)`
- 同色相深浅: `linear-gradient(135deg, var(--color-primary), color-mix(...))`
- 金属质感: `linear-gradient(135deg, #fff 0%, #a3a3a3 50%, #fff 100%)`

### 禁忌
- ❌ 蓝紫粉渐变（#6366f1→#a855f7→#ec4899）
- ❌ 互补色渐变（蓝→橙/红→绿）
- ❌ 给正文文字加渐变
- ❌ 超过3个色标的渐变

---

## 9. 装饰元素规范

### 允许的装饰
- 网格背景: 1px solid rgb(0 0 0 / 0.03), 40-60px
- 噪点纹理: opacity 0.03-0.05
- 渐变光晕: 400-800px, blur(100-150px), opacity 0.1-0.15

### 禁忌
- ❌ 装饰元素总面积超过视口15%
- ❌ 同时出现3个以上光晕
- ❌ emoji作为装饰
- ❌ confetti/彩带动画（除非成功页面）
- ❌ 浮动几何形状随机飘动

---

## 10. Section 节奏规范

### 推荐页面结构
```
1. Nav         (64-80px高)
2. Hero        (min-h-screen)
3. Logo/Ticker (60-80px高，紧凑)
4. Features    (sticky滚动)
5. Bento Grid  (不对称布局)
6. Testimonial (大留白引言)
7. Pricing     (结构化)
8. CTA         (min-h-[50vh]，大文字+按钮)
9. Footer      (200px+，信息密集)
```

### 松紧原则
- Hero → Ticker: 全屏→压缩（视觉呼吸）
- Ticker → Features: 紧凑→展开
- Bento → Testimonial: 密集→留白（视觉休息）
- Pricing → CTA: 结构化→冲击（情绪高潮）

---

## 11. 微交互规范

- 按钮: hover scale(1.02), tap scale(0.97)
- 卡片: hover shadow-md→shadow-lg + translateY(-2px)
- 链接: hover underline或颜色过渡150ms
- 推荐高级: Magnetic Button / Spotlight Card / Text Reveal / Number Counter / Ticker
- 优先动画 `transform` 和 `opacity`（GPU加速）
- 禁止动画 `top/left/width/height/margin/padding`

---

## 12. 图片处理规范

- 产品图: 去底PNG + `drop-shadow`
- 图片圆角: `rounded-xl` (12px)
- 图片hover: `scale-[1.02] transition-transform duration-300`
- 禁止背景图片（用纯色/渐变/图案代替）
- ❌ 图片加border
- ❌ 图片加彩色overlay（除非文字压在上面）

---

## 13. 斜体标题禁令

> 来源：hallmark 57条Slop Test — "Most Reliable AI Tell #1"

- ❌ **绝对禁止**在h1/h2/h3/title等标题元素使用`font-style: italic`或`italic` class
- ❌ **绝对禁止**在ALL CAPS标题使用斜体
- ❌ **绝对禁止**在品牌名称/产品名称使用斜体（除非品牌原始设计就是斜体）
- ✅ 标题使用font-weight、letter-spacing、color实现视觉层次
- ✅ 如需强调使用粗体（font-weight: 600）或更大字号

---

## 14. 侧边条纹卡片禁令

> 来源：hallmark 57条Slop Test — "Most Reliable AI Tell #2"

- ❌ **绝对禁止**卡片使用4-6px纯色左边框（尤其是purple/green/blue）
- ❌ **绝对禁止**使用`border-left: 4px solid #8b5cf6`这类模式
- ❌ **禁止**所有卡片使用相同颜色的侧边条纹作为设计模式
- ✅ 如需视觉区分，使用：背景色块、图标、缩进、阴影层次
- ✅ 如需强调，使用：更粗的字体、更大的字号、color变化

---

## 15. LCP优化规范

> 来源：hallmark 57条Slop Test + Web Vitals最佳实践

- ✅ Hero图片必须使用`loading="eager"` + `fetchpriority="high"`
- ✅ Hero图片必须有明确的`width`和`height`属性防止CLS
- ✅ 首屏字体必须使用`<link rel="preload">` + `font-display: swap`
- ✅ 关键CSS内联到`<head>`（首屏above-the-fold样式）
- ✅ 非必要字体使用`font-display: optional`
- ❌ 禁止首屏图片使用`loading="lazy"`
- ❌ 禁止首屏字体使用默认的`font-display: block`
- ❌ 禁止首屏图片无尺寸声明（导致CLS）

---

## 16. 间距4px倍数纪律

> 来源：hallmark 57条Slop Test + 数值化间距系统

- ✅ **所有**padding/margin/gap值必须是4的倍数
- ✅ 允许值集：4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80, 96, 128
- ❌ 禁止出现5, 7, 11, 13, 15, 17, 19等非4倍数间距
- ❌ 禁止使用px硬编码非4倍数值（如`padding: 17px`）
- ✅ Tailwind类映射：py-1=4px, py-2=8px, py-3=12px, py-4=16px, py-6=24px, py-8=32px, py-10=40px, py-12=48px, py-16=64px, py-20=80px, py-24=96px, py-32=128px
- ✅ 如果需要用非标准值，必须通过CSS变量定义为4px倍数

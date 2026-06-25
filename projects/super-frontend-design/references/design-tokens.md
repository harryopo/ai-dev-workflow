# Design Token 规范参考手册

> 包含三层Token架构、原始Token定义、语义Token映射、组件Token示例、
> CSS变量代码模板、暗色模式适配、OKLCH格式说明和Tailwind CSS集成指南。

---

## 一、三层 Token 架构说明

Design Token 采用三层架构，从抽象到具体：

```
┌─────────────────────────────────────────────┐
│  第1层：原始 Token (Primitive Tokens)         │
│  不含语义的原始值，如颜色值、数值              │
│  例: --blue-500: #3b82f6; --space-4: 16px    │
├─────────────────────────────────────────────┤
│  第2层：语义 Token (Semantic Tokens)          │
│  含语义用途的映射，关联原始Token               │
│  例: --primary: var(--blue-500)              │
│      --background: var(--gray-50)            │
├─────────────────────────────────────────────┤
│  第3层：组件 Token (Component Tokens)         │
│  特定组件的样式值，关联语义Token               │
│  例: --button-bg: var(--primary)             │
│      --card-shadow: var(--shadow-md)         │
└─────────────────────────────────────────────┘
```

### 架构原则
1. **原始层不变**: 原始Token值固定不变，是整个系统的原子基础
2. **语义层可切换**: 通过切换语义Token映射实现主题切换（亮/暗色模式）
3. **组件层引用语义**: 组件Token只引用语义Token，不直接引用原始Token
4. **单向依赖**: 组件 → 语义 → 原始，不可反向引用

---

## 二、原始 Token 定义

### 2.1 颜色原始 Token

#### 灰度色阶
```css
--gray-0:   #ffffff;
--gray-50:  #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;
--gray-950: #030712;
```

#### 蓝色色阶
```css
--blue-50:  #eff6ff;
--blue-100: #dbeafe;
--blue-200: #bfdbfe;
--blue-300: #93c5fd;
--blue-400: #60a5fa;
--blue-500: #3b82f6;
--blue-600: #2563eb;
--blue-700: #1d4ed8;
--blue-800: #1e40af;
--blue-900: #1e3a8a;
--blue-950: #172554;
```

#### 红色色阶
```css
--red-50:  #fef2f2;
--red-100: #fee2e2;
--red-200: #fecaca;
--red-300: #fca5a5;
--red-400: #f87171;
--red-500: #ef4444;
--red-600: #dc2626;
--red-700: #b91c1c;
--red-800: #991b1b;
--red-900: #7f1d1d;
--red-950: #450a0a;
```

#### 绿色色阶
```css
--green-50:  #f0fdf4;
--green-100: #dcfce7;
--green-200: #bbf7d0;
--green-300: #86efac;
--green-400: #4ade80;
--green-500: #22c55e;
--green-600: #16a34a;
--green-700: #15803d;
--green-800: #166534;
--green-900: #14532d;
--green-950: #052e16;
```

#### 黄色色阶
```css
--yellow-50:  #fefce8;
--yellow-100: #fef9c3;
--yellow-200: #fef08a;
--yellow-300: #fde047;
--yellow-400: #facc15;
--yellow-500: #eab308;
--yellow-600: #ca8a04;
--yellow-700: #a16207;
--yellow-800: #854d0e;
--yellow-900: #713f12;
--yellow-950: #422006;
```

#### 紫色色阶
```css
--purple-50:  #faf5ff;
--purple-100: #f3e8ff;
--purple-200: #e9d5ff;
--purple-300: #d8b4fe;
--purple-400: #c084fc;
--purple-500: #a855f7;
--purple-600: #9333ea;
--purple-700: #7e22ce;
--purple-800: #6b21f8;
--purple-900: #581c87;
--purple-950: #3b0764;
```

#### 橙色色阶
```css
--orange-50:  #fff7ed;
--orange-100: #ffedd5;
--orange-200: #fed7aa;
--orange-300: #fdba74;
--orange-400: #fb923c;
--orange-500: #f97316;
--orange-600: #ea580c;
--orange-700: #c2410c;
--orange-800: #9a3412;
--orange-900: #7c2d12;
--orange-950: #431407;
```

#### 青色色阶
```css
--cyan-50:  #ecfeff;
--cyan-100: #cffafe;
--cyan-200: #a5f3fc;
--cyan-300: #67e8f9;
--cyan-400: #22d3ee;
--cyan-500: #06b6d4;
--cyan-600: #0891b2;
--cyan-700: #0e7490;
--cyan-800: #155e75;
--cyan-900: #164e63;
--cyan-950: #083344;
```

#### 粉色色阶
```css
--pink-50:  #fdf2f8;
--pink-100: #fce7f3;
--pink-200: #fbcfe8;
--pink-300: #f9a8d4;
--pink-400: #f472b6;
--pink-500: #ec4899;
--pink-600: #db2777;
--pink-700: #be185d;
--pink-800: #9d174d;
--pink-900: #831843;
--pink-950: #500724;
```

### 2.2 间距原始 Token

```css
--space-0:   0px;
--space-px:  1px;
--space-0-5: 2px;
--space-1:   4px;
--space-1-5: 6px;
--space-2:   8px;
--space-2-5: 10px;
--space-3:   12px;
--space-3-5: 14px;
--space-4:   16px;
--space-5:   20px;
--space-6:   24px;
--space-7:   28px;
--space-8:   32px;
--space-9:   36px;
--space-10:  40px;
--space-11:  44px;
--space-12:  48px;
--space-14:  56px;
--space-16:  64px;
--space-20:  80px;
--space-24:  96px;
--space-28:  112px;
--space-32:  128px;
--space-36:  144px;
--space-40:  160px;
--space-44:  176px;
--space-48:  192px;
--space-52:  208px;
--space-56:  224px;
--space-60:  240px;
--space-64:  256px;
--space-72:  288px;
--space-80:  320px;
--space-96:  384px;
```

### 2.3 字号原始 Token

```css
--font-size-xs:   0.75rem;    /* 12px */
--font-size-sm:   0.875rem;   /* 14px */
--font-size-base: 1rem;       /* 16px */
--font-size-lg:   1.125rem;   /* 18px */
--font-size-xl:   1.25rem;    /* 20px */
--font-size-2xl:  1.5rem;     /* 24px */
--font-size-3xl:  1.875rem;   /* 30px */
--font-size-4xl:  2.25rem;    /* 36px */
--font-size-5xl:  3rem;       /* 48px */
--font-size-6xl:  3.75rem;    /* 60px */
--font-size-7xl:  4.5rem;     /* 72px */
--font-size-8xl:  6rem;       /* 96px */
--font-size-9xl:  8rem;       /* 128px */
```

### 2.4 圆角原始 Token

```css
--radius-none: 0px;
--radius-sm:   2px;
--radius:      4px;
--radius-md:   6px;
--radius-lg:   8px;
--radius-xl:   12px;
--radius-2xl:  16px;
--radius-3xl:  24px;
--radius-full: 9999px;
```

### 2.5 阴影原始 Token

```css
--shadow-xs:  0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm:  0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow:     0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-md:  0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-lg:  0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-xl:  0 25px 50px -12px rgb(0 0 0 / 0.25);
--shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
```

### 2.6 字重原始 Token

```css
--font-weight-thin:       100;
--font-weight-extralight: 200;
--font-weight-light:      300;
--font-weight-normal:     400;
--font-weight-medium:     500;
--font-weight-semibold:   600;
--font-weight-bold:       700;
--font-weight-extrabold:  800;
--font-weight-black:      900;
```

### 2.7 行高原始 Token

```css
--line-height-none:    1;
--line-height-tight:   1.25;
--line-height-snug:    1.375;
--line-height-normal:  1.5;
--line-height-relaxed: 1.625;
--line-height-loose:   2;
```

### 2.8 字间距原始 Token

```css
--letter-spacing-tighter: -0.05em;
--letter-spacing-tight:   -0.025em;
--letter-spacing-normal:  0em;
--letter-spacing-wide:    0.025em;
--letter-spacing-wider:   0.05em;
--letter-spacing-widest:  0.1em;
```

### 2.9 动画原始 Token

```css
--duration-75:   75ms;
--duration-100:  100ms;
--duration-150:  150ms;
--duration-200:  200ms;
--duration-300:  300ms;
--duration-500:  500ms;
--duration-700:  700ms;
--duration-1000: 1000ms;

--ease-linear:      linear;
--ease-in:          cubic-bezier(0.4, 0, 1, 1);
--ease-out:         cubic-bezier(0, 0, 0.2, 1);
--ease-in-out:      cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce:      cubic-bezier(0.34, 1.56, 0.64, 1);
--ease-spring:      cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

### 2.10 Z-index 原始 Token

```css
--z-0:    0;
--z-10:   10;
--z-20:   20;
--z-30:   30;
--z-40:   40;
--z-50:   50;
--z-auto: auto;
```

### 2.11 断点原始 Token

```css
--breakpoint-sm:  640px;
--breakpoint-md:  768px;
--breakpoint-lg:  1024px;
--breakpoint-xl:  1280px;
--breakpoint-2xl: 1536px;
```

---

## 三、语义 Token 映射表

### 3.1 亮色模式语义 Token

```css
:root {
  /* 基础颜色 */
  --background:         var(--gray-0);       /* 页面背景 */
  --foreground:         var(--gray-950);     /* 主要文字 */
  
  /* 主色 */
  --primary:            var(--blue-600);     /* 主色 */
  --primary-hover:      var(--blue-700);     /* 主色悬停 */
  --primary-foreground: var(--gray-0);       /* 主色上的文字 */
  
  /* 次要色 */
  --secondary:          var(--gray-100);     /* 次要背景 */
  --secondary-hover:    var(--gray-200);     /* 次要悬停 */
  --secondary-foreground: var(--gray-900);   /* 次要上的文字 */
  
  /* 强调色 */
  --accent:             var(--blue-100);     /* 强调背景 */
  --accent-hover:       var(--blue-200);     /* 强调悬停 */
  --accent-foreground:  var(--blue-900);     /* 强调上的文字 */
  
  /* 语义色 */
  --destructive:        var(--red-600);      /* 危险/删除 */
  --destructive-hover:  var(--red-700);      /* 危险悬停 */
  --destructive-foreground: var(--gray-0);   /* 危险上的文字 */
  
  --success:            var(--green-600);    /* 成功 */
  --success-hover:      var(--green-700);    /* 成功悬停 */
  --success-foreground: var(--gray-0);       /* 成功上的文字 */
  
  --warning:            var(--yellow-500);   /* 警告 */
  --warning-hover:      var(--yellow-600);   /* 警告悬停 */
  --warning-foreground: var(--gray-950);     /* 警告上的文字 */
  
  --info:               var(--blue-500);     /* 信息 */
  --info-hover:         var(--blue-600);     /* 信息悬停 */
  --info-foreground:    var(--gray-0);       /* 信息上的文字 */
  
  /* 表面 */
  --card:               var(--gray-0);       /* 卡片背景 */
  --card-foreground:    var(--gray-950);     /* 卡片文字 */
  --popover:            var(--gray-0);       /* 弹出层背景 */
  --popover-foreground: var(--gray-950);     /* 弹出层文字 */
  
  /* 边框与分割 */
  --border:             var(--gray-200);     /* 默认边框 */
  --border-hover:       var(--gray-300);     /* 边框悬停 */
  --input:              var(--gray-200);     /* 输入框边框 */
  --input-hover:        var(--gray-300);     /* 输入框悬停 */
  --ring:               var(--blue-500);     /* 焦点环 */
  
  /* 静音 */
  --muted:              var(--gray-100);     /* 静音背景 */
  --muted-foreground:   var(--gray-500);     /* 静音文字 */
}
```

### 3.2 暗色模式语义 Token

```css
.dark {
  /* 基础颜色 */
  --background:         var(--gray-950);
  --foreground:         var(--gray-50);
  
  /* 主色 */
  --primary:            var(--blue-500);
  --primary-hover:      var(--blue-400);
  --primary-foreground: var(--gray-950);
  
  /* 次要色 */
  --secondary:          var(--gray-800);
  --secondary-hover:    var(--gray-700);
  --secondary-foreground: var(--gray-50);
  
  /* 强调色 */
  --accent:             var(--gray-800);
  --accent-hover:       var(--gray-700);
  --accent-foreground:  var(--gray-50);
  
  /* 语义色 */
  --destructive:        var(--red-500);
  --destructive-hover:  var(--red-400);
  --destructive-foreground: var(--gray-950);
  
  --success:            var(--green-500);
  --success-hover:      var(--green-400);
  --success-foreground: var(--gray-950);
  
  --warning:            var(--yellow-500);
  --warning-hover:      var(--yellow-400);
  --warning-foreground: var(--gray-950);
  
  --info:               var(--blue-400);
  --info-hover:         var(--blue-300);
  --info-foreground:    var(--gray-950);
  
  /* 表面 */
  --card:               var(--gray-900);
  --card-foreground:    var(--gray-50);
  --popover:            var(--gray-900);
  --popover-foreground: var(--gray-50);
  
  /* 边框与分割 */
  --border:             var(--gray-800);
  --border-hover:       var(--gray-700);
  --input:              var(--gray-800);
  --input-hover:        var(--gray-700);
  --ring:               var(--blue-400);
  
  /* 静音 */
  --muted:              var(--gray-800);
  --muted-foreground:   var(--gray-400);
}
```

---

## 四、组件 Token 示例

### 4.1 Button 组件 Token

```css
:root {
  /* 默认按钮 */
  --button-bg:               var(--primary);
  --button-bg-hover:         var(--primary-hover);
  --button-foreground:       var(--primary-foreground);
  --button-border:           transparent;
  --button-border-hover:     transparent;
  --button-shadow:           var(--shadow-sm);
  --button-shadow-hover:     var(--shadow-md);
  --button-radius:           var(--radius-md);
  --button-padding-x:        var(--space-4);
  --button-padding-y:        var(--space-2);
  --button-font-size:        var(--font-size-sm);
  --button-font-weight:      var(--font-weight-medium);
  --button-line-height:      var(--line-height-none);
  --button-transition:       all var(--duration-150) var(--ease-in-out);
  
  /* 次要按钮 */
  --button-secondary-bg:           var(--secondary);
  --button-secondary-bg-hover:     var(--secondary-hover);
  --button-secondary-foreground:   var(--secondary-foreground);
  --button-secondary-border:       var(--border);
  --button-secondary-border-hover: var(--border-hover);
  
  /* 轮廓按钮 */
  --button-outline-bg:           transparent;
  --button-outline-bg-hover:     var(--accent);
  --button-outline-foreground:   var(--primary);
  --button-outline-border:       var(--border);
  --button-outline-border-hover: var(--primary);
  
  /* 危险按钮 */
  --button-destructive-bg:           var(--destructive);
  --button-destructive-bg-hover:     var(--destructive-hover);
  --button-destructive-foreground:   var(--destructive-foreground);
  
  /* 幽灵按钮 */
  --button-ghost-bg:           transparent;
  --button-ghost-bg-hover:     var(--accent);
  --button-ghost-foreground:   var(--primary);
  
  /* 按钮尺寸 */
  --button-sm-padding-x:  var(--space-3);
  --button-sm-padding-y:  var(--space-1);
  --button-sm-font-size:  var(--font-size-xs);
  --button-sm-radius:     var(--radius);
  
  --button-lg-padding-x:  var(--space-6);
  --button-lg-padding-y:  var(--space-3);
  --button-lg-font-size:  var(--font-size-base);
  --button-lg-radius:     var(--radius-lg);
  
  /* 图标按钮 */
  --button-icon-size:     var(--space-4);
  --button-icon-padding:  var(--space-2);
}
```

### 4.2 Card 组件 Token

```css
:root {
  --card-bg:               var(--card);
  --card-foreground:       var(--card-foreground);
  --card-border:           var(--border);
  --card-radius:           var(--radius-xl);
  --card-shadow:           var(--shadow);
  --card-padding:          var(--space-6);
  --card-header-padding:   var(--space-6);
  --card-content-padding:  var(--space-6);
  --card-footer-padding:   var(--space-6);
  --card-gap:              var(--space-4);
}
```

### 4.3 Input 组件 Token

```css
:root {
  --input-bg:              var(--background);
  --input-foreground:      var(--foreground);
  --input-border:          var(--input);
  --input-border-hover:    var(--input-hover);
  --input-border-focus:    var(--ring);
  --input-radius:          var(--radius-md);
  --input-padding-x:       var(--space-3);
  --input-padding-y:       var(--space-2);
  --input-font-size:       var(--font-size-sm);
  --input-line-height:     var(--line-height-normal);
  --input-shadow:          var(--shadow-xs);
  --input-shadow-focus:    0 0 0 2px var(--ring);
  --input-placeholder:     var(--muted-foreground);
  
  /* 输入框尺寸 */
  --input-sm-padding-x:  var(--space-2);
  --input-sm-padding-y:  var(--space-1);
  --input-sm-font-size:  var(--font-size-xs);
  
  --input-lg-padding-x:  var(--space-4);
  --input-lg-padding-y:  var(--space-3);
  --input-lg-font-size:  var(--font-size-base);
  
  /* 输入框状态 */
  --input-error-border:   var(--destructive);
  --input-error-shadow:   0 0 0 2px var(--destructive);
  --input-disabled-bg:    var(--muted);
  --input-disabled-opacity: 0.5;
}
```

### 4.4 Badge 组件 Token

```css
:root {
  --badge-radius:          var(--radius-full);
  --badge-padding-x:       var(--space-2);
  --badge-padding-y:       var(--space-0-5);
  --badge-font-size:       var(--font-size-xs);
  --badge-font-weight:     var(--font-weight-medium);
  --badge-line-height:     var(--line-height-none);
  
  --badge-default-bg:           var(--secondary);
  --badge-default-foreground:   var(--secondary-foreground);
  
  --badge-primary-bg:           var(--primary);
  --badge-primary-foreground:   var(--primary-foreground);
  
  --badge-destructive-bg:       var(--destructive);
  --badge-destructive-foreground: var(--destructive-foreground);
  
  --badge-success-bg:           var(--success);
  --badge-success-foreground:   var(--success-foreground);
  
  --badge-warning-bg:           var(--warning);
  --badge-warning-foreground:   var(--warning-foreground);
  
  --badge-outline-bg:           transparent;
  --badge-outline-foreground:   var(--foreground);
  --badge-outline-border:       var(--border);
}
```

### 4.5 Dialog/Modal 组件 Token

```css
:root {
  --dialog-bg:             var(--popover);
  --dialog-foreground:     var(--popover-foreground);
  --dialog-border:         var(--border);
  --dialog-radius:         var(--radius-2xl);
  --dialog-shadow:         var(--shadow-xl);
  --dialog-padding:        var(--space-6);
  --dialog-overlay-bg:     rgb(0 0 0 / 0.5);
  --dialog-header-padding: var(--space-6);
  --dialog-footer-padding: var(--space-6);
  --dialog-gap:            var(--space-4);
  --dialog-max-width:      560px;
  --dialog-z-index:        var(--z-50);
}
```

### 4.6 Tooltip 组件 Token

```css
:root {
  --tooltip-bg:            var(--gray-900);
  --tooltip-foreground:    var(--gray-50);
  --tooltip-radius:        var(--radius);
  --tooltip-padding-x:     var(--space-2);
  --tooltip-padding-y:     var(--space-1);
  --tooltip-font-size:     var(--font-size-xs);
  --tooltip-shadow:        var(--shadow-lg);
  --tooltip-z-index:       var(--z-50);
  --tooltip-arrow-size:    6px;
  --tooltip-duration:      var(--duration-150);
}
```

### 4.7 Navigation 组件 Token

```css
:root {
  --nav-bg:                var(--background);
  --nav-foreground:        var(--foreground);
  --nav-border:            var(--border);
  --nav-height:            64px;
  --nav-padding-x:         var(--space-4);
  --nav-item-padding-x:    var(--space-3);
  --nav-item-padding-y:    var(--space-2);
  --nav-item-radius:       var(--radius-md);
  --nav-item-hover-bg:     var(--accent);
  --nav-item-active-bg:    var(--accent);
  --nav-item-active-foreground: var(--primary);
  --nav-item-font-size:    var(--font-size-sm);
  --nav-item-font-weight:  var(--font-weight-medium);
  --nav-z-index:           var(--z-40);
}
```

---

## 五、CSS 变量代码模板

### 5.1 完整 Design Token CSS 模板

```css
/* ============================================
   Design Token System
   版本: 1.0.0
   生成时间: 2024
   ============================================ */

/* ---- 第1层：原始 Token ---- */
:root {
  /* 颜色 - 灰度 */
  --gray-0:   #ffffff;
  --gray-50:  #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --gray-950: #030712;
  
  /* 颜色 - 主色（蓝色） */
  --blue-50:  #eff6ff;
  --blue-100: #dbeafe;
  --blue-200: #bfdbfe;
  --blue-300: #93c5fd;
  --blue-400: #60a5fa;
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --blue-700: #1d4ed8;
  --blue-800: #1e40af;
  --blue-900: #1e3a8a;
  --blue-950: #172554;
  
  /* 间距 */
  --space-0:   0px;
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-16:  64px;
  
  /* 字号 */
  --font-size-xs:   0.75rem;
  --font-size-sm:   0.875rem;
  --font-size-base: 1rem;
  --font-size-lg:   1.125rem;
  --font-size-xl:   1.25rem;
  --font-size-2xl:  1.5rem;
  --font-size-3xl:  1.875rem;
  --font-size-4xl:  2.25rem;
  
  /* 圆角 */
  --radius-none: 0px;
  --radius-sm:   2px;
  --radius:      4px;
  --radius-md:   6px;
  --radius-lg:   8px;
  --radius-xl:   12px;
  --radius-2xl:  16px;
  --radius-3xl:  24px;
  --radius-full: 9999px;
  
  /* 阴影 */
  --shadow-xs:  0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm:  0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow:     0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-md:  0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-lg:  0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-xl:  0 25px 50px -12px rgb(0 0 0 / 0.25);
  
  /* 动画 */
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ---- 第2层：语义 Token（亮色模式） ---- */
:root {
  --background:         var(--gray-0);
  --foreground:         var(--gray-950);
  --primary:            var(--blue-600);
  --primary-hover:      var(--blue-700);
  --primary-foreground: var(--gray-0);
  --secondary:          var(--gray-100);
  --secondary-hover:    var(--gray-200);
  --secondary-foreground: var(--gray-900);
  --accent:             var(--blue-100);
  --accent-hover:       var(--blue-200);
  --accent-foreground:  var(--blue-900);
  --destructive:        var(--red-600);
  --destructive-hover:  var(--red-700);
  --destructive-foreground: var(--gray-0);
  --success:            var(--green-600);
  --success-hover:      var(--green-700);
  --success-foreground: var(--gray-0);
  --warning:            var(--yellow-500);
  --warning-hover:      var(--yellow-600);
  --warning-foreground: var(--gray-950);
  --info:               var(--blue-500);
  --info-hover:         var(--blue-600);
  --info-foreground:    var(--gray-0);
  --card:               var(--gray-0);
  --card-foreground:    var(--gray-950);
  --popover:            var(--gray-0);
  --popover-foreground: var(--gray-950);
  --border:             var(--gray-200);
  --border-hover:       var(--gray-300);
  --input:              var(--gray-200);
  --input-hover:        var(--gray-300);
  --ring:               var(--blue-500);
  --muted:              var(--gray-100);
  --muted-foreground:   var(--gray-500);
}

/* ---- 第2层：语义 Token（暗色模式） ---- */
.dark {
  --background:         var(--gray-950);
  --foreground:         var(--gray-50);
  --primary:            var(--blue-500);
  --primary-hover:      var(--blue-400);
  --primary-foreground: var(--gray-950);
  --secondary:          var(--gray-800);
  --secondary-hover:    var(--gray-700);
  --secondary-foreground: var(--gray-50);
  --accent:             var(--gray-800);
  --accent-hover:       var(--gray-700);
  --accent-foreground:  var(--gray-50);
  --destructive:        var(--red-500);
  --destructive-hover:  var(--red-400);
  --destructive-foreground: var(--gray-950);
  --success:            var(--green-500);
  --success-hover:      var(--green-400);
  --success-foreground: var(--gray-950);
  --warning:            var(--yellow-500);
  --warning-hover:      var(--yellow-400);
  --warning-foreground: var(--gray-950);
  --info:               var(--blue-400);
  --info-hover:         var(--blue-300);
  --info-foreground:    var(--gray-950);
  --card:               var(--gray-900);
  --card-foreground:    var(--gray-50);
  --popover:            var(--gray-900);
  --popover-foreground: var(--gray-50);
  --border:             var(--gray-800);
  --border-hover:       var(--gray-700);
  --input:              var(--gray-800);
  --input-hover:        var(--gray-700);
  --ring:               var(--blue-400);
  --muted:              var(--gray-800);
  --muted-foreground:   var(--gray-400);
}
```

---

## 六、暗色模式适配规则

### 6.1 自动检测 + 手动切换

```css
/* 方式1：跟随系统偏好 */
@media (prefers-color-scheme: dark) {
  :root { /* 暗色语义Token */ }
}

/* 方式2：class 切换（推荐） */
.dark { /* 暗色语义Token */ }

/* 方式3：data 属性切换 */
[data-theme="dark"] { /* 暗色语义Token */ }
```

### 6.2 JavaScript 主题切换

```javascript
// 主题管理器
const themeManager = {
  // 获取用户偏好
  getTheme() {
    const stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  },
  
  // 设置主题
  setTheme(theme) {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    localStorage.setItem('theme', theme);
  },
  
  // 切换主题
  toggle() {
    const current = this.getTheme();
    this.setTheme(current === 'dark' ? 'light' : 'dark');
  },
  
  // 监听系统偏好变化
  watchSystem() {
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
          this.setTheme(e.matches ? 'dark' : 'light');
        }
      });
  },
  
  // 初始化
  init() {
    this.setTheme(this.getTheme());
    this.watchSystem();
  }
};

// 防止闪烁：在 <head> 中内联
// <script>
//   (function() {
//     const theme = localStorage.getItem('theme') || 
//       (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
//     document.documentElement.classList.add(theme);
//   })();
// </script>
```

### 6.3 暗色模式设计原则

1. **不要简单反转**: 暗色模式不是亮色的反色，需要重新调整色彩
2. **降低背景纯度**: 纯黑(#000)过于刺眼，使用 #0a0a0a ~ #1a1a2e
3. **提高文字亮度**: 使用 #f5f5f5 ~ #fafafa 而非纯白
4. **降低色彩饱和度**: 暗色背景下高饱和度颜色过于刺眼
5. **阴影调整**: 暗色模式下阴影效果减弱，使用更微妙的阴影
6. **图片和图标**: 考虑降低亮度和对比度，或提供暗色版本
7. **边框可见性**: 暗色模式下边框需要更亮才能被感知

---

## 七、OKLCH 格式说明

### 7.1 OKLCH 简介

OKLCH 是一种感知均匀的色彩空间，优于 HSL 和 RGB：
- **O (Lightness)**: 感知亮度 0-1
- **K (Chroma)**: 色彩饱和度 0-0.4+
- **H (Hue)**: 色相角度 0-360

### 7.2 OKLCH 的优势

1. **感知均匀**: 相同的亮度值变化，人眼感知一致
2. **更好的渐变**: 避免HSL渐变中的灰色中间值
3. **精确的色彩调整**: 调整亮度不影响色相
4. **更广的色域**: 支持P3等广色域显示器

### 7.3 常用颜色的 OKLCH 值

```css
/* 蓝色色阶 - OKLCH */
--blue-50:  oklch(0.97 0.01 260);
--blue-100: oklch(0.93 0.03 260);
--blue-200: oklch(0.87 0.06 260);
--blue-300: oklch(0.79 0.10 260);
--blue-400: oklch(0.70 0.15 260);
--blue-500: oklch(0.62 0.19 260);
--blue-600: oklch(0.55 0.20 260);
--blue-700: oklch(0.49 0.20 260);
--blue-800: oklch(0.42 0.18 260);
--blue-900: oklch(0.35 0.16 260);
--blue-950: oklch(0.28 0.12 260);

/* 灰度色阶 - OKLCH */
--gray-50:  oklch(0.97 0.00 0);
--gray-100: oklch(0.93 0.00 0);
--gray-200: oklch(0.87 0.00 0);
--gray-300: oklch(0.78 0.00 0);
--gray-400: oklch(0.68 0.00 0);
--gray-500: oklch(0.58 0.00 0);
--gray-600: oklch(0.48 0.00 0);
--gray-700: oklch(0.40 0.00 0);
--gray-800: oklch(0.30 0.00 0);
--gray-900: oklch(0.22 0.00 0);
--gray-950: oklch(0.15 0.00 0);
```

### 7.4 OKLCH 色相参考

```css
/* 色相角度参考 */
--hue-red:    25;
--hue-orange: 55;
--hue-yellow: 90;
--hue-green:  155;
--hue-cyan:   195;
--hue-blue:   260;
--hue-purple: 295;
--hue-pink:   335;
```

### 7.5 OKLCH 渐变生成

```css
/* 使用OKLCH创建感知均匀的渐变 */
.gradient-blue-purple {
  background: linear-gradient(
    to right,
    oklch(0.6 0.2 260),  /* 蓝色 */
    oklch(0.6 0.2 295)   /* 紫色 */
  );
}

/* 保持亮度不变的色相旋转渐变 */
.gradient-rainbow {
  background: linear-gradient(
    to right,
    oklch(0.7 0.15 25),   /* 红 */
    oklch(0.7 0.15 90),   /* 黄 */
    oklch(0.7 0.15 155),  /* 绿 */
    oklch(0.7 0.15 260),  /* 蓝 */
    oklch(0.7 0.15 335)   /* 粉 */
  );
}
```

---

## 八、Tailwind CSS 集成指南

### 8.1 tailwind.config.js 配置

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      // 颜色映射到语义Token
      colors: {
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        primary: {
          DEFAULT: 'var(--primary)',
          hover: 'var(--primary-hover)',
          foreground: 'var(--primary-foreground)',
        },
        secondary: {
          DEFAULT: 'var(--secondary)',
          hover: 'var(--secondary-hover)',
          foreground: 'var(--secondary-foreground)',
        },
        destructive: {
          DEFAULT: 'var(--destructive)',
          hover: 'var(--destructive-hover)',
          foreground: 'var(--destructive-foreground)',
        },
        success: {
          DEFAULT: 'var(--success)',
          hover: 'var(--success-hover)',
          foreground: 'var(--success-foreground)',
        },
        warning: {
          DEFAULT: 'var(--warning)',
          hover: 'var(--warning-hover)',
          foreground: 'var(--warning-foreground)',
        },
        info: {
          DEFAULT: 'var(--info)',
          hover: 'var(--info-hover)',
          foreground: 'var(--info-foreground)',
        },
        muted: {
          DEFAULT: 'var(--muted)',
          foreground: 'var(--muted-foreground)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          hover: 'var(--accent-hover)',
          foreground: 'var(--accent-foreground)',
        },
        card: {
          DEFAULT: 'var(--card)',
          foreground: 'var(--card-foreground)',
        },
        popover: {
          DEFAULT: 'var(--popover)',
          foreground: 'var(--popover-foreground)',
        },
      },
      
      // 圆角映射
      borderRadius: {
        lg: 'var(--radius-lg)',
        md: 'var(--radius-md)',
        sm: 'var(--radius)',
      },
      
      // 字号映射
      fontSize: {
        xs: ['var(--font-size-xs)', { lineHeight: 'var(--line-height-normal)' }],
        sm: ['var(--font-size-sm)', { lineHeight: 'var(--line-height-normal)' }],
        base: ['var(--font-size-base)', { lineHeight: 'var(--line-height-relaxed)' }],
        lg: ['var(--font-size-lg)', { lineHeight: 'var(--line-height-relaxed)' }],
        xl: ['var(--font-size-xl)', { lineHeight: 'var(--line-height-normal)' }],
        '2xl': ['var(--font-size-2xl)', { lineHeight: 'var(--line-height-tight)' }],
        '3xl': ['var(--font-size-3xl)', { lineHeight: 'var(--line-height-tight)' }],
        '4xl': ['var(--font-size-4xl)', { lineHeight: 'var(--line-height-none)' }],
      },
      
      // 间距映射
      spacing: {
        '0.5': 'var(--space-0-5)',
        '1': 'var(--space-1)',
        '1.5': 'var(--space-1-5)',
        '2': 'var(--space-2)',
        '2.5': 'var(--space-2-5)',
        '3': 'var(--space-3)',
        '3.5': 'var(--space-3-5)',
        '4': 'var(--space-4)',
        '5': 'var(--space-5)',
        '6': 'var(--space-6)',
        '7': 'var(--space-7)',
        '8': 'var(--space-8)',
        '9': 'var(--space-9)',
        '10': 'var(--space-10)',
        '12': 'var(--space-12)',
        '16': 'var(--space-16)',
        '20': 'var(--space-20)',
        '24': 'var(--space-24)',
      },
      
      // 阴影映射
      boxShadow: {
        sm: 'var(--shadow-sm)',
        DEFAULT: 'var(--shadow)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
      },
      
      // 动画映射
      transitionDuration: {
        DEFAULT: 'var(--duration-150)',
        '150': 'var(--duration-150)',
        '200': 'var(--duration-200)',
        '300': 'var(--duration-300)',
      },
      
      // 关键帧
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
```

### 8.2 全局 CSS 入口

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* 导入Design Token */
  :root {
    /* 原始Token + 语义Token（见上文完整定义） */
  }
  
  .dark {
    /* 暗色语义Token（见上文完整定义） */
  }
  
  /* 基础样式 */
  * {
    border-color: var(--border);
  }
  
  body {
    background-color: var(--background);
    color: var(--foreground);
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}
```

### 8.3 组件使用示例

```tsx
// Button 组件使用 Design Token
function Button({ variant = 'default', size = 'default', children }) {
  const variants = {
    default: 'bg-primary text-primary-foreground hover:bg-primary-hover shadow-sm',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary-hover',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive-hover',
    outline: 'border border-border bg-transparent hover:bg-accent text-foreground',
    ghost: 'hover:bg-accent text-foreground',
  };
  
  const sizes = {
    default: 'h-10 px-4 py-2',
    sm: 'h-8 px-3 text-xs',
    lg: 'h-12 px-6 text-base',
  };
  
  return (
    <button className={`
      inline-flex items-center justify-center rounded-md
      font-medium transition-colors duration-150
      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
      disabled:pointer-events-none disabled:opacity-50
      ${variants[variant]} ${sizes[size]}
    `}>
      {children}
    </button>
  );
}
```

### 8.4 CSS 变量与 Tailwind 工具类对照表

| CSS 变量 | Tailwind 类 | 说明 |
|---------|------------|------|
| `var(--background)` | `bg-background` | 页面背景 |
| `var(--foreground)` | `text-foreground` | 主要文字 |
| `var(--primary)` | `bg-primary` / `text-primary` | 主色 |
| `var(--primary-hover)` | `hover:bg-primary-hover` | 主色悬停 |
| `var(--secondary)` | `bg-secondary` | 次要背景 |
| `var(--accent)` | `bg-accent` | 强调背景 |
| `var(--destructive)` | `bg-destructive` | 危险色 |
| `var(--success)` | `bg-success` | 成功色 |
| `var(--warning)` | `bg-warning` | 警告色 |
| `var(--muted)` | `bg-muted` | 静音背景 |
| `var(--muted-foreground)` | `text-muted-foreground` | 静音文字 |
| `var(--border)` | `border-border` | 边框色 |
| `var(--ring)` | `ring-ring` | 焦点环色 |
| `var(--card)` | `bg-card` | 卡片背景 |
| `var(--radius-md)` | `rounded-md` | 中等圆角 |
| `var(--shadow)` | `shadow` | 默认阴影 |
| `var(--space-4)` | `p-4` / `m-4` | 16px间距 |

---

## 附录：Token 命名规范

### 命名格式
```
--{类别}-{属性}-{变体}-{状态}
```

### 示例
```
--color-blue-500           # 类别-属性-变体
--space-4                  # 类别-变体
--font-size-lg             # 类别-属性-变体
--button-bg-hover          # 组件-属性-状态
--card-shadow              # 组件-属性
--input-border-focus       # 组件-属性-状态
```

### 状态关键词
- `hover` - 悬停
- `focus` - 聚焦
- `active` - 激活/按下
- `disabled` - 禁用
- `visited` - 已访问
- `checked` - 选中
- `error` / `invalid` - 错误
- `loading` - 加载中

### 尺寸关键词
- `xs` - 超小
- `sm` - 小
- `md` / `default` - 中等/默认
- `lg` - 大
- `xl` - 超大
- `2xl` - 特大

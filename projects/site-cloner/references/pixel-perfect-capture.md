# ★像素级保真指南 — CSS/字体/交互/设计Token 全量捕获

## 概述

v1.1.0 新增的像素级保真能力，确保复刻后的网站在视觉和交互上与原始网站无法区分。本文档详细说明各项捕获策略和技术细节。

---

## 1. CSS 完整提取

### 1.1 CSS 自定义属性（Custom Properties）

通过 `getComputedStyle(document.documentElement)` 遍历所有 CSS 属性，提取以 `--` 开头的自定义属性：

```javascript
const rootStyles = getComputedStyle(document.documentElement);
for (let i = 0; i < rootStyles.length; i++) {
    const name = rootStyles[i];
    if (name.startsWith('--')) {
        props[name] = rootStyles.getPropertyValue(name).trim();
    }
}
```

**为什么重要：** 现代 CSS 框架（Tailwind、Bootstrap 5、Material UI）大量使用 CSS 变量定义颜色、间距、圆角、阴影等设计 Token。丢失 CSS 变量意味着丢失整个设计系统。

**响应式 CSS 变量：** 在不同视口宽度下重复捕获，因为某些变量通过媒体查询可能有不同值。

### 1.2 @keyframes 动画关键帧

遍历所有 `document.styleSheets`，提取 `CSSRule.KEYFRAMES_RULE` 类型的完整 CSS 文本：

```javascript
for (let sheet of document.styleSheets) {
    for (let rule of sheet.cssRules) {
        if (rule.type === CSSRule.KEYFRAMES_RULE) {
            keyframes.push({ name: rule.name, css: rule.cssText });
        }
    }
}
```

**注意事项：** 跨域样式表的 `cssRules` 可能无法访问。此时需要额外下载 CSS 文件后解析。

**重建策略：** 将所有提取的 @keyframes 写入独立的 `animations.css` 文件。

### 1.3 @font-face 声明

同样遍历 `document.styleSheets`，提取完整的 `@font-face` 规则：

```javascript
if (rule.type === CSSRule.FONT_FACE_RULE) {
    fontFaces.push({
        family: rule.style.fontFamily,
        src: rule.style.src,
        css: rule.cssText
    });
}
```

**重建策略：** 将 @font-face 中的外部字体 URL 替换为下载到本地的字体文件路径。

### 1.4 @media 媒体查询

提取所有媒体查询规则，确保响应式设计完整保留：

```javascript
if (rule.type === CSSRule.MEDIA_RULE) {
    mediaQueries.push({ condition: rule.conditionText, css: rule.cssText });
}
```

### 1.5 伪类样式（:hover/:focus/:active）

伪类样式在 `document.styleSheets` 的规则中天然存在，通过提取 `allCssRules` 保留。特别注意：

- **:hover 态** → 按钮/链接/卡片的悬停效果
- **:focus 态** → 输入框聚焦的边框、阴影变化
- **:active 态** → 按钮按下的状态
- **:visited 态** → 已访问链接的颜色
- **::before / ::after** → 伪元素装饰

---

## 2. 字体完整捕获

### 2.1 页面使用的字体族

```javascript
for (el of document.querySelectorAll('*')) {
    const family = getComputedStyle(el).fontFamily;
    fonts.add(family);
}
```

### 2.2 Google Fonts

识别并下载 Google Fonts 的 CSS 链接：
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap">
```

然后解析 Google Fonts 返回的 CSS（其中包含 @font-face 和字体文件 URL），下载字体文件到本地。

### 2.3 @font-face 字体文件

从 @font-face 的 `src: url(...)` 提取字体文件 URL，下载到 `fonts/` 目录：

```
fonts/
├── Inter-Regular.woff2
├── Inter-SemiBold.woff2
├── PlayfairDisplay-Bold.woff2
└── ...
```

### 2.4 字体回退链

保留完整的 `font-family` 回退链：
```
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### 2.5 iconfont/图标字体

识别 iconfont CSS（如 `@font-face { font-family: 'iconfont'; ... }`），下载对应的图标字体文件。

---

## 3. 交互行为记录

### 3.1 表单校验

```javascript
Array.from(document.querySelectorAll('form')).map(form => ({
    action: form.action,
    method: form.method,
    inputs: Array.from(form.querySelectorAll('input, select, textarea')).map(el => ({
        name: el.name,
        type: el.type,
        required: el.required,
        placeholder: el.placeholder,
        pattern: el.pattern,
        min: el.min,
        max: el.max,
        minLength: el.minLength,
        maxLength: el.maxLength
    }))
}))
```

### 3.2 动效元素

扫描所有元素的 `transition`、`transform`、`animation` 计算样式，识别有动效的元素：

- transition 的默认值是 `all 0s ease 0s`，非默认值说明有动效
- animation 的默认值是 `none 0s ease 0s 1 normal none running`

### 3.3 内联事件处理器

通过 `on*` 属性识别内联事件：
- `onclick` — 点击处理
- `onsubmit` — 表单提交
- `onchange` / `oninput` — 输入变化
- `onfocus` / `onblur` — 焦点事件
- `onmouseenter` / `onmouseleave` — 鼠标悬停
- `onkeydown` / `onkeyup` — 键盘事件

**注意：** `addEventListener` 动态绑定的监听器无法从 DOM 直接获取，但可以通过以下方式推断：
- 按钮的 `type="submit"` 或表单的 `action` 暗含提交行为
- 有 `href="#"` 或 `role="button"` 的元素暗含点击行为
- 下拉菜单的父级 `.dropdown` 类暗含 toggle 行为

---

## 4. 设计 Token 提取

### 4.1 颜色体系

扫描前 1000 个元素的计算样式，从以下 CSS 属性提取颜色：
- `color`（文字色）
- `backgroundColor`（背景色）
- `borderColor` / `borderTopColor` / `borderBottomColor`（边框色）
- `outlineColor`（轮廓色）
- `textDecorationColor`（下划线色）
- `caretColor`（光标色）

过滤条件：排除 `rgba(0,0,0,0)`（透明）和 `transparent`，排除纯黑（`rgb(0,0,0)`）。

### 4.2 排版层级

扫描 `h1-h6, p, span, a, li, div, button, label, input`，按 `fontFamily|fontSize|fontWeight` 去重分组。

提取属性：
- `font-family`（字体族）
- `font-size`（字号）
- `font-weight`（字重 100-900）
- `line-height`（行高）
- `letter-spacing`（字间距）
- `text-transform`（大小写转换）

### 4.3 间距节奏

扫描 `section, .section, .container, .wrapper, nav, header, footer` 等结构元素，提取 `padding` 和 `margin` 值。

**作用：** 知道网站的间距节奏后，可以在重建时使用相同的间距值。

### 4.4 阴影体系

扫描前 1000 个元素的 `box-shadow` 计算样式，去重收集。

常见的阴影层级：
```
0: none
1: 0 1px 2px rgba(0,0,0,0.05)    # 微小阴影
2: 0 4px 6px rgba(0,0,0,0.07)    # 卡片阴影
3: 0 10px 25px rgba(0,0,0,0.1)   # 模态框阴影
4: 0 20px 50px rgba(0,0,0,0.15)  # 最高层阴影
```

### 4.5 圆角体系

扫描前 1000 个元素的 `border-radius` 计算样式，去重收集。

常见圆角层级：
```
0: 0px (直角)
1: 4px (小圆角，按钮/输入框)
2: 8px (中小圆角，卡片)
3: 12px (大圆角，模态框)
4: 16px (特大圆角)
5: 9999px (全圆/胶囊)
```

---

## 5. 响应式保真

### 5.1 多视口捕获

在以下标准视口宽度下重复捕获：
- 1920px（桌面全宽）
- 1440px（桌面常规）
- 1024px（平板横屏）
- 768px（平板竖屏）
- 375px（手机）

### 5.2 媒体查询保留

确保所有 `@media` 规则完整提取，特别是：
- `@media (max-width: 768px)` — 移动端断点
- `@media (prefers-color-scheme: dark)` — 暗色模式
- `@media (prefers-reduced-motion)` — 减弱动效

---

## 6. 常见遗漏与补全

| 遗漏项 | 原因 | 解决方法 |
|--------|------|----------|
| CSS-in-JS 注入的 style 标签 | 动态生成的 style | 从 `document.styleSheets` 获取所有规则 |
| Tailwind 未使用的类 | JIT 模式只生成使用的类 | 从计算样式提取实际值 |
| CSS Module 的 hash 类名 | 原始类名不可用 | 从计算样式提取具体值，重建时用通用选择器 |
| SVG 内联样式 | SVG 内的 style 元素 | 单独遍历 SVG 元素 |
| canvas 渲染内容 | JS 绘制 | 截图保留（不可交互） |
| Shadow DOM 内容 | 封装隔离 | 穿透 shadowRoot 遍历 |

---

## 7. 保真度评分标准

| 评分 | 标准 |
|------|------|
| **A+ (100%)** | 色彩 ΔE<3、字体一致、字号一致、间距一致、动效一致、交互一致、响应式一致 |
| **A (95%+)** | 色彩准确、字体正确、布局一致 |
| **B (85%+)** | 基本布局正确，细微差异（如 line-height 微差） |
| **C (70%+)** | 大致可用，但样式有明显差异 |
| **D (<70%)** | 需要重新捕获 |

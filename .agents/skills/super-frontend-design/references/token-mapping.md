# Cross-Platform Design Token Mapping — 跨平台 Token 映射表

> 支持 Tailwind CSS、SwiftUI、Jetpack Compose、WinUI 3 等平台的设计 Token 输出。
> 遵循 DTCG（Design Token Community Group）规范。

---

## 1. DTCG 规范概述

Design Token 是用于表达设计决策的最小数据单元，具有平台无关性：

```json
{
  "token-name": {
    "value": "...",
    "description": "...",
    "$type": "color | length | duration | font | ...",
    "$extensions": {
      "com.apple.ios.class": "UIColor",
      "com.microsoft.compose.class": "Brush"
    }
  }
}
```

---

## 2. Token 三层架构

```
原始 Token（Primitive）   →   语义 Token（Semantic）   →   组件 Token（Component）
```

| 层级 | 命名 | 用途 | 示例 |
|------|------|------|------|
| Primitive | `--color-blue-500` | 基础值定义 | `#3b82f6` |
| Semantic | `--color-primary` | 设计意图表达 | `var(--color-blue-500)` |
| Component | `--button-bg` | 组件特定值 | `var(--color-primary)` |

---

## 3. 颜色 Token

### 3.1 语义颜色定义

```css
:root {
  /* === 品牌色 === */
  --color-primary: #0ea5e9;
  --color-primary-hover: #0284c7;
  --color-primary-active: #0369a1;
  --color-primary-muted: rgba(14, 165, 233, 0.1);

  /* === 中性色 === */
  --color-surface: #ffffff;
  --color-surface-raised: #f8fafc;
  --color-surface-overlay: #f1f5f9;
  --color-background: #fafafa;

  /* === 文字色 === */
  --color-on-surface: #0f172a;
  --color-on-surface-variant: #475569;
  --color-on-surface-muted: #94a3b8;

  /* === 功能色 === */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #3b82f6;

  /* === 边框 === */
  --color-border: #e2e8f0;
  --color-border-strong: #cbd5e1;
  --color-border-focus: var(--color-primary);
}
```

### 3.2 暗色模式

```css
:root.dark {
  --color-surface: #0f172a;
  --color-surface-raised: #1e293b;
  --color-surface-overlay: #334155;
  --color-background: #020617;

  --color-on-surface: #f8fafc;
  --color-on-surface-variant: #94a3b8;
  --color-on-surface-muted: #64748b;

  --color-border: #334155;
  --color-border-strong: #475569;
}
```

### 3.3 跨平台映射

| Token | CSS | SwiftUI | Compose | WinUI 3 |
|-------|-----|---------|---------|---------|
| primary | `var(--color-primary)` | `Color(.primary)` | `MaterialTheme.colorScheme.primary` | `ApplicationResources.PrimaryBrush` |
| surface | `var(--color-surface)` | `Color(.secondaryBackground)` | `MaterialTheme.colorScheme.surface` | `ApplicationResources.SurfaceBrush` |
| text | `var(--color-on-surface)` | `Color(.primary)` | `MaterialTheme.colorScheme.onSurface` | `ApplicationResources.TextPrimaryBrush` |
| success | `var(--color-success)` | `Color(.green)` | `MaterialTheme.colorScheme.success` | `ApplicationResources.SuccessBrush` |
| border | `var(--color-border)` | `Color(.separator)` | `MaterialTheme.colorScheme.outline` | `ApplicationResources.BorderBrush` |

---

## 4. 字体 Token

### 4.1 定义

```css
:root {
  /* === 字体族 === */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-display: 'Outfit', sans-serif;

  /* === 字号刻度 === */
  --font-xs: 0.75rem;     /* 12px */
  --font-sm: 0.875rem;    /* 14px */
  --font-base: 1rem;      /* 16px */
  --font-md: 1.125rem;    /* 18px */
  --font-lg: 1.25rem;     /* 20px */
  --font-xl: 1.5rem;      /* 24px */
  --font-2xl: 1.875rem;   /* 30px */
  --font-3xl: 2.25rem;    /* 36px */
  --font-4xl: 3rem;       /* 48px */

  /* === 字重 === */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* === 行高 === */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

### 4.2 跨平台映射

| Token | CSS | SwiftUI | Compose | WinUI 3 |
|-------|-----|---------|---------|---------|
| font-sans | `var(--font-sans)` | `.font(.system())` | `MaterialTheme.typography.bodyMedium.fontFamily` | `ApplicationResources.TextPrimaryFontFamily` |
| font-lg | `var(--font-lg)` | `.font(.title2)` | `MaterialTheme.typography.titleMedium` | `ApplicationResources.TextTitleFont` |
| font-weight-bold | `var(--font-weight-bold)` | `.fontWeight(.bold)` | `FontWeight.Bold` | `ApplicationResources.TextBoldWeight` |

---

## 5. 间距 Token

### 5.1 定义

```css
:root {
  --space-xs: 0.25rem;    /* 4px */
  --space-sm: 0.5rem;     /* 8px */
  --space-md: 1rem;       /* 16px */
  --space-lg: 1.5rem;     /* 24px */
  --space-xl: 2rem;       /* 32px */
  --space-2xl: 3rem;      /* 48px */
  --space-3xl: 4rem;      /* 64px */
  --space-4xl: 6rem;      /* 96px */
}
```

### 5.2 跨平台映射

| Token | CSS | SwiftUI | Compose | WinUI 3 |
|-------|-----|---------|---------|---------|
| space-md | `var(--space-md)` | `.padding(16)` | `MaterialTheme.spacing.spaceMd` | `ApplicationResources.ControlMargin` |
| space-lg | `var(--space-lg)` | `.padding(24)` | `MaterialTheme.spacing.spaceLg` | `ApplicationResources.ControlHorizontalMargin` |

---

## 6. 圆角 Token

```css
:root {
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */
  --radius-xl: 1rem;      /* 16px */
  --radius-full: 9999px;
}
```

---

## 7. 阴影 Token

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1);
}
```

---

## 8. 动效 Token

```css
:root {
  /* === 时长 === */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;

  /* === 缓动 === */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 9. 完整 Token 文件输出格式

### 9.1 CSS 输出（默认）

```css
/* 03-design-tokens.css */
:root {
  /* Colors */
  --color-primary: #0ea5e9;
  --color-surface: #ffffff;
  --color-background: #fafafa;
  --color-on-surface: #0f172a;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --space-md: 1rem;
  --space-lg: 1.5rem;

  /* Radius */
  --radius-md: 0.5rem;

  /* Shadow */
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);

  /* Motion */
  --duration-normal: 250ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 9.2 JSON 输出（DTCG）

```json
{
  "color": {
    "primary": {
      "value": "#0ea5e9",
      "type": "color",
      "description": "主品牌色"
    },
    "surface": {
      "value": "#ffffff",
      "type": "color",
      "description": "表面色"
    }
  },
  "font": {
    "sans": {
      "value": "Inter, system-ui, sans-serif",
      "type": "fontFamily",
      "description": "无衬线字体"
    }
  },
  "space": {
    "md": {
      "value": "1rem",
      "type": "dimension",
      "description": "中等间距"
    }
  }
}
```

---

## 10. 平台特定 Token 输出

### 10.1 Tailwind CSS v4

```css
@theme {
  --color-primary: #0ea5e9;
  --color-surface: #ffffff;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-md: 0.5rem;
}
```

### 10.2 SwiftUI

```swift
// ColorExtensions.swift
extension Color {
  static let primary = Color(.sRGB, red: 0.055, green: 0.647, blue: 0.914)
  static let surface = Color(.white)
  static let background = Color(.systemBackground)
}

// FontExtensions.swift
extension Font {
  static let body = Font.system(size: 17, weight: .regular)
  static let title = Font.system(size: 28, weight: .bold)
}
```

### 10.3 Jetpack Compose

```kotlin
// Color.kt
val PrimaryColor = Color(0xFF0EA5E9)
val SurfaceColor = Color(0xFFFFFFFF)
val BackgroundColor = Color(0xFFFAFAFA)

// Type.kt
val Typography = Typography(
  bodyMedium = TextStyle(
    fontFamily = FontFamily.SansSerif,
    fontSize = 16.sp
  )
)
```

### 10.4 WinUI 3

```xaml
<!-- App.xaml -->
<ResourceDictionary>
  <Color x:Key="PrimaryColor">#0EA5E9</Color>
  <Color x:Key="SurfaceColor">#FFFFFF</Color>
  <Brush x:Key="PrimaryBrush">{StaticResource PrimaryColor}</Brush>
</ResourceDictionary>
```

---

## 11. Token 使用规则

1. **永远使用语义 Token**，不使用原始 hex 值
2. **语义 Token 优先于组件 Token**，便于主题切换
3. **暗色模式通过覆盖语义 Token 实现**，不单独定义暗色值
4. **Token 文件应随项目持久化**，不在每次设计时重新生成
5. **跨平台映射时保持一致性**，确保颜色/尺寸/字体在各平台等效

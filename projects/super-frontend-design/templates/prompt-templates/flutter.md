# Flutter Prompt 模板

> Flutter 移动端/桌面端组件生成模板。
> 设计约束同 react-tailwind.md，适配 Material Design 3 + Design Token。

---

## Block: {Block 类型}

```
生成一个 Flutter (Dart) 的 {Block 类型名称} 组件。

**框架约定**：
- Flutter 3.22+
- Material 3 主题
- Dart 3.4+
- 使用 StatelessWidget / StatefulWidget
- 状态管理: Provider / Riverpod（根据项目）
- 图标: flutter_svg (SVG) 或 Material Icons

**全局约束**：
- 配色: 将 DESIGN.md CSS 变量映射为 Material ColorScheme
- 字体: Google Fonts 匹配 Design Brief 选定字体
- 暗色模式: ThemeData.dark() 对应 [data-theme="dark"]
- 品牌人格: 对应 Material 3 的 style strategy

**排版约束**：
- ALL CAPS 元素 letterSpacing ≥ 0.08em
- Display 文字 (≥48px) letterSpacing: -0.02em
- Body 文字 height 属性 ≥ 1.5
- 恰好 3 个 fontWeight (w400 / w500 / w600)

**动效**：
- {动效描述，来自视觉论文 motion-direction}
- 使用 AnimatedContainer / AnimatedOpacity / AnimationController
- respectsReduceMotion: true

**禁止**：见 react-tailwind.md 全局禁止列表（7 反 AI 规则全相同）
```

---

## 核心组件模板

### Material ColorScheme 映射

```dart
final colorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF{primary-hex}),          // var(--color-primary)
  onPrimary: Colors.white,
  surface: Color(0xFF{surface-hex}),          // var(--color-surface)
  onSurface: Color(0xFF{text-hex}),           // var(--color-text)
  error: Color(0xFF{error-hex}),              // var(--color-error)
  outline: Color(0xFF{border-hex}),           // var(--color-border)
);
```

### 按钮 (Flutter)

```
生成 Flutter 按钮组件：
- 类型: ElevatedButton / OutlinedButton / TextButton
- 圆角: BorderRadius.circular(8)
- elevation: 0（扁平设计）
- padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8)
- textStyle: fontWeight w600, letterSpacing 0.02em
- 动效: onPressed → transform scale(0.98)
- 禁止: elevation > 2
```

### 卡片 (Flutter)

```
生成 Flutter 卡片组件：
- 背景: ColorScheme.surface
- 边框: Border.all(color: ColorScheme.outline, width: 1)
- 圆角: 8px
- 禁止: elevation (使用 border 而非阴影)
- 禁止: 圆角 + 彩色左边框组合
```

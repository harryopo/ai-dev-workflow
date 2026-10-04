# Flutter Prompt 模板

> Flutter 移动端/桌面端组件生成模板。
> 设计约束参考 react-tailwind.md，适配 Material Design 3 + Design Token。
> **v2.4.0 规范**: 严格遵循 references/premium-design-rules.md 的16条规则（含斜体标题禁令/侧边条纹禁令/LCP优化/间距4px纪律）、hallmark 21种Macrostructure路由、hallmark 56条Slop Test检查（Flutter适配版）。

---

## Block: {Block 类型}

```
生成一个 Flutter (Dart) 的 {Block 类型名称} 组件。

**框架约定**：
- Flutter 3.22+
- Material 3 主题（必须）
- Dart 3.4+
- 使用 StatelessWidget / StatefulWidget / ConsumerWidget
- 状态管理: Provider / Riverpod（根据项目）
- 图标: flutter_svg (SVG) 或 Material Icons
- 动画库:
  - 首选: Flutter 内置动画（AnimatedContainer / AnimatedOpacity / AnimationController + SpringSimulation）
  - 备选: flutter_animate 包（声明式动画）
  - ❌ 不使用 Framer Motion（Flutter 不支持）
- 使用 MediaQuery 或 LayoutBuilder 做响应式
- 响应式字号: 用 MediaQuery.textScaler 或自定义扩展方法实现类似 clamp() 效果
  - 不支持 CSS clamp()，用响应式计算替代
  - Display: 32-48（根据屏幕宽度缩放）
  - H1: 28-36
  - H2: 22-28
  - H3: 18-22
  - Body: 16（移动端正文不小于16）

**全局约束**：
- 配色: 将 DESIGN.md CSS 变量映射为 Material ColorScheme
- 字体: Google Fonts 匹配 Design Brief 选定字体
- 暗色模式: ThemeData.dark() 对应 [data-theme="dark"]，使用 brightness
- 品牌人格: 对应 Material 3 的 style strategy（Feather / Glance / Surfaces）

**排版约束（Flutter/Material 3 适配）**：
- 使用 TextTheme 定义字号阶：
  ```dart
  TextTheme(
    displayLarge: TextStyle(fontSize: responsiveFont(56), fontWeight: FontWeight.w500, letterSpacing: -1),
    displayMedium: TextStyle(fontSize: responsiveFont(45), fontWeight: FontWeight.w500, letterSpacing: -0.5),
    headlineLarge: TextStyle(fontSize: responsiveFont(36), fontWeight: FontWeight.w500, letterSpacing: -0.5),
    headlineMedium: TextStyle(fontSize: responsiveFont(28), fontWeight: FontWeight.w500, letterSpacing: -0.25),
    headlineSmall: TextStyle(fontSize: responsiveFont(24), fontWeight: FontWeight.w600),
    titleLarge: TextStyle(fontSize: responsiveFont(22), fontWeight: FontWeight.w600),
    bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400, height: 1.6),
    bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w400, height: 1.5),
    labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, letterSpacing: 0.5),
  )
  ```
- Display/H1 字重: FontWeight.w500 (Medium) 或 w400 (Regular)
- H2/H3: FontWeight.w500 或 w600
- Button labels: FontWeight.w600 (Semibold)
- Body: FontWeight.w400 (Regular)
- 字间距（letterSpacing）：
  - Display: -0.5 到 -1.0
  - Headline: -0.25 到 -0.5
  - ALL CAPS/Label: 0.5 到 1.0
- 行高（height 属性）：
  - Display: 1.1
  - Headline: 1.2
  - Body: 1.5-1.6
- 恰好 3-4 个 fontWeight (w400 / w500 / w600)
- 正文最小 fontSize: 14（桌面）/16（移动端）

**动效（Flutter Spring 动画）**：
- {动效描述，来自视觉论文 motion-direction}
- 使用 SpringSimulation 物理动画，参数对应web：
  ```dart
  // Spring 描述（对应 web Motion spring 参数）
  final SpringDescription spring = SpringDescription(
    mass: 1,
    stiffness: 200, // 入场: 200, 过渡: 300, 微交互: 400
    damping: 25,
  );
  
  // 使用 AnimationController + SpringSimulation
  controller.animateWith(SpringSimulation(spring, 0, 1, 0));
  
  // 或用 Curves.easeOutCubic / Curves.easeOutQuart 作为备选
  ```
- 推荐参数：
  - 按钮点击: stiffness 400, damping 25
  - 卡片入场: stiffness 200, damping 25, 初始 offset 20
  - 模态框: stiffness 300, damping 25, scale 0.95→1
- Hover效果（桌面）: InkWell + Matrix4 缩放
- 触摸反馈（移动端）: InkWell + scale 动画，或 GestureDetector
- Stagger子元素: 使用 Interval 在 0.0-1.0 范围内分布
- 动画时长: 200-500ms（移动端比web稍快）
- 必须尊重 MediaQuery.disableAnimations 或 accessibleNavigation
- 优先动画 transform (Matrix4) 和 opacity（性能好）

**圆角规范（Material 3 适配）**：
- 按钮 (Button): BorderRadius.circular(12) — 8-12px 范围
- 输入框 (TextField): BorderRadius.circular(8-12)
- 卡片 (Card): BorderRadius.circular(16) — 12-16px 范围（Material 3 卡片圆角更大）
- 模态框 (BottomSheet/Dialog): BorderRadius.circular(20-28)
- 标签/徽章 (Chip): BorderRadius.circular(8) / StadiumBorder()
- 注意: Material 3 默认圆角比 web 稍大，这是允许的

**禁止**：
- ❌ Framer Motion 包（Flutter 不支持，用内置动画或 flutter_animate）
- ❌ 大标题使用 FontWeight.w700 (Bold) 或更重（w800/w900 绝对禁止）
- ❌ 所有页面/卡片统一内边距
- ❌ 默认 Material 阴影（elevation > 2 需谨慎，优先用边框）
- ❌ AI 经典渐变 (purple→blue / blue→cyan / indigo→pink / 蓝→紫→粉)
- ❌ hex #6366f1 #4f46e5 #4338ca #8b5cf6 #7c3aed
- ❌ emoji 图标 (✨🚀🎯⚡🔥💡🎨🛠️)（用 Material Icons / flutter_svg）
- ❌ 圆角卡片 + 彩色左边框组合
- ❌ 假指标 ("10× faster")
- ❌ 填充文案 (lorem ipsum)
- ❌ 完美对称布局
- ❌ 装饰性 blob/wave 背景
- ❌ 动画时长超过 600ms
- ❌ 动画非transform/opacity属性（如position/size，性能差）
- ❌ CSS clamp() 函数（Dart不支持，用MediaQuery计算）
- ❌ hover 效果在移动端实现
- ❌ 小于48x48的触摸目标

**参考**：
- Design Brief: output/design-system.md
- Premium Rules: references/premium-design-rules.md（Flutter适配）
- Material 3 规范: https://m3.material.io
- 参考源: Material 3 Demo · Flutter Gallery
```

---

## 核心组件模板

### Material ColorScheme 映射

```dart
import 'package:flutter/material.dart';

ColorScheme buildLightColorScheme() {
  return ColorScheme(
    brightness: Brightness.light,
    primary: Color(0xFF{primary-hex}),          // var(--color-primary)
    onPrimary: Colors.white,
    primaryContainer: Color(0xFF{primary-light-hex}),
    onPrimaryContainer: Color(0xFF{primary-dark-hex}),
    surface: Color(0xFF{surface-hex}),          // var(--color-surface)
    onSurface: Color(0xFF{text-hex}),           // var(--color-text)
    surfaceContainerHighest: Color(0xFF{surface-alt-hex}),
    onSurfaceVariant: Color(0xFF{text-secondary-hex}),
    error: Color(0xFF{error-hex}),              // var(--color-error)
    onError: Colors.white,
    outline: Color(0xFF{border-hex}),           // var(--color-border)
    outlineVariant: Color(0xFF{border-subtle-hex}),
    shadow: Colors.black.withValues(alpha: 0.05),
  );
}

ColorScheme buildDarkColorScheme() {
  return ColorScheme(
    brightness: Brightness.dark,
    primary: Color(0xFF{primary-hex-dark}),
    onPrimary: Color(0xFF{primary-dark-text}),
    surface: Color(0xFF{surface-dark}),
    onSurface: Color(0xFF{text-dark}),
    error: Color(0xFF{error-hex}),
    outline: Color(0xFF{border-dark}),
    shadow: Colors.black.withValues(alpha: 0.2),
  );
}
```

### 响应式字号工具

```dart
extension ResponsiveFont on num {
  double responsiveFont(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    // 类似 CSS clamp() 的效果: clamp(min, base * scale, max)
    final scale = screenWidth / 375; // 以 iPhone 14 为基准宽度
    final scaledValue = this * scale.clamp(0.8, 1.4);
    return scaledSize.toDouble();
  }
}

// 使用方式
Text(
  'Hello',
  style: TextStyle(fontSize: 32.responsiveFont(context)),
)
```

### 按钮 (Flutter + Spring 动画)

```dart
import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';

class PremiumButton extends StatefulWidget {
  final String label;
  final VoidCallback? onPressed;
  final ButtonVariant variant;
  final bool disabled;

  const PremiumButton({
    super.key,
    required this.label,
    this.onPressed,
    this.variant = ButtonVariant.primary,
    this.disabled = false,
  });

  @override
  State<PremiumButton> createState() => _PremiumButtonState();
}

class _PremiumButtonState extends State<PremiumButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
    );
    
    // Spring 动画: stiffness 400, damping 25 (对应 web)
    final spring = SpringDescription(
      mass: 1,
      stiffness: 400,
      damping: 25,
    );
    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.97).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleTapDown(TapDownDetails details) {
    if (!widget.disabled) {
      _controller.forward();
    }
  }

  void _handleTapUp(TapUpDetails details) {
    if (!widget.disabled) {
      _controller.reverse();
    }
  }

  void _handleTapCancel() {
    if (!widget.disabled) {
      _controller.reverse();
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    
    return GestureDetector(
      onTapDown: _handleTapDown,
      onTapUp: _handleTapUp,
      onTapCancel: _handleTapCancel,
      onTap: widget.disabled ? null : widget.onPressed,
      child: AnimatedBuilder(
        animation: _scaleAnimation,
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Container(
              constraints: const BoxConstraints(minHeight: 48),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              decoration: BoxDecoration(
                color: widget.variant == ButtonVariant.primary
                    ? colorScheme.primary
                    : widget.variant == ButtonVariant.secondary
                        ? Colors.transparent
                        : Colors.transparent,
                border: widget.variant == ButtonVariant.secondary
                    ? Border.all(color: colorScheme.outline, width: 1)
                    : null,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Center(
                child: Text(
                  widget.label,
                  style: TextStyle(
                    fontFamily: Theme.of(context).textTheme.labelLarge?.fontFamily,
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 0.5,
                    color: widget.variant == ButtonVariant.primary
                        ? colorScheme.onPrimary
                        : colorScheme.onSurface,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

enum ButtonVariant { primary, secondary, ghost }
```

### 卡片 (Flutter + Spring 入场动画)

```dart
import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';

class PremiumCard extends StatefulWidget {
  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry? padding;

  const PremiumCard({
    super.key,
    required this.child,
    this.onTap,
    this.padding,
  });

  @override
  State<PremiumCard> createState() => _PremiumCardState();
}

class _PremiumCardState extends State<PremiumCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _opacityAnimation;
  late Animation<Offset> _positionAnimation;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );

    // Spring 入场动画: stiffness 200, damping 25
    final spring = SpringDescription(
      mass: 1,
      stiffness: 200,
      damping: 25,
    );

    _opacityAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
    );
    _positionAnimation = Tween<Offset>(
      begin: const Offset(0, 20),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic));
    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.0).animate(_controller);

    // 入场动画
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _controller.forward();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleTapDown(TapDownDetails details) {
    if (widget.onTap != null) {
      final spring = SpringDescription(mass: 1, stiffness: 400, damping: 25);
      _scaleAnimation = Tween<double>(begin: 1.0, end: 0.98).animate(
        CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
      );
      setState(() {});
    }
  }

  void _handleTapUp(TapUpDetails details) {
    if (widget.onTap != null) {
      _scaleAnimation = Tween<double>(begin: 0.98, end: 1.0).animate(
        CurvedAnimation(parent: _controller, curve: Curves.easeOutCubic),
      );
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return GestureDetector(
      onTapDown: _handleTapDown,
      onTapUp: _handleTapUp,
      onTapCancel: _handleTapUp,
      onTap: widget.onTap,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Transform.translate(
            offset: _positionAnimation.value,
            child: Transform.scale(
              scale: _scaleAnimation.value,
              child: Opacity(
                opacity: _opacityAnimation.value,
                child: Container(
                  padding: widget.padding ?? const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: colorScheme.surface,
                    border: Border.all(color: colorScheme.outline, width: 1),
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: colorScheme.shadow,
                        blurRadius: 8,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: widget.child,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
```

### 表单 (Flutter)

```dart
生成 Flutter 表单组件：
- 标签: 上置，14px，color colorScheme.onSurfaceVariant，fontWeight w500
- 输入框 (TextField):
  - height: 48+
  - border: OutlineInputBorder with borderRadius 12
  - enabledBorder: colorScheme.outline
  - focusedBorder: colorScheme.primary, width 2
  - fontSize: 16（防止移动端缩放）
- 错误态: InputDecoration errorText + colorScheme.error
- 提交按钮: 全宽 48-52 PremiumButton
- 禁止: hintText 替代 labelText、过小点击区域
```

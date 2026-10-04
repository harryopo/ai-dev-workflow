# React Native + NativeWind Prompt 模板

> React Native 移动端组件生成模板。
> 设计约束参考 react-tailwind.md，适配移动端交互特性。
> **v2.4.0 规范**: 严格遵循 references/premium-design-rules.md 的16条规则（含斜体标题禁令/侧边条纹禁令/LCP优化/间距4px纪律）、hallmark 21种Macrostructure路由、hallmark 57条Slop Test检查（移动端适配版）。

---

## Block: {Block 类型}

```
生成一个 React Native + NativeWind 的 {Block 类型名称} 移动端组件。

**框架约定**：
- React Native 0.73+
- NativeWind 4+ (Tailwind CSS 运行时)
- Expo Router (路由)
- Lucide React Native (图标)
- 动画库: react-native-reanimated 3+（首选）+ Moti（可选，声明式动画）
  - 注意：React Native 不支持 Framer Motion，使用 Reanimated 替代
- 使用 `<View>` / `<Text>` / `<ScrollView>` / `<FlatList>` / `<Pressable>` / `<Animated.View>`

**移动端适配**：
- 最小触摸目标: 48x48pt（比web的44px稍大）
- 安全区域: SafeAreaView（使用 react-native-safe-area-context）
- 键盘避让: KeyboardAvoidingView
- 滚动物理: 原生动量（bounces=true）
- 响应式单位: 使用 PixelRatio 适配不同屏幕密度
- 字号响应式: 使用 react-native-responsive-fontsize 或自定义 hook 实现类似 clamp() 效果
  - 不支持 CSS clamp()，用响应式计算替代
  - Display: 32-48pt（根据屏幕宽度缩放）
  - H1: 28-36pt
  - H2: 22-28pt
  - H3: 18-22pt
  - Body: 16pt（固定，移动端正文不小于16pt避免缩放）

**全局约束**：
- 配色: 主色作为 ColorValue，使用 Design Token 映射
- 字体: 通过 Font.loadAsync 加载，匹配 Design Brief 字体
- 暗色模式: 使用 useColorScheme() + NativeWind dark: 前缀
- 品牌人格: 对应移动端设计语言（iOS Human Interface / Material You 适配）

**排版约束（移动端特化）**：
- 移动端标题字重略高于web（小屏幕需要更强视觉层次）：
  - Display/H1: fontWeight: 500 (Medium) 或 600 (Semibold)
  - H2/H3: fontWeight: 600 (Semibold)
  - Body: fontWeight: 400 (Regular)
  - Button labels: fontWeight: 600 (Semibold)
- 字间距（移动端注意，系统会自动处理）：
  - Display: letterSpacing: -0.5 到 -1pt（对应web的-0.02em）
  - H2/H3: letterSpacing: -0.25 到 -0.5pt
  - ALL CAPS 文字: letterSpacing: 1 到 1.5pt（对应0.08em）
- 行高：
  - Display: lineHeight: 1.1
  - H1/H2: lineHeight: 1.2
  - Body: lineHeight: 1.5-1.6
- 恰好 3-4 个 font-weight (400 / 500 / 600 / 700)（移动端最多到700用于按钮）
- 正文最小字号: 16pt（避免iOS自动缩放）

**动效（react-native-reanimated spring）**：
- {动效描述，来自视觉论文 motion-direction}
- 使用 react-native-reanimated 的 withSpring 物理动画：
  ```ts
  // 按钮点击
  withSpring(1, {
    damping: 25,
    stiffness: 400,
  })
  // 卡片入场
  withTiming({ opacity: 1, translateY: 0 }, {
    duration: 400,
    easing: Easing.out(Easing.cubic),
  })
  // 或者用 spring：
  withSpring({ opacity: 1, translateY: 0 }, {
    damping: 25,
    stiffness: 200,
  })
  ```
- 参数与web对应：
  - stiffness: 200 (入场) / 300 (过渡) / 400 (微交互)
  - damping: 25
- Hover效果：移动端无hover，使用 onPressIn/onPressOut 替代
- 触摸反馈: opacity 0.8-0.9 或 scale 0.97
- Stagger子元素: withDelay + withSequence
- 必须尊重 AccessibilityInfo.isReduceMotionEnabled()

**移动端特有禁止**：
- ❌ Framer Motion 包（RN不支持，用react-native-reanimated）
- ❌ hover 效果（移动端无hover，用press态）
- ❌ 桌面端 fixed sidebar
- ❌ 横向滚动（除非显式需要，如carousel）
- ❌ 过小的文字 (<14pt，正文必须≥16pt)
- ❌ 小于48x48pt的触摸目标
- ❌ CSS clamp() 函数（不支持，用响应式计算）
- ❌ web的shadow-md/shadow-lg直接使用（RN有不同shadow API）
- ❌ 大标题使用 fontWeight: 800/900（Black/Heavy）
- ❌ 所有卡片统一padding（根据内容密度调整）
- ❌ 过长动画 (>500ms，移动端更快节奏)
- ❌ 动画非transform/opacity属性（性能差）
- ❌ emoji 图标（用 Lucide 或 Material Icons）
- ❌ 两色渐变 (purple→blue / blue→cyan / indigo→pink)
- ❌ 假指标、填充文案
- ❌ 完美对称布局
- ❌ 装饰性 blob/wave SVG 背景

**参考**：
- Design Brief: output/design-system.md
- Premium Rules: references/premium-design-rules.md（移动端适配）
- 参考源: Apple HIG · Material 3 · React Native Paper
```

---

## 核心组件模板

### 按钮 (React Native)

```tsx
import { Pressable, Text, ViewStyle, TextStyle } from 'react-native'
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated'

const AnimatedPressable = Animated.createAnimatedComponent(Pressable)

interface ButtonProps {
  title: string
  variant?: 'primary' | 'secondary' | 'ghost'
  disabled?: boolean
  onPress?: () => void
}

export function Button({ title, variant = 'primary', disabled, onPress }: ButtonProps) {
  const scale = useSharedValue(1)

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }))

  return (
    <AnimatedPressable
      onPress={onPress}
      disabled={disabled}
      onPressIn={() => {
        scale.value = withSpring(0.97, { damping: 25, stiffness: 400 })
      }}
      onPressOut={() => {
        scale.value = withSpring(1, { damping: 25, stiffness: 400 })
      }}
      style={[
        animatedStyle,
        {
          minHeight: 48,
          paddingHorizontal: 24,
          paddingVertical: 12,
          borderRadius: 12, /* 移动端按钮圆角比web稍大 */
          backgroundColor: variant === 'primary' ? 'var(--color-primary)' : 'transparent',
          borderWidth: variant === 'secondary' ? 1 : 0,
          borderColor: 'var(--color-border)',
          opacity: disabled ? 0.5 : 1,
          alignItems: 'center',
          justifyContent: 'center',
        } as ViewStyle,
      ]}
    >
      <Text
        style={{
          fontFamily: 'var(--font-body)',
          fontSize: 16,
          fontWeight: '600',
          letterSpacing: 0.3,
          color: variant === 'primary' ? '#fff' : 'var(--color-text)',
        } as TextStyle}
      >
        {title}
      </Text>
    </AnimatedPressable>
  )
}
```

### 卡片 (React Native)

```tsx
import { View, Text, Pressable, ViewStyle, TextStyle } from 'react-native'
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
  Easing,
} from 'react-native-reanimated'
import { useEffect } from 'react'

interface CardProps {
  title: string
  children?: React.ReactNode
  onPress?: () => void
}

export function Card({ title, children, onPress }: CardProps) {
  const opacity = useSharedValue(0)
  const translateY = useSharedValue(20)
  const scale = useSharedValue(1)

  useEffect(() => {
    opacity.value = withTiming(1, { duration: 400, easing: Easing.out(Easing.cubic) })
    translateY.value = withSpring(0, { damping: 25, stiffness: 200 })
  }, [])

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [
      { translateY: translateY.value },
      { scale: scale.value },
    ],
  }))

  return (
    <Animated.View
      style={[
        animatedStyle,
        {
          backgroundColor: 'var(--color-surface)',
          borderWidth: 1,
          borderColor: 'var(--color-border)',
          borderRadius: 16, /* 移动端卡片圆角16px比web的12px稍大 */
          padding: 20,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.05,
          shadowRadius: 8,
          elevation: 2, /* Android elevation */
        } as ViewStyle,
      ]}
    >
      <Pressable
        onPress={onPress}
        onPressIn={() => {
          if (onPress) {
            scale.value = withSpring(0.98, { damping: 25, stiffness: 400 })
          }
        }}
        onPressOut={() => {
          scale.value = withSpring(1, { damping: 25, stiffness: 400 })
        }}
      >
        <Text
          style={{
            fontSize: 18,
            fontWeight: '600',
            letterSpacing: -0.3,
            marginBottom: 8,
            color: 'var(--color-text)',
          } as TextStyle}
        >
          {title}
        </Text>
        {children}
      </Pressable>
    </Animated.View>
  )
}
```

### 底部导航 (移动端)

```tsx
生成 React Native 底部 Tab 导航：
- 高度: 56-64pt + safe area bottom
- 背景: var(--color-bg)（可加毛玻璃: blur(20px)）
- 分隔线: 1px var(--color-border) top
- 图标: 24pt SVG，激活态 var(--color-primary)，非激活态 var(--color-text-tertiary)
- 标签: 10-11pt caption，激活态 600 weight
- 触摸反馈: scale(0.95) spring
- 禁止: emoji 图标、超过 5 个 tab、文字大小不统一
```

### 表单 (移动端)

```tsx
生成 React Native 表单组件：
- 标签: 上置，14pt，color var(--color-text-secondary)，fontWeight 500
- 输入框: height 48pt，border 1px var(--color-border)，border-radius 12pt
- 输入框字号: 16pt（防止iOS自动缩放）
- 聚焦: border-color var(--color-primary)
- 提交: 全宽 48-52pt primary 按钮，带spring动效
- 禁止: placeholder 替代 label、小于48pt高度、小于16pt字号
```

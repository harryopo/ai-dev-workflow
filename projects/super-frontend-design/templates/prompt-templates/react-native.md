# React Native + NativeWind Prompt 模板

> React Native 移动端组件生成模板。
> 设计约束同 react-tailwind.md，适配移动端布局。

---

## Block: {Block 类型}

```
生成一个 React Native + NativeWind 的 {Block 类型名称} 移动端组件。

**框架约定**：
- React Native 0.73+
- NativeWind 4+ (Tailwind CSS 运行时)
- Expo Router (路由)
- Lucide React Native (图标)
- 使用 `<View>` / `<Text>` / `<ScrollView>` / `<FlatList>`

**移动端适配**：
- 最小触摸目标: 44x44px
- 安全区域: SafeAreaView
- 键盘避让: KeyboardAvoidingView
- 滚动物理: 原生动量

**全局约束**：见 react-tailwind.md（配色/字体/反 AI 规则全相同）

**移动端特有禁止**：
- ❌ hover 效果（移动端无 hover）
- ❌ 桌面端 fixed sidebar
- ❌ 横向滚动（除非显式需要）
- ❌ 过小的文字 (≤11px)

**焦点状态**：
- 使用 AccessibilityInfo + focus 事件
- 所有交互元素有 accessible label
```

---

## 核心组件模板

### 卡片 (移动端)

```
生成 React Native 卡片组件：
- 背景: var(--color-surface)
- 圆角: 12px
- 间距: padding 16px
- 触摸反馈: Pressable + opacity 0.8 onPressIn
- 禁止: 阴影层级 >2
```

### 底部导航 (移动端)

```
生成 React Native 底部 Tab 导航：
- 高度: 56px + safe area bottom
- 背景: var(--color-bg)
- 分隔线: 1px var(--color-border)
- 图标: 24px SVG，激活态 var(--color-primary)，非激活态 var(--color-text-tertiary)
- 标签: 10px caption，激活态 primary
- 禁止: emoji 图标、超过 5 个 tab
```

### 表单 (移动端)

```
生成 React Native 表单组件：
- 标签: 上置，14px，color var(--color-text-secondary)
- 输入框: height 48px，border 1px var(--color-border)，border-radius 8px
- 聚焦: border-color var(--color-primary) + 2px primary 光晕
- 提交: 全宽 48px primary 按钮
- 禁止: placeholder 替代 label
```

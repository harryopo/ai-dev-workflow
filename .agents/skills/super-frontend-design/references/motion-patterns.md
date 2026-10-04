# Desktop Motion Patterns — 桌面端动效方案库

> 支持 Electron、Tauri、PySide6、SwiftUI、WinUI 3 等桌面框架的动效设计。
> 与 Web 动效不同，桌面动效更注重系统一致性、性能和资源效率。

---

## 1. 桌面动效设计原则

### 核心差异

| 维度 | 网页动效 | 桌面动效 |
|------|---------|---------|
| 性能预算 | 受限于浏览器 | 直接使用系统资源，性能更高 |
| 系统整合 | 仅浏览器 API | 可访问原生 API（窗口、拖放、剪贴板） |
| 用户预期 | 随时刷新可重置 | 状态持久，动效需尊重历史 |
| 多任务 | 单一标签页 | 多窗口、后台进程 |
| 硬件加速 | GPU 有限 | 可充分利用 GPU/CPU |

### 设计优先级

1. **性能优先**：桌面应用对卡顿更敏感（用户感知更强）
2. **系统一致性**：遵循操作系统动效规范
3. **克制**：桌面用户习惯高效操作，过多动效干扰工作
4. **可中断**：所有动效必须可被用户操作立即中断
5. **减少模式**：尊重 prefers-reduced-motion

---

## 2. 平台动效规范

### 2.1 macOS HIG 动效

| 场景 | 规范 | 时长 |
|------|------|------|
| 窗口打开 | Scale up + fade in | 200-300ms |
| 窗口关闭 | Scale down + fade out | 150-250ms |
| 面板滑入 | Slide from edge | 250-350ms |
| 按钮点击 | 轻微 scale down | 100ms |
| 选中高亮 | 渐变色填充 | 150-200ms |
| 切换视图 | Spring bounce | 400-600ms |

**关键原则**：
- 使用 spring 物理曲线（非线性）
- 窗口动画跟随系统动画速度
- 最小化动效，只在状态变化时播放

### 2.2 Windows Fluent Design 动效

| 场景 | 规范 | 时长 |
|------|------|------|
| 窗口打开 | Fade + slide up | 200-300ms |
| 窗口关闭 | Fade out | 150-200ms |
| Acrylic 模糊 | 渐显 | 100-200ms |
| 按钮悬停 | 轻微 raise + 颜色过渡 | 100-150ms |
| 选中态 | 淡入下划线/高亮 | 100-150ms |

**关键原则**：
- Material（亚克力/mica）效果优先
- Reveal 效果（悬停光晕）
- 平滑过渡，不使用弹跳

### 2.3 Linux (GNOME) 动效

| 场景 | 规范 | 时长 |
|------|------|------|
| 窗口打开 | Fade + scale | 200-250ms |
| 窗口关闭 | Fade out | 150ms |
| 应用切换 | Scale + fade | 250-350ms |

---

## 3. 各框架动效方案

### 3.1 Electron 动效

Electron 基于 Chromium，主要使用 Web 技术实现动效：

```javascript
// 窗口动画
win.webContents.on('did-finish-load', () => {
  win.setBounds({
    x: targetX,
    y: targetY,
    width: targetWidth,
    height: targetHeight
  }, true); // true = 带动画
});

// 使用 CSS transitions
.css({
  'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  'transform': 'translateY(0)',
  'opacity': '1'
})
```

**Electron 动效库推荐**：
- `electron-window-state`：窗口状态持久化
- `electron-context-menu`：右键菜单动画
- CSS transitions（首选，性能最优）
- GSAP（复杂动画）

### 3.2 Tauri 动效

Tauri 使用系统 WebView，动效实现方式与 Electron 类似，但可访问更多系统 API：

```rust
// 窗口显示动画（Tauri v2）
use tauri::{Manager, app::AppHandle};

app.handle().get_window("main").unwrap().show().unwrap();
// Tauri 自动处理窗口显示动画
```

**Tauri 动效推荐**：
- CSS transitions（首选）
- `@tauri-apps/api` 系统 API
- 原生窗口动画（无需 JS）

### 3.3 PySide6 / Qt 动效

PySide6 提供完整的动画框架：

```python
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QWidget

# 淡入淡出动画
def fade_in(widget, duration=300):
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setDuration(duration)
    anim.setEasingCurve(QEasingCurve.InOutCubic)
    anim.start()

# 位置移动动画
def slide_in(widget, target_x, duration=300):
    anim = QPropertyAnimation(widget, b"pos")
    anim.setStartValue(widget.pos())
    anim.setEndValue(QPoint(target_x, widget.y()))
    anim.setDuration(duration)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
```

**PySide6 动效库**：
- `QPropertyAnimation`：属性动画
- `QEasingCurve`：缓动曲线
- `QParallelAnimationGroup`：并行动画
- `QSequentialAnimationGroup`：序列动画

### 3.4 SwiftUI 动效

SwiftUI 原生支持声明式动效：

```swift
// 淡入动画
struct ContentView: View {
    @State private var isVisible = false
    
    var body: some View {
        Text("Hello")
            .opacity(isVisible ? 1 : 0)
            .onAppear {
                withAnimation(.easeInOut(duration: 0.3)) {
                    isVisible = true
                }
            }
    }
}

// 弹簧动画
.withAnimation(.spring(response: 0.4, dampingFraction: 0.6))

// 视图转场
.transition(.move(edge: .leading).combined(with: .opacity))
```

**SwiftUI 动效库**：
- `withAnimation()`：声明式动效
- `.spring()`：弹簧动效
- `.easeInOut()`：平滑过渡
- `.blurEffect()`：毛玻璃效果

### 3.5 WinUI 3 动效

WinUI 3 使用 XAML 动画系统：

```xaml
<!-- 淡入动画 -->
<VisualStateManager.VisualStateGroups>
  <VisualStateGroup x:Name="CommonStates">
    <VisualState x:Name="Normal">
      <VisualState.Setters>
        <Setter Target="MyElement.Opacity" Value="1"/>
      </VisualState.Setters>
    </VisualState>
    <VisualState x:Name="Hidden">
      <VisualState.Setters>
        <Setter Target="MyElement.Opacity" Value="0"/>
      </VisualState.Setters>
    </VisualState>
  </VisualStateGroup>
</VisualStateManager>
```

**WinUI 3 动效库**：
- `Implicit animations`：声明式隐式动画
- `Visual State Manager`：状态驱动动画
- `Composition animations`：高性能 GPU 动画

---

## 4. 桌面应用动效模式

### 4.1 窗口动画

| 场景 | 推荐方案 | 时长 |
|------|---------|------|
| 窗口打开 | Fade in + Scale up | 200-300ms |
| 窗口关闭 | Fade out + Scale down | 150-200ms |
| 窗口最小化 | 缩放到任务栏 | 250-350ms |
| 窗口最大化 | 展开动画 | 200-300ms |
| 浮动面板 | Slide from edge | 200-250ms |

### 4.2 面板/侧栏动画

```
折叠状态：  [图标]    展开状态：  [图标]  内容...
             │              │
             ▼              ▼
      ┌─────────┐      ┌─────────────┐
      │ 📁      │  →   │ 📁  文件树  │
      │ 🔍      │      │ 🔍  搜索    │
      └─────────┘      │ ✅  源码控制│
                       └─────────────┘
```

**实现**：
- 宽度从 48px → 200px 过渡
- 内容使用 `overflow: hidden` 防止溢出
- 使用 `cubic-bezier(0.4, 0, 0.2, 1)` 缓动

### 4.3 列表项动画

| 场景 | 方案 | 说明 |
|------|------|------|
| 新增项 | Slide in from top | 新任务出现 |
| 删除项 | Fade out + Shrink | 任务完成 |
| 排序变化 | FLIP 动画 | 位置过渡平滑 |
| 选中高亮 | 背景色过渡 | 100-150ms |

### 4.4 模态对话框动画

```
触发元素 → 遮罩淡入 + 对话框从中心弹出
                    ↓
              对话框 scale: 0.9 → 1.0
              遮罩 opacity: 0 → 0.5
```

**规范**：
- 时长 200-300ms
- 使用 ease-out 曲线
- 点击遮罩可关闭（带淡出动画）
- ESC 键可关闭

### 4.5 Toast/通知动画

```
位置：右上角/右下角
入场：Slide in from right
停留：3-5秒
离场：Slide out to right 或 Fade out
```

**规范**：
- 自动消失，可手动关闭
- 多个 Toast 堆叠显示
- 重要通知需用户确认

### 4.6 页面/视图切换

| 场景 | 方案 | 时长 |
|------|------|------|
| 前进导航 | Slide left → right | 300ms |
| 后退导航 | Slide right → left | 300ms |
| Tab 切换 | Fade + Scale | 200ms |
| 抽屉展开 | Slide from edge | 250ms |

---

## 5. 动效库选型决策

| 场景 | 推荐库 | 原因 |
|------|--------|------|
| 简单窗口动画 | 系统原生 API | 性能最优，系统整合 |
| 面板折叠/展开 | CSS transitions | 轻量，无需额外依赖 |
| 列表排序动画 | FLIP 技术 | 自动计算位置变化 |
| 复杂时间轴 | GSAP | 精确控制，可嵌套 |
| PySide6 项目 | QPropertyAnimation | 原生集成，性能好 |
| SwiftUI 项目 | withAnimation | 声明式，Xcode 集成 |
| WinUI 3 项目 | Implicit animations | 声明式，性能良好 |

---

## 6. 动效检查清单

- [ ] 动效时长在推荐范围内（150-500ms）
- [ ] 所有动效可使用 `prefers-reduced-motion` 禁用
- [ ] 窗口动画使用系统原生 API
- [ ] 列表项动画使用 transform（非 width/height）
- [ ] 面板折叠使用流畅的宽度过渡
- [ ] 模态对话框有遮罩淡入效果
- [ ] Toast 通知有入场/离场动画
- [ ] 页面切换有过渡效果
- [ ] 按钮点击有反馈（scale/颜色变化）
- [ ] 动效可被用户操作立即中断
- [ ] 动效不阻塞用户交互
- [ ] 动效在低性能设备上可降级
- [ ] 动效风格符合平台规范（macOS/Windows/Linux）

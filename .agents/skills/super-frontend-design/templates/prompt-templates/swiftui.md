# SwiftUI 桌面/iOS 应用 Prompt 模板

> 适用场景：SwiftUI + iOS 17+ / macOS 14+ 原生应用 UI 设计
> 合并来源：desktop-patterns + professional-software + apple-design

## 技术栈

- **框架**：SwiftUI（iOS 17+ / macOS 14+）
- **语言**：Swift 5.9+
- **架构**：MVVM + Observable
- **图标**：SF Symbols
- **动效**：withAnimation + Spring
- **导航**：NavigationStack + NavigationSplitView

## 目录结构

```
project/
├── App/
│   ├── MyApp.swift           # 入口
│   └── AppState.swift        # 全局状态
├── Views/
│   ├── ContentView.swift     # 主界面
│   ├── Components/           # 可复用组件
│   │   ├── Sidebar.swift
│   │   ├── CommandPalette.swift
│   │   └── PropertyPanel.swift
│   └── Pages/
│       ├── DashboardPage.swift
│       └── SettingsPage.swift
├── Models/
│   └── DesignTokens.swift    # Design Token
├── Assets.xcassets           # 资源
└── Resources/
    └── colors.xcassets       # 自定义颜色
```

## 核心设计决策

### 1. Design Token 系统

```swift
// Models/DesignTokens.swift
import SwiftUI

// MARK: - Colors
enum AppColor {
    // 品牌色
    static let primary = Color(.sRGB, red: 0.055, green: 0.647, blue: 0.914)
    static let primaryHover = Color(.sRGB, red: 0.016, green: 0.518, blue: 0.757)

    // 中性色 - Light
    static let surface = Color(.sRGB, red: 1, green: 1, blue: 1)
    static let surfaceRaised = Color(.sRGB, red: 0.973, green: 0.973, blue: 0.98)
    static let background = Color(.sRGB, red: 0.98, green: 0.98, blue: 0.984)
    static let onSurface = Color(.sRGB, red: 0.059, green: 0.09, blue: 0.165)
    static let onSurfaceVariant = Color(.sRGB, red: 0.278, green: 0.333, blue: 0.412)
    static let onSurfaceMuted = Color(.sRGB, red: 0.58, green: 0.639, blue: 0.722)
    static let border = Color(.sRGB, red: 0.886, green: 0.91, blue: 0.941)

    // 功能色
    static let success = Color(.sRGB, red: 0.133, green: 0.773, blue: 0.369)
    static let warning = Color(.sRGB, red: 0.961, green: 0.62, blue: 0.043)
    static let danger = Color(.sRGB, red: 0.937, green: 0.267, blue: 0.267)
    static let info = Color(.sRGB, red: 0.231, green: 0.51, blue: 0.965)
}

extension AppColor {
    // Dark mode
    static let surfaceDark = Color(.sRGB, red: 0.059, green: 0.09, blue: 0.165)
    static let surfaceRaisedDark = Color(.sRGB, red: 0.118, green: 0.161, blue: 0.231)
    static let backgroundDark = Color(.sRGB, red: 0.008, green: 0.024, blue: 0.067)
    static let onSurfaceDark = Color(.sRGB, red: 0.973, green: 0.973, blue: 0.98)
    static let borderDark = Color(.sRGB, red: 0.2, green: 0.255, blue: 0.333)
}

// MARK: - Typography
enum AppFont {
    static let display = Font.system(.largeTitle, design: .rounded, weight: .bold)
    static let title = Font.system(.title, design: .rounded, weight: .semibold)
    static let headline = Font.system(.headline, weight: .semibold)
    static let body = Font.system(.body, design: .default, weight: .regular)
    static let caption = Font.system(.caption, weight: .medium)
    static let mono = Font.monospaced().system(size: 13)
}

// MARK: - Spacing
enum AppSpacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
}

// MARK: - Corner Radius
enum AppRadius {
    static let sm: CGFloat = 4
    static let md: CGFloat = 8
    static let lg: CGFloat = 12
    static let xl: CGFloat = 16
    static let full: CGFloat = 9999
}
```

### 2. 主界面布局（macOS）

```swift
// Views/ContentView.swift
import SwiftUI

struct ContentView: View {
    @State private var sidebarWidth: CGFloat = 220
    @State private var selectedTab: String = "dashboard"
    @State private var showCommandPalette = false

    var body: some View {
        NavigationSplitView {
            // 侧边栏
            SidebarView(
                selectedTab: $selectedTab,
                width: sidebarWidth
            )
        } detail: {
            // 主内容区
            TabView(selection: $selectedTab) {
                DashboardPage()
                    .tabItem { Label("仪表板", systemImage: "square.grid.2x2") }
                    .tag("dashboard")

                ProjectsPage()
                    .tabItem { Label("项目", systemImage: "folder") }
                    .tag("projects")

                SettingsPage()
                    .tabItem { Label("设置", systemImage: "gear") }
                    .tag("settings")
            }
            .toolbar {
                ToolbarItem(placement: .navigation) {
                    SearchBar()
                }
            }
        }
        .frame(minWidth: 1024, minHeight: 768)
        .commandPalette($showCommandPalette)
        .onKeyboardShortcut(KeyEquivalent("k"), modifiers: [.command]) {
            withAnimation(.easeInOut(duration: 0.15)) {
                showCommandPalette.toggle()
            }
        }
    }
}
```

### 3. 侧边栏组件

```swift
// Views/Components/Sidebar.swift
import SwiftUI

struct SidebarView: View {
    @Binding var selectedTab: String
    var width: CGFloat

    let items: [(id: String, icon: String, label: String)] = [
        ("dashboard", "square.grid.2x2", "仪表板"),
        ("projects", "folder", "项目"),
        ("files", "doc", "文件"),
        ("search", "magnifyingglass", "搜索"),
        ("settings", "gear", "设置"),
    ]

    var body: some View {
        VStack(spacing: 0) {
            // Logo
            HStack {
                Image(systemName: "app.fill")
                    .font(.title2)
                    .foregroundStyle(.primary)
                Text("App Name")
                    .font(.headline)
                    .foregroundStyle(.primary)
                Spacer()
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)

            Divider()

            // 导航项
            ScrollView {
                VStack(spacing: 2) {
                    ForEach(items, id: \.id) { item in
                        SidebarItem(
                            icon: item.icon,
                            label: item.label,
                            isSelected: selectedTab == item.id
                        ) {
                            withAnimation(.spring(response: 0.3)) {
                                selectedTab = item.id
                            }
                        }
                    }
                }
                .padding(.vertical, 8)
            }

            Spacer()

            // 底部用户信息
            HStack {
                Image(systemName: "person.circle")
                    .font(.title3)
                Text("用户")
                    .font(.caption)
                Spacer()
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
        }
        .frame(width: width)
        .background(.ultraThinMaterial)
    }
}

struct SidebarItem: View {
    let icon: String
    let label: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.body)
                    .frame(width: 20)
                Text(label)
                    .font(.body)
                Spacer()
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(isSelected ? Color.primary.opacity(0.1) : Color.clear)
            .cornerRadius(6)
        }
        .buttonStyle(.plain)
    }
}
```

### 4. Command Palette

```swift
// Views/Components/CommandPalette.swift
import SwiftUI

struct CommandPalette: View {
    @Binding var isPresented: Bool
    @State private var query = ""
    @State private var selectedIndex = 0

    let commands: [Command] = [
        Command(icon: "doc.fill", label: "新建文件", shortcut: "⌘N"),
        Command(icon: "folder.fill", label: "打开文件...", shortcut: "⌘O"),
        Command(icon: "paintpalette.fill", label: "切换主题", shortcut: "⌘T"),
        Command(icon: "gearshape.fill", label: "设置", shortcut: "⌘,"),
    ]

    var filteredCommands: [Command] {
        if query.isEmpty { return commands }
        return commands.filter { $0.label.localizedCaseInsensitiveContains(query) }
    }

    var body: some View {
        WindowCard {
            VStack(spacing: 0) {
                // 搜索框
                HStack(spacing: 10) {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(.secondary)
                    TextField("搜索命令...", text: $query)
                        .textFieldStyle(.plain)
                    Spacer()
                    if !query.isEmpty {
                        Button { query = "" } label: {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundStyle(.secondary)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 10)
                .background(Color(.controlBackgroundColor))

                Divider()

                // 结果列表
                ScrollView {
                    VStack(spacing: 2) {
                        ForEach(Array(filteredCommands.enumerated()), id: \.offset) { index, cmd in
                            CommandRow(command: cmd, isSelected: index == selectedIndex)
                                .onTapGesture {
                                    // 执行命令
                                    isPresented = false
                                }
                        }
                    }
                    .padding(.vertical, 6)
                }
            }
            .frame(width: 420, height: 320)
            .cornerRadius(12)
            .shadow(radius: 20)
        }
        .onAppear { query = ""; selectedIndex = 0 }
    }
}

struct Command {
    let icon: String
    let label: String
    let shortcut: String
}

struct CommandRow: View {
    let command: Command
    let isSelected: Bool

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: command.icon)
                .foregroundStyle(isSelected ? .accentColor : .secondary)
                .font(.body)
            Text(command.label)
                .foregroundStyle(isSelected ? .accentColor : .primary)
            Spacer()
            Text(command.shortcut)
                .font(.caption2)
                .foregroundStyle(.secondary)
                .padding(.horizontal, 6)
                .padding(.vertical, 2)
                .background(Color(.secondaryLabelColor).opacity(0.2))
                .cornerRadius(4)
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
        .background(isSelected ? Color.accentColor.opacity(0.1) : Color.clear)
        .cornerRadius(6)
    }
}
```

### 5. 窗口控制（macOS Custom Title Bar）

```swift
// Views/Components/WindowControls.swift
import SwiftUI

struct WindowControls: View {
    var body: some View {
        HStack(spacing: 8) {
            windowButton(color: .red, symbol: "minussign.fill")
            windowButton(color: .yellow, symbol: "rectangle.fill")
            windowButton(color: .green, symbol: "chevron.compact.down")
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
    }

    private func windowButton(color: Color, symbol: String) -> some View {
        Button {} label: {
            Image(systemName: symbol)
                .font(.system(size: 8))
                .foregroundStyle(color)
                .frame(width: 12, height: 12)
        }
        .buttonStyle(SquareButtonStyle())
    }
}

struct SquareButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .background(Color.gray.opacity(0.3))
            .clipShape(Circle())
            .overlay(
                Circle()
                    .stroke(Color.gray.opacity(0.5), lineWidth: 0.5)
            )
            .scaleEffect(configuration.isPressed ? 0.9 : 1.0)
    }
}

// 拖拽区域
struct DragArea: View {
    let content: () -> View

    var body: some View {
        GeometryReader { geo in
            ZStack {
                content()
                    .frame(maxWidth: .infinity)
                Rectangle()
                    .fill(Color.clear)
                    .contentShape(Rectangle())
                    .onTapGesture {}
            }
            .frame(height: geo.size.height)
            .frame(maxWidth: .infinity)
        }
        .help("拖动以移动窗口")
    }
}
```

### 6. 应用入口

```swift
// App/MyApp.swift
import SwiftUI

@main
struct MyApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unified)
        .commands {
            CommandGroup(replacing: .newItem) {
                Button("新建") { appState.showCommandPalette = true }
                    .keyboardShortcut("n", modifiers: [.command])
            }
            CommandGroup(after: .appInfo) {
                Button("设置") { appState.openSettings() }
                    .keyboardShortcut(",", modifiers: [.command])
            }
        }
    }
}

// App/AppState.swift
import SwiftUI

@MainActor
class AppState: ObservableObject {
    @Published var selectedTheme: Theme = .dark
    @Published var showCommandPalette = false

    enum Theme: String, CaseIterable {
        case light, dark, system
    }
}
```

## Prompt 使用指南

1. 调用 `super-frontend-design` Skill，路由到 `design` 子命令
2. 在 research 阶段，明确告知技术栈为 **SwiftUI + iOS/macOS**
3. SwiftUI 优势：声明式 UI、原生系统集成、Apple 生态深度整合
4. 设计时参考 `references/desktop-patterns.md` 和 `references/professional-software.md`
5. 输出时包含完整的 SwiftUI 代码 + Design Token 系统

## 关键注意事项

- **HIG 遵循**：严格遵循 Apple Human Interface Guidelines
- **Liquid Glass**：macOS Sequoia 引入的新视觉风格
- **SF Symbols**：优先使用系统图标，保持视觉一致性
- **Dynamic Type**：支持系统字体缩放
- **Split View**：充分利用 iPad/macOS 分屏能力
- **Accessibility**：VoiceOver、Reduced Motion、High Contrast 支持
- **Dark Mode**：使用系统色（.primary/.secondary）而非硬编码颜色

# Tauri 桌面应用 Prompt 模板

> 适用场景：Tauri v2 + React/Vue + Tailwind CSS 桌面应用 UI 设计
> 合并来源：desktop-patterns + professional-software + frontend-design

## 技术栈

- **框架**：Tauri v2（Rust 后端 + Web 前端）
- **前端**：React 19 / Vue 3 / Svelte 5
- **样式**：Tailwind CSS v4 + CSS Custom Properties
- **组件**：shadcn/ui + Radix UI
- **动效**：CSS transitions（首选）+ GSAP（复杂场景）
- **图标**：Lucide React / Heroicons

## 目录结构

```
project/
├── src/
│   ├──-tauri/
│   │   ├── Cargo.toml         # Rust 后端
│   │   └── src/
│   │       ├── main.rs        # 入口
│   │       └── lib.rs         # 命令定义
│   ├── app/                   # 前端应用（与 Vite 集成）
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── styles/
│   │   │   │   └── design-tokens.css
│   │   │   └── pages/
│   │   └── index.html
│   └── package.json
├── tauri.conf.json
└── src-tauri/
    ├── Cargo.toml
    └── build.rs
```

## 核心设计决策

### 1. Tauri 窗口配置

```json
// tauri.conf.json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "App Name",
        "width": 1400,
        "height": 900,
        "minWidth": 1024,
        "minHeight": 768,
        "resizable": true,
        "fullscreen": false,
        "decorations": false,
        "center": true,
        "transparent": true,
        "titleBarStyle": "Overlay"
      }
    ]
  },
  "bundle": {
    "icon": ["icons/32x32.png", "icons/128x128.png", "icons/icon.ico"],
    "active": true,
    "targets": "all"
  }
}
```

### 2. Rust 后端命令

```rust
// src-tauri/src/lib.rs
use tauri::Manager;

#[tauri::command]
async fn open_file() -> Result<String, String> {
    let window = tauri::api::dialog::FileDialogBuilder::new()
        .add_filter("Images", &["png", "jpg", "jpeg"])
        .pick_file()
        .map(|f| f.map(|p| p.to_string_lossy().to_string()))
        .map_err(|e| e.to_string())?;
    Ok(window.unwrap_or_default())
}

#[tauri::command]
fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            open_file,
            get_app_version,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 3. 前端调用后端命令

```tsx
// React
import { invoke } from '@tauri-apps/api/core';

async function handleOpenFile() {
  const result = await invoke<string>('open_file');
  console.log('Selected:', result);
}

// Vue
import { invoke } from '@tauri-apps/api/core';

const selectedFile = ref('');
async function openFile() {
  selectedFile.value = await invoke<string>('open_file');
}
```

### 4. 窗口管理

```typescript
// src/app/src/services/window.ts
import { getCurrentWindow } from '@tauri-apps/api/window';
import { appWindow } from '@tauri-apps/api/window';

export const window = getCurrentWindow();

export async function minimize() {
  await window.minimize();
}

export async function maximize() {
  await window.toggleMaximize();
}

export async function close() {
  await window.close();
}

export async function setSkipTaskbar(skip: boolean) {
  await window.setSkipTaskbar(skip);
}
```

### 5. 三栏布局模板（与 Electron 类似但更轻量）

```tsx
// src/renderer/app/components/Layout.tsx
import { useState } from 'react';
import { minimize, maximize, close } from '../services/window';

export function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden" style={{ perspective: '1000px' }}>
      {/* 自定义标题栏（Tauri 透明窗口） */}
      <div
        className="titlebar flex items-center justify-between px-3"
        style={{ WebkitAppRegion: 'drag' as any }}
      >
        <div className="flex items-center gap-3">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1 hover:bg-muted rounded">
            <MenuIcon />
          </button>
          <span className="text-sm font-medium">App Name</span>
        </div>
        <div className="flex items-center gap-2" style={{ WebkitAppRegion: 'no-drag' as any }}>
          <button onClick={minimize} className="window-btn">─</button>
          <button onClick={maximize} className="window-btn">□</button>
          <button onClick={close} className="window-btn close">✕</button>
        </div>
      </div>

      {/* 主体 */}
      <div className="flex flex-1 overflow-hidden">
        <aside className={`${sidebarOpen ? 'w-52' : 'w-12'} transition-all duration-200 bg-surface border-r border-border`}>
          <Sidebar />
        </aside>
        <main className="flex-1 overflow-auto bg-background">
          {children}
        </main>
      </div>

      {/* 状态栏 */}
      <footer className="h-6 bg-surface border-t border-border flex items-center px-3 text-xs text-muted">
        <span>✓ 就绪</span>
      </footer>
    </div>
  );
}
```

### 6. 系统托盘（Tauri v2）

```typescript
// src/app/src/services/tray.ts
import { Tray } from '@tauri-apps/api/tray';
import { listen } from '@tauri-apps/api/event';

export async function createTray() {
  const tray = new Tray('assets/tray-icon.png');

  tray.on('click', () => {
    // 显示主窗口
  });

  return tray;
}
```

## Prompt 使用指南

1. 调用 `super-frontend-design` Skill，路由到 `design` 子命令
2. 在 research 阶段，明确告知技术栈为 **Tauri + React/Vue**
3. Tauri 的优势：体积更小（~3MB vs Electron ~150MB）、原生 Rust 后端、更好的性能
4. 设计时参考 `references/desktop-patterns.md`
5. 输出时包含完整的 Tauri 配置 + Rust 后端命令

## 与 Electron 的关键差异

| 特性 | Electron | Tauri |
|------|----------|-------|
| 安装包体积 | ~150MB | ~3-10MB |
| 内存占用 | 较高（Chromium） | 较低（系统 WebView） |
| 安全模型 | Context Isolation | Rust 类型安全 |
| 后端语言 | JavaScript | Rust |
| 平台 WebView | 内置 Chromium | 系统 WebView（WKWebView/WebView2） |
| 命令系统 | IPC（JSON） | tauri::command（Rust） |

## 关键注意事项

- **窗口装饰**：使用 `decorations: false` + 自定义标题栏
- **透明窗口**：设置 `transparent: true` 实现圆角窗口
- **命令安全**：所有后端命令在 Rust 中类型安全，前端调用通过 invoke
- **事件系统**：使用 Tauri 的 event 系统实现前后端通信
- **系统托盘**：Tauri v2 原生支持托盘，无需额外依赖
- **打包**：使用 `tauri build` 打包，输出平台原生安装包

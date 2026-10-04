# Electron 桌面应用 Prompt 模板

> 适用场景：Electron + React/Vue + Tailwind CSS 桌面应用 UI 设计
> 合并来源：desktop-patterns + professional-software + frontend-design

## 技术栈

- **框架**：Electron 33+，Node.js 20+
- **前端**：React 19 / Vue 3 / Svelte 5
- **样式**：Tailwind CSS v4 + CSS Custom Properties
- **组件**：shadcn/ui + Radix UI
- **动效**：CSS transitions + GSAP（复杂场景）
- **图标**：Lucide React / Heroicons

## 目录结构

```
project/
├── src/
│   ├── main/               # Electron 主进程
│   │   ├── index.js        # 主入口（窗口管理、托盘、菜单）
│   │   └── preload.js      # 预加载脚本（安全桥接）
│   ├── renderer/           # Electron 渲染进程
│   │   ├── index.html      # 入口 HTML
│   │   └── app/            # 前端应用
│   │       ├── components/
│   │       ├── styles/
│   │       │   └── design-tokens.css
│   │       └── pages/
│   └── shared/             # 共享代码
├── package.json
└── electron-builder.yml    # 打包配置
```

## 核心设计决策

### 1. 窗口配置

```javascript
// src/main/index.js
const { app, BrowserWindow, Menu, Tray, ipcMain } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    trafficLightPosition: { x: 12, y: 12 },
    frame: false,
    backgroundColor: '#0f172a',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  mainWindow.setMenuBarVisibility(false);

  // 窗口状态持久化
  const winState = require('electron-window-state');
  const state = winState({ defaultWidth: 1400, defaultHeight: 900 });
  state.manage(mainWindow);
}
```

### 2. 自定义标题栏

```css
/* 禁止文本选择，支持拖拽 */
.titlebar {
  -webkit-app-region: drag;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 8px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

/* 可点击区域 */
.titlebar-buttons {
  -webkit-app-region: no-drag;
  display: flex;
  gap: 8px;
}
```

### 3. 菜单栏（macOS）

```javascript
const menuTemplate = [
  {
    label: '文件',
    submenu: [
      { label: '新建', accelerator: 'CmdOrCtrl+N', click: () => ipcMain.send('menu:new') },
      { label: '打开', accelerator: 'CmdOrCtrl+O', click: () => ipcMain.send('menu:open') },
      { type: 'separator' },
      { label: '退出', accelerator: 'Cmd+Q', click: () => app.quit() },
    ],
  },
  {
    label: '编辑',
    submenu: [
      { label: '撤销', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
      { label: '重做', accelerator: 'CmdOrCtrl+Shift+Z', role: 'redo' },
      { type: 'separator' },
      { label: '剪切', accelerator: 'CmdOrCtrl+X', role: 'cut' },
      { label: '复制', accelerator: 'CmdOrCtrl+C', role: 'copy' },
      { label: '粘贴', accelerator: 'CmdOrCtrl+V', role: 'paste' },
    ],
  },
  {
    label: '视图',
    submenu: [
      { label: '放大', accelerator: 'CmdOrCtrl+=', role: 'zoomin' },
      { label: '缩小', accelerator: 'CmdOrCtrl+-', role: 'zoomout' },
      { label: '重置', accelerator: 'CmdOrCtrl+0', role: 'resetzoom' },
      { type: 'separator' },
      { label: '全屏', accelerator: 'CmdOrCtrl+Shift+F', role: 'togglefullscreen' },
    ],
  },
];
```

### 4. 三栏布局模板

```tsx
// src/renderer/app/components/Layout.tsx
import { useState } from 'react';

export function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [panelOpen, setPanelOpen] = useState(true);

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden">
      {/* 自定义标题栏 */}
      <div className="titlebar flex items-center justify-between px-3 bg-surface border-b border-border">
        <div className="flex items-center gap-3">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1 hover:bg-muted rounded">
            <MenuIcon />
          </button>
          <span className="text-sm font-medium text-foreground">App Name</span>
        </div>
        <div className="titlebar-buttons">
          <button className="w-3 h-3 rounded-full bg-yellow-500" />
          <button className="w-3 h-3 rounded-full bg-green-500" />
          <button className="w-3 h-3 rounded-full bg-red-500" />
        </div>
      </div>

      {/* 主体布局 */}
      <div className="flex flex-1 overflow-hidden">
        {/* 左侧栏 */}
        <aside className={`${sidebarOpen ? 'w-52' : 'w-12'} transition-all duration-200 bg-surface-raised border-r border-border flex flex-col`}>
          <nav className="p-2 space-y-1">
            <SidebarItem icon="home" label="首页" active />
            <SidebarItem icon="folder" label="文件" />
            <SidebarItem icon="settings" label="设置" />
          </nav>
        </aside>

        {/* 主内容区 */}
        <main className="flex-1 overflow-auto bg-background">
          {children}
        </main>

        {/* 右侧面板 */}
        <aside className={`${panelOpen ? 'w-64' : 'w-0'} transition-all duration-200 bg-surface-raised border-l border-border overflow-hidden`}>
          <div className="p-3">
            <h3 className="text-sm font-medium text-foreground">属性</h3>
            <PropertyPanel />
          </div>
        </aside>
      </div>

      {/* 状态栏 */}
      <footer className="h-6 bg-surface border-t border-border flex items-center px-3 text-xs text-muted">
        <span>✓ 就绪</span>
        <span className="ml-auto">行 42 列 15</span>
      </footer>
    </div>
  );
}
```

### 5. Command Palette

```tsx
// src/renderer/app/components/CommandPalette.tsx
import { useState, useEffect, useRef } from 'react';
import { searchCommands } from '../services/commands';

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
    }
  }, [open]);

  useEffect(() => {
    setResults(searchCommands(query));
  }, [query, open]);

  // 快捷键：Cmd+K / Ctrl+K
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen(!open);
      }
      if (e.key === 'Escape') setOpen(false);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20">
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setOpen(false)} />
      <div className="relative w-full max-w-lg bg-surface border border-border rounded-lg shadow-xl overflow-hidden">
        <div className="flex items-center gap-2 px-3 py-2 border-b border-border">
          <SearchIcon className="w-4 h-4 text-muted" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="搜索命令..."
            className="flex-1 bg-transparent text-sm outline-none text-foreground placeholder:text-muted"
          />
          <kbd className="text-xs text-muted">ESC</kbd>
        </div>
        <div className="max-h-80 overflow-auto p-2">
          {results.map((cmd) => (
            <button
              key={cmd.id}
              className="w-full flex items-center gap-3 px-3 py-2 text-sm text-foreground hover:bg-muted rounded-md"
              onClick={() => { cmd.action(); setOpen(false); }}
            >
              <cmd.icon className="w-4 h-4 text-muted" />
              <span className="flex-1 text-left">{cmd.label}</span>
              {cmd.shortcut && (
                <kbd className="text-xs text-muted">{cmd.shortcut}</kbd>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### 6. 系统托盘

```javascript
// src/main/tray.js
const { Tray, Menu, ipcMain } = require('electron');
const path = require('path');

function createTray(app) {
  const icon = path.join(__dirname, '../assets/tray-icon.png');
  const tray = new Tray(icon);

  const contextMenu = Menu.buildFromTemplate([
    { label: '显示主窗口', click: () => app mainWindow?.show() },
    { label: '设置', click: () => ipcMain.send('menu:settings') },
    { type: 'separator' },
    { label: '退出', click: () => app.quit() },
  ]);

  tray.setToolTip('App Name');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    app mainWindow?.show();
  });

  return tray;
}
```

## Prompt 使用指南

1. 调用 `super-frontend-design` Skill，路由到 `design` 子命令
2. 在 research 阶段，明确告知技术栈为 **Electron + React/Vue**
3. 设计时参考 `references/desktop-patterns.md` 和 `references/professional-software.md`
4. 输出时包含完整的 Electron 主进程 + 渲染进程代码
5. 确保窗口配置、菜单栏、托盘、Command Palette 等桌面特有功能

## 关键注意事项

- **安全**：始终使用 contextIsolation + preload，禁止 nodeIntegration
- **性能**：渲染进程使用 React/Vue 虚拟 DOM，避免频繁 DOM 操作
- **主题**：通过 CSS Custom Properties 支持亮色/暗色切换
- **快捷键**：使用 globalShortcut 注册全局快捷键
- **窗口管理**：实现窗口状态持久化（大小、位置、 maximized 状态）
- **系统托盘**：提供最小化到托盘功能，而非直接关闭
- **文件操作**：使用 electron 的 dialog API，不自己实现文件选择器

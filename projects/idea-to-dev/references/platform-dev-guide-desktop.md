# 桌面软件开发全流程指南

> 来源：第二轮调研 R4
> 用途：阶段 5 编码实施时的桌面开发参考

## 1. 技术栈路线对比

| 框架 | 包体 | 内存 | 性能 | 生态 | 跨平台一致性 | 语言 |
|------|------|------|------|------|------------|------|
| **Electron** | 80-150 MB+ | 高（150-400 MB） | 中 | 极丰富（npm） | 高 | JS/TS |
| **Tauri** | **3-10 MB** | 低（40-100 MB） | 高（Rust） | 中 | 中高 | Rust + 前端 |
| **Qt (PySide6)** | 40-80 MB | 中低 | 高（C++ 原生） | 丰富 | 高 | Python |
| **.NET (WPF/WinUI)** | 中 | 中 | 高 | 丰富（仅 Win） | 低 | C# |
| **SwiftUI (macOS)** | 小 | 低 | 高 | 苹果生态 | 低（仅 Apple） | Swift |
| **Flutter Desktop** | 20-50 MB | 中低 | 高（Skia） | 成长中 | 高 | Dart |

---

## 2. Electron 开发操作清单

- [ ] **前置**：Node.js LTS（https://nodejs.org）
- [ ] **脚手架**：[electron-forge](https://www.electronforge.org/)（官方首选）
- [ ] **打包**：
  - Windows → NSIS/Squirrel
  - macOS → DMG
  - Linux → AppImage/deb/snap
- [ ] **核心坑**：主进程/渲染进程隔离、`contextIsolation: true`、禁用 `nodeIntegration`
- **知名案例**：VS Code、Slack、Discord、Figma、Notion、Obsidian
- 文档：https://www.electronjs.org/docs/latest

---

## 3. Tauri 开发操作清单（重点，2024-2026 新星）

- [ ] **前置**：[Rust](https://www.rust-lang.org/) + Node.js + 系统 WebView
  - Win: WebView2（内置）
  - Mac: WKWebView
  - Linux: WebKitGTK
- [ ] **脚手架**：`npm create tauri-app@latest`（https://tauri.app/）
- [ ] **打包**：
  - Win → MSI/NSIS
  - Mac → DMG/App
  - Linux → deb/AppImage
  - **包体 3-10 MB**（Electron 的 1/10）
- [ ] **特性**：安全 IPC（`invoke`/`command`）、细粒度权限、自动更新
- [ ] **版本**：Tauri 2.x 已支持移动端（iOS/Android）

**何时选 Tauri**：追求小包体/低内存/强安全/启动快；前端已有 Web 资产
**何时仍选 Electron**：需要海量 npm 原生模块、团队不懂 Rust

---

## 4. Python 桌面（PySide6）操作清单

- [ ] **前置**：Python 3.9+，`pip install PySide6`
- [ ] **开发**：
  - [Qt Designer](https://doc.qt.io/qtforpython-6/) 设计 `.ui` → `pyside6-uic` 生成代码
  - `QThread` + 信号槽分离耗时任务
  - 布局用 `QVBoxLayout`/`QGridLayout`
- [ ] **打包**：
  - [PyInstaller](https://pyinstaller.org/)：`pyinstaller --onefile --windowed`（最常用）
  - [Nuitka](https://nuitka.net/)：编译为 C 二进制（商用推荐）
- 文档：https://doc.qt.io/qtforpython-6/

---

## 5. 代码签名与公证（最易踩坑！）

### Windows
- **Authenticode 证书**：
  - **OV**（组织验证）：几百美元/年
  - **EV**（扩展验证）：更贵但**立免 Smart Screen 警告**
- OV 新证书需积累下载量才能通过 Smart Screen 信誉
- 建议用 Azure Trusted Signing 或硬件令牌（EV 强制）
- 文档：https://learn.microsoft.com/windows-hardware/drivers/install/authenticode

### macOS
- **Apple Developer Program**：$99/年
- 必须用 **Developer ID Application** 证书签名
- 发布前强制**公证（Notarization）**：`xcrun notarytool submit`
- Gatekeeper 拦截未签名/未公证应用
- 用户需右键"打开"绕过（体验差）
- 文档：https://developer.apple.com/developer-id/

### Linux
- 无强制签名
- 推荐：
  - [Flatpak](https://flatpak.org/)（Flathub 分发，沙箱）
  - [Snap](https://snapcraft.io/)（Snap Store，自动更新）
  - AppImage（单文件免安装）

---

## 6. 分发渠道

| 渠道 | 成本 | 特点 |
|------|------|------|
| **官网下载** | 免费 | GitHub Releases / CDN / Cloudflare R2，需自推广 |
| **Microsoft Store** | 个人 $19 一次性 | Windows 生态 |
| **Mac App Store** | $99/年 | 沙箱限制严格 |
| **Snap Store / Flathub** | 免费 | Linux，需审核 |
| **国内分发** | 需软著+企业资质 | 腾讯软件中心、360、华为应用市场 |

---

## 7. 成本与时间估算

| 项目 | 个人工具 MVP | 跨平台商业软件 |
|------|------------|--------------|
| 开发人天 | 1-3 天（单平台） | 20-60 天（含签名、自动更新、CI/CD） |
| 签名证书年费 | Win $200-700 + Mac $99 | 同左 |
| 分发成本 | 官网免费 | 商店抽成 |

> **个人开发者**：可先用未签名分发，积累用户后再签

---

## 8. 推荐组合（精简优先）

| 场景 | 推荐栈 |
|------|--------|
| **最快上线且生态成熟** | Electron |
| **小包体/高性能/安全** | Tauri |
| **纯原生体验且会 Python** | PySide6 |
| **只做 Windows 企业内网** | .NET (WPF/WinUI) |
| **只做 Mac** | SwiftUI |
| **跨端（含移动）一致性** | Flutter |

---

## 官方文档速查
- Electron：https://www.electronjs.org/docs/latest
- Tauri：https://tauri.app/
- PySide6：https://doc.qt.io/qtforpython-6/
- PyInstaller：https://pyinstaller.org/
- Nuitka：https://nuitka.net/
- Apple Developer ID：https://developer.apple.com/developer-id/
- Authenticode：https://learn.microsoft.com/windows-hardware/drivers/install/authenticode
- Flatpak：https://flatpak.org/
- Snap：https://snapcraft.io/

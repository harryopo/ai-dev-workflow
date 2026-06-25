# 工具对比指南 — 网站捕获工具选型

## 工具概览

| 工具 | 适用场景 | 优势 | 劣势 | 安装方式 |
|------|----------|------|------|----------|
| **HTTrack** | 传统多页网站、博客、文档站 | 完整镜像，保持链接结构，断点续传 | 不支持 JS 渲染，Windows 需单独安装 | `winget install httrack` 或官网下载 |
| **wget** | 简单静态站、批量下载 | 命令行友好，几乎所有系统预装，递归下载 | 不支持 JS，链接处理有限，无 GUI | Linux 预装，Windows: `choco install wget` |
| **Playwright** | React/Vue/Angular SPA | 完整 JS 渲染，API 拦截，跨浏览器 | 需要 Node.js，首次安装下载 Chromium（~150MB） | `npm i playwright` |
| **Puppeteer** | React/Vue SPA | Google 官方，Chrome 深度集成 | 仅支持 Chrome/Chromium | `npm i puppeteer` |
| **SingleFile** | 单页面保存 | 完美保存单页，CLI 和浏览器扩展 | 不适合整站多页面 | `npm i single-file-cli` |
| **ArchiveBox** | 网页存档 | 多引擎支持，持久化存储 | 配置复杂，需要 Docker | `pip install archivebox` |

## 决策流程图

```
用户提供目标网站 URL
  │
  ├── 静态网站（无 JS 框架特征）？
  │   ├── YES → HTTrack 可用？
  │   │   ├── YES → 使用 HTTrack 完整镜像
  │   │   └── NO → wget 可用？
  │   │       ├── YES → 使用 wget --mirror
  │   │       └── NO → 使用 Python requests 脚本
  │   │
  │   └── NO → 动态 SPA（React/Vue/Angular 等）
  │       ├── Playwright 或 Puppeteer 可用？
  │       │   ├── YES → 使用 Playwright 捕获 + API 拦截
  │       │   └── NO → 安装 Playwright 或降级为静态抓取
  │       │
  │       └── 需要捕获 API 端点？
  │           ├── YES → Playwright 拦截模式（必须）
  │           └── NO → HTTrack 也可尝试（但 JS 内容会丢失）
```

## 各工具详细说明

### HTTrack

**最佳场景：** 传统多页网站、WordPress、文档站。

**优点：**
- 完整镜像整个网站，包括目录结构
- 自动修正内部链接为相对路径
- 支持断点续传
- 可配置深度、文件类型过滤

**注意事项：**
- 无法执行 JavaScript，SPA 内容完全不可见
- Windows 上需要手动安装
- 某些网站的反爬机制可能阻止 HTTrack

**典型命令：**
```bash
httrack "https://example.com" -O "./output" --depth=3 --stay-on-same-address "+*.css" "+*.js" "+*.png" "+*.jpg"
```

### Playwright

**最佳场景：** React/Vue/Angular SPA、需要 API 拦截的场景。

**优点：**
- 完整渲染 JavaScript，捕获 SPA 内容
- 可拦截所有网络请求，获取 API 端点
- 支持 Chrome/Firefox/WebKit
- 可模拟点击、填表、导航等用户操作

**注意事项：**
- 首次安装需下载 Chromium（~150MB）
- 比 HTTrack 慢（需要渲染每个页面）
- 默认无头模式可能被某些网站检测

**典型代码：**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 拦截 API 响应
    api_calls = []
    page.on('response', lambda r: api_calls.append(r) if 'application/json' in r.headers.get('content-type', '') else None)

    page.goto('https://example.com', wait_until='networkidle')
    html = page.content()
    browser.close()
```

### wget

**最佳场景：** 简单静态站点、无 HTTrack 时的备选。

**优点：**
- 几乎所有 Linux 预装
- 支持递归镜像
- 可转换链接为本地路径

**注意事项：**
- 对复杂 JS 站点无效
- 链接转换有时不完美
- Windows 需要额外安装

**典型命令：**
```bash
wget --mirror --page-requisites --convert-links --adjust-extension --no-parent --wait=1 "https://example.com"
```

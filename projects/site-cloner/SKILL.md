---
name: "site-cloner"
description: "网站全栈复刻工具。先深度调研网站定位/功能/模块，再让用户选择复刻范围和深度，最后执行精准复刻。当用户说'复刻网站/克隆网站/扒站/整站下载/仿站/clone website'时调用。"
---

# Site Cloner — 网站全栈复刻工具 (v1.4.0)

**先理解，再复刻。** 不是盲目抓取，而是先深度调研网站的定位、功能、模块、交互逻辑，输出完整的网站分析报告，让用户选择复刻范围和深度后，再精准执行。

## 核心原则

> **调研先行，精准复刻。**
>
> **七大铁律：**
> 1. **先调研再动手** — 必须先通览整个网站，理解定位/功能/模块，输出调研报告
> 2. **用户选择复刻范围** — 不默认全量复刻，让用户基于调研结果做决策
> 3. **智能理解功能** — 分析每个按钮/链接的功能含义，不只是复制 HTML
> 4. **区分前后端需求** — 识别哪些功能需要后端接口，哪些只需前端展示
> 5. 所有内容来自目标网站的真实抓取，绝不凭空编造
> 6. 复刻不了的部分，用占位标记标注说明，诚实告知用户
> 7. 优先使用开源工具链，不重复造轮子

## 工具链（开源项目集成）

按优先级使用以下工具，不重复造轮子：

| 优先级 | 工具 | 用途 | GitHub |
|--------|------|------|--------|
| ★★★ | **SingleFile** | 页面保存为单个 HTML（含所有资源） | [gildas-lormeau/SingleFile](https://github.com/gildas-lormeau/SingleFile) (15k★) |
| ★★★ | **website-scraper** | Node.js 静态站批量下载 | [website-scraper/node-website-scraper](https://github.com/website-scraper/node-website-scraper) (2k★) |
| ★★ | **goclone** | Go 极速网站镜像 | [goclone-dev/goclone](https://github.com/goclone-dev/goclone) (2.1k★) |
| ★★ | **Playwright** | 动态 SPA 渲染 + API 拦截 | [microsoft/playwright](https://github.com/microsoft/playwright) |
| ★ | **HTTrack/wget** | 传统静态站镜像 | 系统预装 |

### 工具选择策略

```
用户说"复刻网站"
    │
    ├── 第一步：SingleFile 保存首页（最快最简单）
    │   → 生成单个 .html 文件，内含所有 CSS/JS/图片/字体
    │   → 用于快速分析网站结构和功能
    │
    ├── 第二步：分析 SingleFile 输出的 HTML
    │   → 识别网站类型（静态/SPA/SSR）
    │   → 识别技术栈
    │   → 识别功能模块
    │
    └── 第三步：按类型选择深度工具
        ├── 静态站 → website-scraper（Node.js）或 goclone（Go）
        ├── 动态 SPA → Playwright + API 拦截
        └── 混合站 → website-scraper（静态资源）+ Playwright（动态部分）
```

### SingleFile 使用方式

**方式1：用户手动另存为（最简单）**
- 用户在浏览器中 Ctrl+S → "网页，全部" → 保存
- 或安装 SingleFile 浏览器扩展 → 一键保存

**方式2：SingleFile CLI（自动化）**
```bash
# 安装
npm install -g single-file-cli

# 保存单个页面
single-file https://example.com output/page.html

# 保存多个页面
single-file https://example.com output/page1.html https://example.com/about output/page2.html
```

**方式3：通过 Playwright 调用 SingleFile 核心库**
```javascript
// 使用 SingleFile 的核心库在 Playwright 中执行
// 详见 scripts/singlefile_capture.js
```

### website-scraper 使用方式

```bash
# 安装
npm install website-scraper website-scraper-puppeteer

# Node.js 脚本调用
node -e "
const scrape = require('website-scraper');
scrape({
  urls: ['https://example.com'],
  directory: './output',
  recursive: true,
  maxRecursiveDepth: 3,
  subdirectories: [
    {directory: 'css', extensions: ['.css']},
    {directory: 'js', extensions: ['.js']},
    {directory: 'images', extensions: ['.jpg','.png','.svg','.gif','.webp']},
    {directory: 'fonts', extensions: ['.woff','.woff2','.ttf','.eot']}
  ]
});
"
```

**动态站支持：** 使用 `website-scraper-puppeteer` 插件
```javascript
const PuppeteerPlugin = require('website-scraper-puppeteer');
scrape({
  urls: ['https://example.com'],
  directory: './output',
  plugins: [new PuppeteerPlugin()]
});
```

### goclone 使用方式

```bash
# 安装
go install github.com/goclone-dev/goclone/cmd/goclone@latest
# 或 brew install goclone

# 镜像网站
goclone https://example.com

# 镜像并预览
goclone https://example.com --serve --open
```

---

## 工作流程

### 第一阶段：深度调研（Deep Research）★ 核心阶段

**目标：** 不是直接抓取，而是先**完整理解**这个网站是什么、做什么、怎么做的。

#### 步骤 1.1：环境检查

```bash
python --version && node --version && npx --version
where httrack 2>/dev/null || echo "HTTrack 未安装"
where wget 2>/dev/null || echo "wget 未安装"
npx playwright --version 2>/dev/null || echo "Playwright 未安装"
npx single-file --version 2>/dev/null || echo "SingleFile CLI 未安装（可选）"
where goclone 2>/dev/null || echo "goclone 未安装（可选）"
```

#### 步骤 1.2：首页通览

使用 WebFetch 获取首页，分析以下维度：

**A. 网站定位**
- 这是什么类型的网站？（企业官网/电商/SaaS/博客/社区/工具/落地页）
- 主要面向什么用户群体？
- 核心价值主张是什么？（一句话描述这个网站做什么）

**B. 整体结构**
- 导航栏有哪些一级菜单？
- 首页有哪些核心区块？（Hero/产品展示/客户案例/定价/关于我们/联系...）
- 页面底部有什么信息？

**C. 技术栈识别**

| 特征 | 网站类型 | 推荐工具 |
|------|----------|----------|
| `<div id="root">` / `__NEXT_DATA__` | React/Next.js SPA | Playwright + API 拦截 |
| `window.__NUXT__` | Nuxt.js SSR | Playwright |
| `<script src="main.xxx.js">` | Webpack/Vite SPA | Playwright + API 拦截 |
| 纯 HTML 无 JS 框架 | 传统静态站 | HTTrack / wget |
| `<meta generator="WordPress">` | WordPress | HTTrack + wget |

#### 步骤 1.3：登录墙检测与凭证获取

在逐页探索之前，先检测网站是否有登录墙（部分内容需要登录才能访问）。

**检测方式：**
- 导航到首页后，检查是否有"登录/Login/Sign In"按钮
- 检查是否有页面返回 401/403 或重定向到登录页
- 检查是否有"需要登录才能查看"的提示

**如果检测到登录墙：**

使用 AskUserQuestion 告知用户并获取凭证：

```
⚠️ 检测到该网站部分内容需要登录才能访问。

以下页面可能需要登录：
- /dashboard（控制台）
- /settings（设置页）
- /profile（个人中心）

请选择一种方式提供凭证：
```

**凭证获取方式（按优先级）：**

| 方式 | 操作 | 安全性 |
|------|------|--------|
| **方式1：Cookie** | 用户在浏览器登录后，F12 → Application → Cookies → 复制全部 | ⚠️ 最完整 |
| **方式2：Token** | 用户在浏览器登录后，F12 → Network → 找到请求头中的 Authorization: Bearer xxx | ⚠️ 精准 |
| **方式3：账号密码** | 用户提供账号密码，由 Playwright 自动登录 | ⚠️ 需信任 |
| **方式4：手动登录** | Playwright 打开浏览器，用户手动登录后继续 | ✅ 最安全 |
| **方式5：跳过登录** | 只复刻公开页面，跳过需要登录的部分 | ✅ 最安全 |

**Playwright 自动登录实现：**

```python
# 方式4：手动登录（推荐）
page.goto("https://example.com/login")
input("请在浏览器中手动登录，完成后按回车继续...")
# 登录后 page 对象保持会话，可以继续访问需要登录的页面

# 方式3：自动登录
page.goto("https://example.com/login")
page.fill('input[name="email"]', user_email)
page.fill('input[name="password"]', user_password)
page.click('button[type="submit"]')
page.wait_for_navigation()
```

**Cookie/Token 注入：**

```python
# 方式1：注入 Cookie
context.add_cookies([
    {'name': 'session_id', 'value': 'xxx', 'domain': 'example.com'},
    {'name': 'token', 'value': 'xxx', 'domain': 'example.com'}
])

# 方式2：注入 Token
page.set_extra_http_headers({
    'Authorization': 'Bearer xxx'
})
```

**安全提醒：**
- 凭证仅用于当前复刻任务，不会保存到任何文件
- 复刻完成后立即清除内存中的凭证
- 不要在代码中硬编码凭证

#### 步骤 1.4：逐页深度探索

**逐一访问**导航栏中的每个链接、首页中的每个按钮，记录：

```
页面功能地图：
├── 首页 (/)
│   ├── Hero 区：品牌标语 + CTA 按钮 → 跳转到 /products
│   ├── 产品展示区：3-4 个产品卡片 → 跳转到 /products/:id
│   ├── 客户案例区：Logo 轮播 → 跳转到 /case-studies
│   ├── 定价区：3 档定价卡片 → 跳转到 /pricing
│   └── 页脚：社交媒体链接 / 隐私政策 / 联系我们
├── 产品页 (/products)
│   ├── 产品列表 → 筛选/分类功能
│   └── 产品详情 (/products/:id) → 图片轮播 + 规格参数 + 购买按钮
├── 关于我们 (/about)
│   ├── 公司介绍
│   ├── 团队成员
│   └── 时间线/里程碑
├── 博客 (/blog)
│   ├── 文章列表 → 分页
│   └── 文章详情 (/blog/:id) → 评论区
├── 联系我们 (/contact)
│   └── 联系表单 → 需要后端 API
├── 登录/注册 (/login, /register)
│   └── 认证系统 → 需要后端 API
└── 其他页面...
```

#### 步骤 1.5：功能-接口分析

对每个页面/功能，分析：

| 功能 | 前端需要 | 后端需要 | 说明 |
|------|----------|----------|------|
| 静态展示页 | ✅ HTML/CSS/JS | ❌ 不需要 | 纯展示，无交互 |
| 产品列表 | ✅ 布局+样式 | ⚠️ 可选 | 可用静态数据，也可接 API |
| 搜索功能 | ✅ 搜索框 UI | ⚠️ 可选 | 可用前端过滤，也可接搜索 API |
| 登录/注册 | ✅ 表单 UI | ✅ 需要 | 必须有认证 API 才能工作 |
| 购物车 | ✅ 购物车 UI | ⚠️ 可选 | 可用 localStorage，也可接 API |
| 评论区 | ✅ 评论 UI | ✅ 需要 | 必须有评论 API |
| 联系表单 | ✅ 表单 UI | ⚠️ 可选 | 可用 mailto，也可接邮件 API |
| 支付流程 | ✅ 占位 UI | ❌ 不可复刻 | 涉及第三方，用占位标记 |
| 实时通知 | ✅ 占位 UI | ❌ 不可复刻 | WebSocket 实时推送 |

#### 步骤 1.6：输出调研报告

**必须输出以下报告，等待用户确认后再继续：**

```markdown
## 🔍 网站调研报告 — {网站名称}

### 网站定位
- **类型：** 企业官网 / 电商 / SaaS / ...
- **面向群体：** {目标用户}
- **核心功能：** {一句话描述}

### 技术栈
- **前端框架：** React / Vue / 传统 HTML / ...
- **CSS 方案：** Tailwind / Bootstrap / 自定义 / ...
- **构建工具：** Vite / Webpack / Next.js / ...
- **字体：** Inter / 自定义 / Google Fonts / ...

### 登录墙检测
- **是否需要登录：** 是 / 否
- **需要登录的页面：** /dashboard, /settings, /profile, ...
- **凭证获取方式：** Cookie / Token / 手动登录 / 跳过

### 功能模块地图

| # | 模块 | 页面 | 功能描述 | 前端 | 后端 |
|---|------|------|----------|------|------|
| 1 | 首页 Hero | / | 品牌展示+CTA | ✅ | ❌ |
| 2 | 产品展示 | /products | 产品列表+筛选 | ✅ | ⚠️ 可选 |
| 3 | 产品详情 | /products/:id | 图片+参数+购买 | ✅ | ⚠️ 可选 |
| 4 | 用户登录 | /login | 账号密码登录 | ✅ | ✅ 需要 |
| 5 | 购物车 | /cart | 加购+结算 | ✅ | ⚠️ 可选 |
| 6 | 博客 | /blog | 文章列表+详情 | ✅ | ⚠️ 可选 |
| 7 | 联系我们 | /contact | 联系表单 | ✅ | ⚠️ 可选 |
| 8 | 支付 | /checkout | 结算支付 | 🔴 占位 | ❌ 不可复刻 |

> ✅ = 必须复刻  ⚠️ = 可选（复刻前端时可预留接口）  🔴 = 不可复刻（用占位）

### 复刻建议
- **完全复刻（推荐）：** 复刻所有模块的前端，核心功能预留后端接口
- **仅前端展示：** 只复刻视觉外观，所有数据用静态快照
- **自定义选择：** 用户逐个选择要复刻的模块
```

---

### 第二阶段：用户决策（User Decision）

使用 AskUserQuestion 让用户选择：

**问题 1：复刻范围**
- 全部复刻（所有模块）
- 大多数模块（跳过次要页面）
- 核心模块（只复刻最重要的 3-5 个页面）
- 自定义选择（逐个勾选）

**问题 2：后端深度**
- 需要后端 API（为交互功能生成 Express.js 后端 + 真实数据）
- 不需要后端（只复刻前端外观，数据用快照）
- 部分需要（只为核心功能预留接口，其他用静态数据）

**问题 3：特殊功能处理**
- 登录/注册：是否需要模拟认证？
- 搜索功能：是否需要真实搜索 API？
- 表单提交：是否需要后端接收？
- 支付/第三方：用占位标记？

---

### 第三阶段：前端捕获（Frontend Capture）

**前置：** 用户已确认复刻范围。只捕获用户选择的模块。

#### 优先使用开源工具（不重复造轮子）

| 场景 | 推荐工具 | 命令 |
|------|----------|------|
| 单页面快速保存 | **SingleFile CLI** | `npx single-file <url> output/page.html` |
| 静态站全量下载 | **website-scraper** | `node scripts/scrape_static.mjs <url> output/` |
| 静态站极速镜像 | **goclone** | `goclone <url> -o` |
| 动态 SPA + API 拦截 | **Playwright** | `python scripts/clone_dynamic.py <url> output/` |
| CDP 深度抓取 | **CDP Session** | `python scripts/cdp_deep_capture.py <url> output/` |
| 传统静态站 | **HTTrack/wget** | 见下方命令 |

#### SingleFile 保存（第一步，用于快速分析）

```bash
# 方式1：用户手动另存为（最简单）
# 方式2：SingleFile CLI
npx single-file https://example.com output/page.html

# SingleFile 保存的 HTML 包含所有资源（CSS/JS/图片/字体全部内联为 base64）
# 可以直接用 WebFetch 读取分析
```

#### website-scraper 批量下载（静态站首选）

```bash
node -e "
import scrape from 'website-scraper';
await scrape({
  urls: ['https://example.com'],
  directory: './output',
  recursive: true,
  maxRecursiveDepth: 3,
  subdirectories: [
    {directory: 'css', extensions: ['.css']},
    {directory: 'js', extensions: ['.js']},
    {directory: 'images', extensions: ['.jpg','.png','.svg','.gif','.webp']},
    {directory: 'fonts', extensions: ['.woff','.woff2','.ttf','.eot']}
  ]
});
"
```

#### goclone 极速镜像（备选）

```bash
goclone https://example.com --serve --open
```

#### HTTrack/wget（传统备选）

```bash
httrack "<URL>" -O "./output/<site_name>" \
  --depth=3 --ext-depth=1 --max-rate=250000 \
  --robots=0 --sockets=8 --stay-on-same-address \
  --disable-security-limits \
  "+*.png" "+*.gif" "+*.jpg" "+*.jpeg" "+*.webp" "+*.svg" \
  "+*.css" "+*.js" "+*.woff2" "+*.woff" "+*.ttf" "+*.eot" \
  "+*.otf" "+*.ico" "+*.json" "+*.xml"
```

#### 动态 SPA 捕获（Playwright）★

当网站是 React/Vue/Next.js 等 SPA 时，必须用 Playwright：

**如果调研阶段检测到登录墙，先注入凭证再捕获：**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    # 注入凭证（如果用户提供了）
    if cookies:
        context.add_cookies(cookies)
    if token:
        context.set_extra_http_headers({'Authorization': f'Bearer {token}'})

    page = context.new_page()

    # 如果需要手动登录
    if need_manual_login:
        browser = p.chromium.launch(headless=False)  # 有头模式
        page.goto(login_url)
        input("请在浏览器中手动登录，完成后按回车...")
        # 登录后 page 保持会话

    # 开始捕获用户选择的页面
    page.goto(target_url, wait_until='networkidle')
```

由 `scripts/clone_dynamic.py` 实现，只遍历用户选择的页面：

| 函数 | 提取内容 |
|------|----------|
| `extract_css_snapshot(page)` | CSS 变量、@keyframes、@font-face、@media |
| `extract_font_capture(page)` | 字体族、Google Fonts、字体文件 URL |
| `extract_interaction_capture(page)` | 表单校验、动效元素、事件处理器 |
| `extract_design_tokens(page)` | 颜色、排版、间距、阴影、圆角 |
| `capture_rendered_html(page)` | 渲染后的完整 DOM |

#### 捕获后处理

1. 路径修正（绝对→相对）
2. 资源重组（css/js/images/fonts）
3. CDN 本地化
4. API URL 重写 → `/api/`
5. CSS 变量注入 → `:root {}`
6. 字体本地化 → `@font-face { src: local(...) }`
7. 动效保留
8. 设计 Token 固化 → `design-tokens.css`

---

### 第四阶段：API 逆向与后端重建

**前置：** 用户在第二阶段选择了需要后端 API。

#### 步骤 4.1：API 端点采集

从 Playwright 拦截 + 用户选择的功能模块中提取 API：

```json
{
    "endpoint": "/api/users",
    "method": "GET",
    "response_body": [{"id": 1, "name": "真实数据"}],
    "belongs_to_module": "用户登录",
    "user_wants_backend": true
}
```

#### 步骤 4.2：按模块组织 API

```
API 模块映射：
├── 用户模块
│   ├── POST /api/login        → 登录
│   ├── POST /api/register     → 注册
│   └── GET  /api/me           → 当前用户
├── 产品模块
│   ├── GET  /api/products     → 产品列表
│   ├── GET  /api/products/:id → 产品详情
│   └── GET  /api/search       → 搜索
├── 博客模块
│   ├── GET  /api/posts        → 文章列表
│   └── GET  /api/posts/:id    → 文章详情
└── 联系模块
    └── POST /api/contact      → 提交联系表单
```

#### 步骤 4.3：生成后端

使用 `scripts/reconstruct_backend.py` 自动生成 Express.js 后端：
- 路由文件按模块拆分
- 数据文件来自真实 API 响应快照
- 认证中间件（如果用户需要登录功能）
- CORS 配置

**绝对禁止：** 虚构数据、Lorem Ipsum、占位符文本。

---

### 第五阶段：前端重建

#### 步骤 5.1：按用户选择重建

| 用户选择 | 策略 |
|----------|------|
| 需要后端 | API 地址 → `/api/`，连接本地后端 |
| 不需要后端 | 数据用 API 响应快照内嵌到 HTML/JS |
| 部分需要 | 核心功能接 API，其他用快照 |

#### 步骤 5.2：智能功能理解

对用户选择的每个交互功能，分析并实现：

```
按钮/功能 → 理解 → 实现策略：
├── "立即购买" 按钮 → 电商下单 → 用户选择：接API / 占位
├── "免费试用" 按钮 → 注册引导 → 用户选择：接注册API / 跳转
├── "联系我们" 表单 → 信息提交 → 用户选择：接邮件API / mailto
├── "搜索" 输入框 → 内容搜索 → 用户选择：接搜索API / 前端过滤
├── "下载" 按钮 → 文件下载 → 提供真实文件或占位
├── "分享" 按钮 → 社交分享 → Web Share API 或链接
└── "播放" 按钮 → 媒体播放 → 保留URL或占位封面
```

#### 步骤 5.3：诚实降级

复刻不了的功能用占位标记：
- 🔴 支付流程 → `<button disabled>购买 (不可用)</button>`
- 🔴 OAuth 登录 → JWT 模拟 + `/* [简化] OAuth→JWT */`
- 🔴 验证码 → 移除 + `/* [简化] 已移除CAPTCHA */`
- 🔴 实时推送 → 静态数据 + `/* [快照] 非实时 */`

---

### 第六阶段：验证与报告

#### 步骤 6.1：启动验证

```bash
cd output/<site_name>/backend && npm install && node server.js &
cd output/<site_name>/frontend && npx serve . -p 3000
```

#### 步骤 6.2：保真验证

| 类别 | 验证项 | 标准 |
|------|--------|------|
| 布局 | 页面结构/响应式 | 元素位置一致 |
| 颜色 | 主色/渐变 | ΔE < 5 |
| 字体 | 字体族/字号/字重 | 数值一致 |
| 间距 | margin/padding | px 一致 |
| 阴影/圆角 | box-shadow/border-radius | 一致 |
| 动效 | transition/animation | 时长/缓动一致 |
| 交互 | 按钮/表单/导航 | 行为一致 |
| 数据 | API 返回结构 | 一致 |
| 图片 | 所有图片 | 无 404 |

#### 步骤 6.3：生成报告

```markdown
## 复刻报告 — {网站名称}

### 调研结果
- 网站类型：{类型}
- 技术栈：{技术栈}
- 总页面数：{N} 个

### 复刻范围
- 用户选择：{全部/大多数/核心/自定义}
- 实际复刻：{N} 个模块，{M} 个页面

### 后端情况
- 用户选择：{需要/不需要/部分需要}
- 生成 API：{N} 个端点
- 数据来源：真实 API 响应快照

### 保真度
- 整体：{X}%
- 前端：{X}%
- 后端：{X}%

### 诚实降级
- 🟢 完整复刻：{N} 项
- 🟡 推断实现：{N} 项
- 🔴 占位标记：{N} 项

### 运行方式
cd output/{name}/backend && npm install && node server.js
cd output/{name}/frontend && npx serve . -p 3000
```

---

## 辅助脚本

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `scripts/scrape_static.mjs` | website-scraper 封装（静态站首选） | Node.js, website-scraper |
| `scripts/clone_dynamic.py` | Playwright SPA 捕获 + CSS/字体/交互/设计Token | Python, Playwright |
| `scripts/cdp_deep_capture.py` | CDP DevTools 深抓（POST body/WebSocket 帧） | Python, Playwright |
| `scripts/analyze_apis.py` | API 端点分析 + 数据模型推断 | Python |
| `scripts/reconstruct_backend.py` | Express.js 后端代码生成 | Python |
| `scripts/clone_static.py` | Python 备选（当 Node.js 不可用时） | Python, requests, bs4 |

---

## 禁止行为

- ❌ **禁止跳过调研直接抓取** — 必须先理解网站再动手
- ❌ **禁止默认全量复刻** — 必须让用户基于调研结果做选择
- ❌ **禁止凭空编造内容** — 不生成目标网站不存在的数据
- ❌ **禁止自创 API** — 不添加拦截中未发现的端点
- ❌ **禁止用 Lorem Ipsum** — 不用占位符文本冒充真实数据
- ❌ **禁止忽略错误** — 资源下载失败必须记录
- ❌ **禁止高频率请求** — 请求间隔 ≥ 500ms
- ❌ **禁止丢弃 CSS 变量/字体/动效** — 像素级保真
- ❌ **禁止伪装 100% 复刻** — 诚实告知未复刻/推断/占位的部分

---

## 参考资料

- 工具对比：`${SKILL_DIR}/references/tools-comparison.md`
- 后端重建：`${SKILL_DIR}/references/backend-reconstruction.md`
- 常见陷阱：`${SKILL_DIR}/references/common-pitfalls.md`
- 像素级保真：`${SKILL_DIR}/references/pixel-perfect-capture.md`
- agent-browser 协作：`${SKILL_DIR}/references/skill-collaboration.md`
- 详细示例/版本历史：[README.md](./README.md)

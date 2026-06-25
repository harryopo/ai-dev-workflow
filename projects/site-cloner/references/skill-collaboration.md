# Skill 协作指南 — site-cloner × agent-browser 协作模式

## 概述

site-cloner 可以与已安装的 **agent-browser** Skill 深度协作，利用真实浏览器的 DevTools 能力实现更强的抓取效果。

## 协作架构

```
┌─────────────────────────────────────────────────┐
│                   site-cloner                    │
│  (指挥中心：分析/决策/代码生成)                   │
│                                                  │
│  1. 接收用户请求 "复刻 xxx.com"                   │
│  2. 分析网站类型，判断需要 agent-browser 协助      │
│  3. 通过 Skill 工具调用 agent-browser             │
│  4. 接收 agent-browser 的截图/DOM/网络数据        │
│  5. 分析 API、生成后端、重建前端                  │
│  6. 最终验证（再次调用 agent-browser 截图对比）    │
└──────────────┬──────────────────────────────────┘
               │ Skill 工具调用
               ▼
┌─────────────────────────────────────────────────┐
│                 agent-browser                    │
│  (执行引擎：浏览器控制/网络拦截/截图)              │
│                                                  │
│  - 启动 Chromium 浏览器（headless 或有头）        │
│  - 打开目标 URL，等待完整渲染                     │
│  - CDP Network 域拦截所有请求                     │
│  - 执行用户交互（点击/填表/滚动）                  │
│  - 截取全页/元素截图                              │
│  - 提取 DOM 内容                                  │
│  - 返回数据给 site-cloner                         │
└─────────────────────────────────────────────────┘
```

## 何时使用协作模式

| 场景 | 单独使用 site-cloner | 协作 agent-browser |
|------|---------------------|-------------------|
| 静态 HTML 网站 | ✅ 直接 HTTrack/wget | 不需要 |
| 简单 SPA (纯展示) | ✅ Playwright | 可选 |
| **复杂 SPA (大量 API)** | ⚠️ 可能遗漏 POST body | ✅ 推荐 |
| **需要点击触发隐藏 API** | ❌ 不易发现 | ✅ 必须 |
| **有 WebSocket** | ❌ Playwright 不支持 | ✅ CDP 可捕获 |
| **需要对比原始vs复刻** | ⚠️ 手动对比 | ✅ 自动截图对比 |
| **需要填写表单触发** | ❌ 需单独写脚本 | ✅ 可视化操作 |
| **有登录/认证页面** | ⚠️ 需手动处理 | ✅ 可录制登录流程 |

## 协作流程详解

### 第一步：site-cloner 发起协作

site-cloner 检测到以下条件之一时，自动提示用户启用协作模式：

1. 目标网站使用 React/Vue/Angular 等 SPA 框架
2. 页面包含大量按钮/表单（暗示有交互 API）
3. 检测到 WebSocket 连接
4. 用户要求 "交互也要一样"

### 第二步：agent-browser 打开网站

```
调用方式：Skill 工具 → agent-browser
传递参数：目标 URL、视口大小、是否 headless
```

agent-browser 启动 Chromium 并打开目标 URL，等待 `networkidle`。

### 第三步：深度网络拦截

agent-browser 通过 CDP `Network.enable` 启用网络监控，捕获：

- `Network.requestWillBeSent` — 所有请求（含完整请求头）
- `Network.responseReceived` — 响应头、状态码、MIME 类型
- `Network.loadingFinished` — 加载完成，触发 `Network.getResponseBody`
- `Network.getRequestPostData` — POST/PUT 请求体

### 第四步：交互式 API 发现

site-cloner 分析 DOM 中的可交互元素，指示 agent-browser 逐个触发：

```
可触发元素类型 → 发现的 API：
- 加载更多按钮 → GET /api/items?page=2
- 搜索框+提交 → GET /api/search?q=keyword
- 筛选下拉 → GET /api/items?category=X
- 表单提交 → POST /api/submit
- 删除按钮 → DELETE /api/item/:id
- 点赞按钮 → POST /api/like/:id
- 评论提交 → POST /api/comment
- 文件上传 → POST /api/upload
```

### 第五步：截图对比验证

1. agent-browser 截取原始网站全页截图
2. site-cloner 完成复刻
3. agent-browser 打开复刻版本 (`http://localhost:3000`)
4. 截取复刻版本全页截图
5. 对比两张截图，识别差异区域
6. 如果有差异 → 自动重新捕获差异区域

### 第六步：生成复刻报告

site-cloner 综合所有数据（网络拦截+交互发现+截图对比+CDP深抓），生成完整复刻报告。

## 工具调用示例

```
# site-cloner 内部调用 agent-browser 的伪代码：

1. Skill("agent-browser")         # 启动 agent-browser
2. agent_browser.navigate(url)    # 导航到目标URL
3. agent_browser.screenshot()     # 截取首页
4. agent_browser.get_network_calls()  # 获取网络请求
5. agent_browser.click(".btn-load-more")  # 点击加载更多
6. agent_browser.get_network_calls()  # 获取新触发的请求
7. agent_browser.fill_form("#search", "keyword")  # 填写搜索
8. agent_browser.click("#search-btn")  # 点击搜索
9. agent_browser.get_network_calls()  # 获取搜索API
10. ... (遍历所有可交互元素)
```

## 降级策略

当 agent-browser 不可用时：

1. 尝试内置 Playwright 模式
2. Playwright 不可用 → 尝试 wget/HTTrack
3. 所有浏览器工具不可用 → 静态 HTML 抓取
4. 告知用户降级情况和建议安装 agent-browser

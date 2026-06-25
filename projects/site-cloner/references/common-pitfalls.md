# 常见陷阱与解决方案

## 陷阱 1：SPA 捕获的 HTML 是空的

**现象：** 使用 curl/wget 获取 SPA 页面，HTML 中只有 `<div id="root"></div>`。

**原因：** React/Vue 等框架在客户端通过 JavaScript 渲染内容，curl/wget 不执行 JS。

**解决：** 使用 Playwright 或 Puppeteer 渲染页面：
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until='networkidle')
    html = page.content()  # 获取渲染后的完整 HTML
    browser.close()
```

## 陷阱 2：相对路径变成绝对路径导致资源 404

**现象：** 下载到本地的网站，图片/JS/CSS 全部 404。

**原因：** 页面中的资源使用了绝对 URL（`https://example.com/style.css`）或根路径（`/style.css`）。

**解决：**
1. HTTrack/wget 使用 `--convert-links` 参数自动转换
2. 手动替换：将所有 `https://原始域名/` 替换为 `./` 或相对路径
3. 对于根路径，确保本地服务器从项目根目录启动

## 陷阱 3：API 请求跨域被阻止

**现象：** 页面加载后 API 请求报 CORS 错误。

**原因：** 前端页面运行在 `localhost:3000`，后端在 `localhost:5000`，浏览器阻止跨域请求。

**解决：** 后端添加 CORS 中间件：
```javascript
// Express.js
const cors = require('cors');
app.use(cors({ origin: '*' }));

// Python Flask
from flask_cors import CORS
CORS(app)
```

## 陷阱 4：CDN 资源未下载

**现象：** 网站使用了 CDN 的 JS 库（如 Bootstrap CDN、Google Fonts），本地无法访问。

**原因：** HTTrack 的 `--stay-on-same-address` 参数跳过了外部域名资源。

**解决：**
1. 不使用 `--stay-on-same-address`（但可能下载大量无关内容）
2. 手动识别 CDN 资源并下载到本地
3. 替换 CDN 链接为本地路径

## 陷阱 5：PostCSS/Tailwind 类丢失

**现象：** Playwright 捕获的 SPA 页面样式正确，但保存为 HTML 后部分样式丢失。

**原因：** 现代构建工具使用动态注入的 CSS（style 标签注入或 CSS-in-JS），保存的 HTML 可能不包含注入的样式。

**解决：**
1. Playwright 捕获时执行 `page.content()` 获取完整 DOM（含注入的 style 标签）
2. 额外保存 `document.styleSheets` 的内容
3. 将提取的样式写入单独的 CSS 文件

## 陷阱 6：图片懒加载导致未下载

**现象：** 长列表页面的图片只下载了前几张。

**原因：** 现代网站使用 `loading="lazy"` 或 Intersection Observer 实现懒加载。

**解决：**
1. Playwright 滚动到页面底部触发懒加载
```python
await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
await page.wait_for_timeout(2000)  # 等待图片加载
```
2. 移除 `loading="lazy"` 属性
3. 将 `data-src` 替换为 `src`

## 陷阱 7：字体文件跨域

**现象：** @font-face 引用的 WOFF2 文件下载失败。

**原因：** 字体文件通常托管在 CDN 上，浏览器有跨域限制。

**解决：**
1. 下载字体文件到本地
2. 修改 CSS 中的 @font-face url 指向本地文件
3. 确保本地服务器返回正确的 Content-Type

## 陷阱 8：反爬虫机制

**现象：** 请求 403 或被 Cloudflare 验证拦截。

**原因：** 目标网站有反爬机制。

**解决：**
1. 使用真实的 User-Agent 头
2. 添加合理的请求间隔（≥ 500ms）
3. Playwright 使用 `headless: false` 有时能绕过
4. 尊重网站的 robots.txt 和反爬意图
5. 如果无法绕过，告知用户并记录在报告中

## 陷阱 9：复刻后表单提交无效

**现象：** 点击提交按钮无反应或报错。

**原因：**
1. 前端 JS 事件监听器可能丢失
2. API 地址未正确替换
3. CSRF token 缺失

**解决：**
1. 检查 Network 面板确认请求是否发出
2. 确保 API 地址已替换为本地端点
3. 移除 CSRF token 验证（本地开发环境）
4. 检查表单 action 属性是否指向本地

## 陷阱 10：动态路由页面被遗漏

**现象：** 只有首页被捕获，其他页面丢失。

**原因：** SPA 的路由是客户端控制的，工具无法自动发现所有路由。

**解决：**
1. 从页面提取所有 `<a>` 标签的 href
2. 手动列出所有需要捕获的路由
3. Playwright 逐个访问并保存
4. 检查 sitemap.xml（如果存在）

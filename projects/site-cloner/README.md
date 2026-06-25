# Site Cloner — 网站全栈复刻工具 v1.2.0

> 完整复刻目标网站的前后端。前端通过 HTTrack/wget/Playwright+CDP 抓取，后端通过拦截 API 请求逆向分析重建。能复刻就复刻，复刻不了诚实告知+占位。

---

## 市场定位

**Claude Code Skill 生态唯一全栈复刻方案。**

经调研 GitHub `awesome-claude-code` (46k★) 及 Claude Code Skill 市场，目前无其他 Skill 实现前端+后端+设计Token 全量复刻。

| 方案 | 类型 | 前端 | 后端 | 设计Token | CSS变量 | 字体下载 | 交互记录 | 诚实降级 |
|------|------|------|------|-----------|---------|----------|----------|----------|
| **site-cloner** | Claude Code Skill | ✅全量 | ✅API逆向重建 | ✅自动提取 | ✅全量 | ✅完整 | ✅完整 | ✅v1.2.0 |
| ai-website-cloner-template (12k★) | GitHub模板 | ✅Next.js重构 | ❌无 | ❌无 | ❌丢失 | ❌丢失 | ❌无 | ❌无 |
| goclone (2.1k★) | Go CLI | ✅静态 | ❌无 | ❌无 | ❌丢失 | ❌部分 | ❌无 | ❌无 |
| webcloner-js | TS CLI | ✅静态+代理 | ❌无 | ❌无 | ❌丢失 | ✅部分 | ❌无 | ❌无 |
| HTTrack | C 应用 | ✅静态 | ❌无 | ❌无 | ❌丢失 | ❌无 | ❌无 | ❌无 |
| website-downloader (128★) | Python脚本 | ✅静态 | ❌无 | ❌无 | ❌丢失 | ❌部分 | ❌无 | ❌无 |

---

## CDP vs Playwright 对比

| 能力 | Playwright page.on('response') | CDP Network.getResponseBody |
|------|------|------|
| 响应体获取 | ✅（仅 text/JSON） | ✅（任意格式含二进制） |
| 请求体获取 | ❌ 无法获取 POST body | ✅ Network.getRequestPostData |
| WebSocket 帧 | ❌ 不支持 | ✅ Network.webSocketFrameReceived |
| 请求时序 | ❌ 不支持 | ✅ 完整 timing 信息 |
| 重定向链 | ❌ 需手动处理 | ✅ 自动记录 |
| 缓存状态 | ❌ 不支持 | ✅ fromDiskCache/fromMemoryCache |
| 连接信息 | ❌ 不支持 | ✅ remoteIPAddress/connectionId |

---

## 局限性声明

本 Skill 无法复刻的内容（诚实告知）：

- 🔒 需要密钥/凭证的功能（支付、OAuth、第三方API）
- 🧠 AI/ML 模型推理结果
- 📡 实时数据流（WebSocket 持续推送）
- 🎬 DRM 保护的内容（加密视频/音频）
- 🔐 服务端闭源逻辑（编译后的后端代码）
- 📊 需要实时数据库的内容（仅能保存快照）
- 🤖 验证码/CAPTCHA
- 💳 任何涉及金钱交易的功能

这些不可复刻项会在输出中诚实标注，并提供最佳替代方案。

---

## 示例

### 示例 1：像素级复刻落地页

```
用户: 帮我完整复刻这个落地页 https://example-landing.com，UI/字体/动效全部一样
→ 侦察 → 静态站 + Google Fonts + CSS动画
→ HTML/CSS/JS 全量下载
→ 从 CSS 提取 @font-face（Inter + Playfair Display）
→ 下载 .woff2 字体文件到 fonts/
→ 提取所有 CSS 变量（--primary, --spacing-lg 等 24 个）
→ 提取 @keyframes（fadeIn, slideUp, scaleIn 3 个动画）
→ 提取 hover 态样式（按钮/卡片/链接）
→ 提取设计Token（7 色 + 8 层阴影 + 5 档圆角 + 6 级字号）
→ 修正所有路径 → 字体装回本地
→ 验证：颜色 ΔE<3 / 字体一致 / 动效时长一致
→ 完成：复刻版本与原始网站视觉上不可区分
```

### 示例 2：SPA 全栈复刻

```
用户: 克隆 https://example-dashboard.com，交互也要一样
→ 侦察 → React SPA + 12 个 API
→ Playwright 渲染 + API 拦截
→ CSS 计算样式完整提取
→ 字体 Inter/Geist 下载到本地
→ 交互记录：表单校验规则、按钮悬停色、下拉菜单 toggle
→ 后端重建：Express.js + 真实数据
→ 前端修正：API→/api/，字体→本地，CSS变量固化
→ 验证：所有交互行为与原始一致
→ 完成
```

### 示例 3：后端获取不到的情况

```
用户: 复刻 https://ssr-site.com
→ 侦察 → Next.js SSR，HTML 中包含服务端渲染数据
→ API 端点有限（大部分数据嵌入 HTML）
→ 从页面布局和交互按钮推断数据流:
  - "加载更多" 按钮 → 推断分页 API
  - 搜索框 → 推断搜索 API
  - 表单提交 → 推断创建 API
→ 标注 "/* 从页面行为推断 */"
→ 生成后端 mock 数据（基于页面上展示的真实数据）
```

---

## CSS 提取参考代码

以下是 Playwright 页面中执行的 CSS 提取核心逻辑（完整实现见 `scripts/clone_dynamic.py`）：

### CSS 自定义属性

```javascript
const rootStyles = getComputedStyle(document.documentElement);
const props = {};
for (let i = 0; i < rootStyles.length; i++) {
    const name = rootStyles[i];
    if (name.startsWith('--')) props[name] = rootStyles.getPropertyValue(name).trim();
}
```

### @keyframes / @font-face

```javascript
for (let sheet of document.styleSheets) {
    try {
        for (let rule of sheet.cssRules) {
            if (rule.type === CSSRule.KEYFRAMES_RULE) { /* 收集 keyframes */ }
            if (rule.type === CSSRule.FONT_FACE_RULE) { /* 收集 fontFaces */ }
        }
    } catch(e) {} // 跨域样式表会抛异常
}
```

### 设计Token提取

```javascript
// 颜色体系：扫描前1000元素的 color/backgroundColor/borderColor/boxShadow
// 排版层级：按 fontFamily|fontSize|fontWeight 去重
// 阴影体系：扫描 boxShadow 计算样式
// 圆角体系：扫描 borderRadius 计算样式
// 渐变体系：扫描 backgroundImage 中的 gradient
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.2.0 | 2026-06-22 | agent-browser协作模式 + CDP DevTools深度抓取 + 诚实降级机制 + 市场调研 |
| v1.1.0 | 2026-06-22 | 像素级保真：CSS/字体/交互/设计Token 全量提取 + 24项保真验证清单 |
| v1.0.0 | 2026-06-22 | 初始版本：六阶段工作流 |

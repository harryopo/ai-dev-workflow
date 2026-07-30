# GitHub Pages 部署完全指南

> 调研日期：2026-07-09
> 适用场景：静态网站、前端 SPA、文档站点、宣传落地页
> 不适用：有后端 API、数据库、服务端渲染的复杂系统

---

## 一、核心三问：快速答案

| 问题                     | 答案                                                                                   |
| ------------------------ | -------------------------------------------------------------------------------------- |
| 前后端复杂系统能部署吗？ | **不能。** 仅支持静态文件（HTML/CSS/JS），无 PHP/Python/Node.js 后端，无数据库。 |
| 只能放一个 HTML 文件吗？ | **不是。** 支持完整文件夹结构、多页面、多层级目录。                              |
| 支持文件夹吗？           | **完全支持。** 可部署任意深度的目录树。                                          |

---

## 二、三种部署方式

### 方式 1：`/docs` 文件夹部署（最推荐）

1. 将静态文件放到仓库 `docs/` 目录
2. 推送：`git push origin main`
3. GitHub → Settings → Pages → Source 选 `Deploy from a branch`
4. Branch 选 `main`，文件夹选 `/docs` → Save
5. 等待 1-2 分钟，访问 `https://用户名.github.io/仓库名/`

### 方式 2：`gh-pages` 分支部署

```bash
git checkout --orphan gh-pages
git rm -rf .
# 放入静态文件
git add . && git commit -m "deploy"
git push origin gh-pages
```

Settings → Pages → Branch 选 `gh-pages`。

### 方式 3：GitHub Actions 自动部署（CI/CD）

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
      - uses: actions/deploy-pages@v4
```

---

## 三、限制与约束

| 限制项     | 数值             |
| ---------- | ---------------- |
| 仓库总大小 | 1 GB（软限制）   |
| 单文件大小 | 100 MB           |
| 每月带宽   | 100 GB（软限制） |
| 每小时构建 | 10 次            |
| 构建超时   | 10 分钟          |
| 用途限制   | 禁止商业用途     |

---

## 四、全栈替代方案对比

| 平台                       | 适合场景                | 免费额度           | 亮点                                  |
| -------------------------- | ----------------------- | ------------------ | ------------------------------------- |
| **Vercel**           | React/Next.js/Vue 全栈  | 100GB 带宽/月      | Serverless Functions，GitHub 一键部署 |
| **Netlify**          | JAMstack + 表单         | 100GB 带宽/月      | 自带表单处理、身份认证                |
| **Cloudflare Pages** | 不限带宽需求            | **无限带宽** | Workers 做后端，全球 CDN 最快         |
| **Render**           | Express/Django 传统后端 | 750h/月            | 支持 Docker、PostgreSQL、Redis        |
| **Railway**          | 全栈 + 数据库           | $5 试用金          | 部署体验最丝滑，自带数据库            |
| **Fly.io**           | Docker 容器化部署       | 3 个免费 VM        | 全球边缘部署                          |

---

## 五、ai-dev-workflow 项目推荐

- **`docs/index.html` 宣传页**（纯静态 36KB）→ **GitHub Pages** 完全够用
- **如需后端 API 或数据库** → **Vercel**（Serverless Functions）或 **Railway**

当前宣传页部署失败是因为 MCP API 上传文件大小受限，本地文件完整可用。建议手动通过 git push 到 `gh-pages` 分支即可部署。
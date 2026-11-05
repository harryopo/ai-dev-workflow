# Web 开发与部署全流程指南

> 来源：第二轮调研 R3
> 用途：阶段 5 编码实施时的 Web 开发参考

## 1. 前端框架选型

| 框架 | 适用场景 | SEO | 学习成本 |
|------|----------|-----|----------|
| **Next.js** (React) | SaaS、动态站、全栈一体化 | 优秀（SSR/SSG/ISR） | 中 |
| **Nuxt** (Vue) | 内容站、管理后台、Vue 生态 | 优秀 | 中 |
| **SvelteKit** | 高性能轻量应用 | 优秀 | 低 |
| **Astro** | 内容站、博客、文档、营销页 | 极佳（默认零 JS） | 低-中 |
| **Remix** | 数据驱动 Web App、表单密集 | 优秀 | 中 |
| **Hexo/Hugo**（静态） | 个人博客、文档站 | 极佳 | 低 |

> **选型要点**：内容/SEO 优先 → Astro 或 Hugo；交互应用 → Next.js/Nuxt；追求体积 → SvelteKit

---

## 2. 后端方案

| 方案 | 适用场景 | 优点 |
|------|----------|------|
| **全栈框架内置 API**（Next API Routes） | 中小项目、单人开发 | 同仓库、零运维 |
| **独立后端**（Node/Python/Go/Rust） | 复杂业务、微服务 | 解耦、可独立扩展 |
| **BaaS**（Supabase/Firebase） | MVP、实时应用、无后端工程师 | 认证/数据库/存储开箱即用 |
| **Serverless**（Cloudflare Workers/Vercel Functions） | 事件驱动、低频访问 | 按调用付费、自动伸缩 |

> **快速上线 → BaaS**；稳定增长 → 独立后端；流量波动大 → Serverless

---

## 3. 免费部署方案（重点）

### Vercel（Next.js 原生）
1. 注册 Vercel → New Project
2. Import Git 仓库 → 自动识别框架 → 一键 Deploy
3. 绑定自定义域名（CNAME）
- **免费层（Hobby）**：带宽 100 GB/月；函数 100k/月；构建 6000 分钟/月
- ⚠️ 不支持商业用途
- 文档：https://vercel.com/docs

### Cloudflare Pages + Workers（额度最慷慨）
1. 登录 Cloudflare → Pages → Connect Git
2. 设置构建命令 + 输出目录
3. Workers：`npx wrangler deploy`
- **免费层**：Pages **无限请求、无限带宽**；Workers 100k 请求/天；D1 5GB；R2 10GB
- 文档：https://developers.cloudflare.com/pages/

### Netlify
- 连接 Git → 自动部署
- 免费层：带宽 100 GB/月、构建 300 分钟/月、函数 125k/月

### GitHub Pages（纯静态）
- 仓库 Settings → Pages → 选择分支
- 免费、1 GB 仓库、100 GB/月带宽

### 国内：腾讯云 CloudBase
- 静态网站托管、Serverless
- 免费试用额度、国内访问快

---

## 4. 自建部署操作清单

### VPS + Docker + Nginx
1. 购买 VPS（阿里云/腾讯云/Vultr/Hetzner）
2. 安装 Docker：`curl -fsSL https://get.docker.com | sh`
3. 编写 `Dockerfile` + `docker-compose.yml`
4. Nginx 反向代理：转发 80/443 → 容器端口
5. 启动：`docker compose up -d`

### 域名注册
- 阿里云/腾讯云（国内，需实名）
- Cloudflare（国际，域名+DNS+CDN 一站式）

### SSL 证书（免费）
- **Let's Encrypt**：`certbot --nginx` 自动签发，90 天自动续期
- **Cloudflare**：Full/Full Strict 模式，边缘证书免费自动续期

### ICP 备案（国内服务器必须）
- **材料**：身份证、域名证书、服务器实例、备案核验单、幕布拍照
- **周期**：约 7-20 个工作日
- **如何避开**：境外服务器 + Cloudflare CDN（访问速度略降，免备案）

---

## 5. 一键部署工具

| 平台 | 定位 | 免费层 |
|------|------|--------|
| **Vercel** | 前端/全栈首选，Git Push 即部署 | Hobby 免费（限个人） |
| **Cloudflare Pages/Workers** | 静态 + 边缘计算 | **最慷慨**（无限带宽） |
| **Railway** | 后端/数据库一键 | 试用额度（约 $5/月） |
| **Render** | Web Service | 免费层（512MB，闲置休眠） |
| **Coolify** | 开源自建 PaaS | 完全免费（仅服务器成本） |

---

## 6. 数据库选型

| 类型 | 推荐 | 托管服务 |
|------|------|---------|
| 关系型 | PostgreSQL、SQLite | Supabase、Neon、PlanetScale、Turso |
| NoSQL | MongoDB、Redis | MongoDB Atlas、Upstash |
| 边缘 | Cloudflare D1 | 内置 |

---

## 7. 成本与时间估算

| 场景 | 开发人天 | 部署平台 | 年费（含域名） |
|------|----------|----------|----------------|
| **个人博客** | 2-5 天 | GitHub Pages / Cloudflare Pages | **≈ 免费**（域名 ¥60） |
| **SaaS MVP** | 15-30 天 | Vercel + Supabase | **≈ 免费**（均免费层） |
| **企业官网** | 5-10 天 | 静态 + Cloudflare | **≈ 免费** |
| **有状态 SaaS（增长期）** | 30-60 天 | VPS + Coolify | ~¥300-1000/年 |
| **国内合规企业站** | 5-10 天 + 备案 20 天 | 腾讯云/阿里云 | ~¥500-2000/年 |

> **要点**：个人/小项目基本可全程免费；付费临界点是商业用途、高流量或专属资源。

---

## 8. 推荐组合（精简优先）

| 场景 | 推荐栈 |
|------|--------|
| **零成本起步** | Astro/Next.js + Cloudflare Pages + Supabase |
| **快速商业化** | Vercel 全家桶（Next.js + Vercel + Supabase） |
| **国内合规** | 腾讯云 + ICP 备案 |
| **完全自主** | VPS + Docker + Coolify + Cloudflare |

---

## 官方文档速查
- Next.js：https://nextjs.org/docs
- Nuxt：https://nuxt.com
- SvelteKit：https://kit.svelte.dev
- Astro：https://docs.astro.build
- Vercel：https://vercel.com/docs
- Cloudflare：https://developers.cloudflare.com
- Supabase：https://supabase.com/docs
- Coolify：https://coolify.io

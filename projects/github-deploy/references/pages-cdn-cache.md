# GitHub Pages 路由与 CDN 缓存机制（v2.0）

> 适用：所有 GitHub Pages 部署/调试场景

## 一、路由真相：User Pages vs Project Pages

### User Pages（用户主页）

- 仓库名必须为 `<username>.github.io`
- 例：`harryopo/harryopo.github.io`
- URL：`https://harryopo.github.io/`
- **所有路径都从这个仓库服务**（包括子目录）

### Project Pages（项目主页）

- 仓库名任意，但 URL 含仓库名
- 例：`harryopo/junlin-tianxia`
- URL：`https://harryopo.github.io/junlin-tianxia/`（用户级）或 `https://harryopo.github.io/junlin-tianxia/`（独立域名）
- **每个仓库独立服务自己的内容**

### 🚨 关键陷阱：同名 Project Pages 优先级

如果同时存在：

- `harryopo/harryopo.github.io/junlin-tianxia/index.html`（主仓库子目录）
- `harryopo/junlin-tianxia/index.html`（独立仓库）

**访问 `https://harryopo.github.io/junlin-tianxia/` 时，GitHub Pages 优先用独立仓库**，主仓库子目录的同名文件**被忽略**。

**判定方法**：

```bash
# 1. 看远端实际内容
curl -sL "https://harryopo.github.io/junlin-tianxia/" | head -30

# 2. 对比两个仓库
curl -sL "https://raw.githubusercontent.com/harryopo/harryopo.github.io/main/junlin-tianxia/index.html" | head -30
curl -sL "https://raw.githubusercontent.com/harryopo/junlin-tianxia/master/index.html" | head -30

# 3. 哪个一致 → 哪个就是真正在服务的仓库
```

## 二、CDN 缓存机制

### Fastly CDN

GitHub Pages 用 Fastly 做全球 CDN：

- 静态资源（HTML/CSS/JS/图片）默认缓存 5-10 分钟
- HTML meta `Cache-Control` **只能控制浏览器**，**不能控制 CDN**
- CDN 缓存由 git push 触发失效

### 绕过缓存的方法

1. **等 1-2 分钟**让 Pages 重建 + CDN 失效
2. **加 query string 绕过浏览器**：`?v=2`、`?nocache=1`
3. **直接 curl 远端 raw 验证**（不受 CDN 影响）

```bash
# 验证 CDN 是否已更新
curl -sL "https://harryopo.github.io/<path>/?v=$(date +%s)" | head -10
```

## 三、Pages 部署流程

```
git push origin main
   ↓
GitHub 收到 push
   ↓
触发 Pages 构建（1-2 分钟）
   ↓
构建产物上传到 Fastly CDN
   ↓
全球边缘节点缓存（5-10 分钟）
   ↓
用户访问看到新内容
```

## 四、Pages 配置文件

### `_config.yml`（Jekyll 项目）

放在仓库根目录。如果有 Jekyll，不需要自己建 index.html。

### `.nojekyll` 文件

放在仓库根目录，禁用 Jekyll 处理，**让所有文件按原样服务**（包括下划线开头的目录如 `_images`）。

**适用场景**：纯静态 HTML 项目，不想被 Jekyll 处理。

### 自定义 404.html

放在仓库根目录，提供友好的 404 页面。

## 五、最佳实践

1. **每个独立项目一个仓库**：避免 Project Pages 路由冲突
2. **主仓库 `harryopo.github.io` 只放门户主页**：`index.html` + 导航卡片
3. **资源放根目录**：`images/`、`assets/` 与 `index.html` 同级
4. **HTML 加 no-cache meta**：避免用户浏览器缓存
5. **推送后等 1-2 分钟**：CDN 重建需要时间
6. **大文件用 git LFS**：GitHub Pages 单文件限制 100MB

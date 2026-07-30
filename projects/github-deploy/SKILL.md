---
name: github-deploy
description: "智能提交代码到 GitHub 并自动部署网页到 GitHub Pages。触发词：'提交代码'、'push到github'、'上传仓库'、'部署网页'、'发布页面'。"
tags: [git, github, deploy, pages, CI/CD]
agent: all
tools: [RunCommand, run_mcp, Read, Write, Glob]
---

# GitHub Deploy — 智能提交与网页部署

## 触发条件

当用户提到以下任一意图时激活：

- "提交代码"、"push"、"上传到github"、"推到仓库"
- "部署网页"、"发布页面"、"部署到pages"
- "更新网站"、"上线页面"

---

## 工作流概览

```
检出当前仓库状态
  → 生成 conventional commit 消息
  → HTTP + pushurl 推送（无弹窗）
  → 扫描 diff 检测网页内容
      ├── 无网页内容 → 完成
      └── 有网页内容 → 询问部署
              ├── 是 → 复制到 harryopo.github.io → 更新导航 → 推送
              └── 否 → 完成
```

---

## 阶段一：提交代码

### 1.1 状态检查

```bash
git status --short
git diff --stat
git log --oneline -5
```

### 1.2 生成提交消息

遵循 Conventional Commits 格式：

```
<type>(<scope>): <简短描述>

<详细说明（可选）>
```

type 选择：

| type | 场景 |
|------|------|
| `feat` | 新功能、新文件 |
| `fix` | 修复 bug |
| `refactor` | 重构（不改功能） |
| `docs` | 文档变更 |
| `style` | 格式调整 |
| `test` | 测试相关 |
| `chore` | 构建、依赖等杂项 |

scope 选当前仓库名或受影响模块名。

**规则：**
- 只提交与本次变更直接相关的文件（`git add <specific-files>`，不用 `git add -A`）
- 不提交 `.env`、`credentials.*`、`secrets.*`
- 提交前向用户展示 commit message 并确认

---

## 阶段二：推送（v2.1 MCP 集成版）

**v2.0 单一 HTTP+pushurl 方案** 仍是日常首选（无弹窗、最稳）。**v2.1 新增 MCP 工具集成**，用于批量文件操作、大文件分块、原子更新等 pushurl 无法覆盖的场景。

### 推送方案选择矩阵

| 场景 | 首选方案 | 备选方案 |
|------|----------|----------|
| 日常代码提交（< 50 文件） | `git push`（pushurl） | — |
| 批量文件推送（50+ 文件） | MCP `push_files` | `git push` |
| 大文件（> 100MB） | Git LFS | MCP `push_files` 分块 |
| 单文件原子更新 | MCP `create_or_update_file` | `git push` |
| pushurl 失败（网络问题） | MCP `push_files` | gh CLI |
| GitHub Releases 附件 | `gh release upload` | 网页手动上传 |

### 方案 A：HTTP + pushurl（日常首选）

```bash
git push origin <branch>
```

**前提**：`.git/config` 已配 pushurl。配置模板：

```ini
[remote "origin"]
    url = https://ghfast.top/https://github.com/<owner>/<repo>.git
    fetch = +refs/heads/*:refs/remotes/origin/*
    pushurl = https://x-access-token:<PAT>@ghfast.top/https://github.com/<owner>/<repo>.git
```

### 方案 B：MCP 工具推送（批量/大文件/原子操作）

**v2.1 新增**：当 pushurl 不可用或需要批量/原子操作时，使用 MCP GitHub Server。

#### B1. push_files — 批量推送多文件

```python
# 适用场景：50+ 文件批量推送、pushurl 失败降级
run_mcp(
    server_name="mcp_GitHub",
    tool_name="push_files",
    args={
        "owner": "harryopo",
        "repo": "<repo-name>",
        "branch": "main",
        "files": [
            {"path": "src/file1.ts", "content": "<base64-encoded>"},
            {"path": "src/file2.ts", "content": "<base64-encoded>"}
        ],
        "message": "feat: batch update via MCP"
    }
)
```

#### B2. create_or_update_file — 单文件原子更新

```python
# 适用场景：只改一个文件、需要 SHA 校验防冲突
run_mcp(
    server_name="mcp_GitHub",
    tool_name="create_or_update_file",
    args={
        "owner": "harryopo",
        "repo": "<repo-name>",
        "path": "docs/README.md",
        "content": "<file-content>",
        "message": "docs: update README",
        "branch": "main",
        "sha": "<optional-if-updating>"   # 更新时需传旧文件 SHA
    }
)
```

#### B3. 大文件分块推送（> 100MB）

```python
# 将大文件切分为 ≤ 50MB 块，逐块 push_files
import base64

def chunk_and_push(file_path, repo, branch, chunk_size=50*1024*1024):
    with open(file_path, "rb") as f:
        data = f.read()
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    for idx, chunk in enumerate(chunks):
        run_mcp(
            server_name="mcp_GitHub",
            tool_name="push_files",
            args={
                "owner": "harryopo",
                "repo": repo,
                "branch": branch,
                "files": [{"path": f"{file_path}.part{idx}", "content": base64.b64encode(chunk).decode()}],
                "message": f"chore: upload chunk {idx+1}/{len(chunks)}"
            }
        )
```

> 更优方案：优先用 **Git LFS**（`git lfs track "*.zip"`），MCP 分块仅作 LFS 不可用时的降级。

### 异常处理

如果 push 仍弹窗或失败：

1. **检查 pushurl 是否生效**：`git config --get-regexp '^remote\.origin\..*url$'`
2. **检查全局 insteadOf**：`git config --global --get-regexp 'url\..*\.insteadof'`，有则删
3. **降级 MCP**：用 `push_files` 绕过网络问题
4. **运行判定脚本**：`python scripts/check_pages_source.py`（用于页面访问问题）
5. **完整排查流程**：见 [references/git-popup-troubleshooting.md](references/git-popup-troubleshooting.md)

---

## 阶段三：网页部署

### 3.1 网页内容检测

扫描本次 diff，匹配以下条件之一即视为网页内容：

- 文件扩展名：`.html`、`.css`、`.js`、`.tsx`、`.jsx`（含 `index.html`）
- 文件路径含 `docs/`、`public/`、`dist/`、`out/`
- 目录结构包含 `index.html` + 样式文件

### 3.2 部署询问

检测到网页内容后，向用户提问：

> "检测到网页内容（列出检测到的文件），要部署到 https://harryopo.github.io 吗？"

选项：
1. **部署** — 复制网页文件到 `harryopo.github.io` 并更新导航
2. **只提交代码** — 跳过部署
3. **告诉我怎么做** — 给出手动部署步骤

### 3.3 部署执行

```
1. 检查 harryopo.github.io 本地克隆是否存在
   ├── 存在 → cd 进入
   └── 不存在 → git clone https://ghfast.top/https://github.com/harryopo/harryopo.github.io.git
   
2. 确定子目录名
   - 从当前仓库名自动生成：ai-dev-workflow → ai-dev-workflow/
   - 或询问用户自定义路径
   
3. 复制网页文件到子目录
   排除项：node_modules/、.git/、*.map、package.json、README.md
   
4. 更新首页导航
   读取 harryopo.github.io/index.html
   在导航区 <!-- NAV-START --> 和 <!-- NAV-END --> 之间插入链接
   格式：<a href="/{项目名}/" class="nav-card">...</a>
   如果已存在同名链接 → 更新而非重复
   
5. commit + push harryopo.github.io（走 pushurl）
```

### 3.4 首页导航格式

每个部署的项目在首页展示为导航卡片：

```html
<!-- NAV-START -->
<!-- 由 github-deploy skill 自动维护，请勿手动编辑 -->

<a href="/ai-dev-workflow/" class="nav-card">
  <span class="nav-card__title">AI 开发工作流</span>
  <span class="nav-card__desc">6 阶段 AI 驱动开发方法论</span>
  <span class="nav-card__tag">skill</span>
</a>

<!-- NAV-END -->
```

卡片信息从当前仓库的 README.md 第一行标题和描述中提取。

---

## 约束与注意事项

### 强制约束

1. **首选 HTTP + pushurl**：日常推送必须用 ghfast 镜像 + pushurl 注入 token，无弹窗、最稳
2. **MCP 工具用于特定场景**：批量文件（50+）、原子更新、pushurl 失败降级时使用 MCP `push_files` / `create_or_update_file`
3. **大文件用 Git LFS**：> 100MB 文件必须用 `git lfs track`，MCP 分块仅作降级
4. **VPN 全局模式**：用户 VPN 常开，网络通常无障碍
5. **不提交敏感文件**：`.env`、`credentials.*`、`secrets.*`、`*.pem` 直接跳过
6. **一次一仓库**：不同仓库的变更分开提交，不混在一起
7. **提交前确认**：向用户展示 commit message 和文件列表，获确认后再 push

### 兜底优先级（v2.1 更新）

```
HTTP + pushurl (git push) → MCP push_files → gh CLI → 告知原因
    ↓ 失败                    ↓ 失败           ↓ 失败
  检查 pushurl             检查 MCP 配置    建议手动操作
```

### 网页部署规则

- **只部署静态内容**：HTML/CSS/JS/图片/字体，不求后端或数据库
- **源码不上 Pages**：Pages 仓库只放渲染产物，不放源码
- **导航不重复**：同一项目名已存在则更新，不新建
- **单页面 = 单目录**：每个部署的网页放在 `harryopo.github.io/<项目名>/` 下

---

## 快速参考

```bash
# 查看仓库状态
git status --short

# 提交
git add <files>
git commit -m "$(cat <<'EOF'
type(scope): 描述
EOF
)"
git push origin <branch>

# 检查 pushurl 配置
git config --get-regexp '^remote\.origin\..*url$'

# 查看远程地址
git remote -v
```

---

# v2.0 升级 — 实战经验与故障案例库（2026-07-23）

> 本节记录自 v1.0 发布以来在 https://harryopo.github.io 实际部署中踩过的坑与解决方案。后续 Skill 执行时**必须**先读本节。

## 🚨 核心架构变更

### ⭐⭐⭐ 子路径真相：`username.github.io/<subpath>` ≠ 主仓库子目录

**这是 GitHub Pages 最重要的隐藏规则，90% 的部署问题源自此处。**

```
https://harryopo.github.io/
  └── 由仓库 harryopo/harryopo.github.io 服务（User Pages）
https://harryopo.github.io/junlin-tianxia/
  └── 实际由仓库 harryopo/junlin-tianxia 服务（同名 Project Pages 优先级更高）
```

**判定方法（必须执行，否则会部署错位置）：**

```bash
# 1. 检查远端实际内容，看哪个仓库在提供内容
curl -sL "https://harryopo.github.io/<subpath>/" | head -20
# 对比 raw.githubusercontent.com/<owner>/<repo>/<branch>/<subpath>/index.html
# 如果两者内容不一致 → 说明有独立仓库同名 Project Pages 在服务

# 2. 用 GitHub API 列出所有同名仓库
# 在 GitHub 搜索 harryopo/<subpath>，若存在同名仓库 → 它就是真正的服务源
```

**结论：**

- 部署到 `harryopo.github.io/<subpath>/` 必须**推到同名独立仓库**（若存在）
- 推到主仓库子目录 `harryopo/harryopo.github.io/<subpath>/` **不会生效**
- 案例：2026-07-23 推送主仓库 `junlin-tianxia/` 子目录后，访问页面仍为旧版，最终发现需推独立仓库 `junlin-tianxia` 才解决

---

### ⭐⭐⭐ 推送机制：ghfast 代理 + URL 注入 token

**旧版（v1.0）失败根因**：在国内网络环境，SSH 连接 GitHub 不稳定，gh CLI 需要交互式认证，MCP API push 大文件超时。

**新版（v2.0）方案**：HTTP 协议 + ghfast 镜像 + URL 注入 PAT（Personal Access Token），完全无弹窗、无交互。

#### 配置文件模板（`~/.gitconfig` 或 `.git/config`）

```ini
[remote "origin"]
    url = https://ghfast.top/https://github.com/<owner>/<repo>.git              # fetch 走代理（速度）
    pushurl = https://x-access-token:<PAT>@ghfast.top/https://github.com/<owner>/<repo>.git   # push 走代理 + URL 注入 token
```

**关键点：**

- `url` 用 ghfast 镜像（fetch 速度快）
- `pushurl` 在 URL 里**直接注入 PAT**（`x-access-token:ghp_xxx@` 格式）
- 浏览器/Git Credential Manager **永远不会弹窗**，因为认证信息已经在 URL 里
- 不要再用 `insteadOf` 重写规则（会和 pushurl 冲突，且会触发弹窗）

**日常 push 命令：**

```bash
git add <files>
git commit -m "..."
git push origin <branch>     # 走 pushurl，无弹窗
```

**若仍弹窗，按以下顺序排查：**

```bash
# 1. 检查 pushurl 是否生效
git config --get-regexp '^remote\.origin\..*url$'

# 2. 检查全局 insteadOf 是否覆盖
git config --global --get-regexp 'url\..*\.insteadOf'
# 如有 url.https://ghfast.top/.insteadOf → 删掉
git config --global --unset 'url.https://ghfast.top/https://github.com/.insteadOf'

# 3. 检查 .git/config 是否有 pushurl
cat .git/config | grep pushurl
```

完整诊断流程见 `references/git-popup-troubleshooting.md`。

---

## ⚠️ GitHub Pages CDN 缓存坑

**症状**：推送后 5-10 分钟访问页面，仍是旧版。

**根因**：

1. GitHub Pages 用 Fastly CDN 缓存静态资源
2. HTML meta `Cache-Control: no-cache, no-store, must-revalidate` **只能控制浏览器**，**不能控制 CDN**
3. CDN 缓存由"内容更新"（git push）触发失效

**正确做法**：

- HTML 加 meta 标签（避免用户浏览器缓存）
- 推送后**等 1-2 分钟**让 Pages 重建
- 验证时**用 `?v=N` 绕过浏览器缓存**（CDN 看 URL 路径，不看 query string 的话也会命中）
- 最稳的验证：直接 curl 远端 raw 仓库，对比本地文件

```bash
# 验证步骤
sleep 60    # 等 Pages 重建
curl -sIL "https://<owner>.github.io/<path>/" | head -10   # 看响应头
# 或浏览器访问 https://<owner>.github.io/<path>/?v=2
```

---

## 🎯 PPT/单页应用部署最佳实践

**案例**：2026-07-23 部署 `junlin-tianxia`（菌菇三下乡 PPT），从 4 层中间页简化为 1 层直入。

### 反模式：多层导航

```
主页 → 项目卡片 → 项目介绍页 → "进入 PPT →" 按钮 → PPT 实际内容
       (多余层)   (多余层)        (多余层)
```

### 正模式：主页直入

```
主页 → 项目卡片 → PPT 实际内容
       (无中间页)
```

### 强制规则（v2.0 起生效）

1. **PPT/单页应用的 index.html 必须直接是内容本身**，不许套"进入 →"中间页
2. **资源文件放根目录**：`images/`、`assets/` 与 `index.html` 同级，避免 `../` 相对路径
3. **保留旧版资料**到 `archive/<project>-v1/` 子目录，不直接删除（用户可能需要回滚）
4. **导航卡片标题要精炼**（≤ 15 字），描述 ≤ 60 字

### 部署步骤（PPT 类）

```bash
# 1. 准备工作目录
mkdir tmp-deploy/<project> && cd tmp-deploy/<project>

# 2. clone 独立仓库（重要：子路径实际由独立仓库服务）
git clone https://ghfast.top/https://github.com/<owner>/<project>.git .

# 3. 配置 pushurl（参照上面的 .git/config 模板）
# 编辑 .git/config，加入 pushurl 行

# 4. 覆盖 index.html + 拷贝资源
cp <source>/index.html .
cp -r <source>/images .   # 如果有
cp -r <source>/assets .

# 5. 提交推送
git add index.html images assets
git -c user.name=... -c user.email=... commit -m "..."
git push origin <branch>

# 6. 清理
cd ../.. && rm -rf tmp-deploy

# 7. 验证（等 1 分钟）
# 访问 https://<owner>.github.io/<project>/
```

---

## 🛠️ 自动维护导航：update_nav.py

**触发时机**：每次有新项目部署到 `harryopo.github.io` 主页时。

**位置**：`projects/github-deploy/scripts/update_nav.py`

**核心机制**：

- 主页 `harryopo.github.io/index.html` 含 `<!-- NAV-START -->` 和 `<!-- NAV-END -->` 标记
- 脚本**只替换标记之间**的内容，保留其他部分
- 卡片信息从 `<project>/README.md` 自动提取（首行标题 + 描述）

**运行方式**：

```bash
python projects/github-deploy/scripts/update_nav.py --repo harryopo.github.io --slug <new-project>
```

---

## 📚 经验教训速查表

| 现象                              | 根因                                          | 解决                                  |
| --------------------------------- | --------------------------------------------- | ------------------------------------- |
| git push 反复弹认证窗口           | ghfast 代理吞 Authorization 头 + insteadOf 冲突 | `.git/config` 加 `pushurl` + URL 注入 token |
| 主页改了但子路径还是旧版          | 实际由独立同名 Project Pages 服务              | 推到独立仓库而非主仓库子目录           |
| 推送后页面没更新                  | GitHub Pages CDN 缓存 + 重建需要 1-2 分钟      | 加 meta `Cache-Control` + 等 + 用 `?v=N` |
| 主页卡片更新后样式错乱            | update_nav.py 生成的 class 与主页 CSS 不一致  | 模板中固定 `class="card"` 与主页对齐   |
| 推送大文件（如图片）              | GitHub API push 限制 100MB                    | 改用 git push (HTTP)                   |
| SSH 推送 Permission denied        | 国内 SSH 直连 GitHub 经常断                    | 改用 HTTPS + ghfast + pushurl         |
| 主页导航重复显示同一项目          | update_nav.py 没去重逻辑                      | 现有用 NAV-START/END 标记规避         |

---

## 🗂️ 相关文件

- `scripts/update_nav.py` — 主页导航自动维护
- `references/git-popup-troubleshooting.md` — Git 弹窗完整排查流程
- `references/pages-cdn-cache.md` — GitHub Pages CDN 缓存机制与绕过
- `evals/evals.json` — 评测集

## 🔗 学习笔记

- `.learnings/LRN-20260723-001-git-popup-fix.md` — Git 弹窗根因 + 修复
- `.learnings/LRN-20260723-002-pages-routing.md` — 子路径由独立仓库服务的发现
- `.learnings/LRN-20260723-003-ppt-direct-entry.md` — PPT 入口统一最佳实践
- `.learnings/LRN-20260730-001-mcp-integration.md` — MCP 工具集成最佳实践（v2.1 新增）

---

# v2.1 MCP 工具集成指南（2026-07-30 新增）

> 基于全网调研，GitHub MCP Server 已成熟，支持批量文件操作、原子更新、自动分支创建等能力。本节补充 MCP 工具在 github-deploy skill 中的具体使用场景和最佳实践。

## 📦 MCP GitHub Server 核心能力

### 工具清单

| 工具名 | 用途 | 适用场景 |
|--------|------|----------|
| `push_files` | 单次提交推送多文件 | 批量文件（50+）、pushurl 失败降级 |
| `create_or_update_file` | 单文件原子更新 | 只改一个文件、需 SHA 校验防冲突 |
| `get_file_contents` | 获取文件/目录内容 | 读取远端文件、对比本地差异 |
| `create_branch` | 创建新分支 | 自动创建特性分支 |
| `search_code` | 搜索代码 | 查找仓库内特定内容 |
| `create_issue` | 创建 Issue | 自动化问题追踪 |
| `create_pull_request` | 创建 PR | 自动化 PR 流程 |

### 配置要求

MCP GitHub Server 需要 Personal Access Token (PAT)：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

## 🎯 使用场景详解

### 场景 1：批量文件推送（50+ 文件）

当需要推送大量文件时，`git push` 可能因网络问题失败，MCP `push_files` 提供更稳定的批量操作：

```python
# 读取所有文件并 base64 编码
import base64
from pathlib import Path

files_to_push = []
for file_path in Path("dist").rglob("*"):
    if file_path.is_file():
        content = base64.b64encode(file_path.read_bytes()).decode()
        files_to_push.append({
            "path": str(file_path.relative_to("dist")),
            "content": content
        })

# 批量推送
run_mcp(
    server_name="mcp_GitHub",
    tool_name="push_files",
    args={
        "owner": "harryopo",
        "repo": "junlin-tianxia",
        "branch": "main",
        "files": files_to_push,
        "message": "deploy: batch upload dist files via MCP"
    }
)
```

### 场景 2：单文件原子更新

修改单个文件时，使用 `create_or_update_file` 可以避免拉取整个仓库：

```python
# 更新 README.md 的版本号
run_mcp(
    server_name="mcp_GitHub",
    tool_name="create_or_update_file",
    args={
        "owner": "harryopo",
        "repo": "junlin-tianxia",
        "path": "README.md",
        "content": "# 菌菇天下 v2.1.0\n\n...",
        "message": "docs: bump version to 2.1.0",
        "branch": "main",
        "sha": "abc123..."  # 可选，用于冲突检测
    }
)
```

### 场景 3：大文件分块推送（> 100MB）

GitHub API 限制单文件 100MB，超大文件需分块：

```python
import base64

def push_large_file(file_path, repo, branch, chunk_size_mb=50):
    """将大文件分块推送到 GitHub"""
    chunk_size = chunk_size_mb * 1024 * 1024
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    total_chunks = (len(data) + chunk_size - 1) // chunk_size
    
    for i in range(total_chunks):
        chunk = data[i * chunk_size : (i + 1) * chunk_size]
        content = base64.b64encode(chunk).decode()
        
        run_mcp(
            server_name="mcp_GitHub",
            tool_name="push_files",
            args={
                "owner": "harryopo",
                "repo": repo,
                "branch": branch,
                "files": [{
                    "path": f"{file_path}.part{i+1:03d}",
                    "content": content
                }],
                "message": f"chore: upload {file_path} chunk {i+1}/{total_chunks}"
            }
        )
    
    print(f"✅ 大文件 {file_path} 已分 {total_chunks} 块上传完成")

# 使用示例
push_large_file("dataset.zip", "my-repo", "main", chunk_size_mb=50)
```

> **注意**：分块文件需要在 README 中说明合并方式，或提供解压脚本。更推荐用 Git LFS。

### 场景 4：自动化 PR 流程

结合 MCP 工具实现完整的 PR 自动化：

```python
# 1. 创建特性分支
run_mcp(
    server_name="mcp_GitHub",
    tool_name="create_branch",
    args={
        "owner": "harryopo",
        "repo": "junlin-tianxia",
        "branch": "feat/new-feature",
        "from_branch": "main"
    }
)

# 2. 推送代码变更
run_mcp(
    server_name="mcp_GitHub",
    tool_name="push_files",
    args={
        "owner": "harryopo",
        "repo": "junlin-tianxia",
        "branch": "feat/new-feature",
        "files": [...],
        "message": "feat: add new feature"
    }
)

# 3. 创建 PR
run_mcp(
    server_name="mcp_GitHub",
    tool_name="create_pull_request",
    args={
        "owner": "harryopo",
        "repo": "junlin-tianxia",
        "title": "feat: 新增智能推荐功能",
        "body": "## 变更内容\n- 新增推荐算法\n- 优化 UI 交互\n\n## 测试情况\n- [x] 单元测试通过\n- [x] 集成测试通过",
        "head": "feat/new-feature",
        "base": "main",
        "draft": False
    }
)
```

## ⚠️ MCP 工具使用注意事项

1. **Token 权限**：PAT 需要 `repo` 完整权限（包括 `repo:status`, `repo_deployment`, `public_repo` 等）
2. **速率限制**：GitHub API 有速率限制（认证用户 5000 次/小时），批量操作时注意控制频率
3. **文件大小**：单文件上限 100MB，超过需用 Git LFS 或分块
4. **网络环境**：国内访问 GitHub API 可能超时，建议配合代理或使用 pushurl 降级
5. **错误处理**：MCP 调用失败时应降级到 `git push` 或提示用户手动操作

## 🔄 MCP 与 Git CLI 对比

| 维度 | Git CLI (`git push`) | MCP (`push_files`) |
|------|---------------------|-------------------|
| 速度 | 快（增量传输） | 慢（全量 base64） |
| 稳定性 | 依赖网络 | 依赖 API 可用性 |
| 批量文件 | 优秀 | 优秀（单次提交） |
| 大文件 | 支持（需 LFS） | 限制 100MB |
| 原子性 | 仓库级 | 文件级 |
| 适用场景 | 日常开发 | 自动化脚本、CI/CD |

**结论**：日常开发用 `git push`，自动化场景用 MCP。

---

# v2.2 官方托管 MCP 与 Agentic Workflows（2026-07-30 更新）

> 基于 2026-07-30 全网调研 + 实际验证，GitHub 官方托管 MCP Server 和 Agentic Workflows 已成熟。
> **MCP 工具实测**：`mcp_GitHub` 服务器的 `search_repositories`、`push_files`、`create_or_update_file` 等工具已验证可用。

## 🚀 GitHub 官方托管 MCP Server

### 核心优势

| 特性 | 本地 Docker | 官方托管端点 |
|------|------------|-------------|
| 维护成本 | 手动升级 Docker 镜像 | GitHub 自动更新 |
| 认证方式 | 管理 PAT | OAuth 一次登录 |
| 访问范围 | 仅 localhost | 任意 IDE/远程开发机 |
| 权限控制 | 需自定义配置 | 内置只读开关和工具集筛选 |

### 配置方式

**VS Code / Cursor 配置**：

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer <YOUR_COPILOT_TOKEN>"
      }
    }
  }
}
```

**只读模式**（安全浏览代码）：

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "X-MCP-Readonly": "true"
      }
    }
  }
}
```

### 工具集筛选

禁用不需要的工具集，减少 token 消耗：

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "toolsets": ["pull_requests", "issues"],  // 只启用 PR 和 Issues
      "disabledToolsets": ["actions", "security"]  // 禁用 Actions 和安全
    }
  }
}
```

### 实测验证（2026-07-30）

当前环境已配置 `mcp_GitHub` 服务器，以下工具已验证可用：

```python
# ✅ 已验证：搜索仓库
run_mcp("mcp_GitHub", "search_repositories", {"query": "github-deploy skill"})
# 返回：16 个相关仓库，包括 zeke/preview-deployments-skill 等

# ✅ 可用工具清单（26 个）
tools = [
    "push_files",              # 批量推送文件
    "create_or_update_file",   # 单文件原子更新
    "get_file_contents",       # 获取文件内容
    "create_branch",           # 创建分支
    "create_issue",            # 创建 Issue
    "create_pull_request",     # 创建 PR
    "search_code",             # 搜索代码
    "search_repositories",     # 搜索仓库
    "list_commits",            # 列出提交
    "list_issues",             # 列出 Issue
    "list_pull_requests",      # 列出 PR
    "get_pull_request",        # 获取 PR 详情
    "merge_pull_request",      # 合并 PR
    # ... 更多工具见 MCP 工具描述文件
]
```

## 🤖 GitHub Agentic Workflows

### 什么是 Agentic Workflows

GitHub Agentic Workflows 是 2026-02 推出的技术预览功能，用 Markdown 定义工作流目标，自动编译为 GitHub Actions YAML，实现 Continuous AI 自动化。

### 核心能力

| 自动化场景 | 描述 |
|-----------|------|
| Continuous Triage | 自动总结、标签、路由新 issues |
| Continuous Documentation | 保持 README 和文档与代码同步 |
| Continuous Code Quality | 自动调查 CI 失败并提出修复建议 |
| Continuous Testing | 评估测试覆盖率并添加高价值测试 |

### 工作流示例

**.github/workflows/auto-triage.md**：

```markdown
---
name: Auto Triage Issues
on:
  issues:
    types: [opened]
---

# 自动分类新 Issues

当新 issue 创建时：
1. 分析 issue 内容，判断类型（bug/feature/question）
2. 自动添加对应标签（bug/enhancement/question）
3. 如果是 bug，检查是否包含复现步骤
4. 如果信息不全，自动评论请求补充信息
5. 分配给对应的维护者
```

### 安全护栏

- **默认只读**：工作流默认只有读取权限
- **Safe Outputs**：写操作（创建 PR、添加评论）通过受控出口执行
- **沙箱执行**：代码在隔离环境运行，防止恶意代码影响
- **工具白名单**：只允许使用预批准的 MCP 工具

## ⚡ Token 效率优化

### 问题背景

Agentic Workflows 每次运行都会消耗 token，未优化的工作流可能产生高额 API 账单。

### 优化策略

**1. 移除未使用的 MCP 工具**

未使用的工具 schema 会占用 10-15 KB 上下文，每次 API 调用都浪费 token：

```python
# 审计工具使用情况
tool_calls = analyze_workflow_logs("workflow_name")
unused_tools = [t for t in all_tools if t not in tool_calls]

# 从配置中移除未使用工具
config["disabled_tools"] = unused_tools
```

**2. 用 GitHub CLI 替代 MCP 调用**

MCP 调用需要完整的 LLM 推理轮次，而 `gh` CLI 直接执行：

```python
# ❌ 低效：MCP 调用获取 PR diff
run_mcp("get_pull_request_files", {...})  # 消耗 1 轮 LLM 推理

# ✅ 高效：直接调用 gh CLI
subprocess.run(["gh", "pr", "diff", "123"])  # 无 LLM 开销
```

**3. 缓存重复查询结果**

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_file_content(owner, repo, path, branch):
    """缓存文件内容，避免重复查询"""
    return run_mcp("get_file_contents", {...})
```

**4. 批量操作合并请求**

```python
# ❌ 低效：逐个文件查询
for file in files:
    content = get_file_content(file)

# ✅ 高效：批量查询
contents = batch_get_file_contents(files)
```

## 📦 大文件推送方案对比（2026 更新）

| 方案 | 单文件上限 | 月免费额度 | 适用场景 | 推荐度 |
|------|-----------|-----------|----------|--------|
| **Git LFS** | 5GB | 1GB 存储 + 1GB 带宽 | 模型权重、数据集、二进制资源 | ⭐⭐⭐⭐⭐ |
| **GitHub Releases** | 2GB | 无限制 | 版本发布附件、安装包 | ⭐⭐⭐⭐ |
| **MCP push_files 分块** | 100MB/块 | 无限制 | 临时降级方案 | ⭐⭐ |
| **split 手动分片** | 95MB/片 | 无限制 | 不可用 LFS 的二进制文件 | ⭐ |

### Git LFS 最佳实践

```bash
# 1. 安装 Git LFS
git lfs install

# 2. 追踪大文件类型
git lfs track "*.pth"      # PyTorch 模型
git lfs track "*.zip"      # 压缩包
git lfs track "*.mp4"      # 视频文件

# 3. 提交 .gitattributes（必须）
git add .gitattributes
git commit -m "chore: configure Git LFS"

# 4. 正常推送，LFS 自动处理大文件
git push origin main
```

### GitHub Releases 自动化

```python
# 使用 gh CLI 自动创建 Release 并上传附件
subprocess.run([
    "gh", "release", "create", "v1.0.0",
    "--title", "v1.0.0 - 首次发布",
    "--notes", "## 新功能\n- 智能推荐\n- 性能优化",
    "./dist/app.zip",      # 自动上传附件
    "./dist/model.pth"
])
```

## 🔐 供应链安全最佳实践（2026）

### 账户安全

1. **启用 2FA**：所有协作者必须启用双因素认证
2. **使用 Fine-grained PAT**：替代 classic PAT，最小权限原则
3. **定期审计 SSH 密钥**：删除未使用的密钥

### 工作流安全

1. **固定 Action 版本**：使用 SHA 而非 tag（`actions/checkout@abc123`）
2. **限制 GITHUB_TOKEN 权限**：在 workflow 中明确声明所需权限
3. **审查第三方 Actions**：检查源码和权限要求

### 代码签名

```yaml
# .github/workflows/release.yml
permissions:
  contents: write
  id-token: write  # 用于 Sigstore 签名

steps:
  - uses: actions/checkout@v4
  
  - name: Sign release artifacts
    uses: sigstore/cosign-installer@v3
    with:
      artifact: dist/app.zip
```

## 📊 监控与告警

### GitHub Actions 成本监控

```python
# 每日审计 Actions 用量
def audit_actions_usage():
    usage = subprocess.run(["gh", "api", "repos/{owner}/{repo}/actions/billing"], 
                          capture_output=True)
    data = json.loads(usage.stdout)
    
    if data["total_minutes_used"] > THRESHOLD:
        send_alert(f"Actions 用量超标：{data['total_minutes_used']} 分钟")
```

### MCP 调用监控

```python
# 记录每次 MCP 调用的 token 消耗
def log_mcp_usage(tool_name, input_tokens, output_tokens):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }
    with open("mcp_usage.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

## 🎯 2026 推荐工作流

### 日常开发流程

```
1. 本地开发
   ↓
2. git push（HTTP + pushurl）
   ↓
3. GitHub Actions 自动测试
   ↓
4. Agentic Workflow 自动审查
   ↓
5. 合并 PR
   ↓
6. 自动部署到 GitHub Pages
```

### 大文件处理流程

```
1. 检测到大文件（> 100MB）
   ↓
2. 自动配置 Git LFS
   ↓
3. git lfs track + commit + push
   ↓
4. LFS 自动上传大文件
   ↓
5. 仓库只保留指针文件
```

### 自动化运维流程

```
1. 新 Issue 创建
   ↓
2. Agentic Workflow 自动分类
   ↓
3. 自动添加标签和分配维护者
   ↓
4. 如果是 bug，自动复现并生成修复 PR
   ↓
5. 维护者审查合并
```

## 📚 参考资源

- [GitHub MCP Server 官方文档](https://github.com/github/github-mcp-server)
- [GitHub Agentic Workflows 技术预览](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)
- [Token 效率优化指南](https://github.blog/ai-and-ml/improving-token-efficiency-in-github-agentic-workflows/)
- [Git LFS 官方文档](https://git-lfs.github.com/)
- [供应链安全最佳实践](https://openssf.org/)

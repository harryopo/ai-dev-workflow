# Git & GitHub 使用教程

> 面向初学者的实用指南，覆盖日常开发 90% 的场景。

---

## 目录

1. [核心概念](#1-核心概念)
2. [首次配置](#2-首次配置)
3. [日常操作流程](#3-日常操作流程)
4. [常用命令速查](#4-常用命令速查)
5. [分支管理](#5-分支管理)
6. [远程仓库操作](#6-远程仓库操作)
7. [常见问题](#7-常见问题)
8. [进阶技巧](#8-进阶技巧)

---

## 1. 核心概念

### Git 是什么？

Git 是一个**版本控制工具**，帮你记录代码的每次修改，随时可以回退到任意版本。

### GitHub 是什么？

GitHub 是一个**代码托管平台**，把你的 Git 仓库存到云端，方便分享和协作。

### 三个区域

```
工作区（你编辑的文件）
    ↓ git add
暂存区（准备提交的修改）
    ↓ git commit
本地仓库（已提交的历史）
    ↓ git push
远程仓库（GitHub 上的备份）
```

---

## 2. 首次配置

### 2.1 安装 Git

```bash
# Windows（已装）
winget install Git.Git

# 验证安装
git --version
```

### 2.2 配置用户信息

```bash
# 设置用户名和邮箱（会记录在每次提交中）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

### 2.3 配置 GitHub 认证

```bash
# 方式一：使用 gh CLI（推荐）
gh auth login
# 按提示选择 GitHub.com → HTTPS → 浏览器登录

# 方式二：使用 Token
# 1. GitHub → Settings → Developer settings → Personal access tokens → Generate
# 2. 复制 token
# 3. 推送时输入用户名和 token 作为密码
```

### 2.4 配置代理（国内网络）

```bash
# 如果你有 VPN/代理（假设端口 7890）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 3. 日常操作流程

### 3.1 新建仓库并推送到 GitHub

```bash
# 1. 进入项目目录
cd my-project

# 2. 初始化 Git
git init

# 3. 创建 .gitignore（排除不需要的文件）
# 编辑 .gitignore 文件，添加：
# __pycache__/
# node_modules/
# .env

# 4. 添加所有文件到暂存区
git add .

# 5. 提交到本地仓库
git commit -m "init: 项目初始化"

# 6. 在 GitHub 创建仓库（用 gh CLI）
gh repo create my-project --public --source . --push

# 或者手动：
# 1. 去 github.com 新建仓库
# 2. 关联远程仓库
git remote add origin https://github.com/用户名/仓库名.git
# 3. 推送
git push -u origin master
```

### 3.2 日常修改并推送

```bash
# 1. 修改文件后，查看改了什么
git status          # 查看哪些文件改了
git diff            # 查看具体改了什么

# 2. 添加修改到暂存区
git add .                    # 添加所有修改
git add 文件1 文件2          # 添加指定文件

# 3. 提交
git commit -m "feat: 添加新功能"

# 4. 推送到 GitHub
git push
```

### 3.3 从 GitHub 克隆仓库

```bash
# 克隆别人的仓库
git clone https://github.com/用户名/仓库名.git

# 克隆到指定目录
git clone https://github.com/用户名/仓库名.git my-folder
```

### 3.4 拉取最新代码

```bash
# 从 GitHub 拉取最新代码
git pull
```

---

## 4. 常用命令速查

### 状态查看

| 命令 | 作用 |
|------|------|
| `git status` | 查看当前状态（改了什么、暂存了什么） |
| `git log` | 查看提交历史 |
| `git log --oneline` | 简洁版提交历史 |
| `git diff` | 查看未暂存的修改 |
| `git diff --staged` | 查看已暂存的修改 |

### 文件操作

| 命令 | 作用 |
|------|------|
| `git add .` | 添加所有修改到暂存区 |
| `git add 文件名` | 添加指定文件 |
| `git commit -m "说明"` | 提交到本地仓库 |
| `git commit -am "说明"` | add + commit 一步完成（仅限已跟踪的文件） |

### 远程操作

| 命令 | 作用 |
|------|------|
| `git push` | 推送到远程仓库 |
| `git pull` | 拉取远程更新 |
| `git remote -v` | 查看远程仓库地址 |
| `git remote add origin URL` | 关联远程仓库 |

### 撤销操作

| 命令 | 作用 |
|------|------|
| `git checkout -- 文件名` | 撤销工作区的修改 |
| `git reset HEAD 文件名` | 从暂存区移除（保留修改） |
| `git reset --soft HEAD~1` | 撤销上次 commit（保留修改在暂存区） |
| `git reset --hard HEAD~1` | 撤销上次 commit（**丢弃修改，慎用**） |

---

## 5. 分支管理

### 什么是分支？

分支就像代码的平行宇宙，你可以在分支上开发新功能，不影响主分支。

```
main ─────────●─────────────●──────── (稳定版本)
               \           /
feature-login   ●────●────●           (新功能开发)
```

### 常用命令

```bash
# 查看分支
git branch              # 本地分支
git branch -a           # 所有分支（含远程）

# 创建并切换到新分支
git checkout -b feature-login

# 切换分支
git checkout main
git checkout feature-login

# 合并分支（在 main 上合并 feature-login）
git checkout main
git merge feature-login

# 删除分支
git branch -d feature-login          # 删除本地分支
git push origin --delete feature-login  # 删除远程分支
```

### 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能 | `feature/login` |
| `fix/` | 修复 bug | `fix/login-error` |
| `hotfix/` | 紧急修复 | `hotfix/security-patch` |
| `release/` | 发布版本 | `release/v1.0.0` |

---

## 6. 远程仓库操作

### 6.1 使用 gh CLI 管理 GitHub

```bash
# 创建仓库
gh repo create my-project --public    # 公开仓库
gh repo create my-project --private   # 私有仓库

# 克隆仓库
gh repo clone 用户名/仓库名

# 查看仓库信息
gh repo view

# 查看 Issues
gh issue list

# 创建 Issue
gh issue create --title "Bug: xxx" --body "描述"

# 创建 Pull Request
gh pr create --title "feat: 新功能" --body "描述"

# 查看 PR
gh pr list
gh pr view 123    # 查看 PR #123
```

### 6.2 Fork 和 PR（参与别人的项目）

```bash
# 1. Fork 仓库（在 GitHub 网页上点 Fork）

# 2. 克隆你 Fork 的仓库
git clone https://github.com/你的用户名/仓库名.git

# 3. 创建新分支
git checkout -b fix-typo

# 4. 修改代码并提交
git add .
git commit -m "fix: 修复 typo"

# 5. 推送到你的 Fork
git push origin fix-typo

# 6. 在 GitHub 上创建 Pull Request
gh pr create
```

---

## 7. 常见问题

### Q: 推送时提示 "Permission denied"

```bash
# 原因：没有配置 SSH Key 或 Token
# 解决：使用 gh CLI 登录
gh auth login
```

### Q: 推送时提示 "Connection reset" 或超时

```bash
# 原因：GitHub 被墙
# 解决：开 VPN/代理，或配置代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

### Q: 提交信息写错了

```bash
# 修改最近一次提交信息
git commit --amend -m "新的提交信息"

# 如果已经推送
git commit --amend -m "新的提交信息"
git push --force   # 强制推送（慎用，只在个人仓库用）
```

### Q: 想撤销上次提交

```bash
# 撤销提交但保留修改
git reset --soft HEAD~1

# 撤销提交并丢弃修改（慎用）
git reset --hard HEAD~1
```

### Q: 文件太大推不上去

```bash
# GitHub 单文件限制 100MB
# 解决：用 Git LFS 管理大文件
git lfs install
git lfs track "*.psd"    # 追踪 PSD 文件
git add .gitattributes
git commit -m "chore: 添加 LFS 追踪"
```

### Q: .gitignore 不生效

```bash
# 原因：文件已经被追踪了
# 解决：先从缓存移除
git rm -r --cached .
git add .
git commit -m "chore: 更新 .gitignore"
```

---

## 8. 进阶技巧

### 8.1 提交信息规范

使用约定式提交（Conventional Commits）：

```
<类型>(<范围>): <描述>

feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
test: 测试
chore: 构建/工具变更
```

示例：
```bash
git commit -m "feat(auth): 添加微信登录"
git commit -m "fix: 修复登录按钮点击无响应"
git commit -m "docs: 更新 README"
```

### 8.2 查看某行代码是谁写的

```bash
git blame 文件名
```

### 8.3 查看某个文件的修改历史

```bash
git log --follow -p -- 文件名
```

### 8.4 暂存当前工作

```bash
# 临时保存当前修改
git stash

# 恢复
git stash pop

# 查看保存列表
git stash list
```

### 8.5 打标签（版本号）

```bash
# 创建标签
git tag v1.0.0

# 推送标签到 GitHub
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### 8.6 使用 SSH（免密推送）

```bash
# 1. 生成 SSH Key
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 2. 复制公钥
cat ~/.ssh/id_ed25519.pub | clip

# 3. 添加到 GitHub
# GitHub → Settings → SSH and GPG keys → New SSH key → 粘贴

# 4. 切换远程地址为 SSH
git remote set-url origin git@github.com:用户名/仓库名.git

# 5. 测试连接
ssh -T git@github.com
```

---

## 附录：工作流示例

### 场景：开发一个新功能

```bash
# 1. 确保主分支是最新的
git checkout master
git pull

# 2. 创建新分支
git checkout -b feature-user-profile

# 3. 开发功能...
# 编辑文件...

# 4. 提交
git add .
git commit -m "feat: 添加用户个人资料页"

# 5. 推送分支
git push origin feature-user-profile

# 6. 创建 PR
gh pr create --title "feat: 添加用户个人资料页" --body "实现内容：..."

# 7. Code Review 通过后，合并到 main
gh pr merge

# 8. 切回主分支，删除功能分支
git checkout master
git pull
git branch -d feature-user-profile
```

### 场景：同步别人的更新

```bash
# 1. 添加上游仓库（只需一次）
git remote add upstream https://github.com/原作者/仓库名.git

# 2. 拉取上游更新
git fetch upstream

# 3. 合并到本地
git checkout master
git merge upstream/master

# 4. 推送到你的 Fork
git push origin master
```

---

**最后更新：** 2026-06-25

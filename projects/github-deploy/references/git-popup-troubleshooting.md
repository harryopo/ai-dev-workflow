# Git 推送弹窗完整排查流程（v2.0）

> 适用：所有"git push 反复弹出 Git Credential Manager 窗口 / 反复要求输入用户名密码"场景

## 症状

```text
$ git push origin main
Username for 'https://github.com':
Password for 'https://2239868923@qq.com@github.com':
```

或者弹窗（Windows 上的 Git Credential Manager）反复出现，输入 token 也无效。

## 根因模型（双坑叠加）

### 坑 1：ghfast 镜像吞 Authorization 头

ghfast.top 是 GitHub 镜像代理，加速国内 fetch。但它**对 Authorization 头处理不完整**——

- fetch 时：客户端传 token，ghfast 转发到 GitHub，OK
- push 时：客户端传 token，ghfast **有时会丢 Authorization 头**，GitHub 收到 401
- Git 客户端检测到 401 → 弹出 Credential Manager 让你手动输入

### 坑 2：本地 insteadOf 规则链式重写

```bash
git config --global --get-regexp 'url\..*\.insteadOf'
# 输出：url.https://ghfast.top/https://github.com/.insteadof https://github.com/
```

`insteadOf` 规则会把 `https://github.com/` 自动改写为 `https://ghfast.top/https://github.com/`，但**会把 pushurl 里的 `https://x-access-token:ghp_xxx@...` 也重写**，导致 URL 解析错乱。

## 完整修复流程

### Step 1：删全局 insteadOf 规则

```bash
git config --global --get-regexp 'url\..*\.insteadOf'   # 先看
git config --global --unset 'url.https://ghfast.top/https://github.com/.insteadof'
git config --global --unset 'url.https://ghfast.top/.insteadof'
```

如果某个规则删不掉，编辑 `~/.gitconfig` 直接删除 `[url "..."]` 段。

### Step 2：检查仓库的 .git/config

```ini
[remote "origin"]
    url = https://ghfast.top/https://github.com/<owner>/<repo>.git
    pushurl = https://x-access-token:ghp_xxx@ghfast.top/https://github.com/<owner>/<repo>.git
```

**关键点：**

- `url` 走 ghfast 镜像（fetch 速度）
- `pushurl` 走 ghfast **+ URL 直接注入 token**（push 无弹窗）
- PAT 在 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic) 生成，**必须勾选 `repo` 权限**

### Step 3：测试 push

```bash
git push origin main
# 正常应该直接显示 To .../repo.git，无任何交互
```

### Step 4：如果仍弹窗

按顺序检查：

```bash
# 1. pushurl 是否生效
git config --get-regexp '^remote\.origin\..*url$'
# 应该看到 url 和 pushurl 两行

# 2. credential helper 是否干扰
git config --global --get-regexp 'credential\..*'
# 如果有 credential.helper=manager / manager-core → 临时清空
git config --global --unset credential.helper

# 3. URL 编码是否正确
# Token 中如果有 @ / : / ? 等特殊字符，必须 URL-encode
# 推荐直接用 x-access-token:ghp_xxx@ 格式，ghp_xxx 内不含特殊字符
```

## 速查命令

```bash
# 一键诊断（PowerShell）
git config --list --show-origin | Select-String -Pattern 'url|insteadOf|pushurl|credential' | Sort-Object
```

## 经验总结

1. **不要混用 insteadOf + pushurl**——两者都会重写 URL，会互相冲突
2. **不要在 URL 里直接放明文 token**——用 `x-access-token:ghp_xxx@` 格式，gh CLI 标准
3. **如果 fetch 慢，用镜像；如果 push 弹窗，用 pushurl 注入**
4. **每次新增仓库都要单独配 pushurl**——不会自动从主仓库继承

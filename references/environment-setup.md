# 环境配置清单

> 所属 Skill：`ai-dev-workflow`
> 目标：列出充分利用本 Skill 所需的完整开发和工具链环境

---

## 一、核心开发环境

### 1.1 版本控制

```bash
# Git（必须）
winget install Git.Git
# 或: https://git-scm.com/download/win

# 验证
git --version  # ≥ 2.40
```

### 1.2 Node.js 生态（前端 / 全栈项目）

```bash
# Node.js LTS（推荐使用 fnm 管理版本）
winget install Schniz.fnm
fnm install 20
fnm use 20

# pnpm（推荐，Monorepo 必备）
npm install -g pnpm

# 验证
node --version  # ≥ 20 LTS
pnpm --version  # ≥ 9
```

### 1.3 Python 生态（后端 / CLI / ML 项目）

```bash
# Python（推荐使用 uv 管理）
winget install Python.Python.3.12
# 或: https://www.python.org/downloads/

# uv（替代 pip + virtualenv，速度快 10-100x）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 验证
python --version  # ≥ 3.12
uv --version      # ≥ 0.4
```

### 1.4 容器化（所有项目推荐）

```bash
# Docker Desktop
winget install Docker.DockerDesktop
# 或: https://www.docker.com/products/docker-desktop/

# 验证
docker --version       # ≥ 26
docker compose version  # ≥ 2
```

---

## 二、代码质量工具链

### 2.1 TypeScript / JavaScript 项目

```bash
# 全局安装（可选，项目级更推荐）
pnpm add -g eslint prettier typescript

# 项目级安装（推荐）
pnpm add -D eslint prettier typescript @typescript-eslint/parser @typescript-eslint/eslint-plugin
pnpm add -D vitest @testing-library/react husky lint-staged
```

**推荐 VS Code 扩展：**

| 扩展 | ID | 用途 |
|------|-----|------|
| ESLint | `dbaeumer.vscode-eslint` | 代码检查 |
| Prettier | `esbenp.prettier-vscode` | 代码格式化 |
| Tailwind CSS IntelliSense | `bradlc.vscode-tailwindcss` | Tailwind 提示 |
| Pretty TypeScript Errors | `yoavbls.pretty-ts-errors` | 类型错误可读化 |

### 2.2 Python 项目

```bash
# 项目级安装（推荐）
uv add --dev ruff pytest pytest-cov mypy pre-commit

# 验证
ruff --version
mypy --version
pytest --version
```

**推荐 VS Code 扩展：**

| 扩展 | ID | 用途 |
|------|-----|------|
| Python | `ms-python.python` | Python 支持 |
| Pylance | `ms-python.vscode-pylance` | 类型检查 + 智能提示 |
| Ruff | `charliermarsh.ruff` | Linter + Formatter |
| Mypy Type Checker | `ms-python.mypy-type-checker` | 类型检查 |

### 2.3 通用工具

```bash
# pre-commit（Git hooks 管理）
pip install pre-commit  # 或: brew install pre-commit

# 配置文件: .pre-commit-config.yaml（见 templates/）
pre-commit install

# 验证
pre-commit --version
```

---

## 三、安全扫描工具链

### 3.1 必须安装

```bash
# truffleHog — 秘密检测（查找泄露的密钥/密码）
winget install trufflehog
# 或: pip install trufflehog3

# Semgrep — SAST 静态应用安全测试
pip install semgrep
# 或: brew install semgrep

# 验证
trufflehog --version
semgrep --version
```

### 3.2 推荐安装

```bash
# pip-audit — Python 依赖漏洞扫描
uv tool install pip-audit

# npm audit — Node.js 内置，无需额外安装
# npm audit  # 直接使用

# ggshield — GitGuardian 密钥检测（需要免费 API key）
pip install ggshield
ggshield auth login

# 验证
pip-audit --version
ggshield --version
```

---

## 四、IDE / AI 编程工具

### 4.1 IDE

| 工具 | 下载 | 说明 |
|------|------|------|
| **Trae** | trae.ai | 内置 Claude，Skill 原生支持 |
| **VS Code** | code.visualstudio.com | 生态最丰富 |
| **Cursor** | cursor.com | AI-first IDE，支持 .cursor/rules |
| **Windsurf** | codeium.com/windsurf | AI flow 模式 |

### 4.2 VS Code 配置（推荐）

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

```json
// .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "charliermarsh.ruff",
    "bradlc.vscode-tailwindcss"
  ]
}
```

---

## 五、环境验证脚本

安装完成后，运行以下脚本验证环境是否就绪：

```bash
#!/bin/bash
# verify-env.sh — 环境验证脚本

echo "=== 核心工具 ==="
echo -n "Git:       "; git --version 2>/dev/null || echo "❌ 未安装"
echo -n "Node.js:   "; node --version 2>/dev/null || echo "❌ 未安装"
echo -n "pnpm:      "; pnpm --version 2>/dev/null || echo "❌ 未安装"
echo -n "Python:    "; python --version 2>/dev/null || echo "❌ 未安装"
echo -n "uv:        "; uv --version 2>/dev/null || echo "❌ 未安装"
echo -n "Docker:    "; docker --version 2>/dev/null || echo "❌ 未安装"

echo ""
echo "=== 代码质量 ==="
echo -n "ESLint:    "; eslint --version 2>/dev/null || echo "⚠️ 建议全局安装"
echo -n "Prettier:  "; prettier --version 2>/dev/null || echo "⚠️ 建议全局安装"
echo -n "Ruff:      "; ruff --version 2>/dev/null || echo "⚠️ 建议安装"
echo -n "mypy:      "; mypy --version 2>/dev/null || echo "⚠️ 建议安装"
echo -n "pytest:    "; pytest --version 2>/dev/null || echo "⚠️ 建议安装"
echo -n "pre-commit:"; pre-commit --version 2>/dev/null || echo "⚠️ 建议安装"

echo ""
echo "=== 安全工具 ==="
echo -n "trufflehog:"; trufflehog --version 2>/dev/null || echo "❌ 必须安装"
echo -n "semgrep:   "; semgrep --version 2>/dev/null || echo "⚠️ 强烈建议"

echo ""
echo "=== 最小可用集 ==="
REQUIRED=(git node python)
for tool in "${REQUIRED[@]}"; do
  command -v $tool >/dev/null 2>&1 && echo "✅ $tool" || echo "❌ $tool (必须安装)"
done

echo ""
echo "=== 推荐安装但非必须 ==="
OPTIONAL=(pnpm uv docker trufflehog semgrep pre-commit ruff mypy)
for tool in "${OPTIONAL[@]}"; do
  command -v $tool >/dev/null 2>&1 && echo "✅ $tool" || echo "⬜ $tool"
done
```

**Windows PowerShell 版本：**

```powershell
# verify-env.ps1
Write-Host "=== 核心工具 ===" -ForegroundColor Cyan
@("git", "node", "pnpm", "python", "uv", "docker") | ForEach-Object {
    try { $v = & $_ --version 2>$null; Write-Host "✅ $_`: $v" -ForegroundColor Green }
    catch { Write-Host "❌ $_ 未安装" -ForegroundColor Red }
}

Write-Host "`n=== 代码质量 ===" -ForegroundColor Cyan
@("eslint", "prettier", "ruff", "mypy", "pytest", "pre-commit") | ForEach-Object {
    try { $v = & $_ --version 2>$null; Write-Host "✅ $_`: $v" -ForegroundColor Green }
    catch { Write-Host "⬜ $_ (建议安装)" -ForegroundColor Yellow }
}

Write-Host "`n=== 安全工具 ===" -ForegroundColor Cyan
@("trufflehog", "semgrep") | ForEach-Object {
    try { $v = & $_ --version 2>$null; Write-Host "✅ $_`: $v" -ForegroundColor Green }
    catch { Write-Host "❌ $_ (必须安装)" -ForegroundColor Red }
}
```

---

## 六、快速安装命令汇总（Windows）

```powershell
# === 一键安装所有核心工具 ===

# 1. Git
winget install Git.Git

# 2. Node.js + pnpm
winget install Schniz.fnm
fnm install 20; fnm use 20
npm install -g pnpm

# 3. Python + uv
winget install Python.Python.3.12
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 4. Docker
winget install Docker.DockerDesktop

# 5. 安全工具
pip install trufflehog3 semgrep pre-commit

# 6. 验证
# 然后运行 verify-env.ps1
```

---

## 七、按项目类型的最低环境要求

| 项目类型 | 必须 | 推荐 |
|---------|------|------|
| **全栈 Web** | Git + Node + pnpm + Python + uv + Docker | trufflehog + semgrep + pre-commit |
| **纯前端** | Git + Node + pnpm | trufflehog + semgrep + pre-commit |
| **纯后端(Python)** | Git + Python + uv + Docker | trufflehog + semgrep + pre-commit |
| **纯后端(Node)** | Git + Node + pnpm + Docker | trufflehog + semgrep + pre-commit |
| **小程序** | Git + Node + pnpm | trufflehog + pre-commit |
| **CLI 工具** | Git + {Python/Node} | trufflehog + pre-commit |
| **AI/ML** | Git + Python + uv + Docker | trufflehog + pre-commit |
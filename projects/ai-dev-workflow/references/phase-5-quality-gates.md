# 阶段五：质量门禁检查清单

> 所属 Skill：`ai-dev-workflow`
> 目标：确保代码在合并前通过所有质量门禁

---

## 1. 门禁流程

```
代码提交 → Gate 3（编码门禁）→ Gate 4（测试门禁）→ Gate 5（部署门禁）→ ✅ 合并
```

每个 Gate = 一组必须通过的自动化检查。🔴 = 阻塞（不通过不可合并），🟡 = 警告。

---

## 2. Gate 3：编码门禁

| # | 检查项 | 通过标准 | 自动化 | 级别 |
|---|--------|----------|--------|------|
| 3.1 | AI Code Review | AI 审查无高危发现 | 全自动 | 🔴 |
| 3.2 | Linter/Formatter | ESLint/Ruff/Prettier 零错误 | 全自动 | 🔴 |
| 3.3 | 类型检查 | tsc strict / mypy strict 通过 | 全自动 | 🔴 |
| 3.4 | 单元测试 | 新增代码行覆盖率 ≥ 85% | 全自动 | 🔴 |
| 3.5 | 依赖审计 | npm audit / pip-audit 无已知高危 | 全自动 | 🔴 |
| 3.6 | 秘密检测 | truffleHog / ggshield 无泄露 | 全自动 | 🔴 |
| 3.7 | 文件大小 | 单文件 ≤ 500 行 | AI 辅助 | 🟡 |
| 3.8 | 圈复杂度 | 单函数 ≤ 15 | 全自动 | 🟡 |
| 3.9 | 禁止模式 | 无 eval/innerHTML/硬编码密钥 | 全自动 | 🔴 |

---

## 3. Gate 4：测试门禁

| # | 检查项 | 通过标准 | 自动化 | 级别 |
|---|--------|----------|--------|------|
| 4.1 | 总覆盖率 | 行覆盖率 ≥ 80%，分支覆盖率 ≥ 70% | 全自动 | 🔴 |
| 4.2 | 集成测试 | 关键路径集成测试全部通过 | 全自动 | 🔴 |
| 4.3 | E2E 测试 | 核心用户流程通过 | 全自动 | 🔴 |
| 4.4 | SAST 安全扫描 | Semgrep/CodeQL 高危清零 | 全自动 | 🔴 |
| 4.5 | SCA 依赖扫描 | 无 Critical/High CVE | 全自动 | 🔴 |
| 4.6 | 性能回归 | P99 延迟 ≤ 基线 * 1.2 | 全自动 | 🟡 |
| 4.7 | 契约测试 | API 契约测试通过 | 全自动 | 🔴 |

---

## 4. Gate 5：部署门禁

| # | 检查项 | 通过标准 | 自动化 | 级别 |
|---|--------|----------|--------|------|
| 5.1 | 灰度发布验证 | 金丝雀 10% 流量 30 分钟无异常 | 全自动 | 🔴 |
| 5.2 | 回滚方案就绪 | 一键回滚脚本可用 | 人工 | 🔴 |
| 5.3 | 监控告警配置 | 关键 SLI 已配置告警 | 全自动 | 🔴 |
| 5.4 | 数据库迁移验证 | Migration 已小批量测试 | 全自动 | 🔴 |

---

## 5. AI 执行质量门禁的命令

```bash
# 编码门禁
pnpm lint              # 或 ruff check .
pnpm type-check        # 或 mypy .
pnpm test --coverage   # 或 pytest --cov

# 安全扫描
semgrep --config=auto .
npm audit              # 或 pip-audit

# 秘密检测
trufflehog filesystem .

# 门禁报告
pnpm gate-check        # 自定义脚本，汇总所有检查结果
```

---

## 6. AI Code Review 四层检查

AI 进行 Code Review 时，按以下四层递进：

```
第一层：AI 快速审查（≤ 5 分钟）
  → 代码风格、Bug 模式、安全漏洞初筛

第二层：自动化检查（并行）
  → Linter + 类型检查 + 测试 + SAST + 依赖审计

第三层：深度 AI 审查（PR > 500 行或核心模块触发）
  → 架构一致性、跨文件影响分析、数据流安全

第四层：人工终审
  → 业务逻辑正确性、设计方案合理性
```

---

## 7. 审查报告模板

```markdown
# Code Review 报告

## PR 信息
- PR #：...
- 作者：...
- 变更行数：+xxx / -xxx
- 涉及模块：...

## 自动检查结果
| 检查项 | 结果 | 详情 |
|--------|------|------|
| Linter | ✅/❌ | ... |
| 类型检查 | ✅/❌ | ... |
| 测试覆盖率 | xx% | ... |
| 安全扫描 | ✅/❌ | ... |
| 依赖审计 | ✅/❌ | ... |

## AI 发现的问题
### 🔴 高危
- ...

### 🟡 中危
- ...

### 🟢 低危
- ...

## 人工审查建议
- ...
```

---

## 8. v3.1 重构：4 大质量门禁（validate / garden / test / smoke-test）

> v3.0 是 3 个门禁（编码/测试/部署），v3.1 重构为 **4 大门禁**，对齐 wshobson-agents 模式。

### 8.1 4 大门禁定义

| Gate | 含义 | 阻塞性 | 触发频率 |
|------|------|--------|----------|
| **validate** | Lint + Format + Type check | ❌ 阻塞 | 每次 push |
| **garden** | AGENTS.md ≤ 150 行 / 文档漂移检测 | ⚠️ 警告 | 每次 push |
| **test** | 单元/集成/E2E + 覆盖率 | ❌ 阻塞 | 每次 PR |
| **smoke-test** | 安全审计 + 依赖审计 + mutation testing | ❌ 阻塞 | 每次 PR |

### 8.2 validate（编码门禁）

**目标**：确保代码风格一致、类型安全。

| 检查项 | 工具 | 通过标准 |
|--------|------|----------|
| ESLint | `pnpm lint` | max-warnings=0 |
| Prettier | `pnpm format:check` | 无 diff |
| TypeScript | `pnpm typecheck` | strict mode 0 错 |
| Ruff | `uv run ruff check .` | 0 错 |
| MyPy | `uv run mypy .` | strict 0 错 |

**对应文件**：`templates/.pre-commit-config.yaml`、`templates/github-actions-ci.yml` (Job 1: lint)

### 8.3 garden（漂移检测门禁）

**目标**：防止规范文档与代码脱节。

| 检查项 | 工具 | 通过标准 |
|--------|------|----------|
| AGENTS.md 行数 | `check-agents-md-length` | ≤ 150 行 |
| CLAUDE.md 同步 | 与 AGENTS.md 同步 | symlink 或 drift=0 |
| 目录约定 | 自定义脚本 | 符合 `core/ + features/ + cli/` |
| 业务分层 | `check-core-layer` | 薄层 ≤ 200 行 |
| 文档链接 | 自定义脚本 | 所有 markdown 链接可解析 |

**对应文件**：`templates/github-actions-ci.yml` (Job 7: agents-md-check)

### 8.4 test（测试门禁）

**目标**：确保功能正确、覆盖率达标。

| 检查项 | 工具 | 通过标准 |
|--------|------|----------|
| 单元测试 | `pnpm test` / `uv run pytest` | 全部通过 |
| 行覆盖率 | `--coverage` | 前端 ≥ 80% / 后端 ≥ 85% |
| 分支覆盖率 | 同上 | ≥ 75% |
| 集成测试 | `pnpm test:integration` | 全部通过 |
| E2E 测试 | Playwright | 核心流程通过 |
| 契约测试 | Pact / Dredd | API 契约符合 |

**v3.1 新增**：mutation testing 作为 test 门禁的可选强化项。

```bash
# TypeScript: Stryker
npx stryker run

# Python: mutmut / mewt
mutmut run
mewt run

# Go: go-mutesting
go-mutesting ./...

# Rust: cargo-mutants
cargo mutants
```

**目标 mutation score**：≥ 75%（Stryker 高 mutation 模式）

### 8.5 smoke-test（安全审计门禁）

**目标**：确保无安全漏洞、无秘密泄露、无依赖风险。

v3.1 扩展为 **7 检查**：

| # | 检查项 | 工具 | 通过标准 |
|---|--------|------|----------|
| 1 | Secret 检测 | gitleaks | 0 泄露 |
| 2 | Secret 检测（备份） | trufflehog | 0 verified 泄露 |
| 3 | SAST | Semgrep | 0 high/critical |
| 4 | 依赖审计 | pnpm audit | 0 high/critical |
| 5 | 依赖审计（Python） | pip-audit | 0 high/critical |
| 6 | CodeQL | GitHub CodeQL | 0 high/critical |
| 7 | **Prompt Defense Baseline**（v3.1 新增） | grep 自定义 | 无注入模式 |

**Prompt Defense Baseline 检查模式**：

```bash
# 注入模式黑名单（必须 0 命中）
PATTERNS=(
  "ignore previous instructions"
  "disregard prior"
  "forget your instructions"
  "system prompt"
  "you are now"
  "act as"
  "developer mode"
  "jailbreak"
)

for p in "${PATTERNS[@]}"; do
  if grep -rE "$p" --include="*.md" --include="*.txt" .; then
    echo "❌ Prompt injection pattern found: $p"
    exit 1
  fi
done
```

**对应文件**：`templates/github-actions-ci.yml` (Job 3: security)

### 8.6 build（构建门禁）

| 检查项 | 工具 | 通过标准 |
|--------|------|----------|
| 前端构建 | `pnpm build` | 0 错 |
| 后端构建 | `pnpm build:server` | 0 错 |
| Docker 构建 | `docker build` | 0 错 |
| Bundle Size | 自定义 | ≤ 预算 |

**对应文件**：`templates/github-actions-ci.yml` (Job 4: build)

### 8.7 commitlint（提交规范门禁，v3.1 强制）

| 检查项 | 通过标准 |
|--------|----------|
| Conventional Commits | type 在白名单内 |
| header-max-length | ≤ 100 字符 |
| **Assisted-by trailer** | **强制存在**（v3.1 强制） |
| body 不为空 | 是（feat/fix 强制） |

**v3.1 透明性铁律**：每个 commit 必须包含 `Assisted-by:` trailer。

```bash
# 正确示例
git commit -m "feat: 实现用户登录

- JWT 鉴权
- 密码哈希

Assisted-by: Claude Code (claude-sonnet-4-20250514)"

# 错误示例（缺 Assisted-by）
git commit -m "feat: 实现用户登录"
# → commitlint 会拒绝
```

**对应文件**：`templates/.pre-commit-config.yaml` (commitlint)、`templates/github-actions-ci.yml` (Job 5: commitlint)

### 8.8 pr-template（PR 模板门禁，v3.1 强制）

**强制必填 section**：

- Summary（变更摘要）
- Test（测试覆盖说明）
- Issue（关联 Issue）
- Assisted-by（透明性声明）
- Quality Gate Checklist（4 大门禁勾选）
- Deployment Notes（部署注意事项）

**CI 自动检查**：

```bash
REQUIRED=("Summary" "Test" "Issue" "Assisted-by")
for section in "${REQUIRED[@]}"; do
  if ! grep -qi "$section" .github/PULL_REQUEST_TEMPLATE.md; then
    echo "❌ Missing: $section"
    exit 1
  fi
done
```

**对应文件**：`templates/pr-template.md`、`templates/github-actions-ci.yml` (Job 6: pr-template)

### 8.9 4 大门禁汇总报告

每次 CI 完成后，GitHub Step Summary 输出：

```markdown
## 🚦 Quality Gate Report (v3.1 · 4 大门禁)

| Gate | Status | 阻塞性 |
|------|--------|--------|
| **validate** Lint & Type | success | ❌ 阻塞 |
| **garden** 漂移检测 | success | ⚠️ 警告 |
| **test** 测试覆盖 | success | ❌ 失败阻塞 |
| **smoke-test** 安全审计 | success | ❌ 失败阻塞 |
| **build** 构建 | success | ❌ 阻塞 |
| **commitlint** 提交规范 | success | ❌ 阻塞 |
| **pr-template** PR 模板 | success | ❌ 阻塞 |
```

**详细配置**：`templates/github-actions-ci.yml` (Job 8: gate-report)

---

## 9. v3.1 门禁规则与五大原则的对应

| 门禁 | 对应原则 | 失败后果 |
|------|----------|----------|
| validate | Principle-3 (Security-First) | 风格/类型错漏 |
| garden | Principle-1 (Agent-First) | AI 读不到完整规范 |
| test | Principle-2 (Test-Driven) | 无质量保证 |
| smoke-test | Principle-3 (Security-First) | 安全风险 |
| commitlint | Transparency | 透明性破坏 |
| pr-template | Transparency + Plan | 上下文丢失 |

---

## 10. v3.1 门禁跳过规则

**禁止事项**：
- ❌ 禁止 `git commit --no-verify` 跳过 commitlint
- ❌ 禁止 `gh pr merge --admin` 跳过 required checks
- ❌ 禁止 `[skip ci]` 跳过 smoke-test（仅在 doc-only PR 可用）

**允许的紧急绕过**：
- ✅ P0 线上事故 → hotfix 流程（详见 `templates/branch-protection.md` 第 6 节）
- ✅ doc-only PR → `[skip ci]` 跳过全部（但保留 commitlint）
- ✅ Draft PR → 可不通过门禁（仅 review 反馈）

---

## 11. 本地一键检查命令

```bash
# v3.1 一键全量检查（替代 pnpm gate-check）
make ci-local
# 或
./scripts/ci-local.sh

# 内容：
# 1. pre-commit run --all-files
# 2. pnpm lint && pnpm typecheck
# 3. pnpm test --coverage
# 4. mutation testing（可选）
# 5. semgrep --config=auto
# 6. gitleaks detect --no-git
# 7. AGENTS.md ≤ 150 行检查
```

---

## 12. v3.2 增强章节（基于用户反馈 2026-07-22 · 减法重构）

> **v3.2 关键变化：** v3.1 的 4 大门禁全部阻塞、AGENTS.md ≤ 150 硬卡、Assisted-by 必填被证明**过于严苛**。v3.2 重构为 **2 阻塞门（Security + Build）+ 5 报告门**。

### 12.1 4 大门禁的分级（v3.2 重构）

| Gate | v3.1 状态 | v3.2 状态 | v3.2 处理 | 何时恢复硬卡 |
|------|----------|----------|----------|------------|
| **validate** Lint & Type | ❌ 阻塞 | 🟡 报告 | warning only（允许 max-warnings=0 关闭） | 团队主动开启 |
| **garden** AGENTS.md ≤ 150 | 🟡 警告 | 🟡 报告 | warning only（推荐 ≤ 200） | 大型 monorepo |
| **test** 覆盖率 ≥ 85% | ❌ 阻塞 | 🟡 报告 | warning only（金融/医疗 ≥ 70% 推荐） | 库/SDK 代码 |
| **smoke-test** 安全 7 检查 | ❌ 阻塞 | 🔴 **阻塞（保留）** | R1-R5 红线 + 漏洞高危 | — |
| **build** 编译构建 | ❌ 阻塞 | 🔴 **阻塞（保留）** | 编译失败阻塞 | — |
| **commitlint** Assisted-by | ❌ 阻塞 | 🟡 报告 | warning only（不阻塞） | 长期项目可选 |
| **pr-template** Assisted-by | ❌ 阻塞 | 🟡 报告 | warning only（不阻塞） | 团队约定 |

**v3.2 哲学：** 安全红线绝不妥协（Security + Build 阻塞），规范建议不阻塞（其他 5 门仅报告）。

### 12.2 validate 门禁 v3.2 软化

| 检查项 | v3.1 标准 | v3.2 标准 | 变化原因 |
|--------|----------|----------|---------|
| ESLint | max-warnings=0 | 🟡 允许 warning | v3.1 过于严苛，团队调整 |
| MyPy | --strict | 🟡 默认配置 | strict 模式对小项目负担重 |
| Prettier | 0 diff | ✅ 保留 0 diff | 格式是低成本合规 |
| TypeScript strict | 必须开启 | 🟡 推荐 | 大型重构时 strict 阻塞升级 |

### 12.3 garden 门禁 v3.2 软化

| 检查项 | v3.1 标准 | v3.2 标准 |
|--------|----------|----------|
| AGENTS.md 行数 | ≤ 150 硬卡 | 🟡 ≤ 200 推荐（不阻塞） |
| 业务分层 | 薄层 ≤ 200 硬卡 | 🟡 ≤ 500 推荐（CLI 工具豁免） |
| CLAUDE.md 同步 | symlink 必填 | 🟡 推荐（非必须） |
| 目录约定 | check-core-layer 必过 | 🟡 warning only |

### 12.4 test 门禁 v3.2 软化

| 项目类型 | v3.1 标准 | v3.2 标准 |
|---------|----------|----------|
| Web 前端 | ≥ 80% 行覆盖 | 🟡 ≥ 60% 推荐 |
| API 服务 | ≥ 85% 行覆盖 | 🟡 关键路径 ≥ 70% 推荐 |
| 桌面应用 | ≥ 85% 行覆盖 | 🟡 关键路径（IPC、数据） |
| Mobile | ≥ 80% 行覆盖 | 🟡 关键路径 |
| CLI 工具 | ≥ 85% 行覆盖 | 🟢 不要求 |
| 库/SDK | ≥ 85% 行覆盖 | 🟡 公开 API ≥ 90% 推荐 |
| 原型/演示 | 必过 | 🟢 手动测试即可 |

**v3.2 关键路径优先原则：**
- ✅ 认证、支付、数据完整性 → 必须有测试
- ✅ 公开 API / 库代码 → 必须有测试
- 🟡 业务逻辑 → 推荐有测试
- 🟢 UI 组件 / 演示 / 原型 → 可有可无

### 12.5 commitlint 门禁 v3.2 软化

| 检查项 | v3.1 状态 | v3.2 状态 |
|--------|----------|----------|
| Conventional Commits | 🔴 必填 | ✅ 保留（推荐） |
| header-max-length ≤ 100 | 🔴 阻塞 | 🟡 推荐 |
| Assisted-by trailer | 🔴 必填 | 🟡 warning（个人项目可省略） |
| body 不为空 | 🟡 推荐 | 🟡 推荐 |

### 12.6 pr-template 门禁 v3.2 软化

| 必填 section | v3.1 状态 | v3.2 状态 |
|------------|----------|----------|
| Summary | 🔴 必填 | ✅ 必填（核心信息） |
| Test | 🔴 必填 | ✅ 必填（覆盖说明） |
| Issue | 🔴 必填 | ✅ 必填（关联问题） |
| Assisted-by | 🔴 必填 | 🟡 推荐（不阻塞） |
| Quality Gate Checklist | 🔴 必填 | 🟡 推荐（不阻塞） |
| Deployment Notes | 🟡 推荐 | 🟡 推荐 |

### 12.7 v3.2 阻塞门汇总（🔴 仅 2 个）

```
🚦 v3.2 阻塞门（不通过不可合并）：
  ├─ 🔴 smoke-test（Security 7 检查）→ R1-R5 红线 + 漏洞高危
  └─ 🔴 build（编译构建）→ 编译失败

📊 v3.2 报告门（不通过仅警告）：
  ├─ 🟡 validate（Lint & Type）→ 团队可选择性加强
  ├─ 🟡 garden（AGENTS.md 长度）→ 推荐 ≤ 200，不阻塞
  ├─ 🟡 test（覆盖率）→ 推荐关键路径 ≥ 70%，不阻塞
  ├─ 🟡 commitlint（提交规范）→ warning only
  └─ 🟡 pr-template（PR 模板）→ warning only
```

### 12.8 v3.2 跳过规则（更灵活）

**v3.2 允许的紧急绕过（扩展 v3.1）：**
- ✅ P0 线上事故 → hotfix 流程
- ✅ doc-only PR → `[skip ci]` 跳过全部（包含 commitlint）
- ✅ Draft PR → 可不通过门禁
- ✅ **新增**：lint/test 单项失败 → `continue-on-error: true` 不阻塞合并
- ✅ **新增**：Assisted-by 缺失 → 不阻塞，warning 提示

**v3.2 禁止事项（缩窄）：**
- ❌ 禁止 `gh pr merge --admin` 跳过 required checks（保留）
- ❌ 禁止 P0 事故跳过 smoke-test（保留）

### 12.9 阶段 5 的 v3.2 核心判断

```markdown
Q: 门禁应该多严？
A: 取决于 3 个问题：
  1. 项目类型？（Web/桌面/Mobile/API/CLI 应用强度不同）
  2. 团队规模？（单人/小团队/企业）
  3. 合规要求？（金融/医疗/普通）

v3.2 默认：🟡 报告门（5 个）+ 🔴 阻塞门（2 个）
v3.2 升级（金融/医疗）：🟡 + 🔴 全部
v3.2 简化（原型/演示）：🟡 全部 + 🔴 仅 build
```

> **v3.2 哲学转变：** 门禁是质量保证工具，不是质量惩罚。**功能优先，合规其次**。

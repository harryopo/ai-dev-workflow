# GitHub Branch Protection 规则（v3.2 · 2 阻塞门 + 5 报告门）

> **本文件可直接复制到 GitHub 仓库的 Settings → Branches → Branch protection rules。**
>
> 适配 ai-dev-workflow v3.2 的质量门禁：2 个阻塞门（Security + Build）+ 5 个报告门（validate/garden/test/commitlint/pr-template）。
> 配套 CI 工作流：`templates/github-actions-ci.yml`

---

## 一、Protected Branches 推荐配置

| 分支 | 保护级别 | 适用场景 |
|------|----------|----------|
| `main` / `master` | 🔒 最高 | 生产分支，仅通过 PR 合并 |
| `dev` / `develop` | 🔒 高 | 集成分支 |
| `release/*` | 🔒 中 | 发布分支（如 `release/v1.2`） |
| `feature/*` | ⚠️ 轻 | 个人特性分支（可 force-push） |

---

## 二、main 分支保护规则（推荐直接复用）

### Branch name pattern
```
main
```

### ⚙️ 1. Protect matching branches

- [x] **Require a pull request before merging**
  - [x] **Required approvals**: `1`（小团队）/ `2`（≥3 人团队）
  - [x] **Dismiss stale pull request approvals when new commits are pushed**
  - [x] **Require review from Code Owners**
  - [x] **Restrict who can dismiss pull request reviews**（仅 maintainer）

- [x] **Require status checks to pass before merging**
  - [x] **Require branches to be up to date before merging**
  - **Required status checks**（v3.2：2 阻塞门 + 5 报告门）：
    ```
    # ===== 阻塞门（不通过不可合并）=====
    security              → Job 3: Security Audit (smoke-test) — R1-R5 红线
    build                 → Job 4: Build — 编译失败
    
    # ===== 报告门（不通过仅警告）=====
    lint                  → Job 1: Lint & Type Check — 警告即可
    test                  → Job 2: Test & Coverage — 关键路径 ≥ 70% 推荐
    commitlint            → Job 5: Commit Convention Check — 警告即可
    pr-template           → Job 6: PR Template Check — 警告即可
    agents-md-check       → Job 7: AGENTS.md ≤ 200 lines (garden) — 推荐
    ```

- [x] **Require conversation resolution before merging**

- [x] **Require signed commits**（安全强化，可选）

- [x] **Require linear history**（推荐，禁止 merge commit）

- [x] **Include administrators**（管理员也必须遵守）

### ⚙️ 2. Rules applied to everyone including administrators

- [x] **Allow force pushes**: ❌ **禁用**
- [x] **Allow deletions**: ❌ **禁用**
- [x] **Allow force pushes to specific people**: ❌ **禁用**

### ⚙️ 3. Allow specified actors to bypass required pull requests

仅在紧急 hotfix 时由 maintainer 临时启用，并配合 `--admin` flag。

---

## 三、dev 分支保护规则

```yaml
Branch name pattern: dev

Protect matching branches:
  - Require a pull request before merging: ✅
  - Required approvals: 1
  - Require status checks to pass before merging: ✅
    Required checks: [lint, test, build]  # 简化版，3 个核心
  - Require linear history: ✅
  - Include administrators: ✅
```

> **降级策略**：dev 分支相比 main 减少 `security` 强制（仅报告），节省迭代时间。
> 任何合入 main 的 PR 必须先经过 dev 完整 CI 验证。

---

## 四、CODEOWNERS 文件（必配）

### 位置
```
.github/CODEOWNERS
```

### 内容（v3.1 业务分层 + 责任分配）

```gitignore
# v3.1 业务分层所有权

# ===== 默认 owner（所有 PR 都需要 review）=====
*                              @org/maintainers

# ===== 业务核心层（core-agent 主导）=====
/core/                         @org/core-team
/packages/core/                @org/core-team
/src/core/                     @org/core-team
/app/core/                     @org/core-team
/src/domain/                   @org/core-team

# ===== 前端 =====
/src/pages/                    @org/frontend-team
/src/features/                 @org/frontend-team
/src/components/               @org/frontend-team
/ui/                           @org/frontend-team

# ===== 后端 =====
/app/api/                      @org/backend-team
/src/api/                      @org/backend-team
/app/models/                   @org/backend-team
/migrations/                   @org/backend-team

# ===== 基础设施 =====
/.github/                      @org/devops-team
/.pre-commit-config.yaml      @org/devops-team
/infra/                        @org/devops-team
/docker-compose*.yml           @org/devops-team

# ===== 安全（强制 senior review）=====
/auth/                         @org/security-team
/security/                     @org/security-team
*.pem                          @org/security-team
*.key                          @org/security-team
```

### 关键规则
- [x] **Code Owners 必须 review 其负责的目录**（PR 中触及 `/core/` 必须 core-team 同意）
- [x] **Code Owners 不能 approve 自己的 PR**
- [x] **热修复（hotfix）** 即使绕过 OWNERS，也必须有 maintainer 第二人 review

---

## 五、Auto-merge 配置（v3.1 推荐）

### 启用条件
所有 Required status checks 全部通过 + 所需 approvals + 无 conversation unresolved → 自动 merge。

### 设置方式
1. 仓库 Settings → General → Pull Requests
2. ✅ **Allow auto-merge**
3. ✅ **Automatically delete head branches**

### 使用示例
```bash
# PR 满足所有条件后，本地或网页启用 auto-merge
gh pr merge --auto --squash
```

---

## 六、紧急绕过（Hotfix 流程）

> **仅限 P0 线上事故**，需 maintainer 决策后执行。

### 步骤
1. **创建 hotfix 分支**：`hotfix/{incident-id}-{short-desc}`
2. **跳过 PR 审批**：
   - 由 maintainer 临时关闭 "Include administrators"
   - 或使用 admin token 直接 push
3. **绕过 commitlint**：
   ```bash
   git commit --no-verify -m "hotfix: 修复 xxx 引起的事故
   
   - 紧急回滚到 v1.2.3
   - 添加防护措施
   
   Incident: INC-2026-0001
   Skip-CI-Reason: P0 线上事故"
   ```
4. **事后补齐**：
   - 24h 内补 issue 跟踪
   - 72h 内补完整 PR 流程

---

## 七、规则检查清单

部署后请用以下脚本自检：

```bash
# 检查 main 分支保护
gh api repos/:owner/:repo/branches/main/protection | jq .

# 列出所有必填 status checks
gh api repos/:owner/:repo/branches/main/protection/required_status_checks | jq .contexts

# 检查 CODEOWNERS 是否生效
gh api repos/:owner/:repo/codeowners/errors
```

---

## 八、与 v3.1 SKILL.md 的关联

| 规则 | SKILL.md 章节 | 配套模板 |
|------|---------------|----------|
| AGENTS.md ≤ 150 行 | §3 渐进式披露 | `templates/AGENTS.md` |
| commitlint Assisted-by 强制 | §0.2 红线 | `templates/.pre-commit-config.yaml` |
| 业务分层 ownership | §2 业务逻辑分层 | `templates/ownership.yaml` |
| 4 大门禁必过 | §5 质量门禁 | `templates/github-actions-ci.yml` |
| PR 模板必填 | §6 PR 流程 | `templates/pr-template.md` |

---

**v3.1 铁律**：
- ❌ 禁止 force-push 到 main
- ❌ 禁止绕过 CODEOWNERS
- ❌ 禁止 admin 跳过 required checks
- ✅ 紧急情况走 hotfix 流程并事后补齐

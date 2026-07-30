<!--
v3.2 Pull Request 模板（推荐结构）
配套：branch-protection.md 推荐项检查
-->

## Summary

<!-- 一句话总结本次 PR 做了什么 -->
> 例：实现用户登录功能（含 JWT 鉴权 + 密码哈希 + 单元测试）

### Changes
- 改动点 1
- 改动点 2
- 改动点 3

### Scope
<!-- 标记本次 PR 的范围 -->
- [ ] 🆕 New feature
- [ ] 🐛 Bug fix
- [ ] ♻️ Refactor
- [ ] 📝 Documentation
- [ ] ⚡ Performance
- [ ] 🧪 Tests only
- [ ] 🔧 Chore (CI/build/deps)

---

## Test

<!-- v3.2 推荐：描述测试覆盖情况（不强制）-->

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated (if applicable)
- [ ] Manual testing done
- [ ] All tests pass locally

### Test Details
<!-- 描述关键测试场景 -->
- 场景 1: xxx → ✅ passed
- 场景 2: xxx → ✅ passed
- 边界场景: xxx → ✅ passed

```bash
# 运行测试的命令
pnpm test
uv run pytest
```

### Coverage Report
<!-- 如果有覆盖率变化，标注 before/after -->
- Line coverage: 85% → 90%
- Branch coverage: 78% → 85%

---

## Issue

<!-- v3.1 强制：关联到具体 Issue -->
- Closes #
- Related to #
- Refs #

> 若无关联 issue，**必须说明原因**（紧急 hotfix / 重构 / 文档修复）

---

## Assisted-by

<!-- 🟡 v3.2 推荐：建议声明 AI/工具辅助情况（透明性原则），不强制 -->

| 工具 | 用途 | 占比 |
|------|------|------|
| Claude Code (claude-sonnet-4) | 架构设计 + 代码实现 | ~60% |
| Copilot | 代码补全 | ~10% |
| 人工 | 需求澄清 + 最终审核 | ~30% |

**Assisted-by:** Claude Code, GitHub Copilot

> 例：
> - `Assisted-by: Claude Code (claude-sonnet-4-20250514)`
> - `Assisted-by: GitHub Copilot`
> - `Assisted-by: 人工`（如果是纯人工实现，请说明）
>
> 多个工具用逗号分隔。
> **v3.2：推荐但不强制，不阻塞合并。**

---

## Quality Gate Checklist

<!-- v3.2 质量门禁（2 阻塞 + 5 报告）-->

### 阻塞门（不通过不可合并）
- [ ] **smoke-test**: 安全审计通过（gitleaks / Semgrep / CodeQL）— R1-R5 红线
- [ ] **build**: 编译构建通过

### 报告门（不通过仅警告，不阻塞合并）
- [ ] **validate**: Lint + Type Check（ESLint / Ruff / MyPy）— 警告即可
- [ ] **garden**: AGENTS.md ≤ 200 行（若本次修改了 AGENTS.md）— 推荐
- [ ] **test**: 关键路径测试覆盖 ≥ 70% — 推荐
- [ ] **commitlint**: Conventional Commits 格式 — 警告即可
- [ ] **pr-template**: 本模板必填项 — 警告即可

### 提交与文档
- [ ] Conventional Commits 格式（feat/fix/docs/...）— 推荐
- [ ] commit message 包含 `Assisted-by:` trailer — 🟡 推荐，不强制
- [ ] CHANGELOG.md 已更新（若需要）
- [ ] 公共 API 文档已更新（若需要）

### 业务分层（v3.2 软化为推荐）
- [ ] 业务逻辑推荐在 `core/`（不在 `cli/`、`mcp/`、`ui/`、`api/`）— 大 monorepo 推荐，CLI 工具可豁免
- [ ] 薄表现层文件 ≤ 500 行（推荐）— CLI 工具可豁免
- [ ] 没有跨层调用（如 `cli/` 直接 import `ui/`）— 推荐

### 安全检查
- [ ] 无 hardcoded secrets（API keys、tokens、passwords）— 🔴 红线
- [ ] 无新的外部依赖（若有，已通过 license + audit）
- [ ] 无 console.log / print 调试残留
- [ ] 无 TODO/FIXME 阻塞性遗留

---

## Code Review Notes

<!-- 给 Reviewer 看的重点 -->

### 重点 Review 项
- [ ] 业务逻辑正确性（特别是 `core/` 层）
- [ ] 边界条件处理
- [ ] 错误处理与日志
- [ ] 性能影响（特别是 hot path）

### 已知限制 / 遗留问题
<!-- 透明声明本次未完成的部分 -->
- 例：xxx 功能在 v3.2 跟进
- 例：xxx 边界场景暂未覆盖

---

## Deployment Notes

<!-- v3.2 推荐：声明是否需要特殊部署步骤（不强制）-->

- [ ] 无特殊部署步骤
- [ ] 需要数据库迁移（已附 migration）
- [ ] 需要环境变量更新
- [ ] 需要 feature flag 切换
- [ ] 涉及缓存失效
- [ ] 涉及 CDN 刷新

```bash
# 特殊部署步骤（若有）
pnpm run migrate
psql -f migrations/xxx.sql
```

---

## Screenshots / Recordings

<!-- UI 变更必须附图 -->

| Before | After |
|--------|-------|
| (screenshot) | (screenshot) |

### 录屏（可选）
- 录屏文件: [link]

---

## Additional Context

<!-- 其他需要 Reviewer 知道的背景 -->
- 相关 PR: #123
- 相关讨论: [link]
- 设计文档: [link]

---

## Reviewer Assignment

<!-- 自动 @ CODEOWNERS -->
/cc @org/core-team @org/frontend-team

---

<!--
📋 模板自检清单（提交前确认）：
- [ ] Summary 描述清晰
- [ ] Test 章节完整
- [ ] Issue 关联正确
- [ ] Assisted-by 透明声明
- [ ] Quality Gate Checklist 全勾
- [ ] 部署注意事项已声明
- [ ] UI 变更附截图
-->

**确认所有项目都已勾选 → 提交 PR**

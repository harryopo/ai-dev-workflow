# 绿门全禁机制详细指南

> **来源**：LEARNINGS.md LRN-20260722-001 经验 1 + 项目收尾经验总结报告_2026-07-30 第三章
> **适用**：所有 AI 辅助开发项目（无论项目类型）
> **核心结论**：**「绿门全禁」是必要非充分条件**——单跑 L1 三绿（lint+typecheck+build）只能证明"代码能跑"，不能证明"功能对"。

---

## 0. 一句话核心

> 单靠 L1 三绿门禁 = "只看图纸不验收房子"。要让代码真正"功能对"，必须跑 **L1 三绿门禁 + L2 质量门禁 + L3 端到端验证** 三层金字塔。

---

## 1. 真实案例：Phase 6 的认知突破

### 1.1 发生了什么

知行读书项目 Phase 6 实施了 11 项 UI 调整，全部跑通：

```bash
npm run lint       # ✅ 0 errors / 192 warnings
npm run typecheck  # ✅ exit 0
npm run build      # ✅ exit 0 in 1m16s
```

按 v3.1 之前所有规范，这是"完美完成"状态。

### 1.2 用户实测发现 5 个暗色模式 bug

| # | bug | 严重度 |
|---|-----|--------|
| 1 | shadow primitives opacity 0（实际无阴影）| P1 |
| 2 | 暗色 border == card 颜色（边框不可见）| P0 |
| 3 | 暗色 primary 跨主题不一致（浅色蓝 vs 暗色粉红）| P1 |
| 4 | 暗色 input 纯黑 `#000000`（显得压抑）| P2 |
| 5 | Badge 三 variant 对比度不足 WCAG AA | P0 |

### 1.3 根因：AI 从未真正"运行"应用去看 UI

三绿门禁检查的是：
- **lint**：代码风格、语法、潜在错误
- **typecheck**：类型正确性
- **build**：可编译性、可打包性

**三绿门禁不检查的：**
- 视觉错位、间距不一致
- 交互逻辑错误（点击没反应）
- 状态不同步、边界 case
- 真实数据下的渲染异常
- 暗色模式跨主题一致性
- WCAG 对比度

> **核心教训**：三绿门禁是"必要非充分条件"。**不跑三绿必出问题，只跑三绿也必出问题**（漏掉 L2 测试和 L3 端到端）。

---

## 2. 绿门全禁三层金字塔

```
       ╱╲
      ╱ L3 ╲      端到端验证（必跑，失败必修）
     ╱────────╲
    ╱   L2 质量  ╲  测试 + 覆盖率（关键路径必跑）
   ╱──────────────╲
  ╱    L1 三绿门禁  ╲  lint + typecheck + build（必跑）
 ╱──────────────────╲
```

### 2.1 L1 三绿门禁（必要条件 · 必跑 · 阻塞）

| 检查 | 命令 | 验证目标 |
|------|------|---------|
| **lint** | `npm run lint` | 代码风格、语法、潜在错误 |
| **typecheck** | `npm run typecheck` | 类型正确性 |
| **build** | `npm run build` | 可编译性、可打包性 |

**阻塞规则**：L1 任何一项失败 → 阻塞合并。

### 2.2 L2 质量门禁（按场景分级 · 关键路径必跑）

| 检查 | 命令 | 验证目标 | 适用项目 |
|------|------|---------|---------|
| **test** | `npm run test` | 关键路径功能正确 | 所有项目（关键路径必跑）|
| **test:cov** | `npm run test:cov` | 覆盖率达标 | 按项目类型分级（见 3.2）|

**L2 失败处理**：
- 关键路径测试失败 → 阻塞
- 非关键路径测试失败 → 警告
- 覆盖率不达标 → 警告（按场景决定目标）

### 2.3 L3 端到端验证（按项目类型必跑 · 失败必修）

| 项目类型 | L3 验证方式 | 推荐工具 | 必跑门槛 |
|---------|------------|---------|---------|
| **桌面应用** | dogfood（截图+复现步骤）| 真实启动 / Playwright 截图 | 关键 UI 流程 |
| **Web 应用** | E2E（Playwright/Cypress）| Playwright / Cypress | 关键用户路径 |
| **Mobile App** | 设备/模拟器真机测试 | Appium / Maestro | 关键功能流 |
| **API 服务** | 集成测试 + 契约测试 | Postman / Pact / 自写 | 关键 API 端到端 |
| **CLI 工具** | 命令行集成测试 | shell/snapshot 测试 | 主命令 + 边界 |
| **纯库/SDK** | consumer test（下游使用）| 文档编译测试 | 公开 API 覆盖 |

**L3 失败处理**：**失败必须修复**，不能"时间紧就绕过"。可临时记录到 LEARNINGS.md 后续修，但**不能宣告完成**。

---

## 3. 按项目类型的 L2/L3 配置

### 3.1 覆盖率目标（按项目类型）

| 项目类型 | lines | functions | branches | 关键模块 |
|---------|-------|-----------|----------|---------|
| **桌面应用** | 75% | 75% | 70% | 95% |
| **Web 应用** | 75% | 75% | 70% | 90% |
| **Mobile App** | 70% | 70% | 65% | 90% |
| **API 服务** | 80% | 80% | 75% | 95%（认证/支付）|
| **CLI 工具** | 60% | 60% | 55% | 80% |
| **纯库/SDK** | 85% | 85% | 80% | 95% |

> **基线策略**：当前覆盖率 - 2-3% 缓冲为最低门槛，逐步提升而非一次到位。

### 3.2 L3 端到端配置示例

#### 桌面应用（dogfood）

```bash
# 1. 启动应用
npm run build && npm run start

# 2. 真实操作关键流程
# - 启动 → 登录 → 主界面 → 设置 → 退出
# - 截图每个关键节点
# - 记录复现步骤

# 3. 提交截图 + 复现步骤
.dogfood/
├── 2026-07-30/
│   ├── 01-launch.png
│   ├── 02-login.png
│   ├── 03-main.png
│   └── REPRO.md
```

#### Web 应用（E2E）

```typescript
// tests/e2e/critical-paths.spec.ts
test('关键用户路径', async ({ page }) => {
  await page.goto('/')
  await page.click('text=登录')
  await page.fill('input[name=email]', 'user@test.com')
  await page.fill('input[name=password]', 'valid-pass')
  await page.click('button[type=submit]')
  await expect(page).toHaveURL('/dashboard')
})
```

#### API 服务（集成测试）

```python
# tests/integration/test_payment_flow.py
def test_payment_end_to_end():
    # 1. 创建订单
    order = client.post('/api/orders', json={...})
    # 2. 发起支付
    payment = client.post(f'/api/orders/{order.id}/pay', ...)
    # 3. 验证支付成功
    assert payment.status_code == 200
    # 4. 验证数据库
    assert get_order(order.id).status == 'paid'
```

---

## 4. 6 个绿门不跑必踩的坑

### G-1: 只跑 L1 不跑 L2-L3

**症状**：跑完 lint+typecheck+build 就宣布完成
**后果**：视觉错位、交互错误、状态不同步
**修复**：强制 L2+L3 必跑；AI 必须能回答"我跑了什么、看到了什么、为什么这样判断"

### G-2: L2 coverage 用通配符

**症状**：`coverage.include: ['src/**']`
**后果**：覆盖率虚高，包含未测试文件
**修复**：用精确文件列表
```json
{
  "coverage": {
    "include": [
      "src/main/services/**/*.ts",
      "src/renderer/features/**/*.tsx",
      "src/renderer/stores/**/*.ts"
    ]
  }
}
```

### G-3: L3 端到端用 mock 代替真跑

**症状**：测试用 mock 替代真实环境
**后果**："假绿"严重，mock 通过但实际不工作
**修复**：必须真实环境执行（启动应用、打开浏览器、调用真 API）

### G-4: L2 测试断言实际行为而非期望行为

**症状**：发现 bug 后写测试断言**错误行为**，"测试通过"
**后果**：测试假绿，bug 未修复
**修复**：
- 测试必须断言**期望行为**
- 或标记 bug → 后续修（不能长期挂着）
- 修完源码后必须更新断言为期望行为

### G-5: L1 build 通过但 L2 test 失败就合并

**症状**：测试失败但合并到主分支
**后果**：累计技术债，最终无法维护
**修复**：L2 失败阻塞（关键路径）或警告（非关键路径）

### G-6: L3 失败但被"时间紧"绕过

**症状**：端到端验证发现问题但"先发布再说"
**后果**："AI 说没问题但实际有问题"
**修复**：失败必须修复，记录到 LEARNINGS.md 后续修，**不能宣告完成**

---

## 5. 绿门全禁的"反问清单"

AI 完成开发任务后**必须**自问：

```
□ L1：lint 通过？typecheck 通过？build 通过？
□ L2：test 通过？覆盖率达标（按项目类型）？
□ L3：端到端验证通过？（截图/复现步骤齐全）
□ silent failure：关键功能有 logger.error，无 try-catch 静默吞？
□ 真实数据：演示/测试数据是真实可查的？
□ 审计独立：实施前 Read+Glob 验证了？
```

> **核心转变**：绿门全禁不是机械跑命令，而是**自问清单 + 实证验证**。AI 必须能回答"我跑了什么、看到了什么、为什么这样判断"。

---

## 6. 实施指南

### 6.1 CI/CD 配置

```yaml
# .github/workflows/green-gate.yml
name: Green Gate Full Prohibition

on: [push, pull_request]

jobs:
  l1-three-green:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint        # 必跑，失败阻塞
      - run: npm run typecheck   # 必跑，失败阻塞
      - run: npm run build       # 必跑，失败阻塞

  l2-quality:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test        # 关键路径必跑，失败阻塞
      - run: npm run test:cov    # 警告（按场景）
        continue-on-error: true

  l3-end-to-end:
    runs-on: ubuntu-latest
    needs: [l1-three-green, l2-quality]
    steps:
      - run: npm run test:e2e    # 必跑，失败阻塞
      - run: npm run dogfood     # 桌面应用，失败必修
        continue-on-error: true
```

### 6.2 本地开发检查

```bash
# 一键跑绿门全禁
npm run green-gate
# 等价于：
# npm run lint && npm run typecheck && npm run build && \
#   npm run test && npm run test:cov && npm run test:e2e
```

### 6.3 失败处理

| 层级 | 失败处理 |
|------|---------|
| **L1** | 阻塞 PR，必须修复后重跑 |
| **L2 关键路径** | 阻塞 PR，必须修复 |
| **L2 非关键路径** | 警告，可继续但不推荐 |
| **L3** | 失败必修，记录到 LEARNINGS.md，**不能宣告完成** |

---

## 7. 核心结论

1. **三绿门禁必要非充分**——L1 必跑，但**不**足够
2. **L3 端到端按项目类型定制**——桌面/Web/Mobile/API/CLI/库各有方式
3. **失败必须修复**——L3 失败不能"时间紧就绕过"
4. **绿门全禁是自问清单**——不是机械跑命令
5. **真实数据 + 审计独立**——绿门之外的辅助硬约束

> **最终警告**：单跑三绿门禁 = "AI 改完就说没问题"。跑绿门全禁 = "AI 改完能证明功能对"。这是 v3.3 的核心方法论升级。

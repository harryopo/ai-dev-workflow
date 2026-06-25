---
name: idea-to-dev
version: 1.0.0
description: |
  从用户的一个想法出发，深度调研市场方案和竞品，定位用户群体和差异化，评估可行性和预算，推荐技术栈与架构，输出完整开发方案并直接实施编码。支持生成小程序、桌面应用、手机App、网页、Claude Code Skill等多平台产品。当用户提到"我想做一个App"、"开发小程序"、"做个软件"、"创建网站"、"做个工具"、"从想法到产品"、"vibe coding"、"一键生成开发方案"时使用此技能。
argument-hint: "[你的产品想法]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Bash Search WebSearch Task
---

# 创意到开发 — 从灵感到可执行产品的一站式超级工作流

**使命**：把用户的模糊想法，通过系统化调研和分析，变成可直接开干的产品开发方案，然后直接编码交付。

**用户是决策者，你是参谋+工程师。**

## 适用场景

- 用户有明确的产品想法，需要从 0 到 1 的全流程指导
- 单平台 MVP 开发（小程序/桌面/网页/手机/Skill）
- Vibe Coding 模式：用户描述需求 → AI 写代码 → 用户测试

## 不适用场景

- 已有代码仓库的维护和迭代
- 需要同时生成多平台产品（每次只做一个平台）
- 需要企业级 CI/CD 流水线和 DevOps
- 用户只是咨询方法论而非实际开发产品

## 前置依赖

| 依赖 | 最低版本 | 用途 |
|------|---------|------|
| Node.js | 18+ | 小程序/网页/手机App 开发 |
| Python | 3.10+ | 桌面应用开发 |
| npm/yarn | 9+ | 包管理 |
| pip | 最新 | Python 包管理 |

## 支持的产品类型

| 类型 | 技术栈 | 模板目录 |
|------|--------|---------|
| 小程序 | Taro + React/TS | `${CLAUDE_SKILL_DIR}/templates/miniapp/` |
| 桌面应用 | Python + PySide6 + SQLite | `${CLAUDE_SKILL_DIR}/templates/desktop/` |
| 手机App | React Native + Expo | `${CLAUDE_SKILL_DIR}/templates/mobile/` |
| 网页应用 | Next.js + Tailwind CSS | `${CLAUDE_SKILL_DIR}/templates/web/` |
| Skill | SKILL.md 标准 | 内置模板 |

## 高风险行动黑名单

以下操作 **绝对禁止**：
- ❌ 自动部署到生产环境（必须用户手动确认）
- ❌ 自动发布到应用商店/小程序商店（必须用户手动操作）
- ❌ 在代码中硬编码 API 密钥、密码、Token 等敏感信息
- ❌ 执行 `rm -rf`、`del /s` 或类似危险删除命令
- ❌ 自动覆盖用户未确认的文件

以下操作 **需要用户确认**：
- ⚠️ 打包成 exe/app 等可分发格式
- ⚠️ 安装新的 npm/pip 依赖
- ⚠️ 创建新的数据库文件
- ⚠️ 修改项目配置文件

---

## 工作流程

```
阶段1: 创意澄清 → 01-创意澄清.md
  ↓ 用户确认
阶段2: 市场调研 → 02-市场调研报告.md
  ↓ 用户确认
阶段3: 定位与差异化 → 03-定位与差异化.md
  ↓ 用户确认
阶段4: 可行性评估 → 04-可行性评估.md
  ↓ 用户决策：做/不做
阶段5: 技术方案 → 05-技术方案.md
  ↓ 用户确认
阶段6: 开发实施 → 直接编码交付
  ↓ 用户测试
阶段7: 迭代优化 → 根据反馈改进
```

---

## 阶段1: 创意澄清

**目标**：把模糊想法变成清晰的产品定义。

**执行**：
1. 问用户：你的想法是什么？多模糊都行
2. 逐项确认（对话形式，不要一次甩10个问题）：
   - 核心功能、目标用户、触发场景、平台形态
   - 已有资源、时间预期、商业目标、竞品认知
3. 整理为结构化创意定义

**产出** → `idea-to-dev-output/01-创意澄清.md`
```markdown
# 创意澄清
## 一句话定义 / 核心功能 / 目标用户画像 / 使用场景
## 平台形态 / 用户现有资源 / 时间与商业预期
## 用户的竞品认知 / 我补充的优化方向
```

**完成后**：展示摘要，等用户确认。

---

## 阶段2: 市场深度调研

**目标**：搞清竞品和用户真实痛点。

**执行**：
1. 设计搜索关键词矩阵（中英文各3-5组）
2. 用 WebSearch 多轮搜索：竞品功能/用户评价/痛点/趋势
3. 每个竞品查3个维度：功能、评价、商业模式
4. 关键数据交叉验证，不采信单一来源

**产出** → `idea-to-dev-output/02-市场调研报告.md`
```markdown
# 市场深度调研报告
## 调研概要 / 现有方案盘点（名称/功能/长处/弊端/定价）
## 用户痛点汇总表 / 未被满足的需求 / 市场趋势判断
## 我补充的分析与建议
```

**完成后**：展示核心发现，等用户确认。

---

## 阶段3: 用户群体定位与差异化

**目标**：明确"做给谁"和"为什么选我们"。

**执行**：
1. 细分用户群体（规模/付费意愿/获取成本）
2. 选择主攻群体
3. 设计差异化策略

**产出** → `idea-to-dev-output/03-定位与差异化.md`
```markdown
# 用户群体定位与差异化
## 用户群体细分 / 主攻群体推荐 / 差异化策略
## 核心价值主张 / 我补充的优化方向
```

---

## 阶段4: 可行性评估与预算

**目标**：算清成本和风险，帮用户做"做/不做"决策。

**执行**：
1. 评估技术可行性、资源需求、风险
2. 拆解研发成本（人力+基础设施+第三方服务）
3. 给出"做/不做"推荐和理由
4. 建议 MVP 范围

**产出** → `idea-to-dev-output/04-可行性评估.md`
```markdown
# 可行性评估与预算
## 技术可行性 / 研发预算估算 / 风险评估表
## MVP 范围建议（必须有/最好有/可以没有）
## 我的推荐（做/不做 + 理由）
```

**关键决策点**：用户说"做"→ 阶段5；"不做"→ 结束；想调整→ 回对应阶段。

---

## 阶段5: 技术方案设计

**目标**：输出技术人员拿到就能开干的方案。

**执行**：
1. 确定产品类型和技术栈（2-3套方案对比）
2. 设计系统架构
3. 选型关键算法和第三方服务

**产出** → `idea-to-dev-output/05-技术方案.md`
```markdown
# 技术方案设计
## 产品类型确认 / 技术栈推荐（方案A/B对比表）
## 系统架构（核心模块/交互） / 关键算法与第三方服务
## 数据库设计概要 / 接口设计概要 / 安全与性能考量
## 我补充的优化方案
```

---

## 阶段6: 开发实施

**目标**：直接编码，交付可运行产品。

**核心理念**：Vibe Coding — 用户描述需求 → AI 写代码 → 用户测试 → 反馈 → AI 修复

**执行**：
1. 创建项目目录结构
2. 按平台技术规范编写代码（参考对应模板目录）
3. 实现核心功能
4. 运行测试

**各平台模板** → 参考 `${CLAUDE_SKILL_DIR}/templates/` 下对应目录：
- 小程序：`templates/miniapp/`（app.ts, app.config.ts, index.tsx, config.ts, package.json）
- 桌面应用：`templates/desktop/`（main.py, main_window.py, database.py, requirements.txt）
- 网页：`templates/web/`（page.tsx, layout.tsx, globals.css, route.ts）
- 手机App：`templates/mobile/`（_layout.tsx, index.tsx, app.json, package.json）

**开发命令速查**：
```bash
# 小程序
npm install -g @tarojs/cli && taro init 项目名 && npm run dev:weapp

# 桌面应用
pip install PySide6 && python main.py
pip install pyinstaller && pyinstaller --onefile --windowed --name AppName main.py

# 网页
npx create-next-app@latest 项目名 --typescript --tailwind --app && npm run dev

# 手机App
npx create-expo-app 项目名 --template blank-typescript && npx expo start
```

**注意事项**：
- 每个文件不超过 300 行
- 使用中文注释和类型注解
- 耗时操作用多线程（QThread / Web Worker / async）
- 路径处理用 `os.path`，不硬编码
- 资源文件用 `get_resource_path()` 函数

**常见错误处理** → 参考 `${CLAUDE_SKILL_DIR}/references/common-errors.md`

---

## 阶段7: 迭代优化

**执行**：
1. 收集用户反馈（功能/界面/性能/bug）
2. 按优先级排列改进项
3. 逐个修复并重新测试

---

## 全局规则

### 提问规则
- 每阶段开始前问 2-3 个关键问题
- 用户答不了的先跳过，后续再补

### 调研规则
- 每次至少搜索 3 轮不同关键词
- 关键结论必须标注来源链接
- 数据有冲突时说明倾向性判断及理由

### 主动优化规则
- 每个"我补充的优化方向"是必填项
- 优化建议要具体可执行
- 敢于提出不同建议，但要说清理由

### 阶段门控规则
- 每阶段完成后汇报核心结论并等确认
- 用户可要求回到任意阶段修改
- 用户说"全流程跑一遍"可省略中间确认

### 编码规范
- 中文注释、类型注解、每文件 ≤300 行
- 错误处理完善、给用户友好提示
- 代码修改后必须检查是否正确实现

### 全网搜索最佳实践
- 开发前先搜索相关开源项目
- 优先使用成熟方案，不闭门造车

---

## 参考资料

- 平台选择指南：`${CLAUDE_SKILL_DIR}/references/platform-comparison.md`
- Skill 开发指南：`${CLAUDE_SKILL_DIR}/references/skill-dev-guide.md`
- 常见错误处理：`${CLAUDE_SKILL_DIR}/references/common-errors.md`

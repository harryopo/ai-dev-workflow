# topics.md — idea-to-dev 主题索引

> 本文件索引 idea-to-dev Skill 的核心主题，方便快速定位。

---

## 版本

- **当前版本**：v2.2
- **版本历史**：见 [project_memory.md](./project_memory.md)

---

## 核心主题

### 1. 工作流程

| 主题 | 说明 | 对应章节 |
|------|------|---------|
| 智能路由 | 4种项目类型分发（A/B/C/D） | [SKILL.md](./SKILL.md) §智能路由 |
| 6段流水线 | 阶段0~5 完整工作流（类型3专用） | [SKILL.md](./SKILL.md) §工作流程总览 |
| 5门控机制 | G1~G5 用户确认点 | [SKILL.md](./SKILL.md) §门控规则 |
| 阶段0 澄清 | 智能询问 + 动态问题清单 | [SKILL.md](./SKILL.md) §阶段0 |
| 阶段1 调研 | agent-reach + deep-research 多平台并发 | [SKILL.md](./SKILL.md) §阶段1 |
| 阶段2 可行性+平台推荐 | 决策树 + 加权评分矩阵 | [SKILL.md](./SKILL.md) §阶段2 |
| 阶段3 方案书 | ★必选/△可选/○高阶 章节裁剪 | [SKILL.md](./SKILL.md) §阶段3 |
| 阶段4 质量自检 | Q1-Q6必过 + Q7-Q12可选 | [SKILL.md](./SKILL.md) §阶段4 |
| 阶段5 编码+沉淀 | Vibe Coding + steering/ | [SKILL.md](./SKILL.md) §阶段5 |

### 2. 智能路由（v2.2新增）

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| 4种项目类型 | 类型1（明确需求）/B（需选型）/C（复杂系统）/D（快速原型） | [SKILL.md](./SKILL.md) §智能路由 |
| 流程精简规则 | A:3问+编码 / B:5问+精简方案书 / C:完整流程 / D:直接编码 | [project_memory.md](./project_memory.md) §v2.2新增内容 |
| 智能询问机制 | 从输入推断已知信息，只问不确定的内容 | [SKILL.md](./SKILL.md) §阶段0 |
| 动态问题清单 | 基于推断结果生成个性化问题列表 | [references/pre-dev-30-questions.md](./references/pre-dev-30-questions.md) |

### 3. 质量门禁

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| Q1-Q6 核心检查 | 所有项目必过 | [references/quality-checklist.md](./references/quality-checklist.md) |
| Q7-Q12 进阶检查 | 类型3必过，类型1/B可选 | [references/quality-checklist.md](./references/quality-checklist.md) |
| 分层门禁规则 | A/B: Q1+Q2+Q6 / C: Q1-Q12 / D: 无 | [SKILL.md](./SKILL.md) §阶段4 |
| 空话检测 | 8类反模式 + 替换建议 | [references/quality-checklist.md](./references/quality-checklist.md) §空话检测清单 |
| evals 质量用例 | quality-01~04 方案书质量测试 | [evals/evals.json](./evals/evals.json) |

### 4. 方案书与模板

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| 12章方案书模板 | ★必选/△可选/○高阶 章节裁剪 | [references/engineering-plan-template.md](./references/engineering-plan-template.md) |
| 精简方案书 | 类型1/B专用（5-6章） | [references/engineering-plan-template.md](./references/engineering-plan-template.md) |
| 文件索引 | 产出物>3个时自动生成 | [project_memory.md](./project_memory.md) §v2.2新增内容 |
| 30问澄清清单 | 动态问题生成基础 | [references/pre-dev-30-questions.md](./references/pre-dev-30-questions.md) |

### 5. 平台开发

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| 平台决策树 | 基于约束客观推荐平台 | [references/platform-decision-tree.md](./references/platform-decision-tree.md) |
| 加权评分矩阵 | 7维度评分 + 推荐论证 | [references/platform-scoring-matrix.md](./references/platform-scoring-matrix.md) |
| 小程序开发指南 | 开发者工具/预览/云开发/类目资质 | [references/platform-dev-guide-miniprogram.md](./references/platform-dev-guide-miniprogram.md) |
| App开发指南 | Xcode/Android Studio/证书/上架 | [references/platform-dev-guide-app.md](./references/platform-dev-guide-app.md) |
| Web开发指南 | 服务器/域名/SSL/ICP/一键部署 | [references/platform-dev-guide-web.md](./references/platform-dev-guide-web.md) |
| 桌面开发指南 | Electron/Tauri/Qt/签名/分发 | [references/platform-dev-guide-desktop.md](./references/platform-dev-guide-desktop.md) |
| 国内合规清单 | ICP/软著/虚拟支付/数据安全 | [references/china-compliance.md](./references/china-compliance.md) |

### 6. 模板与产物

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| 小程序模板 | Taro + React/TS | [templates/miniapp/](./templates/miniapp/) |
| 桌面模板 | Python + PySide6 + SQLite | [templates/desktop/](./templates/desktop/) |
| Web模板 | Next.js + Tailwind | [templates/web/](./templates/web/) |
| 手机App模板 | React Native + Expo | [templates/mobile/](./templates/mobile/) |

### 7. 测试与评估

| 主题 | 说明 | 对应文件 |
|------|------|---------|
| evals.json | 23个测试用例（19基础+4路由+2质量） | [evals/evals.json](./evals/evals.json) |
| 路由判断用例 | routing-01~04 测试4种项目类型识别 | [evals/evals.json](./evals/evals.json) |
| 质量边界用例 | quality-03/04 过度工程化/精简得当案例 | [evals/evals.json](./evals/evals.json) |

---

## 快速导航

| 我想... | 去这里 |
|--------|--------|
| 了解完整工作流程 | [SKILL.md](./SKILL.md) |
| 查看智能路由规则 | [project_memory.md](./project_memory.md) §智能路由 |
| 查看质量自检清单 | [references/quality-checklist.md](./references/quality-checklist.md) |
| 运行测试用例 | [evals/evals.json](./evals/evals.json) |
| 查看版本历史和变更记录 | [project_memory.md](./project_memory.md) |
| 查看平台推荐决策树 | [references/platform-decision-tree.md](./references/platform-decision-tree.md) |
| 查看12章方案书模板 | [references/engineering-plan-template.md](./references/engineering-plan-template.md) |

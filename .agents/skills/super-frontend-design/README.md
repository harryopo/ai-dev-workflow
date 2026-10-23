# super-frontend-design

> 前端设计全流程工作台 — 调研驱动设计，覆盖网页、移动端、桌面端全场景。

[![Version](https://img.shields.io/badge/version-2.10.0-blue)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

---

## 一句话介绍

**调研是核心，无调研不设计。**

`super-frontend-design` 是一个前端设计全流程 Skill，通过 **15 维度深度调研** 引导 AI 完成从需求分析到高质量 UI 实现的完整设计闭环。支持网页、移动端、桌面端（Electron/Tauri/PySide6/SwiftUI）全场景设计。

---

## 核心能力

### 15 维度深度调研

设计前的必做动作，通过 5 轮对话收集完整需求：

| 轮次 | 维度 | 示例问题 |
|------|------|---------|
| 第1轮 | 设计类型 × 企业参考 | "这是一个 SaaS 产品官网还是后台管理系统？想参考哪家产品的感觉？" |
| 第2轮 | 视觉风格 × 配色 × 暗色模式 | "偏向极简/编辑/工业/奢华还是趣味风格？要不要暗色模式？" |
| 第3轮 | 技术栈 × 响应式 × 交互复杂度 | "使用 React+Tailwind 还是 Vue+Nuxt？需要移动端适配吗？" |
| 第4轮 | 品牌人格 × 情绪板 × 设计禁忌 | "如果这个产品是一个人，他是什么性格？有什么绝对不能出现的元素？" |
| 第5轮 | 动效方向 × 交互节奏 × 字体偏好 | "需要滚动驱动动画还是简单的入场效果？有无指定字体？" |

> 第 4 轮决定设计灵魂、第 5 轮决定体验品质，两轮均不可跳过（见 `subskills/research/SKILL.md`）。

调研产出 **Design Brief**，作为后续所有设计决策的输入依据。

### 六阶段工作流

```
research（15维度调研）
  → design-context（设计上下文初始化）
    → creative（灵感探索 · C端品牌场景在此发散 2-3 个方向）
      → theme（确定主题/配色）
        → design（设计实现 · 沿用用户选定方向）
          → review/critique（质量审查）
```

> **C 端品牌场景（Persuade / Experience）多一道方向发散**：creative 阶段产出 2–3 个完整独立方向（命名运动 + 视觉论文 + 关键 Token 提案），并置呈现带取舍分析，由用户选定其一；design 沿用该方向。B 端（Operate）与内容站（Read）跳过此步。详见 `subskills/creative/SKILL.md` §0.5。

### 九个子命令路由

| 子命令 | 触发词 | 功能 |
|--------|--------|------|
| `research` | 需求调研、设计参考、找参考 | 15维度调研 + 全网搜索 |
| `design-context` | 设计上下文、初始化项目 | PRODUCT.md + DESIGN.md 生成 |
| `creative` | 生成艺术、p5.js、粒子系统 | 算法艺术 + 视觉探索 + C端方向发散 |
| `design` | 设计页面、UI、重构前端 | 完整设计实现（含桌面端） |
| `theme` | 配色、字体、主题 | 10预设主题 + 自定义 + Token 输出 |
| `review` | 审查UI、设计评分 | 19维度检查 + 56条 Slop Test（其中可静态判定的部分由 `slop_scan.py` 执行，判定表见 `rules/slop-table.json`，其余人工核对） |
| `critique` | 深度审查、双代理审查 | Assessment A+B + 26条 Craft Floor |
| `refine` | polish、bolder、quieter | 命令式优化接口 |
| `animate` | 动效、GSAP、桌面动效 | 动效设计 + 跨平台动效方案 |

---

## 技术栈覆盖

### 网页应用
- React 19 + Tailwind CSS v4 + shadcn/ui
- Vue 3 + Nuxt 3
- 纯 HTML/CSS/JS
- Flutter Web

### 移动端
- React Native + NativeWind
- Flutter
- SwiftUI iOS/macOS
- Jetpack Compose Android

### 桌面应用
| 框架 | 技术栈 | 特点 |
|------|--------|------|
| **Electron** | React/Vue + Tailwind | 成熟生态，~150MB 安装包 |
| **Tauri** | Rust 后端 + Web 前端 | 轻量 ~3MB，类型安全 |
| **PySide6/Qt** | Python + QSS | 原生跨平台，企业级 |
| **SwiftUI** | Swift 5.9+ | Apple 原生生态 |

---

## 质量保证系统

### hallmark 双代理审查
- **Assessment A**：LLM 设计审查（设计灵魂追溯 + 主观质量评估）
- **Assessment B**：探测器/代码证据（可 Grep 的确定性检查）
- 两者对比生成 **Quality Score**（0-100）

### Craft Floor 26 条探测器规则
分三组：Verify 10 条（必须验证）、Refuse 10 条（发现即拒绝）、实现完整性 6 条

### 14 条精确反 AI 味规则
- 7 宗罪（AI 默认色、两色渐变 Hero、emoji 图标等 — design 必过、review 硬阻止）
- 4 软规则（标准 Section 序列、占位图 CDN、裸 hex 计数、accent 频次 — 警告可裁定）
- 3 抛光规则（data-section-id、装饰性背景、完美对称 — 建议修复）

---

## 快速开始

### 调用方式

```
/super-frontend-design
```

或通过触发词自动匹配：
- **设计场景**：设计、UI、UX、前端、landing page、dashboard、app
- **优化场景**：polish、bolder、quieter、重构、升级、美化页面
- **审查场景**：审查UI、critique、深度审查
- **动效场景**：animate、动效、GSAP
- **桌面场景**：Electron、Tauri、PySide6、SwiftUI

### 示例对话

**场景 1：全新 SaaS 官网设计**
```
用户：帮我设计一个 AI 数据分析产品的官网
→ 触发 15 维度调研（5轮对话）
→ 产出 Design Brief
→ 确定视觉方向（极简科技风）
→ 生成完整 HTML/CSS/JS 实现
→ review/critique 质量审查
```

**场景 2：Electron 桌面应用重构**
```
用户：我的 Electron 应用 UI 太丑了，帮我重构
→ 路由到 design 子命令
→ 加载 electron.md 模板
→ 参考 desktop-patterns.md 三栏布局
→ 参考 professional-software.md Linear 模式
→ 输出完整 Electron + React 代码
```

**场景 3：桌面应用动效设计**
```
用户：给这个 PySide6 应用加窗口动画
→ 路由到 animate 子命令
→ 加载桌面动效规范
→ 使用 QPropertyAnimation + QEasingCurve
→ 输出 Python 动画代码
```

---

## 项目结构

```
super-frontend-design/
├── SKILL.md                        # 主入口：路由 + 工作流 + 约束
├── references/                     # 参考知识
│   ├── desktop-patterns.md         # 桌面应用模式库（10模式）
│   ├── professional-software.md    # 专业软件设计模式（11款分析）
│   ├── token-mapping.md            # 跨平台 Design Token 映射
│   ├── motion-patterns.md          # 桌面端动效方案库
│   ├── macrostructures.md          # 21种 Macrostructure 路由
│   ├── themes.md                   # 20种命名主题风格
│   ├── palettes.md                 # 161色板数据
│   ├── font-pairings.md            # 57字体对
│   ├── ux-guidelines.md            # 99条UX准则
│   ├── anti-ai-slop.md             # 14条反AI味规则
│   ├── premium-design-rules.md     # 16条高级感规范
│   ├── admin-enterprise-patterns.md # B端/企业软件设计模式库
│   ├── design-systems/             # 4个内置设计系统预设（TDesign/Ant/M3/shadcn）
│   └── ...
├── subskills/                      # 子命令实现
│   ├── research/SKILL.md           # 15维度调研
│   ├── design-context/SKILL.md     # 设计上下文
│   ├── creative/SKILL.md           # 灵感探索（C端 §0.5 方向发散）
│   ├── design/SKILL.md             # 设计实现（含桌面/移动端）
│   ├── theme/SKILL.md              # 主题系统
│   ├── review/SKILL.md             # 快速审查
│   ├── critique/SKILL.md           # 深度审查
│   ├── refine/SKILL.md             # 命令式优化
│   └── animate/SKILL.md            # 动效设计（含桌面动效）
├── scripts/
│   ├── audit_integrity.py          # 结构自检门禁（46 项）
│   ├── slop_scan.py                # 静态反 AI 味门禁（30 条）
│   ├── token_lint.py               # Token 门禁
│   ├── structure_lint.mjs          # CSS/HTML 结构门禁
│   ├── render_probe.py             # 渲染量测门禁（Playwright）
│   ├── visual_diff.py              # 参考图逐像素对账
│   ├── random_draw.py              # 结构化随机抽签（os.urandom 等概率）
│   └── apca_contrast.mjs           # APCA Lc 计算器
├── templates/
│   └── prompt-templates/
│       ├── react-tailwind.md       # React+Tailwind 模板
│       ├── vue-nuxt.md             # Vue+Nuxt 模板
│       ├── electron.md             # Electron 桌面模板
│       ├── tauri.md                # Tauri 桌面模板
│       ├── pyside6.md              # PySide6/Qt 模板
│       ├── swiftui.md              # SwiftUI 模板
│       └── ...
└── evals/
    └── evals.json                  # 评测集
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.10.0 | 2026-10-23 | 参考机制 2.0 Phase 2 原创引擎接线：C 端品牌场景方向发散（creative §0.5）+ 二阶反射检查（review §0 #11 / critique）+ 结构化随机兜底（research + random_draw.py） |
| v2.9.1 | 2026-10-23 | 版本治理收口：9 个子技能删除各自 version 字段（主 SKILL.md 为唯一真值源）+ 新增 version-field 门禁；Slop Test 56/30 口径在索引与 README 补说明 |
| v2.9.0 | 2026-10-16 | 参考机制 2.0：参考维度追问 + 反参考 + 参考距离分级 + 反收敛样本池 + 饱和赛道黑名单 + 情绪板参数推导 |
| v2.8.1 | 2026-10-16 | 现有风格重构流程（风格审计 + 设计稿确认门 + 风格固化 + 项目设计规范优先约束） |
| v2.8.0 | 2026-10-11 | 软件设计增强（B端模式库+4款专业软件分析）、字号层级/圆角收敛门禁检查、4个内置设计系统预设、国内企业级组件库接入 |
| v2.7.0 | 2026-08-10 | 新增桌面端支持（Electron/Tauri/PySide6/SwiftUI），新增 4 个参考文件，新增 4 个 Prompt 模板 |
| v2.6.0 | 2026-08-09 | 新增 refine 子命令（polish/bolder/quieter/distill/harden） |
| v2.5.0 | 2026-08-09 | 集成 GSAP 动效系统，增强双代理评估 |
| v2.4.0 | 2026-08-08 | hallmark 审查系统，Craft Floor 探测器规则 |
| v2.3.0 | 2026-08-07 | 15维度深度调研，5轮对话 |
| v2.0.0 | 2026-08-06 | 完整重构：六阶段工作流，九子命令路由 |

---

## 相关 Skill

| Skill | 用途 |
|-------|------|
| `impeccable` | 设计指导与 AI 代码审查规则（本 Skill 的审查方法论来源） |
| `frontend-design` | 快速单页面设计（轻量版） |
| `ui-ux-pro-max` | 设计数据库查询（色板/字体/风格） |
| `skill-workspace` | Skill 工作台（审查/管理/部署） |

---

## 开发说明

### 扩展新参考文件

在 `references/` 目录下创建新 Markdown 文件，并在 `SKILL.md` 的 §6 参考资料索引表中添加条目。

### 扩展 Prompt 模板

在 `templates/prompt-templates/` 目录下创建新模板，并在 `subskills/design/SKILL.md` 的技术栈路由表中添加映射。

### 运行评测

```bash
python -m pytest evals/ -v
```

---

## License

MIT

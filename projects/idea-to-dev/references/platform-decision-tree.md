# 平台推荐决策树

> 来源：调研报告 §四
> 用途：阶段 2 平台推荐的核心决策工具

## 使用方法

每个节点是一个问题，依次询问/推断后沿分支下行，落到叶子即推荐形态。**落到叶子后必须输出"为什么选 X"+"为什么不选 Y"的论证。**

---

## 决策树（主流程）

```
Q1. 产品是否主要面向"开发者/技术人群"且以自动化/效率为核心？
├─ 是 → Q2. 是否需要嵌入现有 AI Agent / IDE / CLI 工作流？
│       ├─ 是 → 推荐：Claude Skill / MCP Server / IDE 插件
│       └─ 否 → Q3. 是否纯命令行交互即可？
│               ├─ 是 → 推荐：CLI（Rust 性能 / Go 运维 / Python 数据 / Node 生态）
│               └─ 否 → 推荐：开发者工具型桌面应用（Tauri/Electron）
└─ 否 → Q4. 是否必须运行在用户手机上、且需要强系统集成（摄像头/蓝牙/后台/推送）？
        ├─ 是 → Q5. 是否国内 C 端 + 依赖微信社交裂变？
        │       ├─ 是 → 推荐：微信小程序（+ 公众号/视频号）
        │       └─ 否 → Q6. 是否双端都要 + 预算有限 + UI 为主？
        │               ├─ 是 → 推荐：Flutter（一致性 UI）/ RN（JS 团队 + Expo）
        │               └─ 否 → 推荐：原生（SwiftUI / Compose）—— 单端或旗舰体验
        └─ 否 → Q7. 是否需要深度桌面系统集成（全局快捷键/托盘/大文件/离线）？
                ├─ 是 → 推荐：桌面应用（Tauri 首选 / Electron 生态优先 / Qt 工业软件）
                └─ 否 → Q8. 是否主要面向浏览器、需要 SEO、需要全球即时触达？
                        ├─ 是 → 推荐：Web 应用（Next.js / Nuxt / SvelteKit / Astro）
                        └─ 否 → Q9. 是否需要增强既有浏览器/网页体验？
                                ├─ 是 → 推荐：浏览器扩展（MV3 + Plasmo）
                                └─ 否 → 默认回退：Web 应用（最通用）
```

---

## 决策树护栏规则

1. **落到叶子后，必须输出论证**：
   - "为什么选 X"（命中用户的高权重约束）
   - "为什么不选 Y"（次优 1-2 项的否决理由）

2. **冲突处理**：若用户需求与多个叶子冲突，必须列出冲突点并请用户澄清，不可强行二选一

3. **国内场景自动叠加合规检查**（见 `china-compliance.md`）：
   - Web 需 ICP 备案
   - 小程序需类目资质
   - App 需软著
   - AI 应用需模型备案

4. **禁止越级**：在未采集约束前不可直接给结论

---

## 各叶子节点的默认推荐栈

### Claude Skill / MCP Server / IDE 插件
- **Skill**：SKILL.md 标准（description + 正文 SOP + 约束）
- **MCP Server**：TypeScript/Python SDK
- **IDE 插件**：VS Code（TypeScript）/ JetBrains（Kotlin）

### CLI
- **Rust**：极致性能（clap）
- **Go**：运维工具（cobra）
- **Python**：数据/AI（click/typer）
- **Node**：JS 生态（commander）

### 桌面应用（开发者工具型）
- **Tauri 首选**：包体 3-10MB，Rust 后端 + Web 前端
- **Electron 备选**：生态最成熟，但内存高

### 微信小程序
- **原生**：WXML/WXSS/JS（纯微信项目）
- **uni-app**：Vue 语法，多端覆盖最广
- **Taro**：React 语法，多端编译

### 跨端 App
- **Flutter**：UI 一致性、动画密集
- **RN + Expo**：JS 团队、快速 MVP

### 原生 App
- **iOS**：SwiftUI + SwiftData/CloudKit
- **Android**：Jetpack Compose + KMP

### 桌面应用（通用）
- **Tauri 首选**（包体小、安全好）
- **Electron 备选**（生态优先）
- **PySide6**（Python 团队）
- **Qt**（工业软件）

### Web 应用
- **Next.js**：全栈 React，Vercel 原生
- **Nuxt**：全栈 Vue
- **SvelteKit**：性能极致
- **Astro**：内容站点

### 浏览器扩展
- **Manifest V3**（Chrome 强制）
- **Plasmo** 框架（React + 热重载）

---

## 与加权评分矩阵的配合

决策树得到候选 Top 2-3 后，用 `platform-scoring-matrix.md` 的加权评分确认最终推荐。

**典型流程**：
1. 决策树推断 → 候选 [Web, 小程序]
2. 加权评分 → Web 得 92 分，小程序得 81 分
3. 输出推荐 Web + 论证 + 敏感性提示

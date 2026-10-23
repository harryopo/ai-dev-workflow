---
name: super-frontend-design:design-context
description: |
  设计上下文管理模块。管理 PRODUCT.md + DESIGN.md 项目级设计上下文，支持访客意图分类（Persuade/Operate/Read/Experience）、
  设计Token提取、Shape设计前规划、Design Brief生成。是设计灵魂（品牌人格+情绪板）的持久化载体。
  由 super-frontend-design 主入口路由调用。
  合并来源：impeccable (teach + extract + shape)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Design Context — 设计上下文管理

## 1. 概述

本模块负责管理项目级设计上下文，确保设计决策的一致性和可追溯性。通过 PRODUCT.md（产品定位）和 DESIGN.md（设计系统Token）实现设计上下文的持久化。

**核心能力：**
- 初始化项目设计上下文（teach 模式）
- 从现有代码库提取设计Token（extract 模式）
- 从参考设计提取设计模式（extract 模式）
- 设计前规划与brief生成（shape 模式）

---

## 2. 触发条件

以下关键词触发本模块：
- "设计上下文"、"初始化项目"、"teach"
- "PRODUCT.md"、"DESIGN.md"、"设计Token"
- "提取设计"、"参考解构"、"extract"
- "设计前规划"、"shape"、"UX规划"
- "访客意图"、"Persuade"、"Operate"、"Read"、"Experience"

---

## 3. 模式选择

根据用户意图选择工作模式：

| 模式 | 触发条件 | 输出 |
|------|----------|------|
| **init** | 新项目、首次初始化 | 创建 PRODUCT.md + DESIGN.md |
| **extract** | 从现有代码/参考设计提取 | 更新 DESIGN.md |
| **shape** | 设计前规划 | 创建 DESIGN_BRIEF.md |
| **read** | 读取现有上下文 | 显示当前上下文摘要 |

---

## 4. PRODUCT.md 模板

```markdown
# Product Context

## What
[产品描述：一句话说明产品是什么]

## Users
[目标用户：谁会用这个产品？]

## Journey
[用户旅程：核心流程步骤]
1. [步骤1]
2. [步骤2]
3. [步骤3]

## Metrics
[核心指标：如何衡量成功？]
- [指标1]
- [指标2]

## Visitor Mode
[访客意图分类]
- [ ] Persuade（说服型：落地页、营销页）
- [ ] Operate（操作型：应用、仪表盘）
- [ ] Read（阅读型：文档、指南）
- [ ] Experience（体验型：作品集、画廊）
```

---

## 5. DESIGN.md 模板

> **DESIGN.md 的三个来源**：① Design Brief 推导（默认路径）② 从现有代码/参考设计提取
> （extract 模式）③ **内置设计系统预设**——`references/design-systems/` 下有
> tdesign / ant-design / material-3 / shadcn-style 四个 9-section 预设，与本章模板
> 同构，可作为 init 的起点：按 Design Brief 的场景与人格选中一个后，**仍须经
> research 调研校准**（预设的基线色只是种子，品牌色、字体、禁忌以调研结论为准）。

> **设计稿确认门（按现有风格重构流程）**：生成 / 更新 DESIGN.md 后，它即该流程的「统一设计稿」——必须呈现给用户并得到明确确认（"设计稿是否 OK？确认后开始重构"）才能进入 design 实现。即使用户说"直接改"，呈现这一步也不可跳过。

```markdown
# Design System

## Colors
```css
:root {
  /* Primary */
  --color-primary: #XXXXXX;
  --color-primary-hover: #XXXXXX;
  --color-primary-active: #XXXXXX;

  /* Secondary */
  --color-secondary: #XXXXXX;

  /* Semantic */
  --color-success: #XXXXXX;
  --color-warning: #XXXXXX;
  --color-error: #XXXXXX;
  --color-info: #XXXXXX;

  /* Neutral */
  --color-surface: #XXXXXX;
  --color-surface-elevated: #XXXXXX;
  --color-on-surface: #XXXXXX;
  --color-border: #XXXXXX;
  --color-muted: #XXXXXX;
}
```

## Typography
```css
:root {
  --font-display: 'FontName', sans-serif;
  --font-body: 'FontName', sans-serif;
  --font-mono: 'FontName', monospace;

  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  --font-size-5xl: 3rem;
}
```

## Spacing
```css
:root {
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;
}
```

## Radius
```css
:root {
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;
}
```

## Shadow
```css
:root {
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

## Components
[组件规范：按钮、卡片、表单等]

## Brand Personality
[品牌人格：如"极客工程师"、"优雅设计师"等]

## Mood Board
[情绪板：3个关键词 + 参数推导（色相策略 / 字体气质 / 材质 / 动效性格）]

## Anti-references
[反参考：来自 research 第 1 轮——明确要避开的方向/品牌/感觉；无则写"无"]
```

---

## 6. Shape 工作流（设计前规划）

### 6.1 Discovery Interview（采访阶段）

使用 AskUserQuestion 进行结构化采访：

**问题 1：用户任务**
```
用户在这个页面上主要做什么？
- [ ] 获取信息（阅读、学习）
- [ ] 完成任务（操作、提交）
- [ ] 做出决策（比较、选择）
- [ ] 欣赏内容（浏览、体验）
```

**问题 2：访客意图**
```
这个页面的主要目的是什么？
- [ ] Persuade（说服用户采取行动）
- [ ] Operate（帮助用户完成操作）
- [ ] Read（帮助用户获取信息）
- [ ] Experience（帮助用户获得体验）
```

**问题 3：品牌人格**
```
品牌的人格特征是什么？（选择 1-3 个）
- [ ] 专业权威
- [ ] 友好亲切
- [ ] 激进创新
- [ ] 克制内敛
- [ ] 温暖包容
- [ ] 精致优雅
```

**问题 4：关键页面**
```
需要设计哪些关键页面？（多选）
- [ ] 首页/Landing Page
- [ ] 列表页
- [ ] 详情页
- [ ] 表单页
- [ ] 仪表盘/Dashboard
- [ ] 其他
```

**问题 5：设计约束**
```
有哪些设计约束？
- [ ] 品牌规范（提供品牌色/字体）
- [ ] 技术栈限制（React/Vue/纯HTML等）
- [ ] 参考设计（提供参考链接）
- [ ] 无障碍要求（WCAG AA/AAA）
- [ ] 性能要求（LCP < 2.5s 等）
```

### 6.2 Resolve Direction（方向确定）

基于采访结果确定设计方向：

| 访客意图 | 推荐 Macrostructure | 推荐 Theme 方向 |
|----------|-------------------|----------------|
| Persuade | Photographic · Bento Grid · Workbench | 温暖、高对比、视觉冲击 |
| Operate | Workbench · Feature Stack · Table | 清晰、紧凑、信息密度高 |
| Read | Editorial · Zigzag · Gallery | 阅读友好、舒适、慢节奏 |
| Experience | Gallery · Cinematic · Interactive | 沉浸、叙事、情感化 |

### 6.3 Write Brief（写brief）

输出 DESIGN_BRIEF.md：
```markdown
# Design Brief

## Project
[项目名称]

## Goals
[设计目标]

## Users
[目标用户]

## Pages
[关键页面列表]

## Style
- 品牌人格: [品牌人格]
- 情绪板: [情绪板关键词 + 参数推导]
- 反参考: [要避开的方向/品牌/感觉；无则写"无"]
- 访客意图: [访客意图]
- 参考距离等级: [结构借鉴 / 原理解构 / 显式复制]
- Macrostructure: [推荐结构]
- Theme: [推荐主题]

## Constraints
[设计约束]

## Success Criteria
[成功标准]
```

---

## 7. Extract 模式（设计Token提取）

### 7.1 从现有代码库提取

> 本小节是**现有风格重构流程**（主 SKILL.md §3.6）的执行部件：完整审计（扫描范围、门禁测量、不一致点清单、统一方案确认）见 research 子技能「现有风格审计模式」；审计确认后，由本模式把统一方案落成 DESIGN.md。

扫描以下位置提取设计Token：
- CSS 变量（:root 定义）与样式文件实际用法（裸值 / var() 混用）
- 设计系统文件（design-system.md、tokens.json、项目根 DESIGN.md）
- 框架配置（tailwind.config.js、theme.config.ts、components.json）
- 组件 / 页面文件中的硬编码值抽查

### 7.2 从参考设计提取

1. 用户提供参考设计链接或截图
2. 分析参考设计的：
   - 颜色系统（主色、辅助色、语义色）
   - 字体系统（标题、正文、代码字体）
   - 间距系统（基础单位、节奏）
   - 圆角系统
   - 阴影系统
   - 组件风格
3. 输出到 DESIGN.md

---

## 8. 访客意图模式详解

### 8.1 Persuade（说服型）

**适用场景：**
- 落地页（Landing Page）
- 营销页面
- 产品主页
- 注册/登录页

**设计特征：**
- 强视觉冲击
- 明确的 CTA
- 社会证明（客户评价、统计数据）
- 叙事节奏（问题→解决方案→行动）

### 8.2 Operate（操作型）

**适用场景：**
- 仪表板（Dashboard）
- 管理后台
- SaaS 应用
- 工具类应用

**设计特征：**
- 信息密度高
- 操作效率优先
- 清晰的导航结构
- 快速操作反馈

### 8.3 Read（阅读型）

**适用场景：**
- 文档站点
- 博客/文章
- 指南/教程
- FAQ 页面

**设计特征：**
- 阅读舒适性优先
- 清晰的排版层级
- 适当的行高和行长
- 减少视觉干扰

### 8.4 Experience（体验型）

**适用场景：**
- 作品集
- 画廊
- 品牌展示
- 互动体验

**设计特征：**
- 沉浸式体验
- 视觉叙事
- 创意表达
- 情感化设计

---

## 9. 输出规范

### 9.1 init 模式输出

创建以下文件：
- `PROJECT_ROOT/PRODUCT.md`
- `PROJECT_ROOT/DESIGN.md`

### 9.2 shape 模式输出

创建以下文件：
- `PROJECT_ROOT/DESIGN_BRIEF.md`

### 9.3 extract 模式输出

更新以下文件：
- `PROJECT_ROOT/DESIGN.md`（添加/更新设计Token）

### 9.4 read 模式输出

显示当前上下文摘要：
```markdown
## 当前设计上下文

### Product
[产品描述摘要]

### Design System
- 主色: [颜色值]
- 字体: [字体名称]
- 间距基数: [基础单位]

### Visitor Mode
[访客意图分类]

### Design Brief
[设计目标摘要]
```

---

## 10. 注意事项

- 设计上下文文件应纳入版本控制
- 每次设计任务开始前检查上下文是否存在
- 上下文与 Design Brief 保持同步更新
- 尊重用户明确指定的设计约束
- 使用 AskUserQuestion 进行必要的确认

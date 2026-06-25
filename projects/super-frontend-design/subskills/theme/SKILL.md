---
name: theme
version: 2.1.0
description: |
  主题与品牌系统模块。支持10个预设主题+自定义主题生成+品牌规范应用，输出Design Token系统。
  由 super-frontend-design 主入口路由调用。
  合并来源：brand-guidelines + theme-factory
  v1.1.0: 新增调研守卫 — 完整流程下检查品牌人格/视觉论文，独立调用时必须询问场景
  v2.0.0: 预设主题降级为参考·视觉论文优先推导·新增用户确认关口; v2.1.0: 企业设计系统参考目录集成
context: fork
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

### 0. 执行前置条件（调研守卫）

> ⚠️ **完整工作流模式下**：必须接收 research 的品牌人格/情绪板 和 creative 的视觉论文。Token 必须从这两者推导，禁止从预设直接复制。

| 条件 | 检查方式 | 不满足时的行为 |
|------|---------|---------------|
| 品牌人格存在 | 检查 `pass-data.yaml` 的 `brand-personality` 字段 | **拒绝从预设主题中选择**，向上游请求品牌人格 |
| 视觉论文存在 | 检查 `pass-data.yaml` 的 `visual-thesis` 字段 | Token 推导时标注「基于风格偏好推导，非视觉论文」 |
| 独立调用 | 非主工作流串联 | **必须询问最小化场景**（用途/行业/风格偏好），禁止从全局画像填充 |

### 全局画像禁令

- ❌ 不从用户全局画像提取「喜欢什么颜色」
- ❌ 不从历史记忆提取「上次选了什么主题」
- ❌ 不从 ontology 提取品牌偏好
- 每次主题选择必须基于本次任务的上下文

---

### 1. 概述

主题系统是 super-frontend-design 的核心子技能之一，负责为任何制品（网站、应用、文档、幻灯片、报告等）提供一致的视觉风格和品牌规范。

**定位：**
- 为所有前端制品提供统一的视觉语言
- 通过 Design Token 系统实现主题的可移植性和一致性
- 支持预设主题快速应用和自定义主题灵活生成

**合并来源：**
- `brand-guidelines`：品牌规范应用，特别是 Anthropic 品牌色彩和排版系统
- `theme-factory`：主题工厂，10 个预设主题和自定义主题生成能力

**核心能力：**
- 10 个精心设计的预设主题，覆盖常见设计风格
- Anthropic 官方品牌规范完整支持
- 自定义主题生成引擎
- 三层 Design Token 架构输出
- 暗色模式自动适配

**关键约束（反安全默认）：**
- **禁止从预设主题直接复制**：Token 必须从 creative 子技能的「视觉论文」推导，每个 Token 必须说明它如何体现了视觉论文的 5 个方向（配色、排版、布局、材质、动效）
- **禁止安全配色**：如果视觉论文指定"冷峻"，不能用默认的蓝色；如果指定"温暖"，不能用默认的橙色
- **字体必须体现品牌人格**：不能默认使用 Inter，必须从 `scripts/search.py fonts` 中选择与品牌人格匹配的字体
- **Token 命名必须语义化**：`--color-primary` 不够，应使用 `--color-brand-warm` 或 `--color-accent-rebel` 等体现品牌性格的命名

---

### 2. 预设主题参考（仅供参考 — 不可直接复制）

> ⚠️ **预设主题仅供概念参考，不直接使用。**
> 实际应用的 Token 必须从 creative 子技能的「视觉论文」的 5 个方向（配色/排版/布局/材质/动效）推导生成。
> 仅在以下情况可参考预设：(1) 用户明确说"给我推荐几个主题看看"；(2) creative 产出偏差需要验证方向。

#### 2.1 Ocean Depths - 专业沉稳的海洋主题

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#0A2647` | 主色调，深海蓝 |
| Secondary | `#144272` | 辅助色，中海蓝 |
| Accent | `#205295` | 强调色，亮海蓝 |
| Highlight | `#2C74B3` | 高亮色，天蓝 |
| Surface | `#F5F9FC` | 表面色，极浅蓝白 |
| Background | `#FFFFFF` | 背景色 |
| Text Primary | `#0A2647` | 主文本 |
| Text Secondary | `#5A7A9A` | 次要文本 |
| Success | `#2D8B55` | 成功色 |
| Warning | `#D4930D` | 警告色 |
| Error | `#C93C3C` | 错误色 |

**字体配对：**
- 标题字体：`Inter`（现代几何无衬线体）
- 正文字体：`Source Sans 3`（高可读性无衬线体）

**视觉特征：**
专业、沉稳、可信赖。适合企业级应用、金融平台、数据分析仪表板。色彩灵感来自深海层次，从深邃的藏蓝到明亮的天蓝，营造出层次分明的专业氛围。

---

#### 2.2 Sunset Boulevard - 温暖活力的日落色彩

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#E85D04` | 主色调，日落橙 |
| Secondary | `#F48C06` | 辅助色，金橙 |
| Accent | `#FAA307` | 强调色，琥珀 |
| Highlight | `#FFBA08` | 高亮色，明黄 |
| Surface | `#FFF8F0` | 表面色，暖白 |
| Background | `#FFFBF5` | 背景色 |
| Text Primary | `#3D1C00` | 主文本 |
| Text Secondary | `#8B5E3C` | 次要文本 |
| Success | `#5A9A3C` | 成功色 |
| Warning | `#E85D04` | 警告色 |
| Error | `#C93C3C` | 错误色 |

**字体配对：**
- 标题字体：`Playfair Display`（优雅衬线体）
- 正文字体：`Nunito`（圆润友好无衬线体）

**视觉特征：**
温暖、活力、富有感染力。适合创意机构、生活方式品牌、餐饮行业。色彩灵感来自洛杉矶日落大道的黄昏，从深橙到明黄，传递热情和能量。

---

#### 2.3 Forest Canopy - 自然踏实的大地色调

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#2D6A4F` | 主色调，森林绿 |
| Secondary | `#40916C` | 辅助色，苔藓绿 |
| Accent | `#52B788` | 强调色，翡翠绿 |
| Highlight | `#74C69D` | 高亮色，嫩叶绿 |
| Surface | `#F4F9F5` | 表面色，极浅绿白 |
| Background | `#FAFCFA` | 背景色 |
| Text Primary | `#1B4332` | 主文本 |
| Text Secondary | `#5A7D6A` | 次要文本 |
| Success | `#2D6A4F` | 成功色 |
| Warning | `#D4930D` | 警告色 |
| Error | `#C93C3C` | 错误色 |

**字体配对：**
- 标题字体：`Merriweather`（经典衬线体）
- 正文字体：`Open Sans`（清晰无衬线体）

**视觉特征：**
自然、踏实、有机。适合环保品牌、健康产业、教育平台。色彩灵感来自热带雨林的树冠层，从深绿到嫩绿，传递生命力和可持续性。

---

#### 2.4 Modern Minimalist - 干净当代的灰度

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#1A1A2E` | 主色调，深靛 |
| Secondary | `#16213E` | 辅助色，暗蓝 |
| Accent | `#0F3460` | 强调色，钢蓝 |
| Highlight | `#E94560` | 高亮色，珊瑚红 |
| Surface | `#F8F9FA` | 表面色 |
| Background | `#FFFFFF` | 背景色 |
| Text Primary | `#1A1A2E` | 主文本 |
| Text Secondary | `#6C757D` | 次要文本 |
| Success | `#28A745` | 成功色 |
| Warning | `#FFC107` | 警告色 |
| Error | `#DC3545` | 错误色 |

**字体配对：**
- 标题字体：`Space Grotesk`（几何现代无衬线体）
- 正文字体：`Inter`（高可读性无衬线体）

**视觉特征：**
干净、当代、克制。适合科技公司、SaaS 产品、设计工作室。以灰度为基础，仅用一个珊瑚红高亮色打破沉闷，体现"少即是多"的设计哲学。

---

#### 2.5 Golden Hour - 丰富温暖的秋季调色板

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#B08401` | 主色调，古金 |
| Secondary | `#CC9A2E` | 辅助色，琥珀金 |
| Accent | `#D4A843` | 强调色，蜂蜜金 |
| Highlight | `#E8C547` | 高亮色，明金 |
| Surface | `#FFFDF5` | 表面色，暖白 |
| Background | `#FFFEF8` | 背景色 |
| Text Primary | `#3D2E00` | 主文本 |
| Text Secondary | `#8B7A4C` | 次要文本 |
| Success | `#5A8A3C` | 成功色 |
| Warning | `#CC9A2E` | 警告色 |
| Error | `#B33A3A` | 错误色 |

**字体配对：**
- 标题字体：`Cormorant Garamond`（优雅衬线体）
- 正文字体：`Lora`（温暖衬线体）

**视觉特征：**
丰富、温暖、经典。适合奢侈品品牌、高端酒店、文化机构。色彩灵感来自秋季黄昏的金色光线，从古金到明金，传递优雅和永恒感。

---

#### 2.6 Arctic Frost - 清凉爽脆的冬季灵感主题

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#A2D2FF` | 主色调，冰蓝 |
| Secondary | `#BDE0FE` | 辅助色，浅冰蓝 |
| Accent | `#CAF0F8` | 强调色，极光蓝 |
| Highlight | `#E0FBFC` | 高亮色，霜白蓝 |
| Surface | `#F0F7FF` | 表面色 |
| Background | `#FAFCFF` | 背景色 |
| Text Primary | `#1B3A5C` | 主文本 |
| Text Secondary | `#6B8DAD` | 次要文本 |
| Success | `#4CAF82` | 成功色 |
| Warning | `#E8A838` | 警告色 |
| Error | `#D45454` | 错误色 |

**字体配对：**
- 标题字体：`Outfit`（现代几何无衬线体）
- 正文字体：`DM Sans`（清晰无衬线体）

**视觉特征：**
清爽、爽脆、纯净。适合健康科技、清洁能源、冬季运动品牌。色彩灵感来自北极的冰晶和霜花，从冰蓝到霜白，传递纯净和清新感。

---

#### 2.7 Desert Rose - 柔和精致的尘土色调

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#C9A9A6` | 主色调，沙漠玫瑰 |
| Secondary | `#D4BEB6` | 辅助色，浅玫瑰 |
| Accent | `#E6D2C3` | 强调色，沙色 |
| Highlight | `#F0E1D7` | 高亮色，奶白 |
| Surface | `#FAF5F2` | 表面色 |
| Background | `#FDF9F7` | 背景色 |
| Text Primary | `#4A3330` | 主文本 |
| Text Secondary | `#8B7068` | 次要文本 |
| Success | `#7DA87D` | 成功色 |
| Warning | `#C9A44C` | 警告色 |
| Error | `#B85C5C` | 错误色 |

**字体配对：**
- 标题字体：`Cormorant`（优雅衬线体）
- 正文字体：`Nunito Sans`（柔和无衬线体）

**视觉特征：**
柔和、精致、温暖。适合美容护肤、室内设计、婚礼策划。色彩灵感来自沙漠中绽放的玫瑰，从尘土粉到奶白，传递温柔和精致感。

---

#### 2.8 Tech Innovation - 大胆现代的科技美学

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#6C63FF` | 主色调，电紫 |
| Secondary | `#7B73FF` | 辅助色，亮紫 |
| Accent | `#00D9FF` | 强调色，霓虹蓝 |
| Highlight | `#00FFD1` | 高亮色，霓虹绿 |
| Surface | `#1A1A2E` | 表面色，深色 |
| Background | `#0D0D1A` | 背景色，极深 |
| Text Primary | `#E8E8FF` | 主文本 |
| Text Secondary | `#A0A0CC` | 次要文本 |
| Success | `#00FFD1` | 成功色 |
| Warning | `#FFD600` | 警告色 |
| Error | `#FF4D6A` | 错误色 |

**字体配对：**
- 标题字体：`JetBrains Mono`（等宽科技字体）
- 正文字体：`Space Grotesk`（几何现代无衬线体）

**视觉特征：**
大胆、现代、前卫。适合 AI/ML 产品、开发者工具、加密货币平台。深色背景搭配霓虹色高亮，营造赛博朋克式的未来感。这是唯一默认使用深色背景的预设主题。

---

#### 2.9 Botanical Garden - 清新有机的花园色彩

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#588157` | 主色调，叶绿 |
| Secondary | `#6B9E6A` | 辅助色，草绿 |
| Accent | `#A3B18A` | 强调色，橄榄绿 |
| Highlight | `#DAD7CD` | 高亮色，暖灰 |
| Surface | `#F5F8F2` | 表面色 |
| Background | `#FAFBF8` | 背景色 |
| Text Primary | `#2D4A2D` | 主文本 |
| Text Secondary | `#6B8B6B` | 次要文本 |
| Success | `#588157` | 成功色 |
| Warning | `#D4A03D` | 警告色 |
| Error | `#C45C5C` | 错误色 |

**字体配对：**
- 标题字体：`Fraunces`（有机衬线体）
- 正文字体：`Work Sans`（友好无衬线体）

**视觉特征：**
清新、有机、宁静。适合有机食品、瑜伽健身、心理健康平台。色彩灵感来自植物园的多样绿色，从深叶绿到橄榄绿，传递自然和宁静感。

---

#### 2.10 Midnight Galaxy - 戏剧性的宇宙深色调

**色彩调色板：**
| 角色 | 色值 | 用途 |
|------|------|------|
| Primary | `#1A0B2E` | 主色调，深空紫 |
| Secondary | `#2D1B69` | 辅助色，星云紫 |
| Accent | `#7B2FBE` | 强调色，亮紫 |
| Highlight | `#F0C27F` | 高亮色，星光金 |
| Surface | `#2A1A4A` | 表面色 |
| Background | `#0F0520` | 背景色 |
| Text Primary | `#E8D5F5` | 主文本 |
| Text Secondary | `#A88BC5` | 次要文本 |
| Success | `#4ADE80` | 成功色 |
| Warning | `#FBBF24` | 警告色 |
| Error | `#F87171` | 错误色 |

**字体配对：**
- 标题字体：`Syne`（大胆展示字体）
- 正文字体：`DM Sans`（清晰无衬线体）

**视觉特征：**
戏剧性、神秘、奢华。适合游戏平台、音乐流媒体、创意展示。色彩灵感来自银河系的深邃空间，从深紫到星光金，传递神秘和壮丽感。第二个默认使用深色背景的预设主题。

---

### 3. 品牌规范（Anthropic品牌）

当用户要求使用 Anthropic 品牌风格时，应用以下完整规范。

#### 3.1 主色系统

| 角色 | 色值 | 用途 |
|------|------|------|
| Dark | `#141413` | 主背景色、标题文本 |
| Light | `#faf9f5` | 浅色背景、表面色 |
| Mid Gray | `#b0aea5` | 次要文本、边框、分割线 |
| Light Gray | `#e8e6dc` | 卡片背景、悬停状态 |

**使用规则：**
- Dark 和 Light 作为基础对比色，确保文本可读性
- Mid Gray 用于辅助信息，不用于关键操作元素
- Light Gray 用于大面积非交互区域

#### 3.2 强调色系统

| 角色 | 色值 | 用途 |
|------|------|------|
| Orange | `#d97757` | 主要强调色，CTA按钮、重要链接 |
| Blue | `#6a9bcc` | 次要强调色，信息提示、辅助链接 |
| Green | `#788c5d` | 第三强调色，成功状态、确认操作 |

**使用规则：**
- Orange 是最高优先级的强调色，用于最重要的行动召唤
- Blue 用于信息性强调，不与 Orange 竞争注意力
- Green 专用于积极/成功语义
- 三个强调色不应同时出现在同一视觉层级

#### 3.3 排版系统

**字体选择：**
- 标题字体：`Poppins`（几何无衬线体，字重 600/700）
- 正文字体：`Lora`（衬线体，字重 400/500）

**字体应用规则：**
- 所有标题（h1-h6）使用 Poppins
- 所有正文段落使用 Lora
- 导航标签和按钮文案使用 Poppins 500
- 代码块使用等宽字体 `JetBrains Mono`
- 字体配对体现"现代几何 + 经典衬线"的对比美学

**智能字体应用：**
- 当制品类型为技术文档时，正文可切换为 `Inter`
- 当制品类型为创意展示时，标题可切换为 `Playfair Display`
- 当制品类型为数据仪表板时，正文可切换为 `Source Sans 3`
- 字体切换需保持品牌调性一致性

#### 3.4 形状和强调色应用

**形状规范：**
- 按钮圆角：`8px`（主要按钮）、`6px`（次要按钮）
- 卡片圆角：`12px`
- 输入框圆角：`6px`
- 模态框圆角：`16px`
- 头像圆角：`50%`（圆形）

**强调色应用规则：**
- Orange 强调色应用于：主 CTA 按钮背景、重要链接、进度条、选中状态
- Blue 强调色应用于：信息标签、辅助图标、工具提示、次要链接
- Green 强调色应用于：成功消息、确认按钮、完成状态
- 强调色不应用于大面积背景（仅限小面积点缀）

**阴影系统：**
- 微阴影：`0 1px 2px rgba(20, 20, 19, 0.05)`
- 轻阴影：`0 2px 8px rgba(20, 20, 19, 0.08)`
- 中阴影：`0 4px 16px rgba(20, 20, 19, 0.12)`
- 重阴影：`0 8px 32px rgba(20, 20, 19, 0.16)`

---

### 4. 自定义主题生成

#### 4.1 生成流程

当预设主题无法满足需求时，启动自定义主题生成：

1. **收集输入**：询问用户以下信息
   - 期望的设计风格/氛围（如：温暖、专业、活泼、极简）
   - 品牌色（如有，提供 hex 值）
   - 目标受众
   - 制品类型（网站、应用、文档等）
   - 是否需要暗色模式

2. **生成调色板**：基于用户输入，生成完整调色板
   - 从品牌色推导 Primary
   - 基于色彩理论推导 Secondary、Accent、Highlight
   - 确保所有色值满足 WCAG AA 对比度要求
   - 生成语义色（Success/Warning/Error）

3. **选择字体配对**：
   - 基于风格关键词匹配字体
   - 确保标题字体和正文字体形成对比
   - 优先选择 Google Fonts 可用字体
   - 限制在两种字体以内

4. **定义视觉特征**：
   - 圆角大小（0px 锐利 → 16px 柔和）
   - 阴影强度（无 → 重）
   - 间距密度（紧凑 → 宽松）

5. **审核展示**：向用户展示生成的主题，等待确认

#### 4.2 主题命名规范

自定义主题命名遵循以下规则：
- 使用英文，PascalCase 格式
- 名称应反映主题的视觉特征
- 格式：`[形容词] [名词]`
- 示例：`Coral Reef`、`Urban Steel`、`Vintage Paper`

#### 4.3 生成后审核

向用户展示以下信息，等待确认后才应用：
- 完整调色板（含色值和用途说明）
- 字体配对（含预览效果）
- 视觉特征描述
- 暗色模式版本（如适用）
- Design Token 预览

用户可以：
- 确认应用
- 请求调整特定色值
- 请求更换字体
- 请求重新生成

---

### 5. Design Token 输出规范

#### 5.1 三层 Token 架构

**第一层：原始 Token（Primitive Tokens）**
- 直接映射到具体色值/数值
- 命名不包含语义信息
- 示例：
```css
:root {
  /* 原始色彩 */
  --color-blue-500: #2C74B3;
  --color-blue-600: #205295;
  --color-blue-700: #144272;
  --color-blue-800: #0A2647;

  /* 原始间距 */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-8: 32px;
  --spacing-10: 40px;
  --spacing-12: 48px;

  /* 原始圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* 原始阴影 */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.16);

  /* 原始字号 */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;

  /* 原始字重 */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* 原始行高 */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

**第二层：语义 Token（Semantic Tokens）**
- 映射到原始 Token，包含语义信息
- 是组件 Token 的基础
- 示例：
```css
:root {
  /* 语义色彩 */
  --color-primary: var(--color-blue-800);
  --color-secondary: var(--color-blue-700);
  --color-accent: var(--color-blue-600);
  --color-highlight: var(--color-blue-500);
  --color-surface: #F5F9FC;
  --color-background: #FFFFFF;
  --color-text-primary: var(--color-blue-800);
  --color-text-secondary: #5A7A9A;
  --color-success: #2D8B55;
  --color-warning: #D4930D;
  --color-error: #C93C3C;

  /* 语义间距 */
  --spacing-inline-xs: var(--spacing-1);
  --spacing-inline-sm: var(--spacing-2);
  --spacing-inline-md: var(--spacing-3);
  --spacing-inline-lg: var(--spacing-4);
  --spacing-stack-xs: var(--spacing-2);
  --spacing-stack-sm: var(--spacing-4);
  --spacing-stack-md: var(--spacing-6);
  --spacing-stack-lg: var(--spacing-8);

  /* 语义排版 */
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Source Sans 3', sans-serif;
  --text-heading-1: var(--font-size-4xl) / var(--line-height-tight) var(--font-weight-bold);
  --text-heading-2: var(--font-size-3xl) / var(--line-height-tight) var(--font-weight-semibold);
  --text-heading-3: var(--font-size-2xl) / var(--line-height-tight) var(--font-weight-semibold);
  --text-body: var(--font-size-base) / var(--line-height-relaxed) var(--font-weight-normal);
  --text-body-sm: var(--font-size-sm) / var(--line-height-normal) var(--font-weight-normal);
  --text-caption: var(--font-size-xs) / var(--line-height-normal) var(--font-weight-medium);

  /* 语义边框 */
  --border-color-default: rgba(10, 38, 71, 0.15);
  --border-color-hover: rgba(10, 38, 71, 0.3);
  --border-color-focus: var(--color-accent);
  --border-radius-sm: var(--radius-sm);
  --border-radius-md: var(--radius-md);
  --border-radius-lg: var(--radius-lg);
}
```

**第三层：组件 Token（Component Tokens）**
- 映射到语义 Token，绑定到具体组件
- 示例：
```css
:root {
  /* 按钮组件 Token */
  --button-primary-bg: var(--color-primary);
  --button-primary-text: #FFFFFF;
  --button-primary-hover-bg: var(--color-secondary);
  --button-primary-padding: var(--spacing-inline-md) var(--spacing-inline-lg);
  --button-primary-radius: var(--border-radius-md);
  --button-primary-font: var(--font-heading);
  --button-primary-shadow: var(--shadow-sm);

  --button-secondary-bg: transparent;
  --button-secondary-text: var(--color-primary);
  --button-secondary-border: var(--border-color-default);
  --button-secondary-hover-border: var(--border-color-hover);

  /* 卡片组件 Token */
  --card-bg: var(--color-surface);
  --card-border: var(--border-color-default);
  --card-radius: var(--border-radius-lg);
  --card-padding: var(--spacing-6);
  --card-shadow: var(--shadow-sm);

  /* 输入框组件 Token */
  --input-bg: var(--color-background);
  --input-border: var(--border-color-default);
  --input-focus-border: var(--border-color-focus);
  --input-padding: var(--spacing-inline-sm) var(--spacing-inline-md);
  --input-radius: var(--border-radius-md);
  --input-text: var(--color-text-primary);
  --input-placeholder: var(--color-text-secondary);

  /* 导航组件 Token */
  --nav-bg: var(--color-background);
  --nav-item-text: var(--color-text-secondary);
  --nav-item-hover-text: var(--color-text-primary);
  --nav-item-active-text: var(--color-primary);
  --nav-item-padding: var(--spacing-inline-sm) var(--spacing-inline-md);

  /* 模态框组件 Token */
  --modal-bg: var(--color-background);
  --modal-overlay: rgba(0, 0, 0, 0.5);
  --modal-radius: var(--radius-xl);
  --modal-padding: var(--spacing-8);
  --modal-shadow: var(--shadow-lg);
}
```

#### 5.2 暗色模式适配

暗色模式通过覆盖语义 Token 实现，原始 Token 保持不变：

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* 覆盖语义色彩 */
    --color-primary: var(--color-blue-500);
    --color-secondary: var(--color-blue-600);
    --color-accent: var(--color-blue-400);
    --color-highlight: var(--color-blue-300);
    --color-surface: #0F1A2E;
    --color-background: #0A1222;
    --color-text-primary: #E8F0F8;
    --color-text-secondary: #8AA4C0;

    /* 覆盖语义边框 */
    --border-color-default: rgba(200, 220, 255, 0.12);
    --border-color-hover: rgba(200, 220, 255, 0.24);
  }
}

/* 手动暗色模式切换 */
[data-theme="dark"] {
  --color-primary: var(--color-blue-500);
  --color-secondary: var(--color-blue-600);
  --color-accent: var(--color-blue-400);
  --color-highlight: var(--color-blue-300);
  --color-surface: #0F1A2E;
  --color-background: #0A1222;
  --color-text-primary: #E8F0F8;
  --color-text-secondary: #8AA4C0;
  --border-color-default: rgba(200, 220, 255, 0.12);
  --border-color-hover: rgba(200, 220, 255, 0.24);
}
```

#### 5.3 语义化命名规范

Token 命名遵循以下层级结构：

```
--{类别}-{属性}-{变体}-{状态}
```

**类别（Category）：**
- `color`：色彩
- `spacing`：间距
- `font`：字体
- `text`：文本排版
- `border`：边框
- `radius`：圆角
- `shadow`：阴影
- `size`：尺寸

**属性（Property）：**
- 色彩：`primary`、`secondary`、`accent`、`highlight`、`surface`、`background`、`text`、`success`、`warning`、`error`
- 间距：`inline`（水平）、`stack`（垂直）
- 文本：`heading`、`body`、`caption`、`label`

**变体（Variant）：**
- 尺寸：`xs`、`sm`、`md`、`lg`、`xl`
- 层级：`1`、`2`、`3`

**状态（State）：**
- `hover`、`focus`、`active`、`disabled`

**完整示例：**
- `--color-primary`：主色
- `--color-text-secondary`：次要文本色
- `--spacing-inline-md`：中等水平间距
- `--text-heading-2`：二级标题排版
- `--button-primary-hover-bg`：主按钮悬停背景色
- `--input-focus-border`：输入框聚焦边框色

---

### 6. 主题应用流程

主题应用遵循严格的交互流程，确保用户始终拥有控制权：

#### 步骤 1：从视觉论文推导 Token（默认流程）

1. **读取视觉论文**：从 `pass-data.yaml` 读取 creative 子技能产出的 `visual-thesis`（含 5 个方向）
2. **Token 推导**：
   - 配色方向 → 主色/辅助色/强调色/中性色
   - 排版方向 → 标题字体/正文字体/字号阶乘
   - 布局方向 → 间距密度/网格系统/构图模式
   - 材质方向 → 圆角/阴影/边框/透明度
   - 动效方向 → 过渡时长/缓动函数类型
3. **每个 Token 必须标注推导来源**：如 `--color-primary: #XXXXXX（来自视觉论文·配色方向·冷峻蓝）`

#### 步骤 2（可选）：向用户展示主题参考

> 仅在用户明确询问"有哪些主题推荐"或 creative 产出偏差时触发。

当用户请求参考时，展示以下预设主题概览（仅名称+场景+关键词，不展示完整色值以保持视觉论文优先）：
```
🎨 可参考主题方向：

1. 🌊 Ocean Depths — 深海专业风（企业/金融/数据）
2. 🌅 Sunset Boulevard — 日落活力风（创意/生活/餐饮）
3. 🌲 Forest Canopy — 森林自然风（环保/健康/教育）
4. ⬜ Modern Minimalist — 极简当代风（科技/SaaS/设计）
5. ✨ Golden Hour — 黄金经典风（奢侈/酒店/文化）
6. ❄️ Arctic Frost — 冰雪纯净风（健康科技/清洁能源）
7. 🌸 Desert Rose — 沙漠柔和风（美容/设计/婚礼）
8. 🚀 Tech Innovation — 科技前卫风（AI/开发工具/加密）
9. 🌿 Botanical Garden — 植物清新风（有机/瑜伽/心理）
10. 🌌 Midnight Galaxy — 宇宙戏剧风（游戏/音乐/创意）
```

#### 步骤 3：从视觉论文推导（核心步骤）

- 明确询问用户选择哪个主题
- 如果用户描述了风格偏好但未指定主题，推荐最匹配的预设主题
- 如果用户需求超出预设范围，引导进入自定义主题生成流程

#### 步骤 4：展示 Design Token 并等待用户确认

> ⚠️ **v2.0.0 新增：这是用户唯一可以拦截和调整 Design Token 的关口。**
> theme 产出后、design 开始前，必须暂停并请求用户确认。

**向用户展示：**
```
🎨 基于您的品牌人格「{品牌人格}」和视觉论文推导的 Design Token：

| Token | 值 | 推导来源 |
|-------|-----|---------|
| --color-primary | {hex} | 视觉论文·配色方向·{关键词} |
| --color-accent | {hex} | {来源} |
| --font-display | {字体} | 视觉论文·排版方向·{关键词} |
| --font-body | {字体} | {来源} |
| --radius-base | {X}px | 视觉论文·材质方向·{关键词} |
| --space-base | {X}px | 视觉论文·布局方向·{关键词} |

暗色模式：{是/否} — {策略}

❓ 这个方案符合你的预期吗？
   - 「确认」→ 进入 design 阶段
   - 「调整配色」→ 请告诉我你想要的方向
   - 「调整字体」→ 请告诉我你偏好的字体风格
   - 「重新推导」→ 回到 creative 阶段重新评估
```

**用户确认后才继续：**
- 用户说"确认" / "可以" / "继续" → 写入 pass-data.yaml，进入 design
- 用户提出调整 → 修改对应 Token，重新展示，再次确认
- 用户说"重新推导" → 回 creative 阶段

#### 步骤 5：应用主题

- 将主题的 Design Token 注入到制品的 CSS 中
- 确保所有组件使用语义 Token 而非硬编码值
- 应用字体（通过 Google Fonts CDN 或本地字体）
- 应用暗色模式变体（如适用）

#### 步骤 6：输出 Design Token

- 生成完整的 Design Token CSS 文件
- 包含三层 Token（原始 → 语义 → 组件）
- 包含暗色模式适配
- 提供可复制粘贴的 CSS 代码块

---

### 7. 资源

#### 7.1 主题数据文件

主题数据存储在 `themes/` 目录下，每个主题一个 JSON 文件：

```
themes/
├── ocean-depths.json
├── sunset-boulevard.json
├── forest-canopy.json
├── modern-minimalist.json
├── golden-hour.json
├── arctic-frost.json
├── desert-rose.json
├── tech-innovation.json
├── botanical-garden.json
├── midnight-galaxy.json
└── anthropic-brand.json
```

每个 JSON 文件包含：
```json
{
  "name": "Ocean Depths",
  "slug": "ocean-depths",
  "description": "专业沉稳的海洋主题",
  "palette": { ... },
  "typography": { ... },
  "spacing": { ... },
  "borderRadius": { ... },
  "shadow": { ... },
  "darkMode": { ... }
}
```

#### 7.2 主题视觉展示

`theme-showcase.pdf` 包含所有主题的视觉预览，用于向用户展示主题效果。每个主题展示：
- 色彩调色板色块
- 字体配对预览
- 组件样式预览（按钮、卡片、输入框）
- 暗色模式预览

#### 7.3 字体资源

所有预设主题使用的字体均来自 Google Fonts：
- 加载方式：`<link>` 标签或 `@import`
- 回退字体栈：`system-ui, -apple-system, sans-serif`
- 字体显示策略：`font-display: swap`

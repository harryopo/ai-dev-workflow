# Macrostructures — 21种页面结构模板

> 本文件定义hallmark的21种命名宏观结构（macrostructure）。
> 每种结构是一个完整的页面"形状"，包含：标题位置 + 正文布局 + 分隔方式 + 按钮风格 + 图片处理 + 入场动画。
>
> **多样性规则（强制）**：同一项目中连续两个输出**不能共享同一个macrostructure**。
> **默认从01-10中选择**，Specimen仅在明确编辑部需求时使用。
>
> 使用方式：根据用户brief的domain关键词选择最匹配的3种（跨类别），让用户选或自动选最合适的。
> 选择后在CSS顶部添加stamp：`/* macrostructure: <name> · theme: <name> · genre: <genre> */`
>
> 参考：hallmark (Nutlope/hallmark, MIT)

---

## Domain → Macrostructure 路由表

| brief关键词 | 推荐的3种macrostructure（跨类别） |
|------------|--------------------------------|
| podcast/audio/music | **08·Photographic** · **09·Quote-Led** · **12·Letter** |
| shop/store/product | **11·Catalogue** · **08·Photographic** · **01·Bento Grid** |
| docs/CLI/API/SDK | **05·Workbench** · **02·Long Document** · **21·Component Playground** |
| platform/SaaS/B2B | **01·Bento Grid** · **05·Workbench** · **04·Stat-Led** |
| agency/portfolio | **18·Portfolio Grid** · **15·Split Studio** · **13·Index-First** |
| personal/one-pager | **02·Long Document** · **12·Letter** · **13·Index-First** |
| restaurant/food | **08·Photographic** · **02·Long Document** · **11·Catalogue** |
| fashion/beauty | **08·Photographic** · **11·Catalogue** · **03·Marquee Hero** |
| fintech/banking | **04·Stat-Led** · **05·Workbench** · **02·Long Document** |
| manifesto/campaign | **07·Manifesto** · **09·Quote-Led** · **04·Stat-Led** |
| editorial/foundry | **10·Specimen** · **02·Long Document** · **17·Type Specimen** |
| product launch/SaaS | **01·Bento Grid** · **05·Workbench** · **04·Stat-Led** |
| conference/event | **03·Marquee Hero** · **07·Manifesto** · **08·Photographic** |
| 无信号（fallback） | **01·Bento Grid** · **02·Long Document** · **07·Manifesto** |

> 注意：domain包含"developer"时，docs页→Workbench，marketing页→Bento Grid。若brief模糊，问一个问题再选。

---

## 01-10：非Specimen首选（覆盖80%需求）

---

### 01 · Bento Grid

不规则网格布局，每个模块大小不同，内容多样（feature/quote/image/stat）。视觉节奏来自尺寸变化而非卡片统一。

- **标题位置**：各模块内
- **正文**：多栏不对称
- **分隔**：负间距/留白
- **按钮**：各模块内
- **图片**：混合（部分模块有图，部分无图）
- **入场**：stagger fade-up

**适用**：多功能展示、SaaS产品页、特性汇总
**推荐主题**：Tally, Studio, Wayfare
**禁止**：所有卡片同一尺寸（必须混合1x1/2x1/1x2/2x2）

---

### 02 · Long Document

连续散文体，像备忘录、信件或日志。无营销结构。页面是"关于产品的文学"。

- **标题位置**：内联（段落中涌现）
- **正文**：单栏 65ch
- **分隔**：负间距
- **按钮**：无（或内联链接）
- **图片**：内联
- **入场**：无

**适用**：博客、公司博客、创始人日志、深度产品介绍
**推荐主题**：Tally, Garden, Newsprint
**禁止**：Hero区、CTA区块、分段分隔线

---

### 03 · Marquee Hero

英雄区就是页面本身。单一大胆陈述或视觉填满视口。无副标题、无折叠内CTA。折下后页面变为其他内容。

- **标题位置**：全视口英雄区
- **正文**：无/极少
- **分隔**：自然过渡
- **按钮**：无或隐藏
- **图片**：全出血
- **入场**：无/淡入

**适用**：品牌宣言、活动宣传、创意工作室
**推荐主题**：Brutal, Wayfare, Sport
**禁止**：折下过多内容（英雄区就是页面）

---

### 04 · Stat-Led

英雄区是一个巨大的数字——指标、计数、百分比。后续内容都围绕它展开。数据即叙事。

- **标题位置**：巨大数字
- **正文**：支撑性文字
- **分隔**：hairline rule
- **按钮**：Outlined
- **图片**：支撑性图表
- **入场**：Number Counter动画

**适用**：数据驱动产品、SaaS指标、金融工具
**推荐主题**：Almanac, Tally, Midnight
**禁止**：假数据/占位指标

---

### 05 · Workbench

产品截图作为主要内容。页面是对应用的引导式游览。少营销文案，多"这是你用它做什么"。

- **标题位置**：每屏顶部小标题
- **正文**：简短说明
- **分隔**：negative space
- **按钮**：Outlined
- **图片**：产品截图（frame内）
- **入场**：fade-up stagger

**适用**：产品演示、SaaS产品页、工具介绍
**推荐主题**：Tally, Studio, Almanac
**禁止**：纯文字hero（Workbench的核心是截图）

---

### 06 · Conversational FAQ

大胆问题 + 简短回答。页面读起来像与产品的诚实访谈。每Q/A可折叠。

- **标题位置**：每个问题作为section头
- **正文**：简短回答
- **分隔**：hairline rule
- **按钮**：无
- **图片**：无
- **入场**：无

**适用**：产品FAQ、帮助文档首页、答疑页
**推荐主题**：Tally, Newsprint, Midnight
**禁止**：超过15个问题

---

### 07 · Manifesto

宣言式大字。宣言能量。页面先告诉读者该相信什么，再告诉他们该买什么。常为政治海报美学。

- **标题位置**：覆盖图片/色块
- **正文**：全出血
- **分隔**：color block
- **按钮**：Oversized solid
- **图片**：全出血
- **入场**：Horizontal sweep

**适用**：激进品牌、活动页面、宣言页
**推荐主题**：Brutal, Manifesto, Sport
**禁止**：温和/中性语气

---

### 08 · Photographic

一张巨大图片主导每个fold。文字是小标注而非标题。设计说"看"而非"读"。

- **标题位置**：图片上的小标注
- **正文**：小文字
- **分隔**：image as divider
- **按钮**：Outlined 或无
- **图片**：全屏主导
- **入场**：fade-up

**适用**：摄影、视觉创意、时尚、旅行
**推荐主题**：Wayfare, Coral, NAJM
**禁止**：大量文字覆盖图片

---

### 09 · Quote-Led

英雄区是引言+出处。标题是借来的可信度，不是品牌自己的声音。页面以社交证明开篇。

- **标题位置**：引用文字作为hero
- **正文**：简短说明
- **分隔**：negative space
- **按钮**：Typographic-only
- **图片**：作者照片可选
- **入场**：fade-up

**适用**：社交证明页、客户案例、推荐展示
**推荐主题**：Atelier, Tally, Newsprint
**禁止**：虚构引用/虚假测试

---

### 10 · Specimen

左边距编号标签 + 巨大衬线字体 + 不对称栏 + 细线 + 排版CTA + 大量留白。编辑/字体铸造能量。

- **标题位置**：左边距编号
- **正文**：不对称span
- **分隔**：hairline rule
- **按钮**：Typographic-only
- **图片**：无
- **入场**：fade-up stagger

**适用**：**仅当用户明确要求编辑/印刷体风格时**
**推荐主题**：Specimen
**禁止**：在SaaS/开发者工具/电商页面上默认使用

---

## 11-21：高级/特殊场景

---

### 11 · Catalogue

均等网格，同一事物的变化——字体、配色、产品SKU。页面是库存的视觉索引。

- **标题位置**：顶部小标题
- **正文**：无
- **分隔**：grid gap
- **按钮**：无
- **图片**：产品/变体图
- **入场**：fade-up stagger

**适用**：商品目录、字体展示、配色方案
**推荐主题**：Riso, Almanac, Newsprint
**禁止**：网格尺寸不一致

---

### 12 · Letter

第一人称、手写、亲密。以问候语开篇（"Dear friend,"）。折叠内无按钮。读起来像创始人的私人笔记。

- **标题位置**：无标题（信件结构）
- **正文**：单栏 prose
- **分隔**：段落间距
- **按钮**：无（或末尾签名）
- **图片**：无
- **入场**：无

**适用**：创始人信、年度总结、私人通知
**推荐主题**：Atelier, Garden, Midnight
**禁止**：营销话术

---

### 13 · Index-First

页面本身就是一组链接。无英雄图、无叙事流。纯导航即设计。

- **标题位置**：链接列表
- **正文**：简短描述
- **分隔**：negative space
- **按钮**：无
- **图片**：无
- **入场**：无

**适用**：导航页、资源索引、作品集首页
**推荐主题**：Terminal, Midnight, Tally
**禁止**：超过50个链接

---

### 14 · Narrative Workflow

编号阶段讲述用户使用产品的时间线故事。每个section是一个阶段（1.0 → 2.0 → 3.0 → 4.0）。

- **标题位置**：编号阶段
- **正文**：每阶段说明
- **分隔**：numbered rule
- **按钮**：Outlined
- **图片**：阶段截图
- **入场**：fade-up + number tick

**适用**：流程展示、onboarding说明、步骤指引
**推荐主题**：Almanac, Midnight, Tally
**禁止**：超过6个阶段

---

### 15 · Split Studio

双联画。每个主要区块分割屏幕——文字在一边，证明在另一边。方向交替。

- **标题位置**：文字侧
- **正文**：文字侧
- **分隔**：image as divider
- **按钮**：Outlined
- **图片**：一侧
- **入场**：fade-up alternate

**适用**：作品集、产品展示、功能介绍
**推荐主题**：Studio, Tally, Wayfare
**禁止**：所有分割方向相同

---

### 16 · Feature Stack

粘性左窗格（标签/描述）+ 滚动同步右窗格（截图循环）。电影级节奏。

- **标题位置**：左窗格粘性
- **正文**：左窗格描述
- **分隔**：无（整体一个section）
- **按钮**：无
- **图片**：右侧切换
- **入场**：none（滚动驱动）

**适用**：产品特性深度展示、长特性页
**推荐主题**：Terminal, Midnight, Tally
**禁止**：粘性标题不随滚动更新

---

### 17 · Type Specimen

字体即设计。字体铸造厂首页或设计系统营销，自定义字体是品牌证明。

- **标题位置**：大字体展示
- **正文**：无或极少
- **分隔**：无
- **按钮**：无
- **图片**：无
- **入场**：无

**适用**：字体品牌、设计系统、印刷体展示
**推荐主题**：Specimen, Riso, Newsprint
**禁止**：超过3种字体（否则失去焦点）

---

### 18 · Portfolio Grid

可筛选项目卡片网格。工作室或设计师主页，作品即产品。

- **标题位置**：顶部小标题
- **正文**：每张卡片简短描述
- **分隔**：grid gap
- **按钮**：Filter按钮
- **图片**：项目缩略图
- **入场**：fade-up stagger

**适用**：设计师作品集、案例展示、项目列表
**推荐主题**：Studio, Tally, Almanac
**禁止**：卡片尺寸全部相同

---

### 19 · Map / Diagram

单一大型空间图组织页面——流程图、平面图、网络图、系统图。信息空间化而非线性。

- **标题位置**：图内标注
- **正文**：图内文字
- **分隔**：图连接线
- **按钮**：无
- **图片**：SVG/Canvas图
- **入场**：draw-in animation

**适用**：系统架构、流程图、网络拓扑、产品机制
**推荐主题**：Terminal, Midnight, Almanac
**禁止**：图过于复杂导致不可读

---

### 20 · Ecosystem Index

多种发现面——精选/最新/按分类/按人。平台价值在涌现和浏览，而非声明。

- **标题位置**：分类标题
- **正文**：无
- **分隔**：分类间距
- **按钮**：无
- **图片**：混合
- **入场**：fade-up stagger

**适用**：平台首页、内容聚合、社区入口
**推荐主题**：Almanac, Studio, Tally
**禁止**：单一分类主导（必须多发现面）

---

### 21 · Component Playground

代码+预览块是主要内容。每个块预览一个组件并展示如何copy-paste。

- **标题位置**：每个组件标题
- **正文**：简短说明
- **分隔**：hairline rule
- **按钮**：Copy代码按钮
- **图片**：组件预览
- **入场**：fade-up

**适用**：组件库文档、设计系统展示
**推荐主题**：Terminal, Midnight, Almanac
**禁止**：超过20个组件

---

## SaaS页面标准序列（非mandatory）

当macrostructure为 **Bento Grid · Stat-Led · Workbench · Marquee Hero** 且brief为B2B SaaS营销页时，按以下顺序组织内容：

1. **Hero** — macrostructure特定
2. **Social proof / Logo墙** — 6-8个monochrome客户logo
3. **Features** — 3-6个特性卡片
4. **Testimonials** — 2-4个引用卡片
5. **Pricing** — 2-3个价格档位
6. **FAQ** — 5-10个问题
7. **Final CTA strip** — 单按钮
8. **Footer** — 主题相关

**SaaS语音规则**：
- Pricing：必须显示真实价格，"联系销售"在各档位出现是AI标志
- Testimonials：必须包含被引者角色+公司，"Engineering Manager"是AI模板
- FAQ：像人回答，不写销售文档
- CTA strip：单按钮，非双按钮

---

## 选择规则

1. **阅读brief** — 注意强烈信号词
2. **检查代码库** — 搜索 `/* macrostructure: <name> */` stamp，排除已用的
3. **匹配brief能量** — 使用路由表选3种，选与上次输出最不同的
4. **代码前声明** — "Macrostructure: Bento Grid"，然后写代码
5. **若犹豫** — 提供跨类别的3种让用户选

**目标**：hallmark为不同brief建的页面应该是不同站点，不是同一模板的色块替换。

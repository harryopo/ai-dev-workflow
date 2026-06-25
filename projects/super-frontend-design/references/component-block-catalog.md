# 组件 Block 分类目录

> 基于 Aceternity UI 的 Block 分类体系 + 21st.dev 的组件市场结构
> design 阶段根据用户需求自动匹配对应 Block 类型生成设计卡

---

## Block 类型总览

| Block 类型 | 适用场景 | 参考来源 | 设计要点 |
|-----------|---------|---------|---------|
| **Hero Sections** | 首页首屏 | Aceternity UI (21+) / 21st.dev | 排版冲击 > 图片，禁止渐变背景 |
| **Feature Sections** | 产品特性展示 | Aceternity UI (18+) | Bento Grid 或交错布局，非均匀卡片 |
| **Bento Grids** | 特性聚合展示 | Aceternity UI (6+) / Magic UI | 大小卡片拼贴，视觉节奏不重复 |
| **CTA Sections** | 行动号召 | Aceternity UI (6+) / 21st.dev | 简洁直接，不超过 2 个 CTA 按钮 |
| **Pricing Cards** | 定价对比 | 21st.dev / shadcn | 最多 3-4 列，高亮推荐列 |
| **Contact Sections** | 联系/表单 | Aceternity UI (4+) | 最少字段，清晰的输入状态 |
| **Blog Sections** | 内容列表 | Aceternity UI (4+) | 图文比例，阅读流导向 |
| **Empty States** | 空数据/首次使用 | Aceternity UI (5+) | 引导 > 空白，有意义的 placeholder |
| **Background Effects** | 页面背景 | Aceternity UI (11+) / Magic UI | 噪点/着色器/波纹/线条，不抢内容 |
| **Shaders** | 着色器背景 | Aceternity UI (3+) | WebGL / Canvas，性能敏感 |
| **Data Tables** | 数据展示 | 21st.dev | 等宽数字、排序、分页、行 hover |
| **Navigation** | 导航栏/侧栏 | 21st.dev | 移动端汉堡菜单，桌面端 sidebar |
| **Forms** | 输入表单 | 21st.dev / shadcn | 验证状态、标签位置、提交反馈 |
| **Cards** | 内容卡片 | Aceternity UI (4+) / 21st.dev | 图片+文字+CTA，信息层级 |
| **Carousels** | 轮播/滑动 | Aceternity UI | Apple 风格极简，非传统 dot 轮播 |
| **Testimonials** | 用户评价墙 | Aceternity UI | 非对称编排，真人感 |
| **Logo Clouds** | 合作品牌展示 | Aceternity UI (6+) | 灰度 logo，不抢视觉 |
| **Footers** | 页脚 | 21st.dev / shadcn | 链接分组，版权行 |

---

## Block 类型 → 场景映射

| 用户描述 | 需要的 Block 类型 |
|---------|-----------------|
| "做个 SaaS 官网" | Hero + Features + Pricing + CTA + Footer |
| "后台管理系统" | Navigation + Data Tables + Forms + Cards |
| "App 落地页" | Hero + Features + Testimonials + CTA + Footer |
| "设计一个 Dashboard" | Navigation + Cards + Data Tables + Charts |
| "产品介绍页" | Hero + Features + Bento Grid + CTA |
| "博客首页" | Hero + Blog Sections + Cards + Footer |
| "联系我们页面" | Hero + Contact Sections + Footer |
| "404 / 空状态" | Empty States + CTA |

---

## 每个 Block 的设计卡格式

```
## Block: {Block 类型名称}

**设计决策来源**：Design Brief §{section} · 品牌人格「{type}」
**参考来源**：Aceternity UI · 21st.dev · {额外参考}

**AI 生成 Prompt**：
生成一个 {框架} {Block 类型} 组件：
- 配色: var(--color-*)
- 布局: {布局描述}
- 字体: var(--font-display) / var(--font-body)
- 动效: {动效描述}
- 禁止: {反 AI 规则}
```

---

## 全局参考索引

| 参考库 | 类型 | 访问方式 |
|--------|------|---------|
| Aceternity UI | React/Tailwind 组件 | https://ui.aceternity.com |
| 21st.dev | React/Tailwind/shadcn 组件市场 | https://21st.dev |
| Magic UI | React/Tailwind 动画组件 | https://magicui.design |
| shadcn/ui | React 基础组件 | https://ui.shadcn.com |
| Inspira UI | Vue/Nuxt 3D 动画组件 | https://inspira-ui.com |

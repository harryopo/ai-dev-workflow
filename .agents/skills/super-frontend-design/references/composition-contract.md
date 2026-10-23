# 构图契约（Composition Contract）— 把"页面形状"变成可校验的字段

> **为什么存在**：`references/macrostructures.md` 定义了 21 种页面形状，每种都写了标题位置 / 正文布局 / 分隔方式 / 按钮风格 / 图片处理 / 入场动画六个要素。但这些要素在 design 阶段**没有任何一处被强制落地**——选了 macrostructure，落地与否全凭模型自觉。
>
> 后果是可预见的：产出看起来"有结构"，但拆开看每个区块的标题锚点、列数、分隔手段都和所选 macrostructure 无关——本质还是默认的"标题居中 + 三列卡片 + 淡灰分隔"。**结构名对了，结构没落地**，和没选一样。
>
> 本文件把六要素转成**机器可判定的标记规范**，让"选了什么"和"做出来什么"能被对账。

---

## 一、构图契约字段（Composition Contract）

选定 macrostructure 后，必须在实现代码里落出这 6 项。每项一个标记注释，格式统一：

```css
/* composition: heading-anchor=各模块内 */
/* composition: body-columns=多栏不对称 */
/* composition: divider=负间距/留白 */
/* composition: imagery=混合（部分模块有图，部分无图） */
/* composition: entrance=stagger fade-up */
/* composition: focus-hierarchy=1 */
```

| 字段 | 含义 | 取值来源 |
|-----|------|---------|
| `heading-anchor` | 标题锚点——标题放在哪（各模块内 / 内联段落 / 全视口英雄区 / 巨大数字 / 每屏顶部 / 覆盖色块 / 图片上标注 / 引用即hero / 模块标题 / 画廊标题 / 巨型数字 / 索引标题 / 流程步骤名 / 分栏标题 / 特性条标题 / 字样标题 / 卡片标题 / 图例标题 / 生态名 / 组件名） | macrostructures.md「标题位置」 |
| `body-columns` | 正文列数与分布（单栏 65ch / 多栏不对称 / 全出血 / 简短说明 / 支撑性文字 / 巨型数字 / 简短回答 / …） | macrostructures.md「正文」 |
| `divider` | 分隔手段（负间距/留白 / hairline rule / color block / 自然过渡 / image as divider / 混合分隔 / 无） | macrostructures.md「分隔」 |
| `imagery` | 图片处理（混合 / 内联 / 全出血 / 产品截图 / 全屏主导 / 无 / 支撑性图表 / …） | macrostructures.md「图片」 |
| `entrance` | 入场动效形态（stagger fade-up / 无 / 淡入 / Number Counter / fade-up stagger / Horizontal sweep / …） | macrostructures.md「入场」 |
| `focus-hierarchy` | 视觉重心层级——**唯一需要自己判断的字段**（1 = 首屏焦点唯一；2 = 两级焦点；3 = 三级） | 见下节 |

> `button` 不单列为契约字段——按钮风格已由 theme 的 Token 体系与 design 的组件规范约束，重复约束收益低。

---

## 二、视觉重心规则（focus-hierarchy）

**定义**：用户视线在首屏落点上的**集中程度**。这是"页面看起来有设计"和"看起来是模板"的分水岭——模板的典型特征是每个区块权重相同，视线无处停留。

| 层级 | 含义 | 适用 macrostructure 倾向 |
|-----|------|----------------------|
| `1` | 首屏只有一个焦点，视线第一落点唯一 | Marquee Hero / Stat-Led / Photographic / Manifesto / Type Specimen |
| `2` | 两级焦点：主焦点 + 次焦点区 | Bento Grid / Workbench / Split Studio / Feature Stack / Narrative Workflow |
| `3` | 三级焦点：主 + 次 + 辅助 | Catalogue / Ecosystem Index / Portfolio Grid / Component Playground |

**判定规则**：

1. **层级由 macrostructure 决定，不由内容决定**——选 Stat-Led 就必须让巨型数字成为唯一焦点，不能因为内容多就塞三处大数字
2. **同屏同级焦点 ≤ 1**——首屏不允许出现两个同等视觉权重的元素（比如两个同样大小的巨号标题）
3. **焦点必须落在契约声明的锚点上**——`focus-hierarchy` 声明为 1 时，视线第一落点必须与 `heading-anchor` 指定的位置一致
4. **B 端例外**：Operate 场景（后台/内部工具）默认 `3`——后台要的是信息密度与效率，均衡布局是优点不是缺陷。但仍需声明层级值，不能省略

---

## 三、落地规范

### 3.1 标记位置

**载体随项目形态，不强制 CSS**——Tailwind v4、单文件 HTML、无独立 CSS 文件的项目里样式不在 `.css` 里，要求"写 CSS 顶部"等于要求这些项目必然违规。门禁 `composition_check.py` 两种载体都认：

| 项目形态 | 载体 | 写法 |
|---------|------|------|
| 有独立 CSS 文件 | CSS 顶部，与 stamp 同区 | `/* composition: xxx=... */` |
| Tailwind / 单文件 HTML | HTML 注释 | `<!-- composition: xxx=... -->` |
| Vue SFC 等双载体 | 可混用 | 同一要素只声明一次（重复取首见） |

```css
/* macrostructure: 01·Bento Grid · theme: Tally · genre: SaaS */
/* composition: heading-anchor=各模块内 */
/* composition: body-columns=多栏不对称 */
/* composition: divider=负间距/留白 */
/* composition: imagery=混合（部分模块有图，部分无图） */
/* composition: entrance=stagger fade-up */
/* composition: focus-hierarchy=2 */
```

HTML 载体的等价写法：

```html
<!-- macrostructure: 01·Bento Grid · theme: Tally -->
<!-- composition: heading-anchor=各模块内 -->
<!-- composition: body-columns=多栏不对称 -->
<!-- composition: divider=负间距/留白 -->
<!-- composition: imagery=混合 -->
<!-- composition: entrance=stagger fade-up -->
<!-- composition: focus-hierarchy=2 -->
```

> 与签名机制（v2.11.0）的载体口径保持一致：`signature_check.py` 同样同时支持 `/* */` 与 `<!-- -->`。

### 3.2 标记 ≠ 声明就完事

标记只是**对账锚点**，不是通行证。真正的落地是代码里确实按契约做了：

| 字段 | 落地判据（代码里看得见的证据） |
|-----|------------------------------|
| `heading-anchor` | 标题元素的实际位置符合声明（模块内 / 段落内 / 全视口 / 数字内…），不是全部居中堆叠 |
| `body-columns` | 实际列数或排布符合声明；`单栏 65ch` 必须有 `max-width: 65ch` 量级约束 |
| `divider` | 实际用到了声明的分隔手段；`hairline rule` 必须有边框线，`负间距/留白` 必须有负 margin 或大间距 |
| `imagery` | 图片处理方式符合声明；`无` 则确实没有图片位 |
| `entrance` | 实际有对应的入场动效或明确无动效 |
| `focus-hierarchy` | 首屏视觉权重符合声明层级；同级焦点 ≤ 1 |

### 3.3 与既有机制的关系

| 机制 | 管什么 | 与构图契约的关系 |
|-----|-------|----------------|
| `macrostructures.md` | 提供 21 种可选形状 | 构图契约是它的**可校验投影**——从它选，然后按它落地 |
| theme Token | 间距/圆角/字号的**量值** | 契约管**结构关系**，Token 管**具体数值**，不重叠 |
| 签名机制（v2.11.0） | "这是哪个产品"（肯定式） | 签名管**辨识度**，契约管**构图质量**，两条正交 |
| slop-test V19 | stamp 缺失检测 | V19 只查 macrostructure stamp 在不在；契约查六要素在不在、落地对不对 |

---

## 四、常见不落地情形（自查）

| 现象 | 判据 | 修法 |
|-----|------|------|
| 选了 Bento Grid，标题全在卡片顶部居中 | `heading-anchor` 声明"各模块内"但标题居中堆叠 | 改标题锚点位置或改声明 |
| 声明"负间距/留白"分隔，实际全是 `border-bottom: 1px solid` | `divider` 与实际不符 | 二选一：改成真实负间距，或改声明 |
| 声明 `focus-hierarchy=1`，首屏有两个同样大的巨号 | 同级焦点 > 1 | 压次焦点到 `2` 级或移出首屏 |
| 六要素全标了，但代码和默认模板无差别 | 标记与实现脱节 | 按 3.2 逐项对照落地，标记不是护身符 |
| macrostructure 换了，构图没换 | 连续两个页面结构雷同 | 换 macrostructure 必须连构图一起换 |

---

## 五、机器校验

```bash
python scripts/composition_check.py <实现代码目录>
```

校验内容：
- 六个 `composition:` 字段是否齐全（缺任一 → FAIL）
- `focus-hierarchy` 取值是否合法（1/2/3）
- 顶层 macrostructure stamp 与 `composition:` 标记是否在同一文件
- `--require-macrostructure` 可核对选定的 macrostructure 与 stamp 是否一致

**设计契约**：零要素 = 选了什么没做（FAIL）；六项齐全但声明与实现脱节 = 脚本查不出，只能靠 review #13 人工核对——**脚本保证"声明了"，review 保证"做对了"**，两者不可互相替代。

# Slop Test — 56条反AI味检查清单

> 本文件定义hallmark的56条slop-test检查规则。
> 在输出代码前必须完整运行此清单。所有答案必须为"无"（无违规）。
> 任何"是"=必须修复后重新输出。
>
> 参考：hallmark (Nutlope/hallmark, MIT) · Together AI

---

## Pre-emit 自评（6轴，输出前1-5分）

| # | 轴 | 评分标准 | 必须≥3 |
|:---:|------|---------|:---:|
| A | **Philosophy** | 页面有没有明确立场？还是只是一个布局？ | ✅ |
| B | **Hierarchy** | 2秒内能否分辨主次？还是所有元素权重相同？ | ✅ |
| C | **Execution** | 细节（规则线重、accent占比、text-wrap、focus rings、对比度）是否到位？ | ✅ |
| D | **Specificity** | 是否像专门为这个brief设计的？还是像"任何人的通用页面"？ | ✅ |
| E | **Restraint** | 是否删掉了所有不贡献价值的内容？ | ✅ |
| F | **Variety** | 是否与上一个输出的结构指纹不同？ | ✅ |

**输出格式**：在CSS顶部添加stamp：
```css
/* super-frontend-design · pre-emit: A4 B5 C4 D3 E5 F4 */
/* ↑ D=3触发本轮修订 */
```

---

## 1-6 · 视觉检查

### V1. 禁用字体检测
**检查**：Display字体是否为 Inter, Roboto, Open Sans, Poppins, Lato 或系统默认？
**修复**：选择 distinctive display face + refined body face 配对

### V2. 渐变检测
**检查**：是否有任何 purple→blue / cyan→magenta / blue→purple→pink 渐变？包括 `background-clip: text` 渐变文字？
**修复**：单一anchor hue。Hero区禁止渐变背景。仅允许黑→灰/同色系深浅/金属质感

### V3. 等宽3列卡片检测
**检查**：是否有3个等宽列，每列有icon-above-heading-above-two-line-body？
**修复**：打破网格。混合列宽。去除icon或内联

### V4. 卡片嵌套检测
**检查**：是否有card inside card？或card inside card inside micro-card？
**修复**：选一个容器层，通常外层是错的

### V5. 侧边条纹卡片检测（hallmark新增）
**检查**：是否有4-6px彩色左边框/右边框（purple/green）？
**修复**：hairline border全围绕 或 小accent square在heading旁

### V6. 居中英雄检测
**检查**：Hero是否为 `min-height: 100vh` + 全居中（标题/副标题/CTA都在同一垂直中轴）？
**修复**：偏置布局。宽左边距+窄右边距。最多2个居中元素

---

## 7-8 · 结构检查

### V7. 结构重复检测
**检查**：页面是否复用不应复用的结构（通用AI模板 或 同一macrostructure）？
**修复**：查找CSS stamp `/* macrostructure: <name> */`，选择不同结构

### V8. 段落节奏单一检测
**检查**：段落是否仅靠等宽空白分隔，无rule/ornament/color shift？
**修复**：混合分隔方式（hairline + negative space + color block）

---

## 9-18 · 微交互检查

### V9. transition-all检测
**检查**：是否有任何地方使用 `transition: all`？
**修复**：指定具体属性（`transition: opacity 150ms, transform 150ms`）

### V10. hover:scale-105检测
**检查**：是否多个不相关元素都应用了统一的 `hover:scale-105`？
**修复**：差异化——按钮scale(1.02)，卡片translateY(-2px)

### V11. bounce/elastic easing检测
**检查**：按钮/弹窗/hover是否使用 `cubic-bezier(0.34, 1.56, ...)` 等overshoot缓动？
**修复**：Exponential ease-out。Overshoot仅用于物理交互

### V12. 多重hover effect检测
**检查**：是否有任何元素同时有>1个hover effect（translate + scale + shadow + color + rotate）？
**修复**：每个元素最多1个hover effect

### V13. width/height/margin/padding动画检测
**检查**：是否有任何元素动画 `width`, `height`, `top`, `left`, `margin`, `padding`？
**修复**：只用 `transform` 和 `opacity`

### V14. Focus ring渐入检测
**检查**：focus ring是否通过opacity fade-in出现？
**修复**：focus ring必须instant出现（`transition: none` on outline）

### V15. 成功Toast检测
**检查**：是否在用户已可见效果的action上弹出成功toast？
**修复**：Silent success。Toast仅用于failure或invisible effect

### V16. Tooltip延迟检测
**检查**：tooltip hover-delay和focus-delay是否相等？
**修复**：Hover延迟800-1000ms，focus延迟0ms

### V17. Carousel pause检测
**检查**：自动旋转内容（carousel/banner/stats）是否缺少pause-on-hover-and-focus？
**修复**：WCAG 2.2.2合规

### V18. 占位名检测
**检查**：是否有任何placeholder名"Jane Doe/John Smith"或startup cliché（Acme/Nexus/Seamless/Unleash）？
**修复**：真实名或合理占位符

---

## 19-20 · 多样性检查

### V19. Macrostructure stamp缺失检测
**检查**：CSS顶部是否缺少 `/* macrostructure: <name> · ... */` stamp？
**修复**：必须添加stamp

### V20. Specimen fall-through检测
**检查**：是否在未明确要求editorial/foundry/specimen energy时默认使用Specimen结构？
**修复**：Specimen仅在brief明确时选用。默认从01-10中选

---

## 21-26 · 实现检查

### V21. 零饱和度中性色检测
**检查**：是否有任何neutral/surface颜色 `oklch(... 0 ...)`（零饱和度）？
**修复**：tint所有neutral toward anchor hue，最低chroma 0.005
**例外**：modern-minimal允许零饱和度neutral（Stripe/ElevenLabs风格）

### V22. Accent占比>5%检测
**检查**：accent颜色是否覆盖>5%的单个视口区域？
**修复**：accent为强调，非填充
**例外**：atmospheric允许accent-tinted radial blooms覆盖≤20%

### V23. 任意间距值检测
**检查**：是否有任何padding/gap/margin不是4px倍数（如17px, 23px）？
**修复**：所有间距使用命名scale（4px倍数）

### V24. Prose宽度检测
**检查**：任何prose容器的max-width是否超出45-75ch范围？
**修复**：<45ch太碎，>75ch难读

### V25. 交互状态不足检测
**检查**：是否有任何交互元素缺少 `:focus-visible`, `:active`, 或 `:disabled` 样式？
**修复**：至少需5种状态（default/hover/focus-visible/active/disabled）

### V26. prefers-reduced-motion检测
**检查**：是否有任何transform/animation keyframe没有 `prefers-reduced-motion` fallback？
**修复**：每个动效必须有降级方案

---

## 27-30 · Hero检查

### V27. LCP杀手检测
**检查**：是否有demo video：autoplay with sound / 无poster / 无fetchpriority="high" / LCP元素用loading="lazy"？
**修复**：video必须 `autoplay muted loop playsinline`，LCP用 `fetchpriority="high"` + `preload="metadata"`

### V28. Aurora blob检测
**检查**：是否有abstract background >1个accent color / >5% footprint / animating mesh-gradient？
**修复**：Solid surface或subtle two-stop gradient + SVG noise <0.1 opacity
**例外**：atmospheric允许≤2个warm-toned radial blooms覆盖≤20-30%

### V29. Icon混合检测
**检查**：页面是否混合2个以上icon库（Material+Heroicons+Lucide）？或使用emoji（✨🚀⚡🔥🎯✅）作为feature/card图标？
**修复**：每个项目选一个icon library（Lucide默认/SaaS/Phosphor/Heavy/Heroicons/Tailwind/shadcn）

### V30. Lottie默认检测
**检查**：是否有illustration默认使用Lottie库而非hand-built SVG或纯CSS？
**修复**：Lottie为最后选项，非默认

---

## 31-32 · 多样性交叉检查

### V31. 变体旋钮未差异化检测
**检查**：若使用与上次相同的archetype，是否选择了至少一个不同的variation knob？
**修复**：在stamp中声明knob deltas

### V32. 装饰性SVG无障碍检测
**检查**：是否有任何visual-only `<svg>`, custom-art `<div>`, `<canvas>`, decorative figure缺少`aria-label`或`aria-hidden="true"`？
**修复**：CSS art和SVG illustration必须有accessible name或explicit hide

---

## 33-36 · 布局安全检测

### V33. 横向滚动检测
**检查**：页面在320-1920px任何viewport是否有横向滚动？
**修复**：`overflow-x: clip` on both html AND body（用clip不用hidden）

### V34. 装饰线位置检测
**检查**：highlighter/em band/accent stroke/underline的视觉位置是否确认？
**修复**：highlighter必须在x-height后（38%-92%），不在baseline。Underline 1-2px，offset 1-2px

### V35. 交互栏垂直居中检测
**检查**：nav/toolbar/command bar/hero CTA row/footer link strip是否显式`align-items: center`？
**修复**：flex row混合height不同元素时必须声明`align-items: center` + `line-height: 1`

### V36. 响应式断点检测
**检查**：页面是否在320/375/414/768px四断点都正常渲染？
**修复**：无横向滚动 + 无两行可点击文字 + image grid用`minmax(0,1fr)`

---

## 37-39 · 字体纪律检测

### V37. 超过3种字体检测
**检查**：页面是否使用>3种distinct font-family？
**修复**：display + body + 最多1个outlier。Mono在非代码上下文中也算一种

### V38. Outlier face超限检测
**检查**：outlier face是否在>2个slot使用？
**修复**：outlier是register不是third body font。wordmark + hero stat是canonical pair

### V39. 斜体标题检测（hallmark新增 · 顶级AI标志）
**检查**：是否有任何heading/display type使用`font-style: italic`？
**修复**：标题必须roman（`font-style: normal`）。强调用weight/accent color/drawn underline
**注意**：italic仅可用于body copy内的强调

---

## 40 · 输入状态检测

### V40. 输入状态5项检测
**检查**：input/textarea/select是否处理所有状态？任一失败：
- Border-width在state间变化
- Focus ring用border而非outline
- Input高度≠adjacent button高度
- Helper-text slot空时折叠
- Disabled仅用opacity
**修复**：border-width恒定1px；focus ring用outline；同高44px floor；min-height:1lh；disabled需3通道

---

## 41-42 · 对比度检测

### V41. 对比度阈值检测
**检查**：是否有任何text/icon/focus-visible ring失败阈值？
**修复**：Body text≥4.5:1 (WCAG) / Lc≥60 (APCA)。Large text/icons/focus rings≥3:1 (WCAG) / Lc≥45

### V42. 最常见对比失败检测
**检查**：任一：
- Button text≈button fill（lightness差<5% AND chroma差<0.05）
- `--color-accent-ink`缺失或未用于accent fill上的文字
- Dark-section ink-on-ink（dark背景下的文字未翻转为浅色）
**修复**：每个dark section必须同时设置`color: <light>`

---

## 43-45 · 导航/页脚/英雄结构检测

### V43. AI导航检测
**检查**：是否使用标准化AI导航（wordmark左/4-5个inline link居中或右组/CTA右/full width/sticky/hairline border）？
**修复**：选择genre-matching nav archetype（Floating pill/Newspaper masthead/Brutal slab/Terminal command/Edge-aligned minimal）

### V44. AI页脚检测
**检查**：是否使用标准化AI页脚（4列links/social icon row/copyright line/hairline top-border/neutral grey）？
**修复**：选择genre-matching footer archetype（Mast-headed/Inline single line/Dense colophon/Statement/Letter close/Newsletter-first/Marquee scroll）

### V45. 假指标检测
**检查**：是否有任何stat-led layout/comparison row/proof bar携带用户未提供的数字？
**修复**：用`—`+灰色块（"metric to confirm"）或ask用户真实数字

---

## 46-49 · 实现质量

### V46. 重绘chrome检测
**检查**：是否有fake browser bars（URL pill+traffic-light dots）/ fake phone frames / fake code-block windows（mock title bar+dots wrapping `<pre>`）/ fake IDE chrome？
**修复**：用真实截图+`<figure>`+hairline border，或省略chrome

### V47. Token improvisation检测
**检查**：是否在代码中inline使用OKLCH/hex/rgb()值而非通过CSS变量`var(--color-*)`引用？
**修复**：所有颜色/font-family必须通过named token引用

### V48. 两行可点击文字检测
**检查**：是否有任何button/primary nav link/footer link/breadcrumb/CTA在移动端显示>1行可点击文字？
**修复**：确保所有可点击元素在320px宽度内不超过1行

### V49. Image grid 1fr检测
**检查**：是否有image-bearing grid track使用bare `1fr`而非`minmax(0, 1fr)`？
**修复**：image-bearing tracks必须用`minmax(0, 1fr)`防止overflow

---

## 50-56 · 特殊规则

### V50. Emoji作为feature icon检测
**检查**：是否使用generic emoji（✨🚀⚡🔥🎯✅）作为feature card/value prop/step/pricing tier的主要图标？
**修复**：选一个icon library或drop icon lead with type

### V51. Eyebrow on every section检测
**检查**：是否每个section都以uppercase mono-cap eyebrow开头（`01 / EXAMPLES`, `02 / WHAT'S INSIDE`）？
**修复**：默认**零eyebrows**。仅在以下情况使用：用户明确要求章节编号 OR macrostructure是Long Document/Manifesto/Catalogue numbered且内容确实有序
**硬禁令**：tag-left/header-right两列section head禁止

### V52. Shadow-glow on dark检测
**检查**：dark background上的card是否有colored halo box-shadow？
**修复**：dark surface用elevation via lightness（brighter surface=higher），不shadow

### V53. Sound-on autoplay检测
**检查**：是否有hero video autoplay with sound（无muted）？
**修复**：video必须`autoplay muted loop playsinline`

### V54. Lazy-loaded LCP检测
**检查**：是否有hero image/video使用`loading="lazy"`？
**修复**：LCP元素必须`fetchpriority="high"` + `preload="metadata"`

### V55. Animate-on-scroll everywhere检测
**检查**：是否每个section都在进入视口时fade in？
**修复**：选一个orchestrated entrance。让其余"只是在那里"

### V56. Glassmorphism without purpose检测
**检查**：是否到处使用frosted-glass panels（通常layered over gradient）？
**修复**：Glassmorphism仅当communicate depth时可用（overlay over content）。不得作为装饰

---

## Slop Test 评分标准

| 通过数 | 评分 | 动作 |
|:---:|:---:|------|
| 56/56 | 100 | ✅ 输出 |
| 51-54/56（90-96%） | 90-96 | 🟡 小幅修订后输出 |
| 45-50/56（80-89%） | 80-89 | 🟡 明显问题，必须修复 |
| <45/56（<80%） | <80 | 🔴 大量问题，必须重写 |

**输出格式**：
```
## Slop Test 检查报告

| # | 状态 | 规则 | 位置 | 建议 |
|:---:|:---:|------|------|------|
| V5 | ✅ PASS | 侧边条纹卡片 | — | — |
| V20 | ❌ FAIL | Specimen fall-through | Hero.jsx:1 | brief无editorial信号，改用Bento Grid |
| V39 | ❌ FAIL | 斜体标题 | H1.jsx:5 | 改为roman，强调用weight |
| ... | ... | ... | ... | ... |

评分: 52/56 (93%)
Pre-emit: A4 B5 C4 D3 E5 F4
```

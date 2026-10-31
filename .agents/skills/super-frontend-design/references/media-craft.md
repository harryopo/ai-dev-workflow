# Media Craft — 视频/图片/图标嵌入手法（精美与性能并重）

> 定位：落地页与产品页里**媒体元素**的取舍与实现手法——背景视频、图片处理、性能纪律、AI 配图、图标体系、lightbox。
> 配套：图片优化硬规则已有（ux-guidelines UX-036 / premium#15 首屏禁 lazy / render_probe 对比度量测）——本文件补"手法与品味"，不重复硬规则。
> 纪律：媒体是**信息与情绪的载体**，不是装饰——每个媒体元素回答"它帮用户理解/感受了什么"，答不出就不放。

---

## 1. 背景视频（hero 级）

**什么时候用**：产品本身就是动态的（地图/3D/工作流演示）——视频替用户回答"它是干什么的"。纯氛围视频（海浪/粒子）= 装饰性媒体，默认不放。

**实现规范**：

```html
<video autoplay muted loop playsinline
       poster="hero-poster.avif"
       preload="metadata"
       aria-hidden="true">
  <source src="hero.webm" type="video/webm">
  <source src="hero.mp4" type="video/mp4">
</video>
```

- **10-30 秒循环、静音（muted）、playsinline**（iOS 自动播放三件套）；无音轨是默认，有音轨必须给控件
- **poster 必给**：视频首帧前的加载占位（AVIF/WebP），同时是低网/降级方案的静态版
- **文字对比度靠 CSS overlay 层**：渐变遮罩/半透明底写在 CSS（`background: linear-gradient(...)` 叠在视频上），不烤进视频——可调、可随主题切
- **性能预算**：视频 ≤3MB（首屏 ≤1.5MB 更好）；`preload="metadata"`；移动端（`pointer: coarse` 或窄视口）降级为 poster 静图
- **降级三连**：`prefers-reduced-motion` → 暂停/换静图；`document.hidden` → 自动暂停；播放失败 → poster 仍是完整可读页面

## 2. 图片处理手法库（给"用什么样的图、怎么放"）

| 手法 | 做法 | 什么时候用 | 反模式 |
|------|------|-----------|--------|
| **品牌色 duotone（双色调）** | 图片去色后叠品牌色（CSS `filter: grayscale(1)` + mix-blend / SVG filter，或生成时就做） | 人物/场景图与品牌色打架时统一质感 | 全站所有图都 duotone——产品截图必须保真色 |
| **grain 噪点** | 半透明噪点层（SVG feTurbulence / PNG 叠加，opacity 3-6%） | 消除渐变带、增加"印刷感" | 高噪点盖住内容；噪点动起来 |
| **渐变遮罩** | 媒体上叠品牌色→透明的 CSS 渐变，保证文字对比度 | 文字压图的 hero | 遮罩过重图变"色块"；对比度不达标（render_probe 会拦） |
| **混合模式构图** | `mix-blend-mode: multiply/screen/luminosity` 让图与底色互融 | 品牌色底 + 去底产品图 | 混完看不清主体 |
| **圆角遮罩构图** | 图片裁进品牌圆角/异形 mask（`clip-path`/`mask-image`） | 打破"全幅矩形图"的模板感 | 异形到看不出图是什么 |
| **截图精致化** | 浏览器截图套样机（设备框/浏览器 chrome/柔和投影+细边线） | B 端产品 hero 的标准解 | 生截图直贴（毛边、错分辨率） |

- **配图风格一致性**：全站插画风格/摄影色调一个体系（插画全部 unDraw 风或全部自定，不混用）；这是"图与图之间的一致性"，与 Token 体系同级重要
- **禁占位图上生产**：unsplash/placehold 等占位 CDN 是 slop 门禁规则（placeholder-cdn）——正式产物里要么真实素材、要么 AI 生图、要么无图

## 3. 性能纪律（媒体是 LCP 大户）

- **格式**：AVIF 优先（含 WebP 兜底）：`<picture><source type="image/avif">…`
- **响应式**：`srcset` + `sizes` 必配（hero 至少 3 档宽度）；移动端给更轻的裁切版（art direction 用 `<source media=>`）
- **加载**：仅 LCP 图 `fetchpriority="high"` + `loading="eager"`；其余全部 `loading="lazy"`；首屏禁 lazy（premium#15）；`preload` 每页最多一个（给 LCP 媒体）
- **CLS 防抖**：`<img>` 必写 `width`/`height`（或 CSS aspect-ratio）——媒体加载前就占好位
- **视频**：见 §1；`preload` 不给 `auto`
- **AI 生图同样受门禁**：生成的图也要过对比度（render_probe）与整体风格一致性检查

## 4. AI 配图通道（seedream，可选——需 ARK_API_KEY）

design 阶段产出落地页时，可用本机 byted-seedream-image-generate skill **直接生成 hero 配图/产品示意图/插画**，替代"找图"：

```bash
python "$SEEDREAM/scripts/seedream_image_generate.py" \
  -p "<提示词>" -s 1440x720 --version 4.0 --no-watermark
```

- **提示词模板**（四要素拼装）：`<情绪板推导的氛围词> + <品牌色与材质约束> + <构图要求（主体位置/留白比例）> + <风格锚（如 flat illustration / isometric / photographic）>`
- **纪律**：生成图**必须落盘**（URL 24h 过期）；提示词里的品牌色写 hex；产出图纳入 slop/对比度检查；页面上标注来源为 AI 生成由项目方决定
- **环境依赖**：`ARK_API_KEY` 等环境变量——未配置时此通道不可用，media 回退到"无图设计"（craft-polish 的排版/压注路线不依赖图片照样成立），**不得用占位 CDN 顶替**

## 5. 图标体系（一套贯穿）

- 选型：**Lucide**（默认，线性、与 Tailwind 生态亲和）/ Tabler / Phosphor（有 weight 变体）/ Iconify（聚合器）——与字体配对同理：**一套贯穿全站**，不混两家
- 笔画粗细、圆角风格与整体设计语言对齐（锐利直角设计配直角图标系）
- 功能图标必配可访问名（svg `aria-hidden` + 按钮文字，或 `aria-label`）；装饰图标 `aria-hidden="true"`
- emoji 当图标是门禁硬规则（emoji-as-icon）——永远用图标库

## 6. Lightbox / 画廊（克制使用）

- 图片画廊/lightbox 只在**内容本身就是图片**时用（作品集/摄影/商品图）；营销页装饰图不放 lightbox
- 无障碍底线：Esc + 点遮罩关闭、焦点圈定在弹层、关闭后焦点归还触发元素、图片有 alt
- 缩略图与原图同比例，防打开时跳动

## 7. 速查表

| 媒体 | 手法入口 | 性能要点 | 门禁挂钩 |
|------|---------|---------|---------|
| 背景视频 | §1 | ≤3MB / poster / 三降级 | reduced-motion / 对比度 |
| Hero 图 | §2 处理库 + §3 | AVIF + fetchpriority + CLS | placeholder-cdn / 对比度 |
| 产品截图 | §2 截图精致化 | 样机化 + 2 档宽度 | — |
| AI 配图 | §4 | 落盘 + 纳入门禁 | 全部 |
| 图标 | §5 | 按需引入（iconify 按集合） | emoji-as-icon |
| 画廊/lightbox | §6 | 缩略图 lazy | 焦点/alt |

# Inspiration Sources — 灵感站地图（双层：agent 检索层 + 用户浏览层）

> 用途：research 阶段"全网搜索设计参考"的**首选入口**。分两层消费：
> **agent 层**（§1-§3）——agent 自己按图索骥；**用户层**（§4-§5）——用户自己去逛、挑中意的东西带回来。
> 纪律：所有站都受**参考距离分级**约束（见 subskills/research/SKILL.md）——
> C 端（Persuade/Experience）只做**原理层解构**（它为什么好看），Operate/Read 允许**结构层借鉴**（它怎么组织）；
> 从任何站回来的方向，先过 `references/saturated-lanes.md` 饱和赛道检查再采用。

---

## 0. 动态搜索优先（机制，先读这条）

**本文件的站点表只是种子，不是边界。** 运行时需要灵感/组件参考时：

1. **先动态搜**——agent 用 WebSearch 按需检索，检索式模板三层：
   - 站内定向：`site:21st.dev <组件类型>`、`site:uiverse.io <元素>`、`site:shadcnblocks.com <场景>`
   - 品类泛搜：`<组件类型> tailwind block gallery`、`<场景> landing page examples 2026`
   - 新站发现：`<品类> ui components browse community marketplace`
2. **WebFetch 验证**：命中的页面要实际读取确认内容质量与许可，不许只凭搜索摘要引用
3. **清单回流**：动态搜索发现的新好站，**追加回本文件对应小节**（带日期与一句定位）——清单是活的、越用越全
4. **给用户的菜单同理**：research 给用户的浏览菜单 = 动态搜索结果 + §4 种子表按场景合成（挑 2-4 个站，不全表砸脸）

## 1. Agent 层怎么用（§2-§3）

1. **先想清楚要什么**：整页气质（品牌官网）/ 单组件样式 / 交互流程怎么走 / 移动端实录——各类站各管一段
2. **用表内检索式**（比泛搜 dribbble 噪音低一个量级）；命中后记录"链接 + 一句解构笔记"，不存图、不克隆页
3. **解构四步**（解构→分析→融合→优化）跑在笔记上，不在页面上；融合时外观从品牌推导，不从参考搬

## 2. Agent 层站点地图

### 2.1 整页灵感（气质 / 布局 / 排版）

| 站点 | 擅长 | 入口/检索式 | 解构要点 |
|------|------|------------|---------|
| **Awwwards** awwards.com | 获奖站全库，质量天花板 | 按类别筛选（`awwwards.com/websites/` + 分类名） | 获奖理由常在动效编排与排版胆量——记"它敢做什么"而非"它用了什么色" |
| **Godly** godly.website | 人工精选，极简与大胆两端 | 首页流 + `godly.website/search?query=<关键词>` | 筛选眼光极严——适合校准"高级感"的基准线 |
| **Land-book** land-book.com | Landing Page 分类库 | 按行业/风格标签筛 | 首屏构图与 CTA 处理的横评素材 |
| **Lapa.ninja** lapa.ninja | 落地页 + 电商 + 作品集 | 标签筛（dark/light/gradient…） | 数量大，适合看同一品类的**差异化做法**（反同质化输入） |
| **SaaS Landing Page** saaslandingpage.com | SaaS 官网专库 | 分类浏览 | 注意：此品类恰是饱和赛道 #2 高发区——只解构差异化策略，不学共性 |
| **Httpster** httpster.net | 排版驱动的展示站 | 首页流 | 字体层级与网格胆量的最佳样本 |
| **Minimal Gallery** minimal.gallery | 极简风专区 | 首页流 | 留白与负空间的节奏 |
| **One Page Love** onepagelove.com | 单页站 | 模板/案例双区 | 单页叙事节奏（滚动叙事结构） |
| **SiteInspire** siteinspire.com | 优质站分类库 | 按风格/主题/类型三轴筛 | 交叉筛出小众方向（反收敛） |

### 2.2 交互与流程实录（怎么"工作"的）

| 站点 | 擅长 | 入口/检索式 | 解构要点 |
|------|------|------------|---------|
| **Mobbin** mobbin.com | App/网页真实 UI 全流程截图库 | 按应用/流程筛（onboarding、settings…） | **B 端/Operate 结构借鉴首选**：信息密度、导航组织、状态处理 |
| **Page Flows** pageflows.com | 完整交互流程录像 | `"<流程名>" site:pageflows.com` | 流程步序与回退路径——喂 design 的状态契约思考 |
| **Refero** refero.design | 按功能流跨应用截图 | 功能关键词检索 | 同一功能在不同产品里的做法横评 |

### 2.3 组件与视觉块（已并入组件目录）

组件灵感走 `references/component-block-catalog.md`（19+ 库索引，含场景决策树）——本表不重复收录。

## 3. 解构纪律（与既有机制的对齐）

- **Dribbble / Behance 降权使用**：概念稿≠可实现——视觉存在渲染与实现落差，且是 AI 味收敛重灾区。低噪音检索式：Dribbble 用 `portfolio landing page minimal`、`<场景> web design shot` 等作品集向词（忌 `UI kit free` 类下载向词）；Behance 用 `brand identity website`、`<行业> case study`。落地前必须过反 AI 味规则与可访问性底线
- **原理层问题清单**（C 端）：它把赌注压在哪（色彩/排版/动效/材质）？视觉锚点有几个？留白敢到什么程度？——答案写进情绪板推导，不写色值
- **结构层问题清单**（B 端/Read）：导航怎么分？密度多高？状态怎么呈现？——答案写进 Macrostructure 与 admin-enterprise 模式选择
- **回程检查**：候选方向若落进饱和赛道（saturated-lanes.md），要么给出 register 理由，要么换方向

---

## 4. 用户浏览目录（给用户自己逛的菜单，按"想挑什么"分类）

> **触发**：research 第 1 轮"参考维度"确认后，用户选"我自己看看"→ 按场景从下表**挑 2-4 个站**给用户（配一句"挑中后发我链接或截图"），再按 §5 映射接回。下表是种子——运行时按 §0 动态搜索扩充。

| 浏览意图 | 推荐站点（种子） | 能挑到什么 |
|---------|-----------------|-----------|
| **挑单个组件** | 21st.dev/community/components、uiverse.io、Aceternity UI、Magic UI、Cult UI、shadcn.io/awesome | 定价区/hero/卡片/动效组件的成品与源码 |
| **挑页面区块/整段** | shadcnblocks.com、Shadcn UI Blocks（约 3,900 block）、Shadcn Space、Origin UI、Tailwind Plus blocks、pagedone.io、tailgrids.com/blocks、Preline examples、Flowbite blocks | 成套 section：hero/特性组/pricing/footer |
| **挑整页气质** | §2.1 九站 | 整页气质与布局方向 |
| **看真实产品怎么做** | §2.2 三站 | 真实 App/网页的流程实录 |
| **挑图标** | lucide.dev、tabler.io/icons、phosphoricons.com、simpleicons.org、iconify.design | 全套图标体系（一套贯穿，配字体配对同理） |
| **挑图片/插画/动效素材** | unsplash、pexels、lummi.ai（AI 图）、unDraw、Ouch by Icons8、storyset、lottiefiles、coverr（视频） | hero 配图/插画/lottie/背景视频 |
| **背景图案/纹理** | heropatterns.com、svgbackgrounds.com | 可定制 SVG 底纹（前景/背景色/透明度可调） |
| **样机展示** | Mockup World、LS Graphics、shots.so | 设备/浏览器样机——产品截图的高级呈现 |
| **调主题/配色** | tweakcn（shadcn 主题编辑器）、uicolors.app | 主题级配色方案 |
| **挑字体** | fontshare.com、fonts.google.com、fontpair | display/正文配对 |
| **元目录（找更多站）** | design-resources.com、Good Design Tools | 目录的目录——§0 动态搜索的助推器 |

## 5. 回流映射（用户挑完怎么接回来）

| 用户带回 | 接法 |
|---------|------|
| 组件的 URL 或名字（如"21st.dev 的 Pricing Section 1"） | 21st.dev Magic MCP 直接装进代码库 / shadcn add / 读源码并入 Token 体系（见 references/mcp-integration.md） |
| 截图 | 多模态读图解构：色/字/布局/签名识别符候选 → 按 Design Brief 确认 → 受参考距离分级约束 |
| 页面 URL | 既有任意网站 Token 提取流程（research SKILL.md，受参考距离分级约束） |
| 整站 URL | site-cloner 抓全站 → research 现有风格审计模式解构 |
| 字体/图标/配色方案 | 直接进 Token 体系（受 craft-polish.md 与字体纪律约束） |

> 所有回流统一后置检查：反参考一票否决 + 饱和赛道回程 + 反 AI 味门禁。

---

## 6. 本地实物参考（零网络依赖的解构源）

- **awesome-design-html**（本机 `C:\Users\Administrator\.zcode\skills\awesome-design-html\assets\web\`）：26 个品牌的**完整可渲染单文件 HTML**（含 `:root` 品牌 token 与 Google Fonts）——research 阶段直接 Read 解构，等价于"用户把参考站搬到了本地"
- 解构方式与「任意网站品牌Token提取流程」一致；Apple/Stripe/Linear/Notion 等常用品牌均在

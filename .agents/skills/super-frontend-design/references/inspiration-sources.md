# Inspiration Sources — 灵感站地图（设计稿 / 交互实录 / 组件灵感）

> 用途：research 阶段"全网搜索设计参考"的**首选入口**——按要找的东西选站，不再盲搜 dribbble。
> 纪律：所有站都受**参考距离分级**约束（见 subskills/research/SKILL.md）——
> C 端（Persuade/Experience）只做**原理层解构**（它为什么好看），Operate/Read 允许**结构层借鉴**（它怎么组织）；
> 从任何站回来的方向，先过 `references/saturated-lanes.md` 饱和赛道检查再采用。

---

## 1. 怎么用这张表

1. **先想清楚要什么**：整页气质（品牌官网）/ 单组件样式 / 交互流程怎么走 / 移动端实录——三类站各管一段
2. **用表内检索式**（比泛搜 dribbble 噪音低一个量级）；命中后记录"链接 + 一句解构笔记"，不存图、不克隆页
3. **解构四步**（解构→分析→融合→优化）跑在笔记上，不在页面上；融合时外观从品牌推导，不从参考搬

## 2. 站点地图

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

组件灵感走 `references/component-block-catalog.md`（Aceternity / 21st.dev / Magic UI / Cult UI / HeroUI / daisyUI / Tremor 等，含场景决策树）——本表不重复收录。

## 3. 解构纪律（与既有机制的对齐）

- **Dribbble / Behance 降权使用**：概念稿≠可实现——视觉存在渲染与实现落差，且是 AI 味收敛重灾区；仅在找"纯视觉情绪"时用，落地前必须过一遍反 AI 味规则与可访问性底线
- **原理层问题清单**（C 端）：它把赌注压在哪（色彩/排版/动效/材质）？视觉锚点有几个？留白敢到什么程度？——答案写进情绪板推导，不写色值
- **结构层问题清单**（B 端/Read）：导航怎么分？密度多高？状态怎么呈现？——答案写进 Macrostructure 与 admin-enterprise 模式选择
- **回程检查**：候选方向若落进饱和赛道（saturated-lanes.md），要么给出 register 理由，要么换方向

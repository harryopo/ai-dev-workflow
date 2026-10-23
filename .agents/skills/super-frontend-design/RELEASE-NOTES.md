# super-frontend-design Release Notes

## v2.13.0 (2026-10-23) — 状态契约：让"只能演示 happy path"变成可机检的失败

### 为什么做这件事

`references/admin-enterprise-patterns.md` §8 早就写了「空态 / 加载态 / 错误态」三态纪律，末尾还有一句"每个列表页交付前自查：首次进入、筛选无结果、加载中、接口失败、无权限——五个状态都有设计才允许交付"。

但实测发现这套纪律有个致命问题：**它只是参考文件里的一张人工清单**。`review` 的 13 项检查表不引用它，`design` 的 Step 6 交付清单也不引用它，没有任何一道门禁会读它。

为了确认这不是印象而是事实，我造了一个"典型 AI 生成的订单列表页"做探针，逐个跑现有全部门禁：

- 第一版带 AI 默认 indigo 色 → slop_scan 抓到了，这是符合预期的
- 改到完全合规（换 teal 主色、补 `:focus-visible`、加签名标记、加构图契约）→ **slop_scan / token_lint / signature_check / composition_check 四道门禁全部 PASS**
- 而这个页面依然：**没有任何加载态、空态、错误态、无权限态**

把接口关掉、数据库清空、网络断掉，用户看到的就是一块空白。**门禁全绿，交付物只能演示 happy path。**

这不是 C 端专属问题——B 端最常见的交付事故正是这个。而且它和前两阶段修的是同一类病的第三个变种：v2.11.0 修"没有辨识度"，v2.12.0 修"层级失焦"，这一版修"半成品交付"。

### 状态契约是什么

页面存在异步数据或用户可触发操作时，用一个标记声明它覆盖哪些状态：

```css
/* states: loading,empty,error */
```

```html
<!-- states: loading,empty,error -->
```

**派生表**由 research 第 3 轮的「交互复杂度」驱动——这是本次新增 `interaction-complexity` pass-data 字段的原因。此前那个问题（问题 8）的答案只进 Design Brief 的自由文本，下游没有任何字段能消费它：

| `interaction-complexity` | 必须声明 |
|---|---|
| `static` | 无（**明确豁免**） |
| `basic` | `error`、`success` |
| `moderate` | `loading`、`empty`、`error` |
| `complex` | `loading`、`empty`、`error`、`no-permission` |
| `app` | `loading`、`empty`、`error`、`success`、`no-permission` |

**`static` 豁免是设计的一部分，不是遗漏**。一条静态营销页没有 loading 态不是缺陷；要求它写 `/* states: */` 只会训练出"为了过门禁而堆标记"的反向作弊——那比没有门禁更糟，因为它让门禁从"防漏"退化成"看会不会抄"。

### 新增第 9 道门禁 `scripts/state_check.py`

判定规则：
- **声明了但代码里没实现 → FAIL**（`state-declared-not-landed`）——这是门禁要抓的核心谎言
- **零声明且零实现、复杂度非 static → FAIL**（`state-absent`）
- **复杂度要求的状态声明里缺 → FAIL**（`state-required-missing`）
- **实现了但没声明 → WARN**，不阻塞（可能是实现先于声明）
- `--complexity` 取值越界 → exit 2，不静默按"无要求"处理

**证据判定刻意宽松**（类名 / `data-state` / 文案三选一）。脚本只证明"这个状态在代码里出现过"，不判断状态设计得好不好——骨架屏对不对位、错误态有没有重试入口，那是 review #14 的人工职责。**脚本保证"做了"，review 保证"做对了"，两者不可互相替代。**

### 顺手修掉 v2.12.0 遗留的一个真 bug

探针过程中发现的：`composition_check.py` 的正则只认 `/* composition: */` CSS 块注释，但 `signature_check.py` 同时支持 HTML 注释。**同一套机制内部口径不一致**——而 Tailwind v4 项目、单文件 HTML 项目根本没有独立 CSS 文件，按 v2.12.0 文档"写 CSS 顶部"的要求，这类项目必然误判为 `composition-absent`。

现在 `composition_check.py` 也支持 `<!-- composition: -->`，`composition-contract.md` §3.1 重写成"载体随项目形态"的三行表。契约测试 17 → 20 项，专门锁住 HTML 载体、双载体混用、HTML 载体缺要素仍要抓。

### 门禁与防退化

新增 `check_phase5_wiring` 审计项：校验 6 处接线存在、五档派生表齐全、三条失败规则未被掏空、static 豁免分支未被删。配 10 条 mutation。audit 检查项 49 → 50。

**mutation 过程中抓到一条假绿灯**：最初审计用 `re.search("state-absent", src)` 裸子串匹配，把 `"rule": "state-absent"` 改成 `"rule": "state-absent-note"` 后仍能匹配——mutation 显示 exit=0 MISMATCH。已改为完整的 `"rule": "xxx"` 形式匹配。**教训和 v2.11.0 那次一样：规则存在性检查不能用裸子串，否则同名前缀的替换就能骗过它。**

### 其余

- 主 SKILL.md 铁律 11 → 12 条（新增「状态契约必须落地到代码」，含 static 豁免条款）；§7.2 pass-data 增 `interaction-complexity` + `states` 字段；§6 资源索引补新参考 / 新脚本 / 新测试
- 门禁数 8 → 9（SKILL.md §3.6 / §6 / §8 + design §16 四处同步）
- README：工作流图标注状态链路、design/review 子命令说明、项目结构补新脚本、版本历史补 v2.13.0
- evals 38 → 44 条：v213-001（moderate 派生）/ 002（static 豁免）/ 003（complex 派生）/ 004（状态审查）/ 005（假声明）/ 006（app 全量五态）

## v2.12.0 (2026-10-23) — 构图契约：让"层级失焦"也变成可机检的失败

### 为什么做这件事

上一版解决了"有没有做对什么"（签名），但没解决"做出来像不像样"。实测发现三个事实：

1. `rules/slop-table.json` 的 **30 条判定规则里，0 条涉及 macrostructure**——构图层完全在反 AI 味体系之外。
2. `references/macrostructures.md` 定义了 21 种结构（含"正文列数""分隔手段""入场形态"等），但**下游没有任何阶段消费**——选完结构就丢了。
3. "视觉重心"（首屏几个焦点、谁最突出）在全仓只出现 2 次，且都在 review 里作为纯人工项。

结果就是一类典型失败：**Token 全对、颜色全对、间距全对，但页面没有主次**。首屏同时放三个同等强调的按钮，三栏正文等宽，三处标题样式完全一致——所有 Token 门禁都过，所有 slop 规则都过，交付物仍然"一眼看完"。

构图契约补的就是这层：**把构图级决策（标题锚点 / 正文列数 / 分隔手段 / 图片处理 / 入场形态 / 视觉重心）也纳入 pass-data 传递，让 design 阶段有可追溯的依据而不只是"照 Token 填"**。

### 落点

**① `references/composition-contract.md`（新）**
六要素字段表写清每项的取值来源与边界（为什么不含 button——button 已被 theme Token 约束，不需要重复占位）；视觉重心三级规则（1 = 首屏唯一焦点 / 2 = 主+次 / 3 = 三级），B 端 Operate 默认 3。核心设计原则写在 §3.2 落地判据表里：**脚本保证"声明了"，review 保证"做对了"，两者不可互相替代。**

**② design Step 1.6「构图契约落地」（不可跳过）**
3 条硬约束：**六项必须全写**（缺一即失败）、**必须写进代码**（CSS 顶部六行 `/* composition: xxx=... */`）、**声明必须与实现一致**。视觉重心给了三级判定表，并明确「层级由 macrostructure 决定，不由内容决定」「同屏同级焦点 ≤ 1」。

**③ review #13「构图契约一致性」**
三步：取声明 → 逐项对账（6 字段判据表）→ 查焦点。**不通过时回 design Step 1.6 重做，而不是加个标记糊弄过去。**

### 新增第 8 道门禁 `scripts/composition_check.py`

判定规则：
- **缺任一要素 → FAIL**（`composition-fields-missing`）
- **有契约无 macrostructure 戳记 → FAIL**（`composition-without-stamp`）——防止随便挑个结构
- **focus-hierarchy 取值非 1/2/3 → FAIL**（`composition-focus-invalid`）
- **要素取值为空 → FAIL**（`composition-field-empty`）
- `--require-macrostructure` 可核对指定结构
- 完全没有契约 → WARN（不阻塞，但会提示）

**macrostructure 戳记解析的坑**：戳记形如 `01·Bento Grid · theme: Tally · genre: SaaS`，结构名本身含 `·`，正则非贪婪匹配到第一个 `·` 就停会只取到 `"01"`。最终改为捕获到 `*/`，再按 "key: value" 形态切分（遇第一个带冒号的段即停），正确取出 `01·Bento Grid`。

### 门禁与防退化

新增 `check_phase4_wiring` 审计项：校验 5 处接线存在、六要素字段齐全、缺要素与无戳记两条失败规则未被掏空。配 6 条 mutation case 证明能变红（契约文件被删 / 落地被删 / focus 层级被删 / 审查被删 / 脚本被掏空 / 戳记规则被掏空）。audit 检查项 48 → 49。

### 其余

- 主 SKILL.md 铁律 10 → 11 条（新增「构图契约必须落地到代码」）；§7.2 pass-data 增 `macrostructure` + `composition` 字段；§6 资源索引补新参考 / 新脚本 / 新测试
- 门禁数 7 → 8（SKILL.md §3.6 / §6 / §8 + design §16 四处同步）
- README：工作流图标注构图链路、design/review 子命令说明、项目结构补新脚本、版本历史补 v2.12.0
- evals 32 → 38 条：v212-001（构图落地）/ 002（构图审查）/ 003（B 端重心三级）/ 004（macrostructure 戳记）/ 005（缺要素）/ 006（focus 取值越界）

## v2.11.0 (2026-10-23) — 签名机制：把"20% 独特选择"从文档变成代码

### 为什么做这件事

`references/anti-ai-slop.md` 里一直有两条标准：「**~80% 成熟模式 + ~20% 独特选择**」和「**灵魂验证问题**——如果截屏后一个不参与项目的人能辨认出这是哪个产品的设计 → 有灵魂；不能 → 你交付的是模板」。

但全仓 grep 只有 `anti-ai-slop.md` 自己命中这两条。**它们是孤儿条款**——写得再好也没有任何阶段会执行它们。

根因是整个检查体系是**否定式**的：56 条反 AI 味清单、饱和赛道黑名单、二阶反射检查，做的全是"排除确定的坏"。这类检查有个共同盲区——**一个干净、正确、但毫无辨识度的设计可以通过全部检查**。前面 11 项 review 检查全过，交付的仍可能是一份"漂亮但可替换"的模板。

签名机制补的就是这半：**这是整套体系里唯一的肯定式检查**（"有没有做对什么"），并且从调研到审查全链路都有承载字段。

### 五处接线

**① research —— 挖掘原料（问题 12.5，第 4 轮）**
调研前 4 轮收集的全是通用信息（品牌人格、情绪板、参考、禁忌），这些足以产出一个"正确但不专属"的设计。真正让产品被认出来的是**只有它才有的东西**：一个行业术语、一个内部黑话、一个只有老用户懂的交互习惯。

新增问题 12.5「签名线索」→ 强制推导表把线索转成可落地的设计决策：

| 线索类型 | 签名识别符形态 | 落点举例 |
|---------|--------------|---------|
| 行业术语 / 黑话 | 术语的视觉化 | 品牌词以等宽字体独立成版式单元 |
| 老用户才懂的交互 | 交互的专属化 | 拖拽排序手柄用磁吸 + 落位微弹 |
| 独有数据 / 指标 | 指标专属呈现 | 关键指标用条带而非卡片承载 |
| 独有动作 / 流程 | 流程专属化 | 三步流程用连续进度带而非圆点 |
| 独有文案语气 | 语气的视觉化 | 标题用负 tracking + 句号收尾 |

**新增铁律 5**：不允许零签名进入后续阶段。用户答不出时从品牌人格 × 情绪板 × 设计类型反推候选并标 `[待用户确认]`。

**② creative —— 绑定方向（§0.5）**
发散规格从三件套变四件套，每个方向必须声明自己的签名实现方式。**新增签名硬门**：两个方向若签名落点相同，即使视觉差异维度够，也视为同一方向的不同措辞，必须重做——签名是方向的指纹。

**③ theme —— 推导专属 Token**
签名的落地方式可能需要专用 Token（术语版式化 → `--font-mono` + `--tracking-term`）。规则：签名专属 Token 是**增量**，不覆盖视觉论文推导的主 Token；至少 1 个，命名带 `--signature-*` 语义。

**④ design —— 落地到代码（Step 1「签名落地」）**
方向只是意图，代码才是交付物。新增 3 条硬约束：**标记注释必写**（`/* signature: */`，机器可判定的锚点）、**至少 1 处**（零落点 = 没做）、**可见性自检**（落在页脚版权行不算数）。配落点选择表（按签名形态给首选/次选落点）与 4 条落地自检。

**⑤ review / critique —— 验收（#12）**
新增 #12「签名可识别性」并展开三步判定法：取证（搜标记注释、统计数量与位置）→ 对照（签名描述的东西在屏幕上看得见吗）→ 代入（陌生人只给一张首屏截图，能否说出这是哪个产品）。

### 新增第 7 道门禁 `scripts/signature_check.py`

判定规则：
- **零落点 → FAIL**（不是"效果不好"，是这一项根本没做）
- **落点全在低关注容器 → FAIL**（看不见的签名等于没有签名）—— 用容器跨度判定（`</footer>` 闭合前的行），不是简单的行邻近，避免 hero 里的签名被下方 footer 误伤
- **首页（index.html）无签名 → FAIL**（陌生人第一眼看的就是这个页面）
- `--require-marker` 可核对指定签名文本
- 扫描零文件 exit 2（空扫描不等于通过）

**嵌套注释不算落点**：HTML 注释里嵌一个 `/* signature: */` 是示例，不是落地。实现上先按 HTML 注释切分再在剩余部分找块/行注释形式——注意 HTML 注释本身也是合法标记载体（`<!-- signature: -->`），不能整体剥掉。

### 门禁与防退化

新增 `check_phase3_wiring` 审计项：校验 7 处接线存在、抽签脚本的留痕字段未被删、零落点失败规则未被掏空、**「灵魂验证问题」不得再退回孤儿状态**。配 5 条 mutation case 证明能变红（挖掘被删 / 落地被删 / 审查被删 / 脚本被掏空 / 灵魂问题变孤儿）。audit 检查项 47 → 48。

### 其余

- 主 SKILL.md 铁律 9 → 10 条（新增「签名必须落地到代码」）；§7.2 pass-data 增 `signature` 字段；§6 资源索引补新脚本与新测试；门禁数 6 → 7（§3.6 与 §8 同步）
- `references/anti-ai-slop.md`「灵魂验证问题」明确移交 review #12，保留为标准出处
- README：工作流图标注签名链路、子命令说明更新、项目结构补新脚本、版本历史补 v2.11.0
- evals 26 → 32 条：v211-001（签名挖掘）/ 002（签名落地）/ 003（签名审查）/ 004（用户答不出线索）/ 005（重构通道）/ 006（页脚落点）

## v2.10.0 (2026-10-23) — 参考机制 2.0 Phase 2：原创引擎接线
执行 `docs/super-frontend-design-参考机制2.0方案书.md` 第三节 Phase 2 三项。C 端品牌场景此前走的是收敛机制（搜索参考 → 提取 → 融合），同一个 skill 里的发散引擎（creative 的命名运动 → 视觉论文）没有被接进主流程——这是产出同质化产物的技术根源。本次把发散接回去，并补上事后检验。

### P2-1 多方向强制发散（creative §0.5 + design Step 1）
- **触发条件**：仅 Design Brief 中「访客意图分类」为 **Persuade / Experience**（官网 / 营销页 / 作品集）。Operate（B 端）与 Read（内容站）跳过——B 端要的是效率与一致性，多方向反而是负担。字段缺失或独立调用时退回单方向。
- **发散规格**：产出 2–3 个方向，每个方向三件套完整独立——命名运动（1–2 词，像真实存在过的设计运动）+ 视觉论文（回答标准 5 问，每问给具体决策而非形容词）+ 关键 Token 提案（3–5 个具体值，供用户判断差异）。
- **差异硬门**：方向之间至少 2 个维度显著不同（配色策略 / 排版性格 / 布局骨架 / 材质质感 / 动效性格）；差异维度 < 2 或关键 Token 主色 hex 相同 → 视为同一方向，必须重做。这条门防止"同一个想法换三种说法"冒充发散。
- **并置呈现**：用 AskUserQuestion 让用户选，**不得替用户默认选定**。取舍分析必须诚实——每个方向都要写代价（识别度 vs 亲和力 / 表现力 vs 性能 / 差异化 vs 行业惯例），不做彩虹屁。
- **两种模式**：默认多方向并置；用户明确要"稳 / 直接给我一个"时走「单方向 + 随机变体」，变体用外部随机抽取。
- **并行子代理（可选）**：每个代理领一份不同约束（建筑 / 印刷史 / 材料科学），≤3 个。约束：必须拿到同一份 Design Brief 约束边界否则会漂出 Brief；代理产出不得直接采用，主流程必须做差异维度校验后才可呈现。
- **输出落盘**：`pass-data.yaml` 增 `direction-candidates` 与 `selected-direction`。
- **design 侧约束**（Step 1 新增「方向来源约束」）：有 `selected-direction` → 沿用，视觉论文必须一致，不一致 🔴 报错退回 creative；有候选无选定 → ⛔ 停止退回 creative，**不得自行挑一个**；擅自换方向 = 严重违规——绕过用户选定方向做参数微调（换色值、改圆角）不叫迭代，叫换方向没告知用户。

### P2-2 二阶反射检查（review §0 #11 + critique）
- **机制**：反 AI 味清单管住了"AI 默认丑"，饱和赛道清单管住了"整页美学家族"，但两者都只做一阶——只从品类出发猜。二阶多问一步：**把反参考也告诉对手**，看还能不能猜到。
- **判定**：构造猜测句「给一个 [品类] 做设计，不要 [反参考]，你会做成什么样？」——能命中本次主题与配色即为二阶反射，🔴 严重。
- **典型二阶陷阱**：反参考是"不要米色 / 不要圆润卡片"，产出改成"深底 + 高对比撞色 + 几何无衬线"——躲开了米色赛道，但"深底撞色几何"同样是当前饱和风格。躲猫猫不是原创。
- **处理方式**：不是换个配色了事——回 creative §0.5 **换掉产生该猜法的那个方向**，而不是在原方向上做参数微调。
- **与 #10 的区别**：#10 是客观比对饱和赛道指纹；#11 是主观可猜性。两者独立，命中任一都要处理。
- critique 侧：Assessment A 评估方法补二阶反射检查，报告模板「设计灵魂追溯」表补反参考遵守 / 饱和赛道反射 / 二阶反射三行。

### P2-3 结构化随机兜底（research + scripts/random_draw.py）
- **问题**：用户说"随便 / 都行 / 你定"时，AI 的默认行为是挑最保守的那一个（安全蓝 + 系统字体 + 居中 Hero）——既浪费了用户的授权，又制造同质化。
- **做法**：先在脑内生成 2–3 个**同等合理**的候选（都通过调研约束与设计禁忌检查），再用真正的外部随机挑一个，并回传结果。随机源是操作系统熵（os.urandom + rejection sampling），不是模型自造的"随机"。
- **新脚本 `scripts/random_draw.py`**：等概率抽取 + 完整留痕（候选列表 / 选中项 / 熵源字节 hex / UTC 时间戳）；候选去重（不因重复获得双倍概率）；候选不足 2 个时 exit 2 并说明"单候选没有随机可言"。
- **纪律**：一个决策点一次抽（不许一次抽多维度再拼装）；禁止造假随机（不得声称随机却没调脚本）；不得静默替换（抽签结果必须出现在回复里，用户否决可另起一次抽签，但不得连抽直到抽中自己想要的）；候选必须同等合理（不能塞明显更差的选项充数）。
- **不适用**：用户说"你推荐"而非"随便"（推荐是主动判断，随机是放弃判断）；有客观正解的问题（合规 / 框架支持）；B 端布局与密度选择（惯例即最优）；风格审计模式（候选取自现有代码，客观上存在正解）。
- **契约测试** `tests/test_random_draw.py` 14 项：等概率性 / 候选可达性 / 无饥饿 / 去重 / 单候选必拒 / 留痕字段完整 / 选中项必在候选内 / 文本模式回显。

### 其余
- 主 SKILL.md 调研铁律 7 → 9 条：新增「C 端品牌场景必须走方向发散」「"随便"不默选保守项」两条；§3 creative 阶段补方向发散说明；§6 资源索引补 `scripts/random_draw.py` 与 `tests/test_random_draw.py`。
- README：六阶段工作流图标注 C 端方向发散环节，creative 子命令说明补「C端方向发散」，项目结构补 scripts 目录清单。
- evals 20 → 26 条：v210-001（C 端官网 + "随便"双触发）/ v210-002（多方向规格）/ v210-003（二阶反射）/ v210-004（随机兜底）/ v210-005（B 端跳过发散）/ v210-006（沿用选定方向）。
- 验证：audit_integrity 46 项全 PASS；契约测试 6 套 —— audit_gate_red 15 项、slop_scan 9 项、structure_lint 10 项、token_lint 12 项、random_draw 14 项全绿；render_probe 因环境缺 Playwright 跳过；visual_diff 因环境缺 Pillow 未运行（两者均为既有环境依赖，非本次引入）。

## v2.9.1 (2026-10-23) — 版本治理收口 + Slop Test 口径补全
- **子技能版本字段清理**：9 个子技能（research / design-context / creative / theme / design / review / critique / refine / animate）的 frontmatter 各自声明 `version: 2.7.0`，而主 SKILL.md 已是 2.9.0 —— 长期漂移无人发现。子技能是主技能的组成部分，独立版本号无意义，故全部删除。主 SKILL.md 成为唯一版本真值源。
- **新增 `version-field` 门禁**（`scripts/audit_integrity.py` → `check_version_fields`）：子技能 frontmatter 出现 `version` 即判失败；主 SKILL.md / `evals/evals.json` / README 徽章三处版本号必须一致。防止手滑写回或漏同步版本号。audit 检查项 43 → 46。
- **Slop Test 56/30 口径补全**：56 条（`references/slop-test.md`，人工核对）与 30 条（`rules/slop-table.json`，脚本静态判定）的关系此前只写在 `review/SKILL.md` §2.18，SKILL.md 索引行、路由段、README 三处只写「56 条」，读者会误以为全部由脚本执行。已在三处补写「其中可静态判定的部分由 `slop_scan.py` 执行，判定表见 `rules/slop-table.json`，其余人工核对」。
- **未实施**：参考机制 2.0 Phase 2（多方向强制发散 P2-1 / 二阶反射检查 P2-2 / 结构化随机兜底 P2-3）——方案书 `docs/super-frontend-design-参考机制2.0方案书.md` 已就绪，待 Phase 1 验收后执行，本次不含。

## v2.9.0 (2026-10-16) — 参考机制 2.0：参照系修复（去同质化 Phase 1）
- **参考维度追问**：第 1 轮"想参考哪家"改造为分层提问——先问参考维度（交互模式 / 布局骨架 / 色彩体系 / 整体感觉，multiSelect），再问参考对象；参考不再默认"全套"。目标受众问题移入第 2 轮（第 1 轮 4 问上限）
- **反参考机制**（借 impeccable 的 anti-references）：第 1 轮新增"要避开什么"（可跳过）；写入 Design Brief、pass-data.yaml（`anti-references`）、DESIGN.md 新增 Anti-references section；review §0 新增 #9 反参考遵守检查
- **参考距离分级**（自研）：场景决定参考能走多深——Operate 结构借鉴/Token 原创；Persuade·Experience 原理解构、外观原创（只取"为什么"，色值不进 Token）；Read 结构为主。用户显式要求复制时允许 Token 提取但须标记"显式复制请求"且其余维度强制差异化。落点：research「参考距离分级」表 + Token 提取流程 Step 0 + design 解构四步（提取范围收窄 + **禁止同层混合**"A 布局 + B 配色" + 外观 Token 来源链：品牌推导 > 视觉论文 > 内置预设）
- **反收敛样本池**：参考对象问题改四选项（软件参考 / 跨领域参考 / 形态描述 / 不参考）；新增「形态 archetype 表」（6 种形态，借 awesome-design-html）+「跨领域参考」引导（建筑/印刷/工业/自然——接入既有跨领域原则）
- **饱和赛道黑名单**：新增 `references/saturated-lanes.md`（首发 3 条：Stripe 邻近编辑排版风 / 紫蓝渐变 SaaS 风 / Notion 邻近米色风），含 register 豁免条件与维护规则；review §0 新增 #10 饱和赛道反射检查；§0 检查总数 8 → 10
- **情绪板升级**：第 4 轮新增强制「情绪板 → 参数推导」表（色相策略 / 字体气质 / 材质 / 动效性格，含示例），推导落进 DESIGN.md 对应 section；Design Brief 与 DESIGN_BRIEF.md 模板同步
- 主 SKILL.md：§3.5 铁律摘要新增第 7 条（参考不默认全套）；§7.1 术语表新增"反参考""参考距离分级"；§7.2 pass-data 增 `mood-board-derivation` / `anti-references` / `reference-distance` 字段
- evals 16 → 20 条（v29-001 Stripe 官网 / v29-002 反AI味诉求 / v29-003 Linear 布局后台 / v29-004 情绪板推导）

## v2.8.1 (2026-10-16) — 现有风格重构流程（风格审计 + 设计稿确认门 + 风格固化）
- 路由新增「按现有风格重构 / 统一风格」分支（SKILL.md §3.6 现有风格重构流程）：保持现有风格的请求走「现状审计 → 统一设计稿 → ⛔用户确认 → 按稿重构」，不再误走"换新风格"的 5 轮问卷或被整体跳过调研；只说"重构"未提风格时，调研第一步先问「保持现有风格统一收敛 / 换新风格」再分流
- research 新增「现有风格审计模式」并列于 5 轮问卷：扫描现有代码 + 门禁测量（token_lint / slop_scan 的 font-size-step-count、radius-value-count、bare-hex-outside-root）作为机器证据 → 风格画像 + 不一致点清单（附文件:行号）→ AskUserQuestion 逐项确认统一方案；品牌人格 / 情绪板从现有证据推导后确认（铁律区补"重构场景的合法替代"说明）
- 设计稿确认硬门：design-context 生成的 DESIGN.md 在该流程中作为「统一设计稿」呈现用户，明确确认后才进入实现；design §0 新增 `refactor-mode: style-audit` 额外前置（检查 pass-data.yaml 的 `spec-confirmed` 字段，缺失即拒绝执行）
- 风格固化 + 后续约束：design 交付清单新增"询问是否将统一风格写入项目根 DESIGN.md/PRODUCT.md"；主 SKILL.md 新增「项目设计规范优先」规则——项目存在 DESIGN.md 时，任何后续设计 / 优化 / refine / theme / animate 请求先读并以它为基准；refine / theme 子技能同步加前置检查
- §0 边界澄清：明确"跨会话 / 跨项目历史偏好（禁止）"与"本项目现有代码 / DESIGN.md（合法且必要的审计对象）"的界限，防止审计被误读为"读历史偏好"而跳过
- evals 13 → 16 条（v28-004 按现有风格重构 / v28-005 统一风格不换风格 / v28-006 有 DESIGN.md 的后续请求）

## 2026-10-11 加固（版本号仍为 v2.8.0）
- `scripts/visual_diff.py` 新增 `clean_path()` 路径契约：所有 CLI 路径参数（位置参数、`--out`、`--reference`）在 argparse 之后统一校验——拒绝空值与 `..` 段、展开 `~`，fail-closed 报错退出 2。本工具是本地 CLI、路径来自操作者本人，这道校验不是安全边界，而是把"手滑写出 ../ 相对层级"挡在读写盘之前；起因是 Mimosa L3 把 main 的 argv→Path 参数流判为 path-traversal 高危（两个扫描引擎均 0 发现，判为误报），以显式校验收敛参数流

## v2.8.0 (2026-10-11) — 软件设计增强 + 字体层级门禁 + 设计系统预设

### 字体层级与风格统一检查
- `rules/stylelint.config.json`：`declaration-strict-value` 属性清单加入 `font-size`——字号必须走 `var(--font-size-*)`，与颜色/字体同等严格度（font-size 是单值属性，天然适配 strict-value）
- `slop_scan.py` + `rules/slop-table.json` 新增两条 measure 规则（28 → 30 条）：
  - `font-size-step-count`（hard，阈值 8）：distinct 字号档位超过 8 报警；px/rem 归一计数（1rem=16px），em/var() 跳过不猜；阈值政策化 `rules/policy.json → font-size-count`
  - `radius-value-count`（warn，阈值 4）：distinct 圆角档位超过 4 报警，锚定 DESIGN.md 契约的 radius Token 档位；政策 `radius-count`
- `render_probe.py` 新增 `JS_FONTSCALE` 渲染量测：标题 computed 字号逐级不增（倒挂报 `font-scale-inverted`）、H1/正文计算字号比不足报 `heading-body-ratio-low`——阈值 1.5 政策化 `heading-body-ratio`（取自 review §2.1.1 既有条文，运行时从 policy.json 读取，脚本不抄数字）
- `rules/policy.json` 政策从 6 条扩到 9 条（新增 font-size-count / radius-count / heading-body-ratio，全部带 prose 对账与 min_hits）
- review §2.16 Typography 硬检查 T1–T8 扩为 T1–T10（T9 档位数→slop_scan 自动判定、T10 标题梯度→render_probe）；typography.md §1/§7 同步；顺带修正 review T2 阈值（≥48px）与 typography.md（≥32px）的漂移
- 夹具与测试：`slop_red.html` 种入 11 档字号与 6 档圆角触发样本、`slop_clean.html` 字号改走 Token（配合 strict-value）；`test_slop_scan.py` 8 → 9 项、`test_structure_lint.py` 9 → 10 项（font-size 严格校验契约）、`test_render_probe.py` 10 → 11 项（字号层级量测契约）、`test_audit_gate_red.py` 的规则数注入缺陷随真值更新（原注入"28→30"，真值已是 30，改为注入 30→31）
- 全仓"28 条规则"声称同步为 30（SKILL.md 索引与 review 两处）

### 软件前端设计增强
- 新增 `references/admin-enterprise-patterns.md`：B 端管理后台/企业软件设计模式库——数据表格（对齐/等宽数字/固定列/排序）、表单系统（分区/分步/校验时机/编辑态与查看态）、筛选与保存视图、批量操作、权限与状态可见性、异步任务与导入导出、三态纪律、四个布局模板（列表/详情/仪表盘/设置）、与 C 端差异对照、交付检查清单
- `references/professional-software.md` 新增四款分析（7 → 11 款）：Trae（AI IDE：对话×画布共栖、diff 预览、任务拆解流）、DaVinci Resolve（页面化工作区、时间线交互）、Blender（快捷键驱动、视口即时反馈）、Warp（块化输出、智能输入框）；对照表扩到 11 列、提取指南补 4 行；原对照表/提取指南/检查清单顺延为 §13-15
- design 子技能新增 Part 17（B 端场景路由、产品类型→参考映射、与 C 端工作流的差异执行要点）；Part 15 两张映射表同步

### 设计系统预设与组件库接入
- 新增 `references/design-systems/` 四个 Token 级预设（严格按 `design-system-template.md` 的 9-section 格式）：`tdesign.md`（--td-* 变量映射）、`ant-design.md`（antd 5 theme.token + cssVar）、`material-3.md`（tonal palette + M3 shape/type scale）、`shadcn-style.md`（OKLCH 中性系，display 字体避开门禁黑名单）；每个预设都声明"是种子不是免调研通行证"
- design-context §5：DESIGN.md 来源新增"内置预设"路径；design Part 2 新增预设推荐表（style-match 起点）；theme 预设主题章节加企业级预设引用
- design Part 7 新增"国内企业级组件库"小节：TDesign / Ant Design / Element Plus / Arco Design 的适用场景、Token 定制入口（--td-* / theme.token / --el-* / Arco 变量）、与三层 Design Token 的映射方式、反 AI 味注意点；`component-block-catalog.md` 全局索引补 4 库

### 版本
- 版本号 v2.7.0 → v2.8.0（SKILL.md frontmatter、README 徽章与版本历史、evals.json）
- 验证：audit_integrity 全项 PASS；6 套契约测试 68 项全绿（token 12 / slop 9 / audit_gate_red 13 / structure 10 / render_probe 11 / visual_diff 13）

## 2026-10-11 对账（版本号仍为 v2.7.0）
- `evals/evals.json` 的 version 字段从 2.4.0 对齐到 2.7.0；静态核对全部 10 条路由样本与 SKILL.md 路由表触发词一致
- `design-002`「全流程」样本的 expected_routing 由 `creative → theme → design → review` 修正为 `research → design-context → creative → theme → design → review`（原期望违反 SKILL.md「路由到 design 必先 research」铁律），expected_output 同步为六阶段
- version-log.md 补记 2026-10-05 两轮加固条目（此前该日志停在 10-04，与 RELEASE-NOTES.md 漂移）
- 复跑 audit_integrity.py 与全部 6 套测试（token 12 / slop 8 / audit_gate_red 13 / structure 9 / render_probe 10 / visual_diff 13）全部通过

## 2026-10-05 修复与门禁扩展（版本号仍为 v2.7.0）
- 新增 `scripts/token_lint.py`：Token 未定义引用、死 Token、与 DESIGN.md 契约双向对账（纯标准库，无 npm 依赖）
- 新增 `scripts/visual_diff.py`：页面截图与参考图逐像素对账，含白屏检测与内容密度骤变兜底（Playwright + Pillow/numpy）
- 新增 `rules/policy.json` 作为政策数字的唯一真值源；`audit_integrity.py` 增加政策一致性对账，同时校验判定表阈值与文档措辞
- 统一字体上限表述：默认两族，第 3 族仅限一个功能性 register 且不超过 2 处 slot；`slop_scan.py` 的 `outlier-face-overuse` 承担可判定部分
- 修正 review 中"首屏强调色使用面积 ≤ 10%"与其余文档的 ≤ 5% 不一致
- `slop_scan.py` 新增 `--only 规则号` 单点复检；`--allow=RULE=理由` 等号写法可用；未知参数一律退出码 2
- `emoji-as-icon` 规则改为按位置判定：元素首字符是 emoji 才算图标（此前把句中提到的 ⚠️ 误报为图标），并把匹配从 8 个手写 emoji 换成 Unicode 区段（真页面上 🧾🛡🛑🤝🔍📊 等 8 处标题图标此前全部漏检）
- 五个门禁脚本输出强制 UTF-8：此前在中文 Windows 下结论正文显示为乱码
- `token_lint.py` 修正四处误判：同行 `:root { --x: … }` 声明漏检、Markdown 的 `---` 围栏被当作 token、死 Token 归属到第一个参数而非声明文件、DESIGN.md front matter 分支未生效
- 修正 11 处遗留的"57条Slop Test"标注（premium-design-rules、refine、review、5 个 Prompt 模板）；`cross-claim` 检查范围扩展到全部 markdown（发布记录除外），并新增判定表条数对账
- review 报告模板的分层评分表补齐到 14 层、总计由 57 改为 56（此前漏掉"实现质量 V46-V49"与"特殊规则 V50-V56"两层，Hero 层少计 1 项）；`audit_integrity.py` 新增 `layer-sum` 校验分层行数相加是否等于总计
- 新增 `tests/test_token_lint.py`（12 项）、`tests/test_visual_diff.py`（13 项）、`tests/test_render_probe.py`（6 项，需 Playwright，跑不了时退出码 2 而非报过）
- `tests/test_audit_gate_red.py` 注入缺陷由 5 类增至 10 类（含政策措辞漂移、判定表阈值漂移、分层评分表不相加），另有 1 项校验参数拼错时拒跑

## 2026-10-05 结构层接入（用户授权后安装，版本号仍为 v2.7.0）
- 新增 `scripts/structure_lint.mjs`：用 stylelint 真解析 CSS、html-validate 真校验标记，补上正则做不到的判定（拼错属性名、无效 hex、重复 id、缺 `type` 的按钮、缺 alt 的图、颜色/字体没走 `var()`）
- 新增 `rules/stylelint.config.json`、`rules/html-validate.config.json` 两份规则表（都是数据）；`border`/`outline` 这类"宽度+样式+颜色"混写的简写不纳入 token 检查，避免 `1px solid var(--x)` 被误判
- 新增 `scripts/apca_contrast.mjs`：APCA Lc 交给 colorjs.io 计算（不自己写近似算法），`render_probe.py --apca` 消费；Lc 阈值只写在 `rules/policy.json`
- 新增 `rules/gates.json` 六道门禁清单与 `gate-inventory` 校验：脚本必须存在、必须被索引、文档"N 道门禁"必须与清单条数一致、文档里称作门禁却没登记的脚本报错
- `templates/sfd-tools/package.json` 提供依赖清单（stylelint 17.16.0 / html-validate 11.16.2 / postcss-html 2.0.0 / stylelint-config-html 2.0.0 / stylelint-declaration-strict-value 1.12.1 / colorjs.io 0.7.1，六个包全部 MIT 且带 LICENSE 文件），装在仓库根 `.sfd-tools`（已加 .gitignore，不动全局环境）
- 实测：15 个真实页面扫出硬判 65 条、警告 199 条；抽查 5 组命中原文（`.text-white{color:#fff}`、三个 `<aside>` 无区分标签、图标按钮无可访问文本、缺 `type` 的按钮、重复 id）全部为真问题
- `no-inline-style` 由硬判降为 warn：动态宽度/进度条这类写法在真实项目里是常规手段（15 个页面里 197 条），硬判会淹没门禁；需要它计入失败时用 `--strict`
- 新增 `tests/test_structure_lint.py`（9 项）、`tests/test_render_probe.py` 增至 10 项（含黑字白底 |Lc|≈107.9、#767676 白底 ≈77.0 的参考值锚定）；`test_audit_gate_red.py` 增至 13 项
- 三种"看起来过了其实没测"的情形一律 exit 2：结构层没装、`--tools` 指错目录、stylelint/html-validate 规则名配错
- APCA 结果按 class 归并再报告：同一个真实页面初测 139 条逐元素警告，归并后 17 组（含"×36 处，最低 Lc=53.3"这类计数），否则警告会把整份审查报告淹掉
- 五个测试脚本的输出也统一强制 UTF-8（此前 FAIL 正文在中文 Windows 下显示为乱码）

## 2026-10-04 修复（版本号仍为 v2.7.0）
- 修正 critique 探测器规则条数标注：59 → 26（Verify 10 + Refuse 10 + 实现完整性 6）
- slop-test 补齐 V41 断号，清单为 56 条；SKILL.md / review / critique / README 的引用同步更新
- 调研轮数统一为 5 轮（research 正文已写第 1～第 5 轮，标题与入口文案此前仍写 4 轮）
- review 维度数标注 15 → 19；design 技术栈标注 10 → 14
- 修复 SKILL.md 中一处未换行的代码围栏，其后文档内容不再被渲染为代码块
- 接入 5 个此前未被引用的 Prompt 模板：react-tailwind / vue-nuxt / html-css / react-native / flutter
- 资源索引补入 references/typography.md、scripts/audit_integrity.py
- 移除 10 个 SKILL.md 的 `context: fork`，改为主上下文运行（fork 内无法取得用户回答）
- allowed-tools 补入 Task、Agent
- 新增 `scripts/audit_integrity.py` 结构自检门禁：引用断链、孤儿资源、条数对账、代码围栏配对、轮数一致性、工具许可
- README 修正：双代理 Assessment A/B 定义、反 AI 味规则的软/抛光条数、上游能力描述

## v2.7.0 (2026-08-10)
- 桌面端支持：Electron / Tauri / PySide6 / SwiftUI
- 新增 4 个参考文件：desktop-patterns / professional-software / motion-patterns / token-mapping
- 新增 4 个桌面 Prompt 模板：electron / tauri / pyside6 / swiftui

## v2.6.0 (2026-08-09)
- 新增 refine 子命令（polish / bolder / quieter / distill / harden）

## v2.5.0 (2026-08-09)
- 集成 GSAP 动效系统，增强双代理评估

## v2.4.0 (2026-08-08)
- GSAP 动效集成：动效库选择规则（Motion vs GSAP 场景表）
- GSAP 性能规范（transform优先/autoAlpha/stagger/prefers-reduced-motion）
- Step 2.5 GSAP 动效规划流程（design subskill）
- §2.19 GSAP 动效质量检查（10项）（review subskill）
- references/gsap-animation-guide.md（GSAP最佳实践参考文档）
- 5个prompt模板更新v2.4.0规范

## v2.3.0 (2026-08-08)
- hallmark 21种Macrostructure路由 + 20种Theme目录集成
- hallmark 57条Slop Test全面检查（§2.18升级）
- Pre-emit 6轴自评（Step 4.5）
- Macrostructure选择（Step 1.5）
- hallmark Study Verb（research skill）
- 斜体标题禁令（premium-rules #13）
- 侧边条纹卡片禁令（premium-rules #14）
- LCP优化规范（premium-rules #15）
- 间距4px倍数纪律（premium-rules #16）

## v2.2.0 (2026-08-04)
- 高级感设计规范（12条数值化规则）
- CSS 2026新特性指南
- Cult UI/Motion组件库集成
- 任意网站品牌Token提取
- §2.18高级感自动扫描

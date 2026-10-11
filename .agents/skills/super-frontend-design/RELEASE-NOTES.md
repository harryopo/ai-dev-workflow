# super-frontend-design Release Notes

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

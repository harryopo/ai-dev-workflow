v2.13.0 (2026-10-23)
- 状态契约落地（把"只能演示 happy path"变成可机检的失败）：
  - 新增 references/state-contract.md：页面级状态六种（loading/empty/error/success/no-permission/offline）+ 交互复杂度五档派生表 + 落地证据判据表 + static 豁免
  - research 第 3 轮问题 8 落成 pass-data `interaction-complexity` 字段（static/basic/moderate/complex/app 五档映射表）；Design Brief 交互需求段同步
  - design Step 1.5 后新增 Step 1.7「状态契约落地」（不可跳过）：3 条硬约束 + 派生表 + 5 条落地自检；Step 6 交付清单增状态契约项
  - review §0 检查表增 #14「状态覆盖完整性」并展开（脚本分工表 + 3 步判定 + 质量判据表）；评分 13 → 14 项；critique Assessment A + 命令行 + 报告模板同步
  - 主 SKILL.md 铁律 11 → 12 条（新增状态契约落地铁律，含 static 豁免）；§7.2 pass-data 增 interaction-complexity + states 字段
- 新增 scripts/state_check.py（第 9 道门禁）：声明与派生表一致性 + 每个声明的状态必须有实现证据；static 豁免；--complexity 取值越界 exit 2
- 新增 tests/test_state_check.py（20 项契约测试）
- 新增门禁 check_phase5_wiring：校验 6 处接线 + 五档派生表 + 三条失败规则（完整 "rule": "xxx" 形式）+ static 豁免分支；配 10 条 mutation；audit 检查项 49 → 50
- **修复 v2.12.0 遗留的载体口径不一致**：composition_check.py 此前只认 CSS 块注释，Tailwind / 单文件 HTML 项目（无独立 CSS 文件）必然误判为 composition-absent。现已支持 HTML 注释载体，与 signature_check 对齐；composition-contract.md §3.1 重写为"载体随项目形态"表；composition_check 契约测试 17 → 20 项
- 门禁数 8 → 9（SKILL.md §3.6 / §6 / §8 + design §16 四处表述同步）
- evals 38 → 44 条（v213-001~006：moderate 派生 / static 豁免 / complex 派生 / 状态审查 / 假声明 / app 全量五态）
- 版本号 2.12.0 → 2.13.0（SKILL.md frontmatter / evals.json / README 徽章三处同步）

v2.12.0 (2026-10-23)
- 构图契约落地（把视觉重心/节奏/密度纳入可追溯传递）：
  - 新增 references/composition-contract.md：构图六要素字段表（取值来源 + 为何不含 button）+ 视觉重心三级规则 + §3.2 落地判据表（标记 ≠ 声明就完事）
  - design Step 1.5 后新增 Step 1.6「构图契约落地」：3 条硬约束（六项全写 / 写进代码 /* composition: */ / 声明与实现一致）+ focus-hierarchy 三级判定表 + 同屏同级焦点 ≤ 1 + B 端默认 3 + 5 条落地自检
  - review §0 检查表增 #13「构图契约一致性」并展开（取声明 → 逐项对账 → 查焦点）；设计灵魂评分 12 → 13 项；critique Assessment A 增条目 + 报告模板增行
  - 主 SKILL.md 铁律 10 → 11 条（新增构图契约落地铁律）；§7.2 pass-data 增 macrostructure + composition 字段
- 新增 scripts/composition_check.py（第 8 道门禁）：校验 /* composition: */ 六要素齐全 / focus-hierarchy 取值合法 / 与 /* macrostructure: */ 戳记一致
- 新增 tests/test_composition_check.py（17 项契约测试）
- 新增门禁 check_phase4_wiring：校验 5 处接线 + 六要素字段齐全 + 缺要素/无戳记失败规则存在；配 6 条 mutation case；audit 检查项 48 → 49
- 门禁数 7 → 8（SKILL.md §3.6 / §6 / §8 + design §16 四处表述同步）
- evals 32 → 38 条（v212-001~006：构图落地 / 构图审查 / B端重心三级 / macrostructure 戳记 / 缺要素 / focus 取值越界）
- 版本号 2.11.0 → 2.12.0（SKILL.md frontmatter / evals.json / README 徽章三处同步）

v2.11.0 (2026-10-23)
- 签名机制落地（反模板的唯一肯定式检查，全流程五处接线）：
  - research 第 4 轮新增问题 12.5「签名线索」+ 强制推导表（线索类型 → 签名识别符形态 → 落点）；新增铁律 5「不允许零签名进入后续阶段」；Design Brief 增 signature-clues / signature-candidates 字段；快捷模式豁免表声明签名线索始终必问
  - creative §0.5 发散规格三件套 → 四件套（新增「签名识别符」）；新增签名硬门（签名落点相同 = 同一方向）；并置呈现格式增签名行；pass-data 落盘增 signature 字段
  - theme 步骤 1 增签名专属 Token 推导（增量、不覆盖主 Token、至少 1 个 --signature-*）
  - design Step 1 新增「签名落地」小节（3 条硬约束：标记注释必写 / 至少 1 处 / 可见性自检 + 落点选择表 + 落地自检清单）；设计灵魂检查清单增签名项
  - review §0 检查表增 #12「签名可识别性」并展开（取证 → 对照 → 代入三步法 + 与 #1–#11 的否定/肯定式对比）；设计灵魂评分 11 → 12 项；critique Assessment A 增签名条目 + 报告模板增行
- 新增 scripts/signature_check.py（第 7 道门禁）：统计 /* signature: */ 落点数量与可见性；零落点 / 全在低关注容器 / 首页无签名判失败；--require-marker 核对指定签名
- 新增 tests/test_signature_check.py（17 项契约测试）
- 新增门禁 check_phase3_wiring：校验 7 处接线 + 抽签脚本留痕字段 + 零落点失败规则存在 + 「灵魂验证问题」不得再是孤儿条款；audit 检查项 47 → 48
- 主 SKILL.md 铁律 9 → 10 条（新增签名落地铁律）；§3.6 与 §8 门禁数 6 → 7；§7.2 pass-data 增 signature 字段；§6 资源索引补新脚本与新测试
- references/anti-ai-slop.md「灵魂验证问题」由孤儿条款转为 review #12 的标准出处（明确移交关系）
- evals 26 → 32 条（v211-001~006：签名挖掘 / 签名落地 / 签名审查 / 用户答不出线索 / 重构通道 / 页脚落点）
- 版本号 2.10.0 → 2.11.0（SKILL.md frontmatter / evals.json / README 徽章三处同步）

v2.10.0 (2026-10-23)
- 参考机制 2.0 Phase 2 全部落地（方案书第三节 Phase 2 三项）：
  - P2-1 多方向强制发散：creative §0.5 新增「方向发散」章节（触发判定 / 发散规格 / 差异维度硬门 / 并置呈现格式 / 并行子代理 / 输出落盘）；design Step 1 新增「方向来源约束」（selected-direction 唯一依据，未选定则拒绝执行）
  - P2-2 二阶反射检查：review §0 检查表新增 #11 并展开判定方法（一阶 vs 二阶 + 典型二阶陷阱 + 与 #10 的区别）；critique Assessment A 评估方法与报告模板同步
  - P2-3 结构化随机兜底：research 新增「结构化随机兜底」章节；新增 scripts/random_draw.py（os.urandom 等概率 + 留痕输出，候选不足 2 个 exit 2）
- 新增 tests/test_random_draw.py（14 项契约测试）
- 主 SKILL.md 铁律 7 → 9 条（新增方向发散铁律 + 随机兜底铁律）；§3 creative 阶段补方向发散说明；§6 资源索引补新脚本与新测试
- evals 20 → 26 条（v210-001~006：C端发散 / 多方向规格 / 二阶反射 / 随机兜底 / B端跳过发散 / 沿用选定方向）
- 版本号 2.9.1 → 2.10.0（SKILL.md frontmatter / evals.json / README 徽章三处同步）

v2.9.1 (2026-10-23)
- 版本治理收口：9 个子技能 frontmatter 删除 version 字段（此前全部停在 2.7.0，主文件已 2.9.0），主 SKILL.md 成为唯一版本真值源
- 新增门禁 check_version_fields：子技能出现 version 即失败；主 SKILL.md / evals.json / README 徽章三处版本号必须一致
- Slop Test 口径补全：SKILL.md 索引行、§路由段、README 补写「56 条中可静态判定的部分由 slop_scan.py 执行，判定表见 rules/slop-table.json，其余人工核对」（此前关系仅写在 review §2.18，索引层读者看不到）
- audit_integrity 检查项 43 → 46
- 未实施：参考机制 2.0 Phase 2（多方向强制发散 / 二阶反射检查 / 结构化随机兜底），方案书已就绪，待 Phase 1 验收后执行

v2.9.0 (2026-10-16)
- 参考机制 2.0（去同质化 Phase 1）：参考维度追问 + 反参考字段（借 impeccable）+ 参考距离分级（自研：Operate 结构借鉴 / C 端原理解构外观原创）+ 反收敛样本池（跨领域 + 形态 archetype 表）+ 饱和赛道黑名单（references/saturated-lanes.md，review 检查 8→10 项）+ 情绪板强制参数推导
- 落点：research（第1/4轮 + 距离分级 + 提取 Step 0 + Brief 模板）、design（解构四步禁同层混合）、design-context（Anti-references section）、review（§0 #9/#10）、SKILL.md（术语表/pass-data/铁律 7）
- evals 16 → 20 条

v2.8.1 (2026-10-16)
- 现有风格重构流程（SKILL.md §3.6）：路由拆支（保持现有风格 vs 换新风格）+ research「现有风格审计模式」（门禁作审计器：token_lint / slop_scan 档位规则）+ 设计稿确认硬门（design-context 呈现 + design §0 `refactor-mode: style-audit` 前置）+ 风格固化询问 + 「项目设计规范优先」约束链（refine/theme 同步加前置检查）+ §0 边界澄清
- evals 13 → 16 条（v28-004/005/006）

v2.8.0 (2026-10-11)
- 字号层级与风格统一检查：stylelint strict-value 加 font-size；slop_scan 新增 font-size-step-count（阈值 8）与 radius-value-count（阈值 4），判定表 28 → 30 条；render_probe 量计算字号（font-scale-inverted / heading-body-ratio-low）；policy.json 政策 6 → 9 条
- review Typography 检查 T1–T8 → T1–T10（含 T2 阈值 48px → 32px 修正）
- B 端企业软件：新增 references/admin-enterprise-patterns.md；design 子技能新增 Part 17
- 专业软件分析 7 → 11 款（Trae / DaVinci Resolve / Blender / Warp）
- 内置设计系统预设：references/design-systems/ 四个（tdesign / ant-design / material-3 / shadcn-style），9-section 格式
- 组件库接入：design Part 7 新增国内企业级组件库小节（TDesign / Ant Design / Element Plus / Arco Design）
- 版本号升 v2.8.0

2026-10-11 对账（未升版本，仍为 v2.7.0）
- evals.json version 字段 2.4.0 → 2.7.0（与 SKILL.md frontmatter 对齐）
- design-002 全流程样本 expected_routing 补 research/design-context（原 creative→theme→design→review 违反「路由到 design 必先 research」铁律）
- 本日志补记 2026-10-05 两轮加固（此前只写了 RELEASE-NOTES.md，两份日志漂移）

2026-10-05 修复与门禁扩展（未升版本，仍为 v2.7.0）
- 新增 token_lint.py（Token 未定义引用/死 Token/与 DESIGN.md 双向对账）与 visual_diff.py（截图×参考图逐像素对账，含白屏检测）
- rules/policy.json 成为政策数字唯一真值源；audit_integrity.py 增加政策一致性对账
- 新增 structure_lint.mjs（stylelint+html-validate 真解析）与 apca_contrast.mjs（APCA Lc 用 colorjs.io 计算），依赖装在仓库根 .sfd-tools
- 新增 rules/gates.json 六道门禁清单与 gate-inventory 校验；no-inline-style 降为 warn；emoji-as-icon 改按 Unicode 区段判定
- slop_scan.py 支持 --only 单点复检与 --allow=RULE=理由；门禁与测试脚本输出强制 UTF-8；字体上限统一为默认两族

2026-10-04 修复（未升版本，仍为 v2.7.0）
- 数字对账：critique 探测器规则 59 → 实际 26 条（Verify 10 + Refuse 10 + 实现完整性 6）
- slop-test 补齐 V41 断号，清单改为 56 条，SKILL.md/review/critique/README 引用同步
- 调研轮数统一为 5 轮（正文实际写了第 1～第 5 轮，旧文案仍写 4 轮）
- review 维度数 15 → 19；design 技术栈 10 → 14
- SKILL.md 第 183 行畸形代码围栏修复（此前会让后半篇被当成代码块）
- 5 个从未被引用的 Prompt 模板（react-tailwind / vue-nuxt / html-css / react-native / flutter）接入 design 技术栈章节
- 资源索引补 references/typography.md 与 scripts/audit_integrity.py
- 移除全部 10 个 SKILL.md 的 `context: fork`（fork 内拿不到 AskUserQuestion 且只有约 10 turn，会静默截断）
- allowed-tools 补 Task、Agent（正文本就要求派发子代理）
- 新增 scripts/audit_integrity.py 结构门禁（断链/孤儿资源/数字对账/围栏配对/轮数一致性/工具许可）

v2.7.0 (2026-08-10)
- 桌面端支持：Electron / Tauri / PySide6 / SwiftUI
- 新增 4 个参考文件（desktop-patterns / professional-software / motion-patterns / token-mapping）
- 新增 4 个桌面 Prompt 模板（electron / tauri / pyside6 / swiftui）

v2.6.0 (2026-08-09)
- 新增 refine 子命令（polish / bolder / quieter / distill / harden）

v2.5.0 (2026-08-09)
- GSAP 动效系统集成，双代理评估增强

v2.4.0 (2026-08-08)
- GSAP 动效集成：动效库选择规则（Motion vs GSAP 场景表）
- GSAP 性能规范（transform优先/autoAlpha/stagger/prefers-reduced-motion）
- Step 2.5 GSAP 动效规划流程
- §2.19 GSAP 动效质量检查（10项）
- references/gsap-animation-guide.md（GSAP最佳实践参考文档）
- 5个prompt模板更新v2.4.0规范

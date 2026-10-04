# super-frontend-design Release Notes

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

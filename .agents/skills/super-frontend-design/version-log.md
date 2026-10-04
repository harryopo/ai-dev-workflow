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

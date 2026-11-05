# agent-memory · 三期路线图

> 配套 `方案书.md`（宪法）阅读。本文件回答"现在干什么、接下来干什么、最终去哪"。
> 最后更新：2026-10-24 · 当前所处：**近期 M1 待启动**

---

## 一、长远（1–3 年）：这个项目最终长成什么

**一句话**：成为"编码 agent 记忆模块"领域一个**被引用的设计参考**——论文有人引、比赛有人记得、自己开发 agent 时随手就用。

| 目标 | 形态 | 成功判据 |
|---|---|---|
| 论文 | arXiv → workshop → 主会（NeurIPS D&B / ACL demo 量级）的阶梯 | 至少一篇 workshop 级发表；arXiv 有外部引用 |
| 跨宿主记忆基础设施（次线） | MCP server：所有 agent 读写同一份记忆 | 3+ 宿主实测接入；super-memory 无感调用 |
| 开源资产 | core 库独立发布（与 super-memory 互相导流） | 有人 issue/star 的真实使用痕迹 |
| 个人复利 | 用户后续每个 agent 项目的记忆模块直接复用 | 新 agent 项目记忆模块搭建 < 1 天 |

**长远的唯一纪律**：主线（参考资产）永远优先于一切亮闪闪的机会——MCP、竞赛、论文都从 core 派生，不反过来。

## 二、中长远（3–6 个月）：手册、基准、竞赛、论文初稿

按依赖顺序（B 依赖 A 的产出）：

| # | 交付 | 内容 | 验收标准 | 依赖 |
|---|---|---|---|---|
| M2 | **注意事项手册** | docs/pitfalls/：dogfood 全部坑集结构化（追加式文件末尾读 / mtime 三角 / 内置提取共存 / 双 README 漂移 / CRLF 假断链 / 门禁连带 / 状态类小节过期……每条=现象+根因+解法+适用边界+事故日期） | ≥12 条目；新 agent 只读手册能避开已知坑 | M1（边做边记） |
| M3 | **算法文档** | docs/algorithms/：检索（BM25-lite+CJK 二元组）/ 巩固四操作 / §0 快照 / 寻址四层 / 体检五项——每篇含"为何这样设计+对比过的替代方案" | 6 篇齐；可独立阅读不依赖代码 | M1 |
| M4a | **基准实测** | eval/：接入 LongMemEval（或 LoCoMo），跑 super-memory/core 的量化数字，与 mem0/Letta 公开数字对比 | 有可引用的实测表 + 诚实差距分析 | M1 |
| M4b | **竞赛首战** | EverMind Memory Genesis（$80k，最对口）或 Devpost「Memories That Last」：core+壳出作品 | 完成提交（得奖是惊喜，完成作品是底线） | M1+M2 |
| M5a | **论文初稿** | paper/：方法论 + 实证（18 评测 + dogfood + M4 基准数字） | arXiv preprint 可发状态 | M3+M4a |
| M5b | workshop 投递 | 从 NeurIPS/ACL/ICLR 的 agent/memory workshop 择机投 | 投出（录用看天，投出靠自己） | M5a |

**触发条件（防提前优化）**：
- M4b 竞赛启动的触发：core 六模块全部带自测 + 手册 ≥8 条
- 次线 MCP 启动的触发：主线 M1–M3 全完成 + 用户当时仍有多宿主记忆孤岛痛感 + 当时宿主生态确认 MCP 是主流接法（2026-10 已是，但重判不亏）

## 三、近期（2–4 周）：M1 框架期——core/ 六模块

**目标**：`import agent_memory` 即用的最小核心库，全部从已验证逻辑迁入重构（不新发明）。

| 顺序 | 模块 | 从哪迁 | 接口草案（稳定面） | 自测 |
|---|---|---|---|---|
| 1 | `core/store.py` | 四套格式的读写规则（capture/knowledge-tiers/memory-addressing/handoff-template 的格式定义） | `read(fmt, path) -> Entry` · `write(fmt, path, entry)` · `validate(fmt, text) -> Errors`（fail-closed） | 每格式正反夹具：合法样例过、缺字段拒 |
| 2 | `core/retrieval.py` | super-memory/scripts/search.py（BM25-lite+CJK 二元组+标题加权） | `search(query, root, top) -> [Hit]` · `terms(text)` | 迁 selftest + 实仓冒烟 |
| 3 | `core/consolidate.py` | 四操作判定规则 + 失效标记三要素 + K-NNN 编号命令 | `decide(new, olds) -> Op(ADD/UPDATE/SUPERSEDE/NOOP)` · `apply(op)` 落盘 | 四操作各一夹具 |
| 4 | `core/snapshot.py` | §0 七槽位模板 + 刷新规则（先刷 §0 再追加编年） | `render(state) -> str`（§0 块） · `refresh(handoff_path, state)` | 七槽位齐全断言 |
| 5 | `core/doctor.py` | memory-doctor 五项检查命令 | `check(root) -> [Finding]`（类型/位置/处置建议） | 注入病灶夹具全检出 |
| 6 | `core/addressing.py` | 四层寻址 + glob 探测命令 + 多命中五步裁决 | `locate(workspace) -> MemoryLayout` | 假 HOME 沙箱夹具 |

**M1 全局约束**：
- 纯 Python 标准库（零依赖）；Python ≥3.9 兼容（用户环境教训）
- 每模块：接口 docstring + 自测（`python -m core.store` 可跑）+ 算法文档占位（M3 补全）
- 一个 `run_all_tests.py` 聚合入口（沿用 super-memory 惯例）
- **M1 完成定义**：六模块自测全绿 + README §0 快照更新为"M1 完成"

**M1 开工前置**（按用户"方案先行"规矩）：先出六模块的详细接口设计（签名/数据结构/错误语义）给用户批，批准后 TDD 式动工。

## 四、当前状态板（每次里程碑更新这里）

| 期 | 状态 | 完成日 |
|---|---|---|
| M0 方案书 v1 | ✅ | 2026-10-16 |
| M0+ 方案书 v2 / README / ROADMAP / 调研索引 | ✅ | 2026-10-24 |
| M1 core 框架 | ✅ 六模块自测 6/6 + 真实环境寻址冒烟通过 | 2026-10-31 |
| **项目暂停** | 用户转回 super-memory 主线；恢复入口见 README §0 | 2026-10-31 |
| M2 手册 | 未开始 | — |
| M3 算法文档 | 未开始 | — |
| M4 基准/竞赛 | 未开始 | — |
| M5 论文 | 未开始 | — |

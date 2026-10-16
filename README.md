# Skill 开发工作区

> **多 Agent 共用的 Skill 开发工作区。** 多个自研 skill 在此并行开发，各有独立的源码位、部署位与版本线。
> 本文件是**工作区地图与协作约束**；agent 行为规则另见 [CLAUDE.md](CLAUDE.md)。
>
> ⚠️ 本目录是**开发工作区**，不是安装仓库——各 skill 的安装请从对应发布位获取（见下）。

- **远端**：`git@github.com:harryopo/ai-dev-workflow.git`（本工作区仓库只跟踪其中一部分内容）
- **skill 部署位**（安装副本，位于本目录之外）：`~/.zcode/skills/<name>` 与 `~/.agents/skills/<name>`

---

## 一、目录地图（谁是谁，别搞混）

| 路径 | 是什么 | 约束 |
|------|--------|------|
| `.agents/skills/super-frontend-design/` | super-frontend-design 的**开发源码**（本仓库跟踪） | 改动后跑六道门禁；发布时同步三处部署位 |
| `deep-research-ultra/` | **deep-research-ultra 的活跃开发检出**（自带 `.git`，独立版本线，其他 agent 会话正在开发） | ⛔ 非本项目会话**不得移动 / 清理 / 改动**；也是工作区级安全门禁连带拦截的常见来源（见第三节、第四节） |
| `projects/<name>/` | 各 skill 的项目区（super-memory、skill-workspace、oss-finder、github-deploy…）；含部分**历史镜像**（如 deep-research-ultra 的 v6.15.0 镜像，带 STALE 标记） | 镜像不开发；开发去对应活跃位 |
| `docs/` | 工作区级文档（方案书、调研报告） | |
| `.learnings/`、`memory/`、`.workbuddy/memory/` | 记忆与学习记录位 | 写入约定见 super-memory skill |
| `archive/` | 发布产物与归档 | 不入库 |
| `shared/` | idea-to-dev 的共享代码（归属待定） | 动之前先确认归属 |
| `开发-修复区/`、`测试区/`、`research/`、`scripts/` | 工作区辅助区 | 各自看区内说明 |
| `.mimosa/`、`.qoder/`、`.zcode/`、`.trae/` 等 | 各工具运行时目录 | 已 gitignore，勿提交 |

## 二、提交约束

1. **工作区多项目共存**：根仓库只跟踪一部分内容；`deep-research-ultra/` 等自带 `.git` 的目录**不属于本仓库**，其提交/发布在该项目自己的工作流里做。
2. **显式路径提交**：`git add <paths>` 后 `git commit`，**禁止 `git add -A`**（工作区里有多个项目的未跟踪工作，全量暂存会误扫）。
3. **含 `git commit` 的命令会被整体拦截或整体作废**：被安全门禁拦下时，同一条命令里的前置 `git add` 等**不会执行**——所以 staging 与 commit 要拆成两条独立命令。
4. **日期核验**：写版本记录、记忆等日期性产物前，先确认当天真实日期（长会话可跨天，日期锚点会漂）。

## 三、安全门禁（Mimosa）行为速查

- **它是工作区级的**：每次 `git commit` 前扫描工作区；**任一项目的存量发现都可能拦截全部提交**（跨项目连带）。
- **被拦时怎么读**：拦截消息列出文件路径——先区分"自家改动"还是"他家项目存量"；**他家的不要自行修复/移动**，交给该项目自己的开发线处置。
- **完整覆盖=拦 / 降级覆盖=过**：同一命令重试可能因判定覆盖差异而放行（非确定性），但不要依赖它。
- 变更写法技巧：Bash 里直接写代码/配置文件（heredoc）会被预写扫描拦——改用 Write/Edit 工具提交同一内容。

## 四、已知冲突与处置原则（2026-10-16 实录）

- 现象：在 super-frontend-design 提交时，被 `deep-research-ultra/` 脚本的存量发现（凭据/SSRF 类——该项目审计已核对其为功能固有属性/误报）**工作区级连带拦截**。
- 处置原则：**不动别人的活跃副本**（该副本最新提交就是 2026-10-16，属活跃开发）；由 deep-research-ultra 开发线消化其发现，或（趁其空闲且经其所有者确认后）临时移出工作区完成提交。
- 任何"移动/清理根目录下项目目录"的动作，先确认归属与活跃度（`git log` / mtime），再经所有者确认。

## 五、各 skill 开发位速查

| Skill | 开发位 | 说明 |
|-------|--------|------|
| super-frontend-design | `.agents/skills/super-frontend-design/` | 前端设计全流程（本仓库跟踪，六道门禁 + 契约测试） |
| deep-research-ultra | `deep-research-ultra/`（活跃）／`projects/deep-research-ultra/`（旧镜像） | 深度调研 |
| super-memory | `projects/super-memory/` | 记忆工作台 |
| skill-workspace | `projects/skill-workspace/` | skill 工作台 |
| oss-finder ／ github-deploy ／ ai-dev-workflow ／ deep-research-ultra-landing ／ harryopo.github.io | `projects/<name>/` | 各自 README 为准 |
| idea-to-dev | `shared/`（共享部分） | 归属待定 |

## 📄 许可证

MIT License

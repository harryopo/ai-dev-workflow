# 项目记忆索引

> 此文件由 super-memory save 子命令维护，记录跨会话的关键知识和事实。

---

## 2026-06-24

### 高星开发类 Skill 安装完成

**背景**：调研后用户要求按推荐安装开发类 Skills，已完成 3 个高星项目的安装。

**已安装技能汇总**：

| 项目 | Stars | 安装技能数 | 核心能力 |
|------|-------|-----------|---------|
| mattpocock/skills | 140K | 21 | 工程纪律套装（TDD、QA、代码审查、PRD、架构审查等） |
| obra/superpowers | 29K | 12 | 完整开发方法论（规划、执行、TDD、调试、分支管理等） |
| context7 | 5K | 1 | 实时文档检索 |

**技术要点**：
- GitHub 国内访问受限，使用 `ghproxy.net` 镜像成功克隆
- 所有技能安装到 `.agents/skills/` 目录下
- 已配置 Git 全局镜像：`gitclone.com/github.com/` 作为 GitHub 替代方案

**用户交互习惯**：
- "嗯" = 认可；"按照推荐安装" = 确定执行
- 安装过程无需额外确认，直接执行
- 用户偏好先调研后行动

**相关文件**：
- `.learnings/LEARNINGS.md` — 详细条目
- `.agents/skills/mattpocock/` — 安装的技能目录
- `.agents/skills/obra/` — 安装的技能目录
- `.agents/skills/context7/` — 安装的技能目录

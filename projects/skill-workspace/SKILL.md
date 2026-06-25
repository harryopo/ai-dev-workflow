---
name: skill-workspace
description: |
  Skill 全生命周期工作台。当用户提到"skill工作台"、"管理skill"、"搜索skill"、
  "下载skill"、"优化skill"、"部署skill"、"合并skill"时触发。开发和审查功能由子技能处理。
  面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等），一站式完成 Skill 的
  搜索、下载、安全审查、开发生成、优化改进、质量测评、部署上线、合并整合、更新卸载。
argument-hint: "[子命令] [参数]"
context: fork
agent: general-purpose
allowed-tools: Read Write Edit Glob Grep Bash WebFetch
---

# Skill 全生命周期工作台

一站式 Skill 管理平台，覆盖 Skill 从发现到退役的完整生命周期。

## 核心原则

> **先检查环境，深入理解需求，全网搜索最佳方案，分阶段开发，循环审查，完整交付。**
>
> **用户在做任何有关 Skill 的事情时，都需要用 LLM 的能力进行对话提问，确保方案正确、方向越发清晰。**

## 子命令路由

| 子命令 | 说明 | 处理方式 |
|--------|------|----------|
| **开发** | 从零创建新 Skill（含需求深挖、全网搜索、方案推送、分阶段开发） | 加载 dev 子技能 |
| **合并** | 将多个相关 Skill 整合为一个更强大的 Skill | 本文件处理（流程七） |
| **审查** | 10 维度质量评分 | 加载 review 子技能 |
| **搜索** | 在线搜索可用 Skill | 本文件处理 |
| **下载** | 从 URL/名称/GitHub 安装 Skill | 本文件处理 |
| **安全审查** | 对 Skill 做安全扫描 | 本文件处理 |
| **优化** | 改进现有 Skill 质量 | 本文件处理 |
| **部署** | 安装到全局目录 | 本文件处理 |
| **管理** | 更新、卸载、列表 | 本文件处理 |

**路由规则：**
1. 用户说"开发xxx skill" → 加载 `subskills/dev/SKILL.md`
2. 用户说"审查skill" / "skill评分" → 加载 `subskills/review/SKILL.md`
3. 用户说"合并skill" / "整合skill" → 在本文件中执行流程七
4. 其他子命令 → 在本文件中处理

## 子技能加载

当路由到子技能时，使用 `Read` 工具加载对应的 SKILL.md：

```
开发 → Read ${SKILL_DIR}/subskills/dev/SKILL.md
审查 → Read ${SKILL_DIR}/subskills/review/SKILL.md
```

子技能是完整的包，有自己的 references 和 evals，可独立使用。

---

## 流程零：环境检查

**目标：** 在任何操作开始之前，确保执行环境正常、依赖完整、网络通畅、权限充足。

**原则：** 先检查，后执行。缺失依赖自动提示并提供安装方案。**先问清环境，再动手检查。**

**详细指南：** `${SKILL_DIR}/references/environment-check.md`

### 执行流程

```
第零步：环境问话（v5.1 新增）— 了解用户环境与偏好
  ↓
第一步：检查基础依赖是否安装
  ↓
第二步：检查环境变量是否配置
  ↓
第三步：检查网络是否通畅
  ↓
第四步：检查权限是否充足
  ↓
第五步：检查搜索增强 Skill 是否已安装
  ↓
生成环境检查报告 → 有缺失？→ 询问用户是否自动安装
```

### 第零步：环境问话

**目标：** 在动手检查前，先通过 LLM 对话了解用户的环境与偏好，避免盲目执行。

**必问清单（使用 AskUserQuestion 工具）：**

1. **操作系统与 Agent**
   - 问题：您当前使用什么操作系统和 Agent？
   - 选项：Windows + Claude Code / macOS + Claude Code / Linux + Codex CLI / 其他
   - 目的：确定依赖安装命令和全局 skills 路径

2. **网络环境**
   - 问题：您的网络环境是否能直接访问 GitHub/npm？
   - 选项：能直接访问 / 需要代理 / 使用镜像源 / 不确定
   - 目的：决定是否启用降级策略和镜像源

3. **已安装的搜索增强 Skill**
   - 问题：您是否已安装深度搜索相关 Skill？
   - 选项：deep-research-pro / multi-search-engine / 都安装了 / 都没安装
   - 目的：判断搜索能力范围

4. **操作偏好**
   - 问题：发现缺失依赖时，您希望？
   - 选项：自动安装 / 手动安装（提供命令）/ 跳过该依赖 / 询问后再决定
   - 目的：确定自动安装策略

**问话原则：**
- 根据用户回答动态调整后续问题
- 用户回答简短时主动追问细节
- 不假设用户环境，必须明确询问
- 问话完成后生成环境画像摘要，供后续流程引用

### 第一步：检查基础依赖

```bash
curl --version    # HTTP 客户端
git --version     # 版本控制
python --version  # Python 运行时
node --version    # Node.js 运行时
npm --version     # npm 包管理器
```

### 第二步：检查搜索增强 Skill

| Skill | 用途 | 检查方式 |
|-------|------|----------|
| deep-research-pro | 深度研究（16 搜索引擎） | 检查 SKILL.md 是否存在 |
| multi-search-engine | 多搜索引擎集成（16 引擎） | 检查 SKILL.md 是否存在 |

```bash
ls ~/.skills/deep-research-pro/SKILL.md 2>/dev/null && echo "已安装" || echo "未安装"
ls ~/.skills/multi-search-engine/SKILL.md 2>/dev/null && echo "已安装" || echo "未安装"
```

### 第三步：检查网络连通性

```bash
curl -s -o /dev/null -w "%{http_code}" https://github.com
curl -s -o /dev/null -w "%{http_code}" https://skillsmp.com
curl -s -o /dev/null -w "%{http_code}" https://registry.npmjs.org
```

### 环境检查报告格式

```
========================================
  环境检查报告
========================================

基础依赖:
  ✅ curl    — 已安装 (7.88.1)
  ✅ git     — 已安装 (2.39.2)
  ✅ python  — 已安装 (3.12.0)
  ✅ node    — 已安装 (20.11.0)
  ✅ npm     — 已安装 (10.2.0)

搜索增强 Skill:
  ✅ deep-research-pro   — 已安装
  ❌ multi-search-engine — 未安装

网络连通性:
  ✅ github.com    — HTTP 200
  ✅ skillsmp.com  — HTTP 200
  ❅ registry.npmjs.org — 超时

========================================
  发现 1 个缺失依赖，1 个网络问题
  是否自动安装缺失依赖？(y/n)
========================================
```

**生成环境检查报告**（v5.1 新增）→ 保存到 `./artifacts/env/env-check-{date}.md`

**环境检查报告模板：**

```markdown
# 环境检查报告

**检查时间：** {date}
**操作系统：** {os}
**Agent：** {agent}
**全局 skills 路径：** {path}

## 环境问话结果

| 问题 | 用户回答 |
|------|----------|
| 操作系统与 Agent | {answer} |
| 网络环境 | {answer} |
| 已安装搜索增强 Skill | {answer} |
| 操作偏好 | {answer} |

## 基础依赖检查

| 依赖 | 状态 | 版本 |
|------|------|------|
| curl | ✅ 已安装 | 7.88.1 |
| git | ✅ 已安装 | 2.39.2 |
| python | ✅ 已安装 | 3.12.0 |
| node | ❌ 未安装 | - |

## 搜索增强 Skill 检查

| Skill | 状态 |
|-------|------|
| deep-research-pro | ✅ 已安装 |
| multi-search-engine | ❌ 未安装 |

## 网络连通性检查

| 目标 | 状态 | HTTP 状态码 |
|------|------|-------------|
| github.com | ✅ 正常 | 200 |
| skillsmp.com | ✅ 正常 | 200 |
| registry.npmjs.org | ❌ 超时 | - |

## 问题汇总

1. {问题 1} — {解决方案}
2. {问题 2} — {解决方案}

## 下一步

- [ ] 用户确认安装方案
- [ ] 执行安装
- [ ] 重新检查
```

### 自动安装机制

- 用户确认 → 根据操作系统选择对应安装命令（详见 `environment-check.md`）
- 用户拒绝 → 输出手动安装指引，继续执行（跳过依赖功能）

**跨平台安装命令：**
- Windows: `winget install` 或 `choco install`
- macOS: `brew install`
- Linux: `apt install` / `yum install` / `dnf install`

**镜像源加速：**
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
npm config set registry https://registry.npmmirror.com
```

---

## 流程一：搜索 Skill

**目标：** 在线查找用户需要的 Skill（面向所有 Agent，不限于特定 Agent），避免重复造轮子。

**详细策略：** `${SKILL_DIR}/references/search-strategy.md`

### 搜索前问话

**目标：** 在搜索前通过 LLM 对话明确搜索意图，避免盲目搜索。

**必问清单（使用 AskUserQuestion 工具）：**

1. **使用场景**
   - 问题：您打算在什么场景下使用这个 Skill？
   - 选项：个人项目 / 团队协作 / 企业生产 / 学习研究
   - 目的：确定 Skill 的成熟度要求和功能范围

2. **技术栈偏好**
   - 问题：您有技术栈偏好吗？
   - 选项：Python / Node.js / Rust / Go / 无所谓
   - 目的：过滤搜索结果，提高匹配度

3. **功能优先级**
   - 问题：您最看重哪些功能？（可多选）
   - 选项：核心功能完整 / 易用性 / 性能 / 安全性 / 文档完善 / 社区活跃
   - 目的：排序搜索结果

4. **集成方式**
   - 问题：您希望如何集成？
   - 选项：直接安装使用 / 改造后使用 / 参考实现自己写 / 仅作调研
   - 目的：决定后续流程（安装/改造/开发）

**问话原则：**
- 用户回答简短时主动追问细节
- 根据用户回答动态调整搜索关键词
- 问话完成后生成搜索画像，供搜索策略参考

### 搜索源（按优先级）

**Tier 1：Skill 聚合市场（最优先）**

SkillsMP (skillsmp.com) — 1.5M+ skills，兼容所有 Agent（Claude Code、Codex CLI、ChatGPT 等）：
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q={关键词}&limit=10&sortBy=stars"
```
- 支持匿名访问（有每日速率限制）
- 可用参数：`category`（分类）、`occupation`（职业）、`page`、`limit`
- 返回：skill 名称、描述、GitHub 链接、stars

**Tier 2：Skills.sh 生态（CLI 工具）**
```bash
npx skills find {关键词}
```
- Skills.sh 是开源 Agent Skills 生态的包管理器
- 支持交互式搜索和关键词搜索
- 安装命令：`bash /path/to/skill/scripts/install-skill.sh <owner/repo@skill-name>`
- 检查更新：`npx skills check`
- 批量更新：`npx skills update`

**Tier 3：CocoLoop API**
```bash
curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"
```

**Tier 4：GitHub 搜索（含国内访问方案）**
```bash
curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"
```

**GitHub 国内访问降级策略：**
```
GitHub 直连 → 超时？
  ├── 尝试镜像站（github.moeyy.xyz / hub.fastgit.xyz / ghproxy.com）
  │   ├── 成功 → 使用镜像站
  │   └── 失败 ↓
  ├── 尝试 GitHub API（api.github.com，比网页更稳定）
  │   ├── 成功 → 使用 API
  │   └── 失败 ↓
  ├── 尝试代理（检测 $http_proxy / $https_proxy）
  │   ├── 成功 → 使用代理
  │   └── 失败 ↓
  └── 降级到 Tier 1-3 搜索源
```

**Tier 5：clawhub CLI（兜底）**
```bash
npx clawhub@latest search {关键词}
```

**Tier 6：深度搜索引擎（v4.0 新增）**

集成 deep-research-pro 和 multi-search-engine 两个增强搜索 Skill：

| Skill | 引擎数 | 适用场景 |
|-------|--------|----------|
| deep-research-pro | 16 个（含 7 个中文） | 深度调研、技术方案、最佳实践、学术研究 |
| multi-search-engine | 16 个（含抖音/B站等） | 通用搜索、中文内容、视频教程、行业分析 |

**调用方式：**

```
Skill: deep-research-pro
任务：调研 {关键词} 的最佳实践和现有方案

Skill: multi-search-engine
关键词：{关键词}
引擎：全部
```

**multi-search-engine 支持的引擎：**

| 类型 | 引擎 | 特点 |
|------|------|------|
| 国内 | 抖音、B站、知乎、掘金、CSDN、微信公众号、小红书 | 中文内容、视频教程 |
| 国际 | Google、GitHub、Stack Overflow、Reddit、Dev.to 等 | 技术文档、社区讨论 |

### 搜索策略

```
第一步：环境检查（流程零）
  ↓ 环境正常
第二步：SkillsMP API 搜索（覆盖面最广）
  ↓ 无结果或超时
第三步：npx skills find（Skills.sh 生态）
  ↓ 无结果或超时
第四步：CocoLoop API 搜索
  ↓ 无结果或超时
第五步：GitHub API 搜索（国内走降级策略）
  ↓ 无结果或超时
第六步：clawhub CLI 搜索
  ↓ 无结果
第七步：调用 deep-research-pro 深度搜索
  ↓ 无结果
第八步：调用 multi-search-engine 多引擎搜索
  ↓ 无结果
第九步：提示用户手动搜索或走「开发」流程
```

**输出格式：**
```
📋 搜索结果（来源：SkillsMP）:
  1. skill-name (⭐ 15.5k stars)
     📝 描述文本
     🔗 GitHub: https://github.com/xxx/xxx
  2. ...

🔍 深度搜索结果（来源：deep-research-pro）:
  1. 方案名称
     📝 描述文本
     📊 推荐度：⭐⭐⭐⭐⭐
```

**搜索后：**
- 展示结果列表，询问用户是否安装
- 如果都没找到 → 建议用户走「开发」流程
- **生成搜索结果报告**（v5.1 新增）→ 保存到 `./artifacts/search/search-results-{date}-{keyword}.md`

**搜索结果报告模板：**

```markdown
# 搜索结果报告

**搜索时间：** {date}
**搜索关键词：** {keyword}
**搜索源：** {sources}

## 搜索结果

### 结果 1: {name}
- **来源：** {source}
- **Stars：** {stars}
- **描述：** {description}
- **链接：** {url}

### 结果 2: {name}
...

## 搜索统计

| 来源 | 结果数 | 耗时 |
|------|--------|------|
| SkillsMP | {count} | {time} |
| Skills.sh | {count} | {time} |
| GitHub | {count} | {time} |

## 推荐

基于搜索结果，推荐以下方案：
1. {recommendation 1}
2. {recommendation 2}

## 下一步

- [ ] 用户选择方案
- [ ] 安全审查
- [ ] 安装/开发
```

---

## 流程二：下载/安装 Skill

**目标：** 从各种来源安全安装 Skill。

**支持的来源：**

| 来源 | 格式 | 处理方式 |
|------|------|----------|
| URL | `https://.../*.skill` | 直接下载 |
| 名称 | `skill-name` | 搜索 → 确认 → 安装 |
| GitHub | `owner/repo` | 克隆 → 检查 → 安装 |

### 安装前问话

**目标：** 在安装前通过 LLM 对话明确安装位置和版本，避免装错地方或装错版本。

**必问清单（使用 AskUserQuestion 工具）：**

1. **安装位置**
   - 问题：您希望安装到哪个位置？
   - 选项：全局目录（~/.skills/）/ 当前工作区（./）/ 项目级（.skills/）/ 其他
   - 目的：确定安装路径

2. **版本选择**
   - 问题：如果有多个版本，您希望？
   - 选项：最新稳定版 / 最新开发版 / 指定版本 / 不在意
   - 目的：确定下载哪个版本

3. **安装后操作**
   - 问题：安装完成后您希望？
   - 选项：立即测试 / 仅安装 / 安装并部署到其他 Agent / 安装并生成使用文档
   - 目的：确定安装后的流程

**问话原则：**
- 根据用户回答动态调整安装流程
- 用户不确定时提供推荐方案
- 问话完成后生成安装计划，供安装流程参考

**安装流程：**

1. **环境检查**（v4.0 新增）
   - 调用流程零检查基础依赖
   - 确保 curl/git 可用

2. **获取 Skill 内容**
   - URL → curl 下载
   - 名称 → 按搜索流程找到后下载
   - GitHub → git clone 或 curl 下载 SKILL.md
   - 国内环境 → 按 GitHub 降级策略获取

3. **安全审查**（强制）
   - 调用「安全审查」流程
   - 评级 ≥ B → 继续
   - 评级 ≤ C → 询问用户是否继续

4. **安装到工作区**
   ```bash
   # 安装到当前工作区（开发模式）
   cp -r {skill目录}/ "./{skill名}/"

   # 或安装到全局（使用模式）
   # 通用路径：~/.skills/{skill名}/
   cp -r {skill目录}/ ~/.skills/{skill名}/
   ```

5. **确认安装结果**

6. **生成安装报告**（v5.1 新增）→ 保存到 `./artifacts/install/install-report-{date}-{skill-name}.md`

**安装报告模板：**

```markdown
# 安装报告

**安装时间：** {date}
**Skill 名称：** {name}
**版本：** {version}
**来源：** {source}
**安装位置：** {path}

## 安装前问话结果

| 问题 | 用户回答 |
|------|----------|
| 安装位置 | {answer} |
| 版本选择 | {answer} |
| 安装后操作 | {answer} |

## 安装过程

| 步骤 | 状态 | 说明 |
|------|------|------|
| 环境检查 | ✅ 通过 | {details} |
| 获取内容 | ✅ 成功 | {details} |
| 安全审查 | ✅ 通过 | 评级：{rating} |
| 复制安装 | ✅ 完成 | {details} |
| 验证结果 | ✅ 成功 | {details} |

## 安装结果

- **安装路径：** {path}
- **文件数量：** {count}
- **总大小：** {size}
- **SKILL.md：** ✅ 存在 / ❌ 缺失

## 下一步

- [ ] 用户测试
- [ ] 部署到其他 Agent（如需要）
- [ ] 生成使用文档（如需要）
```

---

## 流程三：安全审查

**目标：** 对 Skill 进行安全扫描，识别风险。整合 skill-vetter 的 4 步审查协议。

### 审查前问话

**目标：** 在审查前通过 LLM 对话明确审查重点和风险容忍度，避免一刀切。

**必问清单（使用 AskUserQuestion 工具）：**

1. **审查重点**
   - 问题：您最关心哪些安全方面？（可多选）
   - 选项：敏感数据泄露 / 危险命令执行 / 网络访问 / 权限范围 / 全部检查
   - 目的：确定审查重点

2. **风险容忍度**
   - 问题：您的风险容忍度？
   - 选项：严格（任何 WARNING 都拒绝）/ 标准（仅 BLOCK 拒绝）/ 宽松（仅提示不拒绝）
   - 目的：确定审查结论的标准

3. **使用环境**
   - 问题：这个 Skill 将在什么环境使用？
   - 选项：个人开发机 / 团队共享 / 企业生产 / 沙盒环境
   - 目的：根据环境调整风险等级

4. **已知问题**
   - 问题：您是否已经知道这个 Skill 有哪些安全问题？
   - 选项：无 / 有（请描述）/ 不确定
   - 目的：重点关注用户已知的问题

**问话原则：**
- 根据用户回答动态调整审查重点
- 用户不确定时提供标准审查方案
- 问话完成后生成审查计划，供审查流程参考

**审查协议（4 步）：**

### 第 1 步：元数据检查
- [ ] `name` 与预期 skill 名称匹配（无 typosquatting）
- [ ] `version` 遵循语义化版本号
- [ ] `description` 清晰且与实际行为一致
- [ ] `author` 可识别

### 第 2 步：权限范围分析

| 权限 | 风险等级 | 说明 |
|------|----------|------|
| Read | Low | 几乎总是合法的 |
| Write | Medium | 必须说明写入哪些文件 |
| Network | High | 必须说明访问哪些端点 |
| Shell/Bash | Critical | 必须说明执行哪些命令 |

**⚠️ 危险组合：** `network` + `shell` 同时出现 → 可能导致数据泄露

### 第 3 步：内容扫描

**🔴 BLOCK（阻止安装）：**
- 引用 `~/.ssh`、`~/.aws`、`~/.env` 等敏感路径
- 使用 `curl`、`wget`、`nc`、`bash -i` 等命令
- `base64` 混淆内容
- 禁用安全机制
- 未知或可疑 URL

**⚠️ WARNING（需要审查）：**
- `/**/*` 等宽泛通配符
- `sudo` 使用
- 潜在的提示注入

**ℹ️ INFO（信息）：**
- 缺少 description/version/author

### 第 4 步：Typosquat 检测
- 检查单字符交换（如 `skil` vs `skill`）
- 检查同形异义字符（如 `l/1`、`O/0`）
- 检查多余连字符（如 `skill--name`）

**输出格式：**
```
安全审查报告
============
Skill: {name}
安全评级: SAFE / WARNING / DANGER / BLOCK
风险标记: {数量}
建议: install / sandbox first / do not install

详细发现:
- 元数据: ✅ 正常 / ⚠️ 问题描述
- 权限: ✅ 最小权限 / ⚠️ 过度权限
- 内容: ✅ 无风险 / ⚠️ 风险项列表
- Typosquat: ✅ 无 / ⚠️ 可疑命名
```

**生成安全审查报告**（v5.1 新增）→ 保存到 `./artifacts/reviews/security-review-{date}-{skill-name}.md`

**安全审查报告模板：**

```markdown
# 安全审查报告

**审查时间：** {date}
**Skill 名称：** {name}
**Skill 路径：** {path}
**安全评级：** {SAFE / WARNING / DANGER / BLOCK}

## 审查前问话结果

| 问题 | 用户回答 |
|------|----------|
| 审查重点 | {answer} |
| 风险容忍度 | {answer} |
| 使用环境 | {answer} |
| 已知问题 | {answer} |

## 审查发现

### 元数据检查
- [✅ / ⚠️] name 匹配预期名称
- [✅ / ⚠️] version 遵循 semver
- [✅ / ⚠️] description 清晰且与实际行为一致
- [✅ / ⚠️] author 可识别

### 权限范围分析
| 权限 | 风险等级 | 是否使用 | 说明 |
|------|----------|----------|------|
| Read | Low | {是/否} | {说明} |
| Write | Medium | {是/否} | {说明} |
| Network | High | {是/否} | {说明} |
| Shell/Bash | Critical | {是/否} | {说明} |

### 内容扫描
| 级别 | 发现项 | 说明 |
|------|--------|------|
| 🔴 BLOCK | {count} | {details} |
| 🟡 WARNING | {count} | {details} |
| ℹ️ INFO | {count} | {details} |

### Typosquat 检测
- [✅ / ⚠️] 无单字符交换
- [✅ / ⚠️] 无同形异义字符
- [✅ / ⚠️] 无多余连字符

## 风险汇总

| 风险等级 | 数量 | 建议 |
|----------|------|------|
| 🔴 BLOCK | {count} | 必须修复才能安装 |
| 🟡 WARNING | {count} | 建议修复后安装 |
| ℹ️ INFO | {count} | 可忽略 |

## 审查结论

**评级：** {SAFE / WARNING / DANGER / BLOCK}
**建议：** {install / sandbox first / do not install}
**理由：** {说明}

## 下一步

- [ ] 用户确认处理方式
- [ ] 修复风险项（如需要）
- [ ] 重新审查（如修复后）
- [ ] 继续安装流程（如通过）
```

**参考：** 如果 skill-vetter 已安装，可参考其详细审查协议

---

## 流程四：优化 Skill

**目标：** 改进现有 Skill 的质量，解决具体问题。

**优化触发信号：**
- 用户说"这个 skill 不好用"
- 测评发现的问题需要修复
- 用户想增加新功能或改进行为

### 优化前问话

**目标：** 在优化前通过 LLM 对话明确优化目标和优先级，避免盲目优化。

**必问清单（使用 AskUserQuestion 工具）：**

1. **优化目标**
   - 问题：您希望优化哪些方面？（可多选）
   - 选项：触发精准度 / 指令明确性 / 输出质量 / 性能 / 安全性 / 易用性 / 其他
   - 目的：确定优化重点

2. **具体问题**
   - 问题：您遇到的具体问题是什么？
   - 选项：开放式问题，让用户描述具体问题
   - 目的：了解真实痛点

3. **优化优先级**
   - 问题：如果时间有限，您希望优先解决？
   - 选项：最严重的问题 / 最容易解决的问题 / 影响最大的问题 / 全部解决
   - 目的：确定优化顺序

4. **优化约束**
   - 问题：优化有哪些约束？
   - 选项：不能改变触发词 / 不能增加文件大小 / 不能改变输出格式 / 无约束
   - 目的：避免破坏性优化

5. **验收标准**
   - 问题：优化完成后如何验收？
   - 选项：Darwin 评分提升 / 用户实际测试 / evals 通过 / 多评委审查
   - 目的：确定验收方式

**问话原则：**
- 根据用户回答动态调整优化方案
- 用户不确定时基于诊断结果推荐优化方向
- 问话完成后生成优化计划，供优化流程参考

**优化流程：**

1. **诊断** — 先用「审查」流程找出问题
2. **制定方案** — 按优先级排列改进项
3. **执行改进**
   - description 不准 → 改触发词，补正例/反例
   - workflow 有漏洞 → 补步骤，加检查点
   - 输出不合格 → 改格式，补样例
   - 误触发 → 收窄触发条件
4. **验证** — 用同一个 case 跑一遍，确认改善
5. **回归** — 用 evals 重跑，确保没引入新问题
6. **生成优化报告**（v5.1 新增）→ 保存到 `./artifacts/optimize/optimize-report-{date}-{skill-name}.md`

**棘轮优化机制**

优化循环采用棘轮机制，确保质量只升不降：
- 每轮优化后必须通过量化评估（评分 ≥ 上一轮）
- 若本轮评分 < 上一轮，立即自动回滚
- 连续 2 轮 Δ < 2 分时自动停止优化
- 优化后文件大小 ≤ 原始大小 × 1.5

**详细指南：** `${SKILL_DIR}/references/ratchet-mechanism.md`

**多评委独立评估**

采用多评委独立评估机制，避免 LLM 自评偏差：
- 每轮启动至少 2 个独立评委 agent
- 评委不复用，下一轮重新 spawn
- 至少 2 个评委共识才有效
- 子 agent 不可用时自动切换到干跑模式

**详细指南：** `${SKILL_DIR}/references/multi-judge.md`

**优化报告模板：**

```markdown
# 优化报告

**优化时间：** {date}
**Skill 名称：** {name}
**优化前版本：** {version}
**优化后版本：** {new_version}

## 优化前问话结果

| 问题 | 用户回答 |
|------|----------|
| 优化目标 | {answer} |
| 具体问题 | {answer} |
| 优化优先级 | {answer} |
| 优化约束 | {answer} |
| 验收标准 | {answer} |

## 诊断结果

### Darwin 9 维度评分（优化前）

| 维度 | 评分 | 满分 | 问题 |
|------|------|------|------|
| D1 结构完整性 | {分} | 10 | {problem} |
| D2 指令具体性 | {分} | 10 | {problem} |
| ... | ... | ... | ... |
| **总分** | **{分}** | **100** | - |

### 主要问题

1. {问题 1} — 严重程度：{高/中/低}
2. {问题 2} — 严重程度：{高/中/低}

## 优化方案

| 优先级 | 问题 | 优化措施 | 预期效果 |
|--------|------|----------|----------|
| P0 | {问题} | {措施} | {effect} |
| P1 | {问题} | {措施} | {effect} |
| P2 | {问题} | {措施} | {effect} |

## 优化执行

### 轮次 1
- **变更内容：** {changes}
- **变更前评分：** {score}
- **变更后评分：** {score}
- **决策：** {通过 / 回滚}
- **理由：** {reason}

### 轮次 2
...

## 优化结果

### Darwin 9 维度评分（优化后）

| 维度 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| D1 结构完整性 | {分} | {分} | {+/-} |
| D2 指令具体性 | {分} | {分} | {+/-} |
| ... | ... | ... | ... |
| **总分** | **{分}** | **{分}** | **{+/-}** |

### 棘轮机制验证
- [ ] 评分 ≥ 上一轮 ✅
- [ ] 文件大小 ≤ 原始 × 1.5 ✅
- [ ] 无反例黑名单触发 ✅

### 多评委评估
- 评委 A：{分}
- 评委 B：{分}
- 共识状态：{达成 / 仲裁}
- 最终得分：{分}

## 验收结果

| 验收项 | 状态 | 说明 |
|--------|------|------|
| Darwin 评分提升 | ✅ / ❌ | {details} |
| 用户实际测试 | ✅ / ❌ | {details} |
| evals 通过 | ✅ / ❌ | {details} |
| 多评委审查 | ✅ / ❌ | {details} |

## 下一步

- [ ] 用户确认优化结果
- [ ] 部署到全局（如需要）
- [ ] 继续优化（如未达标）
```

---

## 流程五：部署

**目标：** 将本地测试通过的 Skill 安装到全局目录。

### 部署前问话

**目标：** 在部署前通过 LLM 对话明确部署目标和验证方式，避免部署错误。

**必问清单（使用 AskUserQuestion 工具）：**

1. **目标 Agent**
   - 问题：您要部署到哪个 Agent？
   - 选项：Claude Code / TRAE / 两者都部署 / Codex CLI / Cursor / 通用（~/.skills/）
   - 目的：确定部署路径

2. **部署范围**
   - 问题：您希望部署哪些内容？
   - 选项：仅 SKILL.md / 完整 skill 包（含 references）/ 完整包 + 子技能 / 自定义
   - 目的：确定复制范围

3. **已有版本处理**
   - 问题：如果目标位置已有同名 Skill？
   - 选项：覆盖（备份旧版）/ 覆盖（不备份）/ 跳过 / 询问后决定
   - 目的：避免覆盖重要文件

4. **部署后验证**
   - 问题：部署后如何验证？
   - 选项：仅检查文件存在 / 运行 evals / 实际任务测试 / 多评委审查
   - 目的：确定验证方式

**问话原则：**
- 根据用户回答动态调整部署流程
- 用户不确定时提供推荐方案
- 问话完成后生成部署计划，供部署流程参考

**全局目录路径：**

| 平台 | 全局目录 | 说明 |
|------|----------|------|
| Claude | `.agents/skills/` | Claude Code 的全局 skills 目录 |
| TRAE | `.trae/skills/` | TRAE 的全局 skills 目录 |

**部署流程：**

1. **环境检查** — 调用流程零，确保目标目录可写
2. **确认来源** — 工作区中的哪个 skill 目录
3. **检查是否通过测评** — 建议先走「审查」流程
4. **部署到 Claude 全局目录**
   ```powershell
   Copy-Item -Path "projects\{skill名}" -Destination ".agents\skills\{skill名}" -Recurse -Force
   ```
5. **部署到 TRAE 全局目录**
   ```powershell
   Copy-Item -Path "projects\{skill名}" -Destination ".trae\skills\{skill名}" -Recurse -Force
   ```
6. **验证部署**
   ```powershell
   # 检查 Claude 目录
   ls .agents\skills\{skill名}\
   # 检查 TRAE 目录
   ls .trae\skills\{skill名}\
   ```
7. **测试全局可用** — 使用 Agent CLI 验证

**⚠️ 永远用 `cp`/`Copy-Item`，不用 `mv`，保留源文件。**

**⚠️ 如果 Copy-Item 被路径安全策略阻止，使用 robocopy 作为替代方案。**

---

## 流程六：管理

**目标：** 管理已安装的 Skill。

### 管理前问话（v5.1 新增）

**目标：** 在执行管理操作前通过 LLM 对话明确操作意图，避免误操作。

**必问清单（使用 AskUserQuestion 工具）：**

1. **操作类型**
   - 问题：您想执行什么操作？
   - 选项：列出已安装 / 更新单个 / 批量更新 / 检查更新 / 卸载 / 查看详情
   - 目的：确定操作类型

2. **操作范围**（根据操作类型动态调整）
   - 列出：问题：列出范围？选项：全局 / 项目级 / 全部
   - 更新：问题：更新哪个 Skill？选项：指定名称 / 全部 / 按条件筛选
   - 卸载：问题：卸载哪个 Skill？选项：指定名称 / 多个 / 按条件筛选

3. **操作确认**（针对危险操作）
   - 问题：您确认要执行此操作吗？
   - 选项：确认执行 / 取消 / 先查看影响范围
   - 目的：防止误操作

**问话原则：**
- 危险操作（卸载、批量更新）必须二次确认
- 用户不确定时先展示影响范围再询问
- 问话完成后生成操作计划，供管理流程参考

### 列出已安装 Skill
```bash
# 通用路径：~/.skills/
ls ~/.skills/
ls ./
```

### 更新 Skill

**单个更新：**
1. 查询最新版本（SkillsMP API、CocoLoop API 或 GitHub）
2. 比较本地版本与远程版本
3. 有更新 → 备份旧版 → 下载新版 → 安全审查 → 安装

**批量更新（如 find-skills 已安装）：**
```bash
npx skills update
```
- 检查所有已安装 skills 的更新
- 自动更新到最新版本

**检查更新：**
```bash
npx skills check
```

### 卸载 Skill
1. 确认 skill 存在
2. 询问用户确认
3. 删除 skill 目录
4. 清理相关配置

---

## 流程七：合并 Skill

**目标：** 将多个相关 Skill 整合为一个更强大、更完整的 Skill。

**详细指南：** `${SKILL_DIR}/references/merge-workflow.md`

### 合并目标

1. **消除冗余** — 减少功能重叠，降低维护成本
2. **增强能力** — 集成多个 Skill 的优点，形成更强功能
3. **优化体验** — 统一触发条件和输出规范，减少用户困惑
4. **解决问题** — 修复原 Skill 的痛点和缺陷
5. **优化提示词** — 提升触发精准度和指令明确性（v5.1 新增）
6. **优化子技能调用** — 提升调用效率和错误处理（v5.1 新增）
7. **优化用户体验** — 降低使用门槛，提升易用性（v5.1 新增）

### 合并流程

```
第一步：深度分析原 Skill（v5.1 新增）
  ↓ 全面深入理解每个原 skill 的设计理念、核心功能和优化空间
  ↓ 分析功能清单、架构设计、提示词质量、子技能调用工程、优化空间
  ↓ **生成深度分析报告**（v5.1 新增）→ 保存到 `./artifacts/analysis/deep-analysis-{date}-{skill-names}.md`
第二步：审查原 Skill
  ↓ 调用 review 子技能，对每个原 Skill 进行 Darwin 9 维度打分
第三步：理解原 Skill
  ↓ 基于深度分析，理解核心价值、用户场景、使用频率、依赖关系
第四步：询问用户
  ↓ 明确合并方向：保留优点、解决痛点、新增需求、优先级、使用场景、用户群体、成功标准
第五步：网上调研
  ↓ 使用 multi-search-engine 搜索最佳实践、踩坑经验、竞品分析、用户反馈
  ↓ **生成调研报告**（v5.1 新增）→ 保存到 `./artifacts/research/research-report-{date}-{topic}.md`
第六步：综合优化
  ↓ 设计合并方案：保留优点、解决痛点、集成新功能、简化结构、优化提示词、优化子技能调用、优化用户体验
  ↓ **生成合并方案**（v5.1 新增）→ 保存到 `./artifacts/merge/merge-proposal-{date}-{skill-names}.md`
第七步：正常工作流
  ↓ 按标准流程分阶段开发合并后的 Skill
第八步：用户确认
  → 每个阶段完成后都需要用户确认
```

### 合并确认清单

每个阶段完成后都需用户确认：
- [ ] 深度分析结果准确
- [ ] 审查结果准确
- [ ] 理解正确
- [ ] 需求完整
- [ ] 调研结果可用
- [ ] 合并方案满意
- [ ] 提示词优化方案可行
- [ ] 子技能调用优化方案可行
- [ ] 用户体验优化方案可行
- [ ] 最终成果符合预期

### 合并方案文档模板

```markdown
# Skill 合并方案

## 背景
- 合并原因：[说明]
- 原 Skill 列表：[skill A]、[skill B]、[skill C]

## 深度分析结果（v5.1 新增）
- 功能清单对比：[各 skill 功能对比表]
- 架构设计对比：[各 skill 架构对比表]
- 提示词质量对比：[各 skill 提示词质量对比表]
- 子技能调用对比：[各 skill 子技能调用对比表]
- 优化空间汇总：[各 skill 优化空间汇总表]

## 审查结果
[各 Skill Darwin 9 维度评分对比表]

## 用户需求
- 必须保留：[功能列表]
- 必须解决：[问题列表]
- 新增需求：[需求列表]
- 使用场景：[典型使用场景]
- 用户群体：[目标用户]
- 成功标准：[合并成功的判断标准]

## 调研结果
- 最佳实践：[最佳实践]
- 踩坑经验：[踩坑经验]
- 竞品分析：[竞品分析]
- 用户反馈：[用户反馈]

## 合并方案
- 触发条件：[统一后的触发条件]
- 工作流程：[合并后的工作流程]
- 输出规范：[统一后的输出规范]
- 提示词优化方案：[说明如何优化提示词]（v5.1 新增）
- 子技能调用优化方案：[说明如何优化子技能调用]（v5.1 新增）
- 用户体验优化方案：[说明如何优化用户体验]（v5.1 新增）
```

---

## 工作产物管理

**目标：** 所有调研分析、全文搜集、方案推送等工作流都必须生成 md 文件，以便引用、参考、优化和追溯。

**详细指南：** `${SKILL_DIR}/references/artifacts.md`

### 产物类型

| 产物类型 | 生成时机 | 文件命名 | 存放位置 |
|----------|----------|----------|----------|
| 环境检查报告 | 环境检查完成后 | `env-check-{date}.md` | `./artifacts/env/` |
| 搜索结果报告 | 搜索 Skill 完成后 | `search-results-{date}-{keyword}.md` | `./artifacts/search/` |
| 安装报告 | 安装完成后 | `install-report-{date}-{skill-name}.md` | `./artifacts/install/` |
| 安全审查报告 | 安全审查完成后 | `security-review-{date}-{skill-name}.md` | `./artifacts/reviews/` |
| 优化报告 | 优化完成后 | `optimize-report-{date}-{skill-name}.md` | `./artifacts/optimize/` |
| 部署报告 | 部署完成后 | `deploy-report-{date}-{skill-name}.md` | `./artifacts/deploy/` |
| 管理操作报告 | 管理操作完成后 | `manage-report-{date}-{operation}.md` | `./artifacts/manage/` |
| 深度分析报告 | 深度分析原 Skill 完成后 | `deep-analysis-{date}-{skill-names}.md` | `./artifacts/analysis/` |
| 调研报告 | 全网调研完成后 | `research-report-{date}-{topic}.md` | `./artifacts/research/` |
| 方案文档 | 方案推送完成后 | `proposal-{date}-{feature}.md` | `./artifacts/proposals/` |
| 合并方案 | 合并方案设计完成后 | `merge-proposal-{date}-{skill-names}.md` | `./artifacts/merge/` |
| 审查报告 | 审查评分完成后 | `review-report-{date}-{skill-name}.md` | `./artifacts/reviews/` |

### 产物目录结构

```
./artifacts/
├── env/                 # 环境检查报告
├── search/              # 搜索结果报告
├── install/             # 安装报告
├── reviews/             # 审查报告（含安全审查）
├── optimize/            # 优化报告
├── deploy/              # 部署报告
├── manage/              # 管理操作报告
├── analysis/            # 深度分析报告
├── research/            # 调研报告
├── proposals/           # 方案文档
└── merge/               # 合并方案
```

### 必须生成产物的流程

以下流程**必须**生成 md 文件：
1. **环境检查**（流程零）→ 环境检查报告
2. **搜索 Skill**（流程一）→ 搜索结果报告
3. **安装 Skill**（流程二）→ 安装报告
4. **安全审查**（流程三）→ 安全审查报告
5. **优化 Skill**（流程四）→ 优化报告
6. **部署 Skill**（流程五）→ 部署报告
7. **管理 Skill**（流程六）→ 管理操作报告
8. **深度分析原 Skill**（流程七第一步）→ 深度分析报告
9. **网上调研**（流程七第五步）→ 调研报告
10. **合并方案设计**（流程七第六步）→ 合并方案
11. **审查评分**（review 子技能）→ 审查报告

### 产物生成规则

1. **自动创建目录** — 生成产物前，自动创建目录（如果不存在）
2. **命名规范** — `{类型}-{date}-{关键词}.md`
3. **产物引用** — 后续流程引用前序产物时，使用相对路径
4. **产物更新** — 如果同一主题的产物已存在，询问用户处理方式

### 产物使用流程

```
第一步：执行工作流（搜索/分析/调研/方案）
  ↓
第二步：生成产物 md 文件
  ↓
第三步：展示产物摘要给用户
  ↓
第四步：用户确认产物内容
  ↓
第五步：保存产物到 artifacts/ 目录
  ↓
第六步：后续流程引用产物
```

---

## 上下文管理

**详细指南：** `${SKILL_DIR}/references/context-management.md`

### 核心原则

- **主动规划优先** — 任何任务开始前，先生成明确的执行计划
- **阶段性记忆** — 将长任务分解为阶段，每个阶段独立保存关键信息
- **智能压缩** — 当上下文过长时，自动压缩而非丢失信息
- **可追溯性** — 任何决策和完成状态都应有据可查

### Plan 机制

**开始前：** 生成结构化任务计划（目标、拆解、依赖、风险、成功标准）

**执行中：** 每个阶段完成时保存阶段记忆（完成状态、关键输出、关键决策、下阶段输入）

**压缩触发条件：**
- 对话轮次 > 20 轮
- 估算 token 数 > 80% 上下文窗口
- 用户明确要求"继续"或"下一步"时检查

**压缩公式：**
```
压缩后上下文 = 
  最近 5 轮完整对话 +
  所有阶段记忆摘要（每个阶段 ≤ 200 字）+
  当前任务计划 +
  待完成任务列表 +
  关键决策索引
```

---

## 参考资料

**本工作台：**
- 需求深挖指南：`${SKILL_DIR}/references/requirements.md`
- 搜索策略指南：`${SKILL_DIR}/references/search-strategy.md`
- 方案推送模板：`${SKILL_DIR}/references/proposal-template.md`
- 优化方法：`${SKILL_DIR}/references/optimize.md`
- 部署指南：`${SKILL_DIR}/references/deploy.md`
- 合并流程：`${SKILL_DIR}/references/merge-workflow.md`
- 上下文管理：`${SKILL_DIR}/references/context-management.md`
- 环境检查：`${SKILL_DIR}/references/environment-check.md`
- Darwin 评估体系：`${SKILL_DIR}/references/darwin-rubric.md`
- 棘轮机制：`${SKILL_DIR}/references/ratchet-mechanism.md`
- 多评委评估：`${SKILL_DIR}/references/multi-judge.md`
- 反例黑名单：`${SKILL_DIR}/references/anti-patterns.md`
- Agent 中立指南：`${SKILL_DIR}/references/agent-neutral-guide.md`
- 工作产物管理：`${SKILL_DIR}/references/artifacts.md`

**子技能：**
- 开发子技能：`${SKILL_DIR}/subskills/dev/SKILL.md`
- 审查子技能：`${SKILL_DIR}/subskills/review/SKILL.md`

**全局技能（如已安装）：**
- find-skills — Skills.sh 生态搜索
- skill-creation-guide — Anthropic 官方创建指南（含 init_skill.py、package_skill.py）
- skill-vetter — 安全审查协议
- cocoloop — CocoLoop Skill 管理器
- deep-research-pro — 深度研究（16 搜索引擎）
- multi-search-engine — 多搜索引擎集成（16 引擎）

**注意：** 全局技能的安装路径统一为 `~/.skills/`。

## 注意事项

### 必须遵守
- 执行前先做环境检查（流程零）
- **每个流程开始前必须通过 LLM 对话问话明确用户意图**（v5.1.1 新增）
- **每个流程完成后必须生成对应的产物 md 文件**（v5.1.1 新增）
- 深入理解需求，不要只问几个表面问题
- 全网搜索（含 deep-research-pro 和 multi-search-engine），不要自己造轮子
- 分阶段开发，每个阶段都审查打分
- 循环返工，分数低就返工，直到达标
- 完整交付，生成完整 skill 包
- 下载前必须做安全审查
- 部署前建议做质量测评
- 永远用 cp 不用 mv
- 用 AskUserQuestion 与用户交互
- 长对话时主动触发上下文压缩，降低幻觉
- 合并 Skill 时每个阶段都要用户确认
- 优化时采用棘轮机制，确保质量只升不降
- 评估时采用多评委独立审查，避免自评偏差
- 对照反例黑名单检查，避免常见反模式

### 禁止行为
- 跳过环境检查直接执行
- **跳过 LLM 对话问话直接执行**（v5.1.1 新增）
- **跳过产物 md 文件生成**（v5.1.1 新增）
- 跳过需求深挖直接开发
- 跳过全网搜索直接开发
- 跳过审查打分直接交付
- 跳过安全审查直接部署
- 未测试就部署到全局
- 覆盖用户未确认的文件
- 静默执行危险操作
- 合并时假设用户意图而不确认
- 同 context 自评自改（AP-01）
- git reset --hard 当回滚（AP-02）
- 为凑分增冗余（AP-03）
- 跳过 test-prompts 直接评分（AP-04）
- 轮内改多个维度（AP-05）
- dry_run 比例 > 30%（AP-06）
- 静默跳过异常（AP-07）
- 忽视维度相关性单独优化（AP-08）

## 示例

### 搜索并安装
```
用户: 帮我找个代码格式化的 skill
→ 环境检查 → 搜索流程 → 展示结果 → 用户选择 → 安全审查 → 安装
```

### 从零开发
```
用户: 帮我开发一个代码审查 skill
→ 环境检查 → 需求深挖 → 全网搜索（含深度搜索）→ 方案推送 → 分阶段开发 → 完整交付
```

### 审查评分
```
用户: 帮我审查一下这个 skill 的质量
→ 加载 review 子技能 → 安全审查 → Darwin 9 维度评分 → 输出报告
```

### 优化现有
```
用户: 这个 skill 触发不太准，帮我优化
→ 诊断（审查）→ 找出问题 → 改 description → 棘轮验证 → 多评委评估
```

### 合并 Skill
```
用户: 把这几个 skill 合并成一个
→ 环境检查 → 审查原 Skill → 理解原 Skill → 询问用户 → 网上调研 → 综合优化 → 分阶段开发 → 用户确认
```
# 工作流程详细指南

本文档包含 skill-workspace 各流程的详细执行步骤和模板。主 SKILL.md 只保留流程概要，详细内容在此文档中。

---

## 流程零：环境检查详细步骤

### 第零步：环境问话

**必问清单：**

1. **操作系统与 Agent**
   - 问题：您当前使用什么操作系统和 Agent？
   - 选项：Windows + Claude Code / macOS + Claude Code / Linux + Codex CLI / 其他

2. **网络环境**
   - 问题：您的网络环境是否能直接访问 GitHub/npm？
   - 选项：能直接访问 / 需要代理 / 使用镜像源 / 不确定

3. **已安装的搜索增强 Skill**
   - 问题：您是否已安装深度搜索相关 Skill？
   - 选项：deep-research-pro / multi-search-engine / 都安装了 / 都没安装

4. **操作偏好**
   - 问题：发现缺失依赖时，您希望？
   - 选项：自动安装 / 手动安装（提供命令）/ 跳过该依赖 / 询问后再决定

### 第一步：检查基础依赖

```bash
curl --version    # HTTP 客户端
git --version     # 版本控制
python --version  # Python 运行时
node --version    # Node.js 运行时
npm --version     # npm 包管理器
```

### 第二步：检查搜索增强 Skill

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

### 环境检查报告模板

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

## 流程一：搜索 Skill 详细步骤

### 搜索前问话

**必问清单：**

1. **使用场景** — 个人项目 / 团队协作 / 企业生产 / 学习研究
2. **技术栈偏好** — Python / Node.js / Rust / Go / 无所谓
3. **功能优先级** — 核心功能完整 / 易用性 / 性能 / 安全性 / 文档完善 / 社区活跃
4. **集成方式** — 直接安装使用 / 改造后使用 / 参考实现自己写 / 仅作调研

### 搜索源（按优先级）

**Tier 1：SkillsMP (skillsmp.com)**
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q={关键词}&limit=10&sortBy=stars"
```

**Tier 2：Skills.sh 生态**
```bash
npx skills find {关键词}
```

**Tier 3：CocoLoop API**
```bash
curl -s "https://api.cocoloop.com/api/v1/store/skills?page=1&page_size=10&keyword={关键词}&sort=downloads"
```

**Tier 4：GitHub 搜索**
```bash
curl -s "https://api.github.com/search/repositories?q={关键词}+filename:SKILL.md&sort=stars&per_page=5"
```

**GitHub 国内访问降级策略：**
```
GitHub 直连 → 超时？
  ├── 尝试镜像站（github.moeyy.xyz / hub.fastgit.xyz / ghproxy.com）
  ├── 尝试 GitHub API（api.github.com）
  ├── 尝试代理（检测 $http_proxy / $https_proxy）
  └── 降级到 Tier 1-3 搜索源
```

**Tier 5：clawhub CLI**
```bash
npx clawhub@latest search {关键词}
```

**Tier 6：深度搜索引擎**
- deep-research-pro：16 个搜索引擎（含 7 个中文）
- multi-search-engine：16 个引擎（含抖音/B站等）

### 搜索结果报告模板

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

## 流程二：下载/安装 Skill 详细步骤

### 安装前问话

**必问清单：**

1. **安装位置** — 全局目录（~/.skills/）/ 当前工作区（./）/ 项目级（.skills/）/ 其他
2. **版本选择** — 最新稳定版 / 最新开发版 / 指定版本 / 不在意
3. **安装后操作** — 立即测试 / 仅安装 / 安装并部署到其他 Agent / 安装并生成使用文档

### 安装流程

1. **环境检查** — 调用流程零检查基础依赖
2. **获取 Skill 内容**
   - URL → curl 下载
   - 名称 → 按搜索流程找到后下载
   - GitHub → **优先 curl 只下载 SKILL.md**；确需全量源码才 git clone
   - 国内环境 → 按 GitHub 降级策略获取

   ⚠️ **git clone 必须落到受管工作区**（禁止散落，否则无法安全自动清理）：

   ```bash
   SRC=".cache/sources/$(date +%Y%m%d-%H%M%S)-{repo-name}"
   mkdir -p "$SRC"
   git clone --depth 1 {repo-url} "$SRC"     # --depth 1 省 60%+ 空间
   printf 'marker=skill-workspace-source\nsource_url=%s\nskill_name=%s\npurpose=search\ncloned_at=%s\nstatus=in-use\n' \
     "{repo-url}" "{skill名}" "$(date -Iseconds)" > "$SRC/.skill-workspace-source"
   ```

3. **安全审查**（强制）— 评级 ≥ B → 继续；评级 ≤ C → 询问用户是否继续
4. **安装到工作区**
   ```bash
   cp -r {skill目录}/ "./{skill名}/"
   # 或安装到全局
   cp -r {skill目录}/ ~/.skills/{skill名}/
   ```
5. **确认安装结果**
6. **释放源码工作区**（如执行过 git clone）
   ```bash
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" release "{工作区名}"
   bash "${SKILL_DIR}/scripts/source-cleanup.sh" auto
   ```
   安装到全局后源码副本即冗余，必须回收。详见 `references/source-lifecycle.md`。
7. **生成安装报告**

### 安装报告模板

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

## 流程三：安全审查详细步骤

### 审查前问话

**必问清单：**

1. **审查重点** — 敏感数据泄露 / 危险命令执行 / 网络访问 / 权限范围 / 全部检查
2. **风险容忍度** — 严格（任何 WARNING 都拒绝）/ 标准（仅 BLOCK 拒绝）/ 宽松（仅提示不拒绝）
3. **使用环境** — 个人开发机 / 团队共享 / 企业生产 / 沙盒环境
4. **已知问题** — 无 / 有（请描述）/ 不确定

### 审查协议（4 步）

**第 1 步：元数据检查**
- [ ] `name` 与预期 skill 名称匹配（无 typosquatting）
- [ ] `version` 遵循语义化版本号
- [ ] `description` 清晰且与实际行为一致
- [ ] `author` 可识别

**第 2 步：权限范围分析**

| 权限 | 风险等级 | 说明 |
|------|----------|------|
| Read | Low | 几乎总是合法的 |
| Write | Medium | 必须说明写入哪些文件 |
| Network | High | 必须说明访问哪些端点 |
| Shell/Bash | Critical | 必须说明执行哪些命令 |

**第 3 步：内容扫描**

**BLOCK（阻止安装）：**
- 引用 `~/.ssh`、`~/.aws`、`~/.env` 等敏感路径
- 使用 `curl`、`wget`、`nc`、`bash -i` 等命令
- `base64` 混淆内容
- 禁用安全机制
- 未知或可疑 URL

**WARNING（需要审查）：**
- `/**/*` 等宽泛通配符
- `sudo` 使用
- 潜在的提示注入

**第 4 步：Typosquat 检测**
- 检查单字符交换（如 `skil` vs `skill`）
- 检查同形异义字符（如 `l/1`、`O/0`）
- 检查多余连字符（如 `skill--name`）

### 安全审查报告模板

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

---

## 流程四：优化 Skill 详细步骤

### 优化前问话

**必问清单：**

1. **优化目标** — 触发精准度 / 指令明确性 / 输出质量 / 性能 / 安全性 / 易用性 / 其他
2. **具体问题** — 开放式问题，让用户描述具体问题
3. **优化优先级** — 最严重的问题 / 最容易解决的问题 / 影响最大的问题 / 全部解决
4. **优化约束** — 不能改变触发词 / 不能增加文件大小 / 不能改变输出格式 / 无约束
5. **验收标准** — Darwin 评分提升 / 用户实际测试 / evals 通过 / 多评委审查

### 优化流程

1. **诊断** — 先用「审查」流程找出问题
2. **制定方案** — 按优先级排列改进项
3. **执行改进**
   - description 不准 → 改触发词，补正例/反例
   - workflow 有漏洞 → 补步骤，加检查点
   - 输出不合格 → 改格式，补样例
   - 误触发 → 收窄触发条件
4. **验证** — 用同一个 case 跑一遍，确认改善
5. **回归** — 用 evals 重跑，确保没引入新问题
6. **生成优化报告**

### 优化报告模板

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
| D3 失败模式编码 | {分} | 10 | {problem} |
| D4 可执行具体性 | {分} | 10 | {problem} |
| D5 边界条件 | {分} | 10 | {problem} |
| D6 用户确认点 | {分} | 10 | {problem} |
| D7 高风险行动黑名单 | {分} | 10 | {problem} |
| D8 实测表现 | {分} | 20 | {problem} |
| D9 反例黑名单检查 | {分} | 10 | {problem} |
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

## 优化结果

### Darwin 9 维度评分（优化后）

| 维度 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| D1 结构完整性 | {分} | {分} | {+/-} |
| D2 指令具体性 | {分} | {分} | {+/-} |
| D3 失败模式编码 | {分} | {分} | {+/-} |
| D4 可执行具体性 | {分} | {分} | {+/-} |
| D5 边界条件 | {分} | {分} | {+/-} |
| D6 用户确认点 | {分} | {分} | {+/-} |
| D7 高风险行动黑名单 | {分} | {分} | {+/-} |
| D8 实测表现 | {分} | {分} | {+/-} |
| D9 反例黑名单检查 | {分} | {分} | {+/-} |
| **总分** | **{分}** | **{分}** | **{+/-}** |

### 棘轮机制验证
- [ ] 评分 >= 上一轮
- [ ] 文件大小 <= 原始 x 1.5
- [ ] 无反例黑名单触发

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

## 流程五：部署详细步骤

### 部署前问话

**必问清单：**

1. **目标 Agent** — Claude Code / Codex CLI / Cursor / 通用（~/.skills/）/ 多个 Agent
2. **部署范围** — 仅 SKILL.md / 完整 skill 包（含 references）/ 完整包 + 子技能 / 自定义
3. **已有版本处理** — 覆盖（备份旧版）/ 覆盖（不备份）/ 跳过 / 询问后决定
4. **部署后验证** — 仅检查文件存在 / 运行 evals / 实际任务测试 / 多评委审查

### 部署流程

1. **环境检查** — 调用流程零，确保目标目录可写
2. **确认来源** — 工作区中的哪个 skill 目录
3. **检查是否通过测评** — 建议先走「审查」流程
4. **复制到全局**
   ```bash
   cp -r "./{skill名}/" ~/.skills/{skill名}/
   ```
5. **验证部署**
   ```bash
   ls ~/.skills/{skill名}/
   ```
6. **测试全局可用**
   - `claude -p "使用 {name} 完成 XXX"`
   - `codex "使用 {name} 完成 XXX"`
7. **释放源码工作区**（自动执行，无需询问）
   - 前置条件：步骤 5、6 均通过
   - 标记所有 `skill_name={skill名}` 的受管工作区为 releasable
   - 执行回收：
     ```bash
     bash "${SKILL_DIR}/scripts/source-cleanup.sh" release "{工作区名}"
     bash "${SKILL_DIR}/scripts/source-cleanup.sh" auto
     ```
   - 向用户报告释放了哪些、释放多少空间、如何回滚

   详见 `references/source-lifecycle.md`。

**⚠️ 永远用 `cp`，不用 `mv`，保留源文件。**

**⚠️ 注意区分两个「源」：** Skill 源文件（`projects/{skill名}/`，**永不删除**，是回滚依据）vs 分析用下载的第三方源码（`.cache/sources/`，部署后必须释放）。清理只针对后者。

---

## 流程六：管理详细步骤

### 管理前问话

**必问清单：**

1. **操作类型** — 列出已安装 / 更新单个 / 批量更新 / 检查更新 / 卸载 / 查看详情
2. **操作范围** — 全局 / 项目级 / 全部
3. **操作确认** — 确认执行 / 取消 / 先查看影响范围

### 列出已安装 Skill

```bash
ls ~/.skills/
ls ./
```

### 更新 Skill

**单个更新：**
1. 查询最新版本（SkillsMP API、CocoLoop API 或 GitHub）
2. 比较本地版本与远程版本
3. 有更新 → 备份旧版 → 下载新版 → 安全审查 → 安装

**批量更新：**
```bash
npx skills update
```

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

## 流程七：合并 Skill 详细步骤

### 合并目标

1. **消除冗余** — 减少功能重叠，降低维护成本
2. **增强能力** — 集成多个 Skill 的优点，形成更强功能
3. **优化体验** — 统一触发条件和输出规范，减少用户困惑
4. **解决问题** — 修复原 Skill 的痛点和缺陷
5. **优化提示词** — 提升触发精准度和指令明确性
6. **优化子技能调用** — 提升调用效率和错误处理
7. **优化用户体验** — 降低使用门槛，提升易用性

### 合并流程

```
第一步：深度分析原 Skill
  ↓ 全面深入理解每个原 skill 的设计理念、核心功能和优化空间
  ↓ 生成深度分析报告 → 保存到 ./artifacts/analysis/
第二步：审查原 Skill
  ↓ 调用 review 子技能，对每个原 Skill 进行 Darwin 9 维度打分
第三步：理解原 Skill
  ↓ 基于深度分析，理解核心价值、用户场景、使用频率、依赖关系
第四步：询问用户
  ↓ 明确合并方向：保留优点、解决痛点、新增需求、优先级
第五步：网上调研
  ↓ 使用 multi-search-engine 搜索最佳实践、踩坑经验、竞品分析
  ↓ 生成调研报告 → 保存到 ./artifacts/research/
第六步：综合优化
  ↓ 设计合并方案：保留优点、解决痛点、集成新功能、简化结构
  ↓ 生成合并方案 → 保存到 ./artifacts/merge/
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

## 深度分析结果
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
- 提示词优化方案：[说明如何优化提示词]
- 子技能调用优化方案：[说明如何优化子技能调用]
- 用户体验优化方案：[说明如何优化用户体验]
```

---

## 流程八：MCP整合详细步骤

**详细指南：** `${SKILL_DIR}/references/mcp-integration.md`

### MCP整合前问话结果

| 问题 | 用户选择 | 影响 |
|------|----------|------|
| 整合模式 | [MCP包装为Skill / Skill+MCP协同 / MCP Gateway] | 决定整合方案 |
| MCP来源 | [已有配置 / 需搜索 / 需开发] | 决定调研范围 |
| 目标平台 | [Claude Code / TRAE / Cursor / 多平台] | 决定配置格式 |
| 安全要求 | [沙箱 / 权限最小化 / 网络白名单 / 无] | 决定安全策略 |

### MCP整合过程

```
第一步：MCP生态调研
  ├── 搜索官方MCP Servers、社区MCP、awesome-mcp列表
  ├── 评估MCP Server质量、安全性、维护状态
  └── 记录候选MCP Server清单

第二步：确认整合模式
  ├── 模式A：MCP包装为Skill（MCP提供工具，Skill提供工作流）
  ├── 模式B：Skill + MCP协同（Skill调用MCP工具完成任务）
  └── 模式C：MCP Gateway配置（企业级统一MCP入口）

第三步：安全审查（增强版）
  ├── MCP Server权限分析
  ├── 语义-行为一致性检测
  ├── 组合攻击风险评估（MCP+Skill组合风险）
  └── MCP Server来源验证

第四步：生成整合方案
  ├── SKILL.md（含MCP工具调用指引）
  ├── MCP配置片段（.mcp.json）
  └── 使用示例和边界条件

第五步：本地测试
  ├── 验证MCP连接
  ├── 测试Skill调用MCP工具
  └── 审查评分

第六步：部署配置
  ├── 部署Skill到全局目录
  └── 更新对应平台的MCP配置文件
```

### MCP整合结果

- 整合模式：[模式A/B/C]
- MCP Server：[名称]
- 配置文件：[路径]
- 测试结果：[通过/失败]
- 审查评分：[分数]

---

## 流程九：工作流蒸馏详细步骤

**详细指南：** `${SKILL_DIR}/references/workflow-distillation.md`

### 蒸馏前问话结果

| 问题 | 用户选择 | 影响 |
|------|----------|------|
| 工作流类型 | [业务/技术/决策/创作/复合] | 决定蒸馏策略 |
| 复杂度评估 | [阶段数/决策点数/异常路径数] | 决定架构复杂度 |
| 知识库规模 | [小/中/大] | 决定references拆分 |
| 代码量预期 | [纯指令/少量脚本/大量脚本] | 决定scripts封装 |
| 目标用户 | [新手/专家/通用] | 决定引导详细度 |
| 使用频率 | [高频/中频/低频] | 决定优化重点 |

### 蒸馏过程

```
第一步：工作流分析
  ├── 识别阶段数及各阶段输入输出
  ├── 识别决策点（if-else）和异常处理
  ├── 评估复杂度
  └── 决定是否需要三层加载架构

第二步：架构设计（推荐三层加载）
  ├── 第一层：SKILL.md 薄入口（≤200行，理想≤80行）
  │   ├── frontmatter（name, description, allowed-tools）
  │   ├── <objective> 一句话目标
  │   ├── <execution_context> 资源路径指针
  │   ├── <process> 步骤概要 + 决策树
  │   └── 路由到 references/ 和 subskills/
  ├── 第二层：references/ 按需加载知识库
  │   ├── workflow-overview.md（完整流程定义，360-500行）
  │   ├── phase-1-xxx.md（分阶段详情）
  │   ├── decision-trees.md（决策树集合）
  │   ├── error-handling.md（错误处理）
  │   └── domain-knowledge.md（领域知识）
  └── 第三层：subskills/ + scripts/ + templates/ 工具资产
      ├── subskills/（独立子流程）
      ├── scripts/（确定性逻辑脚本）
      └── templates/（可复用模板）

第三步：内容蒸馏
  ├── 将工作流各阶段拆分到 references/phase-*.md
  ├── 决策树抽象到 references/decision-trees.md
  ├── 确定性逻辑封装到 scripts/*.py
  └── 可复用产出物放入 templates/

第四步：Token优化
  ├── 薄入口只保留路由信息和决策树
  ├── references/ 文件控制在 200-500 行
  └── 使用 ${CLAUDE_SKILL_DIR} 变量引用资源

第五步：评测集构建
  ├── 核心样本（覆盖主流程）
  ├── 边界样本（决策点、异常路径）
  └── 大型样本（端到端完整流程）

第六步：审查与沉淀
  ├── Darwin 9维度审查
  └── 改进记忆沉淀到 .dev-memory.md（流程十）
```

### 蒸馏结果

- 架构类型：[单文件 / 三层加载]
- SKILL.md 行数：[行数]
- references/ 文件数：[数量]
- subskills/ 数量：[数量]
- scripts/ 数量：[数量]
- templates/ 数量：[数量]
- evals/ 样本数：[数量]
- 审查评分：[分数]

### 蒸馏关键约束

- SKILL.md 主文档 ≤ 500 行（官方建议），超过 30KB 后 AI 任务理解能力显著下降
- references/ 单文件控制在 200-500 行，按需加载
- 使用 `${CLAUDE_SKILL_DIR}` 变量引用资源，避免硬编码路径
- 工作流蒸馏完成后，必须按流程十沉淀开发记忆

---

## 流程十：开发记忆与发布清洗详细步骤

**详细指南：** `${SKILL_DIR}/references/dev-memory-guide.md`

### 记忆沉淀流程

```
第一步：识别变更
  ├── 本次操作改了什么（What）
  ├── 为什么改（Why）
  ├── 改前的状态（Before）
  ├── 改后的状态（After）
  └── 验证结果（Verification）

第二步：生成记忆记录
  ├── 按规范格式生成记录
  ├── 包含版本号和时间戳
  └── 包含验证结果

第三步：追加到 .dev-memory.md
  ├── 定位目标 Skill 的根目录
  ├── 如果 .dev-memory.md 不存在 → 创建文件（含头部说明）
  ├── 如果存在 → 追加到"记忆记录区"
  └── 不要覆盖已有记忆

第四步：检查主文档污染
  ├── 扫描 SKILL.md 是否包含开发记忆
  ├── 扫描 subskills/*/SKILL.md
  ├── 扫描 references/*.md（正式参考文档除外）
  └── 如有污染 → 移除并迁移到 .dev-memory.md

第五步：确认沉淀完成
  └── 输出沉淀摘要给用户
```

### 发布前清洗流程

```
第一步：检测清洗触发词
  ├── "正式部署"、"部署到全局"、"部署到生产"
  ├── "开源"、"发布到 GitHub"、"上传到社区"
  ├── "打包发布"、"发布新版本"、"release"
  └── "分享给他人"、"给别人用"

第二步：检测 .dev-memory.md 是否存在
  ├── 不存在 → 跳过清洗，直接部署
  └── 存在 → 询问用户是否清洗

第三步：扫描主文档污染
  ├── 扫描 SKILL.md
  │   ├── 检查是否包含"更新概要"、"变更日志"、"版本说明"
  │   ├── 检查是否包含 "vX.Y 新增"、"vX.Y 修改" 等版本标记
  │   ├── 检查是否包含 TODO、FIXME、HACK 等开发注释
  │   ├── 检查是否包含"为什么选择 X" 等决策记录
  │   └── 检查是否包含临时性、开发期特有的指令
  ├── 扫描 subskills/*/SKILL.md（同上）
  └── 扫描 references/*.md（同上）

第四步：清除污染
  ├── 备份原文件（可选，询问用户）
  ├── 从主文档中移除开发记忆内容
  ├── 保留功能指令、工作流程、参考资料等正式内容
  └── 将移除的内容归档到 .dev-memory.md

第五步：验证清洗结果
  ├── 主文档只包含 Skill 指令
  ├── 无版本标记、无开发注释、无决策记录
  └── 功能完整性未受影响（跑一遍 evals）

第六步：生成清洗报告
  └── 保存到 ./artifacts/cleanup/cleanup-report-{date}-{skill-name}.md

第七步：执行发布/部署
```

### 清洗检查清单

- [ ] SKILL.md 中无"更新概要"、"变更日志"、"版本说明"章节
- [ ] SKILL.md 中无 "vX.Y 新增"、"vX.Y 修改" 等版本标记
- [ ] SKILL.md 中无 TODO、FIXME、HACK 等开发注释
- [ ] SKILL.md 中无"为什么选择 X" 等决策记录
- [ ] SKILL.md 中无临时性、开发期特有的指令
- [ ] subskills/*/SKILL.md 同上检查通过
- [ ] references/*.md 同上检查通过（正式参考文档除外）
- [ ] .dev-memory.md 保留在本地，未随包发布
- [ ] 功能完整性测试通过（evals 通过率 ≥ 80%）
- [ ] 清洗报告已生成

---

## 工作产物管理

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
| MCP整合报告 | MCP整合完成后 | `mcp-integration-{date}-{name}.md` | `./artifacts/mcp/` |
| 蒸馏报告 | 工作流蒸馏完成后 | `distillation-{date}-{workflow-name}.md` | `./artifacts/distillation/` |
| 清洗报告 | 发布前清洗完成后 | `cleanup-{date}-{skill-name}.md` | `./artifacts/cleanup/` |

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
├── merge/               # 合并方案
├── mcp/                 # MCP整合报告
├── distillation/        # 工作流蒸馏报告（v5.3新增）
└── cleanup/             # 发布前清洗报告（v5.3新增）
```

### 产物生成规则

1. **自动创建目录** — 生成产物前，自动创建目录（如果不存在）
2. **命名规范** — `{类型}-{date}-{关键词}.md`
3. **产物引用** — 后续流程引用前序产物时，使用相对路径
4. **产物更新** — 如果同一主题的产物已存在，询问用户处理方式

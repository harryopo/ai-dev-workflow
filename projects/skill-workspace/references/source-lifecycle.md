# 源码工作区生命周期管理

> v5.4 新增。解决「下载源码做全量分析 → 源码长期占磁盘」的问题。

## 1. 问题

「搜索 / 开发 / 审查 / 合并」流程会 `git clone` 第三方仓库做全量源码分析。分析完成后源码不再被引用，但默认留在磁盘上。单个仓库几十 MB 到数 GB 不等，累积后严重占用空间。

**核心矛盾：** 直接 `rm -rf` 有删错风险；不管又会撑爆磁盘。

**解法：** 受管目录 + 标记文件 + 两段式回收。只有本工具自己创建、且带标记的目录才允许被清理；清理先移入暂存区（可恢复），冷静期后才真正删除。

---

## 2. 目录约定

**所有 git clone 必须落在受管根目录，禁止散落到工作区任意位置。**

```
{工作区}/
└── .cache/sources/                      # 受管根目录（唯一允许自动清理的地方）
    ├── 20260904-221000-anthropics-skills/
    │   ├── .skill-workspace-source      # 标记文件（必须）
    │   └── ...源码...
    ├── 20260904-223000-superpowers/
    │   ├── .skill-workspace-source
    │   └── ...源码...
    └── .trash/                          # 回收暂存区（stage 后移入此处）
        └── 20260904-221000-anthropics-skills-20260905-090000/
```

**命名规范：** `{YYYYMMDD-HHMMSS}-{repo-name}`

**为什么统一路径：** 清理工具只认这个根。散落的克隆目录无法被识别，也就无法被安全自动清理——那是磁盘泄漏的根源。

---

## 3. 标记文件

每个受管工作区根目录必须有 `.skill-workspace-source`（KEY=VALUE 格式，bash 与 PowerShell 均能解析）：

```
marker=skill-workspace-source
source_url=https://github.com/anthropics/skills
skill_name=my-skill
purpose=dev
cloned_at=2026-09-04T22:10:00+08:00
status=in-use
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `marker` | ✅ | 固定值 `skill-workspace-source`，清理工具的准入凭证 |
| `source_url` | ✅ | 克隆来源，便于日后重新获取 |
| `skill_name` | ⬜ | 关联的 Skill 名，用于 `-Skill` 过滤 |
| `purpose` | ✅ | `search` / `dev` / `review` / `merge` |
| `cloned_at` | ✅ | 克隆时间 |
| `status` | ✅ | `in-use` / `releasable` / `staged` |
| `staged_at` | ⬜ | stage 时自动写入 |
| `staged_from` | ⬜ | stage 时自动写入，记录原目录名供 restore 用 |

**创建方式（clone 后立刻执行）：**

```bash
SRC=".cache/sources/$(date +%Y%m%d-%H%M%S)-{repo-name}"
mkdir -p "$SRC"
git clone --depth 1 {repo-url} "$SRC"     # --depth 1 省 60%+ 空间

cat > "$SRC/.skill-workspace-source" <<EOF
marker=skill-workspace-source
source_url={repo-url}
skill_name={skill-name}
purpose=dev
cloned_at=$(date -Iseconds)
status=in-use
EOF
```

**克隆一律加 `--depth 1`**，分析只需要最新代码，不需要完整提交历史。

---

## 4. 状态机

```
   git clone + 写标记
          │
          ▼
      [in-use]  ──────── 分析进行中，禁止清理
          │
          │  触发点达成（见第 5 节）
          ▼
    [releasable]  ────── 已无用，等待回收
          │
          │  stage（移入 .trash，可 restore）
          ▼
      [staged]  ──────── 占空间但可恢复，冷静期 7 天
          │
          │  purge（冷静期后，真正删除）
          ▼
      [已释放]
```

**关键：任何一步都可通过 `restore` 回滚到 `in-use`。**

---

## 5. 清理触发点

Agent 在以下四个时机**必须**主动处理源码释放，无需用户手动提醒：

### 触发点 A — 部署成功之后（最高优先级）

流程五「部署」执行完第 8 步「验证部署」且通过后：

```
验证部署通过
  ↓
标记所有 purpose=dev 且 skill_name 匹配的源码为 releasable
  ↓
执行 auto（移入 .trash）
  ↓
向用户报告：「已释放源码工作区 N 个，进入 7 天冷静期」
```

**这是用户最关心的场景：Skill 已经部署到全局，源码副本就是纯冗余。**

### 触发点 B — 审查报告产出之后

审查流程生成报告到 `./artifacts/review/` 后，该报告已包含全部结论，源码不再被引用：

```
生成审查报告 → 标记 purpose=review 的源码 releasable → 询问用户是否立即回收
```

审查场景建议**先询问再回收**（用户可能要基于报告继续追问源码细节），不强制 auto。

### 触发点 C — 合并 / 蒸馏完成后

流程七「合并」、流程九「工作流蒸馏」完成后，源 Skill 已被合并进新 Skill，旧源码工作区可释放。

### 触发点 D — 用户显式要求

用户说「清理源码」「释放磁盘」「删掉下载的源码」「清理缓存」时，执行 `list` 展示清单 → 确认 → `stage` → `purge`。

---

## 6. 安全红线（硬约束）

以下规则已编入脚本，**违反即中止执行**，不允许用任何参数绕过：

| # | 规则 | 原因 |
|---|------|------|
| 1 | 只操作受管根目录的**直接子目录** | 防止递归删除扩散 |
| 2 | 目标必须含标记文件且 `marker` 匹配 | 用户自己的目录永远不会被删 |
| 3 | 拒绝 `..`、绝对路径、路径分隔符、隐藏目录 | 防路径注入 |
| 4 | 解析真实路径并检查是否在根内 | 防符号链接逃逸 |
| 5 | 禁止操作根目录自身、`$HOME`、`.`、`/` | 防灾难性删除 |
| 6 | 先 stage 后 purge，**无直接删除路径** | 所有删除都经过可恢复的中转站 |
| 7 | purge 默认 7 天冷静期，默认 dry-run | 误判仍有挽回窗口 |
| 8 | 无标记目录只报告、不处理 | 不碰来路不明的目录 |
| 9 | 非交互环境必须显式 `--yes` / `-Yes` | 防自动化误删 |

**绝不允许的行为：**
- ❌ 对非受管目录执行 `rm -rf` / `Remove-Item -Recurse`
- ❌ 跳过 stage 直接 purge
- ❌ 删除 `.dev-memory.md`、`artifacts/`、`projects/` 等用户资产
- ❌ 因为「看起来没用」就删无标记目录

---

## 7. 脚本用法

### Bash / Git Bash

```bash
SCRIPTS="${SKILL_DIR}/scripts"

# 查看所有受管源码工作区及占用
bash "$SCRIPTS/source-cleanup.sh" list

# 标记某个工作区为可释放
bash "$SCRIPTS/source-cleanup.sh" release 20260904-221000-anthropics-skills

# 回收所有 releasable 的（auto 触发点用这个）
bash "$SCRIPTS/source-cleanup.sh" auto

# 强制回收指定工作区（跳过 in-use 询问）
bash "$SCRIPTS/source-cleanup.sh" stage {name} --yes

# 查看将释放什么（不执行）
bash "$SCRIPTS/source-cleanup.sh" purge --dry-run

# 真正删除暂存区中超过 7 天的内容
bash "$SCRIPTS/source-cleanup.sh" purge --yes

# 立即清空暂存区（跳过冷静期，谨慎）
bash "$SCRIPTS/source-cleanup.sh" purge --older-than 0 --yes

# 误删恢复
bash "$SCRIPTS/source-cleanup.sh" restore {staged-name}
```

### Windows PowerShell

```powershell
$SCRIPTS = "${SKILL_DIR}\scripts"

powershell -ExecutionPolicy Bypass -File "$SCRIPTS\source-cleanup.ps1" list
powershell -ExecutionPolicy Bypass -File "$SCRIPTS\source-cleanup.ps1" auto
powershell -ExecutionPolicy Bypass -File "$SCRIPTS\source-cleanup.ps1" release {name}
powershell -ExecutionPolicy Bypass -File "$SCRIPTS\source-cleanup.ps1" purge -Yes
powershell -ExecutionPolicy Bypass -File "$SCRIPTS\source-cleanup.ps1" restore {staged-name}
```

### 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--root` / `-Root` | 受管根目录 | `.cache/sources` |
| `--skill` / `-Skill` | 按关联 Skill 过滤 | 全部 |
| `--older-than` / `-OlderThan` | purge 冷静期天数 | `7` |
| `--yes` / `-Yes` | 跳过交互确认 | 关闭 |
| `--dry-run` / `-DryRun` | 只预览不执行 | 关闭 |

---

## 8. 与其他流程的协同

| 流程 | 协同方式 |
|------|----------|
| 流程一 搜索 | 下载的参考实现必须落受管目录并写标记 |
| 流程二 下载/安装 | 同上；安装完成即标记 releasable |
| 流程三 安全审查 | 审查对象在受管目录内，审查完不立即删（触发点 B 先询问） |
| 流程五 部署 | **验证通过后自动触发释放**（触发点 A） |
| 流程七 合并 | 合并完成后释放参与合并的源码（触发点 C） |
| 流程九 蒸馏 | 蒸馏完成后释放源工作流仓库（触发点 C） |
| 流程十 发布清洗 | 清洗只处理 Skill 文档污染，不碰源码工作区；两者独立 |

---

## 9. 报告与可见性

清理动作必须对用户可见，不许静默执行。执行后输出：

```
源码工作区释放报告
=================
释放工作区: 2 个
  - 20260904-221000-anthropics-skills  (142 MB) → .trash
  - 20260904-223000-superpowers         (38 MB) → .trash
当前暂存区占用: 180 MB
冷静期: 7 天后自动永久释放
回滚方式: source-cleanup.sh restore {staged-name}
```

**保留的工作区（仍标记 in-use）也要一并列出**，让用户知道还有什么占着空间。

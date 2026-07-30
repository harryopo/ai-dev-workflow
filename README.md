# 🔍 Skill 调研工具集

> 轻量搜索 + 深度调研，覆盖开源项目搜索和多源深度研究。

## 🚀 包含的 Skill

| Skill | 定位 | 特性 |
|-------|------|------|
| **[oss-finder](projects/oss-finder/)** | 开源项目搜索 | gh CLI 优先、并发搜索、本地缓存、自动重试 |
| **[deep-research](projects/deep-research/)** | 深度调研 | 16 引擎并发搜索、智能评分、迭代搜索 |

## 📦 安装

### 方式一：克隆整个仓库

```bash
git clone https://github.com/harryopo/skill-workbench.git
```

然后复制需要的 Skill 到 Claude Code 的 skills 目录：

```bash
# Windows
cp -r skill-workbench/projects/oss-finder ~/.claude/skills/
cp -r skill-workbench/projects/deep-research ~/.claude/skills/

# macOS/Linux
cp -r skill-workbench/projects/oss-finder ~/.claude/skills/
cp -r skill-workbench/projects/deep-research ~/.claude/skills/
```

### 方式二：单独安装

```bash
# 安装 oss-finder
git clone https://github.com/harryopo/skill-workbench.git /tmp/sw
cp -r /tmp/sw/projects/oss-finder ~/.claude/skills/
rm -rf /tmp/sw

# 安装 deep-research
git clone https://github.com/harryopo/skill-workbench.git /tmp/sw
cp -r /tmp/sw/projects/deep-research ~/.claude/skills/
rm -rf /tmp/sw
```

## 🛠️ 使用示例

### oss-finder — 快速搜索

```
/oss-finder react table --stars ">1000" --language typescript
/oss-finder python web framework --platform all --limit 10
/oss-finder ai agent --created-after "2025-01-01" --stars ">500"
```

**特性：**
- ✅ gh CLI 优先（实时数据、无速率限制）
- ✅ 并发搜索（4 平台并行 ~3s）
- ✅ 本地缓存（1 小时 TTL）
- ✅ 自动重试（指数退避）
- ✅ 结果去重
- ✅ 日期筛选
- ✅ 多种输出格式（Markdown/JSON/表格）

### deep-research — 深度调研

```
/deep-research 2025 年最值得学习的 Python Web 框架
/deep-research Kubernetes 生产环境最佳实践
/deep-research 大语言模型微调技术
```

**特性：**
- ✅ 16 引擎并发搜索（中文 7 + 国际 6 + 增强 3）
- ✅ 子 Agent 并行（3-5 个维度同时调研）
- ✅ 多源交叉验证（每个结论 2+ 来源支持）
- ✅ 带引用的结构化报告
- ✅ 整合 oss-finder + crawl4ai + agent-reach

## 📁 目录结构

```
skill-workbench/
├── projects/
│   ├── oss-finder/        # 开源项目搜索
│   │   ├── SKILL.md
│   │   ├── scripts/search.py
│   │   ├── references/
│   │   └── evals/
│   └── deep-research/     # 深度调研
│       ├── SKILL.md
│       ├── references/
│       └── evals/
├── CLAUDE.md              # 工作台规范
└── README.md              # 本文件
```

## 📄 许可证

MIT License

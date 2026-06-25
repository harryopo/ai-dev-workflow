# Deep Research — 深度调研工具 v3.1

> 多源并发搜索、质量评分、迭代搜索、报告生成、CSV 导出、代理支持、搜索历史

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    Deep Research 搜索引擎                      │
├─────────────────────────────────────────────────────────────┤
│  免费层（无需配置）                                             │
│  ├── DuckDuckGo    网页搜索，国内可用                          │
│  ├── Bing          网页搜索，国内可用                          │
│  ├── 百度           网页搜索，国内可用                          │
│  ├── GitHub CLI    开源项目搜索                                │
│  ├── npm           Node.js 包搜索                             │
│  └── PyPI          Python 包查询                              │
├─────────────────────────────────────────────────────────────┤
│  增强层（需要 API Key）                                        │
│  ├── Tavily        AI 搜索引擎，1000次/月免费                  │
│  ├── Jina Reader   网页内容提取（需 VPN）                      │
│  └── Gitee         国内开源项目（需 Token）                    │
├─────────────────────────────────────────────────────────────┤
│  自建层（需要部署）                                            │
│  └── SearXNG       元搜索引擎聚合                             │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 安装依赖

```bash
# 免费层（推荐）
pip install ddgs

# 增强层（可选）
pip install duckduckgo-search  # 已包含在 ddgs 中
```

### 2. 检查数据源可用性

```bash
python scripts/search.py --check
```

**输出示例：**
```
[检查] 数据源可用性...

[网络环境]
   VPN: [无]
   Google: [不可达]
   Jina: [不可达]
   Tavily: [不可达]

[数据源状态]
   duckduckgo: [可用]
   tavily: [不可用]
   jina: [不可用]
   searxng: [不可用]
```

### 3. 开始搜索

```bash
# 基础搜索（DuckDuckGo，免费）
python scripts/search.py "Python Web 框架对比 2025"

# 指定数据源
python scripts/search.py "React vs Vue" --sources duckduckgo,tavily

# JSON 格式输出
python scripts/search.py "Kubernetes" --format json --limit 5

# 读取网页内容（需要 VPN）
python scripts/search.py --read "https://example.com/article"
```

## 数据源详解

### 免费层（无需配置）

| 数据源 | 用途 | 国内可用 | 需要配置 |
|--------|------|----------|----------|
| **DuckDuckGo** | 网页搜索 | ✅ | 无需 |
| **Bing** | 网页搜索 | ✅ | 无需 |
| **百度** | 网页搜索 | ✅ | 无需 |
| **GitHub CLI** | 开源项目 | ✅ | 可选 Token |
| **npm** | Node.js 包 | ✅ | 无需 |
| **PyPI** | Python 包 | ✅ | 无需 |

**DuckDuckGo 优势：**
- 完全免费，无需 API Key
- 国内网络可直接访问
- 支持文本/新闻搜索
- API 简洁，易于集成

**来源：** [ddgs](https://github.com/deedy5/ddgs) (MIT License)

**Bing/百度优势：**
- 完全免费，无需 API Key
- 国内网络可直接访问
- HTML 解析获取结果
- 中文搜索结果丰富（百度）

### 增强层（需要 API Key）

| 数据源 | 用途 | 免费额度 | 获取方式 |
|--------|------|----------|----------|
| **Tavily** | AI 搜索 | 1000次/月 | https://app.tavily.com |
| **Jina Reader** | 网页提取 | 20 RPM | https://jina.ai |
| **Gitee** | 国内项目 | 需认证 | https://gitee.com/profile/personal_access_tokens |

**配置方法：**

```bash
# Tavily（推荐）
export TAVILY_API_KEY=tvly-xxxxx

# Jina（需要 VPN）
export JINA_API_KEY=jina_xxxxx

# Gitee（必须）
export GITEE_TOKEN=your_token
```

### 自建层（需要部署）

| 数据源 | 用途 | 部署方式 |
|--------|------|----------|
| **SearXNG** | 元搜索 | Docker |

**部署命令：**

```bash
# Docker 部署
docker run -d -p 8080:8080 searxng/searxng

# 设置环境变量
export SEARXNG_URL=http://localhost:8080
```

**SearXNG 优势：**
- 完全免费开源（AGPL-3.0）
- 聚合 70+ 搜索引擎
- 自建可控，无隐私风险

**来源：** [github.com/searxng/searxng](https://github.com/searxng/searxng)

## 降级策略

### 自动降级流程

```
用户输入搜索请求
      │
      ▼
┌─────────────────┐
│  检测网络环境    │  判断 VPN、API 可达性
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  检测 API Key   │  检查 Tavily/Jina 配置
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  自动选择可用数据源                                           │
│                                                              │
│  场景 1: 有 VPN + API Key                                     │
│    → DuckDuckGo + Bing + 百度 + Tavily + Jina + oss-finder    │
│                                                              │
│  场景 2: 有 API Key（无 VPN）                                  │
│    → DuckDuckGo + Bing + 百度 + Tavily + oss-finder           │
│                                                              │
│  场景 3: 无 VPN + 无 API Key                                   │
│    → DuckDuckGo + Bing + 百度 + oss-finder（降级方案）          │
└─────────────────────────────────────────────────────────────┘
```

### 降级提示

当数据源不可用时，系统会提示：

```
⚠️  tavily: 不可用，需要 API Key
   获取 Key: https://app.tavily.com
   设置环境变量: export TAVILY_API_KEY=tvly-xxxxx

⚠️  jina: 不可用（可能需要 VPN）

✅ duckduckgo: 可用
```

## 使用场景

### 场景 1：技术选型调研

```bash
# 快速对比 Python Web 框架
python scripts/search.py "2025 Python Web 框架对比 FastAPI Django Flask"

# 搜索开源项目
python ../oss-finder/scripts/search.py "python web framework" --stars ">1000" --limit 10
```

### 场景 2：深度调研

```bash
# 使用 deep-research skill
/deep-research 2025 年最值得学习的 Python Web 框架
```

### 场景 3：网页内容提取

```bash
# 提取网页内容为 Markdown（需要 VPN）
python scripts/search.py --read "https://docs.python.org/3/"
```

## 许可证

本项目整合了以下开源工具：

| 工具 | 许可证 | 来源 |
|------|--------|------|
| DuckDuckGo (ddgs) | MIT | https://github.com/deedy5/ddgs |
| SearXNG | AGPL-3.0 | https://github.com/searxng/searxng |
| oss-finder | MIT | 本项目 |

**商业服务（有免费额度）：**
- Tavily: https://tavily.com
- Jina: https://jina.ai

## 相关项目

- **oss-finder**: 开源项目搜索工具（本项目）
- **skill-workspace**: Skill 开发工作台

## v3.1 新特性

### 🔍 搜索结果缓存
- 缓存目录：`~/.cache/deep-research/`
- TTL：1 小时，自动过期
- 命中时直接返回，不发起网络请求

### 📊 结果质量评分
- 自动评估每个结果（0-100 分）
- 维度：标题相关性(40) + 内容丰富度(30) + 来源权威性(20) + 时效性(10)
- 按质量分排序，支持 `--min-score` 过滤

### 🔄 迭代搜索
- 结果不足时自动用变体关键词重搜
- 中文→英文映射（框架→framework）
- 添加年份和"最佳"变体

### 📋 报告生成
- `--format report` 自动生成结构化研究报告
- 包含：执行摘要、来源分析、质量分布、建议

### 📊 CSV 导出
- `--format csv` 输出标准 CSV 格式
- Excel 可直接打开
- 列：序号, 标题, URL, 摘要, 质量分, 来源, 发布日期

### 🌐 代理支持
- `--proxy http://127.0.0.1:7890` 支持 HTTP/HTTPS 代理
- 企业网络环境可用

### 📜 搜索历史
- `--history` 查看最近 7 天搜索记录
- `--history-days 30` 自定义天数
- 存储：`~/.cache/deep-research/history/`

### 💬 反馈系统
- 用户评分（1-5 星）改进后续搜索
- 相似查询自动关联历史反馈
- 反馈存储：`~/.cache/deep-research/feedback/`

### 🔁 重试机制
- 所有 HTTP 请求自动重试 3 次
- 指数退避：1s → 2s → 4s
- 网络不稳定时自动恢复

### 🚀 使用示例

```bash
# 基础搜索（自动缓存 + 评分）
python scripts/search.py "Python Web 框架"

# 只返回高质量结果
python scripts/search.py "React" --min-score 50

# 迭代搜索（冷门话题）
python scripts/search.py "K8s 部署" --iterative

# 生成研究报告
python scripts/search.py "AI agent" --format report

# 导出 CSV
python scripts/search.py "React" --format csv

# 使用代理
python scripts/search.py "Google" --proxy http://127.0.0.1:7890

# 查看搜索历史
python scripts/search.py --history

# 提交反馈
python scripts/search.py --feedback "Python Web 框架" --rating 5
```

## 更新日志

### v3.1.0 (2026-06-25)

- ✨ 新增报告生成（--format report）
- ✨ 新增 CSV 导出（--format csv）
- ✨ 新增代理支持（--proxy）
- ✨ 新增搜索历史（--history）
- ✨ 新增重试机制（指数退避 3 次）
- ♻️ 更新 SKILL.md 文档

### v3.0.0 (2026-06-25)

- ✨ 新增搜索结果缓存（1小时 TTL）
- ✨ 新增结果质量评分（0-100 分）
- ✨ 新增迭代搜索（--iterative）
- ✨ 新增反馈系统（--feedback --rating）
- ✨ 新增关键词多样性（中英文变体）
- 🐛 优化百度 HTML 解析（修复重定向 URL 过滤）
- ♻️ 更新默认数据源为 duckduckgo,bing,baidu

### v2.2.0 (2026-06-25)

- ✨ 集成 Bing 搜索引擎（免费，国内可用）
- ✨ 集成百度搜索引擎（免费，国内可用，支持 gzip）
- ♻️ 更新架构图，免费层新增 2 个数据源
- 📝 更新文档和 evals.json

### v2.1.0 (2026-06-25)

- 🐛 修复 DuckDuckGo 搜索超时问题（使用中国区域 cn-zh）
- ♻️ 禁用新闻搜索（国内访问 Yahoo News 超时）
- ⚡ 优化去重算法，支持 URL 和标题双重去重

### v2.0.0 (2026-06-25)

- ✨ 新增 DuckDuckGo 搜索（免费，国内可用）
- ✨ 新增网络环境检测
- ✨ 新增数据源可用性检查（--check）
- ♻️ 重构降级策略：免费层 → 增强层 → 自建层
- 📝 更新架构文档，详细说明数据源分层

### v1.0.0 (2026-06-20)

- 🎉 初始版本
- ✨ 整合 Tavily + Jina + SearXNG
- ✨ 支持多源并发搜索

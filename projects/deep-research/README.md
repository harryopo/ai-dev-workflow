# Deep Research — 深度调研工具 v2.2

> 多源并发搜索、子 Agent 并行、生成带引用的研究报告

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

## 更新日志

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

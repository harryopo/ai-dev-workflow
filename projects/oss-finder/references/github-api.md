# GitHub API 参考

## 搜索仓库

**端点：** `GET https://api.github.com/search/repositories`

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `q` | string | 搜索查询（必填） |
| `sort` | string | 排序字段：stars、forks、updated、help-wanted-issues |
| `order` | string | 排序方向：asc、desc（默认） |
| `per_page` | integer | 每页条数，最大 100（默认 30） |
| `page` | integer | 页码（默认 1） |

### 搜索语法

#### 限定符

| 限定符 | 示例 | 说明 |
|--------|------|------|
| `in:name` | `react in:name` | 名称中包含 |
| `in:description` | `web framework in:description` | 描述中包含 |
| `in:readme` | `tutorial in:readme` | README 中包含 |
| `stars:N` | `stars:1000` | Stars 等于 N |
| `stars:>N` | `stars:>1000` | Stars 大于 N |
| `stars:N..M` | `stars:100..1000` | Stars 在 N 到 M 之间 |
| `forks:N` | `forks:100` | Forks 等于 N |
| `forks:>N` | `forks:>100` | Forks 大于 N |
| `language:X` | `language:python` | 使用语言 X |
| `topic:X` | `topic:machine-learning` | 包含 Topic X |
| `license:X` | `license:mit` | 许可证为 X |
| `created:>YYYY-MM-DD` | `created:>2024-01-01` | 创建时间晚于 |
| `pushed:>YYYY-MM-DD` | `pushed:>2024-01-01` | 最后推送晚于 |
| `user:X` | `user:facebook` | 用户 X 的仓库 |
| `org:X` | `org:google` | 组织 X 的仓库 |
| `size:N` | `size:>1000` | 仓库大小（KB） |
| `is:public` | `is:public` | 公开仓库 |
| `is:private` | `is:private` | 私有仓库 |
| `archived:true` | `archived:true` | 已归档仓库 |

#### 组合查询

```
# Python Web 框架，Stars > 1000
stars:>1000 language:python topic:web

# 2024 年创建的 React 项目
language:javascript topic:react created:>2024-01-01

# MIT 许可证的机器学习项目
topic:machine-learning license:mit
```

### 响应示例

```json
{
  "total_count": 11004,
  "incomplete_results": false,
  "items": [
    {
      "id": 123456,
      "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY=",
      "name": "react",
      "full_name": "facebook/react",
      "private": false,
      "owner": {
        "login": "facebook",
        "id": 69631,
        "avatar_url": "https://avatars.githubusercontent.com/u/69631?v=4",
        "html_url": "https://github.com/facebook"
      },
      "html_url": "https://github.com/facebook/react",
      "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
      "fork": false,
      "url": "https://api.github.com/repos/facebook/react",
      "stargazers_count": 220000,
      "watchers_count": 220000,
      "forks_count": 45000,
      "language": "JavaScript",
      "topics": [
        "declarative",
        "frontend",
        "javascript",
        "library",
        "react",
        "ui"
      ],
      "license": {
        "key": "mit",
        "name": "MIT License",
        "spdx_id": "MIT"
      },
      "open_issues_count": 1442,
      "default_branch": "main",
      "created_at": "2013-05-24T16:15:54Z",
      "updated_at": "2026-06-20T10:30:00Z",
      "pushed_at": "2026-06-19T15:45:00Z"
    }
  ]
}
```

### 速率限制

| 认证状态 | Search API | Core API |
|----------|------------|----------|
| 未认证 | 10 次/分钟 | 60 次/小时 |
| Token 认证 | 30 次/分钟 | 5000 次/小时 |

### 认证

```bash
# Personal Access Token
curl -H "Authorization: Bearer ghp_xxxx" \
  "https://api.github.com/search/repositories?q=react"
```

### 响应头

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 28
X-RateLimit-Reset: 1624000000
```

### 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 304 | 未修改 |
| 403 | 速率限制 |
| 422 | 验证失败 |
| 503 | 服务不可用 |

### 限制

- 结果上限 1000 条
- `incomplete_results: true` 时结果可能不完整
- 未认证请求容易被限流

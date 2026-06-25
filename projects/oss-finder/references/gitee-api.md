# Gitee API 参考

## 搜索仓库

**端点：** `GET https://gitee.com/api/v5/search/repositories`

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `q` | string | 搜索关键词（必填） |
| `sort` | string | 排序字段：stars_count、forks_count、watches_count、created_at、updated_at、last_push_at |
| `order` | string | 排序方向：asc、desc（默认） |
| `per_page` | integer | 每页条数（默认 20） |
| `page` | integer | 页码（默认 1） |
| `access_token` | string | Access Token |
| `search_mode` | string | 搜索模式：enhanced（增强模式） |

### 响应示例

```json
[
  {
    "id": 12345,
    "full_name": "owner/repo",
    "html_url": "https://gitee.com/owner/repo",
    "description": "A sample project",
    "stargazers_count": 1234,
    "forks_count": 567,
    "watchers_count": 890,
    "language": "Python",
    "created_at": "2024-01-15T10:00:00+08:00",
    "updated_at": "2026-06-18T15:30:00+08:00",
    "last_push_at": "2026-06-18T15:30:00+08:00",
    "namespace": {
      "id": 6789,
      "name": "owner",
      "path": "owner"
    },
    "public": true,
    "fork": false
  }
]
```

### 速率限制

| 认证状态 | 限制 |
|----------|------|
| 未认证 | 60 次/小时 |
| Token 认证 | 更高（根据用户等级） |

### 认证

```bash
# Access Token（Query 参数）
curl "https://gitee.com/api/v5/search/repositories?q=python&access_token=xxxx"

# Access Token（Header）
curl -H "Authorization: Bearer xxxx" \
  "https://gitee.com/api/v5/search/repositories?q=python"
```

### 响应头

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1624000000
```

### 特殊说明

- **未认证搜索可能返回空结果** — 建议设置 Token
- 响应时间较慢（约 10 秒）
- 国内访问速度快
- 中文项目优势

### 其他搜索端点

```
# 搜索用户
GET /api/v5/search/users?q=keyword

# 搜索组织
GET /api/v5/search/organizations?q=keyword

# 搜索代码
GET /api/v5/search/code?q=keyword
```

### 获取仓库详情

```
# 仓库详情
GET /api/v5/repos/:owner/:repo

# 仓库语言统计
GET /api/v5/repos/:owner/:repo/languages

# 仓库贡献者
GET /api/v5/repos/:owner/:repo/contributors
```

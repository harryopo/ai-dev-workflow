# GitLab API 参考

## 搜索项目

**端点：** `GET https://gitlab.com/api/v4/projects`

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `search` | string | 搜索关键词 |
| `order_by` | string | 排序字段：star_count、created_at、updated_at、last_activity_at、name、path |
| `sort` | string | 排序方向：asc、desc |
| `per_page` | integer | 每页条数，最大 100（默认 20） |
| `page` | integer | 页码（默认 1） |
| `visibility` | string | 可见性：public、internal、private |
| `owned` | boolean | 仅自己的项目 |
| `membership` | boolean | 仅自己是成员的项目 |
| `archived` | boolean | 是否包含归档项目 |
| `topic` | string | Topic 筛选（多个用逗号分隔） |
| `with_programming_language` | string | 编程语言筛选 |

### 响应示例

```json
[
  {
    "id": 12345,
    "name": "project-name",
    "path": "project-name",
    "path_with_namespace": "group/project-name",
    "description": "A sample project",
    "web_url": "https://gitlab.com/group/project-name",
    "star_count": 180,
    "forks_count": 48,
    "visibility": "public",
    "topics": ["react", "redux"],
    "created_at": "2024-01-15T10:00:00Z",
    "last_activity_at": "2026-06-18T15:30:00Z",
    "default_branch": "main",
    "namespace": {
      "id": 6789,
      "name": "group",
      "path": "group",
      "kind": "group"
    }
  }
]
```

### 速率限制

| 认证状态 | 限制 |
|----------|------|
| 未认证 | 500 次/10分钟 |
| Token 认证 | 更高（取决于计划） |

### 认证

```bash
# Private Token
curl -H "PRIVATE-TOKEN: glpat-xxxx" \
  "https://gitlab.com/api/v4/projects?search=react"

# OAuth2 Token
curl -H "Authorization: Bearer glpat-xxxx" \
  "https://gitlab.com/api/v4/projects?search=react"
```

### 响应头

```
ratelimit-limit: 500
ratelimit-remaining: 498
ratelimit-reset: 1624000000
```

### 特殊说明

- `language` 字段在列表接口经常为 null，需额外请求 `/api/v4/projects/:id/languages`
- 不支持 `stars:>N` 范围查询，需客户端筛选
- 无硬性结果数量上限（可深度翻页）
- 自建实例端点：`https://your-gitlab.com/api/v4/projects`

### 搜索替代端点

```
# 全局搜索
GET /api/v4/search?scope=projects&search=keyword

# 组内项目搜索
GET /api/v4/groups/:id/projects?search=keyword

# 用户项目搜索
GET /api/v4/users/:id/projects?search=keyword
```

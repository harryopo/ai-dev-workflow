# npm Registry API 参考

## 搜索包

**端点：** `GET https://registry.npmjs.org/-/v1/search`

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | string | 搜索关键词（必填） |
| `size` | integer | 每页条数，最大 250（默认 20） |
| `from` | integer | 偏移量（分页） |

### 搜索语法

#### 基本搜索

```
# 关键词搜索
react

# 多个关键词
react hooks

# 精确短语
"react hooks"
```

#### 限定符

```
# 作者
author:facebook

# 维护者
maintainer:gaearon

# 关键词
keyword:frontend

# 作用域包
@babel/core

# 版本
react@18.2.0
```

#### 权重调节

```
# 禁用精确匹配优先
boost-exact:false react

# 调整质量权重
popularity:0.5 quality:0.3 maintenance:0.2 react
```

### 响应示例

```json
{
  "total": 501597,
  "objects": [
    {
      "package": {
        "name": "react",
        "scope": "unscoped",
        "version": "19.2.7",
        "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
        "keywords": [
          "react"
        ],
        "date": "2026-06-01T10:00:00.000Z",
        "links": {
          "npm": "https://www.npmjs.com/package/react",
          "homepage": "https://react.dev",
          "repository": "https://github.com/facebook/react",
          "bugs": "https://github.com/facebook/react/issues"
        },
        "author": {
          "name": "Meta Platforms, Inc."
        },
        "publisher": {
          "username": "react-bot",
          "email": "react-bot@fb.com"
        },
        "maintainers": [
          {
            "username": "react-bot",
            "email": "react-bot@fb.com"
          }
        ]
      },
      "score": {
        "final": 0.95,
        "detail": {
          "quality": 0.97,
          "popularity": 0.92,
          "maintenance": 0.98
        }
      },
      "searchScore": 1234.5
    }
  ]
}
```

### 评分系统

| 维度 | 说明 | 计算方式 |
|------|------|----------|
| `quality` | 代码质量 | README 完整性、测试覆盖率、CI 状态 |
| `popularity` | 流行度 | 下载量、依赖数、GitHub Stars |
| `maintenance` | 维护频率 | 最近更新、Issue 响应、发布频率 |

### 速率限制

- 无明确公开速率限制
- 使用 CDN（Fastly），通常不会被限流
- 过度请求可能触发 429

### 认证

- 搜索 API 不需要认证
- 发布包需要 npm token

```bash
# 搜索
curl "https://registry.npmjs.org/-/v1/search?text=react&size=10"

# 获取包详情
curl "https://registry.npmjs.org/react"

# 获取特定版本
curl "https://registry.npmjs.org/react/18.2.0"
```

### 分页

```bash
# 第一页
curl "https://registry.npmjs.org/-/v1/search?text=react&size=20&from=0"

# 第二页
curl "https://registry.npmjs.org/-/v1/search?text=react&size=20&from=20"

# 遍历所有结果
while [ $from -lt $total ]; do
  curl "https://registry.npmjs.org/-/v1/search?text=react&size=200&from=$from"
  from=$((from + 200))
done
```

### 其他端点

```
# 包元数据
GET /:package

# 包版本列表
GET /:package

# 特定版本
GET /:package/:version

# 包的依赖
GET /:package/:version/dependencies
```

### 最佳实践

1. **使用 `size` 参数** — 减少请求次数
2. **缓存结果** — 包数据变化不频繁
3. **使用 `boost-exact:false`** — 获取更多相关结果
4. **结合评分筛选** — 优先选择 quality/popularity 高的包

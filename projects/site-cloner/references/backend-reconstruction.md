# 后端重建模式 — API 逆向工程指南

## 概述

当通过 Playwright 拦截到目标网站的 API 端点后，需要根据拦截数据重建一个功能等效的本地后端。本文档描述常见的后端重建模式和策略。

## API 模式识别

### 模式 1：RESTful CRUD

最常见的 API 模式。

```
GET    /api/resource        → 列表（支持 ?page=&limit= 分页）
GET    /api/resource/:id    → 详情
POST   /api/resource        → 创建
PUT    /api/resource/:id    → 更新
DELETE /api/resource/:id    → 删除
```

**重建策略：**
```javascript
// Express.js 重建
const express = require('express');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('./data/resource.json', 'utf-8'));

router.get('/api/resource', (req, res) => {
    const { page = 1, limit = 10 } = req.query;
    const start = (page - 1) * limit;
    res.json(data.slice(start, start + limit));
});

router.get('/api/resource/:id', (req, res) => {
    const item = data.find(i => i.id == req.params.id);
    item ? res.json(item) : res.status(404).json({ error: 'Not found' });
});

router.post('/api/resource', (req, res) => {
    const newItem = { id: data.length + 1, ...req.body };
    data.push(newItem);
    res.status(201).json(newItem);
});
```

### 模式 2：搜索/筛选 API

```
GET /api/search?q=keyword&category=xxx&sort=price
```

**重建策略：**
```javascript
router.get('/api/search', (req, res) => {
    const { q, category, sort } = req.query;
    let results = [...data];

    if (q) results = results.filter(i => i.name.includes(q));
    if (category) results = results.filter(i => i.category === category);
    if (sort === 'price') results.sort((a, b) => a.price - b.price);

    res.json(results);
});
```

### 模式 3：认证 API

```
POST /api/login     → { username, password } → { token, user }
POST /api/register  → { username, email, password } → { token, user }
GET  /api/me        → Authorization: Bearer xxx → { user }
```

**重建策略：**
```javascript
const jwt = require('jsonwebtoken');
const SECRET = 'local-dev-secret';

router.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    // 模拟认证：接受任意用户名/密码
    const token = jwt.sign({ username, id: Date.now() }, SECRET);
    res.json({ token, user: { id: 1, username } });
});

const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Unauthorized' });
    try {
        req.user = jwt.verify(token, SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
};

router.get('/api/me', authMiddleware, (req, res) => {
    res.json({ id: req.user.id, username: req.user.username });
});
```

### 模式 4：文件上传

```
POST /api/upload    → multipart/form-data { file } → { url: "/uploads/xxx.jpg" }
```

**重建策略：**
```javascript
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

router.post('/api/upload', upload.single('file'), (req, res) => {
    res.json({ url: `/uploads/${req.file.filename}` });
});
```

### 模式 5：分页/无限滚动

```
GET /api/items?page=1&limit=20    → { items: [...], total: 100, hasMore: true }
GET /api/items?cursor=xxx         → { items: [...], nextCursor: "yyy" }
```

**重建策略：**
```javascript
router.get('/api/items', (req, res) => {
    const { page = 1, limit = 20, cursor } = req.query;

    if (cursor) {
        // 基于游标的分页
        const idx = data.findIndex(i => i.id == cursor);
        const items = data.slice(idx + 1, idx + 1 + limit);
        res.json({ items, nextCursor: items.length === limit ? items[items.length - 1].id : null });
    } else {
        // 基于页码的分页
        const start = (page - 1) * limit;
        res.json({ items: data.slice(start, start + limit), total: data.length, hasMore: start + limit < data.length });
    }
});
```

## 数据推断

### 从 API 响应推断数据模型

```python
def infer_model(key, responses):
    """从多个 API 响应中推断数据模型"""
    all_keys = set()
    for resp in responses:
        if isinstance(resp, list):
            for item in resp:
                all_keys.update(item.keys())
        elif isinstance(resp, dict):
            all_keys.update(resp.keys())

    # 推断每个字段的类型
    model = {}
    for key in all_keys:
        types = set()
        for resp in responses:
            items = resp if isinstance(resp, list) else [resp]
            for item in items:
                if key in item:
                    types.add(type(item[key]).__name__)
        model[key] = list(types) if len(types) > 1 else list(types)[0]

    return model

# 示例输出：
# { "id": "int", "name": "str", "price": "float", "tags": "list", "active": "bool" }
```

### 从 URL 结构推断路由

| URL 模式 | 推断 | 后端路由 |
|----------|------|----------|
| `/api/users` | 用户资源列表 | `GET /api/users` |
| `/api/users/123` | 用户详情 | `GET /api/users/:id` |
| `/api/users/123/posts` | 用户的文章 | `GET /api/users/:id/posts` |
| `/api/products?category=电子` | 产品筛选 | `GET /api/products` + query 参数 |

## 特殊场景处理

### 场景 1：SSR 页面（Next.js getServerSideProps）

特征：HTML 中包含 `__NEXT_DATA__` 或 `<script id="__NEXT_DATA__">` 标签。

**处理方式：**
```javascript
// 从 HTML 中提取 SSR 数据
const html = await page.content();
const match = html.match(/<script id="__NEXT_DATA__"[^>]*>(.*?)<\/script>/);
if (match) {
    const ssrData = JSON.parse(match[1]);
    // ssrData.props.pageProps 包含服务端渲染的数据
    // 将这些数据存入对应的 JSON 文件
}
```

### 场景 2：GraphQL API

特征：POST 到 `/graphql`，请求体包含 `query` 和 `variables`。

**处理方式：**
```javascript
router.post('/graphql', (req, res) => {
    const { query, variables } = req.body;

    // 解析 query 中的字段名
    const fieldMatch = query.match(/\{[\s\n]*(\w+)/);
    if (fieldMatch) {
        const resourceName = fieldMatch[1]; // e.g., "users", "products"
        const data = JSON.parse(fs.readFileSync(`./data/${resourceName}.json`));
        res.json({ data: { [resourceName]: data } });
    }
});
```

### 场景 3：WebSocket 实时数据

特征：页面中有 `new WebSocket('wss://...')` 或 Socket.IO 连接。

**处理方式：**
```javascript
// 使用 Socket.IO 重建 WebSocket 服务
const { Server } = require('socket.io');
const io = new Server(httpServer);

io.on('connection', (socket) => {
    // 模拟实时数据推送
    setInterval(() => {
        const data = JSON.parse(fs.readFileSync('./data/realtime.json'));
        socket.emit('update', data);
    }, 5000);
});
```

### 场景 4：后端完全获取不到

当网站是纯 SSR（所有数据服务端渲染到 HTML 中）时：

1. **从页面展示结构推导**
   - 分析 HTML 中的列表项、卡片、表格行
   - 提取展示字段，推断数据模型

2. **从交互按钮推导**
   - "加载更多" → 分页 API
   - "筛选" → 搜索/过滤 API
   - "提交" → 创建 API
   - "删除" → 删除 API

3. **从 URL 模式推导**
   - `/post/123` → 文章详情
   - `/user/admin` → 用户主页
   - `/search?q=xxx` → 搜索

4. **生成最小可用后端**
   - 只生成页面加载所需的 API
   - 标注所有推断的端点
   - 确保页面能正常渲染和导航

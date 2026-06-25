"""
后端代码生成脚本
根据 API 分析结果，自动生成 Express.js 或 Flask 后端代码。
"""

import json
import sys
import shutil
from pathlib import Path
from string import Template


EXPRESS_SERVER_TEMPLATE = Template('''
const express = require('express');
const cors = require('cors');
const path = require('path');
$auth_import

const app = express();
const PORT = process.env.PORT || $port;

app.use(cors({ origin: '*' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use(express.static(path.join(__dirname, '../frontend')));

$route_imports

$auth_middleware

$routes

// 所有其他请求返回前端 index.html（SPA 支持）
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
''')

ROUTE_TEMPLATE = Template('''
const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '..', 'data');

function loadData(filename) {
    const filePath = path.join(dataDir, filename);
    if (!fs.existsSync(filePath)) return [];
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function saveData(filename, data) {
    const filePath = path.join(dataDir, filename);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

$endpoints

module.exports = router;
''')

PACKAGE_JSON_TEMPLATE = Template('''
{
  "name": "$name-backend",
  "version": "1.0.0",
  "description": "Auto-generated backend from site clone",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "node --watch server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
    $extra_deps
  }
}
''')


def generate_express_endpoint(ep):
    """为单个端点生成 Express 路由代码"""
    endpoint = ep['endpoint']
    methods = ep.get('methods', ['GET'])
    route_path = endpoint.replace(':id', ':id')
    resource_name = endpoint.strip('/').split('/')[-1].replace('-', '_')

    if resource_name in (':id', 'api'):
        resource_name = 'data'

    if 'query' in endpoint.lower() or 'search' in endpoint.lower():
        resource_name = endpoint.strip('/').split('/')[-1]

    fragments = []

    for method in methods:
        method_lower = method.lower()

        if method == 'GET':
            if ':id' in route_path:
                fragments.append(f"""
router.get('{route_path}', (req, res) => {{
    const data = loadData('{resource_name}.json');
    const item = Array.isArray(data)
        ? data.find(i => i.id == req.params.id || i._id == req.params.id)
        : data;
    if (item) {{
        res.json(item);
    }} else {{
        res.status(404).json({{ error: 'Not found' }});
    }}
}});
""")
            elif ep.get('query_params'):
                params = ep['query_params']
                filter_logic = ' && '.join(
                    [f"(!req.query.{p} || i.{p} == req.query.{p})" for p in params if p not in ('page', 'limit', 'sort', 'order')]
                ) or 'true'
                fragments.append(f"""
router.get('{route_path}', (req, res) => {{
    let data = loadData('{resource_name}.json');
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;

    // 筛选
    data = data.filter(i => {filter_logic});

    // 分页
    const total = data.length;
    const start = (page - 1) * limit;
    const items = data.slice(start, start + limit);

    res.json(items.length < total ? {{ items, total, page, hasMore: start + limit < total }} : items);
}});
""")
            else:
                fragments.append(f"""
router.get('{route_path}', (req, res) => {{
    const data = loadData('{resource_name}.json');
    res.json(data);
}});
""")

        elif method == 'POST':
            fragments.append(f"""
router.post('{route_path}', (req, res) => {{
    const data = loadData('{resource_name}.json');
    const newItem = {{ id: Date.now(), ...req.body, _created: new Date().toISOString() }};
    data.push(newItem);
    saveData('{resource_name}.json', data);
    res.status(201).json(newItem);
}});
""")

        elif method in ('PUT', 'PATCH'):
            fragments.append(f"""
router.{method_lower}('{route_path}', (req, res) => {{
    const data = loadData('{resource_name}.json');
    const idx = data.findIndex(i => i.id == req.params.id);
    if (idx === -1) return res.status(404).json({{ error: 'Not found' }});
    data[idx] = {{ ...data[idx], ...req.body, _updated: new Date().toISOString() }};
    saveData('{resource_name}.json', data);
    res.json(data[idx]);
}});
""")

        elif method == 'DELETE':
            fragments.append(f"""
router.delete('{route_path}', (req, res) => {{
    let data = loadData('{resource_name}.json');
    const idx = data.findIndex(i => i.id == req.params.id);
    if (idx === -1) return res.status(404).json({{ error: 'Not found' }});
    data.splice(idx, 1);
    saveData('{resource_name}.json', data);
    res.json({{ deleted: true }});
}});
""")

    return ''.join(fragments), resource_name


def save_data_files(endpoints, data_dir, api_calls_file=None):
    """从 API 响应中提取并保存数据文件"""
    data_dir.mkdir(parents=True, exist_ok=True)
    data_files = {}

    # 从 api_calls 文件加载原始数据
    if api_calls_file and Path(api_calls_file).exists():
        with open(api_calls_file, 'r', encoding='utf-8') as f:
            api_calls = json.load(f)

        for call in api_calls:
            if call.get('error') or not call.get('body'):
                continue

            body = call['body']
            if not isinstance(body, (list, dict)):
                continue

            url_path = call['url'].split('?')[0]
            parts = [p for p in url_path.split('/') if p and not p.isdigit()]

            if parts:
                name = parts[-1].replace('-', '_') if parts[-1] != 'api' else (parts[-2].replace('-', '_') if len(parts) > 1 else 'data')
            else:
                name = 'data'

            filename = f"{name}.json"
            filepath = data_dir / filename

            if isinstance(body, list):
                if filepath.exists():
                    existing = json.loads(filepath.read_text('utf-8'))
                    existing = [e for e in existing if e not in body]
                    body = existing + body
                filepath.write_text(json.dumps(body, ensure_ascii=False, indent=2), 'utf-8')
                data_files[name] = filename
            elif isinstance(body, dict) and not filepath.exists():
                filepath.write_text(json.dumps([body], ensure_ascii=False, indent=2), 'utf-8')
                data_files[name] = filename

    # 如果从 api_calls 中没有提取到数据，从 endpoint 的 sample_data 提取
    for ep in endpoints:
        if ep.get('sample_data'):
            resource_name = ep['endpoint'].strip('/').split('/')[-1].replace('-', '_')
            if resource_name in (':id', 'api'):
                continue

            filename = f"{resource_name}.json"
            filepath = data_dir / filename

            sample = ep['sample_data']
            if isinstance(sample, list):
                filepath.write_text(json.dumps(sample, ensure_ascii=False, indent=2), 'utf-8')
            elif isinstance(sample, dict):
                filepath.write_text(json.dumps([sample], ensure_ascii=False, indent=2), 'utf-8')
            data_files[resource_name] = filename

    return data_files


def reconstruct_backend(analysis_file, output_dir, api_calls_file=None, framework='express', port=3001):
    """主函数：根据 API 分析结果生成后端代码"""
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    endpoints = analysis.get('endpoints', [])
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    has_auth = any(ep.get('has_auth') for ep in endpoints)

    # 生成路由代码
    all_routes = []
    resource_names = set()

    for ep in endpoints:
        route_code, resource_name = generate_express_endpoint(ep)
        all_routes.append(f"// {ep['endpoint']} - {ep.get('api_type', '未知')}")
        all_routes.append(route_code)
        resource_names.add(resource_name)

    # 生成 server.js
    auth_import = "const jwt = require('jsonwebtoken');\nconst SECRET = 'local-dev-secret';" if has_auth else ""
    route_imports = "const apiRoutes = require('./routes/api');" if not has_auth else "const apiRoutes = require('./routes/api');\nconst authRoutes = require('./routes/auth');"
    auth_middleware = """
// 认证中间件（模拟）
const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return next(); // 本地开发允许无认证
    try {
        req.user = jwt.verify(token, SECRET);
    } catch {}
    next();
};
app.use(authMiddleware);
""" if has_auth else ""

    routes = "app.use('/api', apiRoutes);" if not has_auth else "app.use('/api', apiRoutes);\napp.use('/auth', authRoutes);"

    server_code = EXPRESS_SERVER_TEMPLATE.substitute(
        auth_import=auth_import,
        port=port,
        route_imports=route_imports,
        auth_middleware=auth_middleware,
        routes=routes
    )

    with open(output_dir / 'server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)

    # 生成路由文件
    routes_dir = output_dir / 'routes'
    routes_dir.mkdir(exist_ok=True)

    route_file_content = ROUTE_TEMPLATE.substitute(endpoints='\n'.join(all_routes))
    with open(routes_dir / 'api.js', 'w', encoding='utf-8') as f:
        f.write(route_file_content)

    if has_auth:
        with open(routes_dir / 'auth.js', 'w', encoding='utf-8') as f:
            f.write("""
const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const SECRET = 'local-dev-secret';

router.post('/login', (req, res) => {
    const { username, password } = req.body;
    const token = jwt.sign({ username, id: Date.now() }, SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: 1, username: username || 'user' } });
});

router.post('/register', (req, res) => {
    const { username, email, password } = req.body;
    const token = jwt.sign({ username, id: Date.now() }, SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: Date.now(), username, email } });
});

router.get('/me', (req, res) => {
    res.json({ id: 1, username: 'user' });
});

module.exports = router;
""")

    # 生成 package.json
    extra_deps = ',\n    "jsonwebtoken": "^9.0.0"' if has_auth else ''
    package_json = PACKAGE_JSON_TEMPLATE.substitute(
        name=Path(output_dir).parent.name,
        extra_deps=extra_deps
    )
    with open(output_dir / 'package.json', 'w', encoding='utf-8') as f:
        f.write(package_json)

    # 保存数据文件
    data_dir = output_dir / 'data'
    data_files = save_data_files(endpoints, data_dir, api_calls_file)

    # 生成中间件目录
    if has_auth:
        middleware_dir = output_dir / 'middleware'
        middleware_dir.mkdir(exist_ok=True)
        with open(middleware_dir / 'auth.js', 'w', encoding='utf-8') as f:
            f.write("""
const jwt = require('jsonwebtoken');
const SECRET = 'local-dev-secret';

module.exports = (req, res, next) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) {
        if (req.url === '/login' || req.url === '/register') return next();
        return res.status(401).json({ error: 'Unauthorized' });
    }
    try {
        req.user = jwt.verify(token, SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
};
""")

    print(f"后端代码已生成到: {output_dir}")
    print(f"  框架: {framework}")
    print(f"  端口: {port}")
    print(f"  路由数: {len(endpoints)}")
    print(f"  数据文件: {len(data_files)}")
    print(f"  认证: {'是' if has_auth else '否'}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python reconstruct_backend.py <analysis.json> <输出目录> [api_calls.json] [framework] [port]")
        print("示例: python reconstruct_backend.py ./api_analysis.json ./backend ./all_api_calls.json express 3001")
        sys.exit(1)

    analysis_file = sys.argv[1]
    output_dir = sys.argv[2]
    api_calls_file = sys.argv[3] if len(sys.argv) > 3 else None
    framework = sys.argv[4] if len(sys.argv) > 4 else 'express'
    port = int(sys.argv[5]) if len(sys.argv) > 5 else 3001

    reconstruct_backend(analysis_file, output_dir, api_calls_file, framework, port)

"""
API 端点分析脚本
从 Playwright 拦截的请求数据中提取 API 端点清单、请求/响应格式、数据模型。
"""

import json
import sys
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from collections import defaultdict


def load_api_calls(file_path):
    """加载 Playwright 拦截的 API 调用数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_endpoint(url, base_url):
    """从完整 URL 提取端点路径"""
    parsed = urlparse(url)
    path = parsed.path

    if parsed.netloc:
        try:
            base_parsed = urlparse(base_url)
        except Exception:
            return path

    return path


def normalize_endpoint(endpoint):
    """规范化端点路径：将 ID 参数替换为占位符"""
    # 替换纯数字路径段
    parts = endpoint.split('/')
    normalized_parts = []
    for part in parts:
        if part.isdigit():
            normalized_parts.append(':id')
        elif re.match(r'^[0-9a-f]{24,}$', part):  # MongoDB ObjectId
            normalized_parts.append(':id')
        elif re.match(r'^[0-9a-f-]{36}$', part):  # UUID
            normalized_parts.append(':id')
        else:
            normalized_parts.append(part)
    return '/'.join(normalized_parts)


def infer_http_method(endpoint, calls):
    """推断端点的 HTTP 方法"""
    methods = set()
    for call in calls:
        if call.get('error'):
            continue
        extracted = extract_endpoint(call['url'], '')
        norm = normalize_endpoint(extracted)
        if norm == endpoint:
            methods.add(call['method'])
    return list(methods) if methods else ['GET']


def infer_data_model(records):
    """从 API 响应数组推断数据模型"""
    if not records:
        return {}

    all_fields = set()
    field_types = defaultdict(set)

    for record in records:
        if isinstance(record, dict):
            for key, value in record.items():
                all_fields.add(key)
                field_types[key].add(type(value).__name__)

    model = {}
    for field in all_fields:
        types = field_types[field]
        model[field] = list(types)[0] if len(types) == 1 else list(types)

    return model


def analyze(file_path, base_url=""):
    """主分析函数"""
    calls = load_api_calls(file_path)

    if not calls:
        print("没有找到 API 调用数据")
        return {}

    # 按端点分组
    endpoint_groups = defaultdict(list)
    for call in calls:
        if call.get('error'):
            continue
        endpoint = extract_endpoint(call['url'], base_url)
        norm = normalize_endpoint(endpoint)
        endpoint_groups[norm].append(call)

    # 分析每个端点
    analysis = {
        'total_calls': len(calls),
        'unique_endpoints': len(endpoint_groups),
        'base_url': base_url,
        'endpoints': []
    }

    for endpoint, group_calls in sorted(endpoint_groups.items()):
        methods = list(set(c['method'] for c in group_calls if not c.get('error')))
        status_codes = list(set(c['status'] for c in group_calls if not c.get('error')))

        # 收集成功的响应
        success_responses = [
            c['body'] for c in group_calls
            if not c.get('error') and c.get('body') and c['status'] < 400
        ]

        # 推断数据模型
        model = None
        sample_data = None
        if success_responses:
            first = success_responses[0]
            if isinstance(first, list):
                model = infer_data_model(first)
                sample_data = first[:3]  # 取前 3 条作为样本
            elif isinstance(first, dict):
                model = infer_data_model([first])
                sample_data = first

        # 推断 API 类型
        api_type = []
        for method in methods:
            if method == 'GET' and endpoint.count(':id') == 0:
                api_type.append('列表查询')
            elif method == 'GET' and ':id' in endpoint:
                api_type.append('详情查询')
            elif method == 'POST':
                api_type.append('创建/提交')
            elif method in ('PUT', 'PATCH'):
                api_type.append('更新')
            elif method == 'DELETE':
                api_type.append('删除')

        # 分析查询参数
        query_params = set()
        for call in group_calls:
            if not call.get('error'):
                parsed = urlparse(call['url'])
                query_params.update(parse_qs(parsed.query).keys())

        endpoint_info = {
            'endpoint': endpoint,
            'methods': methods,
            'api_type': ' | '.join(api_type) if api_type else '未知',
            'status_codes': status_codes,
            'call_count': len(group_calls),
            'has_auth': any(
                'authorization' in c.get('request_headers', {}) or
                'x-auth-token' in c.get('request_headers', {})
                for c in group_calls
            ),
            'query_params': list(query_params),
            'data_model': model,
            'sample_data': sample_data,
            'raw_calls': group_calls[:2]  # 保留前 2 个调用供调试
        }

        analysis['endpoints'].append(endpoint_info)

    return analysis


def generate_route_code(endpoint_info, framework='express'):
    """根据端点信息生成路由代码骨架"""
    endpoint = endpoint_info['endpoint']
    methods = endpoint_info['methods']
    api_type = endpoint_info['api_type']

    fragments = []

    for method in methods:
        route_path = endpoint.replace(':id', ':id')
        method_lower = method.lower()

        if framework == 'express':
            if method == 'GET':
                fragments.append(f"""// {api_type}
router.get('{route_path}', (req, res) => {{
    const data = require('../data/{endpoint_info.get('resource_name', 'data')}.json');
    res.json(data);
}});""")
            elif method == 'POST':
                fragments.append(f"""// {api_type}
router.post('{route_path}', (req, res) => {{
    const newItem = {{ id: Date.now(), ...req.body }};
    res.status(201).json(newItem);
}});""")
            elif method in ('PUT', 'PATCH'):
                fragments.append(f"""// {api_type}
router.{method_lower}('{route_path}', (req, res) => {{
    res.json({{ ...req.body, id: req.params.id, updated: true }});
}});""")
            elif method == 'DELETE':
                fragments.append(f"""// {api_type}
router.delete('{route_path}', (req, res) => {{
    res.json({{ deleted: true, id: req.params.id }});
}});""")

    return '\n\n'.join(fragments)


def save_analysis(analysis, output_path):
    """保存分析结果"""
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python analyze_apis.py <api_calls.json> [base_url]")
        print("示例: python analyze_apis.py ./output/api_responses/all_api_calls.json https://example.com")
        sys.exit(1)

    input_file = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) > 2 else ""

    result = analyze(input_file, base_url)

    # 打印摘要
    print("=" * 50)
    print("API 分析结果")
    print("=" * 50)
    print(f"总 API 调用数: {result['total_calls']}")
    print(f"唯一端点数: {result['unique_endpoints']}")
    print()

    for ep in result['endpoints']:
        print(f"[{', '.join(ep['methods'])}] {ep['endpoint']}")
        print(f"  类型: {ep['api_type']}")
        print(f"  调用次数: {ep['call_count']}")
        print(f"  需要认证: {'是' if ep['has_auth'] else '否'}")
        if ep['query_params']:
            print(f"  查询参数: {', '.join(ep['query_params'])}")
        if ep['data_model']:
            fields = ', '.join(f"{k}: {v}" for k, v in ep['data_model'].items())
            print(f"  数据模型: {{ {fields} }}")
        print()

    # 保存分析结果
    output_path = Path(input_file).parent / 'api_analysis.json'
    save_analysis(result, output_path)
    print(f"分析结果已保存到: {output_path}")

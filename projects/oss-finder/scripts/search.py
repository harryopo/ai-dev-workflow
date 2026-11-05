#!/usr/bin/env python3
"""
OSS Finder - 全网开源项目搜索工具
支持 GitHub/GitLab/Gitee/npm/PyPI 多平台搜索
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import Optional


class PlatformAPI:
    """平台 API 基类"""

    def __init__(self, token: Optional[str] = None):
        self.token = token

    def search(self, query: str, **kwargs) -> dict:
        raise NotImplementedError

    def _request(self, url: str, headers: dict = None) -> dict:
        """发送 HTTP 请求"""
        if headers is None:
            headers = {}

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"⚠️  速率限制，请稍后重试或设置 Token", file=sys.stderr)
            elif e.code == 404:
                print(f"⚠️  资源不存在", file=sys.stderr)
            else:
                print(f"❌ HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
            return None
        except urllib.error.URLError as e:
            print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"❌ 请求失败: {e}", file=sys.stderr)
            return None


class GitHubAPI(PlatformAPI):
    """GitHub API"""

    BASE_URL = "https://api.github.com"

    def search(self, query: str, **kwargs) -> dict:
        # 构建搜索查询
        q_parts = [query]

        if kwargs.get('language'):
            q_parts.append(f"language:{kwargs['language']}")
        if kwargs.get('stars'):
            q_parts.append(f"stars:{kwargs['stars']}")
        if kwargs.get('topic'):
            q_parts.append(f"topic:{kwargs['topic']}")
        if kwargs.get('license'):
            q_parts.append(f"license:{kwargs['license']}")

        q = ' '.join(q_parts)

        params = {
            'q': q,
            'sort': kwargs.get('sort', 'stars'),
            'order': kwargs.get('order', 'desc'),
            'per_page': min(kwargs.get('limit', 20), 100)
        }

        url = f"{self.BASE_URL}/search/repositories?{urllib.parse.urlencode(params)}"

        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"

        data = self._request(url, headers)
        if not data:
            return None

        results = []
        for item in data.get('items', []):
            results.append({
                'name': item['full_name'],
                'url': item['html_url'],
                'stars': item['stargazers_count'],
                'forks': item['forks_count'],
                'language': item.get('language'),
                'description': item.get('description', ''),
                'topics': item.get('topics', []),
                'license': item.get('license', {}).get('spdx_id') if item.get('license') else None,
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'open_issues': item['open_issues_count']
            })

        return {
            'platform': 'github',
            'total': data['total_count'],
            'results': results
        }


class GitLabAPI(PlatformAPI):
    """GitLab API"""

    BASE_URL = "https://gitlab.com/api/v4"

    def search(self, query: str, **kwargs) -> dict:
        params = {
            'search': query,
            'order_by': kwargs.get('sort', 'star_count'),
            'sort': kwargs.get('order', 'desc'),
            'per_page': min(kwargs.get('limit', 20), 100)
        }

        url = f"{self.BASE_URL}/projects?{urllib.parse.urlencode(params)}"

        headers = {}
        if self.token:
            headers['PRIVATE-TOKEN'] = self.token

        data = self._request(url, headers)
        if not data:
            return None

        # 按 stars 筛选（GitLab API 不支持 stars 范围查询）
        min_stars = 0
        if kwargs.get('stars'):
            stars_str = kwargs['stars']
            if stars_str.startswith('>'):
                min_stars = int(stars_str[1:])

        results = []
        for item in data:
            if item.get('star_count', 0) < min_stars:
                continue

            results.append({
                'name': item['path_with_namespace'],
                'url': item['web_url'],
                'stars': item.get('star_count', 0),
                'forks': item.get('forks_count', 0),
                'language': None,  # GitLab 列表接口不返回 language
                'description': item.get('description', ''),
                'topics': item.get('topics', []),
                'license': None,
                'created_at': item['created_at'],
                'updated_at': item.get('last_activity_at', ''),
                'open_issues': 0
            })

        return {
            'platform': 'gitlab',
            'total': len(results),
            'results': results
        }


class GiteeAPI(PlatformAPI):
    """Gitee API"""

    BASE_URL = "https://gitee.com/api/v5"

    def search(self, query: str, **kwargs) -> dict:
        params = {
            'q': query,
            'sort': kwargs.get('sort', 'stars_count'),
            'order': kwargs.get('order', 'desc'),
            'per_page': min(kwargs.get('limit', 20), 100)
        }

        if self.token:
            params['access_token'] = self.token

        url = f"{self.BASE_URL}/search/repositories?{urllib.parse.urlencode(params)}"

        data = self._request(url)
        if not data:
            return None

        results = []
        for item in data:
            results.append({
                'name': item['full_name'],
                'url': item['html_url'],
                'stars': item.get('stargazers_count', 0),
                'forks': item.get('forks_count', 0),
                'language': item.get('language'),
                'description': item.get('description', ''),
                'topics': [],
                'license': None,
                'created_at': item.get('created_at', ''),
                'updated_at': item.get('updated_at', ''),
                'open_issues': 0
            })

        return {
            'platform': 'gitee',
            'total': len(results),
            'results': results
        }


class NpmAPI(PlatformAPI):
    """npm Registry API"""

    BASE_URL = "https://registry.npmjs.org"

    def search(self, query: str, **kwargs) -> dict:
        params = {
            'text': query,
            'size': min(kwargs.get('limit', 20), 250)
        }

        url = f"{self.BASE_URL}/-/v1/search?{urllib.parse.urlencode(params)}"

        data = self._request(url)
        if not data:
            return None

        results = []
        for item in data.get('objects', []):
            pkg = item.get('package', {})
            score = item.get('score', {}).get('detail', {})

            # 从 links 获取仓库信息
            repo_url = None
            links = pkg.get('links', {})
            if links.get('repository'):
                repo_url = links['repository']
            elif links.get('homepage'):
                repo_url = links['homepage']

            results.append({
                'name': pkg['name'],
                'url': repo_url or f"https://www.npmjs.com/package/{pkg['name']}",
                'stars': 0,  # npm API 不返回 stars
                'forks': 0,
                'language': 'JavaScript',
                'description': pkg.get('description', ''),
                'topics': pkg.get('keywords', []),
                'license': None,
                'version': pkg.get('version'),
                'quality': score.get('quality', 0),
                'popularity': score.get('popularity', 0),
                'maintenance': score.get('maintenance', 0),
                'updated_at': pkg.get('date', '')
            })

        return {
            'platform': 'npm',
            'total': data.get('total', len(results)),
            'results': results
        }


class PyPIAPI(PlatformAPI):
    """PyPI API（仅支持按包名查询，不支持搜索）"""

    BASE_URL = "https://pypi.org"

    def search(self, query: str, **kwargs) -> dict:
        # PyPI 没有搜索 API，只能按包名查询
        url = f"{self.BASE_URL}/pypi/{query}/json"

        data = self._request(url)
        if not data:
            return None

        info = data.get('info', {})
        results = [{
            'name': info['name'],
            'url': info.get('home_page') or info.get('project_urls', {}).get('Source', ''),
            'stars': 0,
            'forks': 0,
            'language': 'Python',
            'description': info.get('summary', ''),
            'topics': info.get('keywords', '').split(',') if info.get('keywords') else [],
            'license': info.get('license'),
            'version': info.get('version'),
            'author': info.get('author'),
            'requires_python': info.get('requires_python'),
            'updated_at': ''
        }]

        return {
            'platform': 'pypi',
            'total': 1,
            'results': results
        }


def get_api(platform: str, token: Optional[str] = None) -> PlatformAPI:
    """获取平台 API 实例"""
    apis = {
        'github': GitHubAPI,
        'gitlab': GitLabAPI,
        'gitee': GiteeAPI,
        'npm': NpmAPI,
        'pypi': PyPIAPI
    }

    if platform not in apis:
        print(f"❌ 不支持的平台: {platform}", file=sys.stderr)
        return None

    return apis[platform](token)


def format_markdown(data: dict, query: str) -> str:
    """格式化为 Markdown"""
    if not data or not data.get('results'):
        return f"## 搜索结果：{query}\n\n未找到结果。"

    platform = data['platform']
    total = data['total']
    results = data['results']

    lines = [
        f"## 搜索结果：{query}",
        f"",
        f"共找到 {total} 个项目（来源：{platform}）",
        f"",
        f"| # | 项目 | Stars | Language | 描述 |",
        f"|---|------|-------|----------|------|"
    ]

    for i, item in enumerate(results, 1):
        name = item['name']
        url = item['url']
        stars = item.get('stars', 0)
        language = item.get('language') or '-'
        desc = (item.get('description') or '-')[:60]

        # 格式化 stars
        if stars >= 1000:
            stars_str = f"{stars/1000:.0f}k"
        else:
            stars_str = str(stars)

        lines.append(f"| {i} | [{name}]({url}) | {stars_str} | {language} | {desc} |")

    return '\n'.join(lines)


def format_json(data: dict, query: str) -> str:
    """格式化为 JSON"""
    output = {
        'query': query,
        'platform': data.get('platform'),
        'total': data.get('total', 0),
        'results': data.get('results', [])
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def save_results(data: dict, query: str, output_dir: str):
    """保存结果到文件"""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_query = query.replace(' ', '_')[:30]

    # 保存 JSON
    json_path = os.path.join(output_dir, f"{safe_query}-{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(format_json(data, query))

    # 保存 Markdown
    md_path = os.path.join(output_dir, f"{safe_query}-{timestamp}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(format_markdown(data, query))

    # 更新 latest.json
    latest_path = os.path.join(output_dir, "latest.json")
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(format_json(data, query))

    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(description='OSS Finder - 全网开源项目搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--platform', '-p', default='github',
                        choices=['github', 'gitlab', 'gitee', 'npm', 'pypi', 'all'],
                        help='搜索平台 (默认: github)')
    parser.add_argument('--language', '-l', help='编程语言筛选')
    parser.add_argument('--stars', '-s', help='Stars 筛选，如 ">100"、"100..1000"')
    parser.add_argument('--topic', '-t', help='Topic 标签筛选')
    parser.add_argument('--license', help='许可证筛选')
    parser.add_argument('--sort', default='stars',
                        choices=['stars', 'forks', 'updated', 'relevance'],
                        help='排序方式 (默认: stars)')
    parser.add_argument('--order', default='desc', choices=['asc', 'desc'],
                        help='排序方向 (默认: desc)')
    parser.add_argument('--limit', '-n', type=int, default=20,
                        help='返回数量 (默认: 20)')
    parser.add_argument('--format', '-f', default='markdown',
                        choices=['markdown', 'json', 'table'],
                        help='输出格式 (默认: markdown)')
    parser.add_argument('--output', '-o', help='输出目录')
    parser.add_argument('--save', action='store_true', help='保存结果到文件')

    args = parser.parse_args()

    # 获取 Token
    tokens = {
        'github': os.environ.get('GITHUB_TOKEN'),
        'gitlab': os.environ.get('GITLAB_TOKEN'),
        'gitee': os.environ.get('GITEE_TOKEN')
    }

    # 搜索参数
    search_kwargs = {
        'language': args.language,
        'stars': args.stars,
        'topic': args.topic,
        'license': args.license,
        'sort': args.sort,
        'order': args.order,
        'limit': args.limit
    }

    # 执行搜索
    all_results = []

    if args.platform == 'all':
        # 跨平台搜索
        platforms = ['github', 'gitlab', 'gitee', 'npm']
        for platform in platforms:
            print(f"🔍 搜索 {platform}...", file=sys.stderr)
            api = get_api(platform, tokens.get(platform))
            if api:
                result = api.search(args.query, **search_kwargs)
                if result and result.get('results'):
                    all_results.extend(result['results'])

        # 合并结果
        data = {
            'platform': 'all',
            'total': len(all_results),
            'results': all_results
        }
    else:
        # 单平台搜索
        api = get_api(args.platform, tokens.get(args.platform))
        if not api:
            sys.exit(1)

        data = api.search(args.query, **search_kwargs)
        if not data:
            print("❌ 搜索失败", file=sys.stderr)
            sys.exit(1)

    # 输出结果（处理编码问题）
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if args.format == 'json':
        print(format_json(data, args.query))
    else:
        print(format_markdown(data, args.query))

    # 保存结果
    if args.save:
        output_dir = args.output or os.path.join('output', 'oss-finder')
        json_path, md_path = save_results(data, args.query, output_dir)
        print(f"\n📁 结果已保存:", file=sys.stderr)
        print(f"   JSON: {json_path}", file=sys.stderr)
        print(f"   Markdown: {md_path}", file=sys.stderr)


if __name__ == '__main__':
    main()

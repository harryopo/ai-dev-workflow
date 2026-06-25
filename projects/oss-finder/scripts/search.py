#!/usr/bin/env python3
"""
OSS Finder - 全网开源项目搜索工具
支持 GitHub/GitLab/Gitee/npm/PyPI 多平台搜索

优化特性：
- gh CLI 优先（实时数据）
- 并发搜索（ThreadPoolExecutor）
- 本地缓存（1小时 TTL）
- 自动重试（指数退避）
- 结果去重
- 分页支持
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# ============================================================
# 缓存系统
# ============================================================

CACHE_DIR = Path.home() / '.cache' / 'oss-finder'
CACHE_TTL = timedelta(hours=1)


def _cache_key(query: str, platform: str, **kwargs) -> str:
    """生成缓存键"""
    parts = [query, platform]
    for k in sorted(kwargs.keys()):
        if kwargs[k] is not None:
            parts.append(f"{k}={kwargs[k]}")
    return hashlib.md5('|'.join(parts).encode()).hexdigest()


def _cache_get(key: str) -> Optional[dict]:
    """读取缓存"""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        cached_at = datetime.fromisoformat(data['_cached_at'])
        if datetime.now() - cached_at > CACHE_TTL:
            cache_file.unlink()  # 过期删除
            return None
        return data
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def _cache_set(key: str, data: dict):
    """写入缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data['_cached_at'] = datetime.now().isoformat()
    cache_file = CACHE_DIR / f"{key}.json"
    cache_file.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


# ============================================================
# 重试机制
# ============================================================

def _retry(func, max_retries=3, base_delay=1.0):
    """带指数退避的重试装饰器"""
    def wrapper(*args, **kwargs):
        last_error = None
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    return result
                # None 表示失败，但不是异常
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⚠️  请求失败，{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...", file=sys.stderr)
                    time.sleep(delay)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⚠️  请求异常: {e}，{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...", file=sys.stderr)
                    time.sleep(delay)
        return None
    return wrapper


# ============================================================
# HTTP 请求基类
# ============================================================

class PlatformAPI:
    """平台 API 基类"""

    def __init__(self, token: Optional[str] = None):
        self.token = token

    def search(self, query: str, **kwargs) -> dict:
        raise NotImplementedError

    def _request(self, url: str, headers: dict = None) -> dict:
        """发送 HTTP 请求（带重试）"""
        return _retry(self._do_request)(url, headers)

    def _do_request(self, url: str, headers: dict = None) -> dict:
        """实际发送 HTTP 请求"""
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
            elif e.code >= 500:
                print(f"⚠️  服务端错误 {e.code}，将重试", file=sys.stderr)
                raise  # 触发重试
            else:
                print(f"❌ HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
            return None
        except urllib.error.URLError as e:
            print(f"❌ 网络错误: {e.reason}", file=sys.stderr)
            return None


# ============================================================
# GitHub CLI (gh) 搜索
# ============================================================

class GitHubCLI:
    """GitHub CLI (gh) 搜索 — 优先使用，获取实时数据"""

    @staticmethod
    def is_available() -> bool:
        """检查 gh CLI 是否可用且已认证"""
        try:
            result = subprocess.run(
                ['gh', 'auth', 'status'],
                capture_output=True, text=True, timeout=10,
                encoding='utf-8', errors='replace'
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def search(query: str, **kwargs) -> Optional[dict]:
        """使用 gh search repos 搜索，返回实时数据"""
        cmd = ['gh', 'search', 'repos', query]

        # 筛选参数
        if kwargs.get('language'):
            cmd.extend(['--language', kwargs['language']])
        if kwargs.get('stars'):
            cmd.extend(['--stars', kwargs['stars']])
        if kwargs.get('topic'):
            cmd.extend(['--topic', kwargs['topic']])
        if kwargs.get('license'):
            cmd.extend(['--license', kwargs['license']])
        if kwargs.get('created_after'):
            # gh CLI 需要 >=YYYY-MM-DD 格式
            date = kwargs['created_after']
            if not date.startswith('>='):
                date = f">={date}"
            cmd.extend(['--created', date])
        if kwargs.get('sort'):
            sort_map = {'stars': 'stars', 'forks': 'forks', 'updated': 'updated'}
            cmd.extend(['--sort', sort_map.get(kwargs['sort'], 'stars')])
        if kwargs.get('order'):
            cmd.extend(['--order', kwargs['order']])
        if kwargs.get('limit'):
            cmd.extend(['--limit', str(min(kwargs['limit'], 1000))])

        # JSON 输出字段
        cmd.extend(['--json',
                    'fullName,url,stargazersCount,forksCount,language,description,license,createdAt,updatedAt,openIssuesCount'])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                print(f"⚠️  gh CLI 搜索失败: {result.stderr.strip()}", file=sys.stderr)
                return None

            items = json.loads(result.stdout)
            results = []
            for item in items:
                license_info = item.get('license')
                if isinstance(license_info, dict):
                    license_id = license_info.get('spdxId') or license_info.get('key')
                elif isinstance(license_info, str):
                    license_id = license_info
                else:
                    license_id = None

                results.append({
                    'name': item.get('fullName', ''),
                    'url': item.get('url', ''),
                    'stars': item.get('stargazersCount', 0),
                    'forks': item.get('forksCount', 0),
                    'language': item.get('language'),
                    'description': item.get('description', ''),
                    'topics': [],  # gh CLI 不返回 topics
                    'license': license_id,
                    'created_at': item.get('createdAt', ''),
                    'updated_at': item.get('updatedAt', ''),
                    'open_issues': item.get('openIssuesCount', 0)
                })

            return {
                'platform': 'github',
                'source': 'gh-cli',
                'total': len(results),
                'results': results
            }

        except subprocess.TimeoutExpired:
            print("⚠️  gh CLI 搜索超时", file=sys.stderr)
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️  gh CLI 输出解析失败: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"⚠️  gh CLI 搜索异常: {e}", file=sys.stderr)
            return None


# ============================================================
# 各平台 API 实现
# ============================================================

class GitHubAPI(PlatformAPI):
    """GitHub API — gh CLI 不可用时的降级方案"""

    BASE_URL = "https://api.github.com"

    def search(self, query: str, **kwargs) -> dict:
        # 优先尝试 gh CLI
        if GitHubCLI.is_available():
            print("🔍 使用 gh CLI 搜索（实时数据）...", file=sys.stderr)
            result = GitHubCLI.search(query, **kwargs)
            if result:
                return result
            print("⚠️  gh CLI 搜索失败，降级到 API...", file=sys.stderr)

        # 降级：REST API
        print("🔍 使用 GitHub API 搜索...", file=sys.stderr)

        q_parts = [query]
        if kwargs.get('language'):
            q_parts.append(f"language:{kwargs['language']}")
        if kwargs.get('stars'):
            q_parts.append(f"stars:{kwargs['stars']}")
        if kwargs.get('topic'):
            q_parts.append(f"topic:{kwargs['topic']}")
        if kwargs.get('license'):
            q_parts.append(f"license:{kwargs['license']}")
        if kwargs.get('created_after'):
            q_parts.append(f"created:{kwargs['created_after']}")

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
            'source': 'rest-api',
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
                'language': None,
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

            repo_url = None
            links = pkg.get('links', {})
            if links.get('repository'):
                repo_url = links['repository']
            elif links.get('homepage'):
                repo_url = links['homepage']

            downloads = self._get_downloads(pkg['name'])

            results.append({
                'name': pkg['name'],
                'url': repo_url or f"https://www.npmjs.com/package/{pkg['name']}",
                'stars': 0,
                'forks': 0,
                'language': 'JavaScript',
                'description': pkg.get('description', ''),
                'topics': pkg.get('keywords', []),
                'license': None,
                'version': pkg.get('version'),
                'quality': score.get('quality', 0),
                'popularity': score.get('popularity', 0),
                'maintenance': score.get('maintenance', 0),
                'downloads_weekly': downloads,
                'updated_at': pkg.get('date', '')
            })

        return {
            'platform': 'npm',
            'total': data.get('total', len(results)),
            'results': results
        }

    def _get_downloads(self, package: str) -> int:
        """获取包的最近一周下载量"""
        url = f"https://api.npmjs.org/downloads/point/last-week/{urllib.parse.quote(package, safe='')}"
        data = self._request(url)
        return data.get('downloads', 0) if data else 0


class PyPIAPI(PlatformAPI):
    """PyPI API — 支持搜索（通过 libraries.io）和按包名查询"""

    BASE_URL = "https://pypi.org"

    def search(self, query: str, **kwargs) -> dict:
        libs_key = os.environ.get('LIBRARIES_IO_KEY')
        if libs_key:
            return self._search_via_libraries_io(query, libs_key, **kwargs)
        return self._search_by_name(query)

    def _search_via_libraries_io(self, query: str, api_key: str, **kwargs) -> dict:
        """通过 libraries.io API 搜索 PyPI 包"""
        limit = min(kwargs.get('limit', 20), 100)
        params = {
            'q': query,
            'api_key': api_key,
            'platforms': 'Pypi',
            'per_page': limit
        }
        url = f"https://libraries.io/api/search?{urllib.parse.urlencode(params)}"

        data = self._request(url)
        if not data:
            return self._search_by_name(query)

        results = []
        for item in data:
            name = item.get('name', '')
            pypi_info = self._get_pypi_info(name)
            downloads = self._get_pypi_downloads(name)

            results.append({
                'name': name,
                'url': item.get('homepage') or item.get('repository_url') or f"https://pypi.org/project/{name}/",
                'stars': item.get('stars', 0),
                'forks': item.get('forks', 0),
                'language': 'Python',
                'description': item.get('description') or (pypi_info.get('summary', '') if pypi_info else ''),
                'topics': item.get('keywords', []) or [],
                'license': item.get('normalized_licenses', [None])[0] if item.get('normalized_licenses') else None,
                'version': pypi_info.get('version') if pypi_info else item.get('latest_release_number'),
                'downloads_monthly': downloads,
                'updated_at': item.get('latest_release_published_at', '')
            })

        return {
            'platform': 'pypi',
            'total': len(results),
            'results': results
        }

    def _search_by_name(self, query: str) -> dict:
        """按包名精确查询"""
        url = f"{self.BASE_URL}/pypi/{query}/json"

        data = self._request(url)
        if not data:
            return None

        info = data.get('info', {})
        downloads = self._get_pypi_downloads(query)

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
            'downloads_monthly': downloads,
            'updated_at': ''
        }]

        return {
            'platform': 'pypi',
            'total': 1,
            'results': results
        }

    def _get_pypi_info(self, package: str) -> dict:
        url = f"{self.BASE_URL}/pypi/{package}/json"
        data = self._request(url)
        return data.get('info', {}) if data else {}

    def _get_pypi_downloads(self, package: str) -> int:
        url = f"https://pypistats.org/api/packages/{urllib.parse.quote(package, safe='')}/recent"
        data = self._request(url)
        if data and data.get('data'):
            return data['data'].get('last_month', 0)
        return 0


# ============================================================
# 核心函数
# ============================================================

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


def _dedup_results(results: list) -> list:
    """按项目 URL 去重"""
    seen = set()
    deduped = []
    for item in results:
        url = item.get('url', '')
        # 标准化 URL（去掉末尾斜杠和协议）
        normalized = url.rstrip('/').replace('https://', '').replace('http://', '')
        if normalized not in seen:
            seen.add(normalized)
            deduped.append(item)
    return deduped


def _format_number(n: int) -> str:
    """格式化大数字（1234 → 1.2k）"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


def format_markdown(data: dict, query: str) -> str:
    """格式化为 Markdown"""
    if not data or not data.get('results'):
        return f"## 搜索结果：{query}\n\n未找到结果。"

    platform = data['platform']
    total = data['total']
    results = data['results']
    source = data.get('source', '')

    source_tag = f"（数据来源：{source}）" if source else ""

    has_npm_downloads = any(r.get('downloads_weekly') for r in results)
    has_pypi_downloads = any(r.get('downloads_monthly') for r in results)

    if has_npm_downloads:
        lines = [
            f"## 搜索结果：{query}",
            f"",
            f"共找到 {total} 个项目（来源：{platform}）{source_tag}",
            f"",
            f"| # | 项目 | ⬇️ 周下载 | Language | 描述 |",
            f"|---|------|----------|----------|------|"
        ]
        for i, item in enumerate(results, 1):
            name = item['name']
            url = item['url']
            dl = _format_number(item.get('downloads_weekly', 0))
            language = item.get('language') or '-'
            desc = (item.get('description') or '-')[:60]
            lines.append(f"| {i} | [{name}]({url}) | {dl} | {language} | {desc} |")
    elif has_pypi_downloads:
        lines = [
            f"## 搜索结果：{query}",
            f"",
            f"共找到 {total} 个项目（来源：{platform}）{source_tag}",
            f"",
            f"| # | 项目 | ⬇️ 月下载 | Language | 描述 |",
            f"|---|------|----------|----------|------|"
        ]
        for i, item in enumerate(results, 1):
            name = item['name']
            url = item['url']
            dl = _format_number(item.get('downloads_monthly', 0))
            language = item.get('language') or '-'
            desc = (item.get('description') or '-')[:60]
            lines.append(f"| {i} | [{name}]({url}) | {dl} | {language} | {desc} |")
    else:
        lines = [
            f"## 搜索结果：{query}",
            f"",
            f"共找到 {total} 个项目（来源：{platform}）{source_tag}",
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
            stars_str = _format_number(stars)
            lines.append(f"| {i} | [{name}]({url}) | {stars_str} | {language} | {desc} |")

    return '\n'.join(lines)


def format_table(data: dict, query: str) -> str:
    """格式化为纯文本表格（适合终端）"""
    if not data or not data.get('results'):
        return f"搜索结果：{query}\n\n未找到结果。"

    results = data['results']
    has_downloads = any(r.get('downloads_weekly') or r.get('downloads_monthly') for r in results)

    # 计算列宽
    name_width = max(len(r['name']) for r in results[:20])
    name_width = min(name_width, 40)

    if has_downloads:
        header = f"{'#':>3}  {'项目':<{name_width}}  {'下载量':>10}  {'Language':<12}  描述"
        sep = f"{'---':>3}  {'-'*name_width}  {'----------':>10}  {'-'*12}  ----"
    else:
        header = f"{'#':>3}  {'项目':<{name_width}}  {'Stars':>10}  {'Language':<12}  描述"
        sep = f"{'---':>3}  {'-'*name_width}  {'----------':>10}  {'-'*12}  ----"

    lines = [
        f"搜索结果：{query}",
        f"共找到 {data['total']} 个项目（来源：{data['platform']}）",
        "",
        header,
        sep
    ]

    for i, item in enumerate(results, 1):
        name = item['name']
        language = item.get('language') or '-'
        desc = (item.get('description') or '-')[:50]

        if has_downloads:
            dl = item.get('downloads_weekly') or item.get('downloads_monthly', 0)
            lines.append(f"{i:>3}  {name:<{name_width}}  {_format_number(dl):>10}  {language:<12}  {desc}")
        else:
            stars = item.get('stars', 0)
            lines.append(f"{i:>3}  {name:<{name_width}}  {_format_number(stars):>10}  {language:<12}  {desc}")

    return '\n'.join(lines)


def format_json(data: dict, query: str) -> str:
    """格式化为 JSON"""
    output = {
        'query': query,
        'platform': data.get('platform'),
        'source': data.get('source', ''),
        'total': data.get('total', 0),
        'results': data.get('results', [])
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def save_results(data: dict, query: str, output_dir: str):
    """保存结果到文件"""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_query = query.replace(' ', '_')[:30]

    json_path = os.path.join(output_dir, f"{safe_query}-{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(format_json(data, query))

    md_path = os.path.join(output_dir, f"{safe_query}-{timestamp}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(format_markdown(data, query))

    latest_path = os.path.join(output_dir, "latest.json")
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(format_json(data, query))

    return json_path, md_path


# ============================================================
# 并发搜索
# ============================================================

def search_platform(platform: str, query: str, tokens: dict, **kwargs) -> Optional[dict]:
    """搜索单个平台（带缓存）"""
    # 检查缓存
    cache_key = _cache_key(query, platform, **kwargs)
    cached = _cache_get(cache_key)
    if cached:
        print(f"✅ {platform} 使用缓存", file=sys.stderr)
        return cached

    api = get_api(platform, tokens.get(platform))
    if not api:
        return None

    result = api.search(query, **kwargs)
    if result and result.get('results'):
        _cache_set(cache_key, result)
    return result


def search_all_platforms(query: str, tokens: dict, **kwargs) -> dict:
    """并发搜索所有平台"""
    platforms = ['github', 'gitlab', 'gitee', 'npm']
    all_results = []

    print(f"🔍 并发搜索 {len(platforms)} 个平台...", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(search_platform, p, query, tokens, **kwargs): p
            for p in platforms
        }

        for future in as_completed(futures):
            platform = futures[future]
            try:
                result = future.result()
                if result and result.get('results'):
                    count = len(result['results'])
                    print(f"  ✅ {platform}: {count} 个结果", file=sys.stderr)
                    all_results.extend(result['results'])
                else:
                    print(f"  ⚠️  {platform}: 无结果", file=sys.stderr)
            except Exception as e:
                print(f"  ❌ {platform}: {e}", file=sys.stderr)

    # 去重
    deduped = _dedup_results(all_results)
    if len(deduped) < len(all_results):
        print(f"  🔄 去重: {len(all_results)} → {len(deduped)}", file=sys.stderr)

    return {
        'platform': 'all',
        'total': len(deduped),
        'results': deduped
    }


# ============================================================
# CLI 入口
# ============================================================

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
    parser.add_argument('--created-after', help='创建日期筛选，如 "2024-01-01"')
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
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')

    args = parser.parse_args()

    # 获取 Token
    tokens = {
        'github': os.environ.get('GITHUB_TOKEN'),
        'gitlab': os.environ.get('GITLAB_TOKEN'),
        'gitee': os.environ.get('GITEE_TOKEN'),
        'libraries_io': os.environ.get('LIBRARIES_IO_KEY')
    }

    # 搜索参数
    search_kwargs = {
        'language': args.language,
        'stars': args.stars,
        'topic': args.topic,
        'license': args.license,
        'created_after': args.created_after,
        'sort': args.sort,
        'order': args.order,
        'limit': args.limit
    }

    # 执行搜索
    if args.platform == 'all':
        data = search_all_platforms(args.query, tokens, **search_kwargs)
    else:
        if args.no_cache:
            # 禁用缓存时直接搜索
            api = get_api(args.platform, tokens.get(args.platform))
            if not api:
                sys.exit(1)
            data = api.search(args.query, **search_kwargs)
        else:
            data = search_platform(args.platform, args.query, tokens, **search_kwargs)

        if not data:
            print("❌ 搜索失败", file=sys.stderr)
            sys.exit(1)

    # 输出结果
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if args.format == 'json':
        print(format_json(data, args.query))
    elif args.format == 'table':
        print(format_table(data, args.query))
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

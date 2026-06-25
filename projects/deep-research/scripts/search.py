#!/usr/bin/env python3
"""
Deep Research — 多源搜索引擎 v2.0
整合 DuckDuckGo（免费）+ Tavily（AI 搜索）+ Jina（网页提取）+ SearXNG（元搜索）

架构设计：
┌─────────────────────────────────────────────────────────────┐
│                    Deep Research 搜索引擎                      │
├─────────────────────────────────────────────────────────────┤
│  免费层（无需配置）                                             │
│  ├── DuckDuckGo    网页搜索，国内可用                          │
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

数据来源：
- DuckDuckGo: https://github.com/deedy5/ddgs (MIT)
- Tavily: https://tavily.com (商业，有免费额度)
- Jina: https://jina.ai (商业，有免费额度)
- SearXNG: https://github.com/searxng/searxng (AGPL-3.0)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Any
import subprocess


# ============================================================
# 网络环境检测
# ============================================================

def check_network() -> Dict[str, bool]:
    """检测网络环境，判断能否访问国际服务"""
    results = {
        'can_access_google': False,
        'can_access_jina': False,
        'can_access_tavily': False,
        'has_vpn': False
    }

    # 测试 Google
    try:
        req = urllib.request.Request('https://www.google.com', method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=5) as response:
            results['can_access_google'] = True
    except:
        pass

    # 测试 Jina
    try:
        req = urllib.request.Request('https://r.jina.ai', method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            results['can_access_jina'] = True
    except:
        pass

    # 测试 Tavily
    try:
        req = urllib.request.Request('https://api.tavily.com', method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            results['can_access_tavily'] = True
    except:
        pass

    # 判断是否有 VPN（能访问 Google 通常意味着有 VPN）
    results['has_vpn'] = results['can_access_google']

    return results


# ============================================================
# DuckDuckGo 搜索（免费，国内可用）
# ============================================================

class DuckDuckGoSearch:
    """DuckDuckGo 搜索 — 免费，无需 API Key，国内可用"""

    def __init__(self):
        self._available = None

    def is_available(self) -> bool:
        """检查 ddgs 是否已安装"""
        if self._available is None:
            try:
                import ddgs
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def search(self, query: str, max_results: int = 10,
               region: Optional[str] = None, safesearch: str = 'moderate',
               timelimit: Optional[str] = None) -> Optional[Dict]:
        """
        搜索网页

        Args:
            query: 搜索关键词
            max_results: 最大结果数
            region: 地区（wt-wt=全球, cn-zh=中国, us-en=美国）
                    默认自动检测：国内网络用 cn-zh，否则用 wt-wt
            safesearch: 安全搜索（off/moderate/strict）
            timelimit: 时间限制（d=天, w=周, m=月, y=年）
        """
        if not self.is_available():
            print("⚠️  ddgs 未安装，请运行: pip install ddgs", file=sys.stderr)
            return None

        # 自动检测区域
        if region is None:
            # 尝试全球搜索，失败则用中国区域
            region = 'cn-zh'  # 默认用中国区域，国内更稳定

        try:
            from ddgs import DDGS

            results = DDGS().text(
                query,
                max_results=max_results,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit
            )

            formatted = {
                'source': 'duckduckgo',
                'query': query,
                'answer': '',
                'results': []
            }

            for item in results:
                formatted['results'].append({
                    'title': item.get('title', ''),
                    'url': item.get('href', ''),
                    'content': item.get('body', ''),
                    'score': 0,
                    'published_date': item.get('date', '')
                })

            return formatted

        except Exception as e:
            print(f"⚠️  DuckDuckGo 搜索失败: {e}", file=sys.stderr)
            return None

    def news(self, query: str, max_results: int = 10,
             region: Optional[str] = None,
             timelimit: Optional[str] = None) -> Optional[Dict]:
        """搜索新闻"""
        if not self.is_available():
            return None

        # 自动检测区域
        if region is None:
            region = 'cn-zh'  # 默认用中国区域

        try:
            from ddgs import DDGS

            results = DDGS().news(
                query,
                max_results=max_results,
                region=region,
                timelimit=timelimit
            )

            formatted = {
                'source': 'duckduckgo-news',
                'query': query,
                'answer': '',
                'results': []
            }

            for item in results:
                formatted['results'].append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('body', ''),
                    'score': 0,
                    'published_date': item.get('date', ''),
                    'source': item.get('source', '')
                })

            return formatted

        except Exception as e:
            print(f"⚠️  DuckDuckGo 新闻搜索失败: {e}", file=sys.stderr)
            return None


# ============================================================
# Tavily — AI 搜索引擎（需要 API Key）
# ============================================================

class TavilySearch:
    """Tavily API — 专为 AI Agent 设计的搜索引擎"""

    BASE_URL = "https://api.tavily.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('TAVILY_API_KEY')

    def is_available(self) -> bool:
        return self.api_key is not None

    def search(self, query: str, search_depth: str = "basic",
               max_results: int = 10, include_answer: bool = True,
               topic: str = "general") -> Optional[Dict]:
        """搜索网页"""
        if not self.is_available():
            print("⚠️  Tavily API Key 未设置", file=sys.stderr)
            print("   获取 Key: https://app.tavily.com", file=sys.stderr)
            print("   设置环境变量: export TAVILY_API_KEY=tvly-xxxxx", file=sys.stderr)
            return None

        payload = {
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
            "include_answer": include_answer,
            "topic": topic
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                f"{self.BASE_URL}/search",
                data=data,
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))

            formatted = {
                'source': 'tavily',
                'query': query,
                'answer': result.get('answer', ''),
                'results': []
            }

            for item in result.get('results', []):
                formatted['results'].append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0),
                    'published_date': item.get('published_date', '')
                })

            return formatted

        except urllib.error.HTTPError as e:
            print(f"❌ Tavily API 错误: {e.code} {e.reason}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"❌ Tavily 搜索失败: {e}", file=sys.stderr)
            return None


# ============================================================
# Jina Reader — 网页内容提取（需要 VPN）
# ============================================================

class JinaReader:
    """Jina Reader — 将网页转为 LLM 友好的 Markdown"""

    READER_URL = "https://r.jina.ai"
    SEARCH_URL = "https://s.jina.ai"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('JINA_API_KEY')

    def is_available(self) -> bool:
        """检查 Jina 是否可用（需要网络可达）"""
        try:
            req = urllib.request.Request(self.READER_URL, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as response:
                return True
        except:
            return False

    def search(self, query: str, max_results: int = 10) -> Optional[Dict]:
        """使用 Jina 搜索"""
        if not self.is_available():
            print("⚠️  Jina 服务不可用（可能需要 VPN）", file=sys.stderr)
            return None

        try:
            encoded_query = urllib.parse.quote(query)
            url = f"{self.SEARCH_URL}/{encoded_query}"

            headers = {"Accept": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))

            formatted = {
                'source': 'jina-search',
                'query': query,
                'answer': result.get('answer', ''),
                'results': []
            }

            for item in result.get('data', [])[:max_results]:
                formatted['results'].append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('description', item.get('content', '')),
                    'score': 0,
                    'published_date': ''
                })

            return formatted

        except Exception as e:
            print(f"⚠️  Jina 搜索失败: {e}", file=sys.stderr)
            return None

    def read(self, url: str) -> Optional[str]:
        """提取网页内容为 Markdown"""
        if not self.is_available():
            print("⚠️  Jina 服务不可用（可能需要 VPN）", file=sys.stderr)
            return None

        try:
            encoded_url = urllib.parse.quote(url, safe=':/?=&')
            api_url = f"{self.READER_URL}/{encoded_url}"

            headers = {"Accept": "text/markdown"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')

        except Exception as e:
            print(f"⚠️  Jina 读取失败: {e}", file=sys.stderr)
            return None


# ============================================================
# SearXNG — 元搜索引擎（需要自建）
# ============================================================

class SearXNGSearch:
    """SearXNG — 聚合多个搜索引擎的元搜索引擎"""

    def __init__(self, instance_url: Optional[str] = None):
        self.instance_url = instance_url or os.environ.get('SEARXNG_URL', 'http://localhost:8080')

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.instance_url}/healthz")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False

    def search(self, query: str, max_results: int = 10,
               engines: str = "google,bing,duckduckgo",
               language: str = "auto") -> Optional[Dict]:
        """搜索"""
        if not self.is_available():
            print("⚠️  SearXNG 不可用，请先部署实例", file=sys.stderr)
            print(f"   当前配置: {self.instance_url}", file=sys.stderr)
            print("   部署命令: docker run -d -p 8080:8080 searxng/searxng", file=sys.stderr)
            return None

        try:
            params = {
                'q': query,
                'format': 'json',
                'engines': engines,
                'language': language
            }
            url = f"{self.instance_url}/search?{urllib.parse.urlencode(params)}"

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))

            formatted = {
                'source': 'searxng',
                'query': query,
                'answer': '',
                'results': []
            }

            for item in result.get('results', [])[:max_results]:
                formatted['results'].append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0),
                    'published_date': item.get('publishedDate', ''),
                    'engine': item.get('engine', '')
                })

            return formatted

        except Exception as e:
            print(f"⚠️  SearXNG 搜索失败: {e}", file=sys.stderr)
            return None


# ============================================================
# 多源搜索聚合
# ============================================================

def multi_search(query: str, max_results: int = 10,
                 sources: Optional[List[str]] = None,
                 search_depth: str = "basic",
                 auto_detect: bool = True) -> Dict:
    """
    多源并发搜索

    Args:
        query: 搜索关键词
        max_results: 每个源的最大结果数
        sources: 搜索源列表 (duckduckgo/tavily/jina/searxng)
        search_depth: Tavily 搜索深度 (basic/advanced)
        auto_detect: 是否自动检测可用数据源
    """
    # 默认数据源优先级
    if sources is None:
        sources = ['duckduckgo', 'tavily', 'jina']

    # 初始化搜索引擎
    engines = {
        'duckduckgo': DuckDuckGoSearch(),
        'tavily': TavilySearch(),
        'jina': JinaReader(),
        'searxng': SearXNGSearch()
    }

    # 自动检测可用性
    if auto_detect:
        available = []
        unavailable = []
        for source in sources:
            engine = engines.get(source)
            if engine and engine.is_available():
                available.append(source)
            else:
                unavailable.append(source)
                if source == 'jina':
                    print(f"⚠️  {source}: 不可用（可能需要 VPN）", file=sys.stderr)
                elif source == 'tavily':
                    print(f"⚠️  {source}: 不可用（需要 API Key）", file=sys.stderr)
                elif source == 'searxng':
                    print(f"⚠️  {source}: 不可用（需要自建实例）", file=sys.stderr)
                else:
                    print(f"⚠️  {source}: 不可用", file=sys.stderr)
    else:
        available = sources

    if not available:
        print("❌ 没有可用的搜索引擎", file=sys.stderr)
        print("\n💡 建议：", file=sys.stderr)
        print("   1. 安装 ddgs: pip install ddgs", file=sys.stderr)
        print("   2. 设置 Tavily API Key: export TAVILY_API_KEY=tvly-xxxxx", file=sys.stderr)
        print("   3. 使用 VPN 访问 Jina 服务", file=sys.stderr)
        return {'query': query, 'answer': '', 'results': [], 'sources': []}

    # 并发搜索
    all_results = []
    answers = []
    used_sources = []

    print(f"🔍 搜索: {query}", file=sys.stderr)
    print(f"   数据源: {', '.join(available)}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=len(available)) as executor:
        futures = {}
        for source in available:
            engine = engines[source]
            if source == 'tavily':
                futures[executor.submit(
                    engine.search, query,
                    search_depth=search_depth,
                    max_results=max_results
                )] = source
            elif source == 'duckduckgo':
                # 只使用文本搜索（新闻搜索在国内超时）
                futures[executor.submit(
                    engine.search, query,
                    max_results=max_results
                )] = source
            else:
                futures[executor.submit(
                    engine.search, query,
                    max_results=max_results
                )] = source

        for future in as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                if result and result.get('results'):
                    count = len(result['results'])
                    print(f"   ✅ {source}: {count} 个结果", file=sys.stderr)
                    all_results.extend(result['results'])
                    used_sources.append(source)
                    if result.get('answer'):
                        answers.append(f"[{source}] {result['answer']}")
                else:
                    print(f"   ⚠️  {source}: 无结果", file=sys.stderr)
            except Exception as e:
                print(f"   ❌ {source}: {e}", file=sys.stderr)

    # 智能去重（按 URL 和标题）
    seen_urls = set()
    seen_titles = set()
    deduped = []

    for item in all_results:
        url = item.get('url', '').rstrip('/')
        title = item.get('title', '').lower().strip()

        # URL 去重
        if url in seen_urls:
            continue

        # 标题去重（相似标题合并）
        title_key = title[:50] if title else ''
        if title_key and title_key in seen_titles:
            continue

        if url:
            seen_urls.add(url)
        if title_key:
            seen_titles.add(title_key)
        deduped.append(item)

    return {
        'query': query,
        'answer': '\n\n'.join(answers) if answers else '',
        'results': deduped[:max_results],
        'sources': used_sources
    }


def format_markdown(data: Dict) -> str:
    """格式化为 Markdown"""
    lines = [f"## 搜索结果: {data['query']}", ""]

    if data.get('answer'):
        lines.append("### AI 回答")
        lines.append("")
        lines.append(data['answer'])
        lines.append("")

    lines.append(f"### 来源 ({len(data['results'])} 个)")
    lines.append("")
    lines.append("| # | 来源 | 内容摘要 |")
    lines.append("|---|------|----------|")

    for i, item in enumerate(data['results'], 1):
        title = item.get('title', '-')[:50]
        url = item.get('url', '')
        content = item.get('content', '-')[:80]
        lines.append(f"| {i} | [{title}]({url}) | {content} |")

    lines.append("")
    lines.append(f"**数据源:** {', '.join(data.get('sources', []))}")

    return '\n'.join(lines)


def format_json(data: Dict) -> str:
    """格式化为 JSON"""
    return json.dumps(data, ensure_ascii=False, indent=2)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Deep Research — 多源搜索引擎 v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
数据源说明：
  duckduckgo  免费，无需 API Key，国内可用（推荐）
  tavily      AI 搜索引擎，需要 API Key，1000次/月免费
  jina        网页内容提取，需要 VPN 或 API Key
  searxng     元搜索引擎，需要自建实例

示例：
  %(prog)s "Python Web 框架对比"                    # 使用默认数据源
  %(prog)s "AI agent" --sources duckduckgo,tavily   # 指定数据源
  %(prog)s --read "https://example.com"             # 读取网页内容
  %(prog)s --check                                  # 检查数据源可用性
        """
    )
    parser.add_argument('query', nargs='?', default='', help='搜索关键词')
    parser.add_argument('--sources', '-s', default='duckduckgo,tavily',
                        help='搜索源，逗号分隔 (duckduckgo/tavily/jina/searxng)')
    parser.add_argument('--depth', '-d', default='basic',
                        choices=['basic', 'advanced'],
                        help='搜索深度 (Tavily)')
    parser.add_argument('--limit', '-n', type=int, default=10,
                        help='每个源的最大结果数')
    parser.add_argument('--format', '-f', default='markdown',
                        choices=['markdown', 'json'],
                        help='输出格式')
    parser.add_argument('--read', '-r', help='读取指定 URL 的内容')
    parser.add_argument('--check', action='store_true',
                        help='检查数据源可用性')
    parser.add_argument('--no-auto-detect', action='store_true',
                        help='禁用自动检测，强制使用指定数据源')

    args = parser.parse_args()

    # 检查数据源可用性
    if args.check:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        print("[检查] 数据源可用性...\n")

        network = check_network()
        print("[网络环境]")
        print(f"   VPN: {'[有]' if network['has_vpn'] else '[无]'}")
        print(f"   Google: {'[可达]' if network['can_access_google'] else '[不可达]'}")
        print(f"   Jina: {'[可达]' if network['can_access_jina'] else '[不可达]'}")
        print(f"   Tavily: {'[可达]' if network['can_access_tavily'] else '[不可达]'}")
        print()

        engines = {
            'duckduckgo': DuckDuckGoSearch(),
            'tavily': TavilySearch(),
            'jina': JinaReader(),
            'searxng': SearXNGSearch()
        }

        print("[数据源状态]")
        for name, engine in engines.items():
            status = "[可用]" if engine.is_available() else "[不可用]"
            print(f"   {name}: {status}")
        return

    # 处理 --read 模式
    if args.read:
        jina = JinaReader()
        content = jina.read(args.read)
        if content:
            print(content)
        else:
            print("❌ 读取失败", file=sys.stderr)
            print("\n💡 Jina 需要 VPN 才能访问，或者设置 API Key", file=sys.stderr)
            sys.exit(1)
        return

    # 搜索模式需要 query
    if not args.query:
        parser.error("搜索模式需要提供关键词")

    # 多源搜索
    sources = [s.strip() for s in args.sources.split(',')]
    data = multi_search(
        query=args.query,
        max_results=args.limit,
        sources=sources,
        search_depth=args.depth,
        auto_detect=not args.no_auto_detect
    )

    # 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if args.format == 'json':
        print(format_json(data))
    else:
        print(format_markdown(data))


if __name__ == '__main__':
    main()

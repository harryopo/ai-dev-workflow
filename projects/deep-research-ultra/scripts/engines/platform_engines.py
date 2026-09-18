"""
platform_engines.py — 国内开源平台引擎（Gitee / ModelScope）  [v6.1 新增]

- GiteeEngine：Gitee 仓库搜索（免费公开 API `gitee.com/api/v5/search/repositories`，无需 token）
- ModelScopeEngine：魔搭社区模型/项目搜索（免费公开 API，无需 token）

设计约束：
- 纯 JSON API 直连（不解析 HTML，避免反爬脆弱性），失败返回 None / 空列表
- 解析多字段容错（Gitee 兼容 items[] 与 rows[]；ModelScope 兼容多级嵌套结构）
- 与 SearchEngine 基类契约一致，注册进 Layer 2（Skill+平台层）
"""

from __future__ import annotations

import json
import socket
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional

from .base import SearchEngine, EngineMetadata, SearchResult

_UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
       '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')

TIMEOUT = 8.0


def _host_reachable(host: str, port: int = 443, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def _http_get_json(url: str) -> Optional[Any]:
    """GET JSON（urllib，UA 伪装，超时，容错）。"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': _UA, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode('utf-8', errors='ignore'))
    except Exception:
        return None


def _dedupe(results: List[SearchResult]) -> List[SearchResult]:
    seen = set()
    out = []
    for r in results:
        if r.url not in seen:
            seen.add(r.url)
            out.append(r)
    return out


class GiteeEngine(SearchEngine):
    """Gitee 仓库搜索（免费公开 API，国内主力代码平台）。"""

    @property
    def metadata(self) -> EngineMetadata:
        return EngineMetadata(
            name='gitee',
            layer=2,
            description='Gitee 仓库搜索（免费公开 API，国内代码托管平台）',
            requires_config=False,
            is_china_friendly=True,
            priority=70,
            capabilities=['search', 'opensource'],
        )

    def is_available(self) -> bool:
        return _host_reachable('gitee.com')

    def search(self, query: str, max_results: int = 10, **kwargs) -> Optional[List[SearchResult]]:
        q = urllib.parse.quote(query)
        url = f'https://gitee.com/api/v5/search/repositories?q={q}&per_page={max_results}&sort=best_match'
        data = _http_get_json(url)
        if not data:
            return None
        items = data.get('items') or data.get('rows') or []
        out: List[SearchResult] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            out.append(SearchResult(
                title=it.get('full_name') or it.get('name') or '',
                url=it.get('html_url') or it.get('url') or '',
                content=it.get('description') or '',
                source='gitee',
                published_date=it.get('pushed_at') or '',
                author=it.get('owner', {}).get('login', '') if isinstance(it.get('owner'), dict) else '',
                engine='gitee',
                raw={'stars': it.get('stargazers_count'),
                     'language': it.get('language'),
                     'forks': it.get('forks_count')},
            ))
        return _dedupe(out) or None


class ModelScopeEngine(SearchEngine):
    """魔搭社区（ModelScope）模型/项目搜索（免费公开 API，国内模型集市）。"""

    @property
    def metadata(self) -> EngineMetadata:
        return EngineMetadata(
            name='modelscope',
            layer=2,
            description='魔搭社区模型/项目搜索（免费公开 API，国内模型集市）',
            requires_config=False,
            is_china_friendly=True,
            priority=72,
            capabilities=['search', 'opensource', 'model'],
        )

    def is_available(self) -> bool:
        return _host_reachable('modelscope.cn')

    def search(self, query: str, max_results: int = 10, **kwargs) -> Optional[List[SearchResult]]:
        q = urllib.parse.quote(query)
        # 候选端点：官方 API 可能随版本更名，逐一尝试，全部失败返回 None（降级链接管）
        candidates = [
            f'https://modelscope.cn/api/v1/dolphin/models'
            f'?PageSize={max_results}&PageNumber=1&SingleCriterion={q}',
        ]
        data = None
        for url in candidates:
            data = _http_get_json(url)
            if data is not None:
                break
        if not data:
            return None

        # 兼容多级嵌套结构：Data.Model.Models / Model / items / rows
        items: List[dict] = []
        d = data.get('Data') or data
        m = d.get('Model') or d
        for key in ('Models', 'Model', 'models', 'items', 'rows', 'list', 'List'):
            v = m.get(key)
            if isinstance(v, list):
                items = v
                break
            if isinstance(v, dict):
                nested = v.get('Models') or v.get('models')
                if isinstance(nested, list):
                    items = nested
                    break

        out: List[SearchResult] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            path = it.get('Path') or it.get('path') or it.get('Name') or it.get('name') or ''
            name = it.get('ChineseName') or it.get('Name') or it.get('name') or path.split('/')[-1] if path else ''
            if isinstance(name, list):
                name = name[0] if name else ''
            desc = it.get('Description') or it.get('description') or ''
            if isinstance(desc, list):
                desc = ' '.join(str(x) for x in desc)
            out.append(SearchResult(
                title=str(name),
                url=f'https://modelscope.cn/models/{path}' if path else 'https://modelscope.cn',
                content=str(desc)[:300],
                source='modelscope',
                published_date=it.get('LastUpdatedTime') or it.get('updated_at') or '',
                engine='modelscope',
                raw={'task': it.get('Task'), 'downloads': it.get('Downloads') or it.get('downloads')},
            ))
        return _dedupe(out) or None
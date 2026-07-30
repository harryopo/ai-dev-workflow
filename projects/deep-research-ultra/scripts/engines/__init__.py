"""
Deep Research Ultra v4.0 — 引擎模块包

四层架构：
- Layer 1: MCP 服务器层（mcp_engines.py）
- Layer 2: 全局 Skill 层（skill_engines.py）
- Layer 3: Claude 内置工具层（builtin.py）
- Layer 4: 降级引擎层（fallback.py）
"""

from .base import SearchEngine, SearchResult, EngineMetadata
from .mcp_engines import (
    TavilyMcpEngine,
    FirecrawlMcpEngine,
    OpenWebsearchMcpEngine,
    ArxivMcpEngine,
    PaperSearchMcpEngine,
)
from .skill_engines import (
    AgentReachEngine,
    OssFinderEngine,
    Last30DaysEngine,
    SciverseEngine,
    DefuddleEngine,
    Context7Engine,
)
from .builtin import WebSearchEngine, WebFetchEngine
from .fallback import DuckDuckGoEngine, BaiduHtmlEngine, BingHtmlEngine, SearXNGEngine

__all__ = [
    # 基类
    "SearchEngine", "SearchResult", "EngineMetadata",
    # Layer 1: MCP
    "TavilyMcpEngine", "FirecrawlMcpEngine", "OpenWebsearchMcpEngine",
    "ArxivMcpEngine", "PaperSearchMcpEngine",
    # Layer 2: Skill
    "AgentReachEngine", "OssFinderEngine", "Last30DaysEngine",
    "SciverseEngine", "DefuddleEngine", "Context7Engine",
    # Layer 3: 内置
    "WebSearchEngine", "WebFetchEngine",
    # Layer 4: 降级
    "DuckDuckGoEngine", "BaiduHtmlEngine", "BingHtmlEngine", "SearXNGEngine",
]

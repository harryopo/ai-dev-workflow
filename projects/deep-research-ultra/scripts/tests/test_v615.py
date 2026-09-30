# -*- coding: utf-8 -*-
"""v6.15 搜索准确度/广度缺陷收口的回归测试。

对应《搜索准确度与广度缺陷清单》X-D16 ~ X-D21。
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ============================================================
# X-D16：编排层把检索参数透传给引擎
# ============================================================

class _Args:
    """最小 argparse 替身：只提供 helper 会读到的属性。"""

    def __init__(self, **kw):
        self.time_range = ''
        self.include_domain = None
        self.exclude_domain = None
        self.effort = None
        self.depth = 'standard'
        for k, v in kw.items():
            setattr(self, k, v)


def test_kwargs_empty_when_nothing_specified():
    """不带任何参数时不得凭空造键——否则引擎行为会与改动前不同。"""
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(_Args(), search_depth='basic')
    assert kw == {'search_depth': 'basic'}


def test_kwargs_omit_empty_values():
    """空串 / 空列表不得进 kwargs：传空值 != 不传，语义不同。"""
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(time_range='', include_domain=[], exclude_domain=[]),
        search_depth='')
    assert kw == {}


def test_kwargs_carry_all_four_params():
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(time_range='month',
              include_domain=['arxiv.org', 'nature.com'],
              exclude_domain=['csdn.net']),
        search_depth='advanced')
    assert kw['search_depth'] == 'advanced'
    assert kw['time_range'] == 'month'
    assert kw['include_domains'] == ['arxiv.org', 'nature.com']
    assert kw['exclude_domains'] == ['csdn.net']


def test_kwargs_strip_whitespace_in_domains():
    from research import _build_engine_kwargs
    kw = _build_engine_kwargs(
        _Args(include_domain=[' arxiv.org ', '  ']), search_depth='')
    assert kw['include_domains'] == ['arxiv.org']

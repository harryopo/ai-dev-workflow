#!/usr/bin/env python3
"""
check_pages_source.py — 判定 GitHub Pages 子路径的实际服务仓库

用法：
    python check_pages_source.py <owner> <subpath> [--expected-repo <repo>]

逻辑：
    1. curl https://<owner>.github.io/<subpath>/ 拿实际内容
    2. curl https://raw.githubusercontent.com/<owner>/<owner>.github.io/main/<subpath>/index.html
       拿主仓库子目录内容
    3. 对比两者：
       - 一致 → 主仓库子目录提供服务
       - 不一致 → 存在独立 Project Pages 仓库在服务
"""

import sys
import urllib.request
import hashlib
from pathlib import Path


def fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "check_pages_source/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"<FETCH_ERROR: {e}>"


def fingerprint(content: str) -> str:
    """取 <title> 标签和首 5 行作为指纹"""
    lines = content.splitlines()[:5]
    title = ""
    for line in lines:
        if "<title>" in line.lower():
            title = line.strip()
            break
    return f"{title} | hash={hashlib.md5(content.encode()).hexdigest()[:8]}"


def main():
    if len(sys.argv) < 3:
        print("用法: python check_pages_source.py <owner> <subpath>")
        sys.exit(1)

    owner = sys.argv[1]
    subpath = sys.argv[2].strip("/")

    # 1. 实际访问的页面
    live_url = f"https://{owner}.github.io/{subpath}/"
    live_content = fetch(live_url)
    live_fp = fingerprint(live_content)

    print(f"实际访问 URL: {live_url}")
    print(f"实际内容指纹: {live_fp}")
    print()

    # 2. 主仓库子目录
    main_url = f"https://raw.githubusercontent.com/{owner}/{owner}.github.io/main/{subpath}/index.html"
    main_content = fetch(main_url)
    main_fp = fingerprint(main_content)
    print(f"主仓库子目录:  {main_url}")
    print(f"主仓库内容指纹: {main_fp}")
    print()

    # 3. 对比
    if live_fp == main_fp:
        print("✅ 一致：主仓库子目录在提供服务")
        return 0
    else:
        print("⚠️  不一致！")
        print("→ 实际访问的页面与主仓库子目录内容不同")
        print("→ 高度可能存在独立 Project Pages 仓库 (<owner>/<subpath>)")
        print()
        print("排查步骤：")
        print(f"  1. 访问 https://github.com/{owner}/{subpath} 看仓库是否存在")
        print(f"  2. curl https://raw.githubusercontent.com/{owner}/{subpath}/master/index.html")
        print(f"  3. 若 1+2 存在 → 独立仓库是真正的服务源")
        print(f"  4. 推到独立仓库：cd tmp-deploy/{subpath} && git clone https://github.com/{owner}/{subpath}.git . && ...")
        return 1


if __name__ == "__main__":
    sys.exit(main())

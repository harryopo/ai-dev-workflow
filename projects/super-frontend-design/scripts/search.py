#!/usr/bin/env python3
"""
Super Frontend Design — CLI 搜索工具

查询 references/ 目录下的设计数据库：
  - palettes: 161色彩调色板
  - font-pairings: 57字体配对
  - ux-guidelines: 99条UX准则
  - styles: 50+设计风格
  - chart-types: 25种图表类型
  - design-tokens: Design Token规范

用法:
  python search.py palettes saas          # 搜索SaaS类调色板
  python search.py palettes --id P-001    # 按ID查询调色板
  python search.py styles glassmorphism   # 搜索毛玻璃风格
  python search.py fonts elegant          # 搜索优雅字体配对
  python search.py ux accessibility       # 搜索可访问性准则
  python search.py charts line            # 搜索折线图类型
  python search.py tokens color           # 搜索颜色Token
  python search.py design-system saas     # 生成SaaS设计系统
"""

import sys
import os
import re
import json

# references 目录路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REFS_DIR = os.path.join(SCRIPT_DIR, "..", "references")


def read_ref(filename):
    """读取 references 目录下的文件"""
    filepath = os.path.join(REFS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"错误: 文件不存在 {filepath}")
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def search_palettes(query, by_id=False):
    """搜索色彩调色板"""
    content = read_ref("palettes.md")
    if not content:
        return

    if by_id:
        # 按 ID 查询
        pattern = rf"### {re.escape(query)}:.*?(?=###|\Z)"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            print(matches[0].strip())
        else:
            print(f"未找到调色板: {query}")
    else:
        # 按关键词搜索
        query_lower = query.lower()
        sections = content.split("### ")
        results = []
        for section in sections[1:]:  # 跳过文件头
            if query_lower in section.lower():
                # 取前3行作为摘要
                lines = section.split("\n")
                results.append("### " + "\n".join(lines[:8]))

        if results:
            print(f"找到 {len(results)} 个匹配的调色板:\n")
            for r in results:
                print(r)
                print("---")
        else:
            print(f"未找到匹配 '{query}' 的调色板")


def search_fonts(query):
    """搜索字体配对"""
    content = read_ref("font-pairings.md")
    if not content:
        return

    query_lower = query.lower()
    sections = content.split("### ")
    results = []
    for section in sections[1:]:
        if query_lower in section.lower():
            lines = section.split("\n")
            results.append("### " + "\n".join(lines[:7]))

    if results:
        print(f"找到 {len(results)} 个匹配的字体配对:\n")
        for r in results:
            print(r)
            print("---")
    else:
        print(f"未找到匹配 '{query}' 的字体配对")


def search_ux(query):
    """搜索UX准则"""
    content = read_ref("ux-guidelines.md")
    if not content:
        return

    query_lower = query.lower()
    sections = content.split("### ")
    results = []
    for section in sections[1:]:
        if query_lower in section.lower():
            lines = section.split("\n")
            results.append("### " + "\n".join(lines[:10]))

    if results:
        print(f"找到 {len(results)} 条匹配的UX准则:\n")
        for r in results:
            print(r)
            print("---")
    else:
        print(f"未找到匹配 '{query}' 的UX准则")


def search_styles(query):
    """搜索设计风格"""
    content = read_ref("styles-catalog.md")
    if not content:
        return

    query_lower = query.lower()
    sections = content.split("\n## ")
    results = []
    for section in sections[1:]:
        if query_lower in section.lower():
            lines = section.split("\n")
            results.append("## " + "\n".join(lines[:8]))

    if results:
        print(f"找到 {len(results)} 个匹配的设计风格:\n")
        for r in results:
            print(r)
            print("---")
    else:
        print(f"未找到匹配 '{query}' 的设计风格")


def search_charts(query):
    """搜索图表类型"""
    content = read_ref("chart-types.md")
    if not content:
        return

    query_lower = query.lower()
    sections = content.split("### ")
    results = []
    for section in sections[1:]:
        if query_lower in section.lower():
            lines = section.split("\n")
            results.append("### " + "\n".join(lines[:8]))

    if results:
        print(f"找到 {len(results)} 种匹配的图表类型:\n")
        for r in results:
            print(r)
            print("---")
    else:
        print(f"未找到匹配 '{query}' 的图表类型")


def search_tokens(query):
    """搜索Design Token"""
    content = read_ref("design-tokens.md")
    if not content:
        return

    query_lower = query.lower()
    lines = content.split("\n")
    results = []
    context_lines = 2

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            results.append("\n".join(lines[start:end]))

    if results:
        print(f"找到 {len(results)} 处匹配的Design Token:\n")
        for r in results[:10]:  # 限制输出
            print(r)
            print("---")
    else:
        print(f"未找到匹配 '{query}' 的Design Token")


def generate_design_system(product_type):
    """生成设计系统推荐"""
    print(f"=== {product_type.upper()} 设计系统推荐 ===\n")

    # 搜索调色板
    print("## 推荐调色板")
    search_palettes(product_type)

    # 搜索字体
    print("\n## 推荐字体配对")
    if product_type in ["saas", "dashboard", "fintech", "productivity"]:
        search_fonts("专业商务")
    elif product_type in ["e-commerce", "fashion", "beauty"]:
        search_fonts("优雅奢华")
    elif product_type in ["creative", "portfolio", "agency"]:
        search_fonts("创意设计")
    elif product_type in ["education", "health", "wellness"]:
        search_fonts("温暖有机")
    elif product_type in ["gaming", "crypto", "tech"]:
        search_fonts("科技未来")
    else:
        search_fonts("现代极简")

    # 搜索风格
    print("\n## 推荐风格")
    if product_type in ["saas", "dashboard"]:
        search_styles("minimalism")
    elif product_type in ["creative", "portfolio"]:
        search_styles("bento")
    elif product_type in ["gaming", "crypto"]:
        search_styles("cyberpunk")

    # 搜索UX准则
    print("\n## 关键UX准则")
    search_ux(product_type)


def print_help():
    """打印帮助信息"""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command in ["-h", "--help", "help"]:
        print_help()
    elif command == "palettes":
        if len(sys.argv) < 3:
            print("用法: python search.py palettes <关键词|--id P-XXX>")
            return
        if sys.argv[2] == "--id" and len(sys.argv) >= 4:
            search_palettes(sys.argv[3], by_id=True)
        else:
            search_palettes(sys.argv[2])
    elif command in ["fonts", "font-pairings"]:
        if len(sys.argv) < 3:
            print("用法: python search.py fonts <关键词>")
            return
        search_fonts(sys.argv[2])
    elif command in ["ux", "ux-guidelines"]:
        if len(sys.argv) < 3:
            print("用法: python search.py ux <关键词>")
            return
        search_ux(sys.argv[2])
    elif command in ["styles", "style"]:
        if len(sys.argv) < 3:
            print("用法: python search.py styles <关键词>")
            return
        search_styles(sys.argv[2])
    elif command in ["charts", "chart-types"]:
        if len(sys.argv) < 3:
            print("用法: python search.py charts <关键词>")
            return
        search_charts(sys.argv[2])
    elif command in ["tokens", "design-tokens"]:
        if len(sys.argv) < 3:
            print("用法: python search.py tokens <关键词>")
            return
        search_tokens(sys.argv[2])
    elif command == "design-system":
        if len(sys.argv) < 3:
            print("用法: python search.py design-system <产品类型>")
            print("产品类型: saas, e-commerce, dashboard, fintech, health, education, gaming, creative, portfolio")
            return
        generate_design_system(sys.argv[2])
    else:
        print(f"未知命令: {command}")
        print_help()


if __name__ == "__main__":
    main()

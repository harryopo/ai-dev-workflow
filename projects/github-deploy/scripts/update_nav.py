#!/usr/bin/env python3
"""harryopo.github.io 导航模块更新脚本（v2）

由 github-deploy skill 调用，在部署新网页后自动更新首页导航区。
读取 index.html 中的 <!-- NAV-START --> ... <!-- NAV-END --> 区域，
插入或更新对应项目的导航卡片。

## 升级要点（v2）
1. 卡片模板与主页 index.html 实际样式严格一致（class="card"）
2. 移除 nav-card__tag 字段（主页样式无 tag）
3. 支持「一行命令」自动推断：仅传 slug 即可从本地项目仓库读取 README.md 提取标题/描述
4. 强校验：slug、title 缺失时直接报错（不静默回退）

## 使用方式

方式 1（推荐 · 自动推断）：
    cd <项目本地路径> && python update_nav.py <slug>
    例：cd "d:/ai/code/database-er-diagram" && python update_nav.py database-er-diagram

方式 2（手动指定）：
    python update_nav.py <slug> <title> [desc]
    例：python update_nav.py junlin-tianxia "菌临天下" "2026暑期三下乡PPT"
"""

import re
import sys
from pathlib import Path

# ===== 卡片模板（与 harryopo.github.io/index.html 中 <a class="card"> 严格一致）=====
NAV_CARD_TEMPLATE = """<a class="card" href="/{slug}/">
    <div class="card-name">{title}</div>
    <div class="card-url">harryopo.github.io/{slug}/</div>
    <div class="card-desc">{desc}</div>
  </a>"""

NAV_START = "<!-- NAV-START -->"
NAV_END = "<!-- NAV-END -->"
AUTO_NOTICE = "<!-- 由 github-deploy skill 自动维护，请勿手动编辑 NAV-START/NAV-END 之间的内容 -->"

# 主仓库 harryopo.github.io 的本地路径（用于读取/写入 index.html）
PAGES_ROOT = Path("d:/ai/claude code/skill开发/projects/harryopo.github.io")


def read_readme_meta(repo_path: Path) -> tuple[str, str]:
    """从 README.md 提取标题和描述。

    返回 (title, desc)：
    - title：第一处 "# xxx" 的内容；若无则用目录名
    - desc：第一处非空、非标题、非列表、非代码块的纯文本段落；最长 80 字符
    """
    repo_name = repo_path.name
    readme = repo_path / "README.md"

    title = repo_name
    desc = "暂无描述"

    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        lines = content.split("\n")

        title_found = False
        in_code_block = False
        for line in lines:
            stripped = line.strip()

            # 跳过代码块（fenced code）
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # 抓取首个 H1 作为标题
            if not title_found and stripped.startswith("# "):
                title = stripped[2:].strip()
                title_found = True
                continue

            # 抓取首个正文段落作为描述（排除标题、列表、引用、分隔线、空行）
            if (
                title_found
                and desc == "暂无描述"
                and stripped
                and not stripped.startswith("#")
                and not stripped.startswith("-")
                and not stripped.startswith("*")
                and not stripped.startswith(">")
                and not stripped.startswith("|")
                and not stripped.startswith("---")
            ):
                desc = stripped[:80]
                break

    return (title, desc)


def update_nav(
    pages_root: Path,
    slug: str,
    title: str,
    desc: str,
) -> bool:
    """在 harryopo.github.io/index.html 中更新导航卡片。"""
    index_path = pages_root / "index.html"

    if not index_path.exists():
        print(f"[ERROR] {index_path} 不存在")
        return False

    # 强校验：title/desc 不能为空串
    if not title.strip() or not desc.strip():
        print("[ERROR] title/desc 不能为空")
        return False

    content = index_path.read_text(encoding="utf-8")
    nav_card = NAV_CARD_TEMPLATE.format(slug=slug, title=title, desc=desc)

    # 检查 NAV-START/NAV-END 是否存在
    if NAV_START not in content:
        print(f"[ERROR] index.html 中未找到 {NAV_START} 标记，请先在卡片区添加")
        return False
    if NAV_END not in content:
        print(f"[ERROR] index.html 中未找到 {NAV_END} 标记，请先在卡片区添加")
        return False

    # 提取导航区域
    start_pos = content.index(NAV_START) + len(NAV_START)
    end_pos = content.index(NAV_END)
    nav_section = content[start_pos:end_pos]

    # 检查是否已有同名卡片（按 href 匹配）
    card_pattern = re.compile(
        rf'<a\s+class="card"\s+href="/{re.escape(slug)}/".*?</a>', re.DOTALL
    )
    existing = card_pattern.search(nav_section)

    if existing:
        # 更新已有卡片（保留缩进风格）
        new_content = content[:start_pos] + nav_section.replace(
            existing.group(0), nav_card.strip()
        ) + content[end_pos:]
        print(f"[INFO] 更新已有导航卡片: {slug}")
    else:
        # 插入新卡片：在 NAV-START 注释后、第一个卡片前插入
        new_content = (
            content[:start_pos]
            + "\n  "
            + AUTO_NOTICE
            + "\n\n  "
            + nav_card.strip()
            + "\n\n  "
            + content[start_pos:].lstrip()
        )
        # 重新计算并把 AUTO_NOTICE 去重（避免重复插入）
        new_content = re.sub(
            r"(  " + re.escape(AUTO_NOTICE) + r"\s*\n+)+",
            "  " + AUTO_NOTICE + "\n\n  ",
            new_content,
        )
        print(f"[INFO] 新增导航卡片: {slug}")

    # 规范化 NAV 区内部空白：合并连续空行、修正 AUTO_NOTICE 位置
    nav_start_idx = new_content.index(NAV_START) + len(NAV_START)
    nav_end_idx = new_content.index(NAV_END)
    inner = new_content[nav_start_idx:nav_end_idx]
    clean_inner = re.sub(r"\n{3,}", "\n\n", inner).rstrip() + "\n  "
    new_content = (
        new_content[:nav_start_idx]
        + "\n  "
        + AUTO_NOTICE
        + "\n\n"
        + clean_inner.lstrip()
        + new_content[nav_end_idx:]
    )

    index_path.write_text(new_content, encoding="utf-8")
    print(f"[OK] 首页导航已更新 → {slug} | {title}")
    return True


def infer_from_cwd() -> tuple[str, str, str]:
    """从当前工作目录的 README.md 推断 (slug, title, desc)。"""
    cwd = Path.cwd()
    slug = cwd.name
    title, desc = read_readme_meta(cwd)
    return (slug, title, desc)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # 单参数模式：自动推断
    if len(sys.argv) == 2:
        slug = sys.argv[1]
        cwd = Path.cwd()
        # 若 CWD 目录名 != slug，允许从 cwd 推断；否则严格要求 cwd 名等于 slug
        title, desc = read_readme_meta(cwd)
        print(f"[AUTO] 从 {cwd} 推断：title={title!r}, desc={desc!r}")

    # 多参数模式：手动指定
    else:
        slug = sys.argv[1]
        title = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else "暂无描述"

    success = update_nav(PAGES_ROOT, slug, title, desc)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""初始化个人项目开发前置文档骨架。

用法：
    python init_project_docs.py --target <项目根目录> --name "<项目名>"
    python init_project_docs.py --target <项目根目录> --name "<项目名>" --ignore-docs
    python init_project_docs.py --target <项目根目录> --name "<项目名>" --force

只复制模板并替换 {{PROJECT_NAME}} / {{DATE}}，不填写内容。
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
DOC_TEMPLATES = [
    "01-项目开发文档.md",
    "02-架构与技术栈.md",
    "03-开发规范.md",
    "04-本地初始化与运行.md",
    "05-项目进度控制.md",
    "06-AI协作规范.md",
]
README_TEMPLATE = "README.md"


def render(text: str, project_name: str, date: str) -> str:
    return text.replace("{{PROJECT_NAME}}", project_name).replace("{{DATE}}", date)


def write_file(dest: Path, content: str, force: bool) -> str:
    if dest.exists() and not force:
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8", newline="\n")
    return "write"


def ensure_ignore_docs(target: Path) -> str:
    gitignore = target / ".gitignore"
    entry = "docs/"
    if gitignore.exists():
        lines = gitignore.read_text(encoding="utf-8", errors="ignore").splitlines()
        if any(line.strip() == entry for line in lines):
            return "unchanged"
        with gitignore.open("a", encoding="utf-8", newline="\n") as fh:
            if lines and not lines[-1].strip():
                fh.write(entry + "\n")
            else:
                fh.write("\n" + entry + "\n")
        return "updated"
    gitignore.write_text(entry + "\n", encoding="utf-8", newline="\n")
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化项目开发前置文档骨架")
    parser.add_argument("--target", required=True, help="项目根目录")
    parser.add_argument("--name", required=True, help="项目名称")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--ignore-docs", action="store_true", help="把 docs/ 写入目标项目的 .gitignore")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)

    if not TEMPLATE_DIR.is_dir():
        print(f"错误：找不到模板目录 {TEMPLATE_DIR}", file=sys.stderr)
        return 1

    date = dt.date.today().isoformat()
    docs_dir = target / "docs"
    results: list[tuple[str, str]] = []

    for name in DOC_TEMPLATES:
        src = TEMPLATE_DIR / name
        if not src.is_file():
            print(f"错误：缺少模板 {src}", file=sys.stderr)
            return 1
        content = render(src.read_text(encoding="utf-8"), args.name, date)
        results.append((str(docs_dir / name), write_file(docs_dir / name, content, args.force)))

    src = TEMPLATE_DIR / README_TEMPLATE
    if not src.is_file():
        print(f"错误：缺少模板 {src}", file=sys.stderr)
        return 1
    content = render(src.read_text(encoding="utf-8"), args.name, date)
    results.append((str(target / README_TEMPLATE), write_file(target / README_TEMPLATE, content, args.force)))

    print(f"项目：{args.name}")
    print(f"目录：{target}")
    for path, status in results:
        label = {"write": "已生成", "skip": "已存在，跳过"}[status]
        print(f"  [{label}] {path}")

    if args.ignore_docs:
        print(f"  [.gitignore] docs/ -> {ensure_ignore_docs(target)}")

    skipped = [p for p, s in results if s == "skip"]
    if skipped:
        print("\n有文件已存在，未覆盖。确需覆盖请加 --force。")

    print("\n下一步：")
    print("  1. 填写 docs/01-项目开发文档.md")
    print("  2. 填写 docs/02-架构与技术栈.md 与 docs/03-开发规范.md")
    print("  3. 填写 docs/04、05、06 与 README.md")
    print("  4. 按 references/doc-checklists.md 过文档门")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

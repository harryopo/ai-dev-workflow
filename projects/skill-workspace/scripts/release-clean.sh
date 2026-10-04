#!/usr/bin/env bash
# release-clean.sh — Skill 发布前清洗工具 (Bash / Git Bash / macOS / Linux)
#
# 用途：删除开发期产物、剥离版本号与升级纪要，让发布包只保留运行必需内容。
# 清单见 flows/release-clean.md，本脚本是该清单的可执行版本。
#
# 用法：
#   ./release-clean.sh <skill目录> [--dry-run]
#   ./release-clean.sh <skill目录> --keep-memory     # .dev-memory.md 原地保留，不归档
#
# 安全红线（脚本强制）：
#   1. 目标必须是已存在的目录，且直接包含 SKILL.md，否则拒绝
#   2. 只删除清单内列出的目录/文件，不做目录树遍历删除
#   3. .dev-memory.md 归档而非删除（除非 --keep-memory）
#   4. 默认 --dry-run，显式传 --apply 才实际改动

set -uo pipefail

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'
if [[ "${NO_COLOR:-}" == "1" ]]; then RED=""; GRN=""; YEL=""; DIM=""; RST=""; fi

die()  { printf '%s错误：%s%s\n' "$RED" "$*" "$RST" >&2; exit 1; }
ok()   { printf '%s%s%s\n' "$GRN" "$*" "$RST"; }
info() { printf '%s\n' "$*"; }

APPLY=0
KEEP_MEMORY=0
TARGET=""

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)       APPLY=1 ;;
    --keep-memory) KEEP_MEMORY=1 ;;
    --dry-run)     APPLY=0 ;;
    -h|--help)     usage ;;
    -*)            die "未知参数：$1" ;;
    *)             TARGET="$1" ;;
  esac
  shift
done

[[ -z "$TARGET" ]] && usage
[[ -d "$TARGET" ]] || die "目录不存在：$TARGET"
[[ -f "$TARGET/SKILL.md" ]] || die "目标目录缺少 SKILL.md，不是 skill 目录：$TARGET"

# ---- 1. 删除开发期目录 ----
DEV_DIRS=(.research artifacts __pycache__ .pytest_cache node_modules dist build)

info "【1/4】删除开发期目录"
for d in "${DEV_DIRS[@]}"; do
  found=$(find "$TARGET" -type d -name "$d" -prune 2>/dev/null)
  [[ -z "$found" ]] && continue
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    if [[ $APPLY -eq 1 ]]; then rm -rf "$p"; ok "  已删除目录 $p"; else info "  [dry-run] 将删除目录 $p"; fi
  done <<< "$found"
done

# ---- 2. 删除开发期文件 ----
DEV_FILES=(index.html CHANGELOG.md CHANGELOG HISTORY.md VERSION)
info "【2/4】删除开发期文件"
for f in "${DEV_FILES[@]}"; do
  found=$(find "$TARGET" -maxdepth 2 -type f -name "$f" 2>/dev/null)
  [[ -z "$found" ]] && continue
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    if [[ $APPLY -eq 1 ]]; then rm -f "$p"; ok "  已删除文件 $p"; else info "  [dry-run] 将删除文件 $p"; fi
  done <<< "$found"
done

# 备份与编辑器残留
found=$(find "$TARGET" -maxdepth 3 -type f \( -name "*.bak" -o -name "*.bak-*" -o -name "*~" \) 2>/dev/null)
if [[ -n "$found" ]]; then
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    if [[ $APPLY -eq 1 ]]; then rm -f "$p"; ok "  已删除残留 $p"; else info "  [dry-run] 将删除残留 $p"; fi
  done <<< "$found"
fi

# ---- 3. 归档 .dev-memory.md ----
info "【3/4】处理 .dev-memory.md"
mem=$(find "$TARGET" -maxdepth 2 -type f -name ".dev-memory.md" 2>/dev/null | head -1)
if [[ -n "$mem" ]]; then
  if [[ $KEEP_MEMORY -eq 1 ]]; then
    info "  保留（原地）：$mem"
  else
    skillname=$(basename "$TARGET")
    archive="$(dirname "$TARGET")/.dev-memory/${skillname}.md"
    if [[ $APPLY -eq 1 ]]; then
      mkdir -p "$(dirname "$archive")"
      mv "$mem" "$archive"
      ok "  已归档到 $archive"
    else
      info "  [dry-run] 将归档 $mem → $archive"
    fi
  fi
else
  info "  无 .dev-memory.md"
fi

# ---- 4. 剥离版本号 ----
info "【4/4】剥离版本号与升级纪要"

# 教学/说明文档自身的版本字眼是示例，不剥离
# - release-clean.md：本清洗清单，改了会自相矛盾
# - dev-memory-guide.md：讲"不要写版本标记"，文中版本号是反例示范
# - README.md：面向用户的说明文档，正式版本历史放这里
SKIP_VERSIONS=("release-clean.md" "dev-memory-guide.md" "README.md")

should_skip() {
  local base; base="$(basename "$1")"
  local s
  for s in "${SKIP_VERSIONS[@]}"; do
    [[ "$base" == "$s" ]] && return 0
  done
  return 1
}

strip_one() {
  local f="$1"
  should_skip "$f" && return 0
  # frontmatter 的 version: 行
  if grep -qE '^version:[[:space:]]*' "$f"; then
    if [[ $APPLY -eq 1 ]]; then
      sed -i.bak -E '/^version:[[:space:]]*/d' "$f" && rm -f "$f.bak"
      ok "  已剥离 version 字段：$f"
    else
      info "  [dry-run] 将剥离 version 字段：$f"
    fi
  fi
  # 标题/行内版本后缀：（v5.3.1新增）（v5.1 新增）
  if grep -qE '（v[0-9]+\.[0-9]+(\.[0-9]+)?[[:space:]]*新增）' "$f"; then
    if [[ $APPLY -eq 1 ]]; then
      sed -i.bak -E 's/（v[0-9]+\.[0-9]+(\.[0-9]+)?[[:space:]]*新增）//g' "$f" && rm -f "$f.bak"
      ok "  已剥离版本后缀：$f"
    else
      info "  [dry-run] 将剥离版本后缀：$f"
    fi
  fi
  # 文件头注：> v5.4 新增。
  if grep -qE '^>[[:space:]]*v[0-9]+\.[0-9]+[[:space:]]*新增' "$f"; then
    if [[ $APPLY -eq 1 ]]; then
      sed -i.bak -E 's/^(>[[:space:]]*)v[0-9]+\.[0-9]+[[:space:]]*新增[[:space:]]*/\1/' "$f" && rm -f "$f.bak"
      ok "  已剥离头注版本：$f"
    else
      info "  [dry-run] 将剥离头注版本：$f"
    fi
  fi
}

while IFS= read -r md; do
  [[ -z "$md" ]] && continue
  strip_one "$md"
done < <(find "$TARGET" -maxdepth 3 -type f -name "*.md" 2>/dev/null)

if [[ $APPLY -eq 1 ]]; then
  ok ""
  ok "清洗完成。"
else
  info ""
  info "以上为演练，未实际改动。确认无误后加 --apply 执行。"
fi
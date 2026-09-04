#!/usr/bin/env bash
# source-cleanup.sh — Skill 源码工作区安全清理工具 (Bash / Git Bash / macOS / Linux)
#
# 用途：清理 skill-workspace 在「搜索 / 开发 / 审查 / 合并」流程中 git clone 下来的临时源码。
# 设计：两段式回收 —— 先 stage（移入 .trash，可恢复），再 purge（真正删除，默认 7 天冷静期）。
#
# 用法：
#   ./source-cleanup.sh list [--root DIR]
#   ./source-cleanup.sh stage <name|all> [--root DIR] [--skill NAME]
#   ./source-cleanup.sh restore <staged-name> [--root DIR]
#   ./source-cleanup.sh purge [--root DIR] [--older-than N] [--yes] [--dry-run]
#   ./source-cleanup.sh release <name> [--root DIR]     # 标记 status=releasable
#   ./source-cleanup.sh auto [--root DIR] [--dry-run]   # 释放所有 releasable 的工作区
#
# 安全红线（脚本强制，不可绕过）：
#   1. 只允许操作 ROOT 的直接子目录，拒绝 ".."、绝对路径、符号链接逃逸
#   2. 目标必须含标记文件 .skill-workspace-source 且 marker 匹配，否则拒绝
#   3. 禁止删除 ROOT 自身、.trash 之外的任何路径
#   4. purge 默认 dry-run，必须显式 --yes 才真删

set -uo pipefail

MARKER_FILE=".skill-workspace-source"
MARKER_KEY="skill-workspace-source"
TRASH_DIR=".trash"
DEFAULT_ROOT=".cache/sources"
DEFAULT_RETENTION_DAYS=7

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'
if [[ "${NO_COLOR:-}" == "1" ]]; then RED=""; GRN=""; YEL=""; DIM=""; RST=""; fi

die()  { printf '%s错误：%s%s\n' "$RED" "$*" "$RST" >&2; exit 1; }
warn() { printf '%s警告：%s%s\n' "$YEL" "$*" "$RST" >&2; }
ok()   { printf '%s%s%s\n' "$GRN" "$*" "$RST"; }
info() { printf '%s\n' "$*"; }

usage() {
  sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# ---------- 参数解析 ----------
ROOT="$DEFAULT_ROOT"
CMD=""
TARGET=""
SKILL_FILTER=""
RETENTION="$DEFAULT_RETENTION_DAYS"
ASSUME_YES=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    list|stage|restore|purge|release|auto) CMD="$1"; shift ;;
    --root)       ROOT="${2:?--root 需要参数}"; shift 2 ;;
    --skill)      SKILL_FILTER="${2:?--skill 需要参数}"; shift 2 ;;
    --older-than) RETENTION="${2:?--older-than 需要参数}"; shift 2 ;;
    --yes|-y)     ASSUME_YES=1; shift ;;
    --dry-run)    DRY_RUN=1; shift ;;
    -h|--help)    usage ;;
    *)            [[ -z "$TARGET" ]] && TARGET="$1" || die "未知参数: $1"; shift ;;
  esac
done

[[ -n "$CMD" ]] || usage
[[ "$RETENTION" =~ ^[0-9]+$ ]] || die "--older-than 必须是非负整数"
[[ "$ROOT" == "." || "$ROOT" == "/" || "$ROOT" == "$HOME" ]] && die "拒绝使用危险根目录: $ROOT"

TRASH="$ROOT/$TRASH_DIR"

# ---------- 安全工具 ----------

# 校验目标名是单一路径段，无分隔符、无 ..
assert_safe_name() {
  local name="$1"
  [[ -n "$name" ]] || die "目标名为空"
  [[ "$name" != "." && "$name" != ".." ]] || die "非法目标名: $name"
  [[ "$name" != *"/"* && "$name" != *"\\"* ]] || die "目标名不允许包含路径分隔符: $name"
  [[ "$name" == .* ]] && die "拒绝操作隐藏目录: $name"
  return 0
}

# 解析并确保目标真实路径位于 root 之内（防符号链接逃逸）
resolve_under_root() {
  local root="$1" name="$2"
  local root_real target_real
  [[ -d "$root" ]] || die "根目录不存在: $root（先用 list 确认，或传 --root）"
  [[ -e "$root/$name" ]] || die "目标不存在: $root/$name"
  root_real="$(cd "$root" && pwd -P)" || die "无法解析根目录: $root"
  target_real="$(cd "$root/$name" 2>/dev/null && pwd -P)" || die "无法解析目标: $name"
  [[ "$target_real" == "$root_real" ]] && die "拒绝操作根目录自身"
  case "$target_real" in
    "$root_real"/*) : ;;
    *) die "安全拒绝：目标真实路径逃逸出根目录 → $target_real" ;;
  esac
  printf '%s' "$target_real"
}

# 校验标记文件，未标记的目录一律不碰
require_marker() {
  local dir="$1"
  [[ -f "$dir/$MARKER_FILE" ]] || die "安全拒绝：目标缺少标记文件 $MARKER_FILE，不是 skill-workspace 创建的源码工作区 → $dir"
  grep -q "marker=$MARKER_KEY" "$dir/$MARKER_FILE" 2>/dev/null \
    || die "安全拒绝：标记文件内容不匹配（marker=$MARKER_KEY）→ $dir"
}

# 读取标记字段
read_field() {
  local dir="$1" key="$2"
  [[ -f "$dir/$MARKER_FILE" ]] || return 0
  sed -n "s/^${key}=//p" "$dir/$MARKER_FILE" | head -1
}

# 设置标记字段（不存在则追加）
set_field() {
  local dir="$1" key="$2" val="$3"
  local f="$dir/$MARKER_FILE"
  if grep -q "^${key}=" "$f" 2>/dev/null; then
    sed -i.bak "s|^${key}=.*|${key}=${val}|" "$f" && rm -f "$f.bak"
  else
    printf '%s=%s\n' "$key" "$val" >> "$f"
  fi
}

human_size() {
  local d="$1"
  if command -v du >/dev/null 2>&1; then
    du -sh "$d" 2>/dev/null | cut -f1
  else
    echo "?"
  fi
}

now_stamp() { date +%Y%m%d-%H%M%S; }
now_iso()   { date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S%z'; }

# 列出所有受管工作区（排除 .trash）
list_workspaces() {
  [[ -d "$ROOT" ]] || return 0
  find "$ROOT" -maxdepth 1 -mindepth 1 -type d -not -name "$TRASH_DIR" 2>/dev/null | sort
}

# ---------- 命令实现 ----------

cmd_list() {
  [[ -d "$ROOT" ]] || { info "源码根目录不存在：$ROOT（尚无 git 下载的源码，无需清理）"; return 0; }

  local total_bytes=0
  # 表头用英文：中文在 printf %-Ns 下按字节计宽，会导致列错位
  printf '%-42s %-11s %-9s %-14s %s\n' "WORKSPACE" "STATUS" "SIZE" "SKILL" "SOURCE"
  printf '%s\n' "------------------------------------------------------------------------------------------------"

  local dir name status skill size url marked=0 unmarked=0
  local unmanaged_bytes=0
  while IFS= read -r dir; do
    [[ -n "$dir" ]] || continue
    name="$(basename "$dir")"
    if [[ ! -f "$dir/$MARKER_FILE" ]]; then
      unmarked=$((unmarked + 1))
      unmanaged_bytes=$((unmanaged_bytes + $(du -sk "$dir" 2>/dev/null | cut -f1 | head -1 || echo 0)))
      printf '%-42s %s\n' "$name" "${DIM}(无标记 · 非本工具创建 · 不会自动清理)${RST}"
      continue
    fi
    marked=$((marked + 1))
    [[ -n "$SKILL_FILTER" && "$(read_field "$dir" skill_name)" != "$SKILL_FILTER" ]] && continue
    status="$(read_field "$dir" status)"; status="${status:-in-use}"
    skill="$(read_field "$dir" skill_name)"; skill="${skill:--}"
    url="$(read_field "$dir" source_url)"; url="${url:--}"
    size="$(human_size "$dir")"
    total_bytes=$((total_bytes + $(du -sk "$dir" 2>/dev/null | cut -f1 | head -1 || echo 0)))
    printf '%-42s %-10s %-9s %-8s %s\n' "$name" "$status" "$size" "$skill" "$url"
  done < <(list_workspaces)

  printf '%s\n' "------------------------------------------------------------------------------------------------"
  info "受管工作区：${marked} 个，合计 $((total_bytes / 1024)) MB"
  [[ $unmarked -gt 0 ]] && warn "发现 ${unmarked} 个无标记目录（约 $((unmanaged_bytes / 1024)) MB），非本工具创建，已跳过不动"

  if [[ -d "$TRASH" ]]; then
    local staged staged_bytes=0
    staged="$(find "$TRASH" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
    staged_bytes=$(du -sk "$TRASH" 2>/dev/null | cut -f1 | head -1 || echo 0)
    info "回收暂存区：${staged} 个，占用 $((staged_bytes / 1024)) MB（可用 purge 真正释放）"
  fi
}

# 把工作区移入暂存区（不删除，可恢复）
do_stage() {
  local name="$1"
  assert_safe_name "$name"
  local dir; dir="$(resolve_under_root "$ROOT" "$name")"
  require_marker "$dir"

  local status; status="$(read_field "$dir" status)"; status="${status:-in-use}"
  if [[ "$status" == "in-use" && "$ASSUME_YES" -ne 1 ]]; then
    warn "工作区状态为 in-use（可能仍在使用）：$name"
    [[ -t 0 ]] || die "非交互环境且未加 --yes，已中止。确认无用后请执行：release $name 再 stage，或直接加 --yes"
    read -r -p "确认移入回收暂存区？[y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || { info "已跳过：$name"; return 0; }
  fi

  local stamp; stamp="$(now_stamp)"
  local dest="$TRASH/${name}-${stamp}"
  mkdir -p "$TRASH" || die "无法创建暂存区：$TRASH"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "[dry-run] 将移动：$dir → $dest"
    return 0
  fi

  set_field "$dir" status "staged"
  set_field "$dir" staged_at "$(now_iso)"
  set_field "$dir" staged_from "$name"

  if mv "$dir" "$dest" 2>/dev/null; then
    ok "已移入回收暂存区：$name → $dest（可用 restore 恢复）"
  else
    set_field "$dir" status "$status"
    die "移动失败：$name（可能是文件被占用，关闭相关程序后重试）"
  fi
}

cmd_stage() {
  [[ -d "$ROOT" ]] || die "源码根目录不存在：$ROOT"
  local name="$TARGET"
  if [[ -z "$name" || "$name" == "all" ]]; then
    local dir n status count=0
    while IFS= read -r dir; do
      [[ -n "$dir" ]] || continue
      [[ -f "$dir/$MARKER_FILE" ]] || continue
      n="$(basename "$dir")"
      status="$(read_field "$dir" status)"; status="${status:-in-use}"
      if [[ -n "$SKILL_FILTER" && "$(read_field "$dir" skill_name)" != "$SKILL_FILTER" ]]; then continue; fi
      if [[ "$status" == "releasable" || "$ASSUME_YES" -eq 1 ]]; then
        do_stage "$n" && count=$((count + 1))
      else
        info "跳过（状态 $status）：$n"
      fi
    done < <(list_workspaces)
    info "完成：共移入 $count 个"
  else
    do_stage "$name"
  fi
}

cmd_release() {
  [[ -n "$TARGET" ]] || die "用法：release <name>"
  assert_safe_name "$TARGET"
  local dir; dir="$(resolve_under_root "$ROOT" "$TARGET")"
  require_marker "$dir"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "[dry-run] 将标记 releasable：$TARGET"
    return 0
  fi
  set_field "$dir" status "releasable"
  set_field "$dir" releasable_at "$(now_iso)"
  ok "已标记为可释放：$TARGET（下次 auto 或 stage all 会被回收）"
}

cmd_restore() {
  [[ -n "$TARGET" ]] || die "用法：restore <staged-name>（名称见 .trash 目录，形如 xxx-20260904-221000）"
  assert_safe_name "$TARGET"
  [[ -d "$TRASH/$TARGET" ]] || die "暂存区中不存在：$TRASH/$TARGET"

  local orig; orig="$(read_field "$TRASH/$TARGET" staged_from)"
  [[ -n "$orig" ]] || { orig="$(basename "$TARGET")"; orig="${orig%-*-*}"; }
  assert_safe_name "$orig"

  if [[ -e "$ROOT/$orig" ]]; then
    die "目标位置已存在同名目录：$ROOT/$orig（先处理后再恢复）"
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "[dry-run] 将恢复：$TRASH/$TARGET → $ROOT/$orig"
    return 0
  fi

  if mv "$TRASH/$TARGET" "$ROOT/$orig"; then
    set_field "$ROOT/$orig" status "in-use"
    ok "已恢复：$ROOT/$orig（状态重置为 in-use）"
  else
    die "恢复失败：$TARGET"
  fi
}

cmd_purge() {
  [[ -d "$TRASH" ]] || { info "暂存区为空，无需清理"; return 0; }

  local found
  # 注意：GNU find 的 -mtime +0 语义是「≥24 小时」不是「全部」，
  # 所以 --older-than 0 必须单独走不带时间过滤的分支，否则立即回收会失效。
  if [[ "$RETENTION" -eq 0 ]]; then
    found="$(find "$TRASH" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)"
  else
    found="$(find "$TRASH" -maxdepth 1 -mindepth 1 -type d -mtime "+${RETENTION}" 2>/dev/null | sort)"
  fi

  if [[ -z "$found" ]]; then
    info "暂存区中没有超过 ${RETENTION} 天的条目（冷静期未到，保留以防误删）"
    return 0
  fi

  info "以下条目将被永久删除（已在暂存区超过 ${RETENTION} 天）："
  local d bytes=0
  while IFS= read -r d; do
    [[ -n "$d" ]] || continue
    bytes=$((bytes + $(du -sk "$d" 2>/dev/null | cut -f1 | head -1 || echo 0)))
    printf '  %s  %s\n' "$(basename "$d")" "$(human_size "$d")"
  done <<< "$found"
  info "合计释放：约 $((bytes / 1024)) MB"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "[dry-run] 未执行删除。确认后加 --yes"
    return 0
  fi

  if [[ "$ASSUME_YES" -ne 1 ]]; then
    [[ -t 0 ]] || die "非交互环境，必须显式加 --yes 才会删除"
    read -r -p "永久删除以上内容？此操作不可恢复。[y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || { info "已取消"; return 0; }
  fi

  local freed=0 count=0
  while IFS= read -r d; do
    [[ -n "$d" ]] || continue
    # 二次确认：必须仍在暂存区内
    case "$(cd "$d" 2>/dev/null && pwd -P)" in
      "$(cd "$TRASH" && pwd -P)"/*) : ;;
      *) warn "跳过（路径校验未通过）：$d"; continue ;;
    esac
    if rm -rf "$d"; then
      count=$((count + 1))
      freed=$((freed + $(du -sk "$d" 2>/dev/null | cut -f1 | head -1 || echo 0)))
    else
      warn "删除失败（可能被占用）：$d"
    fi
  done <<< "$found"
  ok "已永久删除 $count 个条目，释放约 $((freed / 1024)) MB"
}

cmd_auto() {
  [[ -d "$ROOT" ]] || { info "源码根目录不存在：$ROOT（无需清理）"; return 0; }
  info "自动释放：扫描 status=releasable 的源码工作区…"
  local dir n status count=0 skipped=0
  while IFS= read -r dir; do
    [[ -n "$dir" ]] || continue
    [[ -f "$dir/$MARKER_FILE" ]] || continue
    n="$(basename "$dir")"
    status="$(read_field "$dir" status)"; status="${status:-in-use}"
    if [[ "$status" == "releasable" ]]; then
      do_stage "$n" && count=$((count + 1))
    else
      skipped=$((skipped + 1))
    fi
  done < <(list_workspaces)
  info "自动释放完成：移入暂存 ${count} 个，保留 ${skipped} 个（仍标记为 in-use）"
  [[ $count -gt 0 ]] && info "提示：这些内容仍在 .trash 中，${RETENTION} 天后 purge 才会真正释放磁盘；如需立即回收请手动执行 purge --older-than 0 --yes"
}

case "$CMD" in
  list)    cmd_list ;;
  stage)   cmd_stage ;;
  release) cmd_release ;;
  restore) cmd_restore ;;
  purge)   cmd_purge ;;
  auto)    cmd_auto ;;
  *)       usage ;;
esac

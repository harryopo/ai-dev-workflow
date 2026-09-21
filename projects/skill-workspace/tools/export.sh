#!/usr/bin/env bash
# 把 projects/skill-workspace/ 导出到各宿主安装位。
# 默认 dry-run：不写任何东西，只列出将要变化的文件。
# 安装位被 .gitignore 忽略，误覆盖无法靠 git 回滚，所以覆盖前先整目录备份。
# 只用 cp/sed/diff，不依赖 rsync（Git for Windows 不带 rsync）。

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

TARGETS=(
  "$(dirname "$(dirname "$SRC")")/.agents/skills/skill-workspace"
  "$HOME/.agents/skills/skill-workspace"
)

APPLY=0
for arg in "$@"; do
  case "$arg" in
    --apply)  APPLY=1 ;;
    -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
    *) echo "未知参数：$arg（可用 --apply）" >&2; exit 2 ;;
  esac
done

norm_eol() { # 目标目录内的文本统一成 LF，否则导出的 .sh 会带 \r 跑不动
  find "$1" -type f \( -name '*.sh' -o -name '*.py' -o -name '*.md' \
       -o -name '*.json' -o -name '*.yaml' \) -print0 \
    | xargs -0 -r sed -i 's/\r$//'
}

# pipefail 会让 `diff | grep` 的退出码被 diff 污染，直接 && / || 判断会得出反的结论。
# 必须先接进变量再看字符串是否为空。
changes() {
  diff -rq --strip-trailing-cr "$SRC" "$1" 2>/dev/null \
    | grep -v '^Only in .*artifacts' || true
}

for tgt in "${TARGETS[@]}"; do
  echo "=============================================="
  echo "目标：$tgt"

  case "$tgt" in
    */skill-workspace) ;;
    *) echo "拒绝：目标路径不以 skill-workspace 结尾 → $tgt" >&2; exit 3 ;;
  esac

  if [ "$APPLY" != 1 ]; then
    if [ -d "$tgt" ]; then
      echo "[dry-run] 内容差异（忽略行尾）："
      d=$(changes "$tgt")
      if [ -n "$d" ]; then
        printf '%s\n' "$d"
        echo "[dry-run] ↑ 以上将被覆盖"
      else
        echo "[dry-run] 无内容差异"
      fi
      n=$(find "$tgt" -type f | wc -l)
      echo "[dry-run] 现有 $n 个文件；artifacts/ 不导出"
    else
      echo "[dry-run] 目标不存在，将新建。"
    fi
    continue
  fi

  if [ -d "$tgt" ]; then
    bak="${tgt}.bak-${STAMP}"
    cp -r "$tgt" "$bak"
    echo "已备份到：$bak"
    rm -rf "$tgt"
  fi
  mkdir -p "$(dirname "$tgt")"
  cp -r "$SRC" "$tgt"
  rm -rf "$tgt/artifacts"
  rm -f "$tgt/.gitattributes"
  norm_eol "$tgt"

  v=$(changes "$tgt")
  if [ -n "$v" ]; then
    echo "!! 导出后仍与源有差异："
    printf '%s\n' "$v"
    echo "   备份在：$( [ -d "${tgt}.bak-${STAMP}" ] && echo "${tgt}.bak-${STAMP}" || echo '无（新建）' )"
    exit 1
  fi
  echo "校验：一致"
done

echo "=============================================="
[ "$APPLY" = 1 ] || echo "未做任何修改。确认无误后加 --apply 才真正写入。"

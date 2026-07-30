#!/usr/bin/env bash
# learnings-summary.sh - v3.6 经验被复用率自动汇总脚本
#
# 用途：每月 1 号自动跑，生成 .learnings/index.md 头部汇总
# 关联：SKILL.md 0.5.5 经验被复用率机制 / references/learnings-reuse-metric.md
#
# 用法：
#   ./learnings-summary.sh                # 扫当前目录 .learnings/
#   ./learnings-summary.sh /path/to/.learnings
#   ./learnings-summary.sh --auto-month   # 自动写入本月汇总到 index.md
#   ./learnings-summary.sh --json         # 输出 JSON 格式
#
# 退出码：
#   0 = 成功
#   1 = 找不到 .learnings 目录
#   2 = 复用率过低（< 0.01 的经验数 > 50%）

set -uo pipefail

# ===== 路径配置 =====
# 第一个非 flag 的位置参数 = LEARNINGS_DIR
LEARNINGS_DIR=".learnings"
TODAY="$(date +%Y-%m-%d)"
AUTO_MONTH=false
OUTPUT_FORMAT="text"

# 参数解析：先扫一遍参数
ARGS=()
for arg in "$@"; do
  case "$arg" in
    --auto-month) AUTO_MONTH=true ;;
    --json) OUTPUT_FORMAT="json" ;;
    --help|-h)
      echo "Usage: $0 [LEARNINGS_DIR] [--auto-month] [--json]"
      exit 0
      ;;
    -*) echo "Unknown flag: $arg"; exit 1 ;;
    *)  ARGS+=("$arg") ;;
  esac
done

# 位置参数 = LEARNINGS_DIR
if [[ ${#ARGS[@]} -gt 0 ]]; then
  LEARNINGS_DIR="${ARGS[0]}"
fi

# ===== 颜色 =====
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# ===== 验证 =====
if [[ ! -d "$LEARNINGS_DIR" ]]; then
  echo -e "${RED}❌ 找不到 $LEARNINGS_DIR 目录${NC}"
  echo "   请先在项目根目录创建 .learnings/ 子目录"
  exit 1
fi

# ===== 统计 =====
TOTAL=$(find "$LEARNINGS_DIR" -name "LRN-*.md" -not -path "*/_archived/*" 2>/dev/null | wc -l)
HIGH_COUNT=0
MID_COUNT=0
LOW_COUNT=0
HIGH_LIST=""
MID_LIST=""
LOW_LIST=""

if [[ $TOTAL -eq 0 ]]; then
  echo -e "${YELLOW}⚠️  未发现任何经验记录（LRN-*.md）${NC}"
  echo "   首次使用请参考 .learnings/template.md 创建第一条经验"
  exit 0
fi

# ===== 计算复用率 =====
while IFS= read -r file; do
  # 提取 reused_count（默认 0）
  reused=$(grep -oP '被引用次数：\K\d+' "$file" 2>/dev/null | head -1 || echo 0)
  reused=${reused:-0}

  # 提取创建日期（YYYY-MM-DD）
  created=$(grep -oP '创建日期：\K\d{4}-\d{2}-\d{2}' "$file" 2>/dev/null | head -1 || echo "$TODAY")

  # 计算天数
  if [[ "$OSTYPE" == "darwin"* ]]; then
    days=$(( ( $(date -j -f "%Y-%m-%d" "$TODAY" +%s) - $(date -j -f "%Y-%m-%d" "$created" +%s) ) / 86400 ))
  else
    days=$(( ( $(date -d "$TODAY" +%s) - $(date -d "$created" +%s) ) / 86400 ))
  fi

  # 防止除零
  [[ $days -lt 1 ]] && days=1

  # 复用率 = reused / days
  rate=$(awk "BEGIN { printf \"%.4f\", $reused / $days }")

  # 分类
  is_high=$(awk "BEGIN { print ($rate >= 0.1) ? 1 : 0 }")
  is_mid=$(awk "BEGIN { print ($rate >= 0.01 && $rate < 0.1) ? 1 : 0 }")
  is_low=$(awk "BEGIN { print ($rate < 0.01) ? 1 : 0 }")

  title=$(head -1 "$file" | sed 's/^# LRN-[0-9-]* · //')

  if [[ "$is_high" == "1" ]]; then
    ((HIGH_COUNT++))
    HIGH_LIST+="| $(basename "$file" .md) | $title | $rate 次/天 |\n"
  elif [[ "$is_mid" == "1" ]]; then
    ((MID_COUNT++))
    MID_LIST+="| $(basename "$file" .md) | $title | $rate 次/天 |\n"
  else
    ((LOW_COUNT++))
    LOW_LIST+="| $(basename "$file" .md) | $title | $rate 次/天 |\n"
  fi
done < <(find "$LEARNINGS_DIR" -name "LRN-*.md" -not -path "*/_archived/*" 2>/dev/null)

# 计算整体复用率
if [[ $TOTAL -gt 0 ]]; then
  OVERALL_RATE=$(awk "BEGIN { printf \"%.4f\", ($HIGH_COUNT * 0.1 + $MID_COUNT * 0.05 + $LOW_COUNT * 0.005) / $TOTAL }")
else
  OVERALL_RATE="0.0000"
fi

# ===== 输出 =====
if [[ "$OUTPUT_FORMAT" == "json" ]]; then
  cat <<EOF
{
  "date": "$TODAY",
  "learnings_dir": "$LEARNINGS_DIR",
  "summary": {
    "total": $TOTAL,
    "high_reuse": $HIGH_COUNT,
    "mid_reuse": $MID_COUNT,
    "low_reuse": $LOW_COUNT,
    "overall_rate": $OVERALL_RATE
  }
}
EOF
else
  echo -e "${BLUE}📊 经验复用率汇总 · $TODAY${NC}"
  echo "================================"
  echo -e "  经验库路径: $LEARNINGS_DIR"
  echo -e "  总经验数:   ${GREEN}$TOTAL${NC} 条"
  echo ""
  echo -e "  🟢 高频复用（≥ 0.1 次/天）:  $HIGH_COUNT 条"
  echo -e "  🟡 中频复用（0.01-0.1 次/天）: $MID_COUNT 条"
  echo -e "  🔴 几乎未复用（< 0.01 次/天）: $LOW_COUNT 条"
  echo ""
  echo -e "  整体复用率: ${BLUE}$OVERALL_RATE 次/天${NC}"
  echo ""

  if [[ $HIGH_COUNT -gt 0 ]]; then
    echo -e "${GREEN}🟢 高频复用 Top 经验${NC}"
    echo "| ID | 标题 | 复用率 | 评估 |"
    echo "|----|------|-------|------|"
    echo -e "$HIGH_LIST"
  fi

  if [[ $LOW_COUNT -gt 0 ]]; then
    echo -e "${RED}🔴 需回顾（几乎未复用）${NC}"
    echo "| ID | 标题 | 复用率 | 处置建议 |"
    echo "|----|------|-------|---------|"
    echo -e "$LOW_LIST"
    echo ""
    echo -e "${YELLOW}⚠️  处置建议：${NC}"
    echo "  1. 触发词不准 → 改写 .learnings/LRN-* 头部的触发词"
    echo "  2. 内容过时 → 更新或删除"
    echo "  3. 与项目不匹配 → 归档到 $LEARNINGS_DIR/_archived/"
  fi
fi

# ===== 自动写入 index.md =====
if [[ "$AUTO_MONTH" == true ]]; then
  INDEX_FILE="$LEARNINGS_DIR/index.md"
  echo ""
  echo -e "${BLUE}📝 自动写入 $INDEX_FILE${NC}"

  cat > "$INDEX_FILE" <<EOF
# 经验索引 · $TODAY 自动汇总

> **本月新增：** 0 条（脚本只统计复用率，不统计新增）
> **总经验数：** $TOTAL 条
> **高频复用（🟢）：** $HIGH_COUNT 条
> **中频复用（🟡）：** $MID_COUNT 条
> **几乎未复用（🔴）：** $LOW_COUNT 条
> **整体复用率：** $OVERALL_RATE 次/天

---

## 🟢 高频复用 Top

| ID | 标题 | 复用率 |
|----|------|-------|
$(echo -e "$HIGH_LIST" | head -10)

## 🔴 需回顾（复用率 < 0.01 次/天）

| ID | 标题 | 原因假设 | 处置 |
|----|------|---------|------|
$(echo -e "$LOW_LIST" | head -10)

---

*此文件由 learnings-summary.sh 自动生成，编辑前请先 review*
EOF
  echo -e "${GREEN}✅ 已写入 $INDEX_FILE${NC}"
fi

# ===== 退出码 =====
LOW_RATIO=$(awk "BEGIN { printf \"%.2f\", $LOW_COUNT / $TOTAL }")
LOW_THRESHOLD=$(awk "BEGIN { print ($LOW_RATIO > 0.5) ? 1 : 0 }")

if [[ "$LOW_THRESHOLD" == "1" ]]; then
  echo ""
  echo -e "${RED}❌ 经验库整体腐化：🔴 比例 $LOW_RATIO > 50%${NC}"
  exit 2
fi

exit 0

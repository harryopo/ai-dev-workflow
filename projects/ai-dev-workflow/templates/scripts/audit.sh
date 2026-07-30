#!/usr/bin/env bash
# audit.sh - v3.6 R-AUDIT-01~04 可执行审计脚本
#
# 用途：把 AGENTS.md 末尾的 4 条审查硬规则落成可执行脚本
# 适用：pre-commit hook / CI workflow / 本地手动检查
# 关联：SKILL.md 0.6 可执行审计脚本专章 / AGENTS.md 审查规则块
#
# 用法：
#   ./audit.sh                # 跑全部 4 条
#   ./audit.sh --rule 01      # 只跑 R-AUDIT-01
#   ./audit.sh --severity high # 只显示 high 级别
#   ./audit.sh --json         # 输出 JSON 格式（CI 用）
#
# 退出码：
#   0 = 全部通过
#   1 = 发现 high 级别问题（阻塞合并）
#   2 = 发现 medium 级别问题（警告，不阻塞）

set -uo pipefail

# ===== 路径配置 =====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LEARNINGS_DIR="${LEARNINGS_DIR:-$PROJECT_ROOT/.learnings}"
OUTPUT_FORMAT="text"
SEVERITY_FILTER="all"
SPECIFIC_RULE=""

# ===== 颜色 =====
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# ===== 结果收集 =====
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0
FINDINGS_JSON="[]"

# ===== 参数解析 =====
while [[ $# -gt 0 ]]; do
  case $1 in
    --rule)
      SPECIFIC_RULE="$2"
      shift 2
      ;;
    --severity)
      SEVERITY_FILTER="$2"
      shift 2
      ;;
    --json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--rule 01|02|03|04] [--severity high|medium|low|all] [--json]"
      exit 0
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done

# ===== 检测函数 =====
# 每个检测函数：
#   - 输入：$1 = 文件路径
#   - 输出：FINDINGS_JSON 更新
#   - 副作用：增加 HIGH_COUNT/MEDIUM_COUNT/LOW_COUNT

# R-AUDIT-01：参数化查询（防 SQL 注入）
check_sql_injection() {
  local file="$1"
  # 排除 node_modules、dist、build、.git
  case "$file" in
    */node_modules/*|*/dist/*|*/build/*|*/.git/*) return ;;
  esac

  # 检测 exec(`...${var}...`) 字符串拼接
  if grep -nE 'exec\s*\(\s*[`"][^`"]*\$\{[^}]+\}' "$file" >/dev/null 2>&1; then
    add_finding "$file" "R-AUDIT-01" "high" "发现 SQL 字符串拼接（exec 内含 \${...}）"
  fi

  # 检测 execute("..." + var) 拼接
  if grep -nE 'execute\s*\(\s*["\x27][^"\x27]*\+\s*[a-zA-Z_]' "$file" >/dev/null 2>&1; then
    add_finding "$file" "R-AUDIT-01" "high" "发现 Python SQL 字符串拼接（execute 含 + var）"
  fi
}

# R-AUDIT-02：API 授权检查（防越权）
check_api_auth() {
  local file="$1"
  case "$file" in
    */node_modules/*|*/dist/*|*/build/*|*/.git/*) return ;;
  esac

  # Express: app.get/post/put/delete 后跟 (req, res) 但无 auth 中间件
  # 简化检测：app.METHOD('/path', handler) 模式
  if grep -nE 'app\.(get|post|put|delete|patch)\s*\(' "$file" >/dev/null 2>&1; then
    while IFS= read -r line; do
      # 同一行检查是否有 authMiddleware / requireRole / requireOwner
      if ! echo "$line" | grep -qE '(authMiddleware|requireRole|requireOwner|requireAuth|authenticate|verifyToken)'; then
        add_finding "$file" "R-AUDIT-02" "high" "API 端点疑似无授权检查: $line"
      fi
    done < <(grep -nE 'app\.(get|post|put|delete|patch)\s*\(' "$file" | head -10)
  fi

  # FastAPI: @app.get/post 装饰器后的 def 函数无 Depends 依赖
  if grep -nE '@app\.(get|post|put|delete|patch)' "$file" >/dev/null 2>&1; then
    while IFS= read -r line; do
      if ! echo "$line" | grep -qE 'Depends\s*\('; then
        # 检查函数签名是否有 Depends 参数
        func_line=$(echo "$line" | awk -F: '{print $1}')
        next_line=$(sed -n "$((func_line+1))p" "$file" 2>/dev/null)
        if ! echo "$next_line" | grep -qE 'Depends\s*=|current_user|current_user'; then
          add_finding "$file" "R-AUDIT-02" "medium" "FastAPI 端点疑似无 Depends 鉴权: $line"
        fi
      fi
    done < <(grep -nE '@app\.(get|post|put|delete|patch)' "$file" | head -10)
  fi
}

# R-AUDIT-03：敏感信息处理（防泄露）
check_secrets() {
  local file="$1"
  case "$file" in
    */node_modules/*|*/dist/*|*/build/*|*/.git/*) return ;;
  esac

  # 检测硬编码 API key / token / password（大小写不敏感：API_KEY/api_key 都要查）
  if grep -niE "(api[_-]?key|token|password|secret|access[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}" "$file" >/dev/null 2>&1; then
    add_finding "$file" "R-AUDIT-03" "high" "发现硬编码敏感字段（API key/token/password）"
  fi

  # 检测 console.log/logging 含明文 apiKey/token
  if grep -niE "(console\.log|logger\.|print)\s*\(.*\$\{?(api[_-]?key|token|secret)" "$file" >/dev/null 2>&1; then
    add_finding "$file" "R-AUDIT-03" "medium" "发现日志可能含明文敏感字段"
  fi
}

# R-AUDIT-04：输入验证（防 XSS / 路径穿越）
check_input_validation() {
  local file="$1"
  case "$file" in
    */node_modules/*|*/dist/*|*/build/*|*/.git/*) return ;;
  esac

  # 检测 path.join(uploadDir, filename) 无 path.resolve 校验
  if grep -nE 'path\.join\s*\(\s*[^,]+,\s*[^,)]*filename' "$file" >/dev/null 2>&1; then
    if ! grep -nE 'path\.resolve|startsWith' "$file" >/dev/null 2>&1; then
      add_finding "$file" "R-AUDIT-04" "high" "文件路径使用 path.join(filename) 但无 path.resolve 校验（路径穿越风险）"
    fi
  fi

  # 检测 res.send(html`${userInput}`) 无 sanitize
  if grep -nE 'res\.send\s*\(.*html.*\$\{' "$file" >/dev/null 2>&1; then
    if ! grep -nE 'DOMPurify|sanitize|escape' "$file" >/dev/null 2>&1; then
      add_finding "$file" "R-AUDIT-04" "high" "HTML 输出含 userInput 但无 DOMPurify 转义（XSS 风险）"
    fi
  fi

  # 检测 innerHTML = 赋值
  if grep -nE '\.innerHTML\s*=' "$file" >/dev/null 2>&1; then
    add_finding "$file" "R-AUDIT-04" "medium" "使用 innerHTML 直接赋值，建议改用 textContent 或受信任 HTML"
  fi
}

# ===== Finding 收集 =====
# 用 bash 数组避免 jq 依赖（CI 环境可能没装 jq）
FINDINGS_FILES=()
FINDINGS_RULES=()
FINDINGS_SEVS=()
FINDINGS_MSGS=()

add_finding() {
  local file="$1"
  local rule="$2"
  local severity="$3"
  local msg="$4"

  case "$severity" in
    high)   ((HIGH_COUNT++)) ;;
    medium) ((MEDIUM_COUNT++)) ;;
    low)    ((LOW_COUNT++)) ;;
  esac

  if [[ "$OUTPUT_FORMAT" == "json" ]]; then
    FINDINGS_FILES+=("$file")
    FINDINGS_RULES+=("$rule")
    FINDINGS_SEVS+=("$severity")
    FINDINGS_MSGS+=("$msg")
  else
    case "$severity" in
      high)   echo -e "${RED}[HIGH]${NC} $rule: $msg in $file" ;;
      medium) echo -e "${YELLOW}[MEDIUM]${NC} $rule: $msg in $file" ;;
      low)    echo -e "${BLUE}[LOW]${NC} $rule: $msg in $file" ;;
    esac
  fi
}

# JSON 输出函数（纯 bash，无 jq 依赖）
output_json() {
  echo -n "{\"summary\":{\"high\":$HIGH_COUNT,\"medium\":$MEDIUM_COUNT,\"low\":$LOW_COUNT},\"findings\":["
  local total=${#FINDINGS_FILES[@]}
  for ((i=0; i<total; i++)); do
    [[ $i -gt 0 ]] && echo -n ","
    # JSON 转义：\ → \\, " → \", 换行 → \n
    local f r s m
    f=$(echo "${FINDINGS_FILES[$i]}" | sed 's/\\/\\\\/g; s/"/\\"/g; s/$/\\n/' | tr -d '\n' | sed 's/\\n$//')
    r="${FINDINGS_RULES[$i]}"
    s="${FINDINGS_SEVS[$i]}"
    m=$(echo "${FINDINGS_MSGS[$i]}" | sed 's/\\/\\\\/g; s/"/\\"/g')
    echo -n "{\"file\":\"$f\",\"rule\":\"$r\",\"severity\":\"$s\",\"message\":\"$m\"}"
  done
  echo "]}"
}

# ===== 入口 =====
echo -e "${BLUE}🔍 R-AUDIT 审计脚本 v3.6${NC}"
echo "  项目根: $PROJECT_ROOT"
echo "  检测范围: ${SPECIFIC_RULE:-01~04 全部}"
echo "  严重度过滤: ${SEVERITY_FILTER}"
echo ""

# 扫描范围（用 -print0 + read -d '' 处理路径空格）
# 计数用不带 -print0 的 find 以避免 $() 吃掉 \0
SCAN_COUNT=$(find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.git/*" \
  -not -path "*/.next/*" \
  -not -path "*/__pycache__/*" 2>/dev/null | wc -l)
echo -e "  扫描文件: ${GREEN}$SCAN_COUNT${NC} 个"
echo ""

# 跑检测（用 while read -d '' 处理路径空格/中文/特殊字符）
while IFS= read -r -d '' file; do
  if [[ -z "$SPECIFIC_RULE" || "$SPECIFIC_RULE" == "01" ]]; then
    check_sql_injection "$file"
  fi
  if [[ -z "$SPECIFIC_RULE" || "$SPECIFIC_RULE" == "02" ]]; then
    check_api_auth "$file"
  fi
  if [[ -z "$SPECIFIC_RULE" || "$SPECIFIC_RULE" == "03" ]]; then
    check_secrets "$file"
  fi
  if [[ -z "$SPECIFIC_RULE" || "$SPECIFIC_RULE" == "04" ]]; then
    check_input_validation "$file"
  fi
done < <(find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.git/*" \
  -not -path "*/.next/*" \
  -not -path "*/__pycache__/*" \
  -print0 2>/dev/null)

# ===== 输出汇总 =====
echo ""
echo "================================"
echo -e "  📊 审计结果汇总"
echo "================================"
echo -e "  ${RED}HIGH:${NC}   $HIGH_COUNT"
echo -e "  ${YELLOW}MEDIUM:${NC} $MEDIUM_COUNT"
echo -e "  ${BLUE}LOW:${NC}    $LOW_COUNT"
echo ""

if [[ "$OUTPUT_FORMAT" == "json" ]]; then
  output_json
  echo ""
fi

# ===== 退出码 =====
if [[ $HIGH_COUNT -gt 0 ]]; then
  echo -e "${RED}❌ 阻塞：发现 HIGH 级别问题，必须修复${NC}"
  exit 1
elif [[ $MEDIUM_COUNT -gt 0 ]]; then
  echo -e "${YELLOW}⚠️  警告：发现 MEDIUM 级别问题，建议修复${NC}"
  exit 2
else
  echo -e "${GREEN}✅ 全部通过：未发现 HIGH/MEDIUM 级别问题${NC}"
  exit 0
fi

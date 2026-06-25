#!/bin/bash

# Skill 全生命周期工作台安装脚本
# 面向所有 Agent（Claude Code、Codex CLI、ChatGPT 等）

echo "=========================================="
echo "  Skill 全生命周期工作台安装脚本"
echo "=========================================="
echo ""

# 检测 Agent 类型
detect_agent() {
    if command -v claude &> /dev/null; then
        echo "claude"
    elif command -v codex &> /dev/null; then
        echo "codex"
    else
        echo "unknown"
    fi
}

AGENT=$(detect_agent)
echo "检测到 Agent: $AGENT"

# 设置安装路径
case $AGENT in
    "claude")
        SKILLS_DIR="$HOME/.claude/skills"
        ;;
    "codex")
        SKILLS_DIR="$HOME/.codex/skills"
        ;;
    *)
        SKILLS_DIR="$HOME/.skills"
        echo "未检测到已知 Agent，使用通用路径: $SKILLS_DIR"
        ;;
esac

# 创建目录
mkdir -p "$SKILLS_DIR"

# 检查是否已安装
if [ -d "$SKILLS_DIR/skill-workspace" ]; then
    echo ""
    echo "⚠️  检测到已安装 skill-workspace"
    read -p "是否覆盖安装？(y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    echo "备份旧版本..."
    mv "$SKILLS_DIR/skill-workspace" "$SKILLS_DIR/skill-workspace.bak.$(date +%Y%m%d%H%M%S)"
fi

# 安装
echo ""
echo "正在安装 skill-workspace..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/skill-workspace" "$SKILLS_DIR/"

# 验证安装
if [ -d "$SKILLS_DIR/skill-workspace" ] && [ -f "$SKILLS_DIR/skill-workspace/SKILL.md" ]; then
    echo ""
    echo "✅ 安装成功！"
    echo ""
    echo "安装位置: $SKILLS_DIR/skill-workspace"
    echo ""
    echo "使用方法："
    case $AGENT in
        "claude")
            echo "  claude -p '使用 skill-workspace 搜索 代码格式化'"
            echo "  claude -p '使用 skill-workspace 开发 代码审查 skill'"
            echo "  claude -p '使用 skill-workspace 审查 skill-dev'"
            ;;
        "codex")
            echo "  codex '使用 skill-workspace 搜索 代码格式化'"
            echo "  codex '使用 skill-workspace 开发 代码审查 skill'"
            echo "  codex '使用 skill-workspace 审查 skill-dev'"
            ;;
        *)
            echo "  请使用你的 Agent CLI 调用 skill-workspace"
            ;;
    esac
    echo ""
    echo "📚 文档: $SKILLS_DIR/skill-workspace/README.md"
else
    echo ""
    echo "❌ 安装失败，请检查错误信息"
    exit 1
fi

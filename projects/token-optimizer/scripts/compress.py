#!/usr/bin/env python3
"""
Token压缩脚本 - 使用headroom进行智能上下文压缩
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from headroom import compress
    HEADROOM_AVAILABLE = True
except ImportError:
    HEADROOM_AVAILABLE = False


def check_dependencies():
    """检查依赖是否安装"""
    if not HEADROOM_AVAILABLE:
        print("headroom-ai未安装，正在安装...")
        os.system('pip install "headroom-ai[all]"')
        return True
    return True


def get_config_path():
    """获取配置文件路径"""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / "config" / "default.json"


def load_config():
    """加载配置"""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "threshold": 5000,
        "auto_compress": True,
        "save_history": True,
        "history_days": 30,
        "price_per_1k_tokens": 0.015
    }


def save_config(config):
    """保存配置"""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_history_path():
    """获取历史记录路径"""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / "data" / "history.json"


def load_history():
    """加载历史记录"""
    history_path = get_history_path()
    if history_path.exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_history(history):
    """保存历史记录"""
    history_path = get_history_path()
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def compress_text(text, config=None):
    """压缩文本"""
    if not check_dependencies():
        return None
    
    if config is None:
        config = load_config()
    
    try:
        result = compress(text)
        return {
            "original": text,
            "compressed": result,
            "original_tokens": len(text.split()) * 1.3,  # 估算
            "compressed_tokens": len(result.split()) * 1.3,  # 估算
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"压缩失败: {e}")
        return None


def compress_messages(messages, config=None):
    """压缩消息列表"""
    if not check_dependencies():
        return None
    
    if config is None:
        config = load_config()
    
    try:
        result = compress(messages)
        return {
            "original": messages,
            "compressed": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"压缩失败: {e}")
        return None


def analyze_compression(text):
    """分析压缩效果"""
    if not check_dependencies():
        return None
    
    try:
        compressed = compress(text)
        original_len = len(text)
        compressed_len = len(compressed)
        saved = original_len - compressed_len
        percentage = (saved / original_len) * 100 if original_len > 0 else 0
        
        return {
            "original_length": original_len,
            "compressed_length": compressed_len,
            "saved": saved,
            "percentage": round(percentage, 2),
            "compressed_text": compressed
        }
    except Exception as e:
        print(f"分析失败: {e}")
        return None


def generate_report(history):
    """生成统计报告"""
    if not history:
        return "暂无历史记录"
    
    config = load_config()
    price_per_1k = config.get("price_per_1k_tokens", 0.015)
    
    total_original = sum(h.get("original_tokens", 0) for h in history)
    total_compressed = sum(h.get("compressed_tokens", 0) for h in history)
    total_saved = total_original - total_compressed
    percentage = (total_saved / total_original * 100) if total_original > 0 else 0
    cost_saved = (total_saved / 1000) * price_per_1k
    
    report = f"""# Token 使用统计报告

## 总体统计
- 总Token使用：{total_original:,.0f}
- 总压缩节省：{total_saved:,.0f}
- 节省比例：{percentage:.1f}%
- 预估节省成本：${cost_saved:.2f}

## 压缩历史
| 时间 | 压缩前 | 压缩后 | 节省 |
|------|--------|--------|------|
"""
    
    for h in history[-10:]:  # 显示最近10条
        timestamp = h.get("timestamp", "未知")
        original = h.get("original_tokens", 0)
        compressed = h.get("compressed_tokens", 0)
        saved = original - compressed
        report += f"| {timestamp} | {original:,.0f} | {compressed:,.0f} | {saved:,.0f} |\n"
    
    return report


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python compress.py [analyze|compress|report] [text]")
        sys.exit(1)
    
    mode = sys.argv[1]
    config = load_config()
    
    if mode == "analyze":
        if len(sys.argv) < 3:
            print("用法: python compress.py analyze <text>")
            sys.exit(1)
        text = sys.argv[2]
        result = analyze_compression(text)
        if result:
            print(f"原始长度: {result['original_length']}")
            print(f"压缩后长度: {result['compressed_length']}")
            print(f"节省: {result['saved']} ({result['percentage']}%)")
            print(f"\n压缩后文本:\n{result['compressed_text']}")
    
    elif mode == "compress":
        if len(sys.argv) < 3:
            print("用法: python compress.py compress <text>")
            sys.exit(1)
        text = sys.argv[2]
        result = compress_text(text, config)
        if result:
            history = load_history()
            history.append(result)
            save_history(history)
            print(f"压缩完成!")
            print(f"压缩后文本:\n{result['compressed']}")
    
    elif mode == "report":
        history = load_history()
        report = generate_report(history)
        print(report)
    
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()

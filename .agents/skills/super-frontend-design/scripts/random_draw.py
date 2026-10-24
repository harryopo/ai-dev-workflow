#!/usr/bin/env python3
"""结构化随机抽签 —— "随便你定"时的决策工具。

用途：用户说"随便 / 都行 / 你定"时，AI 最常见的失败是**默选最保守的那一个**
（经典反收敛解），而不是给出一个合法的随机选择。本脚本提供真正的外部随机：

- 随机源是操作系统熵源（os.urandom），不是模型自造的"随机"
- 每个候选等概率 —— 抽签前不做任何偏好加权
- 抽签过程留痕：候选列表、选中项、时间戳、熵源字节，全部写进输出

设计原则（借鉴 let-fate-decide 的结构化外部随机）：
1. **一个决策点一次抽** —— 不允许一次抽多个维度再拼装
2. **禁止造假随机** —— 不得声称"随机抽到"却没有真随机调用
3. **结果必须回传给用户** —— 抽完要告知抽中了什么，不能静默替换

用法：
    python scripts/random_draw.py "变体一" "变体二" "变体三"
    python scripts/random_draw.py --json "A" "B" "C"
    python scripts/random_draw.py --from-file candidates.txt

退出码：
    0  抽签成功
    2  参数错误（候选不足 2 个 / 空候选 / 不可读文件）
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def draw(candidates):
    """从等概率候选中等概率抽取一个。

    用 os.urandom 取 4 字节做无偏 rejection sampling，避免直接取模带来的
    偏置（小概率区间被多选中）。候选数通常 < 10，取模偏置可忽略，但这里
    仍走规范路径——这条脚本的价值就在于"随机是真的"。
    """
    n = len(candidates)
    limit = (1 << 32) - ((1 << 32) % n)
    while True:
        raw = os.urandom(4)
        value = int.from_bytes(raw, "big")
        if value < limit:
            return candidates[value % n], raw.hex()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="random_draw.py", add_help=True)
    ap.add_argument("candidates", nargs="*", help="候选文本，至少 2 个")
    ap.add_argument("--from-file", help="从文件读取候选（每行一个，忽略空行与 # 注释行）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    ns = ap.parse_args(argv)

    candidates = list(ns.candidates)
    if ns.from_file:
        try:
            with open(ns.from_file, encoding="utf-8") as fh:
                candidates.extend(
                    line.strip() for line in fh
                    if line.strip() and not line.strip().startswith("#")
                )
        except OSError as exc:
            sys.stderr.write("读不到候选文件：%s\n" % exc)
            return 2

    # 去掉重复但保留顺序（同一候选出现两次不该获得两倍概率）
    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    candidates = unique

    if len(candidates) < 2:
        sys.stderr.write("抽签需要至少 2 个候选，当前只有 %d 个 —— 单候选没有随机可言\n"
                         % len(candidates))
        return 2

    picked, entropy = draw(candidates)

    result = {
        "candidates": candidates,
        "selected": picked,
        "entropy_source": "os.urandom(4) + rejection sampling",
        "entropy_hex": entropy,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "note": "等概率抽取，无偏好加权；抽签结果须回传用户，不得静默替换",
    }

    if ns.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("候选：")
        for c in candidates:
            print("  - %s" % c)
        print("抽中：%s" % picked)
        print("熵源：os.urandom(4)=%s（%s）" % (entropy, result["timestamp_utc"]))
        print("提示：结果必须回传用户；如需换方向，另起一次抽签（一个决策点一次抽）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

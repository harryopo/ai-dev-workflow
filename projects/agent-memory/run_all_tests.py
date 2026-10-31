#!/usr/bin/env python3
"""run_all_tests — agent-memory core 六模块自测聚合入口。

用法: python run_all_tests.py
全绿 exit 0；任一 FAIL exit 1。
"""
import importlib
import sys

MODULES = ["store", "retrieval", "consolidate", "snapshot", "doctor", "addressing"]


def main() -> int:
    failures = []
    for name in MODULES:
        m = importlib.import_module(f"core.{name}")
        try:
            rc = m.selftest()
            status = "PASS" if rc == 0 else "FAIL"
        except Exception as e:  # 自测抛异常 = FAIL，不让单模块异常中断全量
            status = f"FAIL({type(e).__name__}: {e})"
        if status != "PASS":
            failures.append(name)
        print(f"  {name:<12} {status}")
    print(f"\ncore 自测: {len(MODULES) - len(failures)}/{len(MODULES)} PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

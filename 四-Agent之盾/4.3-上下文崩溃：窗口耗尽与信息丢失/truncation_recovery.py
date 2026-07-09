# 文件名: truncation_recovery.py
# 功能: 超长截断兜底反推三策略，止于崩救率
# 运行: python truncation_recovery.py

"""截断崩救阶：从摘要/轮数/外部反推关键信息。"""

import random

random.seed(42)


def summary_recover(summary: str, expected_key: str) -> dict:
    return {"recovered": expected_key in summary, "method": "摘要反推"}


def turn_backtrack_recover(turns: int, key_log: dict) -> dict:
    return {"recovered": key_log.get(turns) is not None, "method": "轮数反推"}


def external_store_recover(key_id: str, ext_store: dict) -> dict:
    return {"recovered": key_id in ext_store, "method": "外部反推"}


def simulate_recovery(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        method = random.choice(["摘要", "轮数", "外部"])
        if method == "摘要":
            r = summary_recover("含关键参数的摘要", "关键参数")
            if r["recovered"]:
                success += 1
        elif method == "轮数":
            r = turn_backtrack_recover(i, {i: "关键参数"})
            if r["recovered"]:
                success += 1
        else:
            r = external_store_recover(f"key_{i}", {f"key_{i}": "关键参数"})
            if r["recovered"]:
                success += 1
    return {"n": n, "recovery_rate": success / n}


def main():
    r = simulate_recovery(30)
    print("截断崩救阶仿真结果（n=30）:")
    print(f"  崩救率: {r['recovery_rate']:.0%}（摘要/轮数/外部三策略反推）")
    print(f"  三策略: 摘要反推 / 轮数回溯 / 外部存储")


if __name__ == "__main__":
    main()

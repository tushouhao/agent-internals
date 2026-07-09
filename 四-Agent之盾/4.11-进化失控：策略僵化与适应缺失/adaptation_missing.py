# 文件名: adaptation_missing.py
# 功能: 环境变化无适应+适应检测，止于漏适率
# 运行: python adaptation_missing.py

"""适应缺失阶：多轮漏适检测，崩在漏检。"""

import random

random.seed(42)


def mock_multi_turn_env_change(turn: int, inject_change: bool = False) -> dict:
    if inject_change:
        return {"turn": turn, "adapt": None, "baseline": "ok", "changed": True}
    return {"turn": turn, "adapt": "ok", "baseline": "ok", "changed": False}


def detect_change(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"change_detected": False, "missed": True}
    return {"change_detected": call["adapt"] is None, "missed": False}


def simulate_adaptation(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_env_change(i, inject_change=random.random() < 0.84)
        r = detect_change(call, inject_miss=random.random() < 0.16)
        if r["change_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_adaptation(50)
    print("适应缺失阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（变化被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（适应检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致适应缺失残留）")
    print(f"  崩溃模式: 漏适——适应检测漏检致环境变化无从防患")


if __name__ == "__main__":
    main()

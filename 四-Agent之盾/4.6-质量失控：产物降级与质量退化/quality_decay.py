# 文件名: quality_decay.py
# 功能: 多轮累积质量退化+退化检测，止于退化漏检率
# 运行: python quality_decay.py

"""质量退化阶：多轮退化检测，崩在退化漏检。"""

import random

random.seed(42)


def mock_multi_turn_decay(turn: int, inject_decay: bool = False) -> dict:
    if inject_decay:
        return {"turn": turn, "quality": 0.9 - turn * 0.05, "baseline": 0.9, "decayed": True}
    return {"turn": turn, "quality": 0.9, "baseline": 0.9, "decayed": False}


def detect_decay(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"decay_detected": False, "missed": True}
    return {"decay_detected": call["quality"] < call["baseline"] * 0.5, "missed": False}


def simulate_decay(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_decay(i, inject_decay=random.random() < 0.88)
        r = detect_decay(call, inject_miss=random.random() < 0.12)
        if r["decay_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_decay(50)
    print("质量退化阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（退化被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（退化检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致质量退化残留）")
    print(f"  崩溃模式: 退化漏检——退化检测漏检致质量退化无从防患")


if __name__ == "__main__":
    main()

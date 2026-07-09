# 文件名: cost_explosion.py
# 功能: 单轮成本突增爆炸+突增检测，止于突增漏检率
# 运行: python cost_explosion.py

"""成本爆炸阶：单轮突增检测，崩在突增漏检。"""

import random

random.seed(42)


def mock_single_turn_spike(turn: int, inject_spike: bool = False) -> dict:
    if inject_spike:
        return {"turn": turn, "cost": 5.0, "baseline": 0.1, "spiked": True}
    return {"turn": turn, "cost": 0.1, "baseline": 0.1, "spiked": False}


def detect_spike(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"spike_detected": False, "missed": True}
    return {"spike_detected": call["cost"] > call["baseline"] * 10, "missed": False}


def simulate_spike(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_single_turn_spike(i, inject_spike=random.random() < 0.92)
        r = detect_spike(call, inject_miss=random.random() < 0.08)
        if r["spike_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_spike(50)
    print("成本爆炸阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（突增被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（突增检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致成本爆炸残留）")
    print(f"  崩溃模式: 突增漏检——突增检测漏检致成本爆炸无从防患")


if __name__ == "__main__":
    main()

# 文件名: coordination_disorder.py
# 功能: 多 Agent 协同顺序失序+失序检测，止于失序漏检率
# 运行: python coordination_disorder.py

"""协同失序阶：多轮失序检测，崩在失序漏检。"""

import random

random.seed(42)


def mock_multi_agent_disorder(turn: int, inject_disorder: bool = False) -> dict:
    if inject_disorder:
        return {"turn": turn, "order": turn + 3, "baseline": turn, "disordered": True}
    return {"turn": turn, "order": turn, "baseline": turn, "disordered": False}


def detect_disorder(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"disorder_detected": False, "missed": True}
    return {"disorder_detected": call["order"] > call["baseline"] + 2, "missed": False}


def simulate_disorder(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_agent_disorder(i, inject_disorder=random.random() < 0.87)
        r = detect_disorder(call, inject_miss=random.random() < 0.13)
        if r["disorder_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_disorder(50)
    print("协同失序阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（失序被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（失序检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致协同失序残留）")
    print(f"  崩溃模式: 失序漏检——失序检测漏检致协同失序无从防患")


if __name__ == "__main__":
    main()

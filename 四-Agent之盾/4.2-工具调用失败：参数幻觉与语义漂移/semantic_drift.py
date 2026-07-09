# 文件名: semantic_drift.py
# 功能: 跨轮工具语义漂移+漂移检测，止于漂移漏检率
# 运行: python semantic_drift.py

"""语义漂移阶：跨轮漂移检测，崩在漂移漏检。"""

import random

random.seed(42)


def mock_cross_turn_call(turn: int, inject_drift: bool = False) -> dict:
    original = "读取文件"
    if inject_drift:
        drifted = f"轮{turn} 读取文件并删除"
    else:
        drifted = original
    return {"turn": turn, "original": original, "actual": drifted, "drifted": inject_drift}


def detect_drift(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"drift_detected": False, "missed": True}
    return {"drift_detected": call["actual"] != call["original"], "missed": False}


def simulate_drift(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_cross_turn_call(i, inject_drift=random.random() < 0.96)
        r = detect_drift(call, inject_miss=random.random() < 0.04)
        if r["drift_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_drift(50)
    print("语义漂移阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（漂移被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（漂移检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致漂移残留）")
    print(f"  崩溃模式: 漂移漏检——漂移检测漏检致语义漂移无从防患")


if __name__ == "__main__":
    main()

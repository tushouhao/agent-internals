# 文件名: diagnosis_missing.py
# 功能: 运行异常无诊断+诊断检测，止于漏诊率
# 运行: python diagnosis_missing.py

"""诊断缺失阶：多轮漏诊检测，崩在漏检。"""

import random

random.seed(42)


def mock_multi_turn_anomaly(turn: int, inject_anomaly: bool = False) -> dict:
    if inject_anomaly:
        return {"turn": turn, "diagnosis": None, "baseline": "ok", "anomaly": True}
    return {"turn": turn, "diagnosis": "ok", "baseline": "ok", "anomaly": False}


def detect_anomaly(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"anomaly_detected": False, "missed": True}
    return {"anomaly_detected": call["diagnosis"] is None, "missed": False}


def simulate_diagnosis(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_anomaly(i, inject_anomaly=random.random() < 0.86)
        r = detect_anomaly(call, inject_miss=random.random() < 0.14)
        if r["anomaly_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_diagnosis(50)
    print("诊断缺失阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（异常被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（诊断检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致诊断缺失残留）")
    print(f"  崩溃模式: 漏诊——诊断检测漏检致运行异常无从防患")


if __name__ == "__main__":
    main()

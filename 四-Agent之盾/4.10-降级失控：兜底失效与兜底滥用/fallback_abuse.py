# 文件名: fallback_abuse.py
# 功能: 降级兜底被滥用+滥用检测，止于滥用率
# 运行: python fallback_abuse.py

"""兜底滥用阶：多轮滥用检测，崩在漏检。"""

import random

random.seed(42)


def mock_multi_turn_abuse(turn: int, inject_abuse: bool = False) -> dict:
    if inject_abuse:
        return {"turn": turn, "usage": turn + 3, "baseline": 1, "abused": True}
    return {"turn": turn, "usage": 1, "baseline": 1, "abused": False}


def detect_abuse(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"abuse_detected": False, "missed": True}
    return {"abuse_detected": call["usage"] > call["baseline"] * 2, "missed": False}


def simulate_abuse(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_abuse(i, inject_abuse=random.random() < 0.85)
        r = detect_abuse(call, inject_miss=random.random() < 0.15)
        if r["abuse_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_abuse(50)
    print("兜底滥用阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（滥用被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（滥用检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致滥用残留）")
    print(f"  崩溃模式: 滥用——滥用检测漏检致降级滥用无从防患")


if __name__ == "__main__":
    main()

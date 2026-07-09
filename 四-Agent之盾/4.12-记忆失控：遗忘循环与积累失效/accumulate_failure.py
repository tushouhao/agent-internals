# 文件名: accumulate_failure.py
# 功能: 记忆积累无校验+失效检测，止于漏检率
# 运行: python accumulate_failure.py

"""积累失效阶：多轮失效检测，崩在漏检。"""

import random

random.seed(42)


def mock_multi_turn_accumulate(turn: int, inject_failure: bool = False) -> dict:
    if inject_failure:
        return {"turn": turn, "memory": None, "baseline": "ok", "failed": True}
    return {"turn": turn, "memory": "ok", "baseline": "ok", "failed": False}


def detect_failure(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"failure_detected": False, "missed": True}
    return {"failure_detected": call["memory"] is None, "missed": False}


def simulate_failure(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_accumulate(i, inject_failure=random.random() < 0.83)
        r = detect_failure(call, inject_miss=random.random() < 0.17)
        if r["failure_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_failure(50)
    print("积累失效阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（失效被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（失效检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致积累失效残留）")
    print(f"  崩溃模式: 失效——失效检测漏检致记忆失效无从防患")


if __name__ == "__main__":
    main()

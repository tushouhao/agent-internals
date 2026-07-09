# 文件名: metacog_missing.py
# 功能: 元认知无校验+漏识检测，止于漏检率
# 运行: python metacog_missing.py

"""元认知缺失阶：多轮漏识检测，崩在漏检。"""

import random

random.seed(42)


def mock_multi_turn_metacog(turn: int, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"turn": turn, "metacog": None, "baseline": "ok", "missed": True}
    return {"turn": turn, "metacog": "ok", "baseline": "ok", "missed": False}


def detect_miss(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"miss_detected": False, "missed": True}
    return {"miss_detected": call["metacog"] is None, "missed": False}


def simulate_metacog(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_multi_turn_metacog(i, inject_miss=random.random() < 0.82)
        r = detect_miss(call, inject_miss=random.random() < 0.18)
        if r["miss_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_metacog(50)
    print("元认知缺失阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（漏识被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（漏识检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致元认知缺失残留）")
    print(f"  崩溃模式: 漏识——漏识检测漏检致元认知漏识无从防患")


if __name__ == "__main__":
    main()

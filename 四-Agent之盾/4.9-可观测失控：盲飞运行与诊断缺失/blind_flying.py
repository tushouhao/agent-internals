# 文件名: blind_flying.py
# 功能: Agent 无可观测信号止于盲飞检测缺失致盲飞率 100%
# 运行: python blind_flying.py

"""盲飞运行阶：无信号运行，崩在无信号。"""

import random

random.seed(42)


def mock_blind_flying(run_id: int, inject_blind: bool = False) -> dict:
    if inject_blind:
        return {"id": run_id, "signal": None, "expected": "ok", "blind": True}
    return {"id": run_id, "signal": "ok", "expected": "ok", "blind": False}


def detect_blind(signal: str, expected: str) -> bool:
    return signal == expected


def run_blind_flying(run_id: int) -> dict:
    r = mock_blind_flying(run_id, inject_blind=random.random() < 1.0)
    if detect_blind(r["signal"], r["expected"]):
        return {"observable": True, "reason": "信号正确", "blind": False}
    return {"observable": False, "reason": "盲飞运行", "blind": True}


def simulate_blind(n: int = 50) -> dict:
    observable = 0
    blind = 0
    for i in range(n):
        r = run_blind_flying(i)
        if r["observable"]:
            observable += 1
        else:
            blind += 1
    return {"observable_rate": observable / n, "blind_rate": blind / n, "n": n}


def main():
    r = simulate_blind(50)
    print("盲飞运行阶仿真结果（n=50）:")
    print(f"  可观测率: {r['observable_rate']:.0%}（信号正确即可观测）")
    print(f"  盲飞率: {r['blind_rate']:.0%}（无信号偏离预期）")
    print(f"  崩溃模式: 无信号——盲飞运行无检测即弃无从防患")


if __name__ == "__main__":
    main()

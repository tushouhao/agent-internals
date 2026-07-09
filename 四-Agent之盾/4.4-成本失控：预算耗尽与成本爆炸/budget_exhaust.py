# 文件名: budget_exhaust.py
# 功能: 多轮调用累积成本耗尽预算止于检测缺失致拒答率 100%
# 运行: python budget_exhaust.py

"""预算耗尽阶：多轮累积成本，崩在检测漏。"""

import random

random.seed(42)


def mock_multi_turn_cost(turn: int, inject_exhaust: bool = False) -> dict:
    if inject_exhaust:
        return {"turn": turn, "cost": 1.0 + turn * 0.01, "exhausted": True}
    return {"turn": turn, "cost": turn * 0.01, "exhausted": False}


def detect_budget(cost: float, budget_limit: float = 1.0) -> bool:
    return cost > budget_limit


def run_budget_exhaust(turn: int) -> dict:
    r = mock_multi_turn_cost(turn, inject_exhaust=random.random() < 1.0)
    if not detect_budget(r["cost"]):
        return {"answered": True, "reason": "预算充裕", "exhausted": False}
    return {"answered": False, "reason": "预算耗尽", "exhausted": True}


def simulate_exhaust(n: int = 50) -> dict:
    answered = 0
    exhausted = 0
    for i in range(n):
        r = run_budget_exhaust(i)
        if r["answered"]:
            answered += 1
        else:
            exhausted += 1
    return {"answered_rate": answered / n, "exhausted_rate": exhausted / n, "n": n}


def main():
    r = simulate_exhaust(50)
    print("预算耗尽阶仿真结果（n=50）:")
    print(f"  拒答率: {(1 - r['answered_rate']):.0%}（预算耗尽即弃）")
    print(f"  耗尽率: {r['exhausted_rate']:.0%}（多轮累积成本超预算）")
    print(f"  崩溃模式: 检测漏——预算耗尽无检测即弃无从防患")


if __name__ == "__main__":
    main()

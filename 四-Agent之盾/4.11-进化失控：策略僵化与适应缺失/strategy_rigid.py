# 文件名: strategy_rigid.py
# 功能: Agent 策略无适应止于僵化检测缺失致僵化率 100%
# 运行: python strategy_rigid.py

"""策略僵化阶：无适应进化，崩在无适应。"""

import random

random.seed(42)


def mock_strategy_rigid(run_id: int, inject_rigid: bool = False) -> dict:
    if inject_rigid:
        return {"id": run_id, "adapt": None, "expected": "ok", "rigid": True}
    return {"id": run_id, "adapt": "ok", "expected": "ok", "rigid": False}


def detect_rigid(adapt: str, expected: str) -> bool:
    return adapt == expected


def run_strategy_rigid(run_id: int) -> dict:
    r = mock_strategy_rigid(run_id, inject_rigid=random.random() < 1.0)
    if detect_rigid(r["adapt"], r["expected"]):
        return {"evolved": True, "reason": "适应正确", "rigid": False}
    return {"evolved": False, "reason": "策略僵化", "rigid": True}


def simulate_rigid(n: int = 50) -> dict:
    evolved = 0
    rigid = 0
    for i in range(n):
        r = run_strategy_rigid(i)
        if r["evolved"]:
            evolved += 1
        else:
            rigid += 1
    return {"evolved_rate": evolved / n, "rigid_rate": rigid / n, "n": n}


def main():
    r = simulate_rigid(50)
    print("策略僵化阶仿真结果（n=50）:")
    print(f"  进化率: {r['evolved_rate']:.0%}（适应正确即进化）")
    print(f"  僵化率: {r['rigid_rate']:.0%}（无适应偏离预期）")
    print(f"  崩溃模式: 无适应——策略僵化无检测即弃无从防患")


if __name__ == "__main__":
    main()

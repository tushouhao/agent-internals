# 文件名: race_conflict.py
# 功能: 多 Agent 并发访问共享资源止于检测缺失致冲突率 100%
# 运行: python race_conflict.py

"""竞态冲突阶：并发访问共享，崩在检测漏。"""

import random

random.seed(42)


def mock_race_conflict(agent_id: int, inject_conflict: bool = False) -> dict:
    if inject_conflict:
        return {"agent": agent_id, "shared": "in-use", "expected": "free", "conflicted": True}
    return {"agent": agent_id, "shared": "free", "expected": "free", "conflicted": False}


def detect_race(shared: str, expected: str) -> bool:
    return shared == expected


def run_race_conflict(agent_id: int) -> dict:
    r = mock_race_conflict(agent_id, inject_conflict=random.random() < 1.0)
    if detect_race(r["shared"], r["expected"]):
        return {"executed": True, "reason": "无竞态", "conflicted": False}
    return {"executed": False, "reason": "竞态冲突", "conflicted": True}


def simulate_conflict(n: int = 50) -> dict:
    executed = 0
    conflicted = 0
    for i in range(n):
        r = run_race_conflict(i)
        if r["executed"]:
            executed += 1
        else:
            conflicted += 1
    return {"executed_rate": executed / n, "conflicted_rate": conflicted / n, "n": n}


def main():
    r = simulate_conflict(50)
    print("竞态冲突阶仿真结果（n=50）:")
    print(f"  执行率: {r['executed_rate']:.0%}（无竞态即执行）")
    print(f"  冲突率: {r['conflicted_rate']:.0%}（并发访问共享资源冲突）")
    print(f"  崩溃模式: 检测漏——竞态冲突无检测即弃无从防患")


if __name__ == "__main__":
    main()

# 文件名: deadlock_graph.py
# 功能: 多 Agent 循环等待锁+死锁检测，止于死锁漏检率
# 运行: python deadlock_graph.py

"""死锁图谱阶：循环等待死锁检测，崩在死锁漏检。"""

import random

random.seed(42)


def mock_circular_wait(agent_id: int, inject_deadlock: bool = False) -> dict:
    if inject_deadlock:
        return {"agent": agent_id, "holds": "lock_B", "waits_for": "lock_A", "deadlocked": True}
    return {"agent": agent_id, "holds": "none", "waits_for": "none", "deadlocked": False}


def detect_deadlock(call: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"deadlock_detected": False, "missed": True}
    return {"deadlock_detected": call["holds"] != "none" and call["waits_for"] != "none", "missed": False}


def simulate_deadlock(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        call = mock_circular_wait(i, inject_deadlock=random.random() < 0.86)
        r = detect_deadlock(call, inject_miss=random.random() < 0.14)
        if r["deadlock_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_deadlock(50)
    print("死锁图谱阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（死锁被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（死锁检测漏检）")
    print(f"  �残留率: {r['residual_rate']:.0%}（漏检致死锁图谱残留）")
    print(f"  崩溃模式: 死锁漏检——死锁检测漏检致死锁图谱无从防患")


if __name__ == "__main__":
    main()

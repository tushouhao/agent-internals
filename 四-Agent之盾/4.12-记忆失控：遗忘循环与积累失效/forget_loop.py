# 文件名: forget_loop.py
# 功能: Agent 记忆无积累止于遗忘检测缺失致遗忘率 100%
# 运行: python forget_loop.py

"""遗忘循环阶：无积累记忆，崩在无积累。"""

import random

random.seed(42)


def mock_forget_loop(run_id: int, inject_forget: bool = False) -> dict:
    if inject_forget:
        return {"id": run_id, "memory": None, "expected": "ok", "forgotten": True}
    return {"id": run_id, "memory": "ok", "expected": "ok", "forgotten": False}


def detect_forget(memory: str, expected: str) -> bool:
    return memory == expected


def run_forget_loop(run_id: int) -> dict:
    r = mock_forget_loop(run_id, inject_forget=random.random() < 1.0)
    if detect_forget(r["memory"], r["expected"]):
        return {"accumulated": True, "reason": "记忆正确", "forgotten": False}
    return {"accumulated": False, "reason": "遗忘循环", "forgotten": True}


def simulate_forget(n: int = 50) -> dict:
    accumulated = 0
    forgotten = 0
    for i in range(n):
        r = run_forget_loop(i)
        if r["accumulated"]:
            accumulated += 1
        else:
            forgotten += 1
    return {"accumulated_rate": accumulated / n, "forgotten_rate": forgotten / n, "n": n}


def main():
    r = simulate_forget(50)
    print("遗忘循环阶仿真结果（n=50）:")
    print(f"  积累率: {r['accumulated_rate']:.0%}（记忆正确即积累）")
    print(f"  遗忘率: {r['forgotten_rate']:.0%}（无积累偏离预期）")
    print(f"  崩溃模式: 无积累——遗忘循环无检测即弃无从防患")


if __name__ == "__main__":
    main()

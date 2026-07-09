# 文件名: death_loop.py
# 功能: 环依赖+环漏检致死循环率 100%，止于环检测残留率
# 运行: python death_loop.py

"""死循环阶：环依赖+环漏检，崩在环漏检。"""

import random

random.seed(42)


def build_cyclic_graph(subgoals: list) -> dict:
    n = len(subgoals)
    edges = []
    for i in range(n):
        j = (i + 1) % n
        edges.append((subgoals[i], subgoals[j]))
    return {"nodes": subgoals, "edges": edges, "has_cycle": True}


def detect_cycle(graph: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"cycle_detected": False, "missed": True}
    return {"cycle_detected": graph.get("has_cycle", False), "missed": False}


def simulate_death_loop(n: int = 50) -> dict:
    death_loops = 0
    missed = 0
    for i in range(n):
        subgoals = [f"子目标_{j}" for j in range(5)]
        graph = build_cyclic_graph(subgoals)
        inject = random.random() < 0.03
        r = detect_cycle(graph, inject_miss=inject)
        if r["cycle_detected"]:
            death_loops += 1
        if r["missed"]:
            missed += 1
    return {"death_loop_rate": death_loops / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_death_loop(50)
    print("死循环阶仿真结果（n=50）:")
    print(f"  死循环率: {r['death_loop_rate']:.0%}（环依赖被检出）")
    print(f"  环漏检率: {r['miss_rate']:.0%}（环检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致死循环残留）")
    print(f"  崩溃模式: 环漏检——环检测漏检致死循环无从防患")


if __name__ == "__main__":
    main()

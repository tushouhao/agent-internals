# 文件名: subgoal_explosion.py
# 功能: 子目标拆分+依赖图爆炸，止于收敛率 0%
# 运行: python subgoal_explosion.py

"""子目标爆炸阶：子目标拆分+依赖图，崩在依赖炸。"""

import random

random.seed(42)


def split_subgoals(task: str, n: int) -> list:
    return [f"子目标_{i}" for i in range(n)]


def build_dependency_graph(subgoals: list) -> dict:
    n = len(subgoals)
    edges = []
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.3:
                edges.append((subgoals[i], subgoals[j]))
    return {"nodes": subgoals, "edges": edges, "edge_count": len(edges)}


def check_convergence(graph: dict) -> dict:
    n = len(graph["nodes"])
    threshold = n * 3
    if graph["edge_count"] > threshold:
        return {"converged": False, "reason": "依赖图爆炸"}
    return {"converged": True, "reason": "依赖图收敛"}


def simulate_explosion(n_tasks: int = 50, n_subgoals: int = 15) -> dict:
    converged = 0
    exploded = 0
    for i in range(n_tasks):
        subgoals = split_subgoals(f"任务_{i}", n_subgoals)
        graph = build_dependency_graph(subgoals)
        check = check_convergence(graph)
        if check["converged"]:
            converged += 1
        else:
            exploded += 1
    return {"converged_rate": converged / n_tasks, "exploded_rate": exploded / n_tasks, "n": n_tasks}


def main():
    r = simulate_explosion(50, 15)
    print("子目标爆炸阶仿真结果（n=50, subgoals=15）:")
    print(f"  收敛率: {r['converged_rate']:.0%}（依赖图收敛）")
    print(f"  爆炸率: {r['exploded_rate']:.0%}（N^2 边超阈值）")
    print(f"  崩溃模式: 依赖图爆炸——子目标间 N^2 边超 N*3 即炸")


if __name__ == "__main__":
    main()

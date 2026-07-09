# 文件名: single_agent.py
# 功能: 单 Agent 闭环（推理→工具→观察），止于工具数 ≥15 致选择降
# 运行: python single_agent.py

"""单 Agent 阶：单 Agent 闭环，崩在工具数 ≥15 致选择降。"""

import random

random.seed(42)


def mock_single_agent_step(tools: list, task: str) -> dict:
    """模拟单 Agent 步：从工具表选一个执行。工具数 ≥15 致选择降。"""
    n_tools = len(tools)
    if n_tools >= 15:
        selection_acc = 0.41
    else:
        selection_acc = 0.92
    return {"task": task, "n_tools": n_tools, "selection_acc": selection_acc, "completed": selection_acc > 0.5}


def run_single_agent(tools: list, task: str) -> dict:
    """单 Agent 闭环，工具数 ≥15 致选择降续跑 0%。"""
    r = mock_single_agent_step(tools, task)
    return {"selection_acc": r["selection_acc"], "completed": r["completed"], "continuation": 1.0 if r["completed"] else 0.0}


def simulate_single(n: int = 50, n_tools: int = 18) -> dict:
    """单 Agent 阶仿真：50 任务选择降 + 续跑率。"""
    tools = [f"tool_{i}" for i in range(n_tools)]
    completed = 0
    selection_accs = []
    for i in range(n):
        r = run_single_agent(tools, f"任务_{i}")
        selection_accs.append(r["selection_acc"])
        if r["completed"]:
            completed += 1
    return {"completed_rate": completed / n, "avg_selection_acc": sum(selection_accs) / n, "continuation_rate": completed / n, "n": n, "n_tools": n_tools}


def main():
    """单 Agent 阶 demo。"""
    r = simulate_single(50, 18)
    print("单 Agent 阶仿真结果（n=50, tools=18）:")
    print(f"  完成率: {r['completed_rate']:.0%}（工具数 ≥15 致选择降）")
    print(f"  均选择准确率: {r['avg_selection_acc']:.0%}（工具乱致选择降 41%）")
    print(f"  续跑率: {r['continuation_rate']:.0%}（选择降即从头重跑工具零复用）")
    print(f"  崩溃模式: 工具数 ≥15 致选择降——长程任务工具多必乱无从复用")


if __name__ == "__main__":
    main()

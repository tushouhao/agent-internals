# 文件名: single_goal_fail.py
# 功能: 单目标规划止于工具不可用致完成率 0%
# 运行: python single_goal_fail.py

"""单目标失败阶：单目标规划，崩在工具断。"""

import random

random.seed(42)


def mock_single_goal_plan(task: str, tool_available: bool) -> dict:
    if tool_available:
        return {"task": task, "completed": True, "reason": "工具可用"}
    return {"task": task, "completed": False, "reason": "工具断"}


def run_single_goal(task: str) -> dict:
    tool_available = random.random() < 0.0
    return mock_single_goal_plan(task, tool_available)


def simulate_single(n: int = 50) -> dict:
    completed = 0
    tool_break = 0
    for i in range(n):
        r = run_single_goal(f"任务_{i}")
        if r["completed"]:
            completed += 1
        else:
            tool_break += 1
    return {"completed_rate": completed / n, "tool_break_rate": tool_break / n, "n": n}


def main():
    r = simulate_single(50)
    print("单目标失败阶仿真结果（n=50）:")
    print(f"  完成率: {r['completed_rate']:.0%}（工具断即弃）")
    print(f"  工具断率: {r['tool_break_rate']:.0%}（工具不可用）")
    print(f"  崩溃模式: 工具断——单目标规划工具不可用即弃无降级")


if __name__ == "__main__":
    main()

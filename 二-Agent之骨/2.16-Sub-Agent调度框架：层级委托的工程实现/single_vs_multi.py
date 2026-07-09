# 文件名: single_vs_multi.py
# 功能: 单 Agent 闭环崩点量化 + 多 Agent 委托动机骨架
# 运行: python single_vs_multi.py

"""单 Agent 闭环容量上限与多 Agent 委托动机。"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SingleAgentCollapse:
    """单 Agent 闭环崩点: 名称/量化/原因。"""
    name: str
    metric: str
    root_cause: str


@dataclass
class TaskProfile:
    """任务画像: 判据是否该派子 Agent。"""
    context_tokens: int
    tool_count: int
    subtask_count: int
    debug_trace_req: float


def should_delegate(task: TaskProfile) -> Tuple[bool, str]:
    """判据: 是否该派子 Agent（教学版简化判据）。"""
    reasons = []
    if task.context_tokens > 32000:
        reasons.append(f"上下文炸（{task.context_tokens} token > 32k，compaction 损 18%）")
    if task.tool_count >= 15:
        reasons.append(f"工具乱（{task.tool_count} 个 ≥15，选择准确率降 41%）")
    if task.subtask_count >= 3 and task.debug_trace_req >= 0.70:
        reasons.append(f"调式盲（{task.subtask_count} 子任务交错，trace 73% 无法定位）")
    if reasons:
        return True, " + ".join(reasons)
    return False, "单 Agent 闭环可承载（上下文/工具/子任务均在上限内）"


def main():
    """单 vs 多 Agent 决策演示。"""
    collapses = [
        SingleAgentCollapse("上下文炸", "32k token 超载 → compaction 损 18% 关键信息",
                           "子任务上下文混入主任务，相互污染"),
        SingleAgentCollapse("工具乱", "工具数 ≥15 → LLM 选择准确率降 41%",
                           "单 Agent 注册所有工具，选择空间过大"),
        SingleAgentCollapse("调式盲", "多子任务交错 → 调式 trace 73% 无法定位",
                           "单 Agent loop 状态机只记单流，多流交错失序"),
    ]

    print("=== 单 Agent 闭环三类崩点 ===")
    for c in collapses:
        print(f"  {c.name:8s} | {c.metric}")
        print(f"          | 原因: {c.root_cause}")

    print("\n=== 崩点本质: 单 Agent 闭环容量上限 ===")
    print("上下文窗口 32k / 工具选择准确率上限 15 个 / 调式 trace 可读性上限 3 流")
    print("复杂任务超出上限 → 崩 → 解法: 层级委托（主 Agent 派子 Agent）")

    print("\n=== 是否该派子 Agent 判据演示 ===")
    cases = [
        TaskProfile(5000, 5, 1, 0.50),
        TaskProfile(45000, 20, 4, 0.80),
        TaskProfile(35000, 8, 2, 0.60),
        TaskProfile(10000, 18, 2, 0.50),
    ]
    labels = ["场景A 简单任务", "场景B 复杂任务三崩点全中", "场景C 上下文炸单项", "场景D 工具乱单项"]
    for label, task in zip(labels, cases):
        delegate, reason = should_delegate(task)
        choice = "派子 Agent" if delegate else "单 Agent 闭环"
        print(f"  {label}: ctx{task.context_tokens}t | 工具{task.tool_count}个 | 子任务{task.subtask_count}个 | 调式{task.debug_trace_req:.0%}")
        print(f"    → {choice}")
        print(f"    原因: {reason}")


if __name__ == "__main__":
    main()

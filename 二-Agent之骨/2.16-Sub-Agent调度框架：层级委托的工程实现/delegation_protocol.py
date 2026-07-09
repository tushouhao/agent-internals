# 文件名: delegation_protocol.py
# 功能: 委托协议三件套 + 序列化契约骨架
# 运行: python delegation_protocol.py

"""主→子委托协议: task/ctx/budget 三件套序列化契约。"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskDescription:
    """task 件: 目标 + 输入/输出 schema + 验收判据。"""
    goal: str
    input_schema: Dict[str, str]
    output_schema: Dict[str, str]
    acceptance_criteria: str


@dataclass
class ContextFragment:
    """ctx 件: 主 Agent 抽取的上下文切片（序列化副本）。"""
    relevant_history: List[str]
    relevant_tools: List[str]
    parent_summary: str


@dataclass
class Budget:
    """budget 件: token/工具/时间三上限。"""
    max_tokens: int
    max_tool_calls: int
    max_seconds: int


@dataclass
class DelegationContract:
    """委托契约: 三件套打包（主→子传递的是序列化副本）。"""
    task: TaskDescription
    ctx: ContextFragment
    budget: Budget
    delegate_id: str


@dataclass
class DelegationResult:
    """子 Agent 回执: 结果 + 状态 + 耗费。"""
    delegate_id: str
    result: Dict[str, Any]
    status: str
    cost_tokens: int
    cost_tool_calls: int
    cost_seconds: int


def main():
    """委托协议三件套演示。"""
    print("=== 委托协议三件套 ===")
    print("件一 task 描述: 目标 + 输入/输出 schema + 验收判据（40 行）")
    print("件二 ctx 上下文片段: 主 Agent 抽取的相关切片（30 行，序列化副本）")
    print("件三 budget 预算: token/工具/时间三上限（20 行）")

    contract = DelegationContract(
        task=TaskDescription(
            goal="从给定 URL 列表抓取商品价格并汇总",
            input_schema={"urls": "List[str]", "currency": "str"},
            output_schema={"prices": "List[Dict]", "avg": "float"},
            acceptance_criteria="所有 URL 抓到价格 + avg 精确到 2 位小数"),
        ctx=ContextFragment(
            relevant_history=["用户问: 帮我比价这 5 个 URL"],
            relevant_tools=["fetch_url", "parse_price"],
            parent_summary="主 Agent 已确认用户需求是比价"),
        budget=Budget(max_tokens=8000, max_tool_calls=10, max_seconds=120),
        delegate_id="del_001")

    print("\n--- 委托契约示例 ---")
    print(f"delegate_id: {contract.delegate_id}")
    print(f"task.goal: {contract.task.goal}")
    print(f"task.input_schema: {contract.task.input_schema}")
    print(f"task.output_schema: {contract.task.output_schema}")
    print(f"task.acceptance: {contract.task.acceptance_criteria}")
    print(f"ctx.relevant_history: {contract.ctx.relevant_history}")
    print(f"ctx.relevant_tools: {contract.ctx.relevant_tools}")
    print(f"ctx.parent_summary: {contract.ctx.parent_summary}")
    print(f"budget: max_tokens={contract.budget.max_tokens} / max_tool_calls={contract.budget.max_tool_calls} / max_seconds={contract.budget.max_seconds}")

    result = DelegationResult(
        delegate_id="del_001",
        result={"prices": [{"url": "u1", "price": 99.5}], "avg": 99.5},
        status="完成",
        cost_tokens=3200,
        cost_tool_calls=5,
        cost_seconds=45)

    print("\n--- 子 Agent 回执示例 ---")
    print(f"delegate_id: {result.delegate_id}（与契约关联）")
    print(f"result: {result.result}")
    print(f"status: {result.status}（四态之一，第 4 章拆）")
    print(f"cost: tokens={result.cost_tokens}/{contract.budget.max_tokens} | tools={result.cost_tool_calls}/{contract.budget.max_tool_calls} | seconds={result.cost_seconds}/{contract.budget.max_seconds}")

    print("\n=== 序列化契约设计要点 ===")
    print("1. 主→子传递的是数据副本非引用（子改不影响主）")
    print("2. 与 2.4 工具结果回灌「四类异质统一序列化」思路同构")
    print("3. ctx 是主 Agent 上下文的序列化切片，非共享内存")
    print("4. 隔离让子 Agent 可放心执行不污染主 Agent")


if __name__ == "__main__":
    main()

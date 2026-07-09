# 文件名: result_arbitration.py
# 功能: 子 Agent 回执四态判据 + 主 Agent 仲裁动作骨架
# 运行: python result_arbitration.py

"""回执仲裁: 四态判据（完成/部分/失败/越界）+ 仲裁动作。"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class Budget:
    max_tokens: int
    max_tool_calls: int
    max_seconds: int


@dataclass
class DelegationResultV2:
    """子 Agent 回执（承接第 2 章 DelegationResult + 四态判据字段）。"""
    delegate_id: str
    result: Dict[str, Any]
    status: str
    cost_tokens: int
    cost_tool_calls: int
    cost_seconds: int
    budget_limit: Budget
    acceptance_criteria: str
    tools_called: List[str] = field(default_factory=list)
    sensitive_output: bool = False


def deterministic_check(result: DelegationResultV2, expected_schema: Dict[str, str]) -> Tuple[bool, List[str]]:
    """deterministic 轨: output schema 字段完备性校验。返回 (是否合, 缺字段)。"""
    missing = [k for k in expected_schema if k not in result.result]
    return (len(missing) == 0, missing)


def llm_judge_simulate(result: DelegationResultV2, criteria: str) -> Tuple[bool, str]:
    """LLM-judge 轨模拟: 语义判验收判据是否过（教学模拟）。"""
    if result.status == "完成":
        return True, "LLM-judge 模拟: status=完成，验收判据语义过"
    if result.status == "部分":
        return False, "LLM-judge 模拟: status=部分，验收判据语义部分过"
    return False, "LLM-judge 模拟: status 异常，验收判据不过"


def classify_four_state(result: DelegationResultV2, expected_schema: Dict[str, str]) -> str:
    """四态判据: deterministic + LLM-judge 双轨 + 越界单独判。"""
    if (result.cost_tokens > result.budget_limit.max_tokens
        or result.cost_tool_calls > result.budget_limit.max_tool_calls
        or result.cost_seconds > result.budget_limit.max_seconds
        or result.sensitive_output):
        return "越界"

    schema_ok, missing = deterministic_check(result, expected_schema)
    semantic_ok, _ = llm_judge_simulate(result, result.acceptance_criteria)

    if schema_ok and semantic_ok:
        return "完成"
    if not schema_ok and len(missing) < len(expected_schema):
        return "部分"
    return "失败"


def arbitrate(state: str, result: DelegationResultV2) -> str:
    """主 Agent 据四态做仲裁动作。"""
    if state == "完成":
        return f"收纳: result {result.result} 入主 ctx（双轨校验过）"
    if state == "部分":
        return "续派: 补 budget 30% 再埋试（deterministic 定缺字段 + LLM-judge 估补量）"
    if state == "失败":
        return "重派: 换策略（如串行→并行）或换子 Agent（deterministic 异常码 + LLM-judge 估换策略）"
    return "丢弃: 警报 + 回滚主 ctx 已派变更 + 子 Agent 记黑名单（越界）"


def main():
    """四态判据与仲裁演示。"""
    budget = Budget(max_tokens=8000, max_tool_calls=10, max_seconds=120)
    expected = {"prices": "List[Dict]", "avg": "float"}

    cases = [
        DelegationResultV2("del_001", {"prices": [{"u": 99}], "avg": 99.0}, "完成",
                          3200, 5, 45, budget, "所有 URL 抓到价格 + avg 精确 2 位"),
        DelegationResultV2("del_002", {"prices": [{"u": 99}]}, "部分",
                          3000, 4, 40, budget, "所有 URL 抓到价格 + avg 精确 2 位"),
        DelegationResultV2("del_003", {"error": "timeout"}, "失败",
                          7800, 9, 119, budget, "所有 URL 抓到价格 + avg 精确 2 位"),
        DelegationResultV2("del_004", {"prices": [{"u": 999999}]}, "完成",
                          9500, 12, 130, budget, "所有 URL 抓到价格", sensitive_output=True),
    ]
    labels = ["场景A 完成", "场景B 部分（缺 avg）", "场景C 失败（error）", "场景D 越界（budget 超耗+涉敏）"]

    print("=== 四态判据演示（deterministic + LLM-judge 双轨）===")
    for label, r in zip(labels, cases):
        state = classify_four_state(r, expected)
        action = arbitrate(state, r)
        print(f"\n--- {label} ---")
        print(f"  回执: status={r.status} | cost {r.cost_tokens}/{r.budget_limit.max_tokens}t {r.cost_tool_calls}/{r.budget_limit.max_tool_calls}tools {r.cost_seconds}/{r.budget_limit.max_seconds}s | �涉敏{r.sensitive_output}")
        print(f"  四态判据: {state}")
        print(f"  仲裁动作: {action}")

    print("\n=== 双轨校验承接 2.5 验证护栏 ===")
    print("deterministic 轨: output schema 字段完备性 + budget 上限 + 越界码")
    print("LLM-judge 轨: 验收判据语义判（教学模拟，生产用真 LLM）")
    print("双轨原因: schema 合不代表语义对（如 avg 算错 schema 合但语义不过）")


if __name__ == "__main__":
    main()

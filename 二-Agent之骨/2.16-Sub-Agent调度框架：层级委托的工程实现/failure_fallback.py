# 文件名: failure_fallback.py
# 功能: 四类失败模式兜底动作与代价骨架
# 运行: python failure_fallback.py

"""失败兜底: 超时/异常/越界/资源耗尽四类各挂兜底动作与代价。"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class FailureFallback:
    """失败兜底画像: 模式/判据/动作/代价/承接。"""
    mode: str
    criteria: str
    action: str
    cost: str
    carry_from: str


@dataclass
class SubAgentFailure:
    """子 Agent 失败事件画像。"""
    delegate_id: str
    mode: str
    cost_already_spent: int
    exception_code: str = ""
    rollback_scope: List[str] = field(default_factory=list)


def apply_fallback(event: SubAgentFailure, budget_limit: int) -> Tuple[str, str, str]:
    """据失败模式套兜底，返回 (动作, 代价, 后续)。"""
    if event.mode == "超时":
        wasted = event.cost_already_spent
        return ("强杀 + 重派换策略（如串行→并行）",
                f"浪费已耗 {wasted}t + 延迟 +60s",
                "重派换策略续试")
    if event.mode == "异常":
        return (f"异常码 {event.exception_code} 定位 + 重派换子 Agent",
                "浪费已耗 + 冷启动 +30s",
                "换子 Agent 续试")
    if event.mode == "越界":
        return ("丢弃 + 回滚主 ctx 已派变更 + 子 Agent 记黑名单",
                f"主 ctx 回滚 {len(event.rollback_scope)} 项 + 子 Agent 永弃",
                "跳过该子任务或换新子 Agent")
    if event.mode == "资源耗尽":
        return ("降级（缩验收判据）+ 主 Agent 接手剩余",
                "主 Agent 上下文压 +18%",
                "主 Agent 局部执行")
    return ("未知失败模式", "-", "人工介入")


def main():
    """四类失败兜底演示。"""
    fallbacks = [
        FailureFallback("超时", "cost_seconds > max_seconds",
                        "强杀 + 重派换策略", "浪费已耗 budget + 延迟 +60s", "2.4 工具超时"),
        FailureFallback("异常", "子 Agent 抛 exception",
                        "异常码定位 + 重派换子 Agent", "浪费已耗 + 冷启动 +30s", "2.4 工具异常"),
        FailureFallback("越界", "budget 超耗/工具越权/涉敏",
                        "丢弃 + 回滚 + 黑名单", "主 ctx 回滚 80 行 + 子 Agent 永弃", "2.5 验证护栏"),
        FailureFallback("资源耗尽", "续派补 budget 仍不过",
                        "降级 + 主 Agent 接手", "主 Agent 上下文压 +18%", "2.3 compaction"),
    ]

    print("=== 四类失败兜底对照 ===")
    print(f"{'模式':8s} | {'判据':24s} | {'动作':28s} | {'代价':28s} | 承接")
    for fb in fallbacks:
        print(f"{fb.mode:8s} | {fb.criteria:24s} | {fb.action:28s} | {fb.cost:28s} | {fb.carry_from}")

    print("\n=== 失败事件套兜底演示 ===")
    events = [
        SubAgentFailure("del_001", "超时", 5000),
        SubAgentFailure("del_002", "异常", 3000, exception_code="ToolParseError"),
        SubAgentFailure("del_003", "越界", 9500, rollback_scope=["ctx.line_5", "ctx.line_6"]),
        SubAgentFailure("del_004", "资源耗尽", 7800),
    ]
    labels = ["场景A 超时", "场景B 异常", "场景C 越界", "场景D 资源耗尽"]
    for label, event in zip(labels, events):
        action, cost, follow = apply_fallback(event, 8000)
        print(f"\n--- {label} ---")
        print(f"  失败模式: {event.mode} | 已耗: {event.cost_already_spent}t")
        print(f"  兜底动作: {action}")
        print(f"  代价: {cost}")
        print(f"  后续: {follow}")

    print("\n=== 兜底承接关系 ===")
    print("超时/异常 兜底承接 2.4 工具结果回灌的错误传播思路（异常码定位）")
    print("越界 兜底承接 2.5 验证护栏的越界拦截（回滚 + 黑名单）")
    print("资源耗尽 兜底承接 2.3 compaction 的上下文压降（降级 + 主接手）")


if __name__ == "__main__":
    main()

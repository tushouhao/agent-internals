# 文件名: redline_decision.py
# 功能: 四红线判据串联决策 + 默认拦截演示
# 运行: python redline_decision.py

"""何时上 MCP 的四红线串联判据骨架。"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ProjectContext:
    """项目上下文: 四红线判据的输入。"""
    interop_task_ratio: float    # 互操作任务占比 0-1
    tool_reuse_clients: int      # 工具复用客户端数
    protocol_capability_cover: float  # 协议能力覆盖率 0-1
    lag_tolerance_months: int    # 协议滞后容忍月数


def check_redlines(ctx: ProjectContext) -> Tuple[bool, str, str]:
    """四红线串联决策，任何一条不过即拦截。
    返回: (是否上 MCP, 决策, 原因)
    """
    redlines = [
        (ctx.interop_task_ratio >= 0.30,
         f"红线一 互操作任务占比 {ctx.interop_task_ratio*100:.0f}% ≥ 30%",
         f"红线一 不过: 互操作任务占比 {ctx.interop_task_ratio*100:.0f}% < 30%，留原生"),
        (ctx.tool_reuse_clients >= 3,
         f"红线二 工具复用 {ctx.tool_reuse_clients} 家客户端 ≥ 3",
         f"红线二 不过: 工具复用 {ctx.tool_reuse_clients} 家 < 3，复用价值未达门槛"),
        (ctx.protocol_capability_cover >= 0.85,
         f"红线三 协议能力覆盖率 {ctx.protocol_capability_cover*100:.0f}% ≥ 85%",
         f"红线三 不过: 覆盖率 {ctx.protocol_capability_cover*100:.0f}% < 85%，等协议迭代"),
        (ctx.lag_tolerance_months <= 6,
         f"红线四 协议滞后容忍 {ctx.lag_tolerance_months} 月 ≤ 6 月",
         f"红线四 不过: 滞后容忍 {ctx.lag_tolerance_months} 月 > 6 月，核心能力留私有"),
    ]
    for passed, pass_msg, fail_msg in redlines:
        if not passed:
            return False, "拦截", fail_msg
    return True, "通过", "四红线全过，按谱二混合谱系上 MCP"


def main():
    """三组项目上下文的四红线判据演示。"""
    cases = [
        ProjectContext(0.20, 1, 0.90, 3),   # 互操作占比低 + 复用少
        ProjectContext(0.40, 4, 0.80, 4),   # 覆盖率不足
        ProjectContext(0.50, 5, 0.90, 6),   # 全过
    ]
    labels = ["场景A 内部工具为主", "场景B 协议未覆盖核心能力", "场景C 跨 Agent 协作平台"]

    print("=== 四红线串联判据 ===\n")
    for label, ctx in zip(labels, cases):
        print(f"--- {label} ---")
        print(f"  互操作占比 {ctx.interop_task_ratio*100:.0f}% | 复用 {ctx.tool_reuse_clients} 家 | 覆盖率 {ctx.protocol_capability_cover*100:.0f}% | 滞后容忍 {ctx.lag_tolerance_months} 月")
        passed, decision, reason = check_redlines(ctx)
        print(f"  决策: {decision}")
        print(f"  原因: {reason}\n")

    print("=== 默认拦截哲学 ===")
    print("  标准化收益（摊薄 73%）显性可见")
    print("  标准化代价（翻译损耗/协议滞后）隐性累积")
    print("  默认拦截倒逼先量隐性代价再决定")
    print("  与卷二 2.13 托管式护栏同构: 显性收益 vs 隐性代价的默认保守")

    print("\n=== 四红线 vs 三红线 ===")
    print("  卷二 2.8-2.13 每篇三红线（调敏/具敏/成敏）")
    print("  本篇四红线多一条「协议滞后容忍」")
    print("  原因: MCP 是跨框架协议层，时间维度代价首次显题")


if __name__ == "__main__":
    main()

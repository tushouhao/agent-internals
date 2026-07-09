# 文件名: seven_redlines.py
# 功能: 七串联判据决策 + 生死级剪枝优先骨架
# 运行: python seven_redlines.py

"""选型决策的七串联判据骨架。"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class FullProjectContext:
    """完整项目上下文: 七红线判据的输入。"""
    task_life_months: float
    estimated_loc: int
    is_core_business: bool
    compliance_local: bool
    needs_custom_depth: bool
    debug_transparency_req: float
    vendor_tolerance: float
    interop_ratio: float
    reuse_clients: int
    protocol_cover: float
    lag_tolerance_months: int
    team_size: int
    roi_payback_months: int
    is_prototype: bool


def seven_redlines_decision(ctx: FullProjectContext) -> Tuple[str, str]:
    """七串联判据决策，生死级剪枝优先。返回 (选型, 原因)。"""
    # 生死级剪枝优先: 不该托管的三类
    if ctx.is_core_business or ctx.compliance_local or ctx.needs_custom_depth or ctx.debug_transparency_req >= 0.70:
        return "自研 harness", "生死级剪枝: 核心商业/合规本地/定制深度/调试透明 ≥70% → 自研"

    # 效率级剪枝: 不该自研的三类
    if ctx.is_prototype:
        return "框架内编排", "效率级剪枝: 原型验证快速试错 → 框架内"
    if ctx.task_life_months < 1:
        return "托管 loop", f"效率级剪枝: 短平快任务 {ctx.task_life_months} 月 <1 → 托管"
    if ctx.task_life_months < 3 and ctx.estimated_loc < 280:
        return "托管 loop", "效率级剪枝: 寿命 <3 月 + 工程 <280 行 → 托管"

    # 根节点串联判据: 寿命 ≥3 AND 工程量 ≥280
    if ctx.task_life_months >= 3 and ctx.estimated_loc >= 280:
        if ctx.vendor_tolerance >= 0.60:
            return "托管 loop", "根通过 + 厂商容忍 ≥60% → 托管 loop（护栏后 90-200 行）"
        if (ctx.interop_ratio >= 0.30 and ctx.reuse_clients >= 3
            and ctx.protocol_cover >= 0.85 and ctx.lag_tolerance_months <= 6):
            return "MCP 谱二混合", "根通过 + 协议四红线全过 → MCP 谱二混合（180 行）"
        if ctx.team_size >= 2 and ctx.roi_payback_months <= 6:
            return "框架内编排", "根通过 + 团队 ≥2 + ROI ≤6 月 → 框架内编排（80-200 行）"
        return "自研 harness", "根通过但各岔不过 → 默认自研 harness（280-450 行）"

    return "托管 loop", "默认托管（根判据边缘 + 无生死级触发）"


def main():
    """七串联判据决策演示。"""
    cases = [
        FullProjectContext(0.5, 50, False, False, False, 0.50, 0.80,
                          0.05, 1, 0.90, 3, 1, 1, False),
        FullProjectContext(12, 500, True, False, False, 0.50, 0.20,
                          0.10, 1, 0.90, 3, 3, 8, False),
        FullProjectContext(8, 350, False, False, False, 0.50, 0.40,
                          0.50, 5, 0.90, 6, 2, 5, False),
        FullProjectContext(6, 300, False, False, False, 0.50, 0.70,
                          0.10, 1, 0.90, 3, 2, 4, False),
        FullProjectContext(3, 280, False, False, False, 0.50, 0.50,
                          0.10, 1, 0.90, 3, 2, 5, True),
        FullProjectContext(6, 400, False, False, False, 0.60, 0.50,
                          0.10, 1, 0.90, 3, 2, 6, False),
    ]
    labels = ["A 短平快", "B 核心商业", "C 跨Agent协作", "D 中期托管",
              "E 原型验证", "F 中期框架内"]

    print("=== 七串联判据决策演示 ===\n")
    for label, ctx in zip(labels, cases):
        choice, reason = seven_redlines_decision(ctx)
        print(f"--- {label} ---")
        print(f"  寿命{ctx.task_life_months}月 | 工程{ctx.estimated_loc}行 | 核心{ctx.is_core_business} | 合规{ctx.compliance_local} | 深度{ctx.needs_custom_depth} | 调式{ctx.debug_transparency_req:.0%}")
        print(f"  厂商容忍{ctx.vendor_tolerance:.0%} | 互操作{ctx.interop_ratio:.0%} | 复用{ctx.reuse_clients}家 | 团队{ctx.team_size}人 | 原型{ctx.is_prototype}")
        print(f"  → 选型: {choice}")
        print(f"  原因: {reason}\n")

    print("=== 七红线汇总 ===")
    print("红线一 寿命 ≥3 月        → 不过走全自研")
    print("红线二 工程量 ≥280 行    → 不过走全自研")
    print("红线三 调式 ≥70% OR 核心OR合规OR深度 → 过走自研 loop")
    print("红线四 厂商容忍 ≥60% 非生死 → 过走托管 loop")
    print("红线五 协议四红线全过    → 过走 MCP 谱二")
    print("红线六 团队 ≥2 + ROI ≤6 月 → 过走框架内")
    print("红线七 原型验证快速试错   → 过剪向框架内")
    print("\n优先级: 生死级剪枝（红线三）> 效率级剪枝（红线七/一/二）> 根节点 > 各岔")


if __name__ == "__main__":
    main()

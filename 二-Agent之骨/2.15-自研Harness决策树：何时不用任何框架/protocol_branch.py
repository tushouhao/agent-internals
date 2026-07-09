# 文件名: protocol_branch.py
# 功能: 第三岔承接 2.14 四红线判据 + 决策树引用骨架
# 运行: python protocol_branch.py

"""第三岔: 要不要上 MCP 协议层（承接 2.14 四红线，不重拆判据）。"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ProjectForProtocol:
    """项目对协议层的需求画像（承接 2.14 四红线输入）。"""
    interop_ratio: float
    reuse_clients: int
    protocol_capability_cover: float
    lag_tolerance_months: int


def decide_protocol_branch(ctx: ProjectForProtocol) -> Tuple[str, str]:
    """第三岔承接 2.14 四红线串联判据，返回 (叶节点, 原因)。"""
    if ctx.interop_ratio < 0.30:
        return "原生工具", f"红线一不过: 互操作占比 {ctx.interop_ratio*100:.0f}% < 30%"
    if ctx.reuse_clients < 3:
        return "原生工具", f"红线二不过: 复用 {ctx.reuse_clients} 家 < 3"
    if ctx.protocol_capability_cover < 0.85:
        return "撒谎 schema 过渡", f"红线三不过: 覆盖率 {ctx.protocol_capability_cover*100:.0f}% < 85%，等协议迭代"
    if ctx.lag_tolerance_months > 6:
        return "原生为主", f"红线四不过: 滞后容忍 {ctx.lag_tolerance_months} 月 > 6 月，核心能力留私有"
    return "MCP server + 原生混合谱二", "四红线全过，按 2.14 谱二混合（180 行配置）"


def main():
    """第三岔承接岔演示。"""
    print("=== 第三岔: 承接 2.14 四红线判据 ===")
    print("承接岔不重拆判据，决策树直接引用 2.14 阈值:")
    print("  红线一 互操作任务占比 ≥30%")
    print("  红线二 工具复用 ≥3 家客户端")
    print("  红线三 协议能力覆盖率 ≥85%")
    print("  红线四 协议滞后容忍 ≤6 月")

    print("\n=== 第三岔四红线串联分流演示 ===")
    cases = [
        ProjectForProtocol(0.20, 1, 0.90, 3),
        ProjectForProtocol(0.40, 2, 0.90, 4),
        ProjectForProtocol(0.50, 4, 0.80, 4),
        ProjectForProtocol(0.50, 5, 0.90, 8),
        ProjectForProtocol(0.50, 5, 0.90, 6),
    ]
    labels = ["场景A 内部工具为主", "场景B 复用价值未达门槛", "场景C 协议未覆盖核心能力",
              "场景D 滞后容忍超期", "场景E 跨 Agent 协作平台"]
    for label, ctx in zip(labels, cases):
        leaf, reason = decide_protocol_branch(ctx)
        print(f"  {label}")
        print(f"    互操作{ctx.interop_ratio*100:.0f}% | 复用{ctx.reuse_clients}家 | 覆盖{ctx.protocol_capability_cover*100:.0f}% | 滞后容忍{ctx.lag_tolerance_months}月")
        print(f"    → 叶: {leaf}（{reason}）")

    print("\n=== 承接岔设计收益 ===")
    print("  决策树不重复 2.14 已拆透的判据，保持树简洁")
    print("  与卷二 2.9 承接 2.8 六短板的承接篇套路同构")
    print("  叶节点直接挂 2.14 谱二混合（180 行配置）的实测甜点")
    print("  阈值校准时只改 2.14 一处，决策树自动同步")

    print("\n--- 第三岔叶节点工程量 ---")
    print("原生工具: 50-200 行（承接 2.6 Skill 工程 + 2.14 原生谱）")
    print("MCP server + 原生混合谱二: 180 行（承接 2.14 甜点实测）")
    print("撒谎 schema 过渡: +30 行隐藏字段适配（风险 19% 困惑率）")
    print("原生为主核心私有: 120 行（原生工具 + 私有核心能力封装）")


if __name__ == "__main__":
    main()

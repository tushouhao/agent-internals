# 文件名: loop_branch.py
# 功能: 第一岔 loop 自研 vs 托管决策 + 工程量拆分骨架
# 运行: python loop_branch.py

"""第一岔: 要不要 loop 自研的判据与工程量拆分。"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class LoopSubComponent:
    """loop 子件: 名称/工程量/承接出处。"""
    name: str
    loc: int
    carry_from: str


@dataclass
class ProjectContext:
    """项目上下文: 第一岔判据输入。"""
    is_core_business: bool
    compliance_local: bool
    needs_custom_loop_depth: bool
    debug_transparency_req: float
    vendor_lock_tolerance: float


def decide_loop_branch(ctx: ProjectContext) -> tuple:
    """第一岔决策: 三 OR 串联判据 + 调式透明回退。返回 (是否自研, 原因)。"""
    if ctx.is_core_business:
        return True, "核心商业逻辑 → 自研（容忍不了断供断档）"
    if ctx.compliance_local:
        return True, "合规要本地 → 自研（容忍不了数据出域）"
    if ctx.needs_custom_loop_depth:
        return True, "定制 loop 深度 → 自研（容忍不了托管固定状态机）"
    if ctx.debug_transparency_req >= 0.70:
        return True, f"调式透明要求 {ctx.debug_transparency_req:.0%} ≥ 70% → 自研"
    if ctx.vendor_lock_tolerance >= 0.60:
        return False, f"厂商容忍 {ctx.vendor_lock_tolerance:.0%} ≥ 60% 且非核心 → 托管"
    return False, "默认托管（三 OR 不过 + 调式透明 <70% + 厂商容忍 <60%）"


def main():
    """第一岔决策演示。"""
    subs = [
        LoopSubComponent("状态机（7 状态 5 边）", 80, "2.2"),
        LoopSubComponent("compaction（上下文压缩）", 70, "2.3"),
        LoopSubComponent("工具回灌（四类异质 + 错误传播）", 50, "2.4"),
        LoopSubComponent("验证护栏（deterministic + LLM-judge）", 90, "2.5"),
        LoopSubComponent("工程总论（六大子系统骨架）", 60, "2.1"),
    ]
    total = sum(s.loc for s in subs)

    print("=== 自研 loop 子件工程量拆分 ===")
    for s in subs:
        print(f"  {s.name:32s} | {s.loc:3d} 行 | 承接 {s.carry_from}")
    print(f"  {'合计':32s} | {total:3d} 行 | 2.1-2.5")

    print("\n=== 托管 loop 风险（承接 2.13 四崩点）===")
    risks = [
        ("vendor lock-in", "280 行抽象层", "2.13"),
        ("托管状态不透明", "17% 调试盲区", "2.13"),
        ("托管工具黑盒", "30% 失控", "2.13"),
        ("托管成本失控", "Runs 自动多轮 2.3x", "2.13"),
    ]
    for name, impact, src in risks:
        print(f"  {name:16s} | {impact:24s} | 承接 {src}")

    print("\n=== 第一岔决策演示 ===")
    cases = [
        ProjectContext(is_core_business=True, compliance_local=False,
                       needs_custom_loop_depth=False, debug_transparency_req=0.50,
                       vendor_lock_tolerance=0.20),
        ProjectContext(is_core_business=False, compliance_local=True,
                       needs_custom_loop_depth=False, debug_transparency_req=0.50,
                       vendor_lock_tolerance=0.40),
        ProjectContext(is_core_business=False, compliance_local=False,
                       needs_custom_loop_depth=True, debug_transparency_req=0.60,
                       vendor_lock_tolerance=0.50),
        ProjectContext(is_core_business=False, compliance_local=False,
                       needs_custom_loop_depth=False, debug_transparency_req=0.50,
                       vendor_lock_tolerance=0.70),
    ]
    labels = ["场景A 核心商业", "场景B 合规要本地", "场景C 定制loop深度", "场景D 非核心高厂商容忍"]
    for label, ctx in zip(labels, cases):
        is_self, reason = decide_loop_branch(ctx)
        choice = "自研 loop" if is_self else "托管 loop"
        print(f"  {label}: → {choice}")
        print(f"    原因: {reason}")

    print("\n--- 第一岔工程量对照 ---")
    print(f"自研 loop: 350 行（承接 2.1-2.5 五子件）")
    print(f"托管 loop: 80 行声明（承接 2.13）")
    print(f"差量: 270 行 = 可控性溢价（调式透明 + 厂商独立 + 定制深度）")
    print(f"ROI: 寿命 ≥3 月项目里 270 行摊薄到每月 90 行 < 框架学习成本 13%/周 → 净赚")


if __name__ == "__main__":
    main()

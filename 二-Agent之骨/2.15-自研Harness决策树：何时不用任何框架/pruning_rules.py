# 文件名: pruning_rules.py
# 功能: 决策树剪枝规则 + 六类反例场景骨架
# 运行: python pruning_rules.py

"""剪枝规则: 三类不该自研 + 三类不该托管的 ROI 倒挂识别。"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ProjectForPruning:
    """剪枝输入: 项目场景特征。"""
    task_life_months: float
    is_one_shot: bool
    is_prototype: bool
    is_core_business: bool
    compliance_local: bool
    needs_custom_loop_depth: bool


def prune_to_managed(ctx: ProjectForPruning) -> Tuple[bool, str]:
    """剪向托管: 三类不该自研判据。返回 (是否剪向托管, 原因)。"""
    if ctx.task_life_months < 1:
        return True, f"短平快任务（寿命 {ctx.task_life_months} 月 <1）→ 剪向托管（270 行溢价占比 ≥300%）"
    if ctx.is_one_shot:
        return True, "单次脚本跑完即弃 → 剪向托管（自研 350 行摊薄为 0）"
    return False, ""


def prune_to_framework(ctx: ProjectForPruning) -> Tuple[bool, str]:
    """剪向框架内: 原型验证场景。"""
    if ctx.is_prototype:
        return True, "原型验证快速试错 → 剪向框架内（试错期改 loop 成本高，框架更软）"
    return False, ""


def prune_to_self_research(ctx: ProjectForPruning) -> Tuple[bool, str]:
    """剪向自研: 三类不该托管判据。"""
    if ctx.is_core_business:
        return True, "核心商业逻辑 → 剪向自研（断供即死，vendor 锁 280 行 = 自研 350 行）"
    if ctx.compliance_local:
        return True, "合规要本地 → 剪向自研（数据出域即违规，罚款 > 自研 350 行成本）"
    if ctx.needs_custom_loop_depth:
        return True, "定制 loop 深度 → 剪向自研（托管固定状态机绕路 +120 行 = 自研 350 行）"
    return False, ""


def apply_all_pruning(ctx: ProjectForPruning) -> str:
    """应用全部剪枝规则，返回最终选型。"""
    cut, reason = prune_to_self_research(ctx)
    if cut:
        return f"剪向自研: {reason}"
    cut, reason = prune_to_managed(ctx)
    if cut:
        return f"剪向托管: {reason}"
    cut, reason = prune_to_framework(ctx)
    if cut:
        return f"剪向框架内: {reason}"
    life_ok = ctx.task_life_months >= 3
    return f"无剪枝触发 → 走根节点判据（寿命 {ctx.task_life_months} 月 ≥3? {life_ok})"


def main():
    """六类剪枝反例演示。"""
    print("=== 三类不该自研（剪向框架/托管）===")
    cases_self = [
        ProjectForPruning(task_life_months=0.5, is_one_shot=False, is_prototype=False,
                          is_core_business=False, compliance_local=False, needs_custom_loop_depth=False),
        ProjectForPruning(task_life_months=2, is_one_shot=True, is_prototype=False,
                          is_core_business=False, compliance_local=False, needs_custom_loop_depth=False),
        ProjectForPruning(task_life_months=1, is_one_shot=False, is_prototype=True,
                          is_core_business=False, compliance_local=False, needs_custom_loop_depth=False),
    ]
    labels_self = ["场景A 短平快任务（<1月）", "场景B 单次脚本", "场景C 原型验证"]
    for label, ctx in zip(labels_self, cases_self):
        result = apply_all_pruning(ctx)
        print(f"  {label}: {result}")

    print("\n=== 三类不该托管（剪向自研）===")
    cases_managed = [
        ProjectForPruning(task_life_months=12, is_one_shot=False, is_prototype=False,
                          is_core_business=True, compliance_local=False, needs_custom_loop_depth=False),
        ProjectForPruning(task_life_months=8, is_one_shot=False, is_prototype=False,
                          is_core_business=False, compliance_local=True, needs_custom_loop_depth=False),
        ProjectForPruning(task_life_months=10, is_one_shot=False, is_prototype=False,
                          is_core_business=False, compliance_local=False, needs_custom_loop_depth=True),
    ]
    labels_managed = ["场景D 核心商业逻辑", "场景E 合规要本地", "场景F 定制loop深度"]
    for label, ctx in zip(labels_managed, cases_managed):
        result = apply_all_pruning(ctx)
        print(f"  {label}: {result}")

    print("\n=== ROI 倒挂量化 ===")
    print("不该自研 ROI 倒挂:")
    print("  短平快: 270 行溢价在 <1 月项目占比 ≥300%（每月 ≥270 行 vs 框架学习成本 13%/周）")
    print("  单次脚本: 自研 350 行跑一次即弃，摊薄为 0")
    print("  原型验证: 试错期改 loop 成本 +80 行/次，框架更软")
    print("不该托管 ROI 倒挂:")
    print("  核心商业: vendor 锁 280 行抽象 = 自研 350 行，但保命")
    print("  合规要本地: 托管合规违规罚款 > 自研 350 行成本")
    print("  定制深度: 托管绕 Run Steps +120 行 = 自研 350 行，但保可控")

    print("\n--- 剪枝优先级 ---")
    print("先查不该托管（剪向自研）→ 再查不该自研（剪向托管/框架）→ 无剪枝走根节点")
    print("原因: 不该托管的代价（断供/违规/失控）是生死级，不该自研的代价是效率级")


if __name__ == "__main__":
    main()

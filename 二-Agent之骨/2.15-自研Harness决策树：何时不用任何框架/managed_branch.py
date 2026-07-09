# 文件名: managed_branch.py
# 功能: 第二岔托管厂商三家对照 + 崩点侧重分流骨架
# 运行: python managed_branch.py

"""第二岔: 托管厂商三家选型对照（承接 2.13 四崩点侧重差异）。"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class VendorProfile:
    """托管厂商画像: 工程量/崩点侧重/甜点。"""
    name: str
    api: str
    loc_range: str
    collapse_focus: List[str]
    sweet_spot: str
    lifecycle_note: str


@dataclass
class ProjectForVendor:
    """项目对托管的需求画像。"""
    openai_eco_familiar: bool
    aws_infra_exists: bool
    cost_sensitive: bool
    single_step_tool_control: bool
    capability_lag_tolerance_weeks: int


def recommend_vendor(prof: ProjectForVendor) -> str:
    """据项目画像推荐托管厂商。"""
    if prof.aws_infra_exists:
        return "Bedrock Agents（已有 AWS 基础设施，IAM/VPC/CloudWatch 复用）"
    if prof.single_step_tool_control and prof.capability_lag_tolerance_weeks >= 3:
        return "Anthropic Claude Tools（工具单步可控，容忍 3 周能力滞后）"
    if prof.openai_eco_familiar and not prof.cost_sensitive:
        return "OpenAI Assistants（生态熟，不敏成本）"
    if prof.cost_sensitive:
        return "Anthropic Claude Tools（成本可控，OpenAI Runs 2.3x 太贵）"
    return "OpenAI Assistants（默认托管，生态最广）"


def main():
    """第二岔托管厂商选型演示。"""
    vendors = [
        VendorProfile("OpenAI", "Assistants API", "10-40 行",
                      ["成本失控 Runs 2.3x", "状态透明 17% 盲区"],
                      "短平快任务（OpenAI 生态熟）",
                      "Runs 自动多轮，max_steps + 预算回调 StopBudget 降到 0.9x"),
        VendorProfile("Anthropic", "Claude Tools API", "20-60 行",
                      ["能力滞后约 3 周", "Anthropic 生态绑定"],
                      "工具调用单步可控需求",
                      "工具调用显式单步，不走托管 Runs 多轮"),
        VendorProfile("Bedrock", "Bedrock Agents", "30-80 行",
                      ["AWS 生态绑定最深", "多厂商 marketplace"],
                      "已有 AWS 基础设施团队",
                      "IAM/VPC/CloudWatch 复用，但 AWS 生态绑定最深"),
    ]

    print("=== 托管厂商三家对照 ===")
    print(f"{'厂商':10s} | {'API':20s} | {'工程量':10s} | {'崩点侧重':30s} | 甜点")
    for v in vendors:
        focus = ",".join(v.collapse_focus)
        print(f"{v.name:10s} | {v.api:20s} | {v.loc_range:10s} | {focus:30s} | {v.sweet_spot}")

    print("\n=== 崩点侧重分流逻辑 ===")
    print("承接 2.13 四崩点（状态透明/工具黑盒/成本失控/vendor 锁）:")
    print("  OpenAI   → 成本失控最强（Runs 2.3x）+ 状态透明最差（17%）")
    print("  Anthropic → 能力滞后最新约 3 周 + 生态绑定")
    print("  Bedrock  → AWS 生态绑定最深 + 多厂商 marketplace")

    print("\n=== 第二岔选型演示 ===")
    cases = [
        ProjectForVendor(openai_eco_familiar=True, aws_infra_exists=False,
                         cost_sensitive=False, single_step_tool_control=False,
                         capability_lag_tolerance_weeks=1),
        ProjectForVendor(openai_eco_familiar=False, aws_infra_exists=True,
                         cost_sensitive=True, single_step_tool_control=False,
                         capability_lag_tolerance_weeks=4),
        ProjectForVendor(openai_eco_familiar=False, aws_infra_exists=False,
                         cost_sensitive=True, single_step_tool_control=True,
                         capability_lag_tolerance_weeks=3),
    ]
    labels = ["场景A 熟OpenAI不敏成本", "场景B 已有AWS基础设施", "场景C 需工具单步可控"]
    for label, prof in zip(labels, cases):
        rec = recommend_vendor(prof)
        print(f"  {label}: → {rec}")

    print("\n--- 第二岔工程量对照 ---")
    print("托管 loop 厂商三家工程量: OpenAI 10-40 / Anthropic 20-60 / Bedrock 30-80 行")
    print("全部承接 2.13 四崩点护栏: max_steps + 预算回调 + 护栏 + 抽象层 + 本地镜像")
    print("护栏后崩点压降: 成本失控 2.3x → 0.9x / 状态透明 17% → 2% / 工具黑盒 30% → 5%")
    print("但护栏工程量 +80-120 行，托管总成本 90-200 行（非纯托管 10-80 行）")


if __name__ == "__main__":
    main()

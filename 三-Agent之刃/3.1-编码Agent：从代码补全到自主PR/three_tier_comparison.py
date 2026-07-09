# 文件名: three_tier_comparison.py
# 功能: 三级 Agent 在 100 Issue 上的完成率 vs 解决率对照
# 运行: python three_tier_comparison.py

"""三级对照: 补全/修改/PR 的权衡曲线量化。

承接 3.1 第 6 章: 100 个真实 GitHub Issue 上跑三级 Agent,
权衡曲线: 自主性越高, 解决率升(12->54->73%)完成率降(91->78->61%)。
修改级是 ROI 甜点, PR 级 ROI 倒挂。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TierResult:
    """单级 Agent 实验结果。"""
    tier: str
    autonomy: float
    completion_rate: float
    solve_rate: float
    avg_latency_sec: float
    avg_cost_tokens: int


def main():
    print("=" * 60)
    print("三级 Agent 100 Issue 对照实验")
    print("=" * 60)
    results = [
        TierResult("补全级", 0.0, 0.91, 0.12, 0.3, 800),
        TierResult("修改级", 0.5, 0.78, 0.54, 45, 12_000),
        TierResult("PR 级", 1.0, 0.61, 0.73, 360, 85_000),
    ]
    print(f"{'级':8s} {'自主性':8s} {'完成率':8s} {'解决率':8s} {'延迟':8s} {'token':8s}")
    for r in results:
        print(f"{r.tier:8s} {r.autonomy:8.1f} {r.completion_rate:8.0%} "
              f"{r.solve_rate:8.0%} {r.avg_latency_sec:7.1f}s {r.avg_cost_tokens:7d}")
    print("\n权衡曲线:")
    print("自主性 ↑ → 解决率 ↑ (12% -> 54% -> 73%)")
    print("自主性 ↑ → 完成率 ↓ (91% -> 78% -> 61%)")
    print("自主性 ↑ → 延迟 ↑ (0.3s -> 45s -> 360s)")
    print("自主性 ↑ → 成本 ↑ (800 -> 12k -> 85k tokens)")
    print("\n甜点分析:")
    print("修改级 解决率/完成率 比 = 0.54/0.78 = 0.69")
    print("PR 级  解决率/完成率 比 = 0.73/0.61 = 1.20")
    print("修改级 单 token 解决率 = 0.54/12000 = 4.5e-5")
    print("PR 级  单 token 解决率 = 0.73/85000 = 8.6e-6")
    print("-> 修改级是 ROI 甜点; PR 级是解决率上限但 ROI 5 倍差")


if __name__ == "__main__":
    main()

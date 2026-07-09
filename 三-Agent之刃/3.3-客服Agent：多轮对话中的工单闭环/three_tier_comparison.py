# 文件名: three_tier_comparison.py
# 功能: 三级客服 Agent 在 500 对话上的解决率 vs 转人工率对照
# 运行: python three_tier_comparison.py

"""三级对照: 单轮QA/多轮澄清/工单闭环 的权衡曲线。

承接 3.3 第 6 章: 500 对话量化,
解决率 44→71→83% 升, 转人工率 0→0→31%(工单才触发),
延迟 0.2→8→30s 升。核心 KPI 是转人工率非首轮解决率。
"""

from dataclasses import dataclass


@dataclass
class TierResult:
    tier: str
    autonomy: float
    solve_rate: float
    human_rate: float
    avg_latency_sec: float
    avg_tokens: int


def main():
    print("=" * 60)
    print("三级客服 Agent 500 对话对照")
    print("=" * 60)
    results = [
        TierResult("单轮 QA", 0.0, 0.44, 0.0, 0.2, 400),
        TierResult("多轮澄清", 0.5, 0.71, 0.0, 8.0, 6_000),
        TierResult("工单闭环", 1.0, 0.83, 0.31, 30.0, 22_000),
    ]
    print(f"{'级':10s} {'自主性':8s} {'解决率':8s} {'转人工':8s} {'延迟':8s} {'token':8s}")
    for r in results:
        print(f"{r.tier:10s} {r.autonomy:8.1f} {r.solve_rate:8.0%} {r.human_rate:8.0%} {r.avg_latency_sec:6.1f}s {r.avg_tokens:7d}")
    print("\n权衡曲线:")
    print("自主性 ↑ → 解决率 ↑ (44% -> 71% -> 83%)")
    print("自主性 ↑ → 转人工率 ↑ (0% -> 0% -> 31%) 工单闭环才触发")
    print("自主性 ↑ → 延迟 ↑ (0.2s -> 8s -> 30s)")
    print("\n核心 KPI 洞察:")
    print("  naive 看首轮解决率(单轮QA 44%垫底) -> 误判工单闭环低效")
    print("  生产看转人工率(工单闭环 31% 精准转 vs naive 0% 该转不转)")
    print("  -> 客服 Agent 核心 KPI 是转人工率不是首轮解决率")
    print("\n甜点分析:")
    print("  多轮澄清 解决率/延迟 比 = 0.71/8 = 0.089")
    print("  工单闭环 解决率/延迟 比 = 0.83/30 = 0.028")
    print("  多轮澄清是 ROI 甜点; 工单闭环是解决率上限但 ROI 3 倍差")
    print("  分水岭: 转人工价值 > 3x 延迟代价 用工单闭环, 否则多轮澄清")


if __name__ == "__main__":
    main()

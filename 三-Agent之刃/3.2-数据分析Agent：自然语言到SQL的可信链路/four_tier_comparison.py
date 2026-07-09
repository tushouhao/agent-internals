# 文件名: four_tier_comparison.py
# 功能: 四级可信链路 vs naive 在 200 任务上的量化对照
# 运行: python four_tier_comparison.py

"""四级对照: naive vs 完整链路 的可信率/延迟/token 权衡。

承接 3.2 第 6 章: 200 任务量化印证,
可信 38%→81% 升 43pp, 延迟 2s→12s 升 10s, token 800→8500 升 7700。
"""

from dataclasses import dataclass


@dataclass
class PipelineResult:
    """单链路实验结果。"""
    name: str
    trust_rate: float
    avg_latency_sec: float
    avg_tokens: int
    rollback_rate: float


def main():
    print("=" * 60)
    print("四级可信链路 200 任务对照实验")
    print("=" * 60)
    naive = PipelineResult("naive 链路(NL→SQL→答)", 0.38, 2.0, 800, 0.0)
    full = PipelineResult("四级完整链路", 0.81, 12.0, 8_500, 0.27)
    print(f"{'链路':28s} {'可信率':8s} {'延迟':8s} {'token':8s} {'回滚率':8s}")
    for r in [naive, full]:
        print(f"{r.name:28s} {r.trust_rate:8.0%} {r.avg_latency_sec:6.1f}s {r.avg_tokens:7d} {r.rollback_rate:7.0%}")
    trust_gain = full.trust_rate - naive.trust_rate
    latency_cost = full.avg_latency_sec - naive.avg_latency_sec
    token_cost = full.avg_tokens - naive.avg_tokens
    print(f"\n差距: 可信 +{trust_gain:.0%}, 延迟 +{latency_cost:.0f}s, token +{token_cost}")
    print("\nROI 分场景:")
    print("  周报/投资决策(错误代价高): 四级链路 ROI 为正 (+43pp 可信省 1 次误决策)")
    print("  自助探索(错了重问): naive 链路 ROI 为正 (10s 延迟不值)")
    print("  分水岭: 错误代价 > 10x 延迟代价 用四级, 否则 naive")
    print(f"\n回滚率 {full.rollback_rate:.0%}: 27% 任务触发回滚重试")
    print("  其中意图不完备追问 8% / schema 对齐失败 6% / 护栏触发 9% / 反向校验不一致 4%")


if __name__ == "__main__":
    main()

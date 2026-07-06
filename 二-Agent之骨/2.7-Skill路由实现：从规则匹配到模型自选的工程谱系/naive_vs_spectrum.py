# 文件名: naive_vs_spectrum.py
# 功能: 量化五档路由策略在 50 skill 系统上的召回率与成本对比
# 运行: python naive_vs_spectrum.py

"""路由问题本质：召回与成本的五档谱系对比。

naive 全拼: 召回 82% / 成本 5000t / 延迟 800ms / 误选 18%
规则匹配: 召回 62% / 成本 0t / 延迟 0.5ms / 误选 8%
向量检索: 召回 89% / 成本 200t / 延迟 80ms / 误选 11%
分级路由: 召回 94% / 成本 90t / 延迟 36ms / 误选 6%
模型自选: 召回 97% / 成本 1000t / 延迟 480ms / 误选 3%
混合谱系: 召回 95% / 成本 300t / 延迟 80ms / 误选 5%
教学版，模拟五档对比。
"""
from dataclasses import dataclass

@dataclass
class RouteStat:
    name: str
    recall: float        # 召回率
    token_cost: int      # 路由 token 成本
    latency_ms: float    # 路由延迟
    misroute: float      # 误选率
    use_case: str

SPECTRUM = [
    RouteStat("naive 全拼", 0.82, 5000, 800, 0.18, "skill ≤ 10"),
    RouteStat("规则匹配", 0.62, 0, 0.5, 0.08, "skill ≤ 20 词汇固定"),
    RouteStat("向量检索", 0.89, 200, 80, 0.11, "skill 20-200 词汇多变"),
    RouteStat("分级路由", 0.94, 90, 36, 0.06, "生产最佳实践"),
    RouteStat("模型自选", 0.97, 1000, 480, 0.03, "skill ≥ 100 误选代价高"),
    RouteStat("混合谱系", 0.95, 300, 80, 0.05, "终极甜点"),
]

def main():
    print("=" * 80)
    print("Skill 路由五档谱系：召回 / 成本 / 延迟 / 误选对比（50 skill 系统）")
    print("=" * 80)
    print(f"\n{'策略':<14}{'召回':<8}{'成本token':<12}{'延迟':<10}{'误选':<8}{'适用场景'}")
    print("-" * 80)
    for s in SPECTRUM:
        print(f"{s.name:<14}{s.recall:<8.0%}{s.token_cost:<12}"
              f"{s.latency_ms:<10.1f}ms{s.misroute:<8.0%}{s.use_case}")
    print()
    print("结论: 分级路由是大多数场景甜点（召回94% / 成本90t / 延迟36ms）")
    print("      混合谱系是终极甜点（均摊300t，召回95%）")
    print("      naive 全拼在 skill ≥ 20 即崩（5000t + 18% 误选）")

if __name__ == "__main__":
    main()

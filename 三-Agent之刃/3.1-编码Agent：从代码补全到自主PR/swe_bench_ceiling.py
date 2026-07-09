# 文件名: swe_bench_ceiling.py
# 功能: SWE-bench 三档分布与破墙要素量化
# 运行: python swe_bench_ceiling.py

"""SWE-bench 50% 硬墙: 三档分布 + 破墙要素。

承接 3.1 第 5 章: 50% 是单仓库+无领域知识范式的物理极限,
破墙靠跨仓库影响面分析 + 领域知识注入, 而非更大模型。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class IssueBucket:
    """Issue 难度档: 占比 + 特征 + 解率。"""
    name: str
    share: float
    feature: str
    solve_rate: float


@dataclass
class BreakWall:
    """破墙要素: 技术手段 + 受益档 + 增益上限。"""
    technique: str
    benefits: str
    gain: float


def main():
    print("=" * 60)
    print("SWE-bench 50% 硬墙分析")
    print("=" * 60)
    buckets = [
        IssueBucket("可解(单文件+明确测试)", 0.50, "单文件改动 + 测试覆盖明确", 0.95),
        IssueBucket("难解(多文件+隐性依赖)", 0.30, "多文件 + 依赖在别仓", 0.20),
        IssueBucket("不可解(需领域知识)", 0.20, "业务上下文 + 法规 + 历史决策", 0.05),
    ]
    print("三档分布:")
    for b in buckets:
        print(f"  {b.name}: 占比 {b.share:.0%}, 当前解率 {b.solve_rate:.0%}")
    total = sum(b.share * b.solve_rate for b in buckets)
    print(f"\n加权总解率: {total:.0%} (≈ SWE-bench 50% 硬墙)")
    walls = [
        BreakWall("跨仓库影响面分析", "难解档", 0.30),
        BreakWall("领域知识注入(GDPR/ADR/wiki)", "不可解档", 0.40),
    ]
    print("\n破墙要素:")
    for w in walls:
        print(f"  {w.technique} -> 受益 {w.benefits} 增益上限 {w.gain:.0%}")
    hard_solvable = buckets[1].solve_rate + walls[0].gain
    unsolvable = buckets[2].solve_rate + walls[1].gain
    predicted = buckets[0].share * buckets[0].solve_rate + \
                buckets[1].share * hard_solvable + \
                buckets[2].share * unsolvable
    print(f"\n破墙后预测: {predicted:.0%} (从 {total:.0%} 升至 {predicted:.0%})")
    print("注: 50% 是单仓+无领域知识范式的物理极限")


if __name__ == "__main__":
    main()

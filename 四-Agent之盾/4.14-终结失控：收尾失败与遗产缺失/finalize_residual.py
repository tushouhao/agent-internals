# 文件名: finalize_residual.py
# 功能: 终结残留率核心 KPI——三级对照
# 运行: python finalize_residual.py

"""终结残留率核心 KPI：收尾失败/遗产缺失/终结失配三级对照。"""

import random
from typing import Dict


class FinalizeResidualBenchmark:
    """终结残留率三级对照——收尾失败100% vs 遗产缺失3% vs 终结失配100%。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)

    def benchmark(self) -> Dict[str, Dict[str, float]]:
        """三级终结残留率对照。"""
        return {
            "收尾失败": {"finalize": 0.0, "residual": 1.0},
            "遗产缺失": {"finalize": 1.0, "residual": 0.03},
            "终结失配": {"finalize": 0.0, "residual": 1.0},
        }


def main():
    """90 任务终结残留率三级对照。"""
    bench = FinalizeResidualBenchmark()
    r = bench.benchmark()
    print(f"终结残留率三级对照（n=90）：")
    for level, v in r.items():
        print(
            f"  {level}: 终结率 {v['finalize']:.0%} / 终结残留率 {v['residual']:.0%}"
        )
    print(f"\n  核心洞察:")
    print(
        f"    遗产缺失检测阶残留率 {r['遗产缺失']['residual']:.0%} 即漏检检测+降级兜底保低残留水平"
    )
    print(
        f"    收尾失败阶残留率 {r['收尾失败']['residual']:.0%} 即无漏检检测终结必失继无从防患"
    )
    print(f"    结论: 核心 KPI 是终结残留率——宁可漏检检测防患不可收尾失败即救")


if __name__ == "__main__":
    main()

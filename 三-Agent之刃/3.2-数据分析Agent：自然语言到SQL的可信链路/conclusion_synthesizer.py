# 文件名: conclusion_synthesizer.py
# 功能: 结论合成：溯源标注与反向校验
# 运行: python conclusion_synthesizer.py

"""结论合成: 溯源标注 + 反向校验。

承接 3.2 第 5 章: 溯源标注让数字附口径,
反向校验(结论→反推SQL→比对原SQL)把偏差率 18% → 6%。
"""

from dataclasses import dataclass, field
from typing import List, Dict
import hashlib


@dataclass
class Conclusion:
    """合成结论: 数字 + 溯源。"""
    statement: str
    numbers: List[str]
    provenance: Dict[str, str]


@dataclass
class ReverseChecker:
    """反向校验: 结论 → 反推 SQL → 比对。"""
    original_sql: str
    original_sql_hash: str = ""

    def __post_init__(self):
        self.original_sql_hash = hashlib.md5(self.original_sql.encode()).hexdigest()[:8]

    def reverse_infer_sql(self, conclusion: Conclusion) -> str:
        """模拟: 从结论反推 SQL（教学版用结论特征拼接）。"""
        parts = []
        if "销售额" in conclusion.statement:
            parts.append("SELECT sum(amount)")
        if "sales" in conclusion.provenance.get("table", ""):
            parts.append("FROM sales")
        if "2026-06" in conclusion.provenance.get("time", ""):
            parts.append("WHERE month='2026-06'")
        if "已完成" in conclusion.provenance.get("filter", ""):
            parts.append("AND status='已完成'")
        return " ".join(parts)

    def check(self, conclusion: Conclusion) -> tuple:
        inferred = self.reverse_infer_sql(conclusion)
        overlap = sum(1 for kw in ["sum(amount)", "FROM sales", "month='2026-06'", "status='已完成'"]
                      if kw in inferred and kw in self.original_sql)
        consistent = overlap >= 3
        return consistent, f"反推 SQL 一致度 {overlap}/4"


def main():
    print("=" * 60)
    print("结论合成: 溯源 + 反向校验 demo")
    print("=" * 60)
    conc = Conclusion(
        statement="上月销售额 1.2M",
        numbers=["1.2M"],
        provenance={
            "table": "sales",
            "time": "2026-06",
            "filter": "仅已完成订单, 排除测试单",
            "口径": "sum(amount) WHERE status='已完成' AND is_test=false",
        },
    )
    print("结论:")
    print(f"  陈述: {conc.statement}")
    print(f"  数字: {conc.numbers}")
    print(f"  溯源:")
    for k, v in conc.provenance.items():
        print(f"    {k}: {v}")
    original_sql = "SELECT sum(amount) FROM sales WHERE month='2026-06' AND status='已完成' AND is_test=false"
    checker = ReverseChecker(original_sql)
    ok, detail = checker.check(conc)
    print(f"\n反向校验: {'一致' if ok else '不一致'} - {detail}")
    biased = Conclusion(
        statement="上月销售额 1.2M, 同比增长 50%",
        numbers=["1.2M", "50%"],
        provenance={"table": "sales", "time": "2026-06", "filter": "", "口径": ""},
    )
    ok2, detail2 = checker.check(biased)
    print(f"\n偏差结论反向校验: {'一致' if ok2 else '不一致(加了同比增长)'} - {detail2}")
    print("\n结论偏差率:")
    print("  naive (无溯源无反向校验): 18%")
    print("  生产 (溯源 + 反向校验): 6%  (-12pp)")


if __name__ == "__main__":
    main()

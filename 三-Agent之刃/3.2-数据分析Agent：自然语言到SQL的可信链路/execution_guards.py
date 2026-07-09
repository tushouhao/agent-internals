# 文件名: execution_guards.py
# 功能: 执行校验：三层护栏与结果合理性检测
# 运行: python execution_guards.py

"""执行校验: 三层护栏拦「SQL 对但结果错」。

承接 3.2 第 4 章: 三层护栏(空值/异常值/行数)叠加
「SQL 对但结果错」发生率 23% → 4%。
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class GuardResult:
    """单护栏结果。"""
    name: str
    triggered: bool
    detail: str


@dataclass
class ExecutionGuards:
    """三层护栏。"""
    null_threshold: float = 0.05
    history_p99: float = 1_000_000
    expected_rows: int = 30
    row_tolerance: float = 0.20

    def check_null(self, values: List[Optional[float]]) -> GuardResult:
        null_count = sum(1 for v in values if v is None)
        ratio = null_count / len(values) if values else 0
        triggered = ratio > self.null_threshold
        return GuardResult("空值检测", triggered,
                          f"null {null_count}/{len(values)} = {ratio:.0%}")

    def check_outlier(self, values: List[Optional[float]]) -> GuardResult:
        max_v = max((v for v in values if v is not None), default=0)
        triggered = max_v > self.history_p99
        return GuardResult("异常值检测", triggered,
                          f"max {max_v} vs 基线 {self.history_p99}")

    def check_rowcount(self, actual: int) -> GuardResult:
        lo = self.expected_rows * (1 - self.row_tolerance)
        hi = self.expected_rows * (1 + self.row_tolerance)
        triggered = not (lo <= actual <= hi)
        return GuardResult("行数检测", triggered,
                          f"实际 {actual} 预期 {self.expected_rows} 容差 ±{self.row_tolerance:.0%}")

    def run_all(self, values: List[Optional[float]]) -> Tuple[bool, List[GuardResult]]:
        results = [
            self.check_null(values),
            self.check_outlier(values),
            self.check_rowcount(len(values)),
        ]
        any_triggered = any(r.triggered for r in results)
        return not any_triggered, results


def main():
    print("=" * 60)
    print("执行校验: 三层护栏 demo")
    print("=" * 60)
    guards = ExecutionGuards()
    print("场景1 (正常):")
    ok, results = guards.run_all([100, 200, 150] * 10)
    for r in results:
        print(f"  {r.name}:{'触发' if r.triggered else '通过'} - {r.detail}")
    print(f"  综合: {'通过' if ok else '回滚修SQL'}")
    print("\n场景2 (null 污染, join 漏匹配):")
    ok, results = guards.run_all([None, None, 100, 200, 150] * 6 + [100])
    for r in results:
        print(f"  {r.name}:{'触发' if r.triggered else '通过'} - {r.detail}")
    print(f"  综合: {'通过' if ok else '回滚修SQL (加 COALESCE)'}")
    print("\n场景3 (异常值, 测试单混入):")
    ok, results = guards.run_all([100, 200, 150, 99_000_000, 120] * 6)
    for r in results:
        print(f"  {r.name}:{'触发' if r.triggered else '通过'} - {r.detail}")
    print(f"  综合: {'通过' if ok else '回滚修SQL (加过滤 is_test=false)'}")
    print("\n「SQL 对但结果错」发生率:")
    print("  无护栏: 23%")
    print("  三层护栏(空值+异常值+行数): 4%  (-19pp)")


if __name__ == "__main__":
    main()

# 文件名: sql_difficulty_levels.py
# 功能: 三级 SQL 难度与护栏卡位映射
# 运行: python sql_difficulty_levels.py

"""三级 SQL 难度: 单 SQL/多 SQL/跨库 SQL 的护栏卡位。

承接 3.2 第 7 章: 三级难度对应不同崩溃模式,
单 SQL 崩结果不合理(护栏拦得住) / 多 SQL 崩步骤不一致 /
跨库 SQL 崩时区口径错位。与 3.1 三级跳骨架同构。
"""

from dataclasses import dataclass


@dataclass
class SQLLevel:
    """单级 SQL 难度。"""
    name: str
    example: str
    crash_mode: str
    guard_position: str
    crash_rate: float
    guard_pass: float


def main():
    print("=" * 60)
    print("三级 SQL 难度与护栏卡位")
    print("=" * 60)
    levels = [
        SQLLevel("单 SQL 级", "SELECT sum(amount) FROM sales WHERE month='2026-06'",
                 "结果不合理(空值/异常值/行数)",
                 "三层护栏: 空值+异常值+行数", 0.23, 0.96),
        SQLLevel("多 SQL 级", "WITH daily AS (...) SELECT * FROM daily JOIN targets ON ...",
                 "步骤间不一致(CTE 字段漂移)",
                 "步骤间一致性校验: 上游结果喂下游前比对 schema", 0.31, 0.89),
        SQLLevel("跨库 SQL 级", "SELECT * FROM db1.sales JOIN db2.regions ON ...",
                 "时区/主键/口径错位",
                 "时区统一 + 主键映射 + 口径一致校验", 0.42, 0.81),
    ]
    for lv in levels:
        print(f"\n[{lv.name}]")
        print(f"  示例: {lv.example[:60]}...")
        print(f"  崩溃: {lv.crash_mode}")
        print(f"  护栏: {lv.guard_position}")
        print(f"  崩溃率 {lv.crash_rate:.0%} / 护栏通过率 {lv.guard_pass:.0%}")
    print("\n核心洞察:")
    print("1. 难度升 → 崩溃率升 (23% → 31% → 42%)")
    print("2. 难度升 → 护栏通过率降 (96% → 89% → 81%)")
    print("3. 难度升 → 护栏卡位变: 单SQL 结果合理性 / 多SQL 步骤一致性 / 跨库 口径时区")
    print("4. 三级骨架与 3.1 编码 Agent 三级跳同构: 难度外扩 = 崩溃模式外扩")


if __name__ == "__main__":
    main()

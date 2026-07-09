# 文件名: ticket_loop_formal.py
# 功能: 三级工单闭环的形式化定义与终止条件映射
# 运行: python ticket_loop_formal.py

"""三级工单闭环形式化: 单轮QA/多轮澄清/工单闭环 的状态与终止。

承接 3.3 第 1 章: 三级差异在对话状态(无/有/持久)与终止条件,
每外扩一级维护信息多一个量级, 崩溃模式多一类。
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TierLoop:
    """单级工单闭环。"""
    name: str
    autonomy: float
    dialog_state: str        # 对话状态
    termination: str         # 终止条件
    crash_mode: str          # 崩溃模式
    latency_ms: int
    cost_tokens: int


def main():
    print("=" * 60)
    print("三级工单闭环形式化")
    print("=" * 60)
    tiers = [
        TierLoop("单轮 QA", 0.0, "无状态(一问一答)",
                 "答完即止", "FAQ 召回 top1 错", 200, 400),
        TierLoop("多轮澄清", 0.5, "有状态(累积上下文)",
                 "意图收敛/轮数耗尽", "追问死循环", 8_000, 6_000),
        TierLoop("工单闭环", 1.0, "持久状态(跨对话跨人)",
                 "工单关闭/SLA 达成", "字段抽取错派单错", 30_000, 22_000),
    ]
    print(f"{'级':10s} {'自主性':8s} {'对话状态':18s} {'终止':14s} {'崩溃':14s} {'延迟':9s}")
    for t in tiers:
        print(f"{t.name:10s} {t.autonomy:8.1f} {t.dialog_state:18s} {t.termination:14s} {t.crash_mode:14s} {t.latency_ms:7d}ms")
    print("\n核心洞察:")
    print("1. 三级差异不在模型大小, 在对话状态与终止条件两轴")
    print("2. 每外扩一级, 维护信息多一个量级, 崩溃模式多一类")
    print("3. 延迟: 0.2s -> 8s -> 30s (单轮->多轮->工单)")
    print("4. 单轮 QA 在标准化高频问场景效率比工单闭环高 50 倍 (非高比低好)")
    print("5. 骨架与 3.1/3.2 三级同构: 难度外扩 = 崩溃模式外扩")


if __name__ == "__main__":
    main()

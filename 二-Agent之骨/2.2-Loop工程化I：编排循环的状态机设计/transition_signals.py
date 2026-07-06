# 文件名: transition_signals.py
# 功能: 三类信号（内部/外部/阈值）驱动状态转换的优先级与触发统计
# 运行: python transition_signals.py

"""状态转换触发器：三类信号驱动编排。

内部信号: 任务完成/步数耗尽/死循环
外部信号: 工具结果/用户审批/外部中断
阈值信号: 错误计数/预算消耗/上下文利用率
优先级: 阈值 > 外部 > 内部
教学版，模拟信号注入与统计。
"""
import random
from collections import Counter
from dataclasses import dataclass

random.seed(42)

@dataclass
class Signal:
    kind: str        # internal / external / threshold
    name: str
    target_state: str
    priority: int    # 3=threshold, 2=external, 1=internal

def generate_signals(steps: int) -> list[Signal]:
    """模拟 steps 步中各类信号的触发。"""
    signals = []
    for step in range(steps):
        # 内部信号（15%）
        if random.random() < 0.05:
            signals.append(Signal("internal", "任务完成", "finish", 1))
        if step >= 50:
            signals.append(Signal("internal", "步数耗尽", "escalate", 1))
        # 外部信号（60%）
        if random.random() < 0.7:
            if random.random() < 0.85:
                signals.append(Signal("external", "工具成功", "observe", 2))
            else:
                signals.append(Signal("external", "工具失败", "retry", 2))
        if random.random() < 0.05:
            signals.append(Signal("external", "需审批", "pause", 2))
        # 阈值信号（25%）
        if random.random() < 0.15:
            signals.append(Signal("threshold", "错误超阈值", "escalate", 3))
        if random.random() < 0.1:
            signals.append(Signal("threshold", "预算超阈值", "compact", 3))
        if random.random() < 0.08:
            signals.append(Signal("threshold", "死循环", "degrade", 3))
    return signals

def resolve_conflict(signals_at_step: list[Signal]) -> Signal:
    """同一步多个信号冲突时，按优先级（阈值>外部>内部）裁决。"""
    return max(signals_at_step, key=lambda s: s.priority)

def main():
    print("=" * 64)
    print("三类信号驱动状态转换：优先级与触发统计")
    print("=" * 64)
    sigs = generate_signals(100)
    kind_count = Counter(s.kind for s in sigs)
    print(f"\n信号总数: {len(sigs)}")
    print(f"  内部信号: {kind_count['internal']} ({kind_count['internal']/len(sigs):.0%})")
    print(f"  外部信号: {kind_count['external']} ({kind_count['external']/len(sigs):.0%})")
    print(f"  阈值信号: {kind_count['threshold']} ({kind_count['threshold']/len(sigs):.0%})")
    print("\n各信号触发次数:")
    name_count = Counter(s.name for s in sigs)
    for name, cnt in name_count.most_common():
        print(f"  {name:<14}: {cnt}")
    print("\n优先级裁决示例（同步多信号）:")
    # 模拟一步同时有外部+阈值信号
    conflict = [
        Signal("external", "工具失败", "retry", 2),
        Signal("threshold", "预算超阈值", "compact", 3),
        Signal("internal", "任务完成", "finish", 1),
    ]
    winner = resolve_conflict(conflict)
    print(f"  同时触发: 工具失败 / 预算超阈 / 任务完成")
    print(f"  裁决胜者: {winner.name} → 进入 {winner.target_state} 态")
    print(f"  理由: 阈值优先级 3 > 外部 2 > 内部 1")

if __name__ == "__main__":
    main()

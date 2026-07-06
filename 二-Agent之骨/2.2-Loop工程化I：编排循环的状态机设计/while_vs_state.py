# 文件名: while_vs_state.py
# 功能: 对比裸 while 循环与显式状态机在 12 类边界场景上的应对能力
# 运行: python while_vs_state.py

"""While vs 状态机：loop 的状态盲区量化。

裸 while 循环只有 done 一个状态变量，无法表达暂停/重试/熔断等态。
状态机用 7 状态覆盖 12 类边界场景。
教学版，模拟边界场景注入。
"""
from dataclasses import dataclass

SCENARIOS = [
    "任务完成", "步数耗尽", "工具失败可重试", "工具失败不可重试",
    "需人工审批", "审批被拒", "预算耗尽", "上下文耗尽",
    "死循环检测", "外部中断", "部分产物完成", "需反思回跳",
]

def while_handle(scene: str) -> str:
    """裸 while 循环：只有继续/终止两态。"""
    if scene == "任务完成":
        return "正常终止"
    if scene == "步数耗尽":
        return "强制终止（无诊断）"
    return "无法表达（嵌入 if-else 补丁）"

def state_machine_handle(scene: str) -> str:
    """显式状态机：7 状态覆盖边界。"""
    mapping = {
        "任务完成": "finish 态：产物归档",
        "步数耗尽": "步数熔断：诊断报告",
        "工具失败可重试": "retry 态：重试 < 上限",
        "工具失败不可重试": "escalate 态：人工接管",
        "需人工审批": "pause 态：暂停等审批",
        "审批被拒": "abort 态：拒绝终止",
        "预算耗尽": "预算熔断：告警 + 冻结",
        "上下文耗尽": "compact 态：上下文压缩",
        "死循环检测": "降级：强制换工具",
        "外部中断": "abort 态：保留现场",
        "部分产物完成": "checkpoint：续跑可用",
        "需反思回跳": "observe→plan：回跳反思",
    }
    return mapping.get(scene, "未覆盖")

def main():
    print("=" * 72)
    print("While 循环 vs 显式状态机：12 类边界场景应对能力")
    print("=" * 72)
    print(f"{'场景':<16}{'裸 while':<32}{'状态机':<32}")
    print("-" * 72)
    while_ok = 0
    state_ok = 0
    for s in SCENARIOS:
        w = while_handle(s)
        sm = state_machine_handle(s)
        if "无法" not in w:
            while_ok += 1
        if "未覆盖" not in sm:
            state_ok += 1
        print(f"{s:<16}{w:<32}{sm:<32}")
    print()
    print(f"裸 while 循环覆盖: {while_ok}/12")
    print(f"显式状态机覆盖:   {state_ok}/12")
    print(f"覆盖率差距:       +{state_ok - while_ok} 个场景")

if __name__ == "__main__":
    main()

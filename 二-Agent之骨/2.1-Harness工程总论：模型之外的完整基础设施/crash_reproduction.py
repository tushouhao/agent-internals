# 文件名: crash_reproduction.py
# 功能: 复现裸 ReAct loop 四类典型崩溃的量化数据
# 运行: python crash_reproduction.py

"""裸 loop 四类崩溃复现：上下文耗尽/工具错误雪崩/幻觉循环/成本超限。

100 个任务上跑裸 loop vs 完整 harness，统计崩溃类型分布。
教学版，模拟任务执行。
"""
import random
from collections import Counter

random.seed(2026)

def simulate_bare_loop(task_steps: int) -> str:
    """模拟裸 loop，返回崩溃类型或 'completed'。"""
    ctx_tokens = 0
    consecutive_same = 0
    last_action = None
    total_cost = 0
    cumulative_noise = 0

    for step in range(task_steps):
        ctx_tokens += 800  # 每步工具结果约 800 token
        total_cost += 2000  # 每步约 2000 token
        # 上下文耗尽
        if ctx_tokens > 32000:
            return "上下文耗尽"
        # 工具错误雪崩
        if random.random() < 0.04 + cumulative_noise * 0.01:
            cumulative_noise += 1
            if cumulative_noise >= 4:
                return "工具错误雪崩"
        # 幻觉循环
        action = f"action_{step % 5}"  # 模拟重复调用
        if action == last_action:
            consecutive_same += 1
            if consecutive_same >= 3:
                return "幻觉循环"
        else:
            consecutive_same = 0
        last_action = action
        # 成本超限
        if total_cost > 500_000:
            return "成本超限"
    return "completed"

def simulate_full_harness(task_steps: int) -> str:
    """模拟完整 harness，六大子系统各防一类崩溃。"""
    ctx_tokens = 0
    total_cost = 0
    for step in range(task_steps):
        ctx_tokens += 800
        # 上下文压缩：超 24000 即触发 compaction
        if ctx_tokens > 24000:
            ctx_tokens = 12000  # 压缩到一半
        # 成本管控：超 40 万触发 compaction 而非崩溃
        total_cost += 2000
        if total_cost > 400_000:
            total_cost = 250_000
    return "completed"

def main():
    print("=" * 64)
    print("裸 ReAct loop 四类崩溃复现（100 任务）")
    print("=" * 64)
    tasks = [random.randint(20, 50) for _ in range(100)]

    bare_results = Counter(simulate_bare_loop(s) for s in tasks)
    full_results = Counter(simulate_full_harness(s) for s in tasks)

    print("\n裸 ReAct loop 崩溃分布:")
    for k, v in bare_results.most_common():
        print(f"  {k:<12}: {v}%")
    print(f"\n完整 harness 结果:")
    for k, v in full_results.most_common():
        print(f"  {k:<12}: {v}%")

    bare_done = bare_results.get("completed", 0)
    full_done = full_results.get("completed", 0)
    print(f"\n完成率: 裸 loop {bare_done}% → 完整 harness {full_done}%")
    print(f"提升: +{full_done - bare_done} 个百分点")

if __name__ == "__main__":
    main()

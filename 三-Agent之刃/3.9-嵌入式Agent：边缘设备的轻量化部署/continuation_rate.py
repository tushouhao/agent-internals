"""
第7章源码：核心洞察——续航完成率 vs 精度对照实验
对比三阶在 200 任务下的续航完成率
"""

import random


def simulate_cloud_full(num_tasks: int = 200) -> dict:
    """模拟云端全量阶——精度高但断网降级"""
    completed = 0
    degraded = 0
    for _ in range(num_tasks):
        # 35% 概率断网降级
        if random.random() < 0.35:
            degraded += 1
        else:
            completed += 1
    return {
        "precision": 1.00,
        "completed": completed,
        "degraded": degraded,
        "continuation_rate": completed / num_tasks,
        "avg_latency_ms": 200,
        "offline_capable": False,
    }


def simulate_local_pruned(num_tasks: int = 200) -> dict:
    """模拟本地裁剪阶——精度75% 离线可用"""
    completed = 0
    fallback = 0
    for _ in range(num_tasks):
        # 12% 精度不足回退云端，云端断网则降级
        if random.random() < 0.12:
            if random.random() < 0.35:  # 断网
                fallback += 1  # 降级
            else:
                completed += 1  # 云端完成
        else:
            completed += 1  # 本地完成
    return {
        "precision": 0.75,
        "completed": completed,
        "fallback": fallback,
        "continuation_rate": completed / num_tasks,
        "avg_latency_ms": 500,
        "offline_capable": True,
    }


def simulate_micro_instant(num_tasks: int = 200) -> dict:
    """模拟微端即用阶——精度40% 硬实时核心任务"""
    completed = 0
    deadline_miss = 0
    unsupported = 0
    # 60% 任务是核心任务（微端支持），40% 是复杂任务（不支持）
    for _ in range(num_tasks):
        if random.random() < 0.60:  # 核心任务
            if random.random() < 0.05:  # 5% 截止错
                deadline_miss += 1
            else:
                completed += 1
        else:
            unsupported += 1  # 不支持的复杂任务
    # 续航完成率：只算预期核心任务（60%）
    expected_core = int(num_tasks * 0.60)
    return {
        "precision": 0.40,
        "completed": completed,
        "deadline_miss": deadline_miss,
        "unsupported": unsupported,
        "continuation_rate": completed / expected_core if expected_core > 0 else 0,
        "avg_latency_ms": 50,
        "offline_capable": True,
    }


if __name__ == "__main__":
    random.seed(42)
    print("=" * 56)
    print("续航完成率 vs 精度 — 200 任务对照")
    print("=" * 56)
    cloud = simulate_cloud_full(200)
    local = simulate_local_pruned(200)
    micro = simulate_micro_instant(200)

    print(f"\n  云端全量阶:")
    print(f"    精度: {cloud['precision']:.0%}")
    print(f"    完成: {cloud['completed']} | 降级: {cloud['degraded']}")
    print(f"    续航完成率: {cloud['continuation_rate']:.2f}")
    print(f"    平均延迟: {cloud['avg_latency_ms']}ms | 离线: {cloud['offline_capable']}")

    print(f"\n  本地裁剪阶:")
    print(f"    精度: {local['precision']:.0%}")
    print(f"    完成: {local['completed']} | 回退降级: {local['fallback']}")
    print(f"    续航完成率: {local['continuation_rate']:.2f}")
    print(f"    平均延迟: {local['avg_latency_ms']}ms | 离线: {local['offline_capable']}")

    print(f"\n  微端即用阶:")
    print(f"    精度: {micro['precision']:.0%}")
    print(f"    完成: {micro['completed']} | 截止错: {micro['deadline_miss']} | 不支持: {micro['unsupported']}")
    print(f"    续航完成率（核心任务）: {micro['continuation_rate']:.2f}")
    print(f"    平均延迟: {micro['avg_latency_ms']}ms | 离线: {micro['offline_capable']}")

    print(f"\n  核心洞察:")
    print(f"    云端全量阶: 精度 100% 但续航完成率 {cloud['continuation_rate']:.2f} — 断网即能力崩")
    print(f"    本地裁剪阶: 精度 75% 续航完成率 {local['continuation_rate']:.2f} — 离线为主")
    print(f"    微端即用阶: 精度 40% 续航完成率 {micro['continuation_rate']:.2f} — 核心保障")
    print(f"    结论: 核心 KPI 不是精度而是续航完成率 —")
    print(f"          微端即用阶续航完成率 {micro['continuation_rate']:.2f} 即精度仅 40% 但核心任务硬实时完成,")
    print(f"          云端全量阶精度 100% 但断网 35% 降级导致续航完成率仅 {cloud['continuation_rate']:.2f}")

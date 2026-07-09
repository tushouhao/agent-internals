# 文件名: hybrid_collab_router.py
# 功能: 按任务协作深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_collab_router.py

"""混合路由器：协作深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_collab_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮失序" in task or "失序" in task:
        return "disorder"
    if "低协作" in task:
        return "disorder_msg"
    return "none"


def route(task: str) -> tuple:
    depth = detect_collab_depth(task)
    if depth == "none":
        return "none", True, "协作深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"disorder_msg": 0, "disorder": 0, "mismatch": 0, "none": 0}
    deliver_base = {"disorder_msg": 0.0, "disorder": 0.70, "mismatch": 0.0}
    latency_base = {"disorder_msg": 2, "disorder": 8, "mismatch": 68}
    delivers = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低协作"
        elif r < 0.66:
            task = f"任务_{i} 多轮失序"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        delivers.append(deliver_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_deliver": sum(delivers) / len(delivers) if delivers else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 消息错序 {r['stages']['disorder_msg']} / 协同失序 {r['stages']['disorder']} / 协作失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合送达率: {r['avg_deliver']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全协作失配: 送达 0% 堠迟 68s → 混合送达 {r['avg_deliver']:.0%} 堠迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 堠迟降 {(1 - r['avg_latency']/68)*100:.0f}% 送达不牺牲")


if __name__ == "__main__":
    main()

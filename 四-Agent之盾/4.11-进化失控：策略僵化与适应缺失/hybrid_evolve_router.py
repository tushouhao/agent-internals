# 文件名: hybrid_evolve_router.py
# 功能: 按任务进化深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_evolve_router.py

"""混合路由器：进化深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_evolve_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮漏适" in task or "漏适" in task:
        return "adaptation"
    if "低进化" in task:
        return "rigid"
    return "none"


def route(task: str) -> tuple:
    depth = detect_evolve_depth(task)
    if depth == "none":
        return "none", True, "进化深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"rigid": 0, "adaptation": 0, "mismatch": 0, "none": 0}
    evolve_base = {"rigid": 0.0, "adaptation": 0.66, "mismatch": 0.0}
    latency_base = {"rigid": 2, "adaptation": 9, "mismatch": 72}
    evolves = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低进化"
        elif r < 0.66:
            task = f"任务_{i} 多轮漏适"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        evolves.append(evolve_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_evolve": sum(evolves) / len(evolves) if evolves else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 僵化 {r['stages']['rigid']} / 适应 {r['stages']['adaptation']} / 失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合进化率: {r['avg_evolve']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全进化失配: 进化 0% 堠迟 72s → 混合进化 {r['avg_evolve']:.0%} 堠迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 堠迟降 {(1 - r['avg_latency']/72)*100:.0f}% 进化不牺牲")


if __name__ == "__main__":
    main()

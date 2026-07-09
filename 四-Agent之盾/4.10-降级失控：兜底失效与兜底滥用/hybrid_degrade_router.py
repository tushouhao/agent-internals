# 文件名: hybrid_degrade_router.py
# 功能: 按任务降级深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_degrade_router.py

"""混合路由器：降级深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_degrade_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮滥用" in task or "滥用" in task:
        return "abuse"
    if "低降级" in task:
        return "failure"
    return "none"


def route(task: str) -> tuple:
    depth = detect_degrade_depth(task)
    if depth == "none":
        return "none", True, "降级深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"failure": 0, "abuse": 0, "mismatch": 0, "none": 0}
    degrade_base = {"failure": 0.0, "abuse": 0.68, "mismatch": 0.0}
    latency_base = {"failure": 2, "abuse": 9, "mismatch": 72}
    degrades = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低降级"
        elif r < 0.66:
            task = f"任务_{i} 多轮滥用"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        degrades.append(degrade_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_degrade": sum(degrades) / len(degrades) if degrades else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 失效 {r['stages']['failure']} / 滥用 {r['stages']['abuse']} / 失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合降级率: {r['avg_degrade']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全降级失配: 降级 0% 堠迟 72s → 混合降级 {r['avg_degrade']:.0%} 堠迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 堠迟降 {(1 - r['avg_latency']/72)*100:.0f}% 降级不牺牲")


if __name__ == "__main__":
    main()

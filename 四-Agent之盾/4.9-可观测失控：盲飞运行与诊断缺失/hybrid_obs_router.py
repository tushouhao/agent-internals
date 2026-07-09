# 文件名: hybrid_obs_router.py
# 功能: 按任务可观测深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_obs_router.py

"""混合路由器：可观测深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_observable_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮漏诊" in task or "漏诊" in task:
        return "diagnosis"
    if "低观测" in task:
        return "blind"
    return "none"


def route(task: str) -> tuple:
    depth = detect_observable_depth(task)
    if depth == "none":
        return "none", True, "可观测深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"blind": 0, "diagnosis": 0, "mismatch": 0, "none": 0}
    observable_base = {"blind": 0.0, "diagnosis": 0.68, "mismatch": 0.0}
    latency_base = {"blind": 2, "diagnosis": 9, "mismatch": 72}
    observables = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低观测"
        elif r <  0.66:
            task = f"任务_{i} 多轮漏诊"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        observables.append(observable_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_observable": sum(observables) / len(observables) if observables else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 盲飞 {r['stages']['blind']} / 诊断 {r['stages']['diagnosis']} / 失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合可观测率: {r['avg_observable']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全可观测失配: 可观测 0% 堠迟 72s → 混合可观测 {r['avg_observable']:.0%} 堠迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 堠迟降 {(1 - r['avg_latency']/72)*100:.0f}% 可观测不牺牲")


if __name__ == "__main__":
    main()

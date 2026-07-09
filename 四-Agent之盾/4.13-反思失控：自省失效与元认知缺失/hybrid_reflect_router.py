# 文件名: hybrid_reflect_router.py
# 功能: 按任务反思深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_reflect_router.py

"""混合路由器：反思深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_reflect_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮漏识" in task or "漏识" in task:
        return "metacog"
    if "低反思" in task:
        return "introspect"
    return "none"


def route(task: str) -> tuple:
    depth = detect_reflect_depth(task)
    if depth == "none":
        return "none", True, "反思深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"introspect": 0, "metacog": 0, "mismatch": 0, "none": 0}
    reflect_base = {"introspect": 0.0, "metacog": 0.64, "mismatch": 0.0}
    latency_base = {"introspect": 2, "metacog": 9, "mismatch": 72}
    reflects = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低反思"
        elif r < 0.66:
            task = f"任务_{i} 多轮漏识"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        reflects.append(reflect_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_reflect": sum(reflects) / len(reflects) if reflects else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 失省 {r['stages']['introspect']} / 漏识 {r['stages']['metacog']} / 失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合反思率: {r['avg_reflect']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全反思失配: 反思 0% 延迟 72s → 混合反思 {r['avg_reflect']:.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/72)*100:.0f}% 反思不牺牲")


if __name__ == "__main__":
    main()

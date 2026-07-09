# 文件名: hybrid_memory_router.py
# 功能: 按任务记忆深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_memory_router.py

"""混合路由器：记忆深度判别 + 分流三级 + 拚答护栏。"""

import random

random.seed(42)


def detect_memory_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮失效" in task or "失效" in task:
        return "failure"
    if "低记忆" in task:
        return "forget"
    return "none"


def route(task: str) -> tuple:
    depth = detect_memory_depth(task)
    if depth == "none":
        return "none", True, "记忆深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"forget": 0, "failure": 0, "mismatch": 0, "none": 0}
    accumulate_base = {"forget": 0.0, "failure": 0.65, "mismatch": 0.0}
    latency_base = {"forget": 2, "failure": 9, "mismatch": 72}
    accumulates = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低记忆"
        elif r < 0.66:
            task = f"任务_{i} 多轮失效"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        accumulates.append(accumulate_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_accumulate": sum(accumulates) / len(accumulates) if accumulates else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 遗忘 {r['stages']['forget']} / 失效 {r['stages']['failure']} / 失配 {r['stages']['mismatch']} / 拚答 {r['stages']['none']}")
    print(f"  综合积累率: {r['avg_accumulate']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拚答率: {r['reject_rate']:.0%}")
    print(f"  对比全记忆失配: 积累 0% 堠迟 72s → 混合积累 {r['avg_accumulate']:.0%} 堠迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 堠迟降 {(1 - r['avg_latency']/72)*100:.0f}% 积累不牺牲")


if __name__ == "__main__":
    main()

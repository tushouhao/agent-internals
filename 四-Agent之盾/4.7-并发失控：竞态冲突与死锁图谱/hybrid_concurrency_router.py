# 文件名: hybrid_concurrency_router.py
# 功能: 按任务并发深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_concurrency_router.py

"""混合路由器：并发深度判别 + 分流三级 + 拒答护栏。"""

import random

random.seed(42)


def detect_concurrency_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "循环等待" in task or "死锁" in task:
        return "deadlock"
    if "低并发" in task:
        return "race"
    return "none"


def route(task: str) -> tuple:
    depth = detect_concurrency_depth(task)
    if depth == "none":
        return "none", True, "并发深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"race": 0, "deadlock": 0, "mismatch": 0, "none": 0}
    exec_base = {"race": 0.0, "deadlock": 0.74, "mismatch": 0.0}
    latency_base = {"race": 2, "deadlock": 7, "mismatch": 64}
    execs = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低并发"
        elif r < 0.66:
            task = f"任务_{i} 循环等待死锁"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        execs.append(exec_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_exec": sum(execs) / len(execs) if execs else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 竞态冲突 {r['stages']['race']} / 死锁图谱 {r['stages']['deadlock']} / 并发失配 {r['stages']['mismatch']} / 拒答 {r['stages']['none']}")
    print(f"  综合执行率: {r['avg_exec']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拒答率: {r['reject_rate']:.0%}")
    print(f"  对比全并发失配: 执行 0% 延迟 64s → 混合执行 {r['avg_exec']:.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/64)*100:.0f}% 执行不牺牲")


if __name__ == "__main__":
    main()

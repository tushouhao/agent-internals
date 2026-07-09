# 文件名: hybrid_call_router.py
# 功能: 按任务调用深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_call_router.py

"""混合路由器：调用深度判别 + 分流三级 + 拒答护栏。"""

import random

random.seed(42)


def detect_call_depth(task: str) -> str:
    if "跨版本" in task or "签名" in task:
        return "mismatch"
    if "跨轮" in task or "漂移" in task:
        return "drift"
    if "单调用" in task:
        return "hallucination"
    return "none"


def route(task: str) -> tuple:
    depth = detect_call_depth(task)
    if depth == "none":
        return "none", True, "调用深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"hallucination": 0, "drift": 0, "mismatch": 0, "none": 0}
    call_base = {"hallucination": 0.0, "drift": 0.96, "mismatch": 0.0}
    latency_base = {"hallucination": 2, "drift": 4, "mismatch": 45}
    calls = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 单调用"
        elif r < 0.66:
            task = f"任务_{i} 跨轮漂移"
        else:
            task = f"任务_{i} 跨版本签名"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        calls.append(call_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_call": sum(calls) / len(calls) if calls else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 参数幻觉 {r['stages']['hallucination']} / 语义漂移 {r['stages']['drift']} / 工具失配 {r['stages']['mismatch']} / 拒答 {r['stages']['none']}")
    print(f"  综合调用率: {r['avg_call']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拒答率: {r['reject_rate']:.0%}")
    print(f"  对比全工具失配: 调用 0% 延迟 45s → 混合调用 {r['avg_call']:.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/45)*100:.0f}% 调用不牺牲")


if __name__ == "__main__":
    main()

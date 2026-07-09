# 文件名: hybrid_quality_router.py
# 功能: 按任务质量深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_quality_router.py

"""混合路由器：质量深度判别 + 分流三级 + 拠答护栏。"""

import random

random.seed(42)


def detect_quality_depth(task: str) -> str:
    if "跨要求" in task or "失配" in task:
        return "mismatch"
    if "多轮退化" in task or "退化" in task:
        return "decay"
    if "低质量" in task:
        return "degrade"
    return "none"


def route(task: str) -> tuple:
    depth = detect_quality_depth(task)
    if depth == "none":
        return "none", True, "质量深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"degrade": 0, "decay": 0, "mismatch": 0, "none": 0}
    accept_base = {"degrade": 0.0, "decay": 0.76, "mismatch": 0.0}
    latency_base = {"degrade": 2, "decay": 6, "mismatch": 52}
    accepts = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低质量"
        elif r < 0.66:
            task = f"任务_{i} 多轮退化"
        else:
            task = f"任务_{i} 跨要求失配"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        accepts.append(accept_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_accept": sum(accepts) / len(accepts) if accepts else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 产物降级 {r['stages']['degrade']} / 质量退化 {r['stages']['decay']} / 质量失配 {r['stages']['mismatch']} / 拠答 {r['stages']['none']}")
    print(f"  综合接受率: {r['avg_accept']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拠答率: {r['reject_rate']:.0%}")
    print(f"  对比全质量失配: 接受 0% 延迟 52s → 混合接受 {r['avg_accept']:.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/52)*100:.0f}% 接受不牺牲")


if __name__ == "__main__":
    main()

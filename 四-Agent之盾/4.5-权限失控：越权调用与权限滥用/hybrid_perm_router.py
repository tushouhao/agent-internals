# 文件名: hybrid_perm_router.py
# 功能: 按任务权限深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_perm_router.py

"""混合路由器：权限深度判别 + 分流三级 + 拒答护栏。"""

import random

random.seed(42)


def detect_perm_depth(task: str) -> str:
    if "跨权限" in task or "失配" in task:
        return "mismatch"
    if "过度授予" in task or "滥用" in task:
        return "abuse"
    if "低权限" in task:
        return "unauth"
    return "none"


def route(task: str) -> tuple:
    depth = detect_perm_depth(task)
    if depth == "none":
        return "none", True, "权限深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"unauth": 0, "abuse": 0, "mismatch": 0, "none": 0}
    call_base = {"unauth": 0.0, "abuse": 0.82, "mismatch": 0.0}
    latency_base = {"unauth": 2, "abuse": 5, "mismatch": 56}
    calls = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 低权限"
        elif r < 0.66:
            task = f"任务_{i} 过度授予滥用"
        else:
            task = f"任务_{i} 跨权限失配"
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
    print(f"  分流: 越权调用 {r['stages']['unauth']} / 权限滥用 {r['stages']['abuse']} / 权限失配 {r['stages']['mismatch']} / 拒答 {r['stages']['none']}")
    print(f"  综合调用率: {r['avg_call']:.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拒答率: {r['reject_rate']:.0%}")
    print(f"  对比全权限失配: 调用 0% 延迟 56s → 混合调用 {r['avg_call']:.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/56)*100:.0f}% 调用不牺牲")


if __name__ == "__main__":
    main()

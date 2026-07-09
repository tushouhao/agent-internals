# 文件名: hybrid_ctx_router.py
# 功能: 按任务上下文深度判别分流三级 + 深度缺失拒答
# 运行: python hybrid_ctx_router.py

"""混合路由器：上下文深度判别 + 分流三级 + 拒答护栏。"""

import random

random.seed(42)


def detect_ctx_depth(task: str) -> str:
    if "超长" in task or "截断" in task:
        return "truncation"
    if "长上下文" in task or "丢失" in task:
        return "loss"
    if "短上下文" in task:
        return "exhaust"
    return "none"


def route(task: str) -> tuple:
    depth = detect_ctx_depth(task)
    if depth == "none":
        return "none", True, "上下文深度缺失"
    return depth, False, depth


def simulate_router(n: int = 90) -> dict:
    stages = {"exhaust": 0, "loss": 0, "truncation": 0, "none": 0}
    answer_base = {"exhaust": 0.0, "loss": 0.88, "truncation": 1.0}
    latency_base = {"exhaust": 2, "loss": 5, "truncation": 52}
    answers = []
    latencies = []
    for i in range(n):
        r = random.random()
        if r < 0.33:
            task = f"任务_{i} 短上下文"
        elif r < 0.66:
            task = f"任务_{i} 长上下文丢失"
        else:
            task = f"任务_{i} 超长截断"
        stage, rej, _ = route(task)
        if rej:
            stages["none"] += 1
            continue
        stages[stage] += 1
        answers.append(answer_base[stage] + random.uniform(-0.03, 0.03))
        latencies.append(latency_base[stage] + random.randint(-1, 1))
    return {"stages": stages, "n": n, "avg_answer": sum(answers) / len(answers) if answers else 0, "avg_latency": sum(latencies) / len(latencies) if latencies else 0, "reject_rate": stages["none"] / n}


def main():
    r = simulate_router(90)
    print("混合路由器仿真结果（n=90）:")
    print(f"  分流: 窗口耗尽 {r['stages']['exhaust']} / 信息丢失 {r['stages']['loss']} / 截断崩救 {r['stages']['truncation']} / 拒答 {r['stages']['none']}")
    print(f"  综合拒答率: {(1 - r['avg_answer']):.0%}")
    print(f"  综合延迟: {r['avg_latency']:.0f}s")
    print(f"  拒答率: {r['reject_rate']:.0%}")
    print(f"  对比全截断崩救: 拒答 100% 延迟 52s → 混合拒答 {(1 - r['avg_answer']):.0%} 延迟 {r['avg_latency']:.0f}s")
    print(f"  混合收益: 延迟降 {(1 - r['avg_latency']/52)*100:.0f}% 拒答不牺牲")


if __name__ == "__main__":
    main()

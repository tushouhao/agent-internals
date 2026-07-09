# 文件名: failure_fallback.py
# 功能: 效降级兜底三策略，止于记忆残留率
# 运行: python failure_fallback.py

"""失效降级兜底：从产物/轮数/历史反推失效。"""

import random

random.seed(42)


def artifact_anomaly_detect(artifact: str, expected: str) -> dict:
    return {"failure_detected": artifact != expected, "method": "产物反推"}


def turn_count_limit_detect(turns: int, limit: int = 40) -> dict:
    return {"failure_detected": turns > limit, "method": "轮数反推"}


def baseline_history_detect(memory: str, baseline: str = "ok") -> dict:
    return {"failure_detected": memory != baseline, "method": "历史反推"}


def simulate_fallback(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        method = random.choice(["产物", "轮数", "历史"])
        if method == "产物":
            r = artifact_anomaly_detect("产物_失效", "产物_正常")
            if r["failure_detected"]:
                success += 1
        elif method == "轮数":
            r = turn_count_limit_detect(45, limit=40)
            if r["failure_detected"]:
                success += 1
        else:
            r = baseline_history_detect("失效", baseline="ok")
            if r["failure_detected"]:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（产物/轮数/历史三策略反推）")
    print(f"  三策略: 产物异常 / 轮数上限 / 基线历史")


if __name__ == "__main__":
    main()

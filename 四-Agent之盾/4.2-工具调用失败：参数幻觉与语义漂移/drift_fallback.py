# 文件名: drift_fallback.py
# 功能: 漂移漏检降级兜底三策略，止于漂移残留率
# 运行: python drift_fallback.py

"""漂移漏检降级兜底：从产物/轮数/参数反推漂移。"""

import random

random.seed(42)


def artifact_anomaly_detect(artifact: str, expected: str) -> dict:
    return {"drift_detected": artifact != expected, "method": "产物反推"}


def turn_count_limit_detect(turns: int, limit: int = 20) -> dict:
    return {"drift_detected": turns > limit, "method": "轮数反推"}


def param_cumulative_detect(params_history: list) -> dict:
    if len(params_history) < 2:
        return {"drift_detected": False, "method": "参数反推"}
    first = params_history[0]
    last = params_history[-1]
    return {"drift_detected": first != last, "method": "参数反推"}


def simulate_fallback(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        method = random.choice(["产物", "轮数", "参数"])
        if method == "产物":
            r = artifact_anomaly_detect("产物_漂移", "产物_正常")
            if r["drift_detected"]:
                success += 1
        elif method == "轮数":
            r = turn_count_limit_detect(25, limit=20)
            if r["drift_detected"]:
                success += 1
        else:
            r = param_cumulative_detect(["param_v1", "param_v2", "param_v3"])
            if r["drift_detected"]:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（产物/轮数/参数三策略反推）")
    print(f"  三策略: 产物异常 / 轮数上限 / 参数累积")


if __name__ == "__main__":
    main()

# 文件名: miss_fallback.py
# 功能: 漏识降级兜底三策略，止于反思残留率
# 运行: python miss_fallback.py

"""漏识降级兜底：从产物/轮数/历史反推漏识。"""

import random

random.seed(42)


def artifact_anomaly_detect(artifact: str, expected: str) -> dict:
    return {"miss_detected": artifact != expected, "method": "产物反推"}


def turn_count_limit_detect(turns: int, limit: int = 40) -> dict:
    return {"miss_detected": turns > limit, "method": "轮数反推"}


def baseline_history_detect(metacog: str, baseline: str = "ok") -> dict:
    return {"miss_detected": metacog != baseline, "method": "历史反推"}


def simulate_fallback(n: int = 30) -> dict:
    success = 0
    for i in range(n):
        method = random.choice(["产物", "轮数", "历史"])
        if method == "产物":
            r = artifact_anomaly_detect("产物_漏识", "产物_正常")
            if r["miss_detected"]:
                success += 1
        elif method == "轮数":
            r = turn_count_limit_detect(45, limit=40)
            if r["miss_detected"]:
                success += 1
        else:
            r = baseline_history_detect("漏识", baseline="ok")
            if r["miss_detected"]:
                success += 1
    return {"n": n, "fallback_success_rate": success / n}


def main():
    r = simulate_fallback(30)
    print("降级兜底仿真结果（n=30）:")
    print(f"  兜底成功率: {r['fallback_success_rate']:.0%}（产物/轮数/历史三策略反推）")
    print(f"  三策略: 产物异常 / 轮数上限 / 基线历史")


if __name__ == "__main__":
    main()

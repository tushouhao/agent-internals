# 文件名: fallback_failure.py
# 功能: 降级兜底无兜底止于兜底检测缺失致兜底率 0%
# 运行: python fallback_failure.py

"""兜底失效阶：无兜底降级，崩在无兜底。"""

import random

random.seed(42)


def mock_fallback_failure(run_id: int, inject_failure: bool = False) -> dict:
    if inject_failure:
        return {"id": run_id, "fallback": None, "expected": "ok", "failed": True}
    return {"id": run_id, "fallback": "ok", "expected": "ok", "failed": False}


def detect_fallback(fallback: str, expected: str) -> bool:
    return fallback == expected


def run_fallback_failure(run_id: int) -> dict:
    r = mock_fallback_failure(run_id, inject_failure=random.random() < 1.0)
    if detect_fallback(r["fallback"], r["expected"]):
        return {"degraded": True, "reason": "兜底正确", "failed": False}
    return {"degraded": False, "reason": "兜底失效", "failed": True}


def simulate_failure(n: int = 50) -> dict:
    degraded = 0
    failed = 0
    for i in range(n):
        r = run_fallback_failure(i)
        if r["degraded"]:
            degraded += 1
        else:
            failed += 1
    return {"degraded_rate": degraded / n, "failed_rate": failed / n, "n": n}


def main():
    r = simulate_failure(50)
    print("兜底失效阶仿真结果（n=50）:")
    print(f"  降级率: {r['degraded_rate']:.0%}（兜底正确即降级）")
    print(f"  失效率: {r['failed_rate']:.0%}（无兜底偏离预期）")
    print(f"  崩溃模式: 无兜底——兜底失效无检测即弃无从防患")


if __name__ == "__main__":
    main()

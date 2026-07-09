# 文件名: introspect_failure.py
# 功能: Agent 无自省止于失省检测缺失致失省率 100%
# 运行: python introspect_failure.py

"""自省失效阶：无自省反思，崩在无自省。"""

import random

random.seed(42)


def mock_introspect_failure(run_id: int, inject_failure: bool = False) -> dict:
    if inject_failure:
        return {"id": run_id, "introspect": None, "expected": "ok", "failed": True}
    return {"id": run_id, "introspect": "ok", "expected": "ok", "failed": False}


def detect_failure(introspect: str, expected: str) -> bool:
    return introspect == expected


def run_introspect_failure(run_id: int) -> dict:
    r = mock_introspect_failure(run_id, inject_failure=random.random() < 1.0)
    if detect_failure(r["introspect"], r["expected"]):
        return {"reflected": True, "reason": "自省正确", "failed": False}
    return {"reflected": False, "reason": "自省失效", "failed": True}


def simulate_failure(n: int = 50) -> dict:
    reflected = 0
    failed = 0
    for i in range(n):
        r = run_introspect_failure(i)
        if r["reflected"]:
            reflected += 1
        else:
            failed += 1
    return {"reflected_rate": reflected / n, "failed_rate": failed / n, "n": n}


def main():
    r = simulate_failure(50)
    print("自省失效阶仿真结果（n=50）:")
    print(f"  反思率: {r['reflected_rate']:.0%}（自省正确即反思）")
    print(f"  失省率: {r['failed_rate']:.0%}（无自省偏离预期）")
    print(f"  崩溃模式: 无自省——自省失效无检测即弃无从防患")


if __name__ == "__main__":
    main()

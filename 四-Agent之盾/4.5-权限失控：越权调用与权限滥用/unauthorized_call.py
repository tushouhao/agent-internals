# 文件名: unauthorized_call.py
# 功能: Agent 调用无权限工具止于检测缺失致越权率 100%
# 运行: python unauthorized_call.py

"""越权调用阶：无权限调用，崩在检测漏。"""

import random

random.seed(42)


def mock_unauthorized_call(tool: str, inject_unauth: bool = False) -> dict:
    if inject_unauth:
        return {"tool": tool, "caller_perm": "none", "required_perm": "admin", "unauthorized": True}
    return {"tool": tool, "caller_perm": "admin", "required_perm": "admin", "unauthorized": False}


def detect_permission(caller_perm: str, required_perm: str) -> bool:
    return caller_perm == required_perm


def run_unauthorized_call(tool: str) -> dict:
    r = mock_unauthorized_call(tool, inject_unauth=random.random() < 1.0)
    if detect_permission(r["caller_perm"], r["required_perm"]):
        return {"called": True, "reason": "权限适配", "unauthorized": False}
    return {"called": False, "reason": "越权调用", "unauthorized": True}


def simulate_unauth(n: int = 50) -> dict:
    called = 0
    unauthorized = 0
    for i in range(n):
        r = run_unauthorized_call(f"工具_{i}")
        if r["called"]:
            called += 1
        else:
            unauthorized += 1
    return {"called_rate": called / n, "unauthorized_rate": unauthorized / n, "n": n}


def main():
    r = simulate_unauth(50)
    print("越权调用阶仿真结果（n=50）:")
    print(f"  调用率: {r['called_rate']:.0%}（权限适配即调）")
    print(f"  越权率: {r['unauthorized_rate']:.0%}（调用方无权限越权）")
    print(f"  崩溃模式: 检测漏——越权调用无检测即弃无从防患")


if __name__ == "__main__":
    main()

# 文件名: permission_abuse.py
# 功能: 权限过度授予滥用+滥用检测，止于滥用漏检率
# 运行: python permission_abuse.py

"""权限滥用阶：过度授予滥用检测，崩在滥用漏检。"""

import random

random.seed(42)


def mock_over_grant(tool: str, inject_abuse: bool = False) -> dict:
    if inject_abuse:
        return {"tool": tool, "granted": "admin", "required": "read", "abused": True}
    return {"tool": tool, "granted": "read", "required": "read", "abused": False}


def detect_abuse(grant: dict, inject_miss: bool = False) -> dict:
    if inject_miss:
        return {"abuse_detected": False, "missed": True}
    return {"abuse_detected": grant["granted"] != grant["required"], "missed": False}


def simulate_abuse(n: int = 50) -> dict:
    detected = 0
    missed = 0
    for i in range(n):
        grant = mock_over_grant(f"工具_{i}", inject_abuse=random.random() < 0.90)
        r = detect_abuse(grant, inject_miss=random.random() < 0.10)
        if r["abuse_detected"]:
            detected += 1
        if r["missed"]:
            missed += 1
    return {"detected_rate": detected / n, "miss_rate": missed / n, "residual_rate": missed / n, "n": n}


def main():
    r = simulate_abuse(50)
    print("权限滥用阶仿真结果（n=50）:")
    print(f"  检出率: {r['detected_rate']:.0%}（滥用被检出可防患）")
    print(f"  漏检率: {r['miss_rate']:.0%}（滥用检测漏检）")
    print(f"  残留率: {r['residual_rate']:.0%}（漏检致权限滥用残留）")
    print(f"  崩溃模式: 滥用漏检——滥用检测漏检致权限滥用无从防患")


if __name__ == "__main__":
    main()

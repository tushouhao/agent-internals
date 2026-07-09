# 文件名: permission_mismatch.py
# 功能: 权限与调用方失配+适配检测，止于适配漏校率
# 运行: python permission_mismatch.py

"""权限失配阶：跨权限适配检测，崩在适配漏校。"""

import random

random.seed(42)


def mock_perm_caller_alignment(inject_mismatch: bool = False) -> dict:
    if inject_mismatch:
        return {"caller": "read", "required": "admin", "matched": False}
    return {"caller": "admin", "required": "admin", "matched": True}


def validate_alignment(caller: str, required: str) -> dict:
    if caller == required:
        return {"matched": True, "reason": "权限适配"}
    if required == "read" and caller in ("admin", "write", "read"):
        return {"matched": True, "reason": "权限向下兼容"}
    return {"matched": False, "reason": f"权限失配 {caller}<{required}"}


def simulate_mismatch(n: int = 50) -> dict:
    matched = 0
    mismatched = 0
    for i in range(n):
        r = mock_perm_caller_alignment(inject_mismatch=random.random() < 1.0)
        v = validate_alignment(r["caller"], r["required"])
        if v["matched"]:
            matched += 1
        else:
            mismatched += 1
    return {"matched_rate": matched / n, "mismatched_rate": mismatched / n, "n": n}


def main():
    r = simulate_mismatch(50)
    print("权限失配阶仿真结果（n=50）:")
    print(f"  适配率: {r['matched_rate']:.0%}（适配检测通过）")
    print(f"  失配率: {r['mismatched_rate']:.0%}（调用方 read < 要求 admin 致失配）")
    print(f"  崩溃模式: 适配漏校——权限与调用方无校验即崩")


if __name__ == "__main__":
    main()

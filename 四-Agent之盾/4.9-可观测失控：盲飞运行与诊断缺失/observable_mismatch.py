# 文件名: observable_mismatch.py
# 功能: 观测策略与诊断要求失配+适配检测，止于适配漏校率
# 运行: python observable_mismatch.py

"""可观测失配阶：跨要求适配检测，崩在适配漏校。"""

import random

random.seed(42)


def mock_observable_requirement_alignment(inject_mismatch: bool = False) -> dict:
    if inject_mismatch:
        return {"actual": 1, "required": 6, "matched": False}
    return {"actual": 6, "required": 6, "matched": True}


def validate_alignment(actual: int, required: int, tolerance: int = 1) -> dict:
    if actual > required + tolerance:
        return {"matched": False, "reason": f"超观测 {actual}>{required+tolerance}"}
    if actual < required - tolerance:
        return {"matched": False, "reason": f"欠观测 {actual}<{required-tolerance}"}
    return {"matched": True, "reason": "观测适配"}


def simulate_mismatch(n: int = 50) -> dict:
    matched = 0
    mismatched = 0
    for i in range(n):
        r = mock_observable_requirement_alignment(inject_mismatch=random.random() < 1.0)
        v = validate_alignment(r["actual"], r["required"])
        if v["matched"]:
            matched += 1
        else:
            mismatched += 1
    return {"matched_rate": matched / n, "mismatched_rate": mismatched / n, "n": n}


def main():
    r = simulate_mismatch(50)
    print("可观测失配阶仿真结果（n=50）:")
    print(f"  适配率: {r['matched_rate']:.0%}（适配检测通过）")
    print(f"  失配率: {r['mismatched_rate']:.0%}（观测 1 < 要求 6 致欠观测）")
    print(f"  崩溃模式: 适配漏校——观测与要求无校验即崩")


if __name__ == "__main__":
    main()

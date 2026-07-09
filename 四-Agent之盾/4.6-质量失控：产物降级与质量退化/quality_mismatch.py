# 文件名: quality_mismatch.py
# 功能: 产物质量与任务要求失配+适配检测，止于适配漏校率
# 运行: python quality_mismatch.py

"""质量失配阶：跨要求适配检测，崩在适配漏校。"""

import random

random.seed(42)


def mock_quality_requirement_alignment(inject_mismatch: bool = False) -> dict:
    if inject_mismatch:
        return {"actual": 0.3, "required": 0.8, "matched": False}
    return {"actual": 0.8, "required": 0.8, "matched": True}


def validate_alignment(actual: float, required: float, tolerance: float = 0.1) -> dict:
    ratio = actual / required
    if ratio > 1 + tolerance:
        return {"matched": False, "reason": f"超要求 {ratio:.2f}×"}
    if ratio < 1 - tolerance:
        return {"matched": False, "reason": f"欠要求 {ratio:.2f}×"}
    return {"matched": True, "reason": "质量适配"}


def simulate_mismatch(n: int = 50) -> dict:
    matched = 0
    mismatched = 0
    for i in range(n):
        r = mock_quality_requirement_alignment(inject_mismatch=random.random() < 1.0)
        v = validate_alignment(r["actual"], r["required"])
        if v["matched"]:
            matched += 1
        else:
            mismatched += 1
    return {"matched_rate": matched / n, "mismatched_rate": mismatched / n, "n": n}


def main():
    r = simulate_mismatch(50)
    print("质量失配阶仿真结果（n=50）:")
    print(f"  适配率: {r['matched_rate']:.0%}（适配检测通过）")
    print(f"  失配率: {r['mismatched_rate']:.0%}（产物 0.3 < 要求 0.8 致失配）")
    print(f"  崩溃模式: 适配漏校——产物与要求无校验即崩")


if __name__ == "__main__":
    main()

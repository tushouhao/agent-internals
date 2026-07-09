# 文件名: cost_mismatch.py
# 功能: 成本与预算失配+适配检测，止于适配漏校率
# 运行: python cost_mismatch.py

"""成本失配阶：跨预算适配检测，崩在适配漏校。"""

import random

random.seed(42)


def mock_cost_budget_alignment(budget: float, inject_mismatch: bool = False) -> dict:
    if inject_mismatch:
        return {"budget": budget, "actual_cost": budget * 1.5, "matched": False}
    return {"budget": budget, "actual_cost": budget, "matched": True}


def validate_alignment(cost: float, budget: float, tolerance: float = 0.05) -> dict:
    ratio = cost / budget
    if ratio > 1 + tolerance:
        return {"matched": False, "reason": f"超支 {ratio:.2f}×"}
    if ratio < 1 - tolerance:
        return {"matched": False, "reason": f"欠支 {ratio:.2f}×"}
    return {"matched": True, "reason": "适配对齐"}


def simulate_mismatch(n: int = 50) -> dict:
    matched = 0
    mismatched = 0
    for i in range(n):
        budget = 1.0
        r = mock_cost_budget_alignment(budget, inject_mismatch=random.random() < 1.0)
        v = validate_alignment(r["actual_cost"], r["budget"])
        if v["matched"]:
            matched += 1
        else:
            mismatched += 1
    return {"matched_rate": matched / n, "mismatched_rate": mismatched / n, "n": n}


def main():
    r = simulate_mismatch(50)
    print("成本失配阶仿真结果（n=50）:")
    print(f"  适配率: {r['matched_rate']:.0%}（适配检测通过）")
    print(f"  失配率: {r['mismatched_rate']:.0%}（成本超预算 1.5× 致失配）")
    print(f"  崩溃模式: 适配漏校——成本与预算无校验即崩")


if __name__ == "__main__":
    main()

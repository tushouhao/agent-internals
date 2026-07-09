# 文件名: perm_residual.py
# 功能: 权限残留率量化——滥用检测 6% 精防患 vs 越权调用 100% 无防患
# 运行: python perm_residual.py

"""权限残留率：宁可滥用检测防患不可越权调用即救的核心 KPI。"""

import random

random.seed(42)


def unauthorized_call(task: dict) -> dict:
    return {"called": False, "detected": False, "residual": 1.0}


def permission_abuse(task: dict) -> dict:
    missed = random.random() < 0.18
    if missed:
        return {"called": True, "detected": False, "residual": 0.18}
    return {"called": True, "detected": True, "residual": 0.0}


def permission_mismatch(task: dict) -> dict:
    return {"called": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"unauth": {"called": 0, "residual": []},
             "abuse": {"called": 0, "residual": []},
             "mismatch": {"called": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("unauth", unauthorized_call), ("abuse", permission_abuse), ("mismatch", permission_mismatch)]:
            r = func(task)
            if r["called"]:
                stats[level]["called"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "unauth": {"call": stats["unauth"]["called"] / n, "residual": sum(stats["unauth"]["residual"]) / n},
        "abuse": {"call": stats["abuse"]["called"] / n, "residual": sum(stats["abuse"]["residual"]) / n},
        "mismatch": {"call": stats["mismatch"]["called"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("权限残留率仿真结果（n=90）:")
    for level in ["unauth", "abuse", "mismatch"]:
        v = r[level]
        print(f"  {level}: 调用率 {v['call']:.0%} / 权限残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    权限滥用检测阶残留率 {r['abuse']['residual']:.0%} 即滥用检测+降级兜底保低残留水平")
    print(f"    越权调用阶残留率 {r['unauth']['residual']:.0%} 即无滥用检测权限必滥用无从防患")
    print(f"    结论: 核心 KPI 是权限残留率——宁可滥用检测防患不可越权调用即救")


if __name__ == "__main__":
    main()

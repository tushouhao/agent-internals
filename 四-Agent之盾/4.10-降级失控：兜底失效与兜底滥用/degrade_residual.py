# 文件名: degrade_residual.py
# 功能: 降级残留率量化——滥用检测 2% 精防患 vs 兜底失效 100% 无防患
# 运行: python degrade_residual.py

"""降级残留率：宁可滥用检测防患不可兜底失效即救的核心 KPI。"""

import random

random.seed(42)


def fallback_failure(task: dict) -> dict:
    return {"degraded": False, "detected": False, "residual": 1.0}


def fallback_abuse(task: dict) -> dict:
    missed = random.random() < 0.15
    if missed:
        return {"degraded": True, "detected": False, "residual": 0.15}
    return {"degraded": True, "detected": True, "residual": 0.0}


def degrade_mismatch(task: dict) -> dict:
    return {"degraded": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"failure": {"degraded": 0, "residual": []},
             "abuse": {"degraded": 0, "residual": []},
             "mismatch": {"degraded": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("failure", fallback_failure), ("abuse", fallback_abuse), ("mismatch", degrade_mismatch)]:
            r = func(task)
            if r["degraded"]:
                stats[level]["degraded"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "failure": {"degrade": stats["failure"]["degraded"] / n, "residual": sum(stats["failure"]["residual"]) / n},
        "abuse": {"degrade": stats["abuse"]["degraded"] / n, "residual": sum(stats["abuse"]["residual"]) / n},
        "mismatch": {"degrade": stats["mismatch"]["degraded"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("降级残留率仿真结果（n=90）:")
    for level in ["failure", "abuse", "mismatch"]:
        v = r[level]
        print(f"  {level}: 降级率 {v['degrade']:.0%} / 降级残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    兜底滥用检测阶残留率 {r['abuse']['residual']:.0%} 即滥用检测+降级兜底保低残留水平")
    print(f"    兜底失效阶残留率 {r['failure']['residual']:.0%} 即无滥用检测降级必滥用无从防患")
    print(f"    结论: 核心 KPI 是降级残留率——宁可滥用检测防患不可兜底失效即救")


if __name__ == "__main__":
    main()

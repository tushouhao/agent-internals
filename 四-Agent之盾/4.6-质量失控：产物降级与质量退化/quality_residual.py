# 文件名: quality_residual.py
# 功能: 质量残留率量化——退化检测 4% 精防患 vs 产物降级 100% 无防患
# 运行: python quality_residual.py

"""质量残留率：宁可退化检测防患不可产物降级即救的核心 KPI。"""

import random

random.seed(42)


def artifact_degrade(task: dict) -> dict:
    return {"accepted": False, "detected": False, "residual": 1.0}


def quality_decay(task: dict) -> dict:
    missed = random.random() < 0.12
    if missed:
        return {"accepted": True, "detected": False, "residual": 0.12}
    return {"accepted": True, "detected": True, "residual": 0.0}


def quality_mismatch(task: dict) -> dict:
    return {"accepted": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"degrade": {"accepted": 0, "residual": []},
             "decay": {"accepted": 0, "residual": []},
             "mismatch": {"accepted": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("degrade", artifact_degrade), ("decay", quality_decay), ("mismatch", quality_mismatch)]:
            r = func(task)
            if r["accepted"]:
                stats[level]["accepted"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "degrade": {"accept": stats["degrade"]["accepted"] / n, "residual": sum(stats["degrade"]["residual"]) / n},
        "decay": {"accept": stats["decay"]["accepted"] / n, "residual": sum(stats["decay"]["residual"]) / n},
        "mismatch": {"accept": stats["mismatch"]["accepted"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("质量残留率仿真结果（n=90）:")
    for level in ["degrade", "decay", "mismatch"]:
        v = r[level]
        print(f"  {level}: 接受率 {v['accept']:.0%} / 质量残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    质量退化检测阶残留率 {r['decay']['residual']:.0%} 即退化检测+降级兜底保低残留水平")
    print(f"    产物降级阶残留率 {r['degrade']['residual']:.0%} 即无退化检测质量必退化无从防患")
    print(f"    结论: 核心 KPI 是质量残留率——宁可退化检测防患不可产物降级即救")


if __name__ == "__main__":
    main()

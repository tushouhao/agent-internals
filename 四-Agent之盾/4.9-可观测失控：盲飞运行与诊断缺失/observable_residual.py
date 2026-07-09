# 文件名: observable_residual.py
# 功能: 可观测残留率量化——诊断检测 2% 精防患 vs 盲飞运行 100% 无防患
# 运行: python observable_residual.py

"""可观测残留率：宁可诊断检测防患不可盲飞运行即救的核心 KPI。"""

import random

random.seed(42)


def blind_flying(task: dict) -> dict:
    return {"observable": False, "detected": False, "residual": 1.0}


def diagnosis_missing(task: dict) -> dict:
    missed = random.random() < 0.14
    if missed:
        return {"observable": True, "detected": False, "residual": 0.14}
    return {"observable": True, "detected": True, "residual": 0.0}


def observable_mismatch(task: dict) -> dict:
    return {"observable": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"blind": {"observable": 0, "residual": []},
             "diagnosis": {"observable": 0, "residual": []},
             "mismatch": {"observable": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("blind", blind_flying), ("diagnosis", diagnosis_missing), ("mismatch", observable_mismatch)]:
            r = func(task)
            if r["observable"]:
                stats[level]["observable"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "blind": {"observable": stats["blind"]["observable"] / n, "residual": sum(stats["blind"]["residual"]) / n},
        "diagnosis": {"observable": stats["diagnosis"]["observable"] / n, "residual": sum(stats["diagnosis"]["residual"]) / n},
        "mismatch": {"observable": stats["mismatch"]["observable"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("可观测残留率仿真结果（n=90）:")
    for level in ["blind", "diagnosis", "mismatch"]:
        v = r[level]
        print(f"  {level}: 可观测率 {v['observable']:.0%} / 可观测残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    诊断缺失检测阶残留率 {r['diagnosis']['residual']:.0%} 即诊断检测+降级兜底保低残留水平")
    print(f"    盲飞运行阶残留率 {r['blind']['residual']:.0%} 即无诊断检测运行必漏诊无从防患")
    print(f"    结论: 核心 KPI 是可观测残留率——宁可诊断检测防患不可盲飞运行即救")


if __name__ == "__main__":
    main()

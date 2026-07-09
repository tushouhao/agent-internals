# 文件名: reflect_residual.py
# 功能: 反思残留率量化——漏识检测 3% 精防患 vs 自省失效 100% 无防患
# 运行: python reflect_residual.py

"""反思残留率：宁可漏识检测防患不可自省失效即救的核心 KPI。"""

import random

random.seed(42)


def introspect_failure(task: dict) -> dict:
    return {"reflected": False, "detected": False, "residual": 1.0}


def metacog_missing(task: dict) -> dict:
    missed = random.random() < 0.18
    if missed:
        return {"reflected": True, "detected": False, "residual": 0.18}
    return {"reflected": True, "detected": True, "residual": 0.0}


def reflect_mismatch(task: dict) -> dict:
    return {"reflected": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"introspect": {"reflected": 0, "residual": []},
             "metacog": {"reflected": 0, "residual": []},
             "mismatch": {"reflected": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("introspect", introspect_failure), ("metacog", metacog_missing), ("mismatch", reflect_mismatch)]:
            r = func(task)
            if r["reflected"]:
                stats[level]["reflected"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "introspect": {"reflect": stats["introspect"]["reflected"] / n, "residual": sum(stats["introspect"]["residual"]) / n},
        "metacog": {"reflect": stats["metacog"]["reflected"] / n, "residual": sum(stats["metacog"]["residual"]) / n},
        "mismatch": {"reflect": stats["mismatch"]["reflected"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("反思残留率仿真结果（n=90）:")
    for level in ["introspect", "metacog", "mismatch"]:
        v = r[level]
        print(f"  {level}: 反思率 {v['reflect']:.0%} / 反思残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    元认知缺失检测阶残留率 {r['metacog']['residual']:.0%} 即漏识检测+降级兜底保低残留水平")
    print(f"    自省失效阶残留率 {r['introspect']['residual']:.0%} 即无漏识检测反思必失省无从防患")
    print(f"    结论: 核心 KPI 是反思残留率——宁可漏识检测防患不可自省失效即救")


if __name__ == "__main__":
    main()

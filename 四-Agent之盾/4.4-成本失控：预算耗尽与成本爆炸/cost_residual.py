# 文件名: cost_residual.py
# 功能: 成本残留率量化——适配检测 4% 精防患 vs 预算耗尽 100% 无防患
# 运行: python cost_residual.py

"""成本残留率：宁可适配检测防患不可预算耗尽即救的核心 KPI。"""

import random

random.seed(42)


def budget_exhaust(task: dict) -> dict:
    return {"answered": False, "detected": False, "residual": 1.0}


def cost_explosion(task: dict) -> dict:
    missed = random.random() < 0.14
    if missed:
        return {"answered": True, "detected": False, "residual": 0.14}
    return {"answered": True, "detected": True, "residual": 0.0}


def cost_mismatch(task: dict) -> dict:
    return {"answered": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"exhaust": {"answered": 0, "residual": []},
             "explosion": {"answered": 0, "residual": []},
             "mismatch": {"answered": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("exhaust", budget_exhaust), ("explosion", cost_explosion), ("mismatch", cost_mismatch)]:
            r = func(task)
            if r["answered"]:
                stats[level]["answered"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "exhaust": {"answer": stats["exhaust"]["answered"] / n, "residual": sum(stats["exhaust"]["residual"]) / n},
        "explosion": {"answer": stats["explosion"]["answered"] / n, "residual": sum(stats["explosion"]["residual"]) / n},
        "mismatch": {"answer": stats["mismatch"]["answered"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("成本残留率仿真结果（n=90）:")
    for level in ["exhaust", "explosion", "mismatch"]:
        v = r[level]
        print(f"  {level}: 拒答率 {(1 - v['answer']):.0%} / 成本残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    成本爆炸检测阶残留率 {r['explosion']['residual']:.0%} 即突增检测+降级兜底保低残留水平")
    print(f"    预算耗尽阶残留率 {r['exhaust']['residual']:.0%} 即无适配检测成本必失控无从防患")
    print(f"    结论: 核心 KPI 是成本残留率——宁可适配检测防患不可预算耗尽即救")


if __name__ == "__main__":
    main()

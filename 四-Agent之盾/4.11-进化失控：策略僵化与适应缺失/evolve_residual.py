# 文件名: evolve_residual.py
# 功能: 进化残留率量化——适应检测 2% 精防患 vs 策略僵化 100% 无防患
# 运行: python evolve_residual.py

"""进化残留率：宁可适应检测防患不可策略僵化即救的核心 KPI。"""

import random

random.seed(42)


def strategy_rigid(task: dict) -> dict:
    return {"evolved": False, "detected": False, "residual": 1.0}


def adaptation_missing(task: dict) -> dict:
    missed = random.random() < 0.16
    if missed:
        return {"evolved": True, "detected": False, "residual": 0.16}
    return {"evolved": True, "detected": True, "residual": 0.0}


def evolve_mismatch(task: dict) -> dict:
    return {"evolved": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"rigid": {"evolved": 0, "residual": []},
             "adaptation": {"evolved": 0, "residual": []},
             "mismatch": {"evolved": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("rigid", strategy_rigid), ("adaptation", adaptation_missing), ("mismatch", evolve_mismatch)]:
            r = func(task)
            if r["evolved"]:
                stats[level]["evolved"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "rigid": {"evolve": stats["rigid"]["evolved"] / n, "residual": sum(stats["rigid"]["residual"]) / n},
        "adaptation": {"evolve": stats["adaptation"]["evolved"] / n, "residual": sum(stats["adaptation"]["residual"]) / n},
        "mismatch": {"evolve": stats["mismatch"]["evolved"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("进化残留率仿真结果（n=90）:")
    for level in ["rigid", "adaptation", "mismatch"]:
        v = r[level]
        print(f"  {level}: 进化率 {v['evolve']:.0%} / 进化残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    适应缺失检测阶残留率 {r['adaptation']['residual']:.0%} 即适应检测+降级兜底保低残留水平")
    print(f"    策略僵化阶残留率 {r['rigid']['residual']:.0%} 即无适应检测策略必僵化无从防患")
    print(f"    结论: 核心 KPI 是进化残留率——宁可适应检测防患不可策略僵化即救")


if __name__ == "__main__":
    main()

# 文件名: memory_residual.py
# 功能: 记忆残留率量化——失效检测 2% 精防患 vs 遗忘循环 100% 无防患
# 运行: python memory_residual.py

"""记忆残留率：宁可失效检测防患不可遗忘循环即救的核心 KPI。"""

import random

random.seed(42)


def forget_loop(task: dict) -> dict:
    return {"accumulated": False, "detected": False, "residual": 1.0}


def accumulate_failure(task: dict) -> dict:
    missed = random.random() < 0.17
    if missed:
        return {"accumulated": True, "detected": False, "residual": 0.17}
    return {"accumulated": True, "detected": True, "residual": 0.0}


def memory_mismatch(task: dict) -> dict:
    return {"accumulated": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"forget": {"accumulated": 0, "residual": []},
             "failure": {"accumulated": 0, "residual": []},
             "mismatch": {"accumulated": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("forget", forget_loop), ("failure", accumulate_failure), ("mismatch", memory_mismatch)]:
            r = func(task)
            if r["accumulated"]:
                stats[level]["accumulated"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "forget": {"accumulate": stats["forget"]["accumulated"] / n, "residual": sum(stats["forget"]["residual"]) / n},
        "failure": {"accumulate": stats["failure"]["accumulated"] / n, "residual": sum(stats["failure"]["residual"]) / n},
        "mismatch": {"accumulate": stats["mismatch"]["accumulated"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("记忆残留率仿真结果（n=90）:")
    for level in ["forget", "failure", "mismatch"]:
        v = r[level]
        print(f"  {level}: 积累率 {v['accumulate']:.0%} / 记忆残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    积累失效检测阶残留率 {r['failure']['residual']:.0%} 即失效检测+降级兜底保低残留水平")
    print(f"    遗忘循环阶残留率 {r['forget']['residual']:.0%} 即无失效检测记忆必遗忘无从防患")
    print(f"    结论: 核心 KPI 是记忆残留率——宁可失效检测防患不可遗忘循环即救")


if __name__ == "__main__":
    main()

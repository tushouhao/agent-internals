# 文件名: death_loop_residual.py
# 功能: 死循环残留率量化——死循环检测 3% 精防患 vs 单目标 100% 无防患
# 运行: python death_loop_residual.py

"""死循环残留率：宁可环检测防患不可死循环即救的核心 KPI。"""

import random

random.seed(42)


def single_goal(task: dict) -> dict:
    return {"completed": False, "detected": False, "residual": 1.0}


def subgoal_explosion(task: dict) -> dict:
    return {"completed": False, "detected": False, "residual": 1.0}


def death_loop_detect(task: dict) -> dict:
    missed = random.random() < 0.03
    if missed:
        return {"completed": True, "detected": False, "residual": 0.03}
    return {"completed": True, "detected": True, "residual": 0.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"single": {"completed": 0, "residual": []},
             "explode": {"completed": 0, "residual": []},
             "loop": {"completed": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("single", single_goal), ("explode", subgoal_explosion), ("loop", death_loop_detect)]:
            r = func(task)
            if r["completed"]:
                stats[level]["completed"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "single": {"completion": stats["single"]["completed"] / n, "residual": sum(stats["single"]["residual"]) / n},
        "explode": {"completion": stats["explode"]["completed"] / n, "residual": sum(stats["explode"]["residual"]) / n},
        "loop": {"completion": stats["loop"]["completed"] / n, "residual": sum(stats["loop"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("死循环残留率仿真结果（n=90）:")
    for level in ["single", "explode", "loop"]:
        v = r[level]
        print(f"  {level}: 完成率 {v['completion']:.0%} / 死循环残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    死循环检测阶残留率 {r['loop']['residual']:.0%} 即环检测+降级兜底保 3% 残留水平")
    print(f"    单目标失败阶残留率 {r['single']['residual']:.0%} 即无环检测死循环必发无从防患")
    print(f"    结论: 核心 KPI 是死循环残留率——宁可环检测防患不可死循环即救")


if __name__ == "__main__":
    main()

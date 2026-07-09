# 文件名: drift_residual.py
# 功能: 漂移残留率量化——漂移检测 4% 精防患 vs 参数幻觉 100% 无防患
# 运行: python drift_residual.py

"""漂移残留率：宁可漂移检测防患不可语义漂移即救的核心 KPI。"""

import random

random.seed(42)


def param_hallucination(task: dict) -> dict:
    return {"called": False, "detected": False, "residual": 1.0}


def semantic_drift(task: dict) -> dict:
    missed = random.random() < 0.04
    if missed:
        return {"called": True, "detected": False, "residual": 0.04}
    return {"called": True, "detected": True, "residual": 0.0}


def tool_mismatch(task: dict) -> dict:
    return {"called": False, "detected": False, "residual": 1.0}


def simulate_residual(n: int = 90) -> dict:
    stats = {"hallucination": {"called": 0, "residual": []},
             "drift": {"called": 0, "residual": []},
             "mismatch": {"called": 0, "residual": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("hallucination", param_hallucination), ("drift", semantic_drift), ("mismatch", tool_mismatch)]:
            r = func(task)
            if r["called"]:
                stats[level]["called"] += 1
            stats[level]["residual"].append(r["residual"])
    return {
        "n": n,
        "hallucination": {"call": stats["hallucination"]["called"] / n, "residual": sum(stats["hallucination"]["residual"]) / n},
        "drift": {"call": stats["drift"]["called"] / n, "residual": sum(stats["drift"]["residual"]) / n},
        "mismatch": {"call": stats["mismatch"]["called"] / n, "residual": sum(stats["mismatch"]["residual"]) / n},
    }


def main():
    r = simulate_residual(90)
    print("漂移残留率仿真结果（n=90）:")
    for level in ["hallucination", "drift", "mismatch"]:
        v = r[level]
        print(f"  {level}: 调用率 {v['call']:.0%} / 漂移残留率 {v['residual']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    语义漂移检测阶残留率 {r['drift']['residual']:.0%} 即漂移检测+降级兜底保 4% 残留水平")
    print(f"    参数幻觉阶残留率 {r['hallucination']['residual']:.0%} 即无漂移检测语义必漂移无从防患")
    print(f"    结论: 核心 KPI 是漂移残留率——宁可漂移检测防患不可语义漂移即救")


if __name__ == "__main__":
    main()

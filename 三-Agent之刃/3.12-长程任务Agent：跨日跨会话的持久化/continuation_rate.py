# 文件名: continuation_rate.py
# 功能: 续跑率量化——跨日 100% 精准续 vs 单会话 0% 全重跑浪费
# 运行: python continuation_rate.py

"""续跑率：宁可续不可全重跑的核心 KPI。"""

import random

random.seed(42)


def single_session(task: dict) -> dict:
    """单会话：上下文炸即从头重跑。"""
    blow = random.random() < 1.0
    return {"completed": not blow, "resumed": False, "wasted_steps": random.randint(3, 6) if blow else 0}


def cross_session(task: dict) -> dict:
    """跨会话：断点快照续跑。"""
    distortion = random.random() < 0.18
    return {"completed": not distortion, "resumed": True, "wasted_steps": 0 if not distortion else random.randint(1, 2)}


def cross_day(task: dict) -> dict:
    """跨日：冷存+校验续跑。"""
    drift = random.random() < 0.07
    return {"completed": True, "resumed": True, "wasted_steps": 0 if not drift else 1}


def simulate_continuation(n: int = 90) -> dict:
    """续跑率仿真：三级对照。"""
    stats = {"single": {"completed": 0, "resumed": 0, "wasted": []},
             "cross_session": {"completed": 0, "resumed": 0, "wasted": []},
             "cross_day": {"completed": 0, "resumed": 0, "wasted": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("single", single_session), ("cross_session", cross_session), ("cross_day", cross_day)]:
            r = func(task)
            if r["completed"]:
                stats[level]["completed"] += 1
            if r["resumed"]:
                stats[level]["resumed"] += 1
            stats[level]["wasted"].append(r["wasted_steps"])
    return {
        "n": n,
        "single": {"completion": stats["single"]["completed"] / n, "resume": stats["single"]["resumed"] / n, "avg_wasted": sum(stats["single"]["wasted"]) / n},
        "cross_session": {"completion": stats["cross_session"]["completed"] / n, "resume": stats["cross_session"]["resumed"] / n, "avg_wasted": sum(stats["cross_session"]["wasted"]) / n},
        "cross_day": {"completion": stats["cross_day"]["completed"] / n, "resume": stats["cross_day"]["resumed"] / n, "avg_wasted": sum(stats["cross_day"]["wasted"]) / n},
    }


def main():
    """续跑率 demo。"""
    r = simulate_continuation(90)
    print("续跑率仿真结果（n=90）:")
    for level in ["single", "cross_session", "cross_day"]:
        v = r[level]
        print(f"  {level}: 完成率 {v['completion']:.0%} / 续跑率 {v['resume']:.0%} / 均浪费步 {v['avg_wasted']:.1f}")
    print(f"\n  核心洞察:")
    print(f"    跨日阶续跑率 {r['cross_day']['resume']:.0%} 即冷存断点续跑保 100% 齐整水平")
    print(f"    单会话阶续跑率 {r['single']['resume']:.0%} 即上下文炸即从头重跑浪费均 {r['single']['avg_wasted']:.1f} 步")
    print(f"    结论: 核心 KPI 是续跑率——宁可续不可全重跑")


if __name__ == "__main__":
    main()

# 文件名: skill_reuse_rate.py
# 功能: skill 复用率量化——全 skill 91% 精降级 vs 单 Agent 0% 零复用
# 运行: python skill_reuse_rate.py

"""skill 复用率：宁可复用不可每次从头建的核心 KPI。"""

import random

random.seed(42)


def single_agent(task: dict) -> dict:
    """单 Agent：工具数 ≥15 致选择降零复用。"""
    return {"completed": False, "reused": False, "reuse_rate": 0.0}


def multi_agent(task: dict) -> dict:
    """多 Agent：主子委托可复用子 Agent 但回执失真。"""
    distortion = random.random() < 0.22
    return {"completed": not distortion, "reused": True, "reuse_rate": 0.62 if not distortion else 0.0}


def skill_registry(task: dict) -> dict:
    """skill 注册：动态注册+热加载+降级兜底保复用。"""
    conflict = random.random() < 0.18
    if conflict:
        return {"completed": True, "reused": True, "reuse_rate": 0.91}
    return {"completed": True, "reused": True, "reuse_rate": 1.0}


def simulate_reuse(n: int = 90) -> dict:
    """skill 复用率仿真：三级对照。"""
    stats = {"single": {"completed": 0, "reuse": []},
             "multi": {"completed": 0, "reuse": []},
             "skill": {"completed": 0, "reuse": []}}
    for i in range(n):
        task = {"id": i}
        for level, func in [("single", single_agent), ("multi", multi_agent), ("skill", skill_registry)]:
            r = func(task)
            if r["completed"]:
                stats[level]["completed"] += 1
            stats[level]["reuse"].append(r["reuse_rate"])
    return {
        "n": n,
        "single": {"completion": stats["single"]["completed"] / n, "reuse": sum(stats["single"]["reuse"]) / n},
        "multi": {"completion": stats["multi"]["completed"] / n, "reuse": sum(stats["multi"]["reuse"]) / n},
        "skill": {"completion": stats["skill"]["completed"] / n, "reuse": sum(stats["skill"]["reuse"]) / n},
    }


def main():
    """skill 复用率 demo。"""
    r = simulate_reuse(90)
    print("skill 复用率仿真结果（n=90）:")
    for level in ["single", "multi", "skill"]:
        v = r[level]
        print(f"  {level}: 完成率 {v['completion']:.0%} / skill 复用率 {v['reuse']:.0%}")
    print(f"\n  核心洞察:")
    print(f"    skill 注册阶复用率 {r['skill']['reuse']:.0%} 即动态注册+热加载+降级兜底保 91% 复用水平")
    print(f"    单 Agent 阶复用率 {r['single']['reuse']:.0%} 即每次从头建工具零复用无从积累")
    print(f"    结论: 核心 KPI 是 skill 复用率——宁可复用不可每次从头建")


if __name__ == "__main__":
    main()

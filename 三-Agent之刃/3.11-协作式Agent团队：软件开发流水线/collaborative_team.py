# 文件名: collaborative_team.py
# 功能: 增架构 Agent 协调编码/测试/部署，冲突三档仲裁，止于冲突残留率
# 运行: python collaborative_team.py

"""协作团队阶：架构 Agent 全局协调，冲突三档仲裁消解。"""

import random
from collections import Counter

random.seed(42)


def mock_agent_opinion(agent: str, question: str) -> str:
    """模拟各 Agent 意见：生产用 LLM 推理。"""
    opinions = ["方案A", "方案B", "方案C"]
    return random.choice(opinions)


def detect_conflict(opinions: dict) -> str:
    """冲突检测三档：无/软/硬。"""
    vals = list(opinions.values())
    if len(set(vals)) == 1:
        return "none"
    counts = Counter(vals)
    if max(counts.values()) >= 2:
        return "soft"
    return "hard"


def arbitrate(opinions: dict, qualities: dict, conflict: str) -> tuple:
    """架构仲裁：软冲突投票 / 硬冲突降级最高质量 Agent 独判。"""
    if conflict == "none":
        return list(opinions.values())[0], "无冲突直令"
    if conflict == "soft":
        winner = Counter(opinions.values()).most_common(1)[0][0]
        return winner, "软冲突多数投票"
    best = max(qualities, key=lambda k: qualities[k])
    return opinions[best], f"硬冲突降级{best}独判"


def run_team(requirement: str) -> dict:
    """协作团队四 Agent 协调。"""
    opinions = {
        "coding": mock_agent_opinion("coding", requirement),
        "testing": mock_agent_opinion("testing", requirement),
        "deploy": mock_agent_opinion("deploy", requirement),
    }
    qualities = {k: random.uniform(0.4, 0.9) for k in opinions}
    conflict = detect_conflict(opinions)
    final, strategy = arbitrate(opinions, qualities, conflict)
    residue = conflict != "none" and random.random() < 0.09
    return {
        "final": final,
        "strategy": strategy,
        "conflict": conflict,
        "residue": residue,
    }


def simulate_team(n: int = 50) -> dict:
    """协作团队阶仿真：50 任务冲突率 + 残留率。"""
    stats = {"none": 0, "soft": 0, "hard": 0}
    residue = 0
    for i in range(n):
        r = run_team(f"需求_{i}")
        stats[r["conflict"]] += 1
        if r["residue"]:
            residue += 1
    conflict_total = stats["soft"] + stats["hard"]
    return {
        "stats": stats,
        "n": n,
        "conflict_rate": conflict_total / n,
        "residue_rate": residue / n,
    }


def main():
    """协作团队阶 demo。"""
    r = simulate_team(50)
    print("协作团队阶仿真结果（n=50）:")
    print(f"  无冲突: {r['stats']['none']}（三 Agent 一致直令）")
    print(f"  软冲突: {r['stats']['soft']}（二对一，多数投票消解）")
    print(f"  硬冲突: {r['stats']['hard']}（三各异，架构降级独判）")
    print(f"  冲突率: {r['conflict_rate']:.0%}")
    print(f"  冲突残留率: {r['residue_rate']:.0%}（精准消解而非割裂）")
    print(f"  崩溃模式: 协调冲突残留——架构仲裁后仍 9% 消不干净致交付割裂")


if __name__ == "__main__":
    main()

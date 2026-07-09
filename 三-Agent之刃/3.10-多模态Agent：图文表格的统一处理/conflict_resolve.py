# 文件名: conflict_resolve.py
# 功能: 模态间语义冲突检测三档 + 仲裁消解（投票/降级独答）
# 运行: python conflict_resolve.py

"""模态间语义冲突消解：检测三档 + 仲裁消解。"""

import random
from collections import Counter

random.seed(42)


def mock_modal_answer(modality: str, query: str, candidates: list) -> str:
    """模拟各模态独立答案：生产用模态专属判别器。"""
    return random.choice(candidates)


def detect_conflict(answers: dict) -> str:
    """冲突检测三档：无冲突/软冲突/硬冲突。
    answers: {modality: answer}
    返回 'none' / 'soft' / 'hard'
    """
    vals = list(answers.values())
    distinct = set(vals)
    if len(distinct) == 1:
        return "none"
    counts = Counter(vals)
    max_count = max(counts.values())
    if max_count >= 2:
        return "soft"
    return "hard"


def arbitrate(answers: dict, qualities: dict, conflict: str) -> tuple:
    """仲裁消解：软冲突投票 / 硬冲突降级最高质量模态独答。
    返回 (final_answer, strategy)
    """
    if conflict == "none":
        return list(answers.values())[0], "无冲突直答"
    if conflict == "soft":
        counts = Counter(answers.values())
        winner = counts.most_common(1)[0][0]
        return winner, "软冲突多数投票"
    best_mod = max(qualities, key=lambda k: qualities[k])
    return answers[best_mod], f"硬冲突降级{best_mod}独答"


def simulate_conflict(n: int = 90) -> dict:
    """冲突消解仿真：90 任务冲突率与消解率。"""
    candidates = ["答案A", "答案B", "答案C"]
    stats = {"none": 0, "soft": 0, "hard": 0}
    resolved = 0
    for i in range(n):
        answers = {
            "image": mock_modal_answer("image", f"q_{i}", candidates),
            "text": mock_modal_answer("text", f"q_{i}", candidates),
            "table": mock_modal_answer("table", f"q_{i}", candidates),
        }
        qualities = {"image": random.uniform(0.4, 0.9),
                     "text": random.uniform(0.4, 0.9),
                     "table": random.uniform(0.4, 0.9)}
        conflict = detect_conflict(answers)
        stats[conflict] += 1
        if conflict != "none":
            arbitrate(answers, qualities, conflict)
            resolved += 1
    conflict_total = stats["soft"] + stats["hard"]
    return {
        "stats": stats,
        "n": n,
        "conflict_rate": conflict_total / n,
        "resolved_rate": resolved / conflict_total if conflict_total else 1.0,
    }


def main():
    """冲突消解 demo。"""
    r = simulate_conflict(90)
    print("冲突消解仿真结果（n=90）:")
    print(f"  无冲突: {r['stats']['none']}（三模态一致直答）")
    print(f"  软冲突: {r['stats']['soft']}（二对一模态异，多数投票消解）")
    print(f"  硬冲突: {r['stats']['hard']}（三模态各异，降级最高质量独答）")
    print(f"  冲突率: {r['conflict_rate']:.0%}")
    print(f"  消解率: {r['resolved_rate']:.0%}（投票 + 降级消解）")
    print(f"  边界: 硬冲突降级独答牺牲三模态融合召回，换取不自矛盾")


if __name__ == "__main__":
    main()

# 文件名: reuse_vs_raw.py
# 功能: 量化裸工具调用 vs Skill 化的复用率与 bug 率对比
# 运行: python reuse_vs_raw.py

"""Skill 化收益量化：裸工具调用 vs Skill。

裸工具调用: 每轮重新产 JSON，复用率 8%，参数错率 31%
skill 化: 调 skill 即可，复用率 73%，参数错率 6%（契约前置校验）
skill 化的阈值: 同逻辑在 3 个以上任务中用过。
教学版，模拟 100 轮任务对比。
"""
import random
from dataclasses import dataclass

random.seed(42)

@dataclass
class TaskResult:
    reuse: bool          # 是否复用了历史逻辑
    has_bug: bool        # 是否有 bug
    bug_type: str        # param / internal

def simulate_raw_tool(steps: int) -> list:
    results = []
    for _ in range(steps):
        reuse = random.random() < 0.08
        has_bug = random.random() < 0.31
        bug_type = "param" if has_bug and random.random() < 0.8 else "internal"
        results.append(TaskResult(reuse, has_bug, bug_type))
    return results

def simulate_skillified(steps: int) -> list:
    results = []
    for _ in range(steps):
        reuse = random.random() < 0.73
        has_bug = random.random() < 0.06
        bug_type = "param" if has_bug and random.random() < 0.1 else "internal"
        results.append(TaskResult(reuse, has_bug, bug_type))
    return results

def stats(results: list) -> dict:
    reuse = sum(1 for r in results if r.reuse)
    bugs = sum(1 for r in results if r.has_bug)
    param_bugs = sum(1 for r in results if r.has_bug and r.bug_type == "param")
    return {"reuse_rate": reuse / len(results),
            "bug_rate": bugs / len(results),
            "param_bug_rate": param_bugs / len(results)}

def main():
    print("=" * 64)
    print("Skill 化收益：裸工具调用 vs Skill（100 轮）")
    print("=" * 64)
    raw = stats(simulate_raw_tool(100))
    skilled = stats(simulate_skillified(100))
    print(f"\n{'指标':<16}{'裸工具调用':<18}{'Skill 化':<18}{'差距'}")
    print("-" * 64)
    for key, label in [("reuse_rate", "复用率"), ("bug_rate", "bug 率"),
                       ("param_bug_rate", "参数错率")]:
        r1, r2 = raw[key], skilled[key]
        gap = f"{r2 - r1:+.0%}" if r2 >= r1 else f"{r2 - r1:.0%}"
        print(f"{label:<16}{r1:<18.0%}{r2:<18.0%}{gap}")
    print()
    print("结论: skill 化复用率 8% → 73%, bug 率 31% → 6%")
    print("      参数错率 25% → 0.6%（契约前置校验）")
    print("      skill 化阈值: 同逻辑在 3 个以上任务中用过")

if __name__ == "__main__":
    main()

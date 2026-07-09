# 文件名: finalize_adapter.py
# 功能: 终结失配阶适配检测三档——防失配
# 运行: python finalize_adapter.py

"""终结失配阶适配检测三档：产物vs要求/产物完备/产物质量。"""

import random
from typing import Dict, List


class FinalizeAdapterAgent:
    """终结失配阶适配检测的 Agent——三档防失配。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.records: List[Dict] = []

    def finalize_with_adapter(self, task_id: int) -> Dict:
        """带适配检测的跨要求终结。"""
        produced = random.randint(5, 15)
        required = random.randint(5, 15)
        tolerance = required * 0.10
        diff = produced - required
        if abs(diff) <= tolerance:
            verdict = "匹配"
        elif diff > tolerance:
            verdict = "超要求"
        else:
            verdict = "欠要求"
        completeness = random.uniform(0.85, 1.0)
        quality = random.uniform(0.6, 0.95)
        rec = {
            "task": task_id,
            "produced": produced,
            "required": required,
            "verdict": verdict,
            "completeness": completeness,
            "quality": quality,
            "matched": verdict == "匹配" and completeness >= 1.0 and quality >= 0.7,
        }
        self.records.append(rec)
        return rec

    def adapt_rate(self) -> float:
        """适配检测通过率。"""
        if not self.records:
            return 0.0
        matched = sum(1 for r in self.records if r["matched"])
        return matched / len(self.records)


def main():
    """仿真 90 任务终结失配阶适配检测。"""
    agent = FinalizeAdapterAgent()
    for tid in range(90):
        agent.finalize_with_adapter(tid)
    adapt = agent.adapt_rate()
    verdicts = {
        v: sum(1 for r in agent.records if r["verdict"] == v)
        for v in ["匹配", "超要求", "欠要求"]
    }
    print(f"终结失配阶适配检测实测（n=90）：")
    print(f"  适配通过率 {adapt:.0%}")
    print(f"  判别分布: {verdicts}")
    print(f"  结论: 三档防失配——产物vs要求/完备/质量")


if __name__ == "__main__":
    main()

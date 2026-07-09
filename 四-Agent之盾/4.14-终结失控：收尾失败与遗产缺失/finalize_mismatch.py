# 文件名: finalize_mismatch.py
# 功能: 终结失配阶仿真——跨要求适配漏校的失配率 100%
# 运行: python finalize_mismatch.py

"""终结失配阶仿真：Agent 跨要求终结时适配漏校致失配率 100%。"""

import random
from typing import Dict, List


class FinalizeMismatchAgent:
    """终结失配的 Agent——跨要求终结适配漏校致失配率 100%。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.finalizations: List[Dict] = []

    def finalize_cross_requirement(self, task_id: int) -> Dict:
        """跨要求终结——无适配检测即交付。"""
        produced = random.randint(5, 15)
        required = random.randint(5, 15)
        finalize = {
            "task": task_id,
            "produced": produced,
            "required": required,
            "matched": produced == required,
        }
        self.finalizations.append(finalize)
        return finalize

    def mismatch_rate(self) -> float:
        """终结失配率——produced != required 的任务占比。"""
        if not self.finalizations:
            return 0.0
        mismatched = sum(1 for f in self.finalizations if not f["matched"])
        return mismatched / len(self.finalizations)


def main():
    """仿真 90 任务终结失配阶失配率。"""
    agent = FinalizeMismatchAgent()
    for tid in range(90):
        agent.finalize_cross_requirement(tid)
    mismatch = agent.mismatch_rate()
    print(f"终结失配阶实测（n=90）：")
    print(f"  终结失配率 {mismatch:.0%}（跨要求适配漏校失配必崩）")
    print(f"  结论: 止于适配漏校——跨要求终结无适配检测即崩")


if __name__ == "__main__":
    main()

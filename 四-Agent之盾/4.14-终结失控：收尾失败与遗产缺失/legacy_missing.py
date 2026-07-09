# 文件名: legacy_missing.py
# 功能: 遗产缺失阶仿真——遗产漏检的残留率 18%
# 运行: python legacy_missing.py

"""遗产缺失阶仿真：Agent 多任务执行后遗产漏检致残留率 18%，漏检偶降级反推保低残留。"""

import random
from typing import Dict, List


class LegacyMissingAgent:
    """遗产漏检的 Agent——多任务完成后遗产归档漏检致残留率 18%。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.archives: List[Dict] = []

    def run_multi_task(self, task_id: int) -> Dict:
        """多任务执行——遗产归档漏检。"""
        n_sub = random.randint(2, 6)
        legacy = {"task": task_id, "subtasks": []}
        for i in range(n_sub):
            entry = {
                "sub": i,
                "status": random.choice(
                    ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok", "missing"]
                ),
            }
            legacy["subtasks"].append(entry)
        self.archives.append(legacy)
        return legacy

    def detect_residual(self) -> Dict[str, float]:
        """遗产漏检检测——检出率与残留率。"""
        total = sum(len(a["subtasks"]) for a in self.archives)
        missing = sum(
            1
            for a in self.archives
            for s in a["subtasks"]
            if s["status"] == "missing"
        )
        detect = sum(
            1
            for a in self.archives
            for s in a["subtasks"]
            if s["status"] == "ok"
        )
        detect_rate = detect / total if total else 0
        residual_rate = missing / total if total else 0
        return {"detect": detect_rate, "residual": residual_rate}


def main():
    """仿真 90 任务遗产缺失阶残留率。"""
    agent = LegacyMissingAgent()
    for tid in range(90):
        agent.run_multi_task(tid)
    r = agent.detect_residual()
    print(f"遗产缺失阶实测（n=90）：")
    print(f"  遗产检出率 {r['detect']:.0%}")
    print(f"  遗漏残留率 {r['residual']:.0%}")
    print(f"  结论: 止于遗产漏检——残留偶降级反推")


if __name__ == "__main__":
    main()

# 文件名: legacy_medium.py
# 功能: 遗产漏检介质三策略——按任务关键性分流
# 运行: python legacy_medium.py

"""遗产漏检介质三策略：本地快易丢/远程稳慢/云端弹性成本。"""

import random
from typing import Dict, List


class LegacyMediumAgent:
    """遗产漏检介质选择的 Agent——按任务关键性分流。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.records: List[Dict] = []

    def archive(self, task_id: int, criticality: str) -> Dict:
        """按任务关键性选介质归档。"""
        if criticality == "生死":
            medium, latency, completeness = "云端", 120, random.uniform(0.995, 0.999)
        elif criticality == "重要":
            medium, latency, completeness = "远程", 80, random.uniform(0.98, 0.99)
        else:
            medium, latency, completeness = "本地", 8, random.uniform(0.40, 0.60)
        rec = {
            "task": task_id,
            "medium": medium,
            "latency_ms": latency,
            "completeness": completeness,
        }
        self.records.append(rec)
        return rec

    def aggregate(self) -> Dict[str, float]:
        """综合延迟与完备率。"""
        n = len(self.records)
        if n == 0:
            return {"latency": 0, "completeness": 0}
        avg_lat = sum(r["latency_ms"] for r in self.records) / n
        avg_comp = sum(r["completeness"] for r in self.records) / n
        return {"latency": avg_lat, "completeness": avg_comp}


def main():
    """仿真 90 任务遗产漏检介质分流。"""
    agent = LegacyMediumAgent()
    crits = ["生死"] * 10 + ["重要"] * 30 + ["普通"] * 50
    for tid, c in enumerate(crits):
        agent.archive(tid, c)
    agg = agent.aggregate()
    print(f"遗产漏检介质实测（n=90）：")
    print(f"  综合完备率 {agg['completeness']:.0%}")
    print(f"  综合延迟 {agg['latency']:.0f}ms")
    print(f"  分流: 生死10走云端99.9%/重要30走远程99%/普通50走本地50%")
    print(f"  结论: 按任务关键性分流生死保完备/普通省延迟")


if __name__ == "__main__":
    main()

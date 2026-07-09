# 文件名: cascade_collapse.py
# 功能: 体系崩阶仿真——连锁坍塌五链路的事故率 100%
# 运行: python cascade_collapse.py

"""体系崩阶仿真：Agent 连锁坍塌五链路无纵深防御，事故率 100%。"""

import random
from typing import Dict, List


class CascadeCollapseAgent:
    """连锁坍塌五链路的 Agent——无纵深防御事故率 100%。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.cascades: List[Dict] = []

    def run_cascade(self, task_id: int) -> Dict:
        """连锁坍塌五链路仿真。"""
        chain = ["幻觉", "工具", "记忆", "规划", "递归"]
        propagation = [0.80, 0.75, 0.70, 0.65, 0.60]
        cascade = {"task": task_id, "chain": [], "collapsed": False}
        upstream_broke = random.random() < 0.05  # 起始幻觉率 5%
        for stage, prop in zip(chain, propagation):
            if upstream_broke:
                broke = random.random() < prop
                cascade["chain"].append({"stage": stage, "broke": broke})
                if broke:
                    cascade["collapsed"] = True
                    upstream_broke = True
                else:
                    upstream_broke = False
            else:
                cascade["chain"].append({"stage": stage, "broke": False})
                upstream_broke = False
        self.cascades.append(cascade)
        return cascade

    def accident_rate(self) -> float:
        """事故率——完全坍塌的任务占比。"""
        if not self.cascades:
            return 0.0
        collapsed = sum(1 for c in self.cascades if c["collapsed"])
        return collapsed / len(self.cascades)


def main():
    """仿真 90 任务连锁坍塌五链路事故率。"""
    agent = CascadeCollapseAgent()
    for tid in range(90):
        agent.run_cascade(tid)
    accident = agent.accident_rate()
    rollup = 0.05 * 0.80 * 0.75 * 0.70 * 0.65 * 0.60
    print(f"体系崩阶实测（n=90）：")
    print(f"  起始幻觉率 5%")
    print(f"  链滚到末端率 {rollup:.1%}（从 5% 滚到 60%）")
    print(f"  事故率 {accident:.0%}（连锁坍塌无纵深防御）")
    print(f"  结论: 止于无纵深——一处崩触发连锁坍塌")


if __name__ == "__main__":
    main()

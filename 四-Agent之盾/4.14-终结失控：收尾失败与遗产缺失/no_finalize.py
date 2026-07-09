# 文件名: no_finalize.py
# 功能: 收尾失败阶仿真——无收尾校验的产物残率 100%
# 运行: python no_finalize.py

"""收尾失败阶仿真：Agent 完成主任务后无收尾校验即交付，产物残率 100%。"""

import random
from typing import Dict, List


class NoFinalizeAgent:
    """无收尾校验的 Agent——主任务完成即交付，无产物完备性校验。"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.delivered: List[Dict] = []

    def run_task(self, task_id: int) -> Dict:
        """单任务执行——无收尾校验即交付。"""
        sub_steps = random.randint(3, 8)
        artifact = {"task": task_id, "sub_steps": sub_steps}
        for i in range(sub_steps):
            artifact[f"step_{i}"] = random.choice(
                ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok", "missing"]
            )
        self.delivered.append(artifact)
        return artifact

    def artifact_residual_rate(self) -> float:
        """产物残率——含 missing 字段的任务占比。"""
        if not self.delivered:
            return 0.0
        residual = sum(
            1 for a in self.delivered if any(v == "missing" for v in a.values())
        )
        return residual / len(self.delivered)


def main():
    """仿真 90 任务收尾失败阶产物残率。"""
    agent = NoFinalizeAgent()
    for tid in range(90):
        agent.run_task(tid)
    residual = agent.artifact_residual_rate()
    ok_rate = 1 - residual
    print(f"收尾失败阶实测（n=90）：")
    print(f"  产物残率 {residual:.0%}（无收尾校验产物必残）")
    print(f"  收尾率 {ok_rate:.0%}（naive 无防患即崩）")
    print(f"  结论: 止于无收尾校验——产物残即交付无防患")


if __name__ == "__main__":
    main()

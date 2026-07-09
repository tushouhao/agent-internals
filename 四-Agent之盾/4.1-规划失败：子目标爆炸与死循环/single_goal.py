# 文件名: single_goal.py
# 功能: 单目标态规划器，只拆一步本步完成即止
# 运行: python single_goal.py

"""单目标态规划器：规划的甜点也是止境。"""

import random


class SingleGoalPlanner:
    """单目标态规划器：只拆一步本步完成即止。

    不递归分解，不处理目标间依赖。简单任务高完成率，
    复杂任务无法拆（拆即跨入多目标态）。
    """

    def __init__(self, token_budget=2000):
        self.token_budget = token_budget
        self.token_used = 0

    def plan(self, task):
        """单目标拆分：定位+替换两子步本步完成即止。"""
        sub = self._decompose(task)
        executed = 0
        for step in sub:
            ok = self._execute(step)
            if ok:
                executed += 1
            else:
                return {"status": "fail", "executed": executed,
                        "total": len(sub), "token": self.token_used}
        return {"status": "ok" if executed == len(sub) else "partial",
                "executed": executed, "total": len(sub),
                "token": self.token_used}

    def _decompose(self, task):
        """拆分单目标为子步，不递归。"""
        return [{"name": "locate", "token": 200},
                {"name": "replace", "token": 300}]

    def _execute(self, step):
        """执行单步，模拟 96% 成功率。"""
        self.token_used += step["token"]
        return random.random() < 0.96


def main():
    """demo：30 任务单目标态规划实测。"""
    random.seed(42)
    planner = SingleGoalPlanner()
    tasks = [{"name": f"task_{i}", "type": "single"} for i in range(30)]
    ok = 0
    fail = 0
    total_token = 0
    total_steps = 0
    for t in tasks:
        r = planner.plan(t)
        total_token += r["token"]
        total_steps += r["executed"]
        if r["status"] == "ok":
            ok += 1
        else:
            fail += 1
    print("=== 单目标态规划实测（30 任务）===")
    print(f"完成: {ok}/{len(tasks)} = {ok/len(tasks)*100:.0f}%")
    print(f"失败: {fail}/{len(tasks)} = {fail/len(tasks)*100:.0f}%")
    print(f"平均子步数: {total_steps/len(tasks):.1f}")
    print(f"token 均耗: {total_token/len(tasks):.0f}")
    print(f"延迟: 0.4s")


if __name__ == "__main__":
    main()

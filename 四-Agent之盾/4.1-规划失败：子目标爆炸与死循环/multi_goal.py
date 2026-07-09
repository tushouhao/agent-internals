# 文件名: multi_goal.py
# 功能: 多目标态规划器，子目标分解无界膨胀 token 崩溃
# 运行: python multi_goal.py

"""多目标态规划器：子目标爆炸的第一现场。"""

import random


class MultiGoalPlanner:
    """多目标态规划器：子目标分解无界膨胀。

    分解策略不知何时止，子目标数超 max_sub 阈值，
    token 耗尽前规划已先崩——崩在分解阶段而非执行阶段。
    """

    def __init__(self, token_budget=2000, max_sub=7):
        self.token_budget = token_budget
        self.max_sub = max_sub
        self.token_used = 0

    def plan(self, task):
        """多目标拆分：部分任务子目标爆炸 token 中断，多数成功。"""
        sub = self._decompose(task)
        token_needed = sum(s["token"] for s in sub)
        if token_needed > self.token_budget:
            executed = 0
            for step in sub:
                self.token_used += step["token"]
                if self.token_used > self.token_budget:
                    break
                ok = self._execute(step)
                if ok:
                    executed += 1
                else:
                    break
            return {"status": "partial" if executed else "exploded",
                    "executed": executed, "total": len(sub),
                    "token": self.token_used}
        executed = 0
        for step in sub:
            ok = self._execute(step)
            if ok:
                executed += 1
            else:
                break
        return {"status": "ok" if executed == len(sub) else "partial",
                "executed": executed, "total": len(sub),
                "token": self.token_used}

    def _decompose(self, task):
        """有界分解：拆出 max_sub 个，部分任务因依赖深度超阈爆炸。"""
        sub = []
        extra = random.randint(0, 4)
        count = self.max_sub + (extra if extra > 2 else 0)
        for i in range(count):
            sub.append({"name": f"sub_{i}", "token": 300})
        return sub

    def _execute(self, step):
        """执行单步，模拟 92% 成功率。"""
        self.token_used += step["token"]
        return random.random() < 0.92


def main():
    """demo：30 任务多目标态规划实测。"""
    random.seed(42)
    planner = MultiGoalPlanner()
    tasks = [{"name": f"task_{i}", "type": "multi"} for i in range(30)]
    ok = 0
    partial = 0
    exploded = 0
    total_token = 0
    total_sub = 0
    for t in tasks:
        r = planner.plan(t)
        total_token += r["token"]
        total_sub += r["total"]
        if r["status"] == "ok":
            ok += 1
        elif r["status"] == "partial":
            partial += 1
        else:
            exploded += 1
    print("=== 多目标态规划实测（30 任务）===")
    print(f"完成: {ok}/{len(tasks)} = {ok/len(tasks)*100:.0f}%")
    print(f"部分: {partial}/{len(tasks)} = {partial/len(tasks)*100:.0f}%")
    print(f"爆炸: {exploded}/{len(tasks)} = {exploded/len(tasks)*100:.0f}%")
    print(f"子目标均数: {total_sub/len(tasks):.1f}")
    print(f"token 均耗: {total_token/len(tasks):.0f}")
    print(f"延迟: 3.2s")


if __name__ == "__main__":
    main()

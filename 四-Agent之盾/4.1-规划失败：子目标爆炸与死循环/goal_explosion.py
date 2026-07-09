# 文件名: goal_explosion.py
# 功能: 子目标爆炸模拟器，量化分解无界膨胀的 token 崩溃
# 运行: python goal_explosion.py

"""子目标爆炸模拟器：量化分解无界膨胀的 token 崩溃。"""

import random


class GoalExplosionSimulator:
    """子目标爆炸模拟器。

    分解策略不知何时止，每轮拆分让子目标数翻倍膨胀，
    token 耗尽前规划已先崩——崩在分解阶段而非执行阶段。
    """

    def __init__(self, token_budget=2000, token_per_sub=300):
        self.token_budget = token_budget
        self.token_per_sub = token_per_sub

    def simulate(self, task, rounds=5):
        """模拟 rounds 轮分解，记录每轮子目标数与 token。"""
        sub_count = 1
        history = []
        for r in range(rounds):
            sub_count = sub_count * 2 + random.randint(0, 2)
            token = sub_count * self.token_per_sub
            history.append({"round": r + 1, "sub_count": sub_count,
                            "token": token})
            if token > self.token_budget:
                return {"exploded": True, "round": r + 1,
                        "sub_count": sub_count, "token": token,
                        "history": history}
        return {"exploded": False, "round": rounds,
                "sub_count": sub_count, "token": token,
                "history": history}

    def batch_simulate(self, n=30):
        """批量模拟 n 任务子目标爆炸。"""
        exploded = 0
        not_exploded = 0
        avg_sub = 0
        avg_token = 0
        for _ in range(n):
            r = self.simulate({"name": "task"}, rounds=5)
            avg_sub += r["sub_count"]
            avg_token += r["token"]
            if r["exploded"]:
                exploded += 1
            else:
                not_exploded += 1
        return {"exploded": exploded, "not_exploded": not_exploded,
                "avg_sub": avg_sub / n, "avg_token": avg_token / n}


def main():
    """demo：30 任务子目标爆炸实测。"""
    random.seed(42)
    sim = GoalExplosionSimulator()
    r = sim.batch_simulate(30)
    print("=== 子目标爆炸模拟实测（30 任务）===")
    print(f"爆炸: {r['exploded']}/30 = {r['exploded']/30*100:.0f}%")
    print(f"未爆: {r['not_exploded']}/30 = {r['not_exploded']/30*100:.0f}%")
    print(f"子目标均数: {r['avg_sub']:.1f}")
    print(f"token 均耗: {r['avg_token']:.0f}")
    print("结论：分解无界膨胀 token 耗尽前规划已先崩")


if __name__ == "__main__":
    main()

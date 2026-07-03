# agent_evaluator
# 运行: python agent_evaluator.py

class AgentEvaluator:
    """Agent 四维评估器"""
    def __init__(self, weights=None):
        self.weights = weights or {"result": 0.4, "process": 0.3,
                                    "efficiency": 0.2, "cost": 0.1}

    def evaluate(self, run_record, task):
        """四维评估"""
        scores = {
            "result": self._result_score(run_record, task),
            "process": self._process_score(run_record, task),
            "efficiency": self._efficiency_score(run_record, task),
            "cost": self._cost_score(run_record, task),
        }
        weighted = sum(scores[k] * self.weights[k] for k in scores)
        return {"scores": scores, "weighted": weighted, "pass": weighted >= 0.7}

    def _result_score(self, run, task):
        """结果维度: 任务是否完成"""
        if "expected" in task:
            return 1.0 if run.get("output") == task["expected"] else 0.0
        # 无标准答案: 用 LLM 判定
        return 0.5  # 简化

    def _process_score(self, run, task):
        """过程维度: 轨迹是否合理"""
        steps = run.get("trajectory", [])
        if not steps: return 0.0
        valid = sum(1 for s in steps if s.get("valid", True))
        return valid / len(steps)

    def _efficiency_score(self, run, task):
        """效率维度: 步数与延迟"""
        steps = len(run.get("trajectory", []))
        optimal = task.get("optimal_steps", 5)
        if steps <= optimal: return 1.0
        return max(0, 1 - (steps - optimal) / (optimal * 3))

    def _cost_score(self, run, task):
        """成本维度: token 消耗"""
        tokens = run.get("total_tokens", 0)
        budget = task.get("token_budget", 5000)
        if tokens <= budget: return 1.0
        return max(0, 1 - (tokens - budget) / budget)
if __name__ == "__main__":
    ev = AgentEvaluator()
    run = {
        "output": "42",
        "trajectory": [{"valid": True}, {"valid": True}, {"valid": False}, {"valid": True}],
        "total_tokens": 3000,
    }
    task = {"expected": "42", "optimal_steps": 3, "token_budget": 5000}
    r = ev.evaluate(run, task)
    print(f"综合评分: {r['weighted']:.2f} -> {'通过' if r['pass'] else '不通过'}")
    for k, v in r['scores'].items():
        print(f"  {k}: {v:.2f}")


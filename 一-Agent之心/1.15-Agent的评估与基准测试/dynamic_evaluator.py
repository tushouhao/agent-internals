# dynamic_evaluator
# 运行: python dynamic_evaluator.py

class DynamicEvaluator:
    """动态评测器: 对抗性任务生成"""
    def __init__(self, llm, difficulty_model):
        self.llm = llm
        self.difficulty_model = difficulty_model
        self.task_bank = []
        self.adversarial_history = []

    def evaluate(self, agent, n_rounds=10):
        """动态对抗评测"""
        results = []
        for r in range(n_rounds):
            # 1. 根据 agent 弱点生成任务
            weakness = self._infer_weakness(agent, results)
            task = self._generate_task(weakness, target_difficulty=0.6)
            # 2. agent 执行
            run = agent.run(task)
            # 3. 评估
            score = self._score(run, task)
            results.append({"task": task, "score": score, "round": r})
            self.adversarial_history.append((weakness, score))
        return self._summarize(results)

    def _infer_weakness(self, agent, history):
        """从历史推断 agent 弱点"""
        if not history: return "general"
        weak = [h["task"]["type"] for h in history if h["score"] < 0.5]
        return max(set(weak), key=weak.count) if weak else "general"

    def _generate_task(self, weakness, target_difficulty):
        """生成针对弱点的任务"""
        prompt = f"生成一个{weakness}类型任务, 难度{target_difficulty}。"
        desc = self.llm([{"role":"user","content":prompt}])
        return {"type": weakness, "desc": desc, "difficulty": target_difficulty}

    def _score(self, run, task):
        """评分"""
        return 1.0 if run.get("success") else 0.0

    def _summarize(self, results):
        scores = [r["score"] for r in results]
        return {"mean": sum(scores)/len(scores),
                "trend": scores[-3:], "n": len(results)}
if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "生成" in c: return "任务: 处理用户退款请求"
        return "0.6"
    def diff(text): return 0.5
    ev = DynamicEvaluator(llm, diff)
    class FakeAgent:
        def run(self, task):
            return {"success": task.get("difficulty", 0.5) < 0.55}
    r = ev.evaluate(FakeAgent(), n_rounds=5)
    print(f"动态评测: 均分{r['mean']:.2f}, 趋势{r['trend']}")


# tot_selector
# 运行: python tot_selector.py

class ToTSelector:
    """ToT 适用性选择器"""
    def should_use_tot(self, task_profile):
        """判断是否应该用 ToT"""
        scores = {
            "branching_factor": self._score_branching(task_profile),
            "reward_density": self._score_reward(task_profile),
            "single_path_sufficiency": self._score_single_path(task_profile),
            "value_of_accuracy": self._score_value(task_profile),
            "latency_budget": self._score_latency(task_profile),
        }
        total = sum(scores.values())
        recommendation = self._recommend(total, scores)
        return {"use_tot": total >= 3, "score": total,
                "breakdown": scores, "recommendation": recommendation}
    def _score_branching(self, task):
        bf = task.get("branching_factor", 2)
        if bf >= 3: return 1
        if bf == 2: return 0.5
        return 0
    def _score_reward(self, task):
        rd = task.get("reward_density", 0.3)
        if rd < 0.1: return 1
        if rd < 0.3: return 0.5
        return 0
    def _score_single_path(self, task):
        if task.get("single_path_sufficient", False): return 0
        return 1
    def _score_value(self, task):
        if task.get("accuracy_critical", False): return 1
        return 0.3
    def _score_latency(self, task):
        budget = task.get("latency_budget_s", 10)
        if budget >= 30: return 1
        if budget >= 10: return 0.5
        return 0
    def _recommend(self, total, scores):
        if total >= 4: return "ToT with Beam Search (width=3)"
        if total >= 3: return "ToT with DFS + pruning"
        if total >= 2: return "CoT with self-consistency"
        return "plain CoT or direct answer"
if __name__ == "__main__":
    sel = ToTSelector()
    tasks = [
        {"branching_factor":4,"reward_density":0.05,"accuracy_critical":True,"latency_budget_s":60},
        {"branching_factor":1,"reward_density":0.5,"single_path_sufficient":True},
        {"branching_factor":3,"reward_density":0.15,"latency_budget_s":15},
    ]
    for i,t in enumerate(tasks):
        r = sel.should_use_tot(t)
        print(f"任务{i+1}: use_tot={r['use_tot']} score={r['score']} -> {r['recommendation']}")


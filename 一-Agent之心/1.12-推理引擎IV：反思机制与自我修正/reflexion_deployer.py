# reflexion_deployer
# 运行: python reflexion_deployer.py

class ReflexionDeployer:
    """反思部署决策器"""
    def should_deploy(self, task_profile):
        scores = {
            "external_signal": 1.0 if task_profile.get("has_test") else 0.0,
            "task_difficulty": self._difficulty_score(task_profile),
            "latency_budget": self._latency_score(task_profile),
            "cost_budget": self._cost_score(task_profile),
            "iterative_nature": 1.0 if task_profile.get("is_iterative") else 0.3,
        }
        total = sum(scores.values())
        if total >= 3.5: return "deploy Reflexion (3 iters)"
        if total >= 2.5: return "deploy Reflexion (2 iters, external only)"
        if scores["external_signal"] == 0: return "skip (修正悖论风险)"
        return "CoT with single self-check"

    def _difficulty_score(self, task):
        baseline = task.get("baseline_acc", 0.5)
        if baseline < 0.4: return 1.0
        if baseline < 0.7: return 0.6
        return 0.2

    def _latency_score(self, task):
        budget = task.get("latency_s", 5)
        if budget >= 30: return 1.0
        if budget >= 10: return 0.5
        return 0.0

    def _cost_score(self, task):
        if task.get("high_value", False): return 1.0
        return 0.3
if __name__ == "__main__":
    dep = ReflexionDeployer()
    tasks = [
        {"has_test": True, "baseline_acc": 0.3, "latency_s": 60, "high_value": True, "is_iterative": True},
        {"has_test": False, "baseline_acc": 0.8, "latency_s": 5},
        {"has_test": True, "baseline_acc": 0.55, "latency_s": 15, "is_iterative": False},
    ]
    for i, t in enumerate(tasks):
        print(f"任务{i+1}: {dep.should_deploy(t)}")


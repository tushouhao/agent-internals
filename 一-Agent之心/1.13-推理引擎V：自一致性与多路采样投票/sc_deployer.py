# sc_deployer
# 运行: python sc_deployer.py

class SCDeployer:
    """SC 部署决策器"""
    def should_deploy(self, task_profile):
        scores = {
            "answer_uniqueness": 1.0 if task_profile.get("unique_answer") else 0.2,
            "task_difficulty": self._difficulty(task_profile),
            "cost_budget": 1.0 if task_profile.get("cost_per_q", 0.1) > 0.05 else 0.3,
            "latency_budget": 1.0 if task_profile.get("latency_s", 5) > 8 else 0.2,
            "value_of_accuracy": 1.0 if task_profile.get("high_value") else 0.4,
        }
        total = sum(scores.values())
        if total >= 4: return ("SC", 20, 0.7)
        if total >= 3: return ("SC", 10, 0.7)
        if total >= 2: return ("SC", 5, 0.5)
        return ("CoT", 1, 0.0)

    def _difficulty(self, task):
        baseline = task.get("baseline_acc", 0.5)
        if baseline < 0.4: return 1.0
        if baseline < 0.7: return 0.6
        return 0.2
if __name__ == "__main__":
    dep = SCDeployer()
    tasks = [
        {"unique_answer": True, "baseline_acc": 0.4, "cost_per_q": 0.1, "latency_s": 15, "high_value": True},
        {"unique_answer": False, "baseline_acc": 0.8, "cost_per_q": 0.01},
        {"unique_answer": True, "baseline_acc": 0.55, "cost_per_q": 0.05, "latency_s": 10},
    ]
    for i, t in enumerate(tasks):
        method, n, temp = dep.should_deploy(t)
        print(f"任务{i+1}: {method} N={n} T={temp}")


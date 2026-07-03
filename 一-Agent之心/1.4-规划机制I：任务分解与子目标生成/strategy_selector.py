# strategy_selector
# 运行: python strategy_selector.py

class PlanningStrategySelector:
    """规划策略选择器"""
    def select(self, task_features):
        # 评估任务特征
        env_stability = task_features.get("env_stability", 0.5)
        deps_complexity = task_features.get("deps_complexity", "low")
        template_available = task_features.get("template", False)
        parallelizable = task_features.get("parallelizable", False)

        if template_available:
            return "template"
        if env_stability > 0.7 and deps_complexity == "low":
            return "plan_and_execute"
        if deps_complexity == "high":
            return "dependency_graph"
        if parallelizable:
            return "hierarchical"
        return "react"

if __name__ == "__main__":
    sel = PlanningStrategySelector()
    for task in [{"complexity": 2}, {"complexity": 8, "uncertain": True},
                 {"complexity": 5, "template": "rag"}]:
        print(f"任务 {task} -> {sel.select(task)}")

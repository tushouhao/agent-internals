# 混合式架构：反应层与慎思层的协同
# 运行: python hybrid_agent.py


class ReactiveLayer:
    """反应层：快速响应"""
    def act(self, observation):
        return f"reactive({observation})"

    def refine(self, deliberation):
        return f"refined({deliberation})"


class DeliberativeLayer:
    """慎思层：全局规划"""
    def plan(self, observation):
        return f"deliberative_plan({observation})"


class HybridAgent:
    """混合式架构：反应层 + 慎思层 + 仲裁器"""
    def __init__(self, reactive, deliberative, threshold_ms=100):
        self.reactive = reactive
        self.deliberative = deliberative
        self.threshold = threshold_ms

    def act(self, observation, time_budget_ms):
        if time_budget_ms < self.threshold:
            return self.reactive.act(observation)
        deliberation = self.deliberative.plan(observation)
        return self.reactive.refine(deliberation)


if __name__ == "__main__":
    agent = HybridAgent(ReactiveLayer(), DeliberativeLayer(), threshold_ms=100)

    # 场景1：时间紧张，走反应层
    result1 = agent.act("obstacle_detected", time_budget_ms=50)
    print(f"反应层: {result1}")

    # 场景2：时间充裕，走慎思层 -> 反应层 refine
    result2 = agent.act("crossroads", time_budget_ms=500)
    print(f"混合层: {result2}")

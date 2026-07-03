# strategy_selector
# 运行: python strategy_selector.py

class MemoryStrategySelector:
    """记忆策略选择器"""
    def select(self, task_profile):
        steps = task_profile.get("expected_steps", 30)
        key_dist = task_profile.get("key_info_distribution", "early")
        latency_budget = task_profile.get("latency_budget_ms", 5000)
        precision = task_profile.get("precision_required", "medium")

        if steps <= 30:
            return {"strategy": "sliding_window", "window": min(steps, 20),
                    "rationale": "短任务信息密度低, 滑动窗口足够"}

        if steps <= 100:
            if key_dist == "early" and precision == "high":
                return {"strategy": "window_plus_retrieval",
                        "window": 15, "top_k": 3,
                        "rationale": "早期关键信息需精确召回"}
            return {"strategy": "window_plus_summary",
                    "window": 15, "chunk": 10,
                    "rationale": "中等任务摘要压缩比高, 保真足够"}

        if latency_budget < 3000:
            return {"strategy": "window_plus_summary",
                    "window": 10, "chunk": 8,
                    "rationale": "延迟预算紧, 牺牲远期检索保速度"}
        return {"strategy": "hybrid_three_layer",
                "window": 10, "chunk": 8, "top_k": 5,
                "rationale": "长任务需全层覆盖"}

    def estimate_cost(self, strategy, steps):
        costs = {
            "sliding_window": (0, 0),
            "window_plus_summary": (50 * steps / 10, 200 * steps / 10),
            "window_plus_retrieval": (230 * steps, 400 * steps),
            "hybrid_three_layer": (280 * steps, 600 * steps),
        }
        lat, tokens = costs.get(strategy["strategy"], (0, 0))
        return {"latency_ms": lat, "extra_tokens": tokens}

if __name__ == "__main__":
    sel = MemoryStrategySelector()
    tasks = [
        {"expected_steps": 20},
        {"expected_steps": 60, "key_info_distribution": "early", "precision_required": "high"},
        {"expected_steps": 80, "key_info_distribution": "spread"},
        {"expected_steps": 300, "latency_budget_ms": 8000},
        {"expected_steps": 300, "latency_budget_ms": 2000},
    ]
    for i, t in enumerate(tasks):
        s = sel.select(t)
        cost = sel.estimate_cost(s, t["expected_steps"])
        print(f"任务{i+1} 步数={t.get('expected_steps')}:")
        print(f"  策略: {s['strategy']} | {s['rationale']}")
        print(f"  成本: 延迟{int(cost['latency_ms'])}ms 额外{int(cost['extra_tokens'])}token")


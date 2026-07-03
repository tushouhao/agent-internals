# pruning_strategy
# 运行: python pruning_strategy.py

class PruningStrategy:
    """多级剪枝策略"""
    def __init__(self, confidence_threshold=0.3, max_consecutive_failures=2):
        self.threshold = confidence_threshold
        self.max_failures = max_consecutive_failures

    def should_prune(self, path, evaluation):
        """判断是否应该剪枝当前路径"""
        reasons = []

        # 1. 低置信度剪枝
        if evaluation.confidence < self.threshold:
            reasons.append("low_confidence")

        # 2. 连续失败剪枝
        if evaluation.consecutive_failures >= self.max_failures:
            reasons.append("consecutive_failures")

        # 3. 深度超限剪枝
        if evaluation.depth > evaluation.max_expected_depth * 1.5:
            reasons.append("depth_exceeded")

        # 4. 重复状态剪枝
        if evaluation.state in evaluation.visited_states:
            reasons.append("state_visited")

        return len(reasons) > 0, reasons

if __name__ == "__main__":
    pruner = PruningStrategy(confidence_threshold=0.3)
    class E:
        confidence = 0.2
        consecutive_failures = 0
        depth = 3
        max_expected_depth = 10
        state = "x"
        visited_states = set()
    e = E()
    prune, reasons = pruner.should_prune(None, e)
    print(f"剪枝: {prune}, 原因: {reasons}")

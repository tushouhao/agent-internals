# step_controller
# 运行: python step_controller.py

class StepController:
    """循环步数控制器"""
    def __init__(self, strategy="confidence", max_steps=10):
        self.strategy = strategy
        self.max_steps = max_steps
        self.confidence_threshold = 0.75

    def should_stop(self, step, response, history):
        """判断是否应该终止循环"""
        if step >= self.max_steps:
            return True, "max_steps_reached"

        if self.strategy == "fixed":
            return step >= self.max_steps, "fixed"

        if self.strategy == "confidence":
            conf = self._estimate_confidence(response, history)
            if conf >= self.confidence_threshold:
                return True, f"confidence_{conf:.2f}"
            return False, f"confidence_{conf:.2f}"

        if self.strategy == "signal":
            return "Answer:" in response, "signal"

        return False, "default"

    def _estimate_confidence(self, response, history):
        """估计回答置信度（简化版）"""
        signals = []
        if "Answer:" in response:
            signals.append(0.4)
        if "确定" in response or "确认" in response:
            signals.append(0.2)
        if "可能" in response or "大概" in response:
            signals.append(-0.1)
        if "不确定" in response or "不清楚" in response:
            signals.append(-0.3)
        actions = [h.get("tool_call") for h in history if h.get("tool_call")]
        if len(actions) != len(set(str(a) for a in actions)):
            signals.append(-0.2)
        return max(0.0, min(1.0, 0.5 + sum(signals)))

if __name__ == "__main__":
    sc = StepController("confidence", max_steps=8)
    cases = [
        (3, "Thought: 确定 答案是42\nAnswer: 42", []),
        (2, "Thought: 可能是42", []),
        (5, "Thought: 不确定", []),
        (8, "Thought: 继续", []),
    ]
    for step, resp, hist in cases:
        stop, reason = sc.should_stop(step, resp, hist)
        print(f"步{step}: stop={stop} reason={reason}")


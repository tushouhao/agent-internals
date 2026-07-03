# termination_detector
# 运行: python termination_detector.py

import re

class TerminationDetector:
    """终止条件检测器"""
    def __init__(self):
        self.action_history = []
        self.max_repeats = 3
        self.stagnation_threshold = 4  # 连续无进展步数

    def check(self, step, response, action):
        """多维度终止检测"""
        reasons = []

        if re.search(r'Answer:\s*\S', response):
            reasons.append("explicit_answer")

        if action is None and "Answer" not in response:
            if re.search(r'(无需|不需要|已完成|没有更多)', response):
                reasons.append("no_action_signal")

        if action:
            self.action_history.append(str(action))
            recent = self.action_history[-self.max_repeats:]
            if len(recent) == self.max_repeats and len(set(recent)) == 1:
                reasons.append("repeated_action")

            if len(self.action_history) >= 4:
                seq = self.action_history[-4:]
                if seq[0] == seq[2] and seq[1] == seq[3] and seq[0] != seq[1]:
                    reasons.append("cycle_pattern")

        if step >= self.stagnation_threshold:
            reasons.append("stagnation")

        return {
            "should_terminate": len(reasons) > 0,
            "reasons": reasons,
            "primary": reasons[0] if reasons else None,
        }

if __name__ == "__main__":
    td = TerminationDetector()
    cases = [
        (3, "Answer: 42", None),
        (2, "已完成 无需更多", None),
        (4, "Thought: 继续", {"tool":"search","args":"q"}),
        (5, "Thought: 继续", {"tool":"search","args":"q"}),
        (6, "Thought: 继续", {"tool":"search","args":"q"}),
    ]
    for step, resp, act in cases:
        r = td.check(step, resp, act)
        print(f"步{step}: terminate={r['should_terminate']} reason={r['primary']}")


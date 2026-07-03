# failure_diagnoser
# 运行: python failure_diagnoser.py

class CoTFailureDiagnoser:
    """CoT 失败模式诊断器"""
    def __init__(self):
        self.failure_types = {"premise_error": "推理前提错误",
            "step_jump": "推理步骤跳跃", "extraction_error": "答案提取失败",
            "calculation_error": "计算错误", "logical_error": "逻辑错误"}

    def diagnose(self, reasoning_chain, expected_answer, extracted_answer):
        if extracted_answer == expected_answer:
            return {"status": "correct", "failure_type": None}
        failures = []
        if expected_answer in reasoning_chain and expected_answer != extracted_answer:
            failures.append("extraction_error")
        import re
        calcs = re.findall(r'=\s*(-?\d+\.?\d*)', reasoning_chain)
        if expected_answer not in calcs and calcs:
            failures.append("calculation_error")
        steps = [s.strip() for s in reasoning_chain.split('.') if s.strip()]
        for i in range(len(steps) - 1):
            w1, w2 = set(steps[i].split()), set(steps[i+1].split())
            if len(w1 & w2) / max(len(w1 | w2), 1) < 0.15:
                failures.append("step_jump"); break
        first = reasoning_chain.split('.')[0] if '.' in reasoning_chain else reasoning_chain[:100]
        if "假设" in first and "错误" in first:
            failures.append("premise_error")
        return {"status": "incorrect", "failure_types": failures,
                "primary": failures[0] if failures else "unknown"}
if __name__ == "__main__":
    d = CoTFailureDiagnoser()
    print(d.diagnose("2+2=4. 答案4", "4", "4"))
    print(d.diagnose("2+2=4. 答案5", "4", "5"))
    print(d.diagnose("假设错误. 2+2=5. 答案5", "4", "5"))

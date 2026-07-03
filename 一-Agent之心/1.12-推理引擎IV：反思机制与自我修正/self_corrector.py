# self_corrector
# 运行: python self_corrector.py

class SelfCorrector:
    """自我修正器 (含修正悖论检测)"""
    def __init__(self, llm, has_external_signal=False):
        self.llm = llm
        self.has_external_signal = has_external_signal
        self.correction_log = []

    def correct(self, answer, task):
        """自我修正流程"""
        # 第 1 步: 初始答案
        initial = answer
        # 第 2 步: 自我审查 (关键: 是否有客观信号)
        if self.has_external_signal:
            review = self._review_with_signal(initial, task)
        else:
            review = self._review_blind(initial, task)
        # 第 3 步: 决定是否修正
        if review["should_correct"]:
            corrected = self._apply_correction(initial, review["issues"])
        else:
            corrected = initial
        # 记录用于悖论分析
        self.correction_log.append({
            "initial": initial, "corrected": corrected,
            "changed": initial != corrected
        })
        return corrected

    def _review_with_signal(self, answer, task):
        """有外部信号: 基于客观反馈审查"""
        signal = task.get("test_result", "fail")
        if signal == "pass":
            return {"should_correct": False, "issues": []}
        issues = self._find_issues(answer, task)
        return {"should_correct": len(issues) > 0, "issues": issues}

    def _review_blind(self, answer, task):
        """无外部信号: 纯主观审查 (修正悖论来源)"""
        prompt = f"答案: {answer}\n这个答案正确吗? 有什么问题?"
        review = self.llm([{"role":"user","content":prompt}])
        # 盲审时 LLM 倾向"发现问题" (即使没有)
        should_correct = "问题" in review or "错误" in review or "不" in review
        return {"should_correct": should_correct, "issues": [review]}

    def _find_issues(self, answer, task):
        """基于失败信号定位问题"""
        prompt = f"答案: {answer}\n测试失败: {task.get('test_result','')}\n定位错误。"
        return [self.llm([{"role":"user","content":prompt}])]

    def _apply_correction(self, answer, issues):
        """应用修正"""
        prompt = f"原答案: {answer}\n问题: {'; '.join(issues)}\n修正后答案:"
        return self.llm([{"role":"user","content":prompt}])

    def paradox_rate(self):
        """修正悖论率: 把正确改成错误的比例"""
        # 需要真实标签才能计算, 这里仅返回变更率
        changed = sum(1 for l in self.correction_log if l["changed"])
        return changed / max(len(self.correction_log), 1)
if __name__ == "__main__":
    def llm(msgs): return "发现计算问题需修正"
    # 有外部信号场景
    sc1 = SelfCorrector(llm, has_external_signal=True)
    task1 = {"test_result": "fail"}
    r1 = sc1.correct("错误答案", task1)
    print(f"有信号: '{r1[:20]}', 变更率: {sc1.paradox_rate():.0%}")
    # 无外部信号场景 (修正悖论)
    sc2 = SelfCorrector(llm, has_external_signal=False)
    r2 = sc2.correct("可能正确的答案", {})
    print(f"无信号: '{r2[:20]}', 变更率: {sc2.paradox_rate():.0%}")


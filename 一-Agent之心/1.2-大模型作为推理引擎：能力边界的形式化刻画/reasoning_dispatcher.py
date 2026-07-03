# 基于 Avail 的推理分发器
# 运行: python reasoning_dispatcher.py

class ReasoningDispatcher:
    """基于 Avail 评分的推理分发器"""
    def __init__(self, llm, verifiers, deterministic_handlers):
        self.llm = llm
        self.verifiers = verifiers
        self.deterministic = deterministic_handlers

    def dispatch(self, task, context):
        score = avail_score(task.features, None)
        if score >= 80:
            return self.llm(task, context)
        elif score >= 60:
            candidate = self.llm(task, context)
            return self.verifiers[task.type](candidate)
        elif score >= 40:
            candidate = self.llm(task, context)
            v_result = self.verifiers[task.type](candidate)
            return {"result": candidate, "verification": v_result, "needs_review": True}
        else:
            return self.deterministic[task.type](task, context)

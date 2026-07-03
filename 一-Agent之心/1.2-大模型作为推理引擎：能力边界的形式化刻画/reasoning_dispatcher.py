# 基于 Avail 的推理分发器
# 运行: python reasoning_dispatcher.py

from types import SimpleNamespace

# 内联 Avail 评分（避免跨文件依赖）
def avail_score(task_features, llm_benchmarks):
    """计算推理任务的可用性评分(0-100)"""
    score = 100
    if task_features.get("complexity", 0) > 6:
        score -= 25
    if task_features.get("knowledge_type") == "open":
        score -= 15
    if task_features.get("requires_symbolic"):
        score -= 30
    if task_features.get("requires_tool"):
        score += 10
    if task_features.get("safety_critical"):
        score -= 20
    return max(0, min(100, score))

class ReasoningDispatcher:
    """基于 Avail 评分的推理分发器"""
    def __init__(self, llm, verifiers, deterministic_handlers):
        self.llm = llm
        self.verifiers = verifiers
        self.deterministic = deterministic_handlers

    def dispatch(self, task, context):
        score = avail_score(task.features, None)
        if score >= 80:
            return {"path": "llm_direct", "score": score,
                    "result": self.llm(task, context)}
        elif score >= 60:
            candidate = self.llm(task, context)
            verified = self.verifiers.get(task.type, lambda x: x)(candidate)
            return {"path": "llm_verified", "score": score, "result": verified}
        elif score >= 40:
            candidate = self.llm(task, context)
            v = self.verifiers.get(task.type, lambda x: x)(candidate)
            return {"path": "llm_review", "score": score,
                    "result": candidate, "verification": v, "needs_review": True}
        else:
            handler = self.deterministic.get(task.type)
            return {"path": "deterministic", "score": score,
                    "result": handler(task, context) if handler else None}

if __name__ == "__main__":
    def llm(task, ctx): return f"LLM推理结果({task.desc})"
    def verifier(x): return x + " [已验证]"
    def det_handler(task, ctx): return f"规则引擎处理({task.desc})"

    dispatcher = ReasoningDispatcher(
        llm,
        verifiers={"math": verifier},
        deterministic_handlers={"math": det_handler},
    )

    cases = [
        SimpleNamespace(desc="简单问答", type="qa",
                        features={"complexity": 2, "knowledge_type": "closed"}),
        SimpleNamespace(desc="数学证明", type="math",
                        features={"complexity": 8, "knowledge_type": "open",
                                  "requires_symbolic": True, "safety_critical": True}),
    ]
    for c in cases:
        r = dispatcher.dispatch(c, {})
        print(f"[{c.desc}] 评分={r['score']} 路径={r['path']}")
        print(f"  结果: {r['result']}")

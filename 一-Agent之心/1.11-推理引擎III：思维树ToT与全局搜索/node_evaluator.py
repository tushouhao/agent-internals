# node_evaluator
# 运行: python node_evaluator.py

class NodeEvaluator:
    """节点评估器"""
    def __init__(self, llm, method="absolute"):
        self.llm = llm
        self.method = method
        self.calibration_cache = {}
    def evaluate(self, node, problem):
        """评估节点前景"""
        if self.method == "absolute":
            return self._absolute_score(node, problem)
        elif self.method == "relative":
            return self._relative_score(node, problem)
        elif self.method == "voting":
            return self._voting_score(node, problem)
        return 0.5
    def _absolute_score(self, node, problem):
        """绝对评分: 0-1"""
        prompt = f"问题: {problem}\n当前推理: {node.state}\n前景 0-1 分:"
        resp = self.llm([{"role": "user", "content": prompt}])
        try:
            score = float(resp.strip())
            return max(0.0, min(1.0, score))
        except ValueError:
            return 0.5
    def _relative_score(self, node, problem):
        """相对评分: 与前序节点对比"""
        parent_score = node.parent.score if node.parent else 0.5
        prompt = f"问题: {problem}\n父状态: {node.parent.state if node.parent else '无'}\n当前: {node.state}\n当前比父状态更好/更差/相当?"
        resp = self.llm([{"role": "user", "content": prompt}])
        if "更好" in resp:
            return parent_score + 0.15
        elif "更差" in resp:
            return parent_score - 0.2
        return parent_score
    def _voting_score(self, node, problem, n_voters=3):
        """多票评分: 降低单次评分方差"""
        scores = []
        for i in range(n_voters):
            scores.append(self._absolute_score(node, problem))
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        confidence = max(0, 1 - variance * 4)
        return 0.5 + (avg - 0.5) * confidence
if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "0-1" in c: return "0.7"
        if "更好" in c or "更差" in c or "相当" in c: return "更好"
        return "0.6"
    ev = NodeEvaluator(llm, "voting")
    class N: 
        state="测试"; parent=None
    print(f"投票评分: {ev.evaluate(N(), '问题')}")
    ev2 = NodeEvaluator(llm, "absolute")
    print(f"绝对评分: {ev2.evaluate(N(), '问题')}")


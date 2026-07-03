# tot_engine
# 运行: python tot_engine.py

class ThoughtNode:
    """思维树节点"""
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.score = 0.0
        self.visited = False
        self.depth = depth
class ToTEngine:
    """思维树推理引擎"""
    def __init__(self, llm, max_depth=4, max_branches=3):
        self.llm = llm
        self.max_depth = max_depth
        self.max_branches = max_branches
    def solve(self, problem):
        """四阶段循环求解"""
        root = ThoughtNode(problem)
        frontier = [root]
        for depth in range(self.max_depth):
            next_frontier = []
            for node in frontier:
                candidates = self._decompose(node.state)
                scored = [(self._evaluate(c, problem), c) for c in candidates]
                scored.sort(key=lambda x: -x[0])
                for score, state in scored[:self.max_branches]:
                    child = ThoughtNode(state, parent=node, depth=depth+1)
                    child.score = score
                    node.children.append(child)
                    next_frontier.append(child)
            next_frontier.sort(key=lambda n: -n.score)
            frontier = next_frontier[:self.max_branches]
            for node in frontier:
                if self._is_goal(node.state, problem):
                    return self._trace_path(node)
        best = max(frontier, key=lambda n: n.score) if frontier else root
        return self._trace_path(best)
    def _decompose(self, state):
        """分解: 生成候选下一步"""
        prompt = f"当前状态: {state}\n生成 3 个可能的下一步。"
        resp = self.llm([{"role": "user", "content": prompt}])
        return [s.strip() for s in resp.split('\n') if s.strip()][:3]
    def _evaluate(self, candidate, problem):
        """评估: 给候选打分 0-1"""
        prompt = f"问题: {problem}\n候选: {candidate}\n该候选有多大前景? 0-1 分。"
        resp = self.llm([{"role": "user", "content": prompt}])
        try:
            return float(resp.strip())
        except ValueError:
            return 0.5
    def _is_goal(self, state, problem):
        """目标检测"""
        return "答案" in state or "解决" in state
    def _trace_path(self, node):
        """回溯路径"""
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))

class ThoughtNode:
    """思维树节点"""
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.score = 0.0
        self.visited = False
        self.depth = depth

if __name__ == "__main__":
    def llm(msgs):
        c = msgs[-1]["content"]
        if "生成" in c: return "思路A\n思路B\n思路C"
        if "前景" in c: return "0.7"
        return "答案: 完成"
    eng = ToTEngine(llm, max_depth=2, max_branches=2)
    path = eng.solve("求 24 点: 4,6,2,3")
    print(f"路径({len(path)}步): {path}")


# tot_mcts_hybrid
# 运行: python tot_mcts_hybrid.py

import random, math
class ToTMCTSHybrid:
    """ToT + MCTS 融合引擎"""
    def __init__(self, llm, simulate_fn, max_depth=4, simulations=20):
        self.llm = llm
        self.simulate = simulate_fn
        self.max_depth = max_depth
        self.simulations = simulations
    def solve(self, problem):
        """融合搜索: ToT 分解 + MCTS 模拟评估"""
        root = ThoughtNode(problem)
        return self._mcts_search(root, problem, self.simulations)
    def _mcts_search(self, node, problem, simulations):
        """MCTS 搜索: 用 ToT 分解作为 expand"""
        for _ in range(simulations):
            leaf = self._select(node)
            if leaf.depth < self.max_depth and not leaf.children:
                candidates = self._tot_decompose(leaf, problem)
                for c in candidates:
                    leaf.children.append(c)
            if leaf.children:
                target = random.choice(leaf.children)
            else:
                target = leaf
            reward = self.simulate(target.state)
            self._backpropagate(target, reward)
        best = max(node.children, key=lambda c: getattr(c, 'visits', 0)) if node.children else node
        return self._trace_path(best)
    def _select(self, node):
        """UCB 选择"""
        while node.children:
            total_visits = sum(getattr(c, 'visits', 0) for c in node.children) or 1
            def ucb(c):
                visits = getattr(c, 'visits', 0)
                if visits == 0: return float('inf')
                exploit = getattr(c, 'wins', 0) / visits
                explore = 1.4 * math.sqrt(math.log(total_visits) / visits)
                return exploit + explore
            node = max(node.children, key=ucb)
        return node
    def _tot_decompose(self, node, problem):
        """ToT 分解"""
        prompt = f"问题: {problem}\n状态: {node.state}\n生成 2 个下一步。"
        resp = self.llm([{"role": "user", "content": prompt}])
        candidates = [s.strip() for s in resp.split('\n') if s.strip()][:2]
        return [ThoughtNode(s, parent=node, depth=node.depth+1) for s in candidates]
    def _backpropagate(self, node, reward):
        """回溯更新"""
        while node:
            node.visits = getattr(node, 'visits', 0) + 1
            node.wins = getattr(node, 'wins', 0) + reward
            node = node.parent
    def _trace_path(self, node):
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
    import random
    random.seed(42)
    def llm(msgs): return "思路X\n思路Y"
    def sim(state): return random.random()
    eng = ToTMCTSHybrid(llm, sim, max_depth=2, simulations=10)
    path = eng.solve("复杂决策问题")
    print(f"融合路径({len(path)}步): {path[:3]}")


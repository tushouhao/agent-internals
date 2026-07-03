# mcts_search
# 运行: python mcts_search.py

import math, random

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def ucb_score(self, exploration=1.4):
        if self.visits == 0:
            return float('inf')
        exploitation = self.wins / self.visits
        exploration_term = exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits)
        return exploitation + exploration_term

def mcts_search(root, get_children, simulate, max_iterations=100):
    for _ in range(max_iterations):
        # 1. 选择: 从根到叶子
        node = root
        while node.children:
            node = max(node.children, key=lambda n: n.ucb_score())

        # 2. 扩展: 如果叶子未展开
        if node.visits > 0:
            new_states = get_children(node.state)
            for s in new_states[:3]:  # 限制每步展开数
                child = MCTSNode(s, parent=node)
                node.children.append(child)
            if node.children:
                node = random.choice(node.children)

        # 3. 模拟: 随机执行到结束
        reward = simulate(node.state)

        # 4. 回溯: 更新路径上所有节点
        while node:
            node.visits += 1
            node.wins += reward
            node = node.parent

if __name__ == "__main__":
    random.seed(42)
    root = MCTSNode("root")
    children_fn = lambda s: [f"{s}_{i}" for i in range(2)]
    simulate_fn = lambda s: random.random()
    mcts_search(root, children_fn, simulate_fn, max_iterations=20)
    print(f"访问: {root.visits}, 胜: {root.wins}")
    print(f"子节点: {len(root.children)}")

# search_strategies
# 运行: python search_strategies.py

class ToTSearchStrategies:
    """ToT 三种搜索策略"""
    def __init__(self, llm, evaluator):
        self.llm = llm
        self.evaluator = evaluator
    def bfs_search(self, root, max_depth, get_children):
        """BFS: 逐层展开所有节点"""
        frontier = [root]
        for depth in range(max_depth):
            next_frontier = []
            for node in frontier:
                children = get_children(node)
                for c in children:
                    c.score = self.evaluator(c)
                    next_frontier.append(c)
            frontier = next_frontier
            if not frontier:
                break
        return max(frontier, key=lambda n: n.score) if frontier else root
    def dfs_search(self, node, max_depth, get_children, best=None):
        """DFS: 深度优先递归"""
        if node.depth >= max_depth:
            return max([node, best], key=lambda n: n.score) if best else node
        if best is None:
            best = node
        for child in get_children(node):
            child.score = self.evaluator(child)
            if child.score > best.score:
                best = child
            result = self.dfs_search(child, max_depth, get_children, best)
            if result.score > best.score:
                best = result
        return best
    def beam_search(self, root, max_depth, beam_width, get_children):
        """Beam Search: 每层只保留 top-k"""
        frontier = [root]
        for depth in range(max_depth):
            candidates = []
            for node in frontier:
                for c in get_children(node):
                    c.score = self.evaluator(c)
                    candidates.append(c)
            candidates.sort(key=lambda n: -n.score)
            frontier = candidates[:beam_width]
            if not frontier:
                break
        return frontier[0] if frontier else root

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
    def llm(msgs): return "子1\n子2"
    def ev(node): return len(node.state) % 0.9 + 0.1
    ss = ToTSearchStrategies(llm, ev)
    def gc(node):
        if node.depth >= 2: return []
        return [ThoughtNode(node.state+f".{i}", parent=node, depth=node.depth+1) for i in range(2)]
    root = ThoughtNode("根")
    print(f"BFS最优: {ss.bfs_search(root, 2, gc).state}")
    print(f"DFS最优: {ss.dfs_search(root, 2, gc).state}")
    print(f"Beam最优: {ss.beam_search(root, 2, 2, gc).state}")


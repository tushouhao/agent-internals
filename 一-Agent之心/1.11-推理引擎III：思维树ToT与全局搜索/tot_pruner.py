# tot_pruner
# 运行: python tot_pruner.py

class ToTPruner:
    """ToT 剪枝器"""
    def __init__(self, strategy="threshold"):
        self.strategy = strategy
        self.score_threshold = 0.3
        self.max_stagnation = 2
        self.visited_states = set()
    def should_prune(self, node, path_scores):
        """判断是否剪枝"""
        if self.strategy == "threshold":
            return node.score < self.score_threshold
        elif self.strategy == "stagnation":
            return self._is_stagnant(path_scores)
        elif self.strategy == "duplicate":
            return self._is_duplicate(node)
        elif self.strategy == "combined":
            return (node.score < self.score_threshold or
                    self._is_duplicate(node) or
                    self._is_stagnant(path_scores))
        return False
    def _is_stagnant(self, path_scores):
        """停滞检测: 连续 N 步分数不升"""
        if len(path_scores) < self.max_stagnation + 1:
            return False
        recent = path_scores[-(self.max_stagnation + 1):]
        return all(recent[i] >= recent[i+1] for i in range(len(recent)-1))
    def _is_duplicate(self, node):
        """重复状态检测"""
        sig = hash(node.state[:50])
        if sig in self.visited_states:
            return True
        self.visited_states.add(sig)
        return False
    def prune_children(self, node, children):
        """对子节点列表剪枝"""
        kept = []
        for c in children:
            if not self.should_prune(c, [c.score]):
                kept.append(c)
        return kept if kept else children[:1]  # 至少保留 1 个
if __name__ == "__main__":
    pruner = ToTPruner("combined")
    class N:
        def __init__(self, s, sc): self.state=s; self.score=sc
    nodes = [N("A",0.8), N("B",0.1), N("A",0.5), N("C",0.6)]
    kept = pruner.prune_children(None, nodes)
    print(f"保留: {[(n.state,n.score) for n in kept]}")


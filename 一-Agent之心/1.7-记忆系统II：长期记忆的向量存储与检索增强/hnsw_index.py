# hnsw_index
# 运行: python hnsw_index.py

import random, math

class HNSWIndex:
    """HNSW 索引简化实现"""
    def __init__(self, M=16, ef_construction=200, ef_search=50):
        self.M, self.ef_c, self.ef_s = M, ef_construction, ef_search
        self.layers, self.entry_point, self.max_layer = [], None, -1

    def insert(self, node_id, vector):
        """插入节点: 决定层级 + 逐层连接"""
        level = int(-math.log(random.random() + 0.01) * 2)
        node = {"id": node_id, "vec": vector,
                "neighbors": [[] for _ in range(level + 1)]}
        while len(self.layers) <= level:
            self.layers.append([])
        if self.entry_point is None:
            self.entry_point, self.max_layer = node, level
            self.layers[level].append(node)
            return
        cur = self.entry_point
        for lc in range(self.max_layer, level, -1):
            cur = self._greedy_search(cur, vector, lc)
        for lc in range(min(level, self.max_layer), -1, -1):
            candidates = self._search_layer(cur, vector, self.ef_c, lc)
            neighbors = sorted(candidates, key=lambda x: x[0])[:self.M]
            node["neighbors"][lc] = [n for _, n in neighbors]
            for _, n in neighbors:
                if lc < len(n["neighbors"]):
                    n["neighbors"][lc].append(node)
            cur = neighbors[0][1] if neighbors else cur
        self.layers[level].append(node)
        if level > self.max_layer:
            self.max_layer, self.entry_point = level, node

    def search(self, query_vec, k=5):
        if not self.entry_point:
            return []
        cur = self.entry_point
        for lc in range(self.max_layer, 0, -1):
            cur = self._greedy_search(cur, query_vec, lc)
        candidates = self._search_layer(cur, query_vec, self.ef_s, 0)
        return [n for _, n in sorted(candidates, key=lambda x: x[0])[:k]]

    def _greedy_search(self, entry, vec, layer):
        cur, cur_d = entry, self._dist(vec, entry["vec"])
        improved = True
        while improved:
            improved = False
            for n in (cur["neighbors"][layer] if layer < len(cur["neighbors"]) else []):
                d = self._dist(vec, n["vec"])
                if d < cur_d:
                    cur, cur_d, improved = n, d, True
        return cur
    def _search_layer(self, entry, vec, ef, layer):
        candidates = [(self._dist(vec, entry["vec"]), entry)]
        visited = {id(entry)}
        while len(candidates) < ef:
            added = False
            for _, n in list(candidates):
                for nb in (n["neighbors"][layer] if layer < len(n["neighbors"]) else []):
                    if id(nb) not in visited:
                        candidates.append((self._dist(vec, nb["vec"]), nb))
                        visited.add(id(nb))
                        added = True
            if not added:
                break
        return sorted(candidates, key=lambda x: x[0])[:ef]

    def _dist(self, v1, v2):
        return math.sqrt(sum((a-b)**2 for a, b in zip(v1, v2)))

if __name__ == "__main__":
    import random
    random.seed(42)
    idx = HNSWIndex(M=4, ef_construction=10, ef_search=10)
    for i in range(20):
        idx.insert(i, [random.random() for _ in range(3)])
    q = [0.5, 0.5, 0.5]
    results = idx.search(q, k=3)
    print(f"插入 20 个节点, 检索 Top-3:")
    for r in results:
        print(f"  id={r['id']} vec={[round(x,2) for x in r['vec']]}")
    print(f"层数: {idx.max_layer + 1}")


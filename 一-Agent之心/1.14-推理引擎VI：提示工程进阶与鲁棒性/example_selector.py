# example_selector
# 运行: python example_selector.py

class ExampleSelector:
    """少样本示例选取器"""
    def __init__(self, examples, embed_fn):
        self.examples = examples
        self.embed_fn = embed_fn
        self.embeddings = [embed_fn(e["input"]) for e in examples]

    def select(self, query, strategy="similarity", k=4):
        if strategy == "random":
            return self._random(k)
        elif strategy == "similarity":
            return self._similarity(query, k)
        elif strategy == "diversity":
            return self._diversity(query, k)
        elif strategy == "difficulty":
            return self._difficulty(k)
        return self.examples[:k]

    def _random(self, k):
        import random
        return random.sample(self.examples, min(k, len(self.examples)))

    def _similarity(self, query, k):
        q_emb = self.embed_fn(query)
        scored = [(self._cosine(q_emb, e), ex) for e, ex in zip(self.embeddings, self.examples)]
        scored.sort(key=lambda x: -x[0])
        return [ex for _, ex in scored[:k]]

    def _diversity(self, query, k):
        """MMR: 兼顾相关性与多样性"""
        q_emb = self.embed_fn(query)
        selected, remaining = [], list(range(len(self.examples)))
        for _ in range(k):
            best, best_idx = -1, None
            for i in remaining:
                rel = self._cosine(q_emb, self.embeddings[i])
                if not selected:
                    score = rel
                else:
                    max_sim = max(self._cosine(self.embeddings[i], self.embeddings[j])
                                  for j in selected)
                    score = 0.7 * rel - 0.3 * max_sim
                if score > best:
                    best, best_idx = score, i
            selected.append(best_idx)
            remaining.remove(best_idx)
        return [self.examples[i] for i in selected]

    def _difficulty(self, k):
        """难度排序: 由易到难"""
        sorted_ex = sorted(self.examples, key=lambda e: e.get("difficulty", 0.5))
        return sorted_ex[:k]

    def _cosine(self, a, b):
        dot = sum(x*y for x, y in zip(a, b))
        na = sum(x*x for x in a) ** 0.5
        nb = sum(y*y for y in b) ** 0.5
        return dot / max(na * nb, 1e-9)
if __name__ == "__main__":
    def embed(text):
        return [float(len(w) % 5) / 5 for w in text.split()[:6]] + [0.0] * 6
    examples = [
        {"input": "好评: 好看电影", "output": "正面", "difficulty": 0.3},
        {"input": "差评: 无聊透顶", "output": "负面", "difficulty": 0.5},
        {"input": "中性: 普通水平", "output": "中性", "difficulty": 0.7},
        {"input": "好评: 强烈推荐", "output": "正面", "difficulty": 0.2},
    ]
    sel = ExampleSelector(examples, embed)
    q = "这部电影真不错"
    for strat in ["random", "similarity", "diversity", "difficulty"]:
        picked = sel.select(q, strategy=strat, k=2)
        print(f"{strat}: {[p['input'][:10] for p in picked]}")


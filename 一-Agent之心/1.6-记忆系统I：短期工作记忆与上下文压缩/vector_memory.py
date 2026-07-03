# vector_memory
# 运行: python vector_memory.py

class VectorRetrievalMemory:
    """向量检索增强工作记忆"""
    def __init__(self, embed_fn, top_k=5):
        self.embed_fn = embed_fn
        self.top_k = top_k
        self.store = []

    def add(self, text, metadata=None):
        self.store.append({"id": len(self.store), "text": text,
                           "embedding": self.embed_fn(text),
                           "metadata": metadata or {}})

    def retrieve(self, query, top_k=None):
        k = top_k or self.top_k
        q_emb = self.embed_fn(query)
        scored = [(self._cosine(q_emb, item["embedding"]), item)
                  for item in self.store]
        scored.sort(key=lambda x: -x[0])
        return [item for _, item in scored[:k]]

    def _cosine(self, v1, v2):
        import math
        dot = sum(a*b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a*a for a in v1)) or 1
        n2 = math.sqrt(sum(b*b for b in v2)) or 1
        return dot / (n1 * n2)

    def build_context(self, query, system_prompt):
        retrieved = self.retrieve(query)
        ctx = [{"role": "system", "content": system_prompt}]
        ctx.append({"role": "system", "content":
            "相关记忆:\n" + "\n".join(f"- {r['text']}" for r in retrieved)})
        ctx.append({"role": "user", "content": query})
        return ctx

if __name__ == "__main__":
    def fake_embed(text):
        return [sum(ord(c) for c in text) % 17, len(text) % 13]
    mem = VectorRetrievalMemory(fake_embed, top_k=2)
    mem.add("用户订单 OD2024001 已发货")
    mem.add("用户问北京天气")
    mem.add("订单物流到达北京分拣中心")
    r = mem.retrieve("订单物流")
    print(f"检索 '订单物流' Top-2:")
    for item in r:
        print(f"  - {item['text']}")


# multi_route_retriever
# 运行: python multi_route_retriever.py


import re

class LongTermMemoryStore:
    """内联依赖: 三层长期记忆存储"""
    def __init__(self, embed_fn):
        self.embed_fn = embed_fn
        self.vector_index, self.keyword_index, self.metadata_table = [], {}, []
        self._next_id = 0

    def add(self, content, metadata=None):
        mid = self._next_id; self._next_id += 1
        record = {"id": mid, "content": content,
                  "embedding": self.embed_fn(content),
                  "metadata": metadata or {}}
        self.vector_index.append(record)
        self.metadata_table.append(record)
        for kw in self._extract_keywords(content):
            self.keyword_index.setdefault(kw, []).append(mid)
        return mid

    def _extract_keywords(self, text):
        return list(set(re.findall(r'[\w\u4e00-\u9fff]{2,}', text)))

import math, time

class MultiRouteRetriever:
    """多路检索 + 重排"""
    def __init__(self, store, llm_rerank=None):
        self.store = store
        self.llm_rerank = llm_rerank

    def retrieve(self, query, top_k=5):
        """多路召回 + 重排"""
        vec = self._vector_search(query, top_k * 3)
        kw = self._keyword_search(query, top_k * 3)
        meta = self._metadata_search(query, top_k * 3)
        fused = self._rrf_fuse([vec, kw, meta])
        if self.llm_rerank:
            fused = self._llm_rerank(query, fused, top_k)
        return fused[:top_k]

    def _vector_search(self, query, k):
        q_emb = self.store.embed_fn(query)
        scored = sorted(((self._cosine(q_emb, r["embedding"]), r)
                         for r in self.store.vector_index), key=lambda x: -x[0])
        return [r for _, r in scored[:k]]

    def _keyword_search(self, query, k):
        kws = self.store._extract_keywords(query)
        scores = {}
        for kw in kws:
            for mid in self.store.keyword_index.get(kw, []):
                scores[mid] = scores.get(mid, 0) + 1
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return [self.store.metadata_table[mid] for mid, _ in ranked[:k]]

    def _metadata_search(self, query, k):
        now = time.time()
        return [r for r in self.store.metadata_table
                if now - r["metadata"].get("timestamp", 0) < 7 * 86400][:k]

    def _rrf_fuse(self, result_lists, k=60):
        """Reciprocal Rank Fusion"""
        scores = {}
        for results in result_lists:
            for rank, r in enumerate(results):
                scores[r["id"]] = scores.get(r["id"], 0) + 1 / (k + rank + 1)
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return [self.store.metadata_table[mid] for mid, _ in ranked]

    def _llm_rerank(self, query, results, top_k):
        qk = set(self.store._extract_keywords(query))
        scored = sorted(((len(qk & set(self.store._extract_keywords(r["content"]))), r)
                         for r in results), key=lambda x: -x[0])
        return [r for _, r in scored[:top_k * 2]]

    def _cosine(self, v1, v2):
        dot = sum(a*b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a*a for a in v1)) or 1
        n2 = math.sqrt(sum(b*b for b in v2)) or 1
        return dot / (n1 * n2)

if __name__ == "__main__":
    import time
    def fake_embed(text):
        return [sum(ord(c) for c in text) % 17, len(text) % 13]
    store = LongTermMemoryStore(fake_embed)
    now = time.time()
    store.add("订单 OD2024001 已发货", {"timestamp": now})
    store.add("北京今天晴", {"timestamp": now})
    store.add("订单物流到北京", {"timestamp": now})
    store.add("用户偏好简洁回答", {"timestamp": now - 8 * 86400})
    retriever = MultiRouteRetriever(store, llm_rerank=True)
    for q in ["订单物流", "北京天气"]:
        results = retriever.retrieve(q, top_k=2)
        print(f"查询 '{q}' Top-2:")
        for r in results:
            print(f"  - {r['content']}")


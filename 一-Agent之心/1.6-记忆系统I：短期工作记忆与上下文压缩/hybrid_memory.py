# hybrid_memory
# 运行: python hybrid_memory.py
import math

class VectorRetrievalMemory:
    """内联简化版向量检索记忆（避免跨文件依赖）"""
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
        scored = [(self._cosine(q_emb, it["embedding"]), it) for it in self.store]
        scored.sort(key=lambda x: -x[0])
        return [it for _, it in scored[:k]]

    def _cosine(self, v1, v2):
        dot = sum(a*b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a*a for a in v1)) or 1
        n2 = math.sqrt(sum(b*b for b in v2)) or 1
        return dot / (n1 * n2)


class HybridMemory:
    """三层混合工作记忆"""
    def __init__(self, embed_fn, llm_summarize, config=None):
        cfg = config or {}
        self.recent_window = cfg.get("recent_window", 10)
        self.summary_chunk = cfg.get("summary_chunk", 10)
        self.top_k = cfg.get("retrieval_top_k", 3)
        self.recent = []
        self.summaries = []
        self.long_term = VectorRetrievalMemory(embed_fn, top_k=self.top_k)
        self.llm_summarize = llm_summarize
        self._pending = []

    def add(self, role, content, metadata=None):
        msg = {"role": role, "content": content, "metadata": metadata or {}}
        self.long_term.add(content, metadata)
        self.recent.append(msg)
        self._pending.append(msg)
        if len(self._pending) >= self.summary_chunk:
            self._compress()
        if len(self.recent) > self.recent_window:
            self.recent = self.recent[-self.recent_window:]

    def _compress(self):
        text = "\n".join(f"[{m['role']}]: {m['content']}" for m in self._pending)
        self.summaries.append({"summary": self.llm_summarize(text),
                                "count": len(self._pending)})
        self._pending = []

    def get_context(self, system_prompt, query):
        ctx = [{"role": "system", "content": system_prompt}]
        retrieved = self.long_term.retrieve(query, top_k=self.top_k)
        if retrieved:
            ctx.append({"role": "system", "content":
                "[长期] " + " | ".join(r["text"][:80] for r in retrieved)})
        if self.summaries:
            ctx.append({"role": "system", "content":
                "[摘要] " + " >> ".join(s["summary"] for s in self.summaries[-5:])})
        ctx.extend(self.recent)
        ctx.append({"role": "user", "content": query})
        return ctx

    def stats(self):
        return {"recent": len(self.recent), "summaries": len(self.summaries),
                "long_term": len(self.long_term.store)}

if __name__ == "__main__":
    def fake_embed(text):
        return [sum(ord(c) for c in text) % 17, len(text) % 13]
    def mock_summary(text):
        return f"[{len(text)}字摘要]"
    mem = HybridMemory(fake_embed, mock_summary,
                       config={"recent_window":3, "summary_chunk":3, "retrieval_top_k":2})
    for i in range(8):
        mem.add("user", f"消息{i}: 订单 OD2024{i}")
    ctx = mem.get_context("你是助手", "查订单")
    print(f"统计: {mem.stats()}")
    print(f"上下文层数: {len(ctx)}")


# hierarchical_summarizer
# 运行: python hierarchical_summarizer.py

class HierarchicalSummarizer:
    """分层摘要压缩"""
    def __init__(self, llm_summarize, chunk_size=10):
        self.llm_summarize = llm_summarize
        self.chunk_size = chunk_size
        self.summaries = []
        self.recent_buffer = []

    def add(self, role, content):
        self.recent_buffer.append({"role": role, "content": content})
        if len(self.recent_buffer) >= self.chunk_size:
            self._compress()

    def _compress(self):
        if not self.recent_buffer:
            return
        text = "\n".join(f"[{m['role']}]: {m['content']}"
                         for m in self.recent_buffer)
        summary = self.llm_summarize(text)
        self.summaries.append({"summary": summary,
                                "source_tokens": sum(len(m["content"])
                                                     for m in self.recent_buffer)})
        self.recent_buffer = []

    def get_context(self, system_prompt, query):
        ctx = [{"role": "system", "content": system_prompt}]
        if self.summaries:
            digest = "进展摘要:\n" + "\n".join(
                f"[段{i+1}] {s['summary']}" for i, s in enumerate(self.summaries))
            ctx.append({"role": "system", "content": digest})
        ctx.extend(self.recent_buffer)
        ctx.append({"role": "user", "content": query})
        return ctx

    def stats(self):
        orig = sum(s["source_tokens"] for s in self.summaries)
        comp = sum(len(s["summary"]) for s in self.summaries)
        return {"segments": len(self.summaries),
                "compression_ratio": comp / orig if orig else 0}

if __name__ == "__main__":
    def mock_llm(text):
        return f"摘要: {text[:30]}..."
    hs = HierarchicalSummarizer(mock_llm, chunk_size=3)
    for i in range(7):
        hs.add("user", f"消息内容 {i}")
    ctx = hs.get_context("你是助手", "当前查询")
    print(f"压缩统计: {hs.stats()}")
    print(f"上下文消息数: {len(ctx)}")


# reflection_memory
# 运行: python reflection_memory.py

class ReflectionMemory:
    """反思记忆库"""
    def __init__(self, embed_fn, max_size=100):
        self.embed_fn = embed_fn
        self.max_size = max_size
        self.entries = []  # [(task_sig, reflection, embedding)]

    def write(self, task, reflection):
        """写入反思"""
        emb = self.embed_fn(reflection)
        self.entries.append((self._task_sig(task), reflection, emb))
        if len(self.entries) > self.max_size:
            self.entries.pop(0)  # FIFO 淘汰

    def retrieve(self, task, top_k=3):
        """检索相关反思"""
        if not self.entries: return []
        q_emb = self.embed_fn(self._task_sig(task))
        scored = [(self._cosine(q_emb, e[2]), e[1]) for e in self.entries]
        scored.sort(key=lambda x: -x[0])
        return [r[1] for r in scored[:top_k]]

    def _task_sig(self, task):
        """任务签名: 关键词提取"""
        words = [w for w in task.split() if len(w) > 2]
        return " ".join(words[:5])

    def _cosine(self, a, b):
        """余弦相似度"""
        dot = sum(x*y for x, y in zip(a, b))
        na = sum(x*x for x in a) ** 0.5
        nb = sum(y*y for y in b) ** 0.5
        return dot / max(na * nb, 1e-9)
if __name__ == "__main__":
    def embed(text):
        # 简单 hash 嵌入
        return [float(len(w) % 7) / 7 for w in text.split()[:8]] + [0.0] * 8
    mem = ReflectionMemory(embed, max_size=10)
    mem.write("排序算法", "注意边界条件 i < n-1")
    mem.write("查找算法", "二分需排序先")
    mem.write("排序数组去重", "用双指针")
    results = mem.retrieve("排序问题", top_k=2)
    print(f"检索到 {len(results)} 条反思: {results}")


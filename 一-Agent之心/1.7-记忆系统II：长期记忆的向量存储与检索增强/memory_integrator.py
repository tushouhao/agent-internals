# memory_integrator
# 运行: python memory_integrator.py

import math, re, time

class MemoryIntegrator:
    """记忆整合器"""
    def __init__(self, llm_summarize, max_context_tokens=2000):
        self.llm_summarize = llm_summarize
        self.max_tokens = max_context_tokens

    def integrate(self, query, retrieved_memories):
        """将检索记忆整合为上下文片段"""
        unique = self._deduplicate(retrieved_memories)
        conflicts = self._detect_conflicts(unique)
        scored = self._rank_with_decay(unique, query)
        compressed = self._compress_to_budget(scored)
        return {"context": compressed, "conflicts": conflicts,
                "original_count": len(retrieved_memories),
                "final_count": len(compressed)}

    def _deduplicate(self, memories):
        seen, unique = set(), []
        for m in memories:
            h = hash(m["content"][:100])
            if h not in seen:
                seen.add(h)
                unique.append(m)
        return unique

    def _detect_conflicts(self, memories):
        facts, conflicts = {}, []
        for m in memories:
            for match in re.finditer(r'(\w+):\s*(\d+(?:\.\d+)?)', m["content"]):
                key, val = match.group(1), match.group(2)
                if key in facts and facts[key] != val:
                    conflicts.append({"key": key, "values": [facts[key], val]})
                facts[key] = val
        return conflicts

    def _rank_with_decay(self, memories, query):
        now = time.time()
        scored = sorted(((math.exp(-(now - m["metadata"].get("timestamp", now)) / 86400 / 30), m)
                         for m in memories), key=lambda x: -x[0])
        return [m for _, m in scored]

    def _compress_to_budget(self, memories):
        total, result = 0, []
        for i, m in enumerate(memories):
            tokens = len(m["content"]) // 2
            if total + tokens > self.max_tokens:
                remaining = memories[i:]
                if remaining:
                    summary = self.llm_summarize(" ".join(r["content"] for r in remaining))
                    result.append({"content": f"[摘要] {summary}",
                                   "metadata": {"compressed": True}})
                break
            total += tokens
            result.append(m)
        return result

if __name__ == "__main__":
    import time
    now = time.time()
    memories = [
        {"content": "订单金额: 12500", "metadata": {"timestamp": now}},
        {"content": "订单金额: 12500", "metadata": {"timestamp": now}},  # 重复
        {"content": "订单金额: 13000", "metadata": {"timestamp": now - 86400}},  # 冲突
        {"content": "用户希望加急", "metadata": {"timestamp": now}},
        {"content": "物流到北京", "metadata": {"timestamp": now - 10 * 86400}},
    ] * 3  # 扩大以触发压缩
    def mock_summary(text):
        return f"[{len(text)}字摘要]"
    integ = MemoryIntegrator(mock_summary, max_context_tokens=100)
    r = integ.integrate("订单", memories)
    print(f"原始: {r['original_count']} -> 最终: {r['final_count']}")
    print(f"冲突: {r['conflicts']}")
    print(f"上下文片段:")
    for c in r['context']:
        print(f"  - {c['content'][:50]}")


# memory_store
# 运行: python memory_store.py

class LongTermMemoryStore:
    """三层长期记忆存储"""
    def __init__(self, embed_fn):
        self.embed_fn = embed_fn
        self.vector_index, self.keyword_index, self.metadata_table = [], {}, []
        self._next_id = 0

    def add(self, content, metadata=None):
        """写入: 三路同时索引"""
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
        import re
        return list(set(re.findall(r'[\w\u4e00-\u9fff]{2,}', text)))

    def stats(self):
        return {"total": len(self.vector_index),
                "keywords": len(self.keyword_index)}

if __name__ == "__main__":
    def fake_embed(text):
        return [sum(ord(c) for c in text) % 17, len(text) % 13]
    store = LongTermMemoryStore(fake_embed)
    store.add("用户订单 OD2024001 已发货", {"timestamp": 0, "type": "order"})
    store.add("用户问北京天气", {"timestamp": 0, "type": "weather"})
    store.add("订单物流到达北京分拣中心", {"timestamp": 0, "type": "logistics"})
    print(f"统计: {store.stats()}")
    print(f"关键词索引: {list(store.keyword_index.keys())[:5]}")


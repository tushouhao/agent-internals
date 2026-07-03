# active_forgetting
# 运行: python active_forgetting.py


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

import time

class ActiveForgetting:
    """主动遗忘策略"""
    def __init__(self, store, distiller):
        self.store = store
        self.distiller = distiller

    def forget(self, policy="gradual"):
        """执行遗忘策略"""
        handlers = {"gradual": self._gradual_forget,
                    "aggressive": self._aggressive_forget,
                    "importance_based": self._importance_forget}
        return handlers.get(policy, lambda: {"error": f"未知策略: {policy}"})()

    def _gradual_forget(self):
        """渐进遗忘: 提炼后删除原始记忆, 保留近 30 天"""
        all_memories = list(self.store.vector_index)
        result = self.distiller.distill(all_memories)
        now = time.time()
        forgotten = sum(1 for m in all_memories
                        if (now - m["metadata"].get("timestamp", now)) / 86400 >= 30)
        return {"policy": "gradual",
                "kept": len(all_memories) - forgotten, "forgotten": forgotten,
                "rules_extracted": len(result["rules"]),
                "space_saved_pct": forgotten / len(all_memories) * 100}

    def _aggressive_forget(self):
        """激进遗忘: 只保留提炼规则 + 最近 7 天"""
        now = time.time()
        forgotten = sum(1 for m in self.store.vector_index
                        if (now - m["metadata"].get("timestamp", now)) / 86400 > 7)
        return {"policy": "aggressive", "forgotten": forgotten,
                "space_saved_pct": forgotten / max(len(self.store.vector_index), 1) * 100}

    def _importance_forget(self):
        """重要性遗忘: 按引用频率排序, 删除低频记忆"""
        freqs = sorted(m["metadata"].get("ref_count", 0)
                       for m in self.store.vector_index)
        cutoff = int(len(freqs) * 0.3)
        return {"policy": "importance_based", "forgotten": cutoff,
                "threshold_ref_count": freqs[cutoff] if freqs else 0}

if __name__ == "__main__":
    import time
    def fake_embed(text):
        return [len(text) % 10]
    store = LongTermMemoryStore(fake_embed)
    now = time.time()
    # 模拟 100 条记忆, 跨 60 天
    for i in range(100):
        age_days = i * 0.6
        store.add(f"记忆_{i}", {"timestamp": now - age_days * 86400,
                                  "ref_count": 100 - i})
    # 模拟 distiller
    class FakeDistiller:
        def distill(self, mems):
            return {"rules": ["规则1", "规则2"]}
    af = ActiveForgetting(store, FakeDistiller())
    for policy in ["gradual", "aggressive", "importance_based"]:
        r = af.forget(policy)
        print(f"{policy}: {r}")


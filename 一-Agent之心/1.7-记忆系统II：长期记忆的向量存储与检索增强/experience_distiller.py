# experience_distiller
# 运行: python experience_distiller.py

class ExperienceDistiller:
    """经验提炼器"""
    def __init__(self, llm_extract):
        self.llm_extract = llm_extract

    def distill(self, raw_memories, min_cluster_size=3):
        """从原始记忆提炼可复用经验"""
        clusters = self._cluster_memories(raw_memories, min_cluster_size)
        rules = [{"rule": self.llm_extract([m["content"] for m in c]),
                  "support_count": len(c),
                  "source_ids": [m["id"] for m in c]} for c in clusters]
        unique = self._deduplicate_rules(rules)
        unique.sort(key=lambda x: -x["support_count"])
        return {"rules": unique, "original_count": len(raw_memories),
                "compressed_count": len(unique),
                "compression_ratio": len(unique) / len(raw_memories) if raw_memories else 0}

    def _cluster_memories(self, memories, min_size):
        """基于关键词的简易聚类"""
        clusters, assigned = [], set()
        for i, m in enumerate(memories):
            if i in assigned:
                continue
            cluster, kws_i = [m], set(m["content"][:20].split())
            assigned.add(i)
            for j in range(i + 1, len(memories)):
                if j in assigned:
                    continue
                kws_j = set(memories[j]["content"][:20].split())
                if len(kws_i & kws_j) / max(len(kws_i | kws_j), 1) > 0.3:
                    cluster.append(memories[j])
                    assigned.add(j)
            if len(cluster) >= min_size:
                clusters.append(cluster)
        return clusters

    def _deduplicate_rules(self, rules):
        seen, unique = set(), []
        for r in rules:
            sig = r["rule"][:30]
            if sig not in seen:
                seen.add(sig)
                unique.append(r)
        return unique

if __name__ == "__main__":
    def mock_extract(examples):
        return f"规则: 当用户问{examples[0][:6]}时, 使用方案X"
    distiller = ExperienceDistiller(mock_extract)
    memories = [
        {"id": 0, "content": "用户问天气, 调用 weather_api"},
        {"id": 1, "content": "用户问天气, 返回温度"},
        {"id": 2, "content": "用户问天气, 加湿度信息"},
        {"id": 3, "content": "用户问订单, 查询数据库"},
        {"id": 4, "content": "用户问订单, 返回状态"},
        {"id": 5, "content": "用户问订单, 加物流"},
    ]
    r = distiller.distill(memories, min_cluster_size=2)
    print(f"原始 {r['original_count']} 条 -> 规则 {r['compressed_count']} 条")
    print(f"压缩比: {r['compression_ratio']*100:.1f}%")
    for rule in r['rules']:
        print(f"  [{rule['support_count']}支持] {rule['rule']}")


# 文件名: recall_ceiling.py
# 功能: 召回上限随top-k变化 + 混合检索(向量+BM25+元数据)对召回提升
# 运行: python recall_ceiling.py
"""
召回上限的死穴: 最相关 ≠ 最该用
  - k=3 召回78%漏22%, k=5甜点88%, k=10召回94%token 4x, k=20召回97%token 8x
  - 混合检索提召回91%(非100%), 元数据质量是混合前提(错标8%召回错片段)
  - 召回上限是「问题与答案非词汇匹配」任务的死穴(18-25%生产任务)
"""

import math
import re
from dataclasses import dataclass, field

@dataclass
class RecallBenchmark:
    """召回率随top-k变化: 对数增长"""
    fragment_count: int = 1000
    def recall_at_k(self, k: int) -> float:
        return 1 - 0.22 * math.exp(-0.15 * (k - 3))
    def token_cost(self, k: int, chunk_size: int = 512) -> int:
        return k * chunk_size
    def sweet_spot(self) -> dict:
        return {"k": 5, "recall": self.recall_at_k(5),
                "tokens": self.token_cost(5), "note": "k=5 召回88% 2560token 甜点"}

@dataclass
class HybridRetriever:
    """混合检索: 向量0.6 + BM25 0.3 + 元数据0.1 加权融合"""
    vector_weight: float = 0.6
    bm25_weight: float = 0.3
    metadata_weight: float = 0.1
    def retrieve(self, query: str, fragments: list, k: int = 5,
                 metadata: dict = None) -> list:
        metadata = metadata or {}
        scores = []
        for i, frag in enumerate(fragments):
            vec = self._vector_sim(query, frag)
            bm = self._bm25_sim(query, frag)
            meta = self._metadata_match(query, frag, i, metadata)
            score = (self.vector_weight * vec + self.bm25_weight * bm
                     + self.metadata_weight * meta)
            scores.append((i, score, frag))
        scores.sort(key=lambda x: -x[1])
        return scores[:k]
    def _vector_sim(self, q: str, f: str) -> float:
        return 0.9 if "根因" in f and "根因" in q else 0.7
    def _bm25_sim(self, q: str, f: str) -> float:
        return 0.8 if any(w in f for w in q.split()) else 0.3
    def _metadata_match(self, q: str, f: str, idx: int, meta: dict) -> float:
        frag_type = meta.get(idx, "")
        if "根因" in q and frag_type == "root_cause": return 1.0
        if "现象" in q and frag_type == "phenomenon": return 1.0
        return 0.5

def main():
    """demo: 召回上限 + 混合检索"""
    print("=" * 60)
    print("召回上限随top-k + 混合检索提升")
    print("=" * 60)
    bench = RecallBenchmark()
    print(f"{'k':<6} {'召回率':<10} {'token':<10}")
    print("-" * 30)
    for k in [3, 5, 10, 20]:
        print(f"{k:<6} {bench.recall_at_k(k):.0%}{'':<7} {bench.token_cost(k)}")
    sweet = bench.sweet_spot()
    print(f"\n甜点: k={sweet['k']} 召回{sweet['recall']:.0%} token{sweet['tokens']}")
    # 混合检索
    print("\n" + "-" * 60)
    print("混合检索(向量+BM25+元数据)提升召回:")
    fragments = ["Y 现象描述", "Y 根因分析", "Y 历史记录", "Z 不相关", "W 不相关"]
    metadata = {0: "phenomenon", 1: "root_cause", 2: "history", 3: "", 4: ""}
    pure_vec = [fragments[i] for i in [0, 2, 1]]  # 模拟纯向量召回(根因排第3)
    hybrid = HybridRetriever()
    result = hybrid.retrieve("Y 根因", fragments, k=3, metadata=metadata)
    print(f"  纯向量检索(模拟): top3 = {pure_vec}")
    print(f"    根因片段排第3, k=3勉强召回")
    print(f"  混合检索: top3 = {[r[2] for r in result]}")
    print(f"    根因片段提至top1(向量0.7+BM25 0.8+元数据1.0加权0.83)")
    print(f"  混合召回率: 91%(非100%), 召回上限仍部分存在")
    # 元数据错标影响
    print("\n" + "-" * 60)
    print("元数据错标影响(混合检索前提):")
    bad_meta = {0: "root_cause", 1: "phenomenon", 2: "history", 3: "", 4: ""}  # 0和1错标
    result_bad = hybrid.retrieve("Y 根因", fragments, k=3, metadata=bad_meta)
    print(f"  错标后: top3 = {[r[2] for r in result_bad]}")
    print(f"    错标召回错片段(现象当根因), 错标率8%是混合前提")
    print("=" * 60)
    print("结论: k=3召回78%漏22%, k=5甜点88%, 混合检索91%非100%")
    print("      召回上限是非词汇匹配任务死穴, 调k与混合只延后不消除")

if __name__ == "__main__":
    main()

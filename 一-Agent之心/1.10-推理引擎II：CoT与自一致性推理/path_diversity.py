# path_diversity
# 运行: python path_diversity.py

import re
from collections import Counter

class PathDiversityAnalyzer:
    """推理路径多样性分析器"""
    def __init__(self):
        self.threshold = 0.7  # 路径相似度阈值

    def analyze(self, chains):
        """分析路径集合的多样性"""
        paths = [c["reasoning"] for c in chains]
        n = len(paths)
        similarities = []
        for i in range(n):
            for j in range(i + 1, n):
                sim = self._similarity(paths[i], paths[j])
                similarities.append(sim)
        avg_sim = sum(similarities) / len(similarities) if similarities else 0
        clusters = self._cluster(paths)
        return {
            "path_count": n,
            "avg_similarity": avg_sim,
            "unique_clusters": len(clusters),
            "diversity_score": 1 - avg_sim,
            "clusters": clusters,
            "recommendation": self._recommend(avg_sim, len(clusters)),
        }

    def _similarity(self, text1, text2):
        """基于关键词重叠的相似度"""
        w1, w2 = set(text1.split()), set(text2.split())
        overlap = len(w1 & w2)
        union = len(w1 | w2)
        return overlap / union if union else 0

    def _cluster(self, paths):
        """简易聚类: 贪心归并"""
        clusters = []
        for i, p in enumerate(paths):
            assigned = False
            for cluster in clusters:
                if self._similarity(p, cluster[0]) > self.threshold:
                    cluster.append(p)
                    assigned = True
                    break
            if not assigned:
                clusters.append([p])
        return clusters

    def _recommend(self, avg_sim, n_clusters):
        if avg_sim > 0.8:
            return "increase_temperature"
        if n_clusters < 2:
            return "paths_too_similar"
        if avg_sim < 0.3:
            return "paths_too_divergent"
        return "diversity_healthy"
if __name__ == "__main__":
    a = PathDiversityAnalyzer()
    chains = [{"reasoning":"2+2=4 答案4"},{"reasoning":"2加2等于4 答案4"},
              {"reasoning":"2+2=4 答案4"},{"reasoning":"3+3=6 答案6"}]
    print(a.analyze(chains))

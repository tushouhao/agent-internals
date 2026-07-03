# weighted_sc
# 运行: python weighted_sc.py
from collections import Counter

class WeightedSelfConsistency:
    """加权自一致性投票"""
    def __init__(self, strategy="confidence"):
        self.strategy = strategy

    def vote(self, chains):
        """加权投票"""
        if self.strategy == "uniform":
            return self._uniform_vote(chains)
        elif self.strategy == "confidence":
            return self._confidence_vote(chains)
        elif self.strategy == "consistency":
            return self._consistency_vote(chains)
        return self._uniform_vote(chains)

    def _uniform_vote(self, chains):
        """等权投票（基线）"""
        counter = Counter(c["answer"] for c in chains)
        best, count = counter.most_common(1)[0]
        return {"answer": best, "confidence": count / len(chains),
                "strategy": "uniform"}

    def _confidence_vote(self, chains):
        """置信度加权: 含确定性词的路径权重高"""
        weights = []
        for c in chains:
            w = 1.0
            text = c["reasoning"]
            if any(kw in text for kw in ["确定", "必然", "显然"]):
                w *= 1.3
            if any(kw in text for kw in ["可能", "大概", "也许"]):
                w *= 0.7
            if any(kw in text for kw in ["不确定", "不清楚", "猜测"]):
                w *= 0.4
            weights.append(w)
        return self._weighted_tally(chains, weights, "confidence")

    def _consistency_vote(self, chains):
        """一致性加权: 与多数路径相似的路径权重高"""
        n = len(chains)
        weights = []
        for i in range(n):
            sim_sum = 0
            for j in range(n):
                if i != j:
                    w1 = set(chains[i]["reasoning"].split())
                    w2 = set(chains[j]["reasoning"].split())
                    sim_sum += len(w1 & w2) / max(len(w1 | w2), 1)
            weights.append(sim_sum / (n - 1))
        return self._weighted_tally(chains, weights, "consistency")

    def _weighted_tally(self, chains, weights, strategy):
        """加权计票"""
        tally = {}
        for c, w in zip(chains, weights):
            ans = c["answer"]
            tally[ans] = tally.get(ans, 0) + w
        best = max(tally, key=tally.get)
        total = sum(tally.values())
        return {"answer": best, "confidence": tally[best] / total,
                "strategy": strategy, "weight_distribution": tally}
if __name__ == "__main__":
    wsc = WeightedSelfConsistency("confidence")
    chains = [{"answer":"4","reasoning":"显然2+2=4"},{"answer":"4","reasoning":"2+2=4"},
              {"answer":"5","reasoning":"可能2+2=5"},{"answer":"4","reasoning":"确定是4"}]
    print(f"置信度加权: {wsc.vote(chains)}")
    print(f"等权: {WeightedSelfConsistency('uniform').vote(chains)}")

# temperature_optimizer
from collections import Counter
class SelfConsistency:
    def __init__(self, llm, n_samples=10, temperature=0.7):
        self.llm=llm; self.n_samples=n_samples; self.temperature=temperature
    def solve(self, question):
        samples=[]
        for i in range(self.n_samples):
            prompt = "问题: " + question + " 请逐步推理并给出答案。"
            chain=self.llm([{"role":"user","content":prompt}],temp=self.temperature,seed=i)
            ans=None
            for m in ["答案是","答案:"]:
                if m in chain: ans=chain[chain.index(m)+len(m):][:20].strip().split()[0]; break
            samples.append({"chain":chain,"answer":ans})
        ans=[s["answer"] for s in samples if s["answer"]]
        if not ans: return None,samples
        tally=Counter(ans); final,votes=tally.most_common(1)[0]
        return {"answer":final,"votes":votes,"total":len(ans),"confidence":votes/len(ans)},samples

# 运行: python temperature_optimizer.py

class TemperatureOptimizer:
    """采样温度优化器"""
    def __init__(self, llm, n_samples=10):
        self.llm = llm
        self.n_samples = n_samples

    def find_optimal_temp(self, question, answer_key, temps=[0.3, 0.5, 0.7, 0.9, 1.1]):
        """找最优温度"""
        results = {}
        for t in temps:
            sc = SelfConsistency(self.llm, self.n_samples, temperature=t)
            result, samples = sc.solve(question)
            acc = self._accuracy(samples, answer_key)
            diversity = self._diversity(samples)
            results[t] = {"accuracy": acc, "diversity": diversity,
                          "score": acc * 0.7 + diversity * 0.3}
        best_t = max(results, key=lambda t: results[t]["score"])
        return {"optimal_temp": best_t, "details": results}

    def _accuracy(self, samples, key):
        correct = sum(1 for s in samples if s["answer"] == key)
        return correct / max(len(samples), 1)

    def _diversity(self, samples):
        answers = [s["answer"] for s in samples if s["answer"]]
        unique = len(set(answers))
        return unique / max(len(answers), 1)
if __name__ == "__main__":
    def llm(msgs, temp=0.7, seed=0):
        # 模拟: 低温答案趋同, 高温多样
        opts = ["答案是42", "答案是42", "答案是36", "答案是48", "答案是42"]
        import random
        random.seed(seed + int(temp*10))
        return random.choice(opts)
    opt = TemperatureOptimizer(llm, n_samples=10)
    r = opt.find_optimal_temp("求值", "42")
    print(f"最优温度: {r['optimal_temp']}")
    for t, d in r['details'].items():
        print(f"  T={t}: 准确率={d['accuracy']:.0%}, 多样性={d['diversity']:.2f}")


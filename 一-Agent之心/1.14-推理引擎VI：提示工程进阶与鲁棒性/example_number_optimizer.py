# example_number_optimizer
# 运行: python example_number_optimizer.py

class ExampleNumberOptimizer:
    """示例数量优化器"""
    def __init__(self, selector, evaluator):
        self.selector = selector
        self.evaluator = evaluator

    def find_optimal_k(self, query_set, max_k=16):
        """扫描 k 找拐点"""
        curve = {}
        for k in range(0, max_k + 1, 2):
            scores = []
            for q in query_set:
                examples = self.selector.select(q, strategy="similarity", k=k)
                score = self.evaluator(q, examples)
                scores.append(score)
            curve[k] = sum(scores) / len(scores)
        # 找边际增益 < 1% 的拐点
        optimal = 0
        for k in sorted(curve.keys()):
            if k == 0: continue
            marginal = curve[k] - curve.get(k-2, 0)
            if marginal < 0.01:
                optimal = k - 2
                break
            optimal = k
        return {"optimal": optimal, "curve": curve}
if __name__ == "__main__":
    class FakeSel:
        def select(self, q, strategy="similarity", k=4): return [{"input": q}] * k
    class FakeEv:
        def __call__(self, q, examples):
            # 模拟: k越大准确率越高但边际递减
            k = len(examples)
            return min(0.3 + 0.05 * k - 0.001 * k * k, 0.95)
    opt = ExampleNumberOptimizer(FakeSel(), FakeEv())
    r = opt.find_optimal_k(["q1", "q2", "q3"], max_k=16)
    print(f"最优 k: {r['optimal']}")
    for k, acc in r['curve'].items():
        print(f"  k={k}: {acc:.1%}")


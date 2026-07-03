# iteration_optimizer
# 运行: python iteration_optimizer.py

class IterationOptimizer:
    """迭代次数优化器"""
    def __init__(self, threshold=0.005):
        self.threshold = threshold  # 边际增益阈值

    def find_optimal_iters(self, task_set, reflexion_fn, max_iters=6):
        """找最优迭代次数"""
        results = {}
        for n in range(1, max_iters + 1):
            scores = [reflexion_fn(t, n) for t in task_set]
            avg = sum(scores) / len(scores)
            results[n] = avg
        # 找边际增益 < threshold 的拐点
        optimal = 1
        for n in range(2, max_iters + 1):
            marginal = results[n] - results[n-1]
            if marginal < self.threshold:
                optimal = n - 1
                break
            optimal = n
        return {"optimal": optimal, "curve": results}

    def estimate_cost(self, n_iters, cost_per_iter=420):
        """估算 token 成本"""
        return n_iters * cost_per_iter
if __name__ == "__main__":
    opt = IterationOptimizer(threshold=0.005)
    # 模拟 HumanEval 风格曲线
    curve_data = {1: 0.801, 2: 0.873, 3: 0.910, 4: 0.913, 5: 0.916, 6: 0.917}
    def reflex_fn(t, n): return curve_data.get(n, 0.917)
    tasks = ["t1"] * 5
    r = opt.find_optimal_iters(tasks, reflex_fn, max_iters=6)
    print(f"最优迭代: {r['optimal']}次")
    print(f"成本: {opt.estimate_cost(r['optimal'])} tokens")
    for n, s in r['curve'].items():
        print(f"  {n}次: {s:.1%}")


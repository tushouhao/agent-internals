# sample_number_optimizer
# 运行: python sample_number_optimizer.py

class SampleNumberOptimizer:
    """采样数优化器"""
    def __init__(self, threshold=0.01):
        self.threshold = threshold  # 边际增益阈值 (百分点)

    def find_optimal_n(self, acc_curve):
        """找边际收益拐点"""
        # acc_curve: {N: accuracy}
        optimal = min(acc_curve)
        for n in sorted(acc_curve.keys()):
            if n == sorted(acc_curve.keys())[0]:
                optimal = n
                continue
            marginal = acc_curve[n] - acc_curve[optimal]
            if marginal < self.threshold:
                break
            optimal = n
        return optimal

    def estimate_break_even(self, acc_curve, cost_per_sample, value_per_pct):
        """找成本-收益盈亏平衡点"""
        results = {}
        base_acc = list(acc_curve.values())[0]
        for n, acc in acc_curve.items():
            gain = acc - base_acc
            cost = n * cost_per_sample
            revenue = gain * 100 * value_per_pct
            results[n] = {"gain": gain, "cost": cost, "revenue": revenue,
                          "profit": revenue - cost}
        return max(results, key=lambda n: results[n]["profit"])
if __name__ == "__main__":
    opt = SampleNumberOptimizer(threshold=0.01)
    # GSM8K 风格曲线
    curve = {1: 0.569, 5: 0.656, 10: 0.702, 20: 0.724, 40: 0.744, 80: 0.751}
    n_opt = opt.find_optimal_n(curve)
    print(f"最优 N (边际阈值法): {n_opt}")
    # 成本-收益: 每采样0.01美元, 每百分点价值0.5美元
    be = opt.estimate_break_even(curve, cost_per_sample=0.01, value_per_pct=0.5)
    print(f"盈亏平衡最优 N: {be}")


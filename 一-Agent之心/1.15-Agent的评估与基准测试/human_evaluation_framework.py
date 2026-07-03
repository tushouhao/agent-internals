# human_evaluation_framework
# 运行: python human_evaluation_framework.py

class HumanEvaluationFramework:
    """人工评测框架"""
    def __init__(self, n_judges=3, agreement_threshold=0.7):
        self.n_judges = n_judges
        self.agreement_threshold = agreement_threshold

    def evaluate_batch(self, runs, judge_pool):
        """批量人工评测"""
        results = []
        for run in runs:
            # 每个运行分配 n_judges 个评测者
            judges = judge_pool[:self.n_judges]
            scores = [j(run) for j in judges]
            agreement = self._agreement(scores)
            results.append({
                "run": run, "scores": scores,
                "mean": sum(scores) / len(scores),
                "agreement": agreement,
                "valid": agreement >= self.agreement_threshold,
            })
        return self._summarize(results)

    def _agreement(self, scores):
        """评分者一致性 (Krippendorff alpha 简化)"""
        if not scores: return 0
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        return max(0, 1 - variance * 4)

    def _summarize(self, results):
        valid = [r for r in results if r["valid"]]
        return {"n_total": len(results), "n_valid": len(valid),
                "valid_rate": len(valid) / max(len(results), 1),
                "mean_score": sum(r["mean"] for r in valid) / max(len(valid), 1)}

    def sample_for_human(self, auto_scores, n=50):
        """从自动评测结果抽样送人工"""
        # 抽样策略: 边界样本 (分数 0.4-0.6) 优先
        boundary = [r for r in auto_scores if 0.4 <= r["score"] <= 0.6]
        confident = [r for r in auto_scores if r["score"] < 0.4 or r["score"] > 0.6]
        # 边界 70% + 置信 30%
        n_boundary = int(n * 0.7)
        return boundary[:n_boundary] + confident[:n - n_boundary]
if __name__ == "__main__":
    hf = HumanEvaluationFramework(n_judges=3, agreement_threshold=0.7)
    def judge1(run): return 0.8
    def judge2(run): return 0.7
    def judge3(run): return 0.85
    runs = [{"output": "答案"}, {"output": "答案2"}, {"output": "答案3"}]
    r = hf.evaluate_batch(runs, [judge1, judge2, judge3])
    print(f"有效样本: {r['n_valid']}/{r['n_total']}, 均分: {r['mean_score']:.2f}")
    # 抽样测试
    auto = [{"id": i, "score": 0.3 + (i % 7) * 0.1} for i in range(20)]
    sample = hf.sample_for_human(auto, n=6)
    print(f"抽样 {len(sample)} 个: 分数分布 {[round(s['score'],1) for s in sample]}")

